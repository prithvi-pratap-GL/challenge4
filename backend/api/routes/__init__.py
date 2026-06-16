"""
VentureMind AI — API Routes
HTTP endpoint definitions for all API services.
"""

from backend.api.routes.scoring import router as scoring_router

__all__ = ["scoring_router"]
