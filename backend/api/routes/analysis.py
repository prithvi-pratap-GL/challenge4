"""Analysis endpoints.

Person 5 owns this module.
Handles startup analysis workflow.
"""

import asyncio
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional, Dict, Any
from uuid import uuid4

from backend.contracts import StartupInput, FinalReport, AnalysisState
from backend.orchestrator.graph import build_analysis_graph

router = APIRouter()

# In-memory storage for demo (use database in production)
analysis_store: Dict[str, AnalysisState] = {}
orchestrator_graph = build_analysis_graph()


class AnalysisRequest(BaseModel):
    """Analysis request payload."""

    startup_name: str
    website_url: Optional[str] = None
    pitch_deck_path: Optional[str] = None


class AnalysisResponse(BaseModel):
    """Analysis response payload."""

    id: str
    status: str
    current_agent: str
    progress_percent: int


class AnalysisStatus(BaseModel):
    """Analysis status response."""

    id: str
    status: str
    current_agent: str
    progress: int


@router.post("/analysis")
async def start_analysis(request: AnalysisRequest) -> AnalysisResponse:
    """
    Start a new startup analysis.

    Args:
        request: Analysis request with startup info

    Returns:
        Analysis ID and initial status
    """
    analysis_id = str(uuid4())

    # Create initial state
    startup_input = StartupInput(
        startup_name=request.startup_name,
        website_url=request.website_url,
        pitch_deck_path=request.pitch_deck_path
    )

    state = AnalysisState(startup_input=startup_input)
    analysis_store[analysis_id] = state

    # Run orchestrator asynchronously
    try:
        final_state = orchestrator_graph.invoke(state)
        analysis_store[analysis_id] = final_state

        return AnalysisResponse(
            id=analysis_id,
            status="completed",
            current_agent="final_report",
            progress_percent=100
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")


@router.get("/analysis/{analysis_id}")
async def get_analysis_status(analysis_id: str) -> AnalysisStatus:
    """
    Get analysis status and progress.

    Args:
        analysis_id: Analysis ID

    Returns:
        Current status, agent running, and progress percentage
    """
    if analysis_id not in analysis_store:
        raise HTTPException(status_code=404, detail="Analysis not found")

    state = analysis_store[analysis_id]

    # Calculate progress
    progress = 0
    current_agent = "pending"

    if state.bull_output and state.bear_output and state.red_team_output:
        progress = 30
        current_agent = "reviewer"

    if state.review_output:
        progress = 50
        current_agent = "committee"

    if state.committee_decision:
        progress = 70
        current_agent = "digital_twin"

    if state.simulation_output:
        progress = 90
        current_agent = "final_report"

    if state.final_report:
        progress = 100
        current_agent = "completed"

    return AnalysisStatus(
        id=analysis_id,
        status="completed" if progress == 100 else "in_progress",
        current_agent=current_agent,
        progress=progress
    )


@router.get("/report/{analysis_id}")
async def get_final_report(analysis_id: str) -> FinalReport:
    """
    Get final report for completed analysis.

    Args:
        analysis_id: Analysis ID

    Returns:
        Final investment recommendation report
    """
    if analysis_id not in analysis_store:
        raise HTTPException(status_code=404, detail="Analysis not found")

    state = analysis_store[analysis_id]

    if not state.final_report:
        raise HTTPException(status_code=202, detail="Analysis still in progress")

    return state.final_report


@router.get("/committee/{analysis_id}")
async def get_committee_decision(analysis_id: str):
    """
    Get committee decision details.

    Args:
        analysis_id: Analysis ID

    Returns:
        Committee decision with reasoning
    """
    if analysis_id not in analysis_store:
        raise HTTPException(status_code=404, detail="Analysis not found")

    state = analysis_store[analysis_id]

    if not state.committee_decision:
        raise HTTPException(status_code=202, detail="Analysis still in progress")

    return {
        "verdict": state.committee_decision.verdict,
        "confidence": state.committee_decision.confidence,
        "reasoning": state.committee_decision.reasoning
    }


@router.get("/analysis/{analysis_id}/progress")
async def get_analysis_progress(analysis_id: str) -> Dict[str, Any]:
    """
    Get detailed analysis progress.

    Args:
        analysis_id: Analysis ID

    Returns:
        Detailed progress including all intermediate outputs
    """
    if analysis_id not in analysis_store:
        raise HTTPException(status_code=404, detail="Analysis not found")

    state = analysis_store[analysis_id]

    return {
        "id": analysis_id,
        "startup_input": state.startup_input.dict() if state.startup_input else None,
        "research_output": state.research_output,
        "knowledge_output": state.knowledge_output,
        "bull_output": state.bull_output.dict() if state.bull_output else None,
        "bear_output": state.bear_output.dict() if state.bear_output else None,
        "red_team_output": state.red_team_output.dict() if state.red_team_output else None,
        "review_output": state.review_output.dict() if state.review_output else None,
        "committee_decision": state.committee_decision.dict() if state.committee_decision else None,
        "simulation_output": [s.dict() for s in state.simulation_output] if state.simulation_output else None,
        "final_report": state.final_report.dict() if state.final_report else None
    }
