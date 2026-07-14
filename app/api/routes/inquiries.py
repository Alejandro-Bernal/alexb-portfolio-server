import logging
from typing import cast
from datetime import datetime, timedelta, timezone
from fastapi import APIRouter, Depends, HTTPException, status, Request
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models.contact import ContactForm
from app.models.contact_submission import ContactSubmission
from app.models.follow_up_request import FollowUpRequest  # Import the new model
from app.services.email import EmailSendError, send_contact_email
from app.crud import get_initial_submission_by_email  # Use the renamed function
from app.security import get_api_key
from app.limiter import limiter

log = logging.getLogger(__name__)

router = APIRouter(prefix="/contact", tags=["contact"])

class ContactResponse(BaseModel):
    id: int
    created_at: str
    email_id: str
    is_follow_up: bool  # Add a field to indicate if it was a follow-up


@router.post("", status_code=status.HTTP_201_CREATED, response_model=ContactResponse)
@limiter.limit("1/hour")
async def submit_contact(
    request: Request,
    form: ContactForm,
    db: AsyncSession = Depends(get_db),
    _api_key: str = Depends(get_api_key),
) -> ContactResponse:
    initial_submission = await get_initial_submission_by_email(db, email=str(form.email))

    if initial_submission:
        # User has submitted before. Check the timestamp.
        time_since_submission = datetime.now(timezone.utc) - initial_submission.created_at
        if time_since_submission < timedelta(hours=1):
            # It has been less than 1 hour. Reject the request.
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail="You have submitted a message recently. Please wait at least 1 hour before sending a follow-up.",
            )

        # It has been more than 1 hour. Create a follow-up request.
        new_submission = FollowUpRequest(
            name=form.name,
            email=str(form.email),
            subject=form.subject,
            message=form.message,
            original_submission_id=cast(int, initial_submission.id),
        )
        is_follow_up = True

    else:
        # This is a new user. Create an initial contact submission.
        new_submission = ContactSubmission(
            name=form.name,
            email=str(form.email),
            subject=form.subject,
            message=form.message,
        )
        is_follow_up = False

    db.add(new_submission)

    try:
        email_id = await send_contact_email(form)
    except EmailSendError as exc:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=str(exc),
        ) from exc

    await db.commit()
    await db.refresh(new_submission)
    
    log.info(
        "contact_submission_processed",
        extra={
            "submission_id": cast(int, new_submission.id),
            "is_follow_up": is_follow_up,
            "email": str(form.email),
        },
    )

    return ContactResponse(
        id=cast(int, new_submission.id),
        created_at=new_submission.created_at.isoformat(),
        email_id=email_id,
        is_follow_up=is_follow_up,
    )