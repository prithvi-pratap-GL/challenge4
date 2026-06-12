"""
Pydantic models for agent outputs.
These schemas enforce strict typing for all analytical agents and must be imported by respective modules.
Shared contracts - no internal implementation imports.
"""

from typing import List
from pydantic import BaseModel, Field


# ============================================================================
# Bull Agent Output
# ============================================================================
class BullOutput(BaseModel):
    """Investment case arguing for funding the startup."""

    investment_case: str = Field(
        ...,
        description="Comprehensive bullish narrative supporting investment"
    )
    strengths: List[str] = Field(
        ...,
        description="Key strengths and opportunities identified"
    )
    confidence: int = Field(
        ...,
        ge=0,
        le=100,
        description="Confidence level in the investment case (0-100)"
    )


# ============================================================================
# Bear Agent Output
# ============================================================================
class BearOutput(BaseModel):
    """Rejection case arguing against funding the startup."""

    rejection_case: str = Field(
        ...,
        description="Comprehensive bearish narrative against investment"
    )
    weaknesses: List[str] = Field(
        ...,
        description="Key weaknesses and risks identified"
    )
    confidence: int = Field(
        ...,
        ge=0,
        le=100,
        description="Confidence level in the rejection case (0-100)"
    )


# ============================================================================
# Reviewer Agent Output
# ============================================================================
class ReviewOutput(BaseModel):
    """Review of analysis completeness and accuracy."""

    approved: bool = Field(
        ...,
        description="Whether the analysis is approved for final committee decision"
    )
    feedback: str = Field(
        ...,
        description="Detailed feedback on gaps, inconsistencies, or areas needing improvement"
    )
    retry_required: bool = Field(
        ...,
        description="Whether the analysis should be regenerated based on feedback"
    )


# ============================================================================
# Red Team Agent Output
# ============================================================================
class RedTeamOutput(BaseModel):
    """Red team analysis challenging assumptions and claims."""

    challenges: List[str] = Field(
        ...,
        description="Specific challenges to claims made in the analysis"
    )
    contradictions: List[str] = Field(
        ...,
        description="Contradictions between different sources or assumptions"
    )
    missing_evidence: List[str] = Field(
        ...,
        description="Critical evidence that should be present but is missing"
    )


# ============================================================================
# Committee Agent Output
# ============================================================================
class CommitteeDecision(BaseModel):
    """Final investment committee decision."""

    verdict: str = Field(
        ...,
        description="Final investment recommendation (e.g., 'INVEST', 'PASS', 'CONDITIONAL')"
    )
    confidence: int = Field(
        ...,
        ge=0,
        le=100,
        description="Confidence level in the decision (0-100)"
    )
    reasoning: str = Field(
        ...,
        description="Detailed reasoning synthesizing bull case, bear case, and red team challenges"
    )


# ============================================================================
# Digital Twin Agent Output
# ============================================================================
class SimulationOutput(BaseModel):
    """Simulation scenario results from digital twin."""

    scenario: str = Field(
        ...,
        description="Description of the simulated scenario"
    )
    survival_probability: int = Field(
        ...,
        ge=0,
        le=100,
        description="Probability of startup survival under this scenario (0-100)"
    )
    opportunities: List[str] = Field(
        ...,
        description="Identified opportunities in this scenario"
    )
    risks: List[str] = Field(
        ...,
        description="Identified risks in this scenario"
    )
