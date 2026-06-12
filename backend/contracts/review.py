"""Reviewer Agent output contract.

Person 4 returns this contract.
Person 5 owns the contract definition.
"""

from pydantic import BaseModel


class ReviewOutput(BaseModel):
    """Reviewer Agent output."""

    approved: bool
    feedback: str
    retry_required: bool
