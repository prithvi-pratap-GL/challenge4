"""Startup input contract.

Person 5 owns this contract.
"""

from pydantic import BaseModel
from typing import Optional


class StartupInput(BaseModel):
    """Input contract for startup analysis."""

    startup_name: str
    website_url: Optional[str] = None
    pitch_deck_path: Optional[str] = None
