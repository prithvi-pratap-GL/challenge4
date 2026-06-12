"""LangGraph workflow graph definition.

Person 5 owns this module.
Defines the DAG (Directed Acyclic Graph) for analysis workflow.
"""

import asyncio
from langgraph.graph import StateGraph
from backend.contracts import AnalysisState, FinalReport

# Import Person 2 research agent
try:
    from backend.agents.research.agent import run_research
except ImportError:
    run_research = None

# Import Person 3 knowledge agents
try:
    from backend.ingestion.pdf.pipeline import ingest_pitch_deck
    from backend.ingestion.website.pipeline import ingest_website
    from backend.knowledge.retrieval.service import retrieve_context
except ImportError:
    ingest_pitch_deck = None
    ingest_website = None
    retrieve_context = None

# Import Person 4 agents
from backend.agents.bull.agent import run_bull_case
from backend.agents.bear.agent import run_bear_case
from backend.agents.red_team.agent import run_red_team
from backend.agents.reviewer.agent import review_analysis
from backend.agents.committee.agent import run_committee
from backend.agents.digital_twin.agent import simulate_scenarios


async def node_research(state: AnalysisState) -> AnalysisState:
    """Research node - calls Person 2's research agent."""
    if run_research is None:
        # Fallback if Person 2 agent not available
        state.research_output = {}
        return state

    research_output = await run_research(state.startup_input)
    state.research_output = research_output
    return state


async def node_knowledge(state: AnalysisState) -> AnalysisState:
    """Knowledge node - calls Person 3's ingestion and retrieval agents."""
    if ingest_pitch_deck is None:
        # Fallback if Person 3 agents not available
        state.knowledge_output = {}
        return state

    # Ingest based on available inputs
    if state.startup_input.pitch_deck_path:
        knowledge_output = await ingest_pitch_deck(state.startup_input.pitch_deck_path)
    elif state.startup_input.website_url:
        knowledge_output = await ingest_website(state.startup_input.website_url)
    else:
        knowledge_output = {}

    state.knowledge_output = knowledge_output
    return state


async def node_bull(state: AnalysisState) -> AnalysisState:
    """Bull agent node - calls Person 4's Bull agent."""
    bull_output = await run_bull_case(
        state.research_output,
        state.knowledge_output
    )
    state.bull_output = bull_output
    return state


async def node_bear(state: AnalysisState) -> AnalysisState:
    """Bear agent node - calls Person 4's Bear agent."""
    bear_output = await run_bear_case(
        state.research_output,
        state.knowledge_output
    )
    state.bear_output = bear_output
    return state


async def node_red_team(state: AnalysisState) -> AnalysisState:
    """Red team agent node - calls Person 4's Red Team agent."""
    red_team_output = await run_red_team(
        state.research_output,
        state.knowledge_output
    )
    state.red_team_output = red_team_output
    return state


async def node_reviewer(state: AnalysisState) -> AnalysisState:
    """Reviewer node - calls Person 4's Reviewer agent."""
    review_output = await review_analysis(
        state.bull_output,
        state.bear_output,
        state.red_team_output,
        state.research_output,
        state.knowledge_output
    )
    state.review_output = review_output
    return state


async def node_committee(state: AnalysisState) -> AnalysisState:
    """Committee node - calls Person 4's Committee agent."""
    committee_output = await run_committee(
        state.bull_output,
        state.bear_output,
        state.red_team_output,
        state.research_output,
        state.knowledge_output
    )
    state.committee_decision = committee_output
    return state


async def node_digital_twin(state: AnalysisState) -> AnalysisState:
    """Digital Twin node - calls Person 4's Digital Twin agent."""
    simulation_output = await simulate_scenarios(
        state.research_output,
        state.knowledge_output
    )
    state.simulation_output = simulation_output
    return state


async def node_final_report(state: AnalysisState) -> AnalysisState:
    """Generate final report from all analysis outputs."""
    final_report = FinalReport(
        founder_score=75,
        market_score=78,
        risk_score=60,
        recommendation=state.committee_decision.reasoning,
        executive_summary=f"Committee verdict: {state.committee_decision.verdict}",
        committee_decision=state.committee_decision.verdict
    )
    state.final_report = final_report
    return state


def should_retry(state: AnalysisState) -> str:
    """Conditional edge: check if review requires retry."""
    if state.review_output and state.review_output.retry_required:
        return "retry"
    else:
        return "continue"


def build_analysis_graph():
    """
    Build the complete analysis workflow graph.

    Complete Workflow:
    1. Research (Person 2) -> Knowledge (Person 3)
    2. Knowledge -> Bull & Bear & Red Team (Person 4, parallel)
    3. All three -> Reviewer (Person 4)
    4. Reviewer -> [Decision: retry?]
       - If retry: back to Bull
       - If ok: continue to Committee
    5. Committee -> Digital Twin
    6. Digital Twin -> Final Report
    """
    graph = StateGraph(AnalysisState)

    # Add nodes
    graph.add_node("research", node_research)
    graph.add_node("knowledge", node_knowledge)
    graph.add_node("bull", node_bull)
    graph.add_node("bear", node_bear)
    graph.add_node("red_team", node_red_team)
    graph.add_node("reviewer", node_reviewer)
    graph.add_node("committee", node_committee)
    graph.add_node("digital_twin", node_digital_twin)
    graph.add_node("final_report", node_final_report)

    # Add edges - sequential: Research -> Knowledge
    graph.add_edge("START", "research")
    graph.add_edge("research", "knowledge")

    # Parallel execution: Knowledge -> Bull & Bear & Red Team
    graph.add_edge("knowledge", "bull")
    graph.add_edge("knowledge", "bear")
    graph.add_edge("knowledge", "red_team")

    # All three converge to reviewer
    graph.add_edge("bull", "reviewer")
    graph.add_edge("bear", "reviewer")
    graph.add_edge("red_team", "reviewer")

    # Conditional edge: retry or continue
    graph.add_conditional_edges(
        "reviewer",
        should_retry,
        {
            "retry": "bull",
            "continue": "committee"
        }
    )

    # Continue to committee
    graph.add_edge("committee", "digital_twin")
    graph.add_edge("digital_twin", "final_report")
    graph.add_edge("final_report", "END")

    # Compile graph
    return graph.compile()
