"""Bull Agent output contract.

Person 4 returns this contract.
Person 5 owns the contract definition.
"""

from pydantic import BaseModel, Field
from typing import List


class BullOutput(BaseModel):
    """Bull Agent investment case output."""

    investment_case: str
    strengths: List[str] = []
    confidence: int = Field(..., ge=0, le=100)
