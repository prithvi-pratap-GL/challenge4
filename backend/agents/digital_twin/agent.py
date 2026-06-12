"""Digital Twin Agent - Business model stress-testing and scenario simulation."""

from typing import Any, Dict, List, Optional
from backend.agents.digital_twin.prompts import (
    DIGITAL_TWIN_SYSTEM_PROMPT,
    DEFAULT_SCENARIOS,
    SCENARIO_USER_PROMPT_TEMPLATE
)
from backend.agents.schemas import SimulationOutput
from backend.llm.client import LLMClient


async def simulate_scenarios(
    research_output: Dict[str, Any],
    knowledge_output: Dict[str, Any],
    scenario_prompts: Optional[List[str]] = None
) -> List[SimulationOutput]:
    """
    Run business model stress-tests under different scenarios.

    This agent simulates how the startup would survive under various macro/microeconomic
    scenarios. It estimates survival probability based on unit economics, competitive position,
    and founder adaptability.

    Args:
        research_output: ResearchOutput from Research Agent
            - founders: List[str] - Founder backgrounds
            - competitors: List[str] - Competitors
            - market_summary: str - Market analysis
            - funding_summary: str - Funding history
            - industry_summary: str - Industry context

        knowledge_output: KnowledgeOutput from RAG Agent
            - startup_summary: str - Company description
            - business_model: str - Revenue/unit economics
            - risks: List[str] - Identified risks
            - financials: List[str] - Financial metrics
            - market_claims: List[str] - Market claims
            - evidence: List[str] - Supporting evidence

        scenario_prompts: Optional list of custom scenarios
            If None, uses DEFAULT_SCENARIOS

    Returns:
        List of SimulationOutput, one per scenario with:
            - scenario: str (scenario description)
            - survival_probability: int (0-100)
            - opportunities: List[str] (emerging opportunities)
            - risks: List[str] (critical risks in scenario)

    Example:
        >>> research = {"founders": [...], "competitors": [...], ...}
        >>> knowledge = {"business_model": "...", "financials": [...], ...}
        >>> results = await simulate_scenarios(research, knowledge)
        >>> for result in results:
        ...     assert isinstance(result, SimulationOutput)
        ...     assert 0 <= result.survival_probability <= 100
    """

    scenarios_to_run = scenario_prompts or DEFAULT_SCENARIOS

    results = []

    for scenario_prompt in scenarios_to_run:
        # Extract baseline metrics
        business_model = knowledge_output.get("business_model", "")
        financials = knowledge_output.get("financials", [])
        risks = knowledge_output.get("risks", [])

        current_mrr = _extract_metric(financials, "MRR")
        nrr = _extract_metric(financials, "NRR")
        burn_rate = _extract_metric(financials, "burn")
        runway = _extract_metric(financials, "runway")

        # Extract research data
        competitors = _format_list(research_output.get("competitors", []))
        founder_backgrounds = _format_list(research_output.get("founders", []))
        market_summary = research_output.get("market_summary", "")
        tam = _extract_tam(market_summary)

        # Identify key dependencies and execution risks
        key_dependencies = _identify_dependencies(
            founder_backgrounds, knowledge_output.get("evidence", [])
        )
        strategic_risks = [r for r in risks if any(
            word in r.lower() for word in ["market", "competition", "regulatory"]
        )]
        execution_risks = [r for r in risks if any(
            word in r.lower() for word in ["team", "founder", "execution", "scaling"]
        )]

        # Build user prompt
        user_prompt = SCENARIO_USER_PROMPT_TEMPLATE.format(
            startup_name=knowledge_output.get("startup_summary", "Startup").split("\n")[0],
            scenario_prompt=scenario_prompt,
            business_model=business_model,
            current_mrr=current_mrr or "Not provided",
            nrr=nrr or "Not provided",
            burn_rate=burn_rate or "Not provided",
            runway=runway or "Not provided",
            tam=tam,
            competitors=competitors,
            founder_track_record=_assess_founder_track_record(founder_backgrounds),
            key_dependencies=key_dependencies,
            strategic_risks="\n- ".join(strategic_risks) if strategic_risks else "None identified",
            execution_risks="\n- ".join(execution_risks) if execution_risks else "None identified"
        )

        # Calculate survival probability based on scenario and baseline
        survival_prob = _calculate_survival_probability(
            scenario_prompt, knowledge_output, research_output
        )

        # Identify opportunities and risks in scenario
        opportunities = _identify_opportunities(scenario_prompt, founder_backgrounds)
        scenario_risks = _identify_scenario_risks(scenario_prompt, risks)

        # Integrate with LLM client for dynamic simulation
        llm_client = LLMClient()
        response = await llm_client.generate(
            system_prompt=DIGITAL_TWIN_SYSTEM_PROMPT,
            user_prompt=user_prompt,
            response_model=SimulationOutput
        )
        results.append(response)

    return results


def _extract_metric(financials: List[str], metric_name: str) -> Optional[str]:
    """Extract a specific metric from financials list."""
    for financial in financials:
        if metric_name.lower() in financial.lower():
            return financial
    return None


def _extract_tam(market_summary: str) -> str:
    """Extract TAM from market summary."""
    if "$" in market_summary:
        # Find the dollar amount (rough extraction)
        parts = market_summary.split()
        for i, part in enumerate(parts):
            if "$" in part:
                return f"{part} {parts[i+1] if i+1 < len(parts) else ''}"
    return "Not quantified"


def _format_list(items: List[str]) -> str:
    """Format list for prompt inclusion."""
    if not items:
        return "None"
    return ", ".join(items[:5])  # Limit to first 5


def _identify_dependencies(founder_info: str, evidence: List[str]) -> str:
    """Identify key person dependencies."""
    if "founder" in founder_info.lower() or "ceo" in founder_info.lower():
        return "High founder/CEO dependency for technical and business decisions"
    return "Distributed leadership team"


def _assess_founder_track_record(founder_info: str) -> str:
    """Assess founder's ability to adapt in crisis."""
    if "ex-" in founder_info.lower() or "experienced" in founder_info.lower():
        return "Strong track record - proven ability to execute at scale"
    elif "first-time" in founder_info.lower():
        return "First-time founder - limited crisis management experience"
    return "Moderate experience"


def _calculate_survival_probability(
    scenario: str,
    knowledge_output: Dict[str, Any],
    research_output: Dict[str, Any]
) -> int:
    """
    Calculate realistic survival probability under scenario.

    Baseline logic:
    - Start at 60% (average startup survival in downturns)
    - Penalize based on scenario severity and startup weaknesses
    - Adjust based on founder track record and unit economics
    """

    # Start with baseline
    survival_prob = 60

    scenario_lower = scenario.lower()
    nrr = _extract_nrr_value(knowledge_output.get("financials", []))
    founder_experienced = "ex-" in _format_list(research_output.get("founders", [])).lower()

    # Scenario severity adjustments
    if "google" in scenario_lower or "aws" in scenario_lower or "microsoft" in scenario_lower:
        survival_prob -= 25  # Massive competitor entering
    elif "doubles" in scenario_lower or "triples" in scenario_lower:
        survival_prob -= 20  # Cost increases
    elif "shrinks" in scenario_lower or "50%" in scenario_lower:
        survival_prob -= 30  # Market contraction
    elif "key person" in scenario_lower or "founder leaves" in scenario_lower:
        survival_prob -= 25 if not founder_experienced else -15
    elif "major customer churns" in scenario_lower or "customer leaves" in scenario_lower:
        survival_prob -= 20
    elif "vc dries up" in scenario_lower or "fundraising" in scenario_lower:
        survival_prob -= 15
    elif "open-source" in scenario_lower:
        survival_prob -= 20
    elif "expands" in scenario_lower:
        survival_prob -= 5  # Expansion risk but potential upside

    # Unit economics adjustment
    if nrr and nrr < 100:
        survival_prob -= 15  # Below break-even NRR makes scenarios worse
    elif nrr and nrr > 120:
        survival_prob += 10  # Strong NRR helps survive downturns

    # Founder experience adjustment (already factored into key person risk)
    if founder_experienced:
        survival_prob += 5  # Track record helps adaptability

    # Ensure bounds
    return max(0, min(100, survival_prob))


def _extract_nrr_value(financials: List[str]) -> Optional[int]:
    """Extract NRR percentage value."""
    for financial in financials:
        if "nrr" in financial.lower():
            # Try to extract percentage
            for part in financial.split():
                if "%" in part:
                    try:
                        return int(part.replace("%", ""))
                    except ValueError:
                        pass
    return None


def _identify_opportunities(scenario: str, founder_info: str) -> List[str]:
    """Identify opportunities that emerge in a scenario."""
    opportunities = []
    scenario_lower = scenario.lower()

    if "expands" in scenario_lower:
        opportunities.append("International expansion provides new revenue streams")
        opportunities.append("Market diversification reduces single-market dependency")
    elif "key person leaves" in scenario_lower:
        if "ex-" in founder_info.lower():
            opportunities.append("Opportunity to build stronger management team")
            opportunities.append("Founder experience helps identify successor talent")
    elif "open-source" in scenario_lower:
        opportunities.append("Partner with open-source community for integration")
        opportunities.append("Focus on services/support as differentiation")
    elif "vc dries up" in scenario_lower:
        opportunities.append("Bootstrap/profitability focus improves unit economics")
        opportunities.append("Focus on best customers increases NRR")

    return opportunities


def _identify_scenario_risks(scenario: str, baseline_risks: List[str]) -> List[str]:
    """Identify critical risks that emerge in scenario."""
    scenario_risks = []
    scenario_lower = scenario.lower()

    # Scenario-specific risks
    if "google" in scenario_lower or "aws" in scenario_lower:
        scenario_risks.extend([
            "Price war with well-capitalized vendor",
            "Loss of market share to bundled competitive offering",
            "Customer reluctance to switch from established vendor"
        ])
    elif "cac doubles" in scenario_lower:
        scenario_risks.extend([
            "Unsustainable unit economics if CAC:LTV ratio breaks",
            "Runway dramatically shortened",
            "May need to raise capital in unfavorable terms"
        ])
    elif "market shrinks" in scenario_lower:
        scenario_risks.extend([
            "TAM no longer supports multiple competitors",
            "Customer consolidation pressure",
            "Revenue decline even with unchanged market share"
        ])
    elif "key person leaves" in scenario_lower:
        scenario_risks.extend([
            "Loss of technical vision and direction",
            "Customer relationships at risk",
            "Remaining team may lack sufficient depth"
        ])
    elif "vc dries up" in scenario_lower:
        scenario_risks.extend([
            "Cannot invest in growth and product development",
            "May need to cut expenses/workforce",
            "Competitive disadvantage vs funded competitors"
        ])

    # Add baseline risks that intensify in crisis
    if baseline_risks:
        scenario_risks.extend([f"Baseline: {r}" for r in baseline_risks[:2]])

    return scenario_risks[:5]  # Limit to top 5
