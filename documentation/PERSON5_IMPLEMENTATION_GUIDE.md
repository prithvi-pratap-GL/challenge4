# Person 5 Implementation Guide

## Completing Platform & Orchestration

---

## Overview

Person 4 has delivered all 6 analytical agents, fully tested and integrated with the LLM client. Your task is to build the orchestration layer that ties everything together.

**Current Status**:
- ✅ All agent contracts ready
- ✅ LLM client fully functional
- ✅ Database models defined
- ✅ API structure in place
- ⏳ Orchestrator nodes need implementation
- ❌ Config module missing

---

## Step 1: Create Config Module

### Create Files

```bash
mkdir -p backend/config
touch backend/config/__init__.py
touch backend/config/settings.py
touch backend/config/env.py
touch backend/config/logging.py
```

### Implementation: settings.py

```python
from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    """Application settings from environment variables."""
    
    # LLM Configuration
    API_KEY: str
    MODEL_NAME: str = "gpt-4o-mini"
    BASE_URL: str = "https://api.openai.com/v1"
    LLM_TEMPERATURE: float = 0.7
    
    # Database Configuration
    DATABASE_URL: str
    
    # API Configuration
    API_HOST: str = "0.0.0.0"
    API_PORT: int = 8000
    API_DEBUG: bool = False
    
    # Logging Configuration
    LOG_LEVEL: str = "INFO"
    
    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()
```

### Implementation: env.py

```python
import os
from backend.config.settings import settings

def load_env():
    """Load environment variables."""
    return {
        'api_key': settings.API_KEY,
        'model_name': settings.MODEL_NAME,
        'base_url': settings.BASE_URL,
        'database_url': settings.DATABASE_URL,
        'log_level': settings.LOG_LEVEL,
    }
```

### Implementation: logging.py

```python
import logging
from backend.config.settings import settings

def setup_logging():
    """Configure application logging."""
    logging.basicConfig(
        level=getattr(logging, settings.LOG_LEVEL),
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
```

### Implementation: __init__.py

```python
from backend.config.settings import Settings, settings
from backend.config.env import load_env
from backend.config.logging import setup_logging

__all__ = ["Settings", "settings", "load_env", "setup_logging"]
```

---

## Step 2: Implement Orchestrator Nodes

### Edit: backend/orchestrator/graph.py

Replace the stubs with actual implementations:

```python
"""LangGraph workflow graph definition."""

from langgraph.graph import StateGraph
from backend.contracts import AnalysisState

# Import Person 2 research agent
from backend.agents.research.agent import run_research

# Import Person 3 knowledge agent
from backend.agents.knowledge.agent import run_knowledge

# Import Person 4 agents
from backend.agents.bull.agent import run_bull_case
from backend.agents.bear.agent import run_bear_case
from backend.agents.red_team.agent import run_red_team
from backend.agents.reviewer.agent import review_analysis
from backend.agents.committee.agent import run_committee
from backend.agents.digital_twin.agent import simulate_scenarios


async def node_research(state: AnalysisState) -> AnalysisState:
    """Research node - calls Person 2's research agent."""
    research_output = await run_research(state.startup_input)
    state.research_output = research_output
    return state


async def node_knowledge(state: AnalysisState) -> AnalysisState:
    """Knowledge node - calls Person 3's knowledge agent."""
    knowledge_output = await run_knowledge(
        state.startup_input,
        state.research_output
    )
    state.knowledge_output = knowledge_output
    return state


async def node_bull(state: AnalysisState) -> AnalysisState:
    """Bull agent node - calls Person 4's Bull agent."""
    bull_output = await run_bull_case(
        state.research_output,
        state.knowledge_output
    )
    state.bull_output = bull_output
    return state


async def node_bear(state: AnalysisState) -> AnalysisState:
    """Bear agent node - calls Person 4's Bear agent."""
    bear_output = await run_bear_case(
        state.research_output,
        state.knowledge_output
    )
    state.bear_output = bear_output
    return state


async def node_red_team(state: AnalysisState) -> AnalysisState:
    """Red Team agent node - calls Person 4's Red Team agent."""
    red_team_output = await run_red_team(
        state.research_output,
        state.knowledge_output
    )
    state.red_team_output = red_team_output
    return state


async def node_reviewer(state: AnalysisState) -> AnalysisState:
    """Reviewer node - calls Person 4's Reviewer agent."""
    review_output = await review_analysis(
        state.bull_output,
        state.bear_output,
        state.red_team_output,
        state.research_output,
        state.knowledge_output
    )
    state.review_output = review_output
    
    # Check if retry is needed
    if review_output.retry_required:
        # Reset for retry
        state.bull_output = None
        state.bear_output = None
        state.red_team_output = None
    
    return state


async def node_committee(state: AnalysisState) -> AnalysisState:
    """Committee node - calls Person 4's Committee agent."""
    committee_output = await run_committee(
        state.bull_output,
        state.bear_output,
        state.red_team_output,
        state.research_output,
        state.knowledge_output
    )
    state.committee_decision = committee_output
    return state


async def node_digital_twin(state: AnalysisState) -> AnalysisState:
    """Digital Twin node - calls Person 4's Digital Twin agent."""
    simulation_output = await simulate_scenarios(
        state.research_output,
        state.knowledge_output
    )
    state.simulation_output = simulation_output
    return state


async def node_final_report(state: AnalysisState) -> AnalysisState:
    """Generate final report - Person 5 implements."""
    # Synthesize all outputs into FinalReport
    from backend.contracts import FinalReport
    
    final_report = FinalReport(
        founder_score=80,  # Extract from outputs
        market_score=75,   # Extract from outputs
        risk_score=60,     # Extract from outputs
        recommendation=state.committee_decision.reasoning,
        executive_summary=f"Committee verdict: {state.committee_decision.verdict}",
        committee_decision=state.committee_decision.verdict
    )
    state.final_report = final_report
    return state


def build_analysis_graph() -> StateGraph:
    """
    Build the complete analysis workflow graph.

    Workflow:
    1. Start → Research (Person 2)
    2. Research → Knowledge (Person 3)
    3. Knowledge → Bull & Bear (Person 4, parallel)
    4. Bull & Bear → Red Team (Person 4, parallel)
    5. Red Team → Reviewer (Person 4)
    6. Reviewer → [Decision: retry?]
       - If retry: → Bull (back to step 3)
       - If ok: → Committee
    7. Committee → Digital Twin (Person 4)
    8. Digital Twin → Final Report (Person 5)
    9. Final Report → End
    """
    
    graph = StateGraph(AnalysisState)
    
    # Add nodes
    graph.add_node("research", node_research)
    graph.add_node("knowledge", node_knowledge)
    graph.add_node("bull", node_bull)
    graph.add_node("bear", node_bear)
    graph.add_node("red_team", node_red_team)
    graph.add_node("reviewer", node_reviewer)
    graph.add_node("committee", node_committee)
    graph.add_node("digital_twin", node_digital_twin)
    graph.add_node("final_report", node_final_report)
    
    # Add edges - Sequential path
    graph.add_edge("START", "research")
    graph.add_edge("research", "knowledge")
    
    # Parallel execution: Bull and Bear
    graph.add_edge("knowledge", "bull")
    graph.add_edge("knowledge", "bear")
    
    # Red Team parallel with Bull/Bear
    graph.add_edge("knowledge", "red_team")
    
    # Wait for all three to complete, then Reviewer
    graph.add_edge("bull", "reviewer")
    graph.add_edge("bear", "reviewer")
    graph.add_edge("red_team", "reviewer")
    
    # Conditional edge: if retry_required, go back to bull
    def should_retry(state: AnalysisState) -> str:
        if state.review_output and state.review_output.retry_required:
            return "bull"  # Retry from Bull
        else:
            return "committee"  # Continue to Committee
    
    graph.add_conditional_edges(
        "reviewer",
        should_retry,
        {"bull": "bull", "committee": "committee"}
    )
    
    # Continue to Digital Twin
    graph.add_edge("committee", "digital_twin")
    
    # Final Report
    graph.add_edge("digital_twin", "final_report")
    graph.add_edge("final_report", "END")
    
    # Compile graph
    return graph.compile()
```

---

## Step 3: Integrate with API Routes

### Edit: backend/api/routes/analysis.py

```python
from fastapi import APIRouter, HTTPException
from backend.contracts import StartupInput, AnalysisState, FinalReport
from backend.orchestrator.graph import build_analysis_graph
from backend.database.repositories.analysis_repository import AnalysisRepository
from uuid import uuid4

router = APIRouter(prefix="/analysis", tags=["analysis"])

# Initialize orchestrator graph
graph = build_analysis_graph()
repo = AnalysisRepository()


@router.post("/{startup_id}")
async def submit_analysis(startup_id: str, startup_input: StartupInput):
    """Submit startup for analysis."""
    
    # Create initial state
    state = AnalysisState(
        startup_input=startup_input,
        research_output=None,
        knowledge_output=None,
        bull_output=None,
        bear_output=None,
        red_team_output=None,
        review_output=None,
        committee_decision=None,
        simulation_output=None,
        final_report=None
    )
    
    # Run orchestrator
    try:
        final_state = graph.invoke(state)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
    # Save results
    await repo.save_analysis(startup_id, final_state)
    
    return {
        "status": "completed",
        "startup_id": startup_id,
        "verdict": final_state.committee_decision.verdict
    }


@router.get("/{startup_id}")
async def get_analysis(startup_id: str):
    """Get analysis status and results."""
    
    result = await repo.get_analysis(startup_id)
    if not result:
        raise HTTPException(status_code=404, detail="Analysis not found")
    
    return {
        "startup_id": startup_id,
        "status": "completed",
        "committee_decision": result.committee_decision,
        "recommendation": result.final_report.recommendation
    }


@router.get("/{startup_id}/report")
async def get_report(startup_id: str) -> FinalReport:
    """Get final report."""
    
    result = await repo.get_analysis(startup_id)
    if not result or not result.final_report:
        raise HTTPException(status_code=404, detail="Report not found")
    
    return result.final_report
```

---

## Step 4: Create Database Migrations

### Create: backend/database/migrations/001_create_analysis_table.sql

```sql
CREATE TABLE IF NOT EXISTS analyses (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    startup_input JSONB NOT NULL,
    research_output JSONB,
    knowledge_output JSONB,
    bull_output JSONB,
    bear_output JSONB,
    red_team_output JSONB,
    review_output JSONB,
    committee_decision JSONB,
    simulation_output JSONB,
    final_report JSONB,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_analyses_created_at ON analyses(created_at);
```

---

## Step 5: Environment Configuration

### Create: .env

```
# LLM Configuration
API_KEY=your-api-key-here
MODEL_NAME=gpt-4o-mini
BASE_URL=https://api.openai.com/v1
LLM_TEMPERATURE=0.7

# Database Configuration
DATABASE_URL=postgresql://user:password@localhost:5432/venturemind

# API Configuration
API_HOST=0.0.0.0
API_PORT=8000
API_DEBUG=false

# Logging
LOG_LEVEL=INFO
```

---

## Step 6: Testing

### Test Orchestrator

```bash
# Create test file: tests/test_orchestrator.py

import pytest
from backend.orchestrator.graph import build_analysis_graph
from backend.contracts import AnalysisState, StartupInput

@pytest.mark.asyncio
async def test_orchestrator_execution():
    """Test complete orchestrator execution."""
    
    graph = build_analysis_graph()
    
    startup_input = StartupInput(
        startup_name="TestCo",
        website_url="https://testco.com",
        pitch_deck_path=None
    )
    
    state = AnalysisState(startup_input=startup_input)
    
    # Run orchestrator
    final_state = graph.invoke(state)
    
    # Verify all outputs are populated
    assert final_state.research_output is not None
    assert final_state.knowledge_output is not None
    assert final_state.bull_output is not None
    assert final_state.bear_output is not None
    assert final_state.committee_decision is not None
    assert final_state.final_report is not None
```

### Run Tests

```bash
pytest tests/test_orchestrator.py -v
pytest tests/test_agents_integration.py -v
pytest tests/test_api_routes.py -v
```

---

## Implementation Checklist

- [ ] Create backend/config/ module (settings.py, env.py, logging.py)
- [ ] Implement 8 orchestrator node functions
- [ ] Build and compile LangGraph StateGraph
- [ ] Integrate API routes with orchestrator
- [ ] Create database migration scripts
- [ ] Set up .env file with configuration
- [ ] Test orchestrator execution end-to-end
- [ ] Test API routes
- [ ] Verify LLM client integration
- [ ] Check Pydantic schema validation

---

## Success Criteria

✅ All agent functions called in orchestrator
✅ State flows correctly through 8 nodes
✅ Conditional retry logic works
✅ API endpoints respond correctly
✅ Database saves all intermediate outputs
✅ Final report generated successfully
✅ All tests pass
✅ No import violations (only use contracts)

---

## Key Integration Points

**Person 4 Agents Called**:
```python
from backend.agents.bull.agent import run_bull_case
from backend.agents.bear.agent import run_bear_case
from backend.agents.red_team.agent import run_red_team
from backend.agents.reviewer.agent import review_analysis
from backend.agents.committee.agent import run_committee
from backend.agents.digital_twin.agent import simulate_scenarios
```

**Schemas Imported**:
```python
from backend.contracts import (
    AnalysisState,
    StartupInput,
    ResearchOutput,
    KnowledgeOutput,
    BullOutput,
    BearOutput,
    RedTeamOutput,
    ReviewOutput,
    CommitteeDecision,
    SimulationOutput,
    FinalReport
)
```

**LLM Client Ready**:
```python
from backend.llm.client import LLMClient
# Already integrated in all Person 4 agents
```

---

## Timeline Estimate

- Config module: **1-2 hours**
- Orchestrator nodes: **3-4 hours**
- API integration: **1-2 hours**
- Database/migrations: **1 hour**
- Testing: **2 hours**

**Total: 8-11 hours** to completion

---

**Status**: All Person 4 deliverables ready. You have everything you need to complete orchestration.

Good luck! 🚀
