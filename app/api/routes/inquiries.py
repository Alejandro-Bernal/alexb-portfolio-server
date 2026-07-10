from fastapi import APIRouter, Depends, HTTPException, status, Request
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models.contact import ContactForm
from app.models.contact_submission import ContactSubmission
from app.services.email import EmailSendError, send_contact_email
from app.crud import get_submission_by_email
from app.security import get_api_key
from app.limiter import limiter

router = APIRouter(prefix="/contact", tags=["contact"])


class ContactResponse(BaseModel):
    id: int
    created_at: str
    email_id: str


@router.post("", status_code=status.HTTP_201_CREATED, response_model=ContactResponse)
@limiter.limit("5/hour")  # Limit to 5 requests per hour per IP
async def submit_contact(
    request: Request,
    form: ContactForm,
    db: AsyncSession = Depends(get_db),
    _api_key: str = Depends(get_api_key),
) -> ContactResponse:
    # check if email exists in the database
    existing_submission = await get_submission_by_email(db, email=form.email)
    if existing_submission:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="A submission with this email address already exists. If you need to follow up, please contact us directly.",
        )
        
    submission = ContactSubmission(
        name=form.name,
        email=str(form.email),
        subject=form.subject,
        message=form.message,
    )
    db.add(submission)

    try:
        email_id = await send_contact_email(form)
    except EmailSendError as exc:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=str(exc),
        ) from exc

    await db.commit()
    await db.refresh(submission)

    return ContactResponse(
        id=submission.id,
        created_at=submission.created_at.isoformat(),
        email_id=email_id,
    )