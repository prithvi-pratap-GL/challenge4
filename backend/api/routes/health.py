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


@router.get("/status")
async def service_status():
    """Service status endpoint."""
    return {
        "status": "running",
        "service": "venturemind-ai",
        "features": [
            "Startup analysis",
            "Research intelligence",
            "Knowledge extraction",
            "Agent analysis",
            "Committee decision",
            "Scenario simulation"
        ]
    }
