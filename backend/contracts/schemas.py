from pydantic import BaseModel, Field
from typing import Optional, List


# ========================
# Global Shared Contracts
# ========================


class StartupInput(BaseModel):
    """Input contract for startup analysis."""

    startup_name: str
    website_url: Optional[str] = None
    pitch_deck_path: Optional[str] = None


class FinalReport(BaseModel):
    """Final investment recommendation report."""

    founder_score: int = Field(..., ge=0, le=100)
    market_score: int = Field(..., ge=0, le=100)
    risk_score: int = Field(..., ge=0, le=100)
    recommendation: str
    executive_summary: str
    committee_decision: str


# ========================
# Research Layer Output
# ========================


class ResearchOutput(BaseModel):
    """Research Intelligence module output."""

    founders: List[str] = []
    competitors: List[str] = []
    market_summary: str = ""
    funding_summary: str = ""
    industry_summary: str = ""
    sources: List[str] = []


# ========================
# RAG & Knowledge Output
# ========================


class KnowledgeOutput(BaseModel):
    """Knowledge Intelligence module output."""

    startup_summary: str
    business_model: str
    risks: List[str] = []
    financials: List[str] = []
    market_claims: List[str] = []
    evidence: List[str] = []


class RetrievalOutput(BaseModel):
    """RAG retrieval output."""

    context: str
    sources: List[str] = []


# ========================
# Agent Intelligence Output
# ========================


class BullOutput(BaseModel):
    """Bull Agent investment case output."""

    investment_case: str
    strengths: List[str] = []
    confidence: int = Field(..., ge=0, le=100)


class BearOutput(BaseModel):
    """Bear Agent rejection case output."""

    rejection_case: str
    weaknesses: List[str] = []
    confidence: int = Field(..., ge=0, le=100)


class ReviewOutput(BaseModel):
    """Reviewer Agent output."""

    approved: bool
    feedback: str
    retry_required: bool


class RedTeamOutput(BaseModel):
    """Red Team Agent output."""

    challenges: List[str] = []
    contradictions: List[str] = []
    missing_evidence: List[str] = []


class CommitteeDecision(BaseModel):
    """Committee Agent final decision."""

    verdict: str
    confidence: int = Field(..., ge=0, le=100)
    reasoning: str


class SimulationOutput(BaseModel):
    """Digital Twin simulation output."""

    scenario: str
    survival_probability: int = Field(..., ge=0, le=100)
    opportunities: List[str] = []
    risks: List[str] = []


# ========================
# Workflow State
# ========================


class AnalysisState(BaseModel):
    """Complete analysis workflow state."""

    startup_input: Optional[StartupInput] = None
    research_output: Optional[ResearchOutput] = None
    knowledge_output: Optional[KnowledgeOutput] = None
    bull_output: Optional[BullOutput] = None
    bear_output: Optional[BearOutput] = None
    review_output: Optional[ReviewOutput] = None
    red_team_output: Optional[RedTeamOutput] = None
    committee_decision: Optional[CommitteeDecision] = None
    simulation_output: Optional[SimulationOutput] = None
    final_report: Optional[FinalReport] = None
