"""Bear Agent - Builds the strongest rejection case."""

from typing import Any, Dict, List
from backend.agents.schemas import BearOutput
from backend.agents.bear.prompts import BEAR_SYSTEM_PROMPT, BEAR_USER_PROMPT_TEMPLATE


async def run_bear_case(
    research_output: Dict[str, Any],
    knowledge_output: Dict[str, Any]
) -> BearOutput:
    """
    Build the strongest possible rejection case for a startup.

    This agent analyzes research findings and knowledge base context to construct
    a compelling bearish narrative highlighting execution risks, competitive threats,
    market limitations, and reasons to pass on the investment.

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
        BearOutput with:
            - rejection_case: Comprehensive bearish narrative (3-4 paragraphs)
            - weaknesses: 6-8 key weaknesses and risks identified
            - confidence: 0-100 confidence score in the rejection case

    Example:
        >>> research = {
        ...     "founders": ["Jane Doe (failed startup 2x)"],
        ...     "competitors": ["Incumbent A", "Incumbent B", "10+ startups"],
        ...     "market_summary": "$50B TAM but highly saturated",
        ...     "funding_summary": "Seed round from unknown VCs",
        ...     "industry_summary": "Commoditized AI-driven SaaS",
        ...     "sources": ["Crunchbase", "LinkedIn"]
        ... }
        >>> knowledge = {
        ...     "startup_summary": "Another AI-powered SaaS tool",
        ...     "business_model": "Unsustainable pricing, negative unit economics",
        ...     "risks": ["Tech risk", "Market risk", "Execution risk"],
        ...     "financials": ["Burning $500K/month", "3-month runway"],
        ...     "market_claims": ["We're the fastest (unverified)"],
        ...     "evidence": []
        ... }
        >>> result = await run_bear_case(research, knowledge)
        >>> assert isinstance(result, BearOutput)
        >>> assert 0 <= result.confidence <= 100
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
    user_prompt = BEAR_USER_PROMPT_TEMPLATE.format(
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

    # TODO: Integrate with Person 5's LLM wrapper once available
    # For now, this demonstrates the expected integration pattern
    # llm_client = LLMClient()  # Person 5's client
    # response = await llm_client.generate(
    #     system_prompt=BEAR_SYSTEM_PROMPT,
    #     user_prompt=user_prompt,
    #     response_model=BearOutput
    # )
    # return response

    # Temporary: Return a placeholder to demonstrate function structure
    raise NotImplementedError(
        "Awaiting Person 5's LLM client integration in backend.llm.client"
    )


def _format_list(items: List[str]) -> str:
    """Format a list of strings for inclusion in prompts."""
    if not items:
        return "None provided"
    return "\n- " + "\n- ".join(items)
