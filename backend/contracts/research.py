"""Research layer output contract.

Person 2 returns this contract.
Person 5 owns the contract definition.
"""

from pydantic import BaseModel
from typing import List


class ResearchOutput(BaseModel):
    """Research Intelligence module output."""

    founders: List[str] = []
    competitors: List[str] = []
    market_summary: str = ""
    funding_summary: str = ""
    industry_summary: str = ""
    sources: List[str] = []
