from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models.contact import ContactForm
from app.models.contact_submission import ContactSubmission
from app.services.email import EmailSendError, send_contact_email

router = APIRouter(prefix="/contact", tags=["contact"])


class ContactResponse(BaseModel):
    id: int
    created_at: str
    email_id: str


@router.post("", status_code=status.HTTP_201_CREATED, response_model=ContactResponse)
async def submit_contact(
    form: ContactForm,
    db: AsyncSession = Depends(get_db),
) -> ContactResponse:
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