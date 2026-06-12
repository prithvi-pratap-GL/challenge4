"""Final report contract.

Person 5 owns this contract.
"""

from pydantic import BaseModel, Field


class FinalReport(BaseModel):
    """Final investment recommendation report."""

    founder_score: int = Field(..., ge=0, le=100)
    market_score: int = Field(..., ge=0, le=100)
    risk_score: int = Field(..., ge=0, le=100)
    recommendation: str
    executive_summary: str
    committee_decision: str
