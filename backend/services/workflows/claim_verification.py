"""
VentureMind AI — Claim Verification Agent
LangGraph workflow for verifying startup claims against ingested evidence.

Orchestrates a two-node graph: evidence retrieval → LLM-based evaluation.
Enforces traceability and strict multi-tenant isolation at every step.
"""

import json
import logging
from typing import List, TypedDict

from langgraph.graph import END, StateGraph
from openai import AsyncOpenAI

from backend.core.settings import settings
from backend.domain.interfaces import IRetrievalService
from backend.domain.schemas import RetrievedChunk

logger = logging.getLogger(__name__)


class VerificationState(TypedDict):
    """
    Typed state dictionary for claim verification workflow.

    Tracks the claim, evidence, and LLM judgment throughout the workflow.
    """

    claim_text: str
    deal_id: str
    retrieved_evidence: List[RetrievedChunk]
    verification_status: str  # PENDING, VERIFIED, CONTRADICTED, UNVERIFIED, UNVERIFIABLE
    reasoning: str
    supporting_chunk_ids: List[str]


class ClaimVerificationWorkflow:
    """
    Production-ready claim verification workflow using LangGraph.

    Workflow:
    1. retrieve_evidence: Search Qdrant for evidence related to the claim
    2. evaluate_claim: Use LLM to compare claim against retrieved evidence

    Features:
    - Strict traceability (chunk_id links to evidence)
    - Multi-tenant isolation via deal_id
    - Type-safe state management with TypedDict
    - Graceful handling of missing evidence
    - JSON-mode LLM output for deterministic parsing
    """

    def __init__(
        self,
        retrieval_service: IRetrievalService,
    ):
        """
        Initialize the claim verification workflow.

        Args:
            retrieval_service: IRetrievalService instance for evidence retrieval.
        """
        self.retrieval_service = retrieval_service
        self.llm_client = AsyncOpenAI(
            api_key=settings.hf_router_api_key,
            base_url=settings.hf_router_base_url,
        )
        self.llm_model = settings.llm_model_name

        # Build and compile the LangGraph
        self.graph = self._build_graph()
        logger.info("✓ Claim verification workflow initialized")

    def _build_graph(self) -> StateGraph:
        """
        Build and compile the LangGraph workflow.

        Graph structure:
        retrieve_evidence → evaluate_claim → END

        Returns:
            Compiled StateGraph instance.
        """
        workflow = StateGraph(VerificationState)

        # Add nodes
        workflow.add_node("retrieve_evidence", self._retrieve_evidence_node)
        workflow.add_node("evaluate_claim", self._evaluate_claim_node)

        # Add edges
        workflow.set_entry_point("retrieve_evidence")
        workflow.add_edge("retrieve_evidence", "evaluate_claim")
        workflow.add_edge("evaluate_claim", END)

        # Compile
        compiled_graph = workflow.compile()
        logger.info("✓ LangGraph compiled successfully")
        return compiled_graph

    async def _retrieve_evidence_node(
        self, state: VerificationState
    ) -> VerificationState:
        """
        Node 1: Retrieve evidence from Qdrant.

        Uses the injected retrieval service to search for evidence
        related to the claim. Updates state with retrieved chunks.

        Args:
            state: Current workflow state.

        Returns:
            Updated state with retrieved_evidence populated.
        """
        logger.info(
            f"[Node: retrieve_evidence] Searching for evidence "
            f"claim='{state['claim_text'][:60]}...' deal_id={state['deal_id']}"
        )

        try:
            # Search Qdrant for evidence
            response = await self.retrieval_service.search(
                query=state["claim_text"],
                deal_id=state["deal_id"],
                top_k=5,  # Retrieve top 5 relevant chunks
            )

            retrieved_evidence = response.results
            logger.info(
                f"  ✓ Retrieved {len(retrieved_evidence)} evidence chunks "
                f"in {response.execution_time_ms:.2f}ms"
            )

            # Log retrieved evidence for debugging
            for i, chunk in enumerate(retrieved_evidence, 1):
                logger.debug(
                    f"    [{i}] chunk_id={chunk.chunk_id} score={chunk.score:.4f} "
                    f"source={chunk.source_id}"
                )

            # Update state
            state["retrieved_evidence"] = retrieved_evidence

            if not retrieved_evidence:
                logger.warning("  ⚠ No evidence found in Qdrant")
                state["verification_status"] = "UNVERIFIABLE"
                state["reasoning"] = "No relevant evidence found in knowledge base"
                state["supporting_chunk_ids"] = []

            return state

        except Exception as e:
            logger.error(f"  ✗ Failed to retrieve evidence: {e}", exc_info=True)
            state["verification_status"] = "UNVERIFIABLE"
            state["reasoning"] = f"Failed to retrieve evidence: {e}"
            state["retrieved_evidence"] = []
            state["supporting_chunk_ids"] = []
            return state

    async def _evaluate_claim_node(
        self, state: VerificationState
    ) -> VerificationState:
        """
        Node 2: Evaluate claim using LLM.

        Compares the claim against retrieved evidence using an LLM judge.
        The LLM returns structured JSON with verification status, reasoning,
        and supporting chunk IDs for full traceability.

        Args:
            state: Current workflow state (populated by retrieve_evidence).

        Returns:
            Updated state with verification_status, reasoning, and supporting_chunk_ids.
        """
        logger.info(
            f"[Node: evaluate_claim] Evaluating claim against "
            f"{len(state['retrieved_evidence'])} evidence chunks"
        )

        # If no evidence, skip LLM evaluation
        if not state["retrieved_evidence"]:
            logger.warning("  ⚠ No evidence to evaluate, skipping LLM")
            return state

        try:
            # Build evidence context for LLM
            evidence_context = self._build_evidence_context(state["retrieved_evidence"])

            # Construct system prompt
            system_prompt = (
                "You are an expert auditor verifying startup claims. "
                "Analyze the CLAIM against the provided EVIDENCE. "
                "Return a JSON object with:\n"
                '- "status": one of VERIFIED, CONTRADICTED, UNVERIFIED (not enough info)\n'
                '- "reasoning": your detailed explanation (2-3 sentences)\n'
                '- "supporting_chunk_ids": list of chunk IDs that support your verdict\n'
                "\nBe precise. Only mark VERIFIED if the evidence directly supports the claim. "
                "Only mark CONTRADICTED if evidence directly contradicts it. "
                "Otherwise, mark UNVERIFIED."
            )

            user_prompt = (
                f"CLAIM: {state['claim_text']}\n\n"
                f"EVIDENCE:\n{evidence_context}"
            )

            logger.debug(f"LLM Input:\nSystem: {system_prompt}\nUser: {user_prompt}")

            # Call LLM with JSON mode
            response = await self.llm_client.chat.completions.create(
                model=self.llm_model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt},
                ],
                response_format={"type": "json_object"},
                temperature=0.0,  # Deterministic evaluation
                max_tokens=500,
            )

            response_text = response.choices[0].message.content
            logger.debug(f"LLM Response: {response_text}")

            # Parse JSON response
            evaluation = json.loads(response_text)

            # Extract fields with validation
            verification_status = evaluation.get("status", "UNVERIFIED").upper()
            reasoning = evaluation.get("reasoning", "No reasoning provided")
            supporting_chunk_ids = evaluation.get("supporting_chunk_ids", [])

            # Validate status
            valid_statuses = ["VERIFIED", "CONTRADICTED", "UNVERIFIED", "UNVERIFIABLE"]
            if verification_status not in valid_statuses:
                logger.warning(
                    f"  ⚠ Invalid status '{verification_status}' from LLM, "
                    f"defaulting to UNVERIFIED"
                )
                verification_status = "UNVERIFIED"

            # Validate supporting chunk IDs (must exist in retrieved evidence)
            available_chunk_ids = {
                chunk.chunk_id for chunk in state["retrieved_evidence"]
            }
            valid_supporting_ids = [
                cid for cid in supporting_chunk_ids if cid in available_chunk_ids
            ]

            if len(valid_supporting_ids) < len(supporting_chunk_ids):
                logger.warning(
                    f"  ⚠ LLM referenced non-existent chunks. "
                    f"Valid: {valid_supporting_ids}"
                )

            # Update state
            state["verification_status"] = verification_status
            state["reasoning"] = reasoning
            state["supporting_chunk_ids"] = valid_supporting_ids

            logger.info(
                f"  ✓ Evaluation complete: status={verification_status} "
                f"supporting_chunks={len(valid_supporting_ids)}"
            )

            return state

        except json.JSONDecodeError as e:
            logger.error(f"  ✗ Failed to parse LLM JSON response: {e}")
            state["verification_status"] = "UNVERIFIABLE"
            state["reasoning"] = "Failed to parse LLM evaluation"
            state["supporting_chunk_ids"] = []
            return state

        except Exception as e:
            logger.error(
                f"  ✗ LLM evaluation failed ({type(e).__name__}): {e}",
                exc_info=True,
            )
            state["verification_status"] = "UNVERIFIABLE"
            state["reasoning"] = f"LLM evaluation failed: {e}"
            state["supporting_chunk_ids"] = []
            return state

    def _build_evidence_context(
        self, retrieved_chunks: List[RetrievedChunk]
    ) -> str:
        """
        Build a formatted context string from retrieved evidence chunks.

        Args:
            retrieved_chunks: List of RetrievedChunk objects.

        Returns:
            Formatted string for LLM consumption.
        """
        if not retrieved_chunks:
            return "No evidence found."

        context_parts = []
        for i, chunk in enumerate(retrieved_chunks, 1):
            # Format: [1] (chunk_id, score) text...
            context_parts.append(
                f"[{i}] (chunk_id={chunk.chunk_id}, score={chunk.score:.4f})\n"
                f"    Source: {chunk.metadata.get('url', 'unknown')}\n"
                f"    Category: {chunk.metadata.get('category', 'unknown')}\n"
                f"    Text: {chunk.text[:300]}{'...' if len(chunk.text) > 300 else ''}\n"
            )

        return "\n".join(context_parts)

    async def verify_claim(self, claim: str, deal_id: str) -> VerificationState:
        """
        Verify a claim using the compiled LangGraph workflow.

        Main entry point for claim verification. Orchestrates the full
        workflow from evidence retrieval to LLM evaluation.

        Args:
            claim: The claim text to verify.
            deal_id: The deal/startup ID for strict isolation.

        Returns:
            Final VerificationState with complete verification results.

        Raises:
            Exception: If the workflow fails critically.
        """
        logger.info("=" * 80)
        logger.info(f"Starting claim verification: '{claim[:80]}...'")
        logger.info(f"Deal ID: {deal_id}")
        logger.info("=" * 80)

        # Initialize state
        initial_state: VerificationState = {
            "claim_text": claim,
            "deal_id": deal_id,
            "retrieved_evidence": [],
            "verification_status": "PENDING",
            "reasoning": "",
            "supporting_chunk_ids": [],
        }

        try:
            # Invoke the compiled graph
            final_state = await self.graph.ainvoke(initial_state)

            logger.info("\n" + "=" * 80)
            logger.info("✓ Claim verification completed")
            logger.info(f"  Status: {final_state['verification_status']}")
            logger.info(f"  Reasoning: {final_state['reasoning']}")
            logger.info(
                f"  Supporting Chunks: {final_state['supporting_chunk_ids']}"
            )
            logger.info(f"  Evidence Retrieved: {len(final_state['retrieved_evidence'])}")
            logger.info("=" * 80)

            return final_state

        except Exception as e:
            logger.error(
                f"✗ Claim verification workflow failed: {type(e).__name__}: {e}",
                exc_info=True,
            )
            raise
