"""
Example: How Person 5 (Orchestrator) uses Person 2's Research Module

This shows the proper integration pattern between modules.
Person 5 ONLY imports from contracts, not from internal Person 2 modules.
"""

from backend.contracts.startup import StartupInput
from backend.contracts.research import ResearchOutput

# CORRECT IMPORT (Person 5 only imports the public function)
from backend.agents.research.agent import run_research


def example_research_flow():
    """
    Example research flow for orchestrator (Person 5)
    """
    print("\n" + "=" * 70)
    print("EXAMPLE: How Person 5 Uses Person 2's Research Module")
    print("=" * 70)

    # Step 1: Create startup input
    startup_input = StartupInput(
        startup_name="OpenAI",
        website_url="https://openai.com",
        pitch_deck_path=None
    )
    print(f"\n[1] Created startup input: {startup_input.startup_name}")

    # Step 2: Call research (Person 5 only calls this function)
    research_output: ResearchOutput = run_research(startup_input)
    print(f"[2] Research complete")

    # Step 3: Person 5 has access to research output
    print(f"\n[3] Research Results:")
    print(f"    - Founders: {len(research_output.founders)}")
    for founder in research_output.founders:
        print(f"      * {founder.name} (Credibility: {founder.credibility_score}/100)")

    print(f"\n    - Competitors: {len(research_output.competitors)}")
    for competitor in research_output.competitors:
        print(f"      * {competitor.name} ({competitor.market_position})")

    # Step 4: Person 5 can now pass research to Person 4 (Bull/Bear agents)
    print(f"\n[4] Research output is now available for Person 4's agents")
    print(f"    - Person 4 receives: ResearchOutput contract")
    print(f"    - Person 4 uses it for Bull/Bear/Red Team analysis")

    # Step 5: Serialization for storage/API responses
    research_dict = research_output.to_dict()
    print(f"\n[5] Serialized to dict for API/storage")
    print(f"    Keys: {list(research_dict.keys())}")

    # Step 6: Show sources
    print(f"\n[6] All sources used in research:")
    for i, source in enumerate(research_output.sources, 1):
        print(f"    {i}. {source}")


def example_wrong_imports():
    """
    Example of WRONG imports (DON'T DO THIS)
    Person 5 should NOT import from Person 2's internal modules
    """
    print("\n" + "=" * 70)
    print("WRONG: How NOT to use Person 2's Module")
    print("=" * 70)

    print("\n[BAD] Person 5 imports internal Person 2 modules:")
    print("  WRONG: from backend.agents.research.workflow import ResearchWorkflow")
    print("  WRONG: from backend.services.tavily.client import TavilySearchService")

    print("\n[WHY WRONG]")
    print("  - Violates module contract boundaries")
    print("  - Creates tight coupling between Person 2 and Person 5")
    print("  - If Person 2 changes internal implementation, Person 5 breaks")
    print("  - Multiple modules might try to use Tavily directly (violates contract)")

    print("\n[CORRECT] Person 5 only imports public functions and contracts:")
    print("  CORRECT: from backend.contracts.startup import StartupInput")
    print("  CORRECT: from backend.contracts.research import ResearchOutput")
    print("  CORRECT: from backend.agents.research.agent import run_research")


def example_how_person_4_uses_research():
    """
    Example of how Person 4 (Bull Agent) uses Person 2's research
    """
    print("\n" + "=" * 70)
    print("EXAMPLE: How Person 4 Uses Research Output")
    print("=" * 70)

    startup_input = StartupInput(
        startup_name="Stripe",
        website_url="https://stripe.com"
    )

    # Person 4 receives ResearchOutput from Person 5
    research_output: ResearchOutput = run_research(startup_input)

    print(f"\nPerson 4 (Bull Agent) receives research and analyzes:")
    print(f"\n1. Founder Analysis:")
    for founder in research_output.founders:
        if founder.credibility_score > 90:
            print(f"   [STRONG SIGNAL] {founder.name} - High credibility ({founder.credibility_score}/100)")
            print(f"   - Background: {founder.background}")
            print(f"   - Experience: {founder.experience}")

    print(f"\n2. Competitive Landscape:")
    for competitor in research_output.competitors:
        print(f"   - {competitor.name}: {competitor.market_position}")
        print(f"     Differentiators: {competitor.key_differentiators}")

    print(f"\n3. Market Context:")
    print(f"   {research_output.market_summary[:200]}...")

    print(f"\n4. Funding History:")
    print(f"   {research_output.funding_summary[:200]}...")

    print(f"\n[Bull Agent uses this to build investment case]")


def example_workflow_state():
    """
    Example of how research fits into workflow state (Person 5)
    """
    print("\n" + "=" * 70)
    print("EXAMPLE: Workflow State (Person 5's Orchestrator)")
    print("=" * 70)

    startup_input = StartupInput(
        startup_name="Notion",
        website_url="https://notion.so"
    )

    # This is what Person 5's orchestrator does
    class AnalysisState:
        def __init__(self, startup_input):
            self.startup_input = startup_input
            self.research_output = None

    state = AnalysisState(startup_input)

    # Step 1: Get research
    print(f"\n[STEP 1] Get research from Person 2")
    state.research_output = run_research(startup_input)
    print(f"  Result: ResearchOutput with {len(state.research_output.founders)} founders")

    # Step 2: Pass to Person 3 (Knowledge)
    print(f"\n[STEP 2] Pass research to Person 3 (Knowledge)")
    print(f"  Person 3 receives: ResearchOutput")
    print(f"  Person 3 uses for: Initial knowledge base seeding")

    # Step 3: Pass to Person 4 (Agents)
    print(f"\n[STEP 3] Pass research to Person 4 (Bull/Bear/Red Team)")
    print(f"  Person 4 receives: ResearchOutput")
    print(f"  Person 4 uses for: Analysis and debate")

    # Store in state
    print(f"\n[STEP 4] Store in workflow state")
    print(f"  state.research_output = {type(state.research_output).__name__}")


if __name__ == "__main__":
    example_research_flow()
    example_wrong_imports()
    example_how_person_4_uses_research()
    example_workflow_state()

    print("\n" + "=" * 70)
    print("KEY TAKEAWAYS")
    print("=" * 70)
    print("""
1. Person 2 exposes ONE public function: run_research()
2. All other teams import ONLY: StartupInput, ResearchOutput, run_research
3. Never import internal modules (workflow, client, prompts)
4. Never call Tavily, Firecrawl, or Crunchbase directly
5. Use ResearchOutput.to_dict() for serialization
6. All research data is fully attributed with sources
    """)
