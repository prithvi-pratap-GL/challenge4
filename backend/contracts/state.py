"""Workflow state contract.

Person 5 owns this contract.
Tracks all intermediate outputs during analysis pipeline.
"""

from pydantic import BaseModel
from typing import Optional
from .startup import StartupInput
from .research import ResearchOutput
from .knowledge import KnowledgeOutput
from .bull import BullOutput
from .bear import BearOutput
from .review import ReviewOutput
from .red_team import RedTeamOutput
from .committee import CommitteeDecision
from .simulation import SimulationOutput
from .report import FinalReport


class AnalysisState(BaseModel):
    """Complete analysis workflow state."""

    startup_input: Optional[StartupInput] = None
    research_output: Optional[ResearchOutput] = None
    knowledge_output: Optional[KnowledgeOutput] = None
    bull_output: Optional[BullOutput] = None
    bear_output: Optional[BearOutput] = None
    review_output: Optional[ReviewOutput] = None
    red_team_output: Optional[RedTeamOutput] = None
    committee_decision: Optional[CommitteeDecision] = None
    simulation_output: Optional[SimulationOutput] = None
    final_report: Optional[FinalReport] = None
