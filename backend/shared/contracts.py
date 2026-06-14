"""
Shared contracts for VentureMind AI - All modules use these
No module may import internal implementation from another module.
Only shared contracts may be imported.
"""

from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class StartupInput:
    """Global input contract for all analyses"""
    startup_name: str
    website_url: Optional[str] = None
    pitch_deck_path: Optional[str] = None


@dataclass
class Founder:
    """Founder information structure"""
    name: str
    background: str
    experience: str
    credibility_score: int  # 0-100
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
    """
    Research Intelligence Owner (Person 2) output contract
    All downstream agents (Person 4, Person 3, Person 5) consume this only.
    No one else talks to Tavily or Firecrawl directly.
    """
    founders: List[Founder]
    competitors: List[Competitor]
    market_summary: str
    funding_summary: str
    industry_summary: str
    sources: List[str]  # All unique URLs used across research


# Global shared contracts (Person 5 - Platform & Orchestration)
@dataclass
class FinalReport:
    """Final output from entire system"""
    founder_score: int
    market_score: int
    risk_score: int
    recommendation: str
    executive_summary: str
    committee_decision: str
