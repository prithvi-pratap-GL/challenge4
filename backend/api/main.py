"""
FastAPI Backend for VentureMind AI
Exposes Person 2's research workflow to frontend
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import json
from datetime import datetime

from backend.agents.research.workflow import ResearchWorkflow
from backend.contracts.startup import StartupInput
from backend.contracts.research import ResearchOutput, Founder, Competitor

# Initialize FastAPI
app = FastAPI(
    title="VentureMind AI - Research Intelligence",
    description="Person 2's Research Intelligence API",
    version="1.0.0"
)

# CORS middleware for frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173", "*"],  # React dev servers
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request/Response models
class ResearchRequest(BaseModel):
    startup_name: str
    research_type: Optional[str] = "comprehensive"  # comprehensive, quick, founders_only, etc.


class FounderResponse(BaseModel):
    name: str
    background: str
    experience: str
    credibility_score: int
    sources: List[str]


class CompetitorResponse(BaseModel):
    name: str
    market_position: str
    funding: str
    key_differentiators: str
    sources: List[str]


class EnrichedSource(BaseModel):
    url: str
    title: str
    source_type: str
    content_length: int
    status: str


class ResearchResponse(BaseModel):
    startup_name: str
    founders: List[FounderResponse]
    competitors: List[CompetitorResponse]
    market_summary: str
    funding_summary: str
    industry_summary: str
    total_sources: int
    enriched_sources: List[EnrichedSource]
    timestamp: str


# Global research workflow instance
workflow = None


def get_workflow() -> ResearchWorkflow:
    """Get or create research workflow instance"""
    global workflow
    if workflow is None:
        workflow = ResearchWorkflow()
    return workflow


@app.get("/")
async def root():
    """Health check"""
    return {
        "status": "ok",
        "service": "VentureMind AI - Research Intelligence",
        "owner": "Person 2",
        "endpoints": [
            "GET / - Health check",
            "POST /research - Run full research",
            "GET /status - Service status"
        ]
    }


@app.get("/status")
async def status():
    """Service status"""
    return {
        "status": "running",
        "timestamp": datetime.utcnow().isoformat(),
        "service": "Research Intelligence (Person 2)",
        "features": [
            "Tavily web search",
            "Firecrawl content enrichment",
            "Founder research",
            "Competitor discovery",
            "Market analysis",
            "Funding tracking",
            "Industry analysis"
        ]
    }


@app.post("/research")
async def run_research(request: ResearchRequest) -> ResearchResponse:
    """
    Run comprehensive research on a startup

    Args:
        request: Research request with startup name

    Returns:
        ResearchResponse with all findings
    """
    try:
        startup_name = request.startup_name.strip()
        if not startup_name:
            raise HTTPException(status_code=400, detail="Startup name is required")

        print(f"\n[API] Received research request for: {startup_name}")

        # Get workflow
        workflow_instance = get_workflow()

        # Run research
        startup_input = StartupInput(startup_name=startup_name)
        research_output = workflow_instance.run_research(startup_input)

        # Convert enriched sources to response format
        enriched_sources_response = []
        for url, enriched_data in research_output.enriched_sources.items():
            enriched_sources_response.append(
                EnrichedSource(
                    url=url,
                    title=enriched_data.get("metadata", {}).get("title", url),
                    source_type="research",
                    content_length=len(enriched_data.get("markdown", "")),
                    status=enriched_data.get("status", "unknown")
                )
            )

        # Build response
        response = ResearchResponse(
            startup_name=startup_name,
            founders=[
                FounderResponse(
                    name=f.name,
                    background=f.background,
                    experience=f.experience,
                    credibility_score=f.credibility_score,
                    sources=f.sources
                )
                for f in research_output.founders
            ],
            competitors=[
                CompetitorResponse(
                    name=c.name,
                    market_position=c.market_position,
                    funding=c.funding,
                    key_differentiators=c.key_differentiators,
                    sources=c.sources
                )
                for c in research_output.competitors
            ],
            market_summary=research_output.market_summary,
            funding_summary=research_output.funding_summary,
            industry_summary=research_output.industry_summary,
            total_sources=len(research_output.sources),
            enriched_sources=enriched_sources_response,
            timestamp=datetime.utcnow().isoformat()
        )

        return response

    except HTTPException:
        raise
    except Exception as e:
        print(f"[API ERROR] {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/research/{startup_name}")
async def get_research_quick(startup_name: str) -> ResearchResponse:
    """
    Quick research endpoint (GET variant)

    Args:
        startup_name: Name of startup to research

    Returns:
        Research results
    """
    request = ResearchRequest(startup_name=startup_name)
    return await run_research(request)


@app.get("/health")
async def health_check():
    """Detailed health check"""
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "services": {
            "tavily": "configured",
            "firecrawl": "configured",
            "storage": "ready"
        }
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "backend.api.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )
