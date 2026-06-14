"""
Research Agent Module
Person 2 - Research Intelligence Owner
Public function: run_research(startup_input: StartupInput) -> ResearchOutput
"""

from backend.contracts.startup import StartupInput
from backend.contracts.research import ResearchOutput
from backend.agents.research.workflow import ResearchWorkflow


class ResearchIntelligenceAgent:
    """
    Main Research Intelligence Agent
    Entry point for all research operations

    GUARANTEE:
    - No other team accesses Tavily directly
    - Everyone consumes ResearchOutput only
    """

    def __init__(self):
        self.workflow = ResearchWorkflow()

    def run_research(self, startup_input: StartupInput) -> ResearchOutput:
        """
        PUBLIC FUNCTION for Person 2
        Input: StartupInput (startup_name, website_url, pitch_deck_path)
        Output: ResearchOutput (complete research contract)

        This is the ONLY public interface for research operations.
        All other modules import ResearchOutput from contracts.
        """
        return self.workflow.run_research(startup_input)


# Singleton instance
_research_agent = None


def get_research_agent() -> ResearchIntelligenceAgent:
    """Get or create the research agent singleton"""
    global _research_agent
    if _research_agent is None:
        _research_agent = ResearchIntelligenceAgent()
    return _research_agent


def run_research(startup_input: StartupInput) -> ResearchOutput:
    """
    Main entry point for research pipeline
    Person 5 (orchestrator) calls this function

    Args:
        startup_input: StartupInput contract

    Returns:
        ResearchOutput: Complete research findings
    """
    agent = get_research_agent()
    return agent.run_research(startup_input)
