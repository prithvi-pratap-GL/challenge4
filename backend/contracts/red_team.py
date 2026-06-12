"""Red Team Agent output contract.

Person 4 returns this contract.
Person 5 owns the contract definition.
"""

from pydantic import BaseModel
from typing import List


class RedTeamOutput(BaseModel):
    """Red Team Agent output."""

    challenges: List[str] = []
    contradictions: List[str] = []
    missing_evidence: List[str] = []
