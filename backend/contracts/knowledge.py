"""Knowledge Intelligence output contract.

Person 3 returns these contracts.
Person 5 owns the contract definitions.
"""

from pydantic import BaseModel
from typing import List


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
