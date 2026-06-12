# P3 Knowledge Intelligence Module - Quick Start

## One-Minute Overview

The P3 module ingests startup data (pitch decks + websites) and makes it queryable for agents.

```python
# P5 Orchestrator: Ingest data
from backend.ingestion.pipeline import ingest_startup_sync
from backend.contracts import StartupInput

knowledge = ingest_startup_sync(
    StartupInput(
        startup_name="Acme",
        website_url="https://acme.com",
        pitch_deck_path="acme.pdf"
    ),
    startup_id="acme-001"
)

# P4 Agents: Query data
from backend.knowledge.retrieval.service import retrieve_context

result = retrieve_context(
    query="What is the business model?",
    startup_id="acme-001"
)
```

---

## Setup (5 Minutes)

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Configure environment
cp .env.example .env
# Edit .env and set:
# - OPENAI_API_KEY
# - QDRANT_URL (default: http://localhost:6333)

# 3. Start Qdrant
docker run -p 6333:6333 qdrant/qdrant

# 4. Verify setup
python backend/test_module.py
```

---

## Public APIs

### For P5 Orchestrator

| Function | Purpose | Returns |
|----------|---------|---------|
| `ingest_pitch_deck(pdf_path)` | Process pitch deck | `KnowledgeOutput` |
| `ingest_website(url)` | Process website | `KnowledgeOutput` |
| `ingest_startup_sync(input, id)` | Process both sources | `KnowledgeOutput` |

### For P4 Agents

| Function | Purpose | Returns |
|----------|---------|---------|
| `retrieve_context(query, startup_id)` | Query knowledge | `RetrievalOutput` |

### Storage

| Function | Purpose |
|----------|---------|
| `save_startup_memory(id, knowledge)` | Save for comparison |
| `get_startup_memory(id)` | Retrieve saved data |

---

## Data Contracts

### Input
```python
StartupInput(
    startup_name: str
    website_url: Optional[str]
    pitch_deck_path: Optional[str]
)
```

### Output
```python
KnowledgeOutput(
    startup_summary: str
    business_model: str
    risks: list[str]
    financials: list[str]
    market_claims: list[str]
    evidence: list[str]
    retrieved_context: str
)
```

### Retrieval
```python
RetrievalOutput(
    context: str
    sources: list[str]
)
```

---

## Directory Structure

```
backend/
├── contracts/         ← Frozen interfaces
├── ingestion/         ← Data ingestion
│   ├── pdf/          ← PDF processing
│   ├── website/      ← Website processing
│   └── vision/       ← Vision analysis
└── knowledge/        ← Storage & retrieval
    ├── embeddings/   ← Vector generation
    ├── qdrant/       ← Vector database
    ├── retrieval/    ← Agent API
    └── memory/       ← Startup memory
```

---

## Common Tasks

### Process a pitch deck
```python
from backend.ingestion.pdf.pipeline import ingest_pitch_deck

knowledge = ingest_pitch_deck("deck.pdf", "StartupName")
```

### Process a website
```python
from backend.ingestion.website.pipeline import ingest_website

knowledge = ingest_website("https://startup.com", "StartupName")
```

### Query a startup
```python
from backend.knowledge.retrieval.service import retrieve_context

result = retrieve_context(
    query="Revenue and growth metrics",
    startup_id="startup-001"
)
print(result.context)
```

### Search across all startups
```python
from backend.knowledge.retrieval.service import retrieve_context

result = retrieve_context(
    query="AI machine learning",
    startup_id=None  # Search all
)
```

### Save startup for later
```python
from backend.knowledge.memory.service import save_startup_memory

save_startup_memory("startup-001", knowledge)
```

### Retrieve saved startup
```python
from backend.knowledge.memory.service import get_startup_memory

knowledge = get_startup_memory("startup-001")
```

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Module not found | `python -c "import sys; sys.path.insert(0, '.'); from backend.contracts import StartupInput"` |
| API key missing | Set `OPENAIN_API_KEY` in `.env` |
| Qdrant error | Start with `docker run -p 6333:6333 qdrant/qdrant` |
| PDF not found | Verify file exists and path is correct |
| Vision fails | Check OpenAI API quota and permissions |

---

## Documentation

- **Full Documentation**: `P3_MODULE_README.md`
- **Integration Guide**: `P3_INTEGRATION_GUIDE.md`
- **Implementation Details**: `IMPLEMENTATION_SUMMARY.md`
- **Examples**: `backend/examples.py`
- **Tests**: `python backend/test_module.py`

---

## Key Features

✓ **Multi-source ingestion** - PDFs and websites  
✓ **Vision analysis** - Extract from slides and images  
✓ **Semantic search** - Natural language queries  
✓ **Startup memory** - Compare and track startups  
✓ **Type safe** - Full type hints and Pydantic validation  
✓ **Error handling** - Comprehensive logging and error messages  
✓ **Well documented** - Examples and guides included  

---

## Status: ✓ READY FOR USE

All implementation complete. P5 orchestrator and P4 agents can integrate immediately.

For questions, see `P3_MODULE_README.md` or check `backend/examples.py` for usage patterns.
