from datetime import datetime
from sqlalchemy import (
    Column,
    DateTime,
    ForeignKey,
    Integer,
    String,
    Text,
    func,
)
from sqlalchemy.orm import relationship
from app.database import Base


class FollowUpRequest(Base):
    __tablename__ = "follow_up_requests"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    email = Column(String, index=True, nullable=False)
    subject = Column(String, nullable=False)
    message = Column(Text, nullable=False)
    created_at = Column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    # Foreign Key to link to the original submission
    original_submission_id = Column(
        Integer, ForeignKey("contact_submissions.id"), nullable=False
    )

    # Relationship to access the original submission object
    original_submission = relationship("ContactSubmission", back_populates="follow_ups")

    def __repr__(self):
        return f"<FollowUpRequest(id={self.id}, subject='{self.subject}')>"
