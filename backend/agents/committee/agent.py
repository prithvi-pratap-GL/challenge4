"""Committee Agent - Final investment decision maker."""

from typing import Any, Dict, List
from backend.agents.schemas import CommitteeDecision
from backend.agents.committee.prompts import COMMITTEE_SYSTEM_PROMPT, COMMITTEE_USER_PROMPT_TEMPLATE


async def run_committee(
    bull_output: Dict[str, Any],
    bear_output: Dict[str, Any],
    red_team_output: Dict[str, Any],
    research_output: Dict[str, Any],
    knowledge_output: Dict[str, Any]
) -> CommitteeDecision:
    """
    Make final investment committee decision by synthesizing all perspectives.

    This agent acts as the managing partner, weighing arguments from Bull, Bear,
    and Red Team agents to make a grounded investment recommendation. The reasoning
    explicitly references the debate between perspectives.

    Args:
        bull_output: BullOutput from Bull Agent
            - investment_case: str (bullish narrative)
            - strengths: List[str] (opportunities)
            - confidence: int (0-100 in investment case)

        bear_output: BearOutput from Bear Agent
            - rejection_case: str (bearish narrative)
            - weaknesses: List[str] (risks)
            - confidence: int (0-100 in rejection case)

        red_team_output: RedTeamOutput from Red Team Agent
            - challenges: List[str] (specific challenges to claims)
            - contradictions: List[str] (contradictions between sources)
            - missing_evidence: List[str] (gaps in analysis)

        research_output: ResearchOutput from Research Agent
            - founders: List[str] (founder backgrounds)
            - competitors: List[str] (identified competitors)
            - market_summary: str (market analysis)
            - funding_summary: str (funding history)
            - industry_summary: str (industry context)

        knowledge_output: KnowledgeOutput from RAG Agent
            - startup_summary: str (company description)
            - business_model: str (revenue model)
            - risks: List[str] (identified risks)
            - financials: List[str] (financial metrics)
            - market_claims: List[str] (startup's claims)
            - evidence: List[str] (supporting evidence)

    Returns:
        CommitteeDecision with:
            - verdict: str (INVEST / PASS / CONDITIONAL)
            - confidence: int (0-100 confidence in decision)
            - reasoning: str (explicit references to all perspectives)

    Example:
        >>> bull = {"investment_case": "...", "strengths": [...], "confidence": 85}
        >>> bear = {"rejection_case": "...", "weaknesses": [...], "confidence": 75}
        >>> red_team = {"challenges": [...], "contradictions": [...], "missing_evidence": [...]}
        >>> research = {"founders": [...], "competitors": [...], ...}
        >>> knowledge = {"business_model": "...", "evidence": [...], ...}
        >>> result = await run_committee(bull, bear, red_team, research, knowledge)
        >>> assert isinstance(result, CommitteeDecision)
        >>> assert result.verdict in ["INVEST", "PASS", "CONDITIONAL"]
    """

    # Analyze the debate between Bull and Bear
    debate_analysis = _analyze_bull_vs_bear(bull_output, bear_output, red_team_output)

    # Evaluate Red Team challenges
    red_team_severity = _evaluate_red_team_challenges(red_team_output)

    # Assess research and knowledge completeness
    completeness_assessment = _assess_analysis_completeness(
        research_output, knowledge_output, red_team_output
    )

    # Make grounded decision
    decision = _make_investment_decision(
        debate_analysis, red_team_severity, completeness_assessment,
        bull_output, bear_output, red_team_output, research_output, knowledge_output
    )

    return decision


def _analyze_bull_vs_bear(
    bull_output: Dict[str, Any],
    bear_output: Dict[str, Any],
    red_team_output: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Analyze the debate between Bull and Bear arguments.

    Returns:
    - bull_stronger: bool (is Bull case stronger?)
    - confidence_gap: int (difference between Bull and Bear confidence)
    - contested_areas: List[str] (areas where they disagree)
    - unaddressed_bear_points: List[str] (Bear points Bull doesn't refute)
    """
    bull_confidence = bull_output.get("confidence", 50)
    bear_confidence = bear_output.get("confidence", 50)

    # Calculate confidence gap (positive = Bull stronger, negative = Bear stronger)
    confidence_gap = bull_confidence - bear_confidence

    # Identify unaddressed Bear points
    bull_strengths = set(s.lower() for s in bull_output.get("strengths", []))
    bear_weaknesses = bear_output.get("weaknesses", [])

    unaddressed = [
        weakness for weakness in bear_weaknesses
        if not any(strength.lower() in weakness.lower() for strength in bull_strengths)
    ]

    return {
        "bull_stronger": confidence_gap > 0,
        "confidence_gap": abs(confidence_gap),
        "contested_areas": min(len(bull_strengths), len(bear_weaknesses)),
        "unaddressed_bear_points": unaddressed
    }


def _evaluate_red_team_challenges(red_team_output: Dict[str, Any]) -> Dict[str, Any]:
    """
    Evaluate severity of Red Team challenges.

    Returns:
    - challenge_count: int (number of challenges)
    - contradiction_count: int (number of contradictions)
    - missing_evidence_count: int (number of gaps)
    - severity: str (LOW / MEDIUM / HIGH / CRITICAL)
    """
    challenges = red_team_output.get("challenges", [])
    contradictions = red_team_output.get("contradictions", [])
    missing_evidence = red_team_output.get("missing_evidence", [])

    total_issues = len(challenges) + len(contradictions) + len(missing_evidence)

    # Determine severity
    if len(contradictions) > 2 or total_issues > 8:
        severity = "CRITICAL"
    elif total_issues > 5:
        severity = "HIGH"
    elif total_issues > 2:
        severity = "MEDIUM"
    else:
        severity = "LOW"

    return {
        "challenge_count": len(challenges),
        "contradiction_count": len(contradictions),
        "missing_evidence_count": len(missing_evidence),
        "total_issues": total_issues,
        "severity": severity
    }


def _assess_analysis_completeness(
    research_output: Dict[str, Any],
    knowledge_output: Dict[str, Any],
    red_team_output: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Assess completeness of due diligence.

    Returns:
    - has_founder_analysis: bool
    - has_competitor_analysis: bool
    - has_market_data: bool
    - has_evidence: bool
    - is_complete: bool
    - gaps: List[str]
    """
    gaps = []

    # Check founder analysis
    has_founder_analysis = len(research_output.get("founders", [])) > 0
    if not has_founder_analysis:
        gaps.append("Founder background analysis missing")

    # Check competitor analysis
    has_competitor_analysis = len(research_output.get("competitors", [])) > 0
    if not has_competitor_analysis:
        gaps.append("Competitor analysis missing")

    # Check market data
    has_market_data = bool(research_output.get("market_summary"))
    if not has_market_data:
        gaps.append("Market data missing")

    # Check evidence quality
    evidence = knowledge_output.get("evidence", [])
    has_evidence = len(evidence) > 0
    if not has_evidence:
        gaps.append("Evidence supporting claims missing")

    # Check Red Team coverage
    red_team_issues = (
        len(red_team_output.get("challenges", [])) +
        len(red_team_output.get("contradictions", []))
    )
    if red_team_issues == 0:
        gaps.append("Red Team analysis shallow or missing")

    is_complete = all([has_founder_analysis, has_competitor_analysis, has_market_data, has_evidence])

    return {
        "has_founder_analysis": has_founder_analysis,
        "has_competitor_analysis": has_competitor_analysis,
        "has_market_data": has_market_data,
        "has_evidence": has_evidence,
        "is_complete": is_complete,
        "gaps": gaps
    }


def _make_investment_decision(
    debate_analysis: Dict[str, Any],
    red_team_severity: Dict[str, Any],
    completeness: Dict[str, Any],
    bull_output: Dict[str, Any],
    bear_output: Dict[str, Any],
    red_team_output: Dict[str, Any],
    research_output: Dict[str, Any],
    knowledge_output: Dict[str, Any]
) -> CommitteeDecision:
    """
    Make final investment decision based on synthesis of all inputs.

    Decision logic:
    - INVEST: Bull stronger, Red Team issues manageable, analysis complete
    - PASS: Bear stronger, critical Red Team issues, or analysis incomplete
    - CONDITIONAL: Mixed signals but potential if conditions met
    """

    # Build reasoning narrative
    reasoning_parts = []

    # Start with debate analysis
    if debate_analysis["bull_stronger"]:
        reasoning_parts.append(
            f"Bull case is stronger (confidence gap: +{debate_analysis['confidence_gap']}%). "
            f"Founder track record and market opportunity outweigh execution risks."
        )
    else:
        reasoning_parts.append(
            f"Bear case is stronger (confidence gap: {debate_analysis['confidence_gap']}%). "
            f"Execution risk and competitive threats are significant concerns."
        )

    # Address Red Team findings
    red_team_msg = (
        f"Red Team identified {red_team_severity['total_issues']} issues "
        f"({red_team_severity['contradiction_count']} contradictions, "
        f"{red_team_severity['missing_evidence_count']} evidence gaps). "
        f"Severity: {red_team_severity['severity']}."
    )
    reasoning_parts.append(red_team_msg)

    # Address completeness
    if completeness["gaps"]:
        gaps_str = ", ".join(completeness["gaps"])
        reasoning_parts.append(f"Analysis gaps: {gaps_str}.")
    else:
        reasoning_parts.append("Due diligence is thorough across all dimensions.")

    # Make verdict
    if not completeness["is_complete"]:
        verdict = "PASS"
        confidence = 40
        reasoning_parts.append(
            "RECOMMENDATION: PASS - Analysis incomplete. Cannot make confident investment decision."
        )
    elif red_team_severity["severity"] == "CRITICAL":
        verdict = "PASS"
        confidence = 35
        reasoning_parts.append(
            "RECOMMENDATION: PASS - Critical contradictions unresolved. Risk too high."
        )
    elif debate_analysis["bull_stronger"] and red_team_severity["severity"] in ["LOW", "MEDIUM"]:
        verdict = "INVEST"
        confidence = min(85, 50 + debate_analysis["confidence_gap"])
        reasoning_parts.append(
            "RECOMMENDATION: INVEST - Bull case compelling, Red Team issues manageable, "
            "founder execution track record strong."
        )
    elif not debate_analysis["bull_stronger"] and red_team_severity["severity"] in ["HIGH", "CRITICAL"]:
        verdict = "PASS"
        confidence = min(80, 50 + (100 - debate_analysis["confidence_gap"]))
        reasoning_parts.append(
            "RECOMMENDATION: PASS - Bear case stronger, Red Team issues serious, "
            "risk profile unfavorable."
        )
    else:
        verdict = "CONDITIONAL"
        confidence = 60
        reasoning_parts.append(
            "RECOMMENDATION: CONDITIONAL - Mixed signals. Consider follow-on investment "
            "contingent on: (1) Red Team challenge resolution, (2) Additional market validation, "
            "(3) Management milestones."
        )

    final_reasoning = " ".join(reasoning_parts)

    return CommitteeDecision(
        verdict=verdict,
        confidence=confidence,
        reasoning=final_reasoning
    )
