"""Bull Agent - Builds the strongest investment case."""

from typing import Any, Dict, List
from backend.agents.schemas import BullOutput
from backend.agents.bull.prompts import BULL_SYSTEM_PROMPT, BULL_USER_PROMPT_TEMPLATE


# Placeholder for Person 5's LLM wrapper integration
# This will be replaced with actual LLM client once Person 5 provides it
class LLMClientPlaceholder:
    """Temporary placeholder - will be replaced by Person 5's llm.client module."""

    async def generate(
        self,
        system_prompt: str,
        user_prompt: str,
        response_model: type
    ) -> Any:
        """Generate response from LLM with structured output."""
        raise NotImplementedError(
            "LLM client not yet integrated. Awaiting Person 5's llm.client module."
        )


async def run_bull_case(
    research_output: Dict[str, Any],
    knowledge_output: Dict[str, Any]
) -> BullOutput:
    """
    Build the strongest possible investment case for a startup.

    This agent analyzes research findings and knowledge base context to construct
    a compelling bullish narrative highlighting founder credibility, market opportunity,
    competitive advantages, and growth potential.

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
        BullOutput with:
            - investment_case: Comprehensive bullish narrative (3-4 paragraphs)
            - strengths: 6-8 key strengths and opportunities
            - confidence: 0-100 confidence score in the investment

    Example:
        >>> research = {
        ...     "founders": ["Jane Doe (ex-Google)"],
        ...     "competitors": ["Competitor A", "Competitor B"],
        ...     "market_summary": "$50B TAM, growing 40% YoY",
        ...     "funding_summary": "Seed round $2M from top-tier investors",
        ...     "industry_summary": "AI-driven SaaS in enterprise",
        ...     "sources": ["Crunchbase", "LinkedIn"]
        ... }
        >>> knowledge = {
        ...     "startup_summary": "AI-powered data analytics platform",
        ...     "business_model": "PLG SaaS, $5K-50K ACV",
        ...     "risks": ["Competitive threat from large vendors"],
        ...     "financials": ["$500K MRR, 120% NRR"],
        ...     "market_claims": ["Fastest data processing in category"],
        ...     "evidence": ["3 Fortune 500 customers", "50% QoQ growth"]
        ... }
        >>> result = await run_bull_case(research, knowledge)
        >>> assert isinstance(result, BullOutput)
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
    user_prompt = BULL_USER_PROMPT_TEMPLATE.format(
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
    #     system_prompt=BULL_SYSTEM_PROMPT,
    #     user_prompt=user_prompt,
    #     response_model=BullOutput
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
