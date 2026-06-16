"""
VentureMind AI — Scoring API Routes
HTTP endpoints for startup evaluation and investment recommendations.

Follows REST conventions and DDD principles: routes handle HTTP only,
delegate all business logic to the Service layer.
"""

import logging
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field

from backend.api.dependencies import get_scoring_service
from backend.domain.interfaces import IScoringEngine
from backend.domain.schemas import InvestmentRecommendation

logger = logging.getLogger(__name__)

# Create router
router = APIRouter(
    prefix="/api/v1/scoring",
    tags=["Scoring"],
    responses={
        500: {"description": "Internal server error during evaluation"},
        400: {"description": "Invalid request parameters"},
    },
)


class ScoringRequest(BaseModel):
    """Request payload for startup evaluation."""

    deal_id: str = Field(
        ...,
        description="Unique identifier for the deal/startup to evaluate",
        examples=["startup_xyz123"],
    )

    class Config:
        json_schema_extra = {
            "example": {
                "deal_id": "startup_abc789"
            }
        }


class ErrorResponse(BaseModel):
    """Standard error response payload."""

    status: str = Field(..., description="Error status")
    message: str = Field(..., description="Error message")
    detail: Optional[str] = Field(None, description="Additional details")


@router.post(
    "/evaluate",
    response_model=InvestmentRecommendation,
    status_code=200,
    summary="Evaluate a Startup",
    description="Evaluates a startup across 5 investment categories (Team, Market, Product, Financial, Risk) and produces an investment recommendation.",
)
async def evaluate_startup(
    request: ScoringRequest,
    service: IScoringEngine = Depends(get_scoring_service),
) -> InvestmentRecommendation:
    """
    Evaluate a startup and produce an investment recommendation.

    **Request:**
    - `deal_id` (str, required): The unique identifier for the startup to evaluate.

    **Response:**
    Returns an `InvestmentRecommendation` containing:
    - `deal_id`: The evaluated startup
    - `status`: Investment recommendation (INVEST, WATCHLIST, PASS)
    - `reasoning`: Executive summary of the recommendation
    - `category_scores`: Detailed scores for Team, Market, Product, Financial, Risk

    **Scoring Logic:**
    - **INVEST**: All core categories > 75 AND risk < 40
    - **WATCHLIST**: 2+ core categories > 60 AND risk < 60
    - **PASS**: Otherwise

    **Example Request:**
    ```json
    {
        "deal_id": "startup_xyz123"
    }
    ```

    **Example Response:**
    ```json
    {
        "deal_id": "startup_xyz123",
        "status": "invest",
        "reasoning": "Strong team, market, and product with healthy financials.",
        "category_scores": [
            {
                "category": "team",
                "aggregate_score": 85,
                "factors": [...]
            }
        ]
    }
    ```

    **Error Responses:**
    - 400: Invalid request (missing deal_id)
    - 500: Server error during evaluation

    Args:
        request: ScoringRequest containing deal_id
        service: Injected IScoringEngine (DeterministicScoringService)

    Returns:
        InvestmentRecommendation: Complete evaluation result

    Raises:
        HTTPException: 400 for validation errors, 500 for server errors
    """
    logger.info(f"[POST /api/v1/scoring/evaluate] Received evaluation request: deal_id={request.deal_id}")

    # Validate request
    if not request.deal_id or not request.deal_id.strip():
        logger.warning("Invalid request: deal_id is empty")
        raise HTTPException(
            status_code=400,
            detail="deal_id is required and cannot be empty",
        )

    try:
        # Delegate to service layer
        logger.info(f"  Invoking scoring service for deal_id={request.deal_id}")
        recommendation = await service.evaluate_startup(request.deal_id)

        logger.info(
            f"  ✓ Evaluation complete: status={recommendation.status.value} "
            f"deal_id={recommendation.deal_id}"
        )

        return recommendation

    except ValueError as e:
        # Validation error from service layer
        logger.warning(f"  ✗ Validation error: {e}")
        raise HTTPException(
            status_code=400,
            detail=f"Validation error: {str(e)}",
        )

    except RuntimeError as e:
        # Service layer errors (retrieval, LLM, etc.)
        logger.error(f"  ✗ Service error: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Service error: {str(e)}",
        )

    except Exception as e:
        # Unexpected errors
        logger.error(f"  ✗ Unexpected error: {type(e).__name__}: {e}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=f"Unexpected error: {type(e).__name__}",
        )


@router.get(
    "/health",
    response_model=dict,
    status_code=200,
    summary="Health Check",
    description="Verify that the scoring service is operational.",
)
async def health_check() -> dict:
    """
    Health check endpoint for the scoring API.

    Returns:
        Dictionary with status information.
    """
    logger.debug("[GET /api/v1/scoring/health] Health check")
    return {
        "status": "healthy",
        "service": "scoring",
        "version": "1.0",
    }
