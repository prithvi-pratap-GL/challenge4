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

# Technology Stack

## Frontend

- React
- TypeScript
- TailwindCSS

## Backend

- FastAPI
- LangGraph
- LangChain
- OpenAI

## Database

- PostgreSQL
- Qdrant Vector DB

---

# Team Ownership

## Person 1

Frontend application and UI

## Person 2

Research Intelligence - Tavily, Firecrawl, market analysis

## Person 3

Knowledge Intelligence - PDF/website ingestion, embeddings, Qdrant

## Person 4

Agent Intelligence - Bull, Bear, Red Team, Reviewer, Committee, Digital Twin

## Person 5

Platform & Orchestration - API, orchestrator, contracts, database, LLM client

---

# Architecture

```text
Startup Input
    ↓
Research Layer (Person 2)
    ↓
Knowledge Layer (Person 3)
    ↓
Parallel Agents (Person 4)
├── Bull Agent
├── Bear Agent
└── Red Team Agent
    ↓
Reviewer Agent
    ↓
Committee Agent
    ↓
Digital Twin
    ↓
Final Report
```

---

# Integration

All persons' code is integrated through shared contracts in `backend/contracts/`.

**Critical Rule**: No module may import internal implementation from another module. Only shared contracts may be imported.

---

**Status**: All 5 persons integrated and ready for testing
