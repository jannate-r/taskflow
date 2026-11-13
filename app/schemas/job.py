
"""
Pydantic schemas for TaskFlow jobs.

These schemas define the data accepted by the API when a client
creates a job and the data returned when a job is retrieved.

Unlike SQLAlchemy models, these classes are responsible for
validating and serializing API data, not storing database records.
"""

from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict, Field


class JobCreate(BaseModel):
    """
    Validates the data required to create a new job.

    The client provides the job type and input payload.
    max_retries is optional and defaults to 3.
    """

    # Identifies the type of task the worker should execute.
    job_type: str = Field(..., min_length=1, max_length=100)

    # Contains the input data required to execute the job.
    payload: dict[str, Any]

    # Maximum number of retries allowed if execution fails.
    max_retries: int = Field(default=3, ge=0, le=10)


class JobResponse(BaseModel):
    """
    Defines the structure of a job returned by the API.

    Includes fields generated or maintained by the application,
    such as the job ID, status, result, and timestamps.
    """

    # Allows Pydantic to read values directly from SQLAlchemy objects.
    model_config = ConfigDict(from_attributes=True)

    # Unique identifier generated when the job is created.
    id: str

    # Original task type and input data.
    job_type: str
    payload: dict[str, Any]

    # Current execution state and output, if available.
    status: str
    result: dict[str, Any] | None

    # Retry configuration.
    max_retries: int

    # Automatically maintained timestamps.
    created_at: datetime
    updated_at: datetime
