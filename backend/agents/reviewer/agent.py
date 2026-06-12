"""Reviewer Agent - Quality assurance and reflection loop trigger."""

from typing import Any, Dict, List, Optional
from backend.agents.schemas import ReviewOutput
from backend.agents.reviewer.prompts import REVIEWER_SYSTEM_PROMPT, REVIEWER_USER_PROMPT_TEMPLATE


async def review_analysis(
    bull_output: Optional[Dict[str, Any]],
    bear_output: Optional[Dict[str, Any]],
    red_team_output: Optional[Dict[str, Any]],
    research_output: Optional[Dict[str, Any]],
    knowledge_output: Optional[Dict[str, Any]]
) -> ReviewOutput:
    """
    Review the current analysis state for completeness, accuracy, and relevance.

    This agent evaluates outputs from Bull, Bear, and Red Team agents to determine
    if the analysis is ready for the Committee Agent or if the reflection loop should
    trigger re-analysis by previous agents.

    Args:
        bull_output: BullOutput from Bull Agent (optional)
            - investment_case: str
            - strengths: List[str]
            - confidence: int

        bear_output: BearOutput from Bear Agent (optional)
            - rejection_case: str
            - weaknesses: List[str]
            - confidence: int

        red_team_output: RedTeamOutput from Red Team Agent (optional)
            - challenges: List[str]
            - contradictions: List[str]
            - missing_evidence: List[str]

        research_output: ResearchOutput from Research Agent (optional)
            - founders: List[str]
            - competitors: List[str]
            - market_summary: str
            - funding_summary: str
            - industry_summary: str

        knowledge_output: KnowledgeOutput from RAG Agent (optional)
            - startup_summary: str
            - business_model: str
            - risks: List[str]
            - financials: List[str]
            - market_claims: List[str]
            - evidence: List[str]

    Returns:
        ReviewOutput with:
            - approved: bool - Is analysis ready for committee?
            - feedback: str - Specific feedback on gaps or issues
            - retry_required: bool - Should orchestrator re-trigger previous agents?

    Example:
        >>> bull = {"investment_case": "...", "strengths": [...], "confidence": 80}
        >>> bear = {"rejection_case": "...", "weaknesses": [...], "confidence": 70}
        >>> red_team = {"challenges": [...], "contradictions": [...], "missing_evidence": [...]}
        >>> research = {"founders": [...], "competitors": [...], ...}
        >>> knowledge = {"business_model": "...", "evidence": [...], ...}
        >>> result = await review_analysis(bull, bear, red_team, research, knowledge)
        >>> assert isinstance(result, ReviewOutput)
        >>> if result.retry_required:
        ...     # Orchestrator will re-trigger Bull/Bear/Red Team
        ...     pass
    """

    # Validate completeness of each analysis
    completeness_checks = _check_completeness(
        bull_output, bear_output, red_team_output, research_output, knowledge_output
    )

    # Validate accuracy of analyses
    accuracy_checks = _check_accuracy(
        bull_output, bear_output, red_team_output, knowledge_output
    )

    # Validate consistency between analyses
    consistency_checks = _check_consistency(
        bull_output, bear_output, red_team_output
    )

    # Compile feedback
    feedback_items = []
    retry_required = False

    # Add completeness feedback
    if completeness_checks["missing_analyses"]:
        feedback_items.append(
            f"Missing analyses: {', '.join(completeness_checks['missing_analyses'])}. "
            f"Trigger re-run of relevant agents."
        )
        retry_required = True

    if completeness_checks["shallow_analyses"]:
        feedback_items.append(
            f"Shallow analyses detected: {', '.join(completeness_checks['shallow_analyses'])}. "
            f"Provide more substantive, evidence-based analysis."
        )
        retry_required = True

    # Add accuracy feedback
    if accuracy_checks["issues"]:
        feedback_items.extend(accuracy_checks["issues"])
        retry_required = True

    # Add consistency feedback
    if consistency_checks["issues"]:
        feedback_items.extend(consistency_checks["issues"])

    # Determine approval status
    approved = not retry_required and len(feedback_items) == 0

    # Build final feedback
    if approved:
        final_feedback = (
            "Analysis approved. All perspectives (Bull, Bear, Red Team) are thorough, "
            "evidence-based, and ready for committee decision."
        )
    elif retry_required:
        final_feedback = "Analysis requires retry. " + " ".join(feedback_items)
    else:
        final_feedback = "Analysis has issues. " + " ".join(feedback_items)

    return ReviewOutput(
        approved=approved,
        feedback=final_feedback,
        retry_required=retry_required
    )


def _check_completeness(
    bull_output: Optional[Dict[str, Any]],
    bear_output: Optional[Dict[str, Any]],
    red_team_output: Optional[Dict[str, Any]],
    research_output: Optional[Dict[str, Any]],
    knowledge_output: Optional[Dict[str, Any]]
) -> Dict[str, Any]:
    """
    Check completeness of analysis coverage.

    Returns dict with:
    - missing_analyses: List of analyses not provided
    - shallow_analyses: List of analyses that are incomplete
    """
    missing = []
    shallow = []

    # Check each analysis is provided
    if bull_output is None:
        missing.append("Bull case")
    elif _is_shallow_analysis(bull_output.get("investment_case", "")):
        shallow.append("Bull case (investment narrative too brief)")

    if bear_output is None:
        missing.append("Bear case")
    elif _is_shallow_analysis(bear_output.get("rejection_case", "")):
        shallow.append("Bear case (rejection narrative too brief)")

    if red_team_output is None:
        missing.append("Red team analysis")
    elif len(red_team_output.get("challenges", [])) < 2:
        shallow.append("Red team (insufficient challenges identified)")

    if research_output is None:
        missing.append("Research findings")
    elif not research_output.get("competitors"):
        shallow.append("Research (no competitors identified)")

    if knowledge_output is None:
        missing.append("Knowledge base context")
    elif not knowledge_output.get("evidence"):
        shallow.append("Knowledge base (no evidence provided)")

    return {
        "missing_analyses": missing,
        "shallow_analyses": shallow
    }


def _check_accuracy(
    bull_output: Optional[Dict[str, Any]],
    bear_output: Optional[Dict[str, Any]],
    red_team_output: Optional[Dict[str, Any]],
    knowledge_output: Optional[Dict[str, Any]]
) -> Dict[str, Any]:
    """
    Check accuracy of analyses for hallucinations and unsupported claims.

    Returns dict with:
    - issues: List of accuracy issues found
    """
    issues = []

    # Check Bull output for substantive analysis
    if bull_output:
        if _contains_generic_language(bull_output.get("investment_case", "")):
            issues.append(
                "Bull case contains generic language without specific evidence. "
                "Provide concrete metrics and customer validation."
            )

    # Check Bear output for substantive analysis
    if bear_output:
        if _contains_generic_language(bear_output.get("rejection_case", "")):
            issues.append(
                "Bear case contains generic risks without specificity. "
                "Identify concrete risks relevant to this company."
            )

    # Check Red Team for specific contradictions
    if red_team_output:
        if len(red_team_output.get("contradictions", [])) == 0:
            issues.append(
                "Red team found no contradictions. "
                "Deeper analysis needed to compare claims vs research."
            )

    # Check Knowledge for evidence quality
    if knowledge_output:
        market_claims = knowledge_output.get("market_claims", [])
        evidence = knowledge_output.get("evidence", [])
        if len(market_claims) > len(evidence):
            issues.append(
                f"More claims ({len(market_claims)}) than evidence ({len(evidence)}). "
                f"Validate all market claims with third-party sources."
            )

    return {"issues": issues}


def _check_consistency(
    bull_output: Optional[Dict[str, Any]],
    bear_output: Optional[Dict[str, Any]],
    red_team_output: Optional[Dict[str, Any]]
) -> Dict[str, Any]:
    """
    Check consistency between different analyses.

    Returns dict with:
    - issues: List of consistency issues
    """
    issues = []

    # Check that Bull and Bear address same company aspects
    if bull_output and bear_output:
        bull_strengths = set(s.lower() for s in bull_output.get("strengths", []))
        bear_weaknesses = set(w.lower() for w in bear_output.get("weaknesses", []))

        # Some overlap is expected but not complete (both shouldn't focus only on same areas)
        if not bull_strengths and not bear_weaknesses:
            issues.append(
                "Bull and Bear analyses lack specific details. "
                "Provide concrete strengths/weaknesses, not generic statements."
            )

    # Check that Red Team challenges are substantive
    if red_team_output:
        red_challenges = red_team_output.get("challenges", [])
        if red_challenges and all(_is_generic_challenge(c) for c in red_challenges):
            issues.append(
                "Red team challenges are too generic. "
                "Identify specific contradictions in the startup's claims."
            )

    return {"issues": issues}


def _is_shallow_analysis(text: str) -> bool:
    """Check if analysis is too brief to be substantive."""
    if not text:
        return True
    word_count = len(text.split())
    return word_count < 50  # Less than 50 words is likely too shallow


def _contains_generic_language(text: str) -> bool:
    """Check if text relies on generic statements without specifics."""
    generic_phrases = [
        "potentially",
        "could be",
        "might",
        "seems to",
        "appears to",
        "likely to",
        "probably"
    ]

    if not text:
        return False

    text_lower = text.lower()
    generic_count = sum(1 for phrase in generic_phrases if phrase in text_lower)

    # If more than 30% generic language, it's too vague
    total_words = len(text.split())
    return (generic_count / max(1, total_words)) > 0.3


def _is_generic_challenge(challenge: str) -> bool:
    """Check if a challenge is too generic (not specific to this startup)."""
    generic_keywords = [
        "execution risk",
        "market risk",
        "technology risk",
        "competition",
        "scaling",
        "profitability"
    ]

    challenge_lower = challenge.lower()
    # If challenge is ONLY these generic terms with no specifics, it's too generic
    return all(keyword not in challenge_lower for keyword in ["specifically", "this", "their", "the startup"])
