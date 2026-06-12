"""Red Team Agent - Adversarial fact-checker and contradiction identifier."""

from typing import Any, Dict, List
from backend.agents.schemas import RedTeamOutput
from backend.agents.red_team.prompts import RED_TEAM_SYSTEM_PROMPT, RED_TEAM_USER_PROMPT_TEMPLATE
from backend.llm.client import LLMClient


async def run_red_team(
    research_output: Dict[str, Any],
    knowledge_output: Dict[str, Any]
) -> RedTeamOutput:
    """
    Run adversarial fact-checking and contradiction detection.

    This agent analyzes startup claims against external research to identify:
    - Unsupported or contradicted claims
    - Contradictions between sources
    - Missing critical evidence
    - Logical fallacies and risky assumptions

    Args:
        research_output: ResearchOutput containing:
            - founders: List[str] - Founder names and backgrounds
            - competitors: List[str] - Identified competitors
            - market_summary: str - Market opportunity analysis
            - funding_summary: str - Historical funding information
            - industry_summary: str - Industry context
            - sources: List[str] - Source references

        knowledge_output: KnowledgeOutput containing:
            - startup_summary: str - Company overview
            - business_model: str - Business model description
            - risks: List[str] - Identified risks
            - financials: List[str] - Financial data points
            - market_claims: List[str] - Startup's market claims
            - evidence: List[str] - Supporting evidence

    Returns:
        RedTeamOutput with:
            - challenges: List of specific challenges to claims
            - contradictions: List of contradictions found
            - missing_evidence: List of gaps in due diligence

    Example:
        >>> research = {
        ...     "founders": ["CEO (new to market)"],
        ...     "competitors": ["20+ direct competitors", "Google entering"],
        ...     "market_summary": "Saturated, declining margins",
        ...     "funding_summary": "Seed from tier-2 investors",
        ...     "industry_summary": "Consolidation trend",
        ...     "sources": ["Crunchbase", "LinkedIn"]
        ... }
        >>> knowledge = {
        ...     "startup_summary": "AI governance platform",
        ...     "business_model": "$5K-50K ACV",
        ...     "risks": ["Competition", "Tech risk"],
        ...     "financials": ["$300K MRR"],
        ...     "market_claims": ["Only real-time governance", "10x faster"],
        ...     "evidence": ["3 customers", "no independent validation"]
        ... }
        >>> result = await run_red_team(research, knowledge)
        >>> assert isinstance(result, RedTeamOutput)
        >>> assert len(result.challenges) > 0
        >>> assert len(result.contradictions) > 0
    """

    # Extract data from research and knowledge outputs
    founders = _format_list(research_output.get("founders", []))
    competitors = _format_list(research_output.get("competitors", []))
    market_summary = research_output.get("market_summary", "")
    funding_summary = research_output.get("funding_summary", "")
    industry_summary = research_output.get("industry_summary", "")

    business_model = knowledge_output.get("business_model", "")
    market_claims = _format_list(knowledge_output.get("market_claims", []))
    evidence = _format_list(knowledge_output.get("evidence", []))
    identified_risks = _format_list(knowledge_output.get("risks", []))
    startup_name = knowledge_output.get("startup_summary", "Startup").split("\n")[0]

    # Build the user prompt with extracted data
    user_prompt = RED_TEAM_USER_PROMPT_TEMPLATE.format(
        startup_name=startup_name,
        founders=founders,
        funding_summary=funding_summary,
        competitors=competitors,
        market_summary=market_summary,
        industry_summary=industry_summary,
        business_model=business_model,
        market_claims=market_claims,
        evidence=evidence,
        identified_risks=identified_risks
    )

    # Integrate with LLM client
    llm_client = LLMClient()
    response = await llm_client.generate(
        system_prompt=RED_TEAM_SYSTEM_PROMPT,
        user_prompt=user_prompt,
        response_model=RedTeamOutput
    )
    return response


def _format_list(items: List[str]) -> str:
    """Format a list of strings for inclusion in prompts."""
    if not items:
        return "None provided"
    return "\n- " + "\n- ".join(items)


def _compare_claims_to_research(
    market_claims: List[str],
    competitors: List[str],
    market_summary: str
) -> List[str]:
    """
    Helper function to find contradictions between claims and research.

    This is a utility for testing the contradiction-finding logic
    before LLM integration.
    """
    contradictions = []

    # Check for claim of uniqueness vs known competitors
    unique_claims = [c for c in market_claims if "only" in c.lower() or "unique" in c.lower()]
    if unique_claims and competitors:
        contradictions.append(
            f"Claim of uniqueness contradicted by {len(competitors)} identified competitors"
        )

    # Check for market opportunity claims vs market saturation
    if "saturated" in market_summary.lower() or "commoditized" in market_summary.lower():
        opportunity_claims = [c for c in market_claims if "opportunity" in c.lower() or "large" in c.lower()]
        if opportunity_claims:
            contradictions.append(
                "Claims of market opportunity contradict research showing market saturation"
            )

    return contradictions
