"""Committee Agent output contract.

Person 4 returns this contract.
Person 5 owns the contract definition.
"""

from pydantic import BaseModel, Field


class CommitteeDecision(BaseModel):
    """Committee Agent final decision."""

    verdict: str
    confidence: int = Field(..., ge=0, le=100)
    reasoning: str
