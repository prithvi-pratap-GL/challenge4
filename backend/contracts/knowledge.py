"""Knowledge Intelligence output contract.

Person 3 returns these contracts.
Person 5 owns the contract definitions.
"""

from dataclasses import dataclass, field
from typing import List, Dict, Any


@dataclass
class KnowledgeOutput:
    """Knowledge Intelligence module output."""

    startup_summary: str
    business_model: str
    risks: List[str] = field(default_factory=list)
    financials: List[str] = field(default_factory=list)
    market_claims: List[str] = field(default_factory=list)
    evidence: List[str] = field(default_factory=list)


@dataclass
class RetrievalOutput:
    """RAG retrieval output."""

    context: str
    sources: List[str] = field(default_factory=list)
