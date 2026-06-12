"""
Person 2 → Person 3 Handoff Service
Converts Research Intelligence output to Knowledge Intelligence input
Handles the contract transition between research and RAG pipeline
"""

from typing import List, Dict, Any
from datetime import datetime
from backend.contracts.research import ResearchOutput
from backend.contracts.knowledge import KnowledgeInput, KnowledgeSource


class Person3Handoff:
    """
    Converts Person 2's research output to Person 3's knowledge input

    Flow:
    1. Person 2 runs research → ResearchOutput
    2. Person3Handoff.convert() → KnowledgeInput
    3. Person 3 ingests and processes → KnowledgeOutput
    """

    @staticmethod
    def convert(research_output: ResearchOutput, startup_name: str) -> KnowledgeInput:
        """
        Convert ResearchOutput to KnowledgeInput for Person 3's RAG pipeline

        Args:
            research_output: Output from Person 2's research workflow
            startup_name: Name of the startup being analyzed

        Returns:
            KnowledgeInput ready for Person 3's ingestion pipeline
        """
        # Convert enriched sources to knowledge sources
        knowledge_sources = Person3Handoff._extract_knowledge_sources(research_output)

        # Create knowledge input
        knowledge_input = KnowledgeInput(
            startup_name=startup_name,
            research_data=research_output.to_dict(),
            enriched_sources=knowledge_sources,
            timestamp=datetime.utcnow().isoformat(),
            source_person="Person2"
        )

        return knowledge_input

    @staticmethod
    def _extract_knowledge_sources(research_output: ResearchOutput) -> List[KnowledgeSource]:
        """
        Extract enriched sources from research output as KnowledgeSources

        Converts Firecrawl markdown into structured knowledge sources
        """
        knowledge_sources = []

        enriched = research_output.enriched_sources or {}

        for url, enriched_data in enriched.items():
            if enriched_data.get("status") != "success":
                continue  # Skip failed enrichments

            markdown = enriched_data.get("markdown", "")
            if not markdown:
                continue  # Skip empty content

            # Determine source type from URL and content
            source_type = Person3Handoff._infer_source_type(url, markdown)

            # Create knowledge source
            source = KnowledgeSource(
                url=url,
                title=enriched_data.get("metadata", {}).get("title", url),
                content=markdown,
                source_type=source_type,
                metadata={
                    "url": url,
                    "status": enriched_data.get("status"),
                    "extracted_at": datetime.utcnow().isoformat(),
                    "content_length": len(markdown),
                    "links": enriched_data.get("links", [])
                }
            )

            knowledge_sources.append(source)

        return knowledge_sources

    @staticmethod
    def _infer_source_type(url: str, content: str) -> str:
        """Infer the type of source based on URL and content"""
        url_lower = url.lower()
        content_lower = content.lower()

        # Check URL patterns
        if "wikipedia" in url_lower and ("founder" in content_lower or "ceo" in content_lower):
            return "founder_bio"
        elif "wikipedia" in url_lower:
            return "company_wiki"
        elif "linkedin" in url_lower:
            return "professional_profile"
        elif "crunchbase" in url_lower:
            return "funding_data"
        elif "techcrunch" in url_lower or "forbes" in url_lower:
            return "press_coverage"
        elif "market" in url_lower or "statista" in url_lower:
            return "market_research"
        elif "competitor" in url_lower or "alternative" in url_lower:
            return "competitor_analysis"

        # Check content patterns
        if any(word in content_lower for word in ["competitor", "alternative", "vs ", "comparison"]):
            return "competitor_analysis"
        elif any(word in content_lower for word in ["market size", "tam", "addressable"]):
            return "market_research"
        elif any(word in content_lower for word in ["funding", "series a", "investor", "raised"]):
            return "funding_data"
        elif any(word in content_lower for word in ["founder", "ceo", "biography", "background"]):
            return "founder_bio"

        return "general_research"

    @staticmethod
    def save_handoff(knowledge_input: KnowledgeInput, output_path: str = None) -> str:
        """
        Save Person 3 handoff to JSON for manual review/transfer

        Args:
            knowledge_input: Converted knowledge input
            output_path: Optional custom output path

        Returns:
            Path to saved handoff file
        """
        import json
        from pathlib import Path
        from datetime import datetime

        if not output_path:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_dir = Path("research_results/handoffs")
            output_dir.mkdir(parents=True, exist_ok=True)
            output_path = str(output_dir / f"{knowledge_input.startup_name}_handoff_{timestamp}.json")

        # Save handoff
        with open(output_path, "w") as f:
            json.dump(knowledge_input.to_dict(), f, indent=2)

        print(f"[HANDOFF] Person 3 input saved to {output_path}")
        return output_path


# Example usage documentation
HANDOFF_EXAMPLE = """
# Person 2 → Person 3 Handoff Example

```python
from backend.agents.research.workflow import ResearchWorkflow
from backend.contracts.startup import StartupInput
from backend.services.handoff.person3_handoff import Person3Handoff

# Person 2: Run research
startup = StartupInput(startup_name="OpenAI")
workflow = ResearchWorkflow()
research_output = workflow.run_research(startup)

# Handoff to Person 3
knowledge_input = Person3Handoff.convert(research_output, "OpenAI")

# Person 3 can now:
# - Access research_output.research_data (summaries, founders, competitors, etc.)
# - Access knowledge_input.enriched_sources (full markdown for embedding)
# - Process with RAG pipeline
# - Store in Qdrant

# Example: Person 3 accesses enriched content
for source in knowledge_input.enriched_sources:
    print(f"Processing: {source.title}")
    print(f"Type: {source.source_type}")
    print(f"Content length: {len(source.content)} chars")
    # → Generate embeddings
    # → Store in vector DB
```

## Data Flow

```
ResearchOutput (Person 2)
    ├─ founders: [...]
    ├─ competitors: [...]
    ├─ market_summary: "..."
    ├─ funding_summary: "..."
    ├─ industry_summary: "..."
    └─ enriched_sources: {
        "url": {
            "markdown": "Full page content (100KB)...",
            "status": "success",
            ...
        }
    }
        ↓
    Person3Handoff.convert()
        ↓
KnowledgeInput (Person 3)
    ├─ startup_name: "OpenAI"
    ├─ research_data: { ... }
    └─ enriched_sources: [
        {
            "url": "...",
            "title": "...",
            "content": "Full markdown...",
            "source_type": "founder_bio|company_wiki|market_research|...",
            "metadata": { ... }
        }
    ]
        ↓
    Person 3 RAG Pipeline
        ├─ Chunk content
        ├─ Generate embeddings
        ├─ Store in Qdrant
        └─ Build memory index
        ↓
KnowledgeOutput (Person 3)
    ├─ embedded_sources: { ... }
    ├─ vector_store_id: "..."
    └─ memory_index: { ... }
```
"""
