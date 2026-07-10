from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import EmailStr
from typing import Optional

from app.models.contact_submission import ContactSubmission

async def get_submission_by_email(db: AsyncSession, email: EmailStr) -> Optional[ContactSubmission]:
    result = await db.execute(select(ContactSubmission).where(ContactSubmission.email == str(email)))
    
    return result.scalars().first()
