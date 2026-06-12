"""Workflow state management.

Person 5 owns this module.
Manages AnalysisState through the LangGraph workflow.
"""

from backend.contracts import AnalysisState


class StateManager:
    """Manages workflow state transitions."""

    def __init__(self):
        """Initialize state manager."""
        pass

    def create_state(self, startup_input) -> AnalysisState:
        """Create new analysis state."""
        return AnalysisState(startup_input=startup_input)

    def update_research(self, state: AnalysisState, research_output) -> AnalysisState:
        """Update state with research results."""
        state.research_output = research_output
        return state

    def update_knowledge(self, state: AnalysisState, knowledge_output) -> AnalysisState:
        """Update state with knowledge results."""
        state.knowledge_output = knowledge_output
        return state

    def update_bull(self, state: AnalysisState, bull_output) -> AnalysisState:
        """Update state with bull analysis."""
        state.bull_output = bull_output
        return state

    def update_bear(self, state: AnalysisState, bear_output) -> AnalysisState:
        """Update state with bear analysis."""
        state.bear_output = bear_output
        return state

    def update_review(self, state: AnalysisState, review_output) -> AnalysisState:
        """Update state with review feedback."""
        state.review_output = review_output
        return state

    def update_red_team(self, state: AnalysisState, red_team_output) -> AnalysisState:
        """Update state with red team challenges."""
        state.red_team_output = red_team_output
        return state

    def update_committee(self, state: AnalysisState, committee_decision) -> AnalysisState:
        """Update state with committee decision."""
        state.committee_decision = committee_decision
        return state

    def update_simulation(self, state: AnalysisState, simulation_output) -> AnalysisState:
        """Update state with simulation results."""
        state.simulation_output = simulation_output
        return state

    def update_final_report(self, state: AnalysisState, final_report) -> AnalysisState:
        """Update state with final report."""
        state.final_report = final_report
        return state
