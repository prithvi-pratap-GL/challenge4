# VentureMind - AI-Powered Venture Investment Analysis Platform

**Intelligent pitch deck analysis and investment scoring system powered by vision models and semantic search.**

---

## 📋 Table of Contents

- [Overview](#overview)
- [Key Features](#key-features)
- [System Architecture](#system-architecture)
- [Technology Stack](#technology-stack)
- [Project Structure](#project-structure)
- [Setup & Installation](#setup--installation)
- [Configuration](#configuration)
- [API Endpoints](#api-endpoints)
- [Usage Examples](#usage-examples)
- [System Components](#system-components)
- [Data Flow](#data-flow)
- [Development](#development)

---

## 🎯 Overview

VentureMind is an intelligent investment analysis platform that:

1. **Ingests pitch decks** via PDF upload or website crawling
2. **Extracts information** using vision models and text analysis
3. **Semantically indexes** content into a vector database
4. **Scores deals** across 5 investment categories (TEAM, MARKET, PRODUCT, FINANCIAL, RISK)
5. **Generates investment recommendations** with supporting evidence

The system is designed for VCs, angel investors, and investment teams to automate due diligence and quickly evaluate startup opportunities.

---

## ✨ Key Features

### 📄 PDF Ingestion
- **Hybrid extraction**: Text + vision-based analysis for image-heavy decks
- **Concurrent processing**: Analyzes 16 pages in parallel (asyncio.gather)
- **Graceful degradation**: Falls back to text-only if vision model fails
- **Intelligent chunking**: Creates semantic chunks from visual analysis

### 🔍 Vision-Based Analysis
- **Image understanding**: Groq vision model extracts charts, graphs, tables
- **Deterministic extraction**: Temperature=0.0 for reproducible results
- **Structured output**: PageAnalysis schema with summaries, claims, metrics, entities
- **Financial intelligence**: Automatically extracts KPIs, ARR, growth rates, TAM

### 🧠 Semantic Search
- **384-dimensional embeddings**: BAAI/bge-small-en-v1.5 model
- **Cosine similarity**: Fast retrieval of contextual chunks
- **Deal isolation**: Filters results by deal_id for multi-tenant support
- **Top-k retrieval**: Configurable result count for evaluation

### 🎯 Investment Scoring
- **5 categories**: TEAM, MARKET, PRODUCT, FINANCIAL, RISK
- **Evidence-based**: Links scores to actual chunks from pitch deck
- **LLM extraction**: Llama-3.1-8B fact extraction from retrieved chunks
- **Validation pipeline**: Cross-references findings against source chunks

### 📊 Vector Storage
- **Qdrant**: High-performance vector database with GPU support
- **384-dimensional vectors**: Optimized for semantic search
- **Two collections**: `pitch_deck_chunks` + `startup_website_chunks`
- **Batch upsert**: Efficient storage with automatic indexing

---

## 🏗️ System Architecture

### High-Level Overview

```
┌─────────────────────────────────────────────┐
│        PRESENTATION LAYER (Frontend)        │
│  ├─ Ingestion Portal (file upload)          │
│  └─ Evaluation UI (search & scoring)        │
└────────────────┬────────────────────────────┘
                 │
┌────────────────▼────────────────────────────┐
│           API LAYER (FastAPI)               │
│  ├─ POST /api/v1/ingest (PDF/URL)          │
│  └─ POST /api/v1/evaluate (scoring)        │
└────────────────┬────────────────────────────┘
                 │
    ┌────────────┴────────────┐
    ▼                         ▼
┌──────────────────┐  ┌──────────────────┐
│ INGESTION        │  │ SCORING          │
│ PIPELINE         │  │ ENGINE           │
│                  │  │                  │
│ • PDF Extract    │  │ • Retrieval      │
│ • Vision Parse   │  │ • LLM Extract    │
│ • Embedding      │  │ • Scoring Logic  │
│ • Qdrant Store   │  │ • Recommendation │
└────────────┬─────┘  └────────────┬─────┘
             │                     │
             └──────────┬──────────┘
                        ▼
             ┌─────────────────────┐
             │ QDRANT VECTOR DB    │
             │  (384-dim vectors)  │
             └─────────────────────┘
                        │
                ┌───────┴───────┐
                ▼               ▼
         ┌────────────┐  ┌────────────┐
         │ Pitch Deck │  │ Website    │
         │ Chunks     │  │ Chunks     │
         └────────────┘  └────────────┘
```

### External AI Services

| Service | Purpose | Model | Endpoint |
|---------|---------|-------|----------|
| **Groq** | Vision PDF analysis | meta-llama/llama-4-scout-17b-16e-instruct | https://api.groq.com/openai/v1 |
| **HuggingFace Router** | LLM fact extraction | meta-llama/Llama-3.1-8B-Instruct:novita | https://router.huggingface.co/v1 |
| **Sentence Transformers** | Text embeddings | BAAI/bge-small-en-v1.5 | Local (384-dim) |

---

## 🛠️ Technology Stack

### Backend
- **Framework**: FastAPI (async-first)
- **Language**: Python 3.11+
- **Database**: PostgreSQL (optional, for metadata)
- **Vector DB**: Qdrant (cloud-hosted)
- **Async Runtime**: asyncio, httpx

### AI/ML
- **Vision Model**: Groq (meta-llama/llama-4-scout)
- **LLM Model**: HuggingFace Router (Llama-3.1-8B)
- **Embeddings**: Sentence Transformers (BAAI/bge-small-en-v1.5)
- **PDF Processing**: PyMuPDF (fitz) + Pillow

### Data Processing
- **Text Extraction**: fitz.get_text()
- **Image Rendering**: fitz.get_pixmap(dpi=150)
- **Vector Operations**: numpy
- **JSON Schema**: Pydantic

### Frontend
- **Framework**: React (planned/optional)
- **UI Components**: Material-UI or similar
- **State Management**: React hooks or Redux

---

## 📁 Project Structure

```
ventureMind-V2/
├── backend/
│   ├── api/
│   │   ├── routes/
│   │   │   ├── ingestion.py           # POST /ingest endpoint
│   │   │   ├── evaluation.py          # POST /evaluate endpoint
│   │   │   └── health.py              # Health check
│   │   └── main.py                    # FastAPI app initialization
│   │
│   ├── core/
│   │   ├── settings.py                # Configuration (env vars)
│   │   └── constants.py               # System constants
│   │
│   ├── domain/
│   │   ├── schemas.py                 # Data models (Pydantic)
│   │   │   ├─ PageAnalysis           # Vision output schema
│   │   │   ├─ DealEvaluation         # Scoring output
│   │   │   ├─ Finding                # Extracted facts
│   │   │   └─ RetrievedChunk         # Search results
│   │   └── interfaces.py              # Protocol/interface definitions
│   │
│   ├── infrastructure/
│   │   ├── parsers/
│   │   │   └── vision_parser.py       # VisionPdfParser (Groq integration)
│   │   │
│   │   ├── embeddings/
│   │   │   ├── provider.py            # EmbeddingProvider interface
│   │   │   └── local.py               # LocalEmbedding (Sentence Transformers)
│   │   │
│   │   ├── vectorstore/
│   │   │   └── qdrant_client.py       # Qdrant async operations
│   │   │
│   │   ├── classifiers/
│   │   │   └── llm_page_classifier.py # Page type classification
│   │   │
│   │   └── extractors/
│   │       └── llm_finding_extractor.py # Fact extraction via LLM
│   │
│   └── services/
│       ├── ingestion/
│       │   ├── pdf/
│       │   │   └── pipeline.py        # PdfIngestionService
│       │   └── web/
│       │       └── crawler.py         # Web crawling service
│       │
│       ├── evaluation/
│       │   └── scorer.py              # DealEvaluationService
│       │
│       └── workflows/
│           └── claim_verification.py  # Verification workflow
│
├── storage/
│   └── uploads/                       # PDF storage directory
│
├── .env                               # Environment configuration
├── requirements.txt                   # Python dependencies
├── README.md                          # This file
├── SYSTEM_ARCHITECTURE_GUIDE.md       # Detailed architecture
├── AGENTS_INVENTORY.md                # System components list
└── COMPREHENSIVE_README.md            # Extended documentation
```

---

## 🚀 Setup & Installation

### Prerequisites
- Python 3.11+
- PostgreSQL (optional, for metadata storage)
- Qdrant vector database (cloud or local)
- API keys: Groq, HuggingFace Router, Firecrawl

### Installation Steps

1. **Clone the repository**
   ```bash
   git clone https://github.com/your-org/venturemind-v2.git
   cd ventureMind-V2
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables** (see Configuration section)
   ```bash
   cp .env.example .env
   # Edit .env with your credentials
   ```

5. **Initialize vector database**
   ```bash
   python -c "from backend.infrastructure.vectorstore.qdrant_client import ensure_collections_exist; asyncio.run(ensure_collections_exist())"
   ```

6. **Run the application**
   ```bash
   uvicorn backend.api.main:app --reload --host 0.0.0.0 --port 8000
   ```

The API will be available at `http://localhost:8000`. OpenAPI docs at `/docs`.

---

## ⚙️ Configuration

### Environment Variables

```env
# Vector Database
QDRANT_URL=https://your-qdrant-instance.eu-central-1-0.aws.cloud.qdrant.io
QDRANT_API_KEY=your-qdrant-api-key

# Embeddings
EMBEDDING_MODEL=BAAI/bge-small-en-v1.5
EMBEDDING_DEVICE=cpu  # or 'cuda' for GPU

# Vision Model (Groq)
GROQ_API_KEY=gsk_your_groq_api_key
GROQ_BASE_URL=https://api.groq.com/openai/v1
VISION_MODEL=meta-llama/llama-4-scout-17b-16e-instruct

# LLM Model (HuggingFace Router)
HF_ROUTER_API_KEY=hf_your_huggingface_token
HF_ROUTER_BASE_URL=https://router.huggingface.co/v1
LLM_MODEL_NAME=meta-llama/Meta-Llama-3.1-8B-Instruct:novita

# Web Crawling
FIRECRAWL_API_KEY=fc_your_firecrawl_api_key

# Database (optional)
DATABASE_URL=postgresql+asyncpg://user:password@localhost:5432/venturemind
```

### Key Configuration Notes

- **EMBEDDING_DEVICE**: Use `cuda` if you have GPU with CUDA support (faster embedding computation)
- **VISION_MODEL**: Must be a vision-capable model on Groq (llama-4-scout is recommended)
- **LLM_MODEL_NAME**: Includes provider suffix (`:novita` routes to Novita provider)
- **Qdrant collections** are auto-created on first run if they don't exist

---

## 📡 API Endpoints

### 1. PDF Ingestion

**Endpoint**: `POST /api/v1/ingest`

**Request**:
```bash
curl -X POST http://localhost:8000/api/v1/ingest \
  -F "pitch_deck=@tesla-pitch-deck.pdf" \
  -H "Content-Type: multipart/form-data"
```

**Response** (200 OK):
```json
{
  "deal_id": "tesla",
  "status": "success",
  "chunks_created": 48,
  "tokens_used": 1250,
  "processing_time_ms": 3420
}
```

**Errors**:
- `400 Bad Request`: No file provided or file is not a PDF
- `413 Payload Too Large`: File exceeds size limit
- `500 Internal Server Error`: Vision model or embedding service unavailable

### 2. Investment Evaluation

**Endpoint**: `POST /api/v1/evaluate`

**Request**:
```json
POST /api/v1/evaluate
{
  "deal_id": "tesla",
  "top_k_per_category": 10
}
```

**Response** (200 OK):
```json
{
  "deal_id": "tesla",
  "overall_score": 7.8,
  "categories": {
    "TEAM": {
      "score": 8.2,
      "findings": [
        {
          "text": "Founded by Elon Musk, former CEO of PayPal and co-founder of X.com",
          "evidence_chunks": ["chunk_id_123"],
          "confidence": 0.95
        }
      ]
    },
    "MARKET": {
      "score": 8.5,
      "findings": [...]
    },
    "PRODUCT": {
      "score": 7.2,
      "findings": [...]
    },
    "FINANCIAL": {
      "score": 7.5,
      "findings": [...]
    },
    "RISK": {
      "score": 7.1,
      "findings": [...]
    }
  },
  "recommendation": {
    "decision": "STRONG_BUY",
    "reasoning": "Strong team with automotive expertise...",
    "key_risks": ["Regulatory risk", "Supply chain vulnerability"]
  }
}
```

**Errors**:
- `404 Not Found`: No chunks found for deal_id
- `422 Unprocessable Entity`: Invalid deal_id format
- `500 Internal Server Error`: LLM or retrieval service unavailable

### 3. Health Check

**Endpoint**: `GET /health`

**Response**:
```json
{
  "status": "healthy",
  "services": {
    "qdrant": "connected",
    "embedding_model": "loaded",
    "groq_vision": "available",
    "hf_router_llm": "available"
  }
}
```

---

## 💡 Usage Examples

### Example 1: Ingest a Tesla Pitch Deck

```python
import requests

# Upload pitch deck
response = requests.post(
    "http://localhost:8000/api/v1/ingest",
    files={"pitch_deck": open("tesla-pitch-deck.pdf", "rb")}
)

result = response.json()
print(f"Created {result['chunks_created']} chunks for deal_id={result['deal_id']}")
# Output: Created 48 chunks for deal_id=tesla
```

### Example 2: Evaluate a Deal

```python
# Score the deal across 5 categories
response = requests.post(
    "http://localhost:8000/api/v1/evaluate",
    json={"deal_id": "tesla", "top_k_per_category": 10}
)

evaluation = response.json()
print(f"Overall Score: {evaluation['overall_score']}/10")
print(f"TEAM Category: {evaluation['categories']['TEAM']['score']}")
print(f"Recommendation: {evaluation['recommendation']['decision']}")
```

### Example 3: Verify Vision Model is Working

```python
# Test vision parser directly
from backend.infrastructure.parsers.vision_parser import VisionPdfParser
import asyncio

parser = VisionPdfParser()
analysis = asyncio.run(parser.parse_page("page_0.png", "raw text"))

print(f"Page Type: {analysis.page_type}")
print(f"Summary: {analysis.visual_summary[:100]}...")
print(f"Metrics Found: {len(analysis.metrics)}")
```

---

## 🔧 System Components

### Core Services

| Component | Purpose | Technology |
|-----------|---------|-----------|
| **VisionPdfParser** | Vision-based PDF analysis | Groq (llama-4-scout) |
| **LocalEmbedding** | Text→vector conversion | Sentence Transformers |
| **QdrantClient** | Vector storage & retrieval | Qdrant |
| **LlmFindingExtractor** | Fact extraction | HuggingFace Router (Llama-3.1) |
| **LlmPageClassifier** | Page type classification | HuggingFace Router |
| **PdfIngestionService** | PDF processing pipeline | Internal orchestration |
| **DealEvaluationService** | Investment scoring | Internal logic |
| **ClaimVerificationService** | Finding validation | HuggingFace Router |

### Key Schemas

```python
# Vision model output
class PageAnalysis(BaseModel):
    page_number: int
    page_type: str  # cover, team, product, chart, etc.
    visual_summary: str  # Investment-relevant facts
    claims: List[str]  # Business claims
    metrics: List[str]  # Financial KPIs
    entities: List[str]  # Companies, people, products

# Evaluation output
class DealEvaluation(BaseModel):
    deal_id: str
    overall_score: float  # 0.0 - 10.0
    categories: Dict[str, CategoryScore]  # TEAM, MARKET, etc.
    recommendation: Recommendation

# Extracted facts
class Finding(BaseModel):
    text: str  # The actual finding
    supporting_chunk_ids: List[str]  # References to evidence
    confidence: float  # 0.0 - 1.0
    category: str  # TEAM, MARKET, etc.
```

---

## 📊 Data Flow

### Ingestion Flow

```
1. PDF Upload
   └─→ File validation & storage

2. Text Extraction
   └─→ fitz.get_text() on all pages
   └─→ If text > 40 chars: use text pipeline
   └─→ Else: use vision pipeline

3. Vision Analysis (if needed)
   └─→ Render pages to PNG (150 DPI)
   └─→ Parallel processing: asyncio.gather(16 concurrent)
   └─→ Call Groq vision model per page
   └─→ Parse PageAnalysis schema
   └─→ Extract chunks from summaries/claims/metrics

4. Embedding Generation
   └─→ BAAI/bge-small-en-v1.5.encode(chunk)
   └─→ 384-dimensional vectors

5. Qdrant Storage
   └─→ Batch upsert (50 points/batch)
   └─→ Create indexes on deal_id
   └─→ Confirm storage

Output: chunks_created count
```

### Evaluation Flow

```
1. Validation
   └─→ Verify chunks exist for deal_id

2. For each category (TEAM, MARKET, PRODUCT, FINANCIAL, RISK)
   
   a) Semantic Search
      └─→ Embed category query (384-dim)
      └─→ Qdrant cosine similarity search
      └─→ Retrieve top_k chunks
      
   b) LLM Fact Extraction
      └─→ Format chunks as context
      └─→ Call Llama-3.1 via HuggingFace Router
      └─→ Extract facts in JSON format
      └─→ Validate chunk references
      
   c) Scoring
      └─→ Count/weight findings
      └─→ Assign category score (0-10)

3. Aggregation
   └─→ Calculate overall score (average of 5 categories)
   └─→ Generate recommendation

Output: DealEvaluation with scores & findings
```

---

## 👨‍💻 Development

### Running Tests

```bash
# Unit tests
pytest tests/unit -v

# Integration tests (requires services)
pytest tests/integration -v

# Specific test file
pytest tests/unit/test_vision_parser.py -v
```

### Code Style

```bash
# Format code
black backend/

# Lint
flake8 backend/

# Type checking
mypy backend/
```

### Adding New Features

1. **New ingestion source** (e.g., image URLs):
   - Create new parser in `backend/infrastructure/parsers/`
   - Implement `IPdfParser` interface
   - Add route in `backend/api/routes/ingestion.py`

2. **New scoring category**:
   - Add to `INVESTMENT_CATEGORIES` in `constants.py`
   - Define semantic queries in `DealEvaluationService`
   - Update `DealEvaluation` schema

3. **New AI service**:
   - Add configuration in `settings.py`
   - Create service wrapper in `backend/infrastructure/`
   - Integrate in appropriate workflow

### Debugging

Enable debug logging:
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

Enable Qdrant request logging:
```python
from qdrant_client import QdrantClient
client = QdrantClient(..., prefer_grpc=False)  # Use HTTP for verbose logs
```

---

## 📚 Additional Resources

- **[System Architecture Guide](SYSTEM_ARCHITECTURE_GUIDE.md)** - Detailed control flows & diagrams
- **[Agents Inventory](AGENTS_INVENTORY.md)** - Complete component list
- **[Comprehensive README](COMPREHENSIVE_README.md)** - Extended documentation

---

## 🔐 Security Considerations

- **API Keys**: Never commit `.env` file. Use environment variables only
- **PDF Storage**: Files stored in `storage/uploads/` - ensure proper access control
- **Vector DB**: Qdrant API key should be environment-only
- **Rate Limiting**: Implement rate limits on `/ingest` and `/evaluate` endpoints
- **Input Validation**: All file uploads validated for size & type
- **Authentication**: Consider OAuth2 for multi-tenant deployments

---

## 📝 License

[Add your license here]

---

## 📧 Support

For issues, feature requests, or questions:
- Create an issue on GitHub
- Email: team@venturemind.io
- Slack: #venturemind-support

---

**Last Updated**: June 2026  
**Version**: 2.0.0  
**Status**: Production Ready
