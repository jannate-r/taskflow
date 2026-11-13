
"""
SQLAlchemy model for TaskFlow job execution attempts.

This module defines the job_attempts table in PostgreSQL.

Whenever a worker tries to execute a job, an attempt record can
track that execution. This preserves execution history, including
attempt numbers, statuses, errors, and timestamps.
"""

from datetime import datetime, timezone

from sqlalchemy import DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.database import Base


class JobAttempt(Base):
    """
    Represents one execution attempt for a job.

    A job may have multiple attempts if its execution fails and
    the worker retries it.

    Each attempt belongs to exactly one parent Job.
    """

    # Name of the PostgreSQL table represented by this model.
    __tablename__ = "job_attempts"

    # Unique identifier for each execution attempt.
    # PostgreSQL generates the integer ID automatically.
    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True
    )

    # Foreign key connecting this attempt to its parent job.
    # References the id column in the jobs table.
    job_id: Mapped[str] = mapped_column(
        String(36),
        ForeignKey("jobs.id"),
        nullable=False
    )

    # Indicates which attempt this is for the parent job.
    # For example, 1 represents the first execution attempt.
    attempt_number: Mapped[int] = mapped_column(
        Integer,
        nullable=False
    )

    # Tracks the outcome of this individual execution attempt.
    # A newly created attempt starts in the RUNNING state.
    status: Mapped[str] = mapped_column(
        String(20),
        default="RUNNING",
        nullable=False
    )

    # Stores error details if this particular attempt fails.
    # Remains NULL when no error has occurred.
    error_message: Mapped[str | None] = mapped_column(
        Text,
        nullable=True
    )

    # Records when this execution attempt started.
    started_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False
    )

    # Records when this execution attempt finished.
    # Remains NULL while the attempt is still running.
    completed_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True
    )

    # Defines the many-to-one relationship to the parent Job.
    # Connects to the attempts relationship in the Job model.
    job: Mapped["Job"] = relationship(
        back_populates="attempts"
    )
