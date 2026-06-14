"""FastAPI application entry point."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import os

from backend.api.routes import health, analysis


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifecycle."""
    print("Starting VentureMind AI API")
    yield
    print("Shutting down VentureMind AI API")


app = FastAPI(
    title="VentureMind AI",
    description="AI Venture Capital Analyst Platform",
    version="1.0.0",
    lifespan=lifespan,
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routes
app.include_router(health.router, prefix="/api/v1", tags=["Health"])
app.include_router(analysis.router, prefix="/api/v1", tags=["Analysis"])


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "message": "VentureMind AI Backend",
        "version": "1.0.0",
        "docs": "/docs",
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        reload=os.getenv("DEBUG", "False") == "True",
    )
