"""
VentureMind AI — FastAPI Application Entrypoint
Main application factory and configuration.

Initializes the FastAPI server with all middleware, routes, and dependencies.
Ready for production deployment.
"""

import logging
from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from backend.api.routes import scoring_router
# NEW: Import the ingestion router directly from the file
from backend.api.routes.ingestion import router as ingestion_router

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

# ============================================================================
# FastAPI Application Factory
# ============================================================================

app = FastAPI(
    title="VentureMind AI API",
    description="Deterministic startup evaluation and investment recommendation engine",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
)

# ============================================================================
# Middleware Configuration
# ============================================================================

# CORS Middleware - Allow all origins for demo
# Production: Restrict to specific origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins (frontend during demo)
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)

logger.info("✓ CORS middleware configured")

# ============================================================================
# Router Registration
# ============================================================================

app.include_router(scoring_router)
logger.info("✓ Scoring router registered: /api/v1/scoring")

# NEW: Mount the ingestion router
app.include_router(ingestion_router)
logger.info("✓ Ingestion router registered: /api/v1/ingest")

# ============================================================================
# Static Files Configuration
# ============================================================================

uploads_dir = Path("storage/uploads")
if uploads_dir.exists():
    app.mount("/uploads", StaticFiles(directory=str(uploads_dir)), name="uploads")
    logger.info("✓ Static file serving mounted: /uploads → storage/uploads/")
else:
    logger.warning(f"⚠ Uploads directory not found: {uploads_dir.absolute()}")

# ============================================================================
# Health Check Endpoint
# ============================================================================

@app.get(
    "/health",
    tags=["Health"],
    summary="API Health Check",
    description="Verify that the API is running and operational.",
    response_model=dict,
)
async def api_health() -> dict:
    """
    Health check endpoint for the entire API.

    Returns:
        Dictionary with API status and version information.
    """
    logger.debug("[GET /health] Health check")
    return {
        "status": "healthy",
        "service": "venturemind-api",
        "version": "1.0.0",
    }


# ============================================================================
# Startup Event
# ============================================================================

@app.on_event("startup")
async def startup_event():
    """
    Called when the application starts up.

    Logs initialization messages for debugging.
    """
    logger.info("=" * 80)
    logger.info("VentureMind AI API Starting Up")
    logger.info("=" * 80)
    logger.info("API Documentation available at: /docs")
    logger.info("Alternative docs available at: /redoc")
    logger.info("OpenAPI schema available at: /openapi.json")
    logger.info("=" * 80)


# ============================================================================
# Shutdown Event
# ============================================================================

@app.on_event("shutdown")
async def shutdown_event():
    """
    Called when the application shuts down.

    Logs shutdown messages for debugging.
    """
    logger.info("=" * 80)
    logger.info("VentureMind AI API Shutting Down")
    logger.info("=" * 80)


# ============================================================================
# Running the Application
# ============================================================================

if __name__ == "__main__":
    import uvicorn

    logger.info("Starting Uvicorn server...")
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info",
    )