"""
Global Shared Contracts for VentureMind AI
Person 5 owns all contracts, but Person 2 publishes research output to ResearchOutput
"""

from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class StartupInput:
    """Global input contract for all analyses"""
    startup_name: str
    website_url: Optional[str] = None
    pitch_deck_path: Optional[str] = None
