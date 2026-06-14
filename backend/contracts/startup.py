"""Startup input contract.

Person 5 owns this contract.
"""

from dataclasses import dataclass
from typing import Optional


@dataclass
class StartupInput:
    """Input contract for startup analysis."""

    startup_name: str
    website_url: Optional[str] = None
    pitch_deck_path: Optional[str] = None
