
"""
Main entry point for the TaskFlow API.

This module creates the FastAPI application, registers API routers,
and defines general application endpoints such as the health check.
"""

from fastapi import FastAPI

from app.api.routes.jobs import router as jobs_router


# Create the main FastAPI application instance.
app = FastAPI(
    title="TaskFlow API",
    description="A distributed job processing and workflow automation system.",
    version="0.1.0"
)


# Register the job management routes with the application.
app.include_router(jobs_router)


@app.get("/health", tags=["Health"])
def health_check():
    """
    Check whether the TaskFlow API is responding.

    Returns:
        A simple status message confirming the API is running.
    """

    return {"status": "healthy"}
