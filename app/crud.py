from datetime import datetime, timedelta, timezone
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.contact_submission import ContactSubmission


async def get_initial_submission_by_email(
    db: AsyncSession, email: str
) -> ContactSubmission | None:
    """
    Finds the initial contact submission for a given email address.
    """
    stmt = select(ContactSubmission).where(ContactSubmission.email == email)
    result = await db.execute(stmt)
    return result.scalars().first()
