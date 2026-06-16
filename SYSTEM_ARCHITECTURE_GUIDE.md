# VentureMind System Architecture Guide

**Complete visual and textual guide to system architecture and control flows**

---

## 1. Complete System Architecture

### Full System Components Map

```
┌─────────────────────────────────────────────────────────────────────────┐
│                                                                          │
│                         VENTUREMIND SYSTEM                              │
│                                                                          │
└─────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────┐
│                          PRESENTATION LAYER                             │
│                                                                          │
│  ┌──────────────────────┐              ┌──────────────────────┐        │
│  │  IngestionPortal     │              │   EvaluationUI       │        │
│  │  - File upload       │              │   - Deal search      │        │
│  │  - URL input         │              │   - Score display    │        │
│  │  - Progress tracker  │              │   - Evidence view    │        │
│  └─────────┬────────────┘              └──────────┬───────────┘        │
│            │                                       │                    │
└────────────┼───────────────────────────────────────┼────────────────────┘
             │                                       │
             ▼                                       ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                          API LAYER (FastAPI)                            │
│                                                                          │
│  ┌──────────────────────────────┐   ┌──────────────────────────────┐  │
│  │  POST /api/v1/ingest         │   │  POST /evaluate              │  │
│  │  ├─ pitch_deck (File)        │   │  ├─ deal_id (str)           │  │
│  │  └─ company_url (str)        │   │  └─ Returns: scores+rec.    │  │
│  └──────────┬───────────────────┘   └──────────┬───────────────────┘  │
│             │                                   │                      │
└─────────────┼───────────────────────────────────┼──────────────────────┘
              │                                   │
              ▼                                   ▼
┌──────────────────────────────────┐   ┌─────────────────────────────┐
│    INGESTION PIPELINE            │   │  SCORING ENGINE            │
│                                  │   │                            │
│ ┌────────────────────────────┐  │   │ ┌──────────────────────┐   │
│ │ 1. FILE HANDLER            │  │   │ │ 1. CATEGORY MAPPER   │   │
│ │  - Save to storage         │  │   │ │  - TEAM              │   │
│ │  - Derive deal_id          │  │   │ │  - MARKET            │   │
│ └────────────┬───────────────┘  │   │ │  - PRODUCT           │   │
│              │                  │   │ │  - FINANCIAL         │   │
│ ┌────────────▼───────────────┐  │   │ │  - RISK              │   │
│ │ 2. TEXT EXTRACTOR (fitz)   │  │   │ └────────────┬─────────┘   │
│ │  - get_text()              │  │   │              │              │
│ │  - Page by page            │  │   │ ┌────────────▼─────────┐   │
│ │  - Chunk content           │  │   │ │ 2. RETRIEVAL SERVICE │   │
│ └────────────┬───────────────┘  │   │ │  - Semantic search   │   │
│              │                  │   │ │  - Filter by deal_id │   │
│ ┌────────────▼───────────────┐  │   │ │  - Top-k retrieval   │   │
│ │ 3. VISION PIPELINE         │  │   │ └────────────┬─────────┘   │
│ │  - Render PNG (150 DPI)    │  │   │              │              │
│ │  - Call vision model       │  │   │ ┌────────────▼─────────┐   │
│ │  - Parse PageAnalysis      │  │   │ │ 3. LLM EXTRACTOR     │   │
│ │  - Handle fallback         │  │   │ │  - Fact extraction   │   │
│ └────────────┬───────────────┘  │   │ │  - Chunk validation  │   │
│              │                  │   │ │  - Finding scoring   │   │
│ ┌────────────▼───────────────┐  │   │ └────────────┬─────────┘   │
│ │ 4. EMBEDDING PROVIDER      │  │   │              │              │
│ │  - BAAI/bge model          │  │   │ ┌────────────▼─────────┐   │
│ │  - 384-dimensional vectors │  │   │ │ 4. SCORING LOGIC     │   │
│ └────────────┬───────────────┘  │   │ │  - Aggregate scores  │   │
│              │                  │   │ │  - Weight categories │   │
│ ┌────────────▼───────────────┐  │   │ │  - Generate rec.     │   │
│ │ 5. QDRANT UPSERT           │  │   │ └────────────┬─────────┘   │
│ │  - Batch size: 50          │  │   │              │              │
│ │  - Create indexes          │  │   │              ▼              │
│ │  - Confirm storage         │  │   │     RECOMMENDATION         │
│ └────────────┬───────────────┘  │   │     ├─ Score (0-10)        │
│              │                  │   │     ├─ Finding[]           │
└──────────────┼──────────────────┘   │     ├─ Decision            │
               │                      │     └─ Evidence            │
               │                      └─────────────────────────────┘
               │
               ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                     DATA LAYER (QDRANT VECTOR DB)                       │
│                                                                          │
│  ┌────────────────────────────────┐   ┌────────────────────────────┐  │
│  │  Collection: pitch_deck_chunks │   │ Collection: startup_website │  │
│  │                                │   │ _chunks                    │  │
│  │  ┌──────────────────────────┐  │   │ ┌────────────────────────┐ │  │
│  │  │ Point Example:           │  │   │ │ Point Example:         │ │  │
│  │  │ {                        │  │   │ │ {                      │ │  │
│  │  │   id: uuid.hex,          │  │   │ │   id: uuid.hex,        │ │  │
│  │  │   vector: [384 floats],  │  │   │ │   vector: [384],       │ │  │
│  │  │   payload: {             │  │   │ │   payload: {           │ │  │
│  │  │     startup_id: "tesla", │  │   │ │     deal_id: "uber",   │ │  │
│  │  │     page_number: 1,      │  │   │ │     source_id: "web",  │ │  │
│  │  │     page_type: "title",  │  │   │ │     url: "...",        │ │  │
│  │  │     text: "...",         │  │   │ │     text: "...",       │ │  │
│  │  │     entities: [...]      │  │   │ │     category: "..."    │ │  │
│  │  │   }                      │  │   │ │   }                    │ │  │
│  │  │ }                        │  │   │ │ }                      │ │  │
│  │  └──────────────────────────┘  │   │ └────────────────────────┘ │  │
│  │  Indexing: deal_id (keyword)   │   │ Indexing: deal_id           │  │
│  └────────────────────────────────┘   └────────────────────────────┘  │
│                                                                          │
│  Vector DB Host: http://localhost:6333 (or cloud)                      │
│  Embedding Dimension: 384 (BAAI/bge-small-en-v1.5)                    │
│  Distance Metric: Cosine Similarity                                     │
│                                                                          │
└─────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────┐
│                      EXTERNAL AI SERVICES                               │
│                                                                          │
│  ┌──────────────────────────────┐   ┌──────────────────────────────┐  │
│  │  HuggingFace Router          │   │  Groq API (AsyncOpenAI)      │  │
│  │  ├─ LLM Model                │   │  ├─ Vision Model             │  │
│  │  │  (Llama-3.1-8B:novita)    │   │  │  (Llama-4-Scout)          │  │
│  │  ├─ Purpose: Finding Extract │   │  ├─ Purpose: PDF Analysis    │  │
│  │  ├─ JSON Mode Response       │   │  ├─ Image Processing        │  │
│  │  ├─ Temperature: 0.0         │   │  ├─ Temperature: 0.0         │  │
│  │  └─ Endpoint                 │   │  └─ Endpoint                 │  │
│  │     https://router.hf.co/v1  │      https://api.groq.com/...   │  │
│  └──────────────────────────────┘   └──────────────────────────────┘  │
│                                                                          │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## 2. Detailed Control Flow Diagrams

### 2.1 PDF Ingestion Control Flow

```
POST /api/v1/ingest (pitch_deck)
  │
  ├─ [1] FILE VALIDATION
  │  ├─ Check file exists: ✅
  │  └─ Derive deal_id from filename: "tesla"
  │
  ├─ [2] SAVE TO DISK
  │  └─ storage/uploads/tesla_tesla-pitch-deck.pdf
  │
  ├─ [3] TEXT EXTRACTION
  │  ├─ Open with fitz: Document object
  │  ├─ For each page:
  │  │  └─ page.get_text() → str
  │  └─ Collect into chunks list
  │
  ├─ [4] TEXT COVERAGE CHECK
  │  │
  │  ├─ IF text_length > 40 chars:
  │  │  │
  │  │  └─ ✅ USE TEXT PIPELINE (FAST)
  │  │     ├─ Chunk by \n\n
  │  │     ├─ Filter < 40 chars
  │  │     └─ Continue to [6]
  │  │
  │  └─ ELSE (image-based PDF):
  │     │
  │     └─ ⚠️ USE VISION PIPELINE
  │        ├─ [4a] RENDER PAGES
  │        │  └─ For each page:
  │        │     ├─ page.get_pixmap(dpi=150) → Image object
  │        │     └─ Save PNG to temp file
  │        │
  │        ├─ [4b] VISION ANALYSIS (CONCURRENT)
  │        │  └─ For each page (asyncio.gather):
  │        │     ├─ Base64 encode PNG
  │        │     ├─ Call VisionPdfParser.parse_page()
  │        │     │  ├─ API call to Groq
  │        │     │  │  ├─ Model: meta-llama/llama-4-scout-17b-16e-instruct
  │        │     │  │  ├─ Payload: system_prompt + image
  │        │     │  │  ├─ Temperature: 0.0 (deterministic)
  │        │     │  │  └─ Response: JSON
  │        │     │  ├─ Parse PageAnalysis
  │        │     │  │  ├─ page_number
  │        │     │  │  ├─ page_type
  │        │     │  │  ├─ visual_summary
  │        │     │  │  ├─ claims[]
  │        │     │  │  ├─ metrics[]
  │        │     │  │  └─ entities[]
  │        │     │  └─ Return PageAnalysis or Fallback
  │        │     │     (On error: return empty PageAnalysis)
  │        │     └─ Continue
  │        │
  │        └─ [4c] COMBINE ANALYSES
  │           └─ Create chunks from PageAnalysis
  │              (visual_summary + claims + metrics)
  │
  ├─ [5] VALIDATION
  │  ├─ IF no chunks: RETURN 400
  │  │  └─ "Could not extract usable text"
  │  └─ ELSE: Continue
  │
  ├─ [6] EMBEDDING GENERATION
  │  └─ For each chunk:
  │     ├─ BAAI/bge-small-en-v1.5.encode(text)
  │     ├─ Output: 384-dimensional vector
  │     └─ Create point object:
  │        {
  │          id: uuid.uuid4().hex,
  │          vector: [384 floats],
  │          payload: {
  │            startup_id: "tesla",
  │            document_id: "/path/to/pdf",
  │            page_number: 1,
  │            page_type: "title",
  │            text: chunk_content,
  │            entities: [...],
  │            metrics: [...]
  │          }
  │        }
  │
  ├─ [7] QDRANT UPSERT
  │  ├─ Collection: pitch_deck_chunks
  │  ├─ Batch size: 50 points
  │  ├─ For each batch:
  │  │  ├─ client.upsert(points)
  │  │  └─ Create index: deal_id (keyword)
  │  └─ Confirm storage
  │
  └─ [8] RESPONSE
     └─ {
          success: true,
          deal_id: "tesla",
          chunks_processed: 16,
          pdf_url: "/uploads/tesla_tesla-pitch-deck.pdf"
        }
```

### 2.2 Evaluation Control Flow

```
POST /evaluate (deal_id="tesla")
  │
  ├─ [1] VALIDATION
  │  └─ Verify chunks exist for deal_id in Qdrant: ✅
  │
  ├─ [2] INITIALIZE SCORING
  │  └─ categories = [TEAM, MARKET, PRODUCT, FINANCIAL, RISK]
  │
  ├─ [3] FOR EACH CATEGORY:
  │  │
  │  ├─ [3.1] MAP TO SEMANTIC QUERY
  │  │  ├─ TEAM:
  │  │  │  "Founders, team background, domain expertise,
  │  │  │   technical skills, leadership history..."
  │  │  │
  │  │  ├─ MARKET:
  │  │  │  "Market size, TAM, growth rate,
  │  │  │   competitive landscape, adoption trends..."
  │  │  │
  │  │  ├─ PRODUCT:
  │  │  │  "Features, roadmap, differentiation,
  │  │  │   competitive advantage, value proposition..."
  │  │  │
  │  │  ├─ FINANCIAL:
  │  │  │  "Revenue, ARR, burn rate, unit economics,
  │  │  │   cash runway, profitability..."
  │  │  │
  │  │  └─ RISK:
  │  │     "Risks, challenges, execution dependencies,
  │  │      regulatory threats, market risks..."
  │  │
  │  ├─ [3.2] SEMANTIC SEARCH
  │  │  │
  │  │  ├─ BAAI/bge.encode(query) → 384-dim vector
  │  │  │
  │  │  ├─ Qdrant search:
  │  │  │  ├─ query_vector: [384 floats]
  │  │  │  ├─ filter: {startup_id == "tesla"}
  │  │  │  ├─ limit: 10 (top_k)
  │  │  │  ├─ distance_metric: cosine_similarity
  │  │  │  └─ Sort by: score (descending)
  │  │  │
  │  │  └─ Return: ScoredPoint[]
  │  │     ├─ id: chunk_id
  │  │     ├─ score: 0.85 (similarity)
  │  │     ├─ vector: [384 floats]
  │  │     └─ payload: {text, page_number, ...}
  │  │
  │  ├─ [3.3] CHECK RETRIEVAL
  │  │  ├─ IF chunks.length == 0:
  │  │  │  └─ Return empty findings for category
  │  │  └─ ELSE: Continue
  │  │
  │  ├─ [3.4] LLM FACT EXTRACTION
  │  │  │
  │  │  ├─ Build context string:
  │  │  │  └─ Format chunks with metadata
  │  │  │     ```
  │  │  │     [Chunk 1 ID: abc123]
  │  │  │     Founded in 2010 by John Doe
  │  │  │     10+ years experience in fintech
  │  │  │     
  │  │  │     [Chunk 2 ID: def456]
  │  │  │     Led Series B raise of $50M
  │  │  │     ```
  │  │  │
  │  │  ├─ LLM Call (via HuggingFace Router):
  │  │  │  ├─ provider: HuggingFace Router
  │  │  │  ├─ model: "meta-llama/Llama-3.1-8B-Instruct:novita"
  │  │  │  ├─ temperature: 0.0 (deterministic)
  │  │  │  ├─ response_format: {"type": "json_object"}
  │  │  │  │
  │  │  │  ├─ system_prompt:
  │  │  │  │  "You are a meticulous data extractor.
  │  │  │  │   Extract ONLY quantifiable facts and
  │  │  │  │   definitive statements from context.
  │  │  │  │   Return JSON array of findings."
  │  │  │  │
  │  │  │  └─ user_prompt:
  │  │  │     "Category: TEAM
  │  │  │      Extract factual findings..."
  │  │  │
  │  │  ├─ Response Parse:
  │  │  │  ├─ Extract JSON
  │  │  │  └─ Parse finding objects:
  │  │  │     {
  │  │  │       "finding_text": "Founded in 2010",
  │  │  │       "supporting_chunk_ids": ["abc123"]
  │  │  │     }
  │  │  │
  │  │  └─ Validate chunk IDs:
  │  │     ├─ For each chunk_id in supporting_ids:
  │  │     │  └─ Verify: chunk_id in retrieved_chunks
  │  │     ├─ Keep: only valid findings
  │  │     └─ Remove: hallucinated references
  │  │
  │  ├─ [3.5] SCORE CATEGORY
  │  │  ├─ findings_count × quality_weight
  │  │  ├─ Scale: 0-10
  │  │  └─ Store: category_scores[TEAM] = 8.0
  │  │
  │  └─ [3.6] NEXT CATEGORY (MARKET, PRODUCT, etc.)
  │
  ├─ [4] AGGREGATE SCORING
  │  ├─ weights = {
  │  │  TEAM: 0.20,
  │  │  MARKET: 0.25,
  │  │  PRODUCT: 0.25,
  │  │  FINANCIAL: 0.20,
  │  │  RISK: 0.10
  │  │ }
  │  │
  │  ├─ aggregate_health = SUM(score × weight)
  │  └─ Result: 7.5 (out of 10)
  │
  ├─ [5] GENERATE RECOMMENDATION
  │  ├─ IF aggregate_health > 7.5:
  │  │  └─ recommendation = "INVEST"
  │  │
  │  ├─ ELIF aggregate_health >= 5.0:
  │  │  └─ recommendation = "WATCHLIST"
  │  │
  │  └─ ELSE:
  │     └─ recommendation = "PASS"
  │
  └─ [6] RESPONSE
     └─ {
          status: "success",
          deal_id: "tesla",
          category_scores: {
            TEAM: 8.0,
            MARKET: 7.5,
            PRODUCT: 8.5,
            FINANCIAL: 7.0,
            RISK: 6.5
          },
          aggregateHealth: 7.5,
          recommendation: "INVEST",
          findings_by_category: {...},
          pdf_url: "/uploads/tesla_deck.pdf"
        }
```

---

## 3. Data Transformation Pipeline

```
RAW INPUT
  │
  ├─ PDF File
  │  │
  │  ├─ [EXTRACTION]
  │  │  ├─ fitz.open() → Document
  │  │  ├─ For each page:
  │  │  │  ├─ get_text() → raw text
  │  │  │  └─ get_pixmap(dpi=150) → PNG image
  │  │  └─ Output: text + images
  │  │
  │  ├─ [VISION ANALYSIS] (if text empty)
  │  │  ├─ Encode PNG to base64
  │  │  ├─ Call Groq vision model (meta-llama/llama-4-scout)
  │  │  └─ Output: PageAnalysis
  │  │     {visual_summary, claims, metrics, entities}
  │  │
  │  └─ [CHUNKING]
  │     ├─ Split text by paragraphs
  │     ├─ Filter < 40 chars
  │     └─ Output: chunks[]
  │
  └─ Website URL
     │
     ├─ [CRAWLING]
     │  ├─ requests.get(url)
     │  ├─ BeautifulSoup parse
     │  └─ Extract: p, h1-h3, li elements
     │
     └─ [CHUNKING]
        ├─ Split by newlines
        ├─ Filter < 40 chars
        └─ Output: chunks[]

[COMMON PATH]
  │
  ├─ [PREPROCESSING]
  │  ├─ Normalize whitespace
  │  ├─ Remove special chars
  │  └─ Output: clean chunks
  │
  ├─ [EMBEDDING]
  │  ├─ BAAI/bge.encode(chunk)
  │  └─ Output: 384-dim vector
  │
  ├─ [POINT CREATION]
  │  └─ {id: uuid, vector: [...], payload: {...}}
  │
  ├─ [BATCHING]
  │  ├─ Group points (size: 50)
  │  └─ Output: batch[]
  │
  └─ [QDRANT STORAGE]
     ├─ For each batch:
     │  └─ client.upsert(batch)
     └─ Output: stored vectors
```

---

## 4. AI Agent Interaction Map

```
┌─────────────────────────────────────────────────────────┐
│               EVALUATION REQUEST                        │
└────────────────┬────────────────────────────────────────┘
                 │
         ┌───────▼──────────┐
         │ DeterministicSC  │◄────── Orchestration Agent
         │  (Main Engine)   │
         └───────┬──────────┘
                 │
                 │ For each category
                 │
      ┌──────────▼──────────────┐
      │                         │
      ▼                         ▼
┌──────────────────┐   ┌────────────────────────┐
│ QdrantRetrieval  │   │ LlmFindingExtractor    │◄──── AI Agents
│ Service          │   │                        │
│                  │   │ ┌──────────────────┐   │
│ ├─ Query embed   │   │ │ HuggingFace      │   │
│ ├─ Search Qdrant │   │ │ Router API       │   │
│ └─ Filter deal_id│   │ │ - Llama 3.1      │   │
│                  │   │ │ - JSON mode      │   │
│    ↓             │   │ │ - Temp: 0.0      │   │
│  Top 10 chunks   │   │ └──────────────────┘   │
└──────────┬───────┘   │                        │
           │           │ ├─ Build context    │   │
           │           │ ├─ Call LLM         │   │
           │           │ ├─ Parse JSON       │   │
           │           │ ├─ Validate IDs     │   │
           │           │ └─ Return findings  │   │
           │           └────────────────────────┘
           │                      │
           └──────────┬───────────┘
                      │
              ┌───────▼──────────┐
              │ Scoring Logic    │
              │ - Count findings │
              │ - Weight scores  │
              │ - 0-10 scale     │
              └────────┬─────────┘
                       │
            ┌──────────▼──────────┐
            │ Recommendation Gen  │
            │ - Aggregate scores  │
            │ - INVEST/WATCH/PASS │
            └────────────────────┘
```

---

## 5. Error Handling & Fallback Mechanisms

```
INGESTION FAILURES:

Text Extraction Error
  └─ Vision pipeline fallback
     ├─ Render PNG
     ├─ Call vision model
     └─ IF fails → Return empty PageAnalysis

Vision Model Unavailable
  └─ Graceful fallback
     ├─ VisionPdfParser catches exception
     ├─ Returns fallback PageAnalysis
     │  {page_type: "unknown", visual_summary: "Failed..."}
     └─ Pipeline continues (non-blocking)

No Chunks Created
  └─ Return 400 error
     {detail: "Could not extract usable text"}

EVALUATION FAILURES:

No Chunks Found for deal_id
  └─ Return empty findings for category
     (No score penalty, graceful skip)

LLM API Timeout
  └─ Retry with exponential backoff
     └─ IF still fails → Skip category

Hallucinated Chunk IDs
  └─ Validation catches & removes
     (Invalid references filtered out)

Invalid JSON Response
  └─ Parse error handling
     ├─ Retry LLM call
     └─ IF fails → Return empty findings
```

---

## 6. Performance Characteristics

```
LATENCY PROFILE:

PDF Ingestion (16-page deck):
  ├─ Text extraction: ~100ms
  ├─ Vision analysis (concurrent, 16 pages):
  │  ├─ Render: 500ms
  │  ├─ API calls: 3-5s (parallel)
  │  └─ Parse: 200ms
  ├─ Embedding generation: 2s
  ├─ Qdrant upsert: 500ms
  └─ Total: 5-8 seconds

Evaluation (5 categories):
  ├─ Semantic search × 5: ~2 seconds
  │  (Parallel queries, sequential categories)
  │
  ├─ LLM extraction × 5: ~15-25 seconds
  │  (Sequential per category, ~3-5s per call)
  │
  ├─ Scoring: <100ms
  └─ Total: 30-60 seconds


CONCURRENCY:

Within Document:
  └─ Vision: 16 pages parallel (asyncio.gather)

Across Categories:
  └─ Search: Parallel (task.gather)
  └─ LLM: Sequential (bottleneck)

Scaling:
  ├─ Multiple documents: Can process in parallel
  ├─ GPU embedding: Would improve by 50%
  ├─ Batch LLM: Could reduce by 30%
  └─ Caching: Query embeddings (10-20% faster)
```

---

## 7. Data Isolation & Security

```
DEAL_ID ISOLATION:

Ingestion:
  └─ All chunks tagged with startup_id/deal_id
     {payload: {startup_id: "tesla", ...}}

Qdrant Indexing:
  └─ deal_id keyword index
     (Fast filtering by company)

Evaluation:
  └─ All searches filtered: deal_id == "tesla"
     (Zero cross-company data leakage)

Retrieval:
  └─ LLM never sees other companies' data
     (Safe for multi-tenant scenarios)
```

---

**Document Version:** 1.0  
**Last Updated:** 2026-06-16  
**Status:** Complete System Documentation
