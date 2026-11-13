
"""
API routes for managing TaskFlow jobs.

This module exposes HTTP endpoints for creating jobs and
retrieving existing jobs from the PostgreSQL database.

The routes use Pydantic schemas to validate requests and format
responses, and SQLAlchemy sessions to interact with the database.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.models.job import Job
from app.schemas.job import JobCreate, JobResponse


# Creates a router to group all job-related endpoints.
router = APIRouter(
    prefix="/jobs",
    tags=["Jobs"]
)


@router.post(
    "",
    response_model=JobResponse,
    status_code=status.HTTP_201_CREATED
)
def create_job(
    job_data: JobCreate,
    db: Session = Depends(get_db)
):
    """
    Create a new job and save it to PostgreSQL.

    Args:
        job_data: Validated job information provided by the client.
        db: Database session provided by FastAPI dependency injection.

    Returns:
        The newly created job, including its generated ID and status.
    """

    # Convert the validated request data into a SQLAlchemy model.
    new_job = Job(
        job_type=job_data.job_type,
        payload=job_data.payload,
        max_retries=job_data.max_retries
    )

    # Add the new job to the current database session.
    db.add(new_job)

    # Commit the transaction to permanently save the job.
    db.commit()

    # Refresh the object to load database-generated values.
    db.refresh(new_job)

    return new_job


@router.get(
    "",
    response_model=list[JobResponse]
)
def get_jobs(db: Session = Depends(get_db)):
    """
    Retrieve all jobs stored in PostgreSQL.

    Args:
        db: Database session provided by FastAPI.

    Returns:
        A list of jobs.
    """

    # Build a query that selects every job.
    query = select(Job)

    # Execute the query and return all matching records.
    jobs = db.scalars(query).all()

    return jobs


@router.get(
    "/{job_id}",
    response_model=JobResponse
)
def get_job(
    job_id: str,
    db: Session = Depends(get_db)
):
    """
    Retrieve one job using its unique ID.

    Args:
        job_id: UUID of the requested job.
        db: Database session provided by FastAPI.

    Returns:
        The matching job.

    Raises:
        HTTPException: If no job exists with the supplied ID.
    """

    # Build a query that searches for the requested job ID.
    query = select(Job).where(Job.id == job_id)

    # Execute the query and retrieve one matching job, if available.
    job = db.scalar(query)

    # Return HTTP 404 if the requested job does not exist.
    if job is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Job not found"
        )

    return job
