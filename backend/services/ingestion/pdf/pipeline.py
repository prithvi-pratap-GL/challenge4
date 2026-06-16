import asyncio
import logging
import os
import tempfile
import uuid
from typing import List, Protocol

import fitz  # PyMuPDF

from backend.domain.interfaces import IPdfParser
from backend.domain.schemas import Evidence, PageAnalysis, Source
from backend.infrastructure.embeddings.provider import get_embedding_provider
from backend.infrastructure.vectorstore.qdrant_client import (
    ensure_collections_exist,
    get_async_qdrant_client,
)

logger = logging.getLogger(__name__)


class SourceRepository(Protocol):
    """Protocol for Source persistence operations."""

    async def save(self, source: Source) -> None: ...


class EvidenceRepository(Protocol):
    """Protocol for Evidence persistence operations."""

    async def save(self, evidence: Evidence) -> None: ...


class PdfIngestionService:
    """
    Orchestrates the financial-grade PDF ingestion pipeline.
    Steps: Extraction & Rendering -> Concurrent Vision Analysis -> Chunking -> Vectorization & Storage -> Traceability.
    """

    def __init__(
        self,
        parser: IPdfParser,
        source_repo: SourceRepository,
        evidence_repo: EvidenceRepository,
    ):
        self.parser = parser
        self.source_repo = source_repo
        self.evidence_repo = evidence_repo
        self.embedding_provider = get_embedding_provider()
        self.qdrant_client = get_async_qdrant_client()
        self.semaphore = asyncio.Semaphore(2)  # Limit concurrency to avoid API rate limits

    async def initialize(self) -> None:
        """Ensure vector store collections are provisioned before ingestion."""
        await ensure_collections_exist()

    async def _parse_page_safely(
        self, image_path: str, raw_text: str, page_number: int
    ) -> PageAnalysis:
        """Parse a single page with concurrency control via semaphore."""
        async with self.semaphore:
            analysis = await self.parser.parse_page(image_path, raw_text)
            # Ensure page number is correctly set even if the model omits it
            analysis.page_number = page_number
            return analysis

    async def ingest(self, pdf_path: str, startup_id: str) -> None:
        """
        Execute the full ingestion pipeline for a given PDF file.
        """
        logger.info("Starting PDF ingestion pipeline for: %s", pdf_path)
        await self.initialize()

        pages_data: List[tuple[str, str, int]] = []

        # 1. Extraction & Rendering
        with tempfile.TemporaryDirectory() as temp_dir:
            doc = fitz.open(pdf_path)
            try:
                for page_num, page in enumerate(doc):
                    raw_text = page.get_text("text")
                    image_path = os.path.join(temp_dir, f"page_{page_num + 1}.png")
                    # Render at 150 DPI for optimal vision model performance
                    pix = page.get_pixmap(dpi=150)
                    pix.save(image_path)
                    pages_data.append((image_path, raw_text, page_num + 1))
            finally:
                doc.close()

            # 2. Concurrent Vision Analysis
            logger.info("Analyzing %d pages concurrently", len(pages_data))
            tasks = [
                self._parse_page_safely(img_path, text, p_num)
                for img_path, text, p_num in pages_data
            ]
            analyses: List[PageAnalysis] = await asyncio.gather(*tasks)

        # 3. Chunking Strategy & 4. Vectorization & Storage
        points = []
        source_id = str(uuid.uuid4())

        for analysis in analyses:
            # Prepend visual summary to text chunks so the embedding model has context
            chunk_text = (
                f"Visual Context: {analysis.visual_summary}\n\n"
                f"Claims: {', '.join(analysis.claims)}\n"
                f"Metrics: {', '.join(analysis.metrics)}"
            )

            vector = self.embedding_provider.embed(chunk_text)

            points.append(
                {
                    "id": uuid.uuid4().hex,
                    "vector": vector,
                    "payload": {
                        "startup_id": startup_id,
                        "document_id": pdf_path,
                        "page_number": analysis.page_number,
                        "page_type": analysis.page_type,
                        "text": chunk_text,
                        "entities": analysis.entities,
                        "metrics": analysis.metrics,
                    },
                }
            )

        # Upsert to Qdrant asynchronously
        if points:
            await self.qdrant_client.upsert(
                collection_name="pitch_deck_chunks", points=points
            )
            logger.info("Successfully upserted %d chunks to Qdrant", len(points))

        # 5. Traceability: Create Source and Evidence entities
        source = Source(
            id=source_id,
            document_type="pdf",
            file_path=pdf_path,
            startup_id=startup_id,
        )
        await self.source_repo.save(source)

        for analysis in analyses:
            evidence = Evidence(
                id=str(uuid.uuid4()),
                source_id=source_id,
                content=analysis.visual_summary,
                page_number=analysis.page_number,
                metadata={
                    "claims": analysis.claims,
                    "metrics": analysis.metrics,
                    "entities": analysis.entities,
                    "page_type": analysis.page_type,
                },
            )
            await self.evidence_repo.save(evidence)

        logger.info(
            "PDF ingestion pipeline completed successfully for: %s", pdf_path
        )