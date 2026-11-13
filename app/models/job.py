
"""
SQLAlchemy model for TaskFlow jobs.

This module defines the structure of the jobs table in PostgreSQL.
Each record represents one job submitted to the TaskFlow API.

A job stores its input, current execution status, output, retry
configuration, and timestamps. It can also have multiple execution
attempts, which are represented by the JobAttempt model.
"""

import uuid
from datetime import datetime, timezone

from sqlalchemy import DateTime, Integer, JSON, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.database import Base


class Job(Base):
    """
    Represents a job record in the database.

    Each job has a unique UUID, a task type, input payload, execution
    status, optional result, retry limit, and timestamps.

    The attempts relationship connects a job to its execution history.
    """

    # Name of the PostgreSQL table represented by this model.
    __tablename__ = "jobs"

    # Unique identifier for each job.
    # A UUID is generated automatically when a new job is created.
    id: Mapped[str] = mapped_column(
        String(36),
        primary_key=True,
        default=lambda: str(uuid.uuid4())
    )

    # Identifies the type of task to execute, such as document_processing.
    job_type: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )

    # Stores the input data required to execute the job as JSON.
    payload: Mapped[dict] = mapped_column(
        JSON,
        nullable=False
    )

    # Tracks the current lifecycle state of the job.
    # A newly created job starts in the PENDING state.
    status: Mapped[str] = mapped_column(
        String(20),
        default="PENDING",
        nullable=False
    )

    # Stores the output produced by the worker after execution.
    # This remains NULL until a result is available.
    result: Mapped[dict | None] = mapped_column(
        JSON,
        nullable=True
    )

    # Maximum number of execution retries permitted for this job.
    max_retries: Mapped[int] = mapped_column(
        Integer,
        default=3,
        nullable=False
    )

    # Records when the job was first created.
    # The timestamp is generated using UTC.
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False
    )

    # Records the most recent time the job was updated.
    # onupdate refreshes this timestamp when SQLAlchemy updates the record.
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
        nullable=False
    )

    # Defines the one-to-many relationship between jobs and job attempts.
    # One job can have multiple attempts; each attempt belongs to one job.
    attempts: Mapped[list["JobAttempt"]] = relationship(
        back_populates="job"
    )
