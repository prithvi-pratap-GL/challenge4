"""Digital Twin simulation output contract.

Person 4 returns this contract.
Person 5 owns the contract definition.
"""

from pydantic import BaseModel, Field
from typing import List


class SimulationOutput(BaseModel):
    """Digital Twin simulation output."""

    scenario: str
    survival_probability: int = Field(..., ge=0, le=100)
    opportunities: List[str] = []
    risks: List[str] = []
