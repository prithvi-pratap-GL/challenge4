# Person 5 - Platform & Orchestration Implementation

**Role**: You are the Platform Architect responsible for infrastructure, orchestration, and API layer.

## ✅ What's Implemented (Person 5)

### 1. LLM Client & Configuration
**Files**: `backend/llm/`, `backend/config/`

- ✅ OpenAI-compatible LLM wrapper supporting multiple providers
- ✅ Environment-based configuration using Pydantic Settings
- ✅ Structured output support with JSON Schema
- ✅ Streaming and temperature control

**Usage**:
```python
from backend.llm import get_llm_client
from backend.contracts import BullOutput

client = get_llm_client()
response = client.generate(
    system_prompt="...",
    user_prompt="...",
    response_model=BullOutput  # Optional structured output
)
```

### 2. Contracts (Data Schemas)
**Files**: `backend/contracts/`

Split into separate files for organization:
- `startup.py` - `StartupInput`
- `research.py` - `ResearchOutput`
- `knowledge.py` - `KnowledgeOutput`, `RetrievalOutput`
- `bull.py` - `BullOutput`
- `bear.py` - `BearOutput`
- `review.py` - `ReviewOutput`
- `red_team.py` - `RedTeamOutput`
- `committee.py` - `CommitteeDecision`
- `simulation.py` - `SimulationOutput`
- `report.py` - `FinalReport`
- `state.py` - `AnalysisState` (workflow state)

All contracts use Pydantic for validation.

### 3. FastAPI Application
**Files**: `backend/api/`

**Main entry point**: `backend/api/main.py`
- FastAPI app with CORS middleware
- Lifecycle management (startup/shutdown)
- Routes for analysis, health checks

**Routes**: `backend/api/routes/`
- `health.py` - `/health`, `/ready` endpoints
- `analysis.py` - `/analysis`, `/report`, `/committee` endpoints

**Run the API**:
```bash
cd backend
python -m uvicorn api.main:app --reload
```

### 4. LangGraph Orchestrator
**Files**: `backend/orchestrator/`

**Workflow Graph**: `graph.py`
- Defines DAG (Directed Acyclic Graph) for analysis pipeline
- Node definitions for each agent
- Edge connections between agents
- Parallel execution where applicable

**State Management**: `state.py`
- `StateManager` class for state transitions
- Methods to update state after each agent completes

**Workflow Executor**: `workflow.py`
- `AnalysisWorkflow` class
- Methods to execute pipeline
- Stream execution results
- Cancel workflows

**Workflow Order**:
```
1. Research (Person 2) → ResearchOutput
2. Knowledge (Person 3) → KnowledgeOutput
3. Bull & Bear (Person 4) [parallel] → BullOutput, BearOutput
4. Reviewer (Person 4) → ReviewOutput
5. Red Team (Person 4) [parallel] → RedTeamOutput
6. Committee (Person 4) → CommitteeDecision
7. Digital Twin (Person 4) → SimulationOutput
8. Final Report (Person 5) → FinalReport
```

### 5. PostgreSQL Database
**Files**: `backend/database/`

**Connection**: `postgres.py`
- SQLAlchemy engine setup
- Session management
- Database initialization functions

**Models**: `models/analysis.py`
- `AnalysisRecord` - Stores analysis execution records
- Tracks status, progress, all intermediate outputs
- Stores final results

**Repository**: `repositories/analysis_repository.py`
- `AnalysisRepository` - Data access layer
- Methods to create, read, update analysis records
- Methods to update specific outputs

**Usage**:
```python
from backend.database.postgres import get_db
from backend.database.repositories import AnalysisRepository

db = SessionLocal()
repo = AnalysisRepository(db)
analysis = repo.create(startup_name="Airbnb")
repo.update_status(analysis.id, "processing", current_agent="research")
```

### 6. Shared Utilities
**Files**: `backend/shared/`

- `logger.py` - Logging configuration
- `exceptions.py` - Custom exception hierarchy
- `utils.py` - Helper functions (JSON serialization, progress calc, etc.)

## 📋 TODO - What Needs Implementation

### Database Initialization
```python
# In main.py or startup script
from backend.database.postgres import init_db
init_db()
```

### Complete LangGraph Integration
The `backend/orchestrator/graph.py` has node stubs. You need to:

1. Import actual agent implementations when other team members complete them
2. Build the StateGraph with nodes and edges
3. Implement error handling and retries
4. Add conditional routing if needed

Example structure:
```python
from langgraph.graph import StateGraph, END
from backend.agents.research import ResearchAgent
from backend.agents.bull import BullAgent
# ... etc

def build_analysis_graph():
    graph = StateGraph(AnalysisState)
    
    # Add nodes
    graph.add_node("research", node_research)
    graph.add_node("knowledge", node_knowledge)
    graph.add_node("bull", node_bull)
    graph.add_node("bear", node_bear)
    # ... etc
    
    # Add edges
    graph.add_edge("START", "research")
    graph.add_edge("research", "knowledge")
    # ... etc
    
    return graph.compile()
```

### Complete API Endpoints
`backend/api/routes/analysis.py` has endpoint stubs:

1. `POST /analysis` - Start new analysis
2. `GET /analysis/{id}` - Get status
3. `GET /report/{id}` - Get final report
4. `GET /committee/{id}` - Get committee decision
5. `GET /analysis/{id}/progress` - Get detailed progress

You'll need to:
- Call `AnalysisWorkflow.execute()`
- Store analysis ID in database
- Return status updates
- Handle errors gracefully

### Workflow State Persistence
Currently state is in-memory. Consider:
- Persisting state to database between steps
- Implementing checkpoints for recovery
- Adding webhooks for external notifications

### Authentication & Authorization
Currently wide open. Consider adding:
- API key authentication
- Role-based access control
- Rate limiting

## 🔧 Configuration

**Environment Variables** (see `.env.example`):
```
# LLM
MODEL_NAME=gpt-4o-mini
BASE_URL=https://api.openai.com/v1
API_KEY=sk-...
TEMPERATURE=0.7

# Database
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_USER=venturemind_user
POSTGRES_PASSWORD=...
POSTGRES_DB=venturemind_ai

# External APIs (for Person 2/3)
TAVILY_API_KEY=...
QDRANT_URL=...
QDRANT_API_KEY=...
```

## 📁 Directory Structure (Person 5 Ownership)

```
backend/
├── api/                      ← FastAPI application
│   ├── main.py              ✅ Implemented
│   ├── routes/
│   │   ├── health.py        ✅ Implemented
│   │   └── analysis.py      ⚠️  Stubs only
│   ├── dependencies/        📦 For DI
│   └── middleware/          📦 For middleware
│
├── orchestrator/             ← LangGraph workflow
│   ├── graph.py             ⚠️  Structure only
│   ├── state.py             ✅ Implemented
│   └── workflow.py          ⚠️  Stubs only
│
├── contracts/               ← Data schemas (frozen)
│   ├── startup.py           ✅ Implemented
│   ├── research.py          ✅ Implemented
│   ├── knowledge.py         ✅ Implemented
│   ├── bull.py              ✅ Implemented
│   ├── bear.py              ✅ Implemented
│   ├── review.py            ✅ Implemented
│   ├── red_team.py          ✅ Implemented
│   ├── committee.py         ✅ Implemented
│   ├── simulation.py        ✅ Implemented
│   ├── report.py            ✅ Implemented
│   ├── state.py             ✅ Implemented
│   └── __init__.py          ✅ Implemented
│
├── database/                ← PostgreSQL
│   ├── postgres.py          ✅ Implemented
│   ├── models/
│   │   ├── analysis.py      ✅ Implemented
│   │   └── __init__.py      ✅ Implemented
│   └── repositories/
│       ├── analysis_repository.py ✅ Implemented
│       └── __init__.py      ✅ Implemented
│
├── llm/                     ← LLM client
│   ├── client.py            ✅ Implemented
│   └── __init__.py          ✅ Implemented
│
├── config/                  ← Configuration
│   ├── settings.py          ✅ Implemented
│   └── __init__.py          ✅ Implemented
│
├── shared/                  ← Utilities
│   ├── logger.py            ✅ Implemented
│   ├── exceptions.py        ✅ Implemented
│   ├── utils.py             ✅ Implemented
│   └── __init__.py          ✅ Implemented
│
└── knowledge/               ← Person 3 owns this
    ├── embeddings/
    ├── qdrant/
    ├── retrieval/
    └── memory/
```

## 🔗 Integration Points

### With Person 2 (Research)
- Calls `research_agent.run_research(startup_input)` in workflow
- Expects `ResearchOutput` contract
- Stores result in analysis record

### With Person 3 (Knowledge)
- Calls `knowledge_agent.ingest_*()` in workflow  
- Expects `KnowledgeOutput` contract
- Stores embeddings in Qdrant (Person 3 manages)

### With Person 4 (Agents)
- Calls all agent `.run()` methods in workflow
- Passes research + knowledge outputs
- Expects contracts: Bull, Bear, Review, RedTeam, Committee, Simulation
- Aggregates outputs for final report

### With Frontend (Person 1)
- Provides REST API at `/api/v1/*`
- Returns JSON responses
- Streams progress updates

## 🚀 Getting Started

1. **Setup environment**:
   ```bash
   cp .env.example .env
   # Edit .env with your credentials
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Initialize database**:
   ```python
   from backend.database.postgres import init_db
   init_db()
   ```

4. **Start API server**:
   ```bash
   python -m uvicorn backend.api.main:app --reload --host 0.0.0.0 --port 8000
   ```

5. **Test health endpoint**:
   ```bash
   curl http://localhost:8000/health
   ```

## 📊 Testing

Unit tests are in `backend/tests/`:
- `test_llm_client.py` - LLM client tests

Add more tests as you implement features.

Run tests:
```bash
pytest backend/tests/ -v
```

## 🎯 Next Steps (Priority Order)

1. ⚠️ **Complete LangGraph Graph** (`backend/orchestrator/graph.py`)
   - Import actual agent implementations
   - Build StateGraph with all nodes
   - Define all edges and routing

2. ⚠️ **Complete API Endpoints** (`backend/api/routes/analysis.py`)
   - Implement analysis start endpoint
   - Implement status polling endpoint
   - Implement report retrieval endpoint
   - Add proper error handling

3. 📊 **Workflow Execution** (`backend/orchestrator/workflow.py`)
   - Implement `execute()` method
   - Add progress tracking
   - Add error handling and recovery

4. 🔐 **Add Authentication**
   - API key validation
   - Request signing

5. 📈 **Add Monitoring**
   - Logging of agent execution
   - Metrics collection
   - Error tracking

6. 🧪 **Add Integration Tests**
   - Test full workflow
   - Test database persistence
   - Test API endpoints

## 💡 Notes

- **Contracts are frozen**: Other team members depend on these schemas. Don't modify without discussion.
- **Parallel execution**: Bull and Bear agents run in parallel. Red Team can also run in parallel.
- **Error handling**: Consider what happens if any agent fails. Should workflow retry? Continue?
- **Scalability**: Consider using Celery or similar for async task queue if workflows get heavy.
- **Streaming**: Consider WebSocket support for real-time progress updates to frontend.

## 📞 Support

When other team members implement their modules, ask them to:
1. Create the node function that takes `AnalysisState` and returns `AnalysisState`
2. Update their output in the state
3. Return the updated state

Example:
```python
def run_bull_agent(state: AnalysisState) -> AnalysisState:
    agent = BullAgent()
    output = agent.run(
        state.research_output,
        state.knowledge_output
    )
    state.bull_output = output
    return state
```

---

**Status**: ✅ Ready for team integration  
**Ownership**: Person 5 (You)  
**Last Updated**: 2024-06-12
