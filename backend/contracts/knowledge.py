"""
Knowledge Intelligence Input Contract
Person 3 consumes this contract from Person 2's research output
Defines the input format for RAG pipeline, ingestion, and embeddings
"""

from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional


@dataclass
class KnowledgeSource:
    """Individual source document for knowledge base"""
    url: str
    title: str
    content: str  # Markdown content from Firecrawl
    source_type: str  # "founder_bio", "competitor_analysis", "market_report", etc.
    metadata: Dict[str, Any] = field(default_factory=dict)
    chunks: List[str] = field(default_factory=list)  # Text chunks for embedding


@dataclass
class KnowledgeInput:
    """
    Input contract for Person 3's RAG pipeline

    Receives enriched research output from Person 2 and processes for:
    - PDF ingestion (if provided)
    - Vision analysis (if images present)
    - Embedding generation
    - Vector storage in Qdrant
    - Memory management
    """
    startup_name: str

    # From Person 2's research
    research_data: Dict[str, Any]  # Full ResearchOutput as dict

    # Enriched content from Firecrawl
    enriched_sources: List[KnowledgeSource] = field(default_factory=list)

    # Optional: Startup documents provided by user
    documents: List[Dict[str, Any]] = field(default_factory=list)  # PDFs, pitch decks, etc.

    # Metadata
    timestamp: str = ""
    source_person: str = "Person2"  # Who provided this data

    def get_all_content(self) -> str:
        """Get all enriched content as single text for processing"""
        content_parts = []

        # Add research summaries
        if "market_summary" in self.research_data:
            content_parts.append(f"Market Analysis:\n{self.research_data['market_summary']}\n")

        if "funding_summary" in self.research_data:
            content_parts.append(f"Funding History:\n{self.research_data['funding_summary']}\n")

        if "industry_summary" in self.research_data:
            content_parts.append(f"Industry Analysis:\n{self.research_data['industry_summary']}\n")

        # Add enriched source content
        for source in self.enriched_sources:
            content_parts.append(f"\n--- Source: {source.title} ---\n{source.content}\n")

        return "\n".join(content_parts)

    def to_dict(self):
        """Convert to dictionary for serialization"""
        return {
            "startup_name": self.startup_name,
            "research_data": self.research_data,
            "enriched_sources": [
                {
                    "url": s.url,
                    "title": s.title,
                    "content": s.content,
                    "source_type": s.source_type,
                    "metadata": s.metadata
                }
                for s in self.enriched_sources
            ],
            "documents": self.documents,
            "timestamp": self.timestamp,
            "source_person": self.source_person
        }


@dataclass
class KnowledgeOutput:
    """
    Output contract from Person 3's knowledge processing

    Person 3 produces this after:
    - Ingesting PDFs and processing documents
    - Generating embeddings
    - Storing in Qdrant
    - Building memory index
    """
    startup_name: str

    # Embedded knowledge
    embedded_sources: Dict[str, Any] = field(default_factory=dict)  # URL -> embedding metadata

    # Vector store references
    vector_store_id: str = ""
    vector_collection_name: str = ""

    # Processed documents
    processed_documents: List[Dict[str, Any]] = field(default_factory=list)

    # Ingestion stats
    total_chunks: int = 0
    embedded_chunks: int = 0

    # Memory index
    memory_index: Dict[str, Any] = field(default_factory=dict)

    # Status
    success: bool = True
    error_message: str = ""

    def to_dict(self):
        return {
            "startup_name": self.startup_name,
            "embedded_sources": self.embedded_sources,
            "vector_store_id": self.vector_store_id,
            "vector_collection_name": self.vector_collection_name,
            "processed_documents": self.processed_documents,
            "total_chunks": self.total_chunks,
            "embedded_chunks": self.embedded_chunks,
            "memory_index": self.memory_index,
            "success": self.success,
            "error_message": self.error_message
        }
