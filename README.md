# VentureMind AI

> AI-Powered Startup Due Diligence Platform

VentureMind AI is a multi-agent system that helps investors evaluate startups by combining:

- External market research
- Startup document intelligence
- Retrieval-Augmented Generation (RAG)
- Agent debates
- Reflection loops
- Risk analysis
- Investment committee decisions

The platform simulates how a real venture capital firm performs startup due diligence.

---

# Features

## Startup Analysis

Analyze startups using:

- Startup Website
- Pitch Deck (PDF)
- External Research Sources

---

## Knowledge Intelligence Layer

Extract structured knowledge from:

- PDFs
- Images
- Charts
- Tables
- Startup Websites

Pipeline:

```text
PDF
 ↓
Vision Analysis
 ↓
Structured Knowledge
 ↓
Qdrant
```

---

## Research Intelligence Layer

Research:

- Founders
- Competitors
- Market Trends
- Industry Insights
- Funding Information

Sources:

- Tavily
- Firecrawl
- Crunchbase (Optional)
- LinkedIn (Optional)

---

## Investment Committee

The system simulates a VC investment committee.

### Bull Agent

Builds the strongest investment case.

### Bear Agent

Builds the strongest rejection case.

### Reviewer Agent

Checks completeness and quality.

### Red Team Agent

Challenges assumptions and claims.

### Committee Agent

Makes the final investment decision.

---

## Reflection Loop

If the Reviewer Agent identifies issues:

```text
Reviewer
    ↓
Feedback
    ↓
Regenerate
    ↓
Review Again
```

The cycle continues until:

- Approved
- Retry limit reached

---

## Digital Twin

Simulates future startup scenarios.

Examples:

- Revenue decline
- Market expansion
- New competitors
- Increased acquisition cost

---

# Architecture

```text
Startup Input
       │
       ▼
Knowledge Layer
       │
       ▼
Research Agent
       │
       ▼
Bull Agent
       │
       ▼
Bear Agent
       │
       ▼
Reviewer
       │
 Approved?
   ┌───┴───┐
   │       │
  No      Yes
   │       │
Reflection │
   │       ▼
   └──> Red Team
             │
             ▼
        Committee
             │
             ▼
       Digital Twin
             │
             ▼
        Final Report
```

---

# Technology Stack

## Frontend

- React
- TypeScript
- TailwindCSS

## Backend

- FastAPI
- LangGraph
- LangChain

## LLM Layer

OpenAI SDK

Supports:

- OpenAI
- OpenRouter
- Azure OpenAI
- Ollama
- Local Models

Configuration is environment-driven.

## Database

### PostgreSQL

Stores:

- Analysis Metadata
- Startup Records
- Reports

### Qdrant Cloud

Stores:

- Embeddings
- Knowledge Objects
- Startup Memory

---

# Repository Structure

```text
frontend/

backend/
├── services/
├── agents/
├── ingestion/
├── knowledge/
├── api/
├── orchestrator/
├── contracts/
├── database/
├── llm/
└── config/
```

---

# Team Ownership

## Person 1

Owns:

```text
frontend/
```

Responsibilities:

- UI
- Dashboards
- Report Screens
- API Integration

---

## Person 2

Owns:

```text
backend/services/
backend/agents/research/
```

Responsibilities:

- Tavily
- Firecrawl
- Founder Research
- Competitor Discovery
- Market Analysis

---

## Person 3

Owns:

```text
backend/ingestion/
backend/knowledge/
```

Responsibilities:

- PDF Processing
- Vision Analysis
- Qdrant
- Embeddings
- Memory

---

## Person 4

Owns:

```text
backend/agents/bull/
backend/agents/bear/
backend/agents/reviewer/
backend/agents/red_team/
backend/agents/committee/
backend/agents/digital_twin/
```

Responsibilities:

- Bull Agent
- Bear Agent
- Reviewer
- Red Team
- Committee
- Digital Twin

---

## Person 5

Owns:

```text
backend/api/
backend/orchestrator/
backend/contracts/
backend/database/
backend/llm/
backend/config/
```

Responsibilities:

- FastAPI
- LangGraph
- OpenAI Wrapper
- PostgreSQL
- Shared Contracts
- Workflow Orchestration

---

# Contracts

All shared contracts live in:

```text
backend/contracts/
```

Examples:

```text
startup.py
research.py
knowledge.py
bull.py
bear.py
review.py
red_team.py
committee.py
simulation.py
report.py
state.py
```

## Rule

No module may import another module's internal implementation.

Modules communicate only through contracts.


---

# Development Workflow

1. Freeze contracts
2. Build modules independently
3. Use mocked responses during development
4. Integrate through LangGraph
5. Perform end-to-end testing
6. Prepare demo flow

---

# Project Goal

Build an AI Venture Capital Firm that can:

- Analyze startups
- Research markets
- Debate investment decisions
- Challenge assumptions
- Simulate future outcomes
- Generate investor-ready reports