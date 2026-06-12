"""Health check endpoints.

Person 5 owns this module.
"""

from fastapi import APIRouter

router = APIRouter()


@router.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "service": "venturemind-ai"}


@router.get("/ready")
async def readiness_check():
    """Readiness check endpoint."""
    return {"status": "ready", "service": "venturemind-ai"}
