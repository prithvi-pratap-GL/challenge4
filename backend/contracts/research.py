"""Research layer output contract.

Person 2 returns this contract.
Person 5 owns the contract definition.
"""

from dataclasses import dataclass, field
from typing import List, Dict, Any


@dataclass
class Founder:
    """Founder information structure"""
    name: str
    background: str
    experience: str
    credibility_score: int
    sources: List[str] = field(default_factory=list)


@dataclass
class Competitor:
    """Competitor analysis structure"""
    name: str
    market_position: str
    funding: str
    key_differentiators: str
    sources: List[str] = field(default_factory=list)


@dataclass
class ResearchOutput:
    """Research Intelligence module output."""
    founders: List[Founder]
    competitors: List[Competitor]
    market_summary: str
    funding_summary: str
    industry_summary: str
    sources: List[str]
    enriched_sources: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self):
        """Convert to dictionary for JSON serialization"""
        return {
            "founders": [
                {
                    "name": f.name,
                    "background": f.background,
                    "experience": f.experience,
                    "credibility_score": f.credibility_score,
                    "sources": f.sources
                }
                for f in self.founders
            ],
            "competitors": [
                {
                    "name": c.name,
                    "market_position": c.market_position,
                    "funding": c.funding,
                    "key_differentiators": c.key_differentiators,
                    "sources": c.sources
                }
                for c in self.competitors
            ],
            "market_summary": self.market_summary,
            "funding_summary": self.funding_summary,
            "industry_summary": self.industry_summary,
            "sources": self.sources,
            "enriched_sources": self.enriched_sources
        }
