from datetime import datetime

from sqlalchemy import DateTime, String, Text, func
from sqlalchemy.orm import relationship  # Import relationship
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class ContactSubmission(Base):
    __tablename__ = "contact_submissions"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    email: Mapped[str] = mapped_column(String(255), nullable=False)
    subject: Mapped[str] = mapped_column(String(150), nullable=False)
    message: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )
    
# Relationship to see all follow-up requests
    follow_ups = relationship("FollowUpRequest", back_populates="original_submission")

    def __repr__(self):
        return f"<ContactSubmission(id={self.id}, email='{self.email}')>"