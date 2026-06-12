"""Bear Agent output contract.

Person 4 returns this contract.
Person 5 owns the contract definition.
"""

from pydantic import BaseModel, Field
from typing import List


class BearOutput(BaseModel):
    """Bear Agent rejection case output."""

    rejection_case: str
    weaknesses: List[str] = []
    confidence: int = Field(..., ge=0, le=100)
