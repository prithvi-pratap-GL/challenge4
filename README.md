# VentureMind AI - Startup Due Diligence Platform

## Overview

VentureMind AI is a multi-agent system that automates startup due diligence analysis using AI agents, external research, knowledge bases, and simulations.

**Status**: Phase 1 Complete - Research Intelligence Module Ready

## 🏗️ Project Structure

```
venturemind-ai/
├── frontend/                    (Person 1 - Frontend Owner)
│   └── [React/TypeScript UI]
│
├── backend/
│   ├── services/               (Person 2 - Research Owner)
│   │   ├── tavily/            ← Web search API
│   │   ├── firecrawl/         ← Website extraction
│   │   ├── crunchbase/        ← Funding data
│   │   └── linkedin/          ← Founder profiles
│   │
│   ├── agents/
│   │   ├── research/          (Person 2 - Research Owner)
│   │   │   └── 5 research agents
│   │   ├── bull/              (Person 4 - Agent Owner)
│   │   ├── bear/              (Person 4 - Agent Owner)
│   │   ├── reviewer/          (Person 4 - Agent Owner)
│   │   ├── red_team/          (Person 4 - Agent Owner)
│   │   ├── committee/         (Person 4 - Agent Owner)
│   │   └── digital_twin/      (Person 4 - Agent Owner)
│   │
│   ├── ingestion/             (Person 3 - Knowledge Owner)
│   │   ├── pdf/              ← PDF parsing
│   │   ├── website/          ← Website ingestion
│   │   └── vision/           ← Vision analysis
│   │
│   ├── knowledge/             (Person 3 - Knowledge Owner)
│   │   ├── embeddings/
│   │   ├── qdrant/
│   │   ├── retrieval/
│   │   └── memory/
│   │
│   ├── api/                   (Person 5 - Platform Owner)
│   │   ├── routes/
│   │   ├── dependencies/
│   │   └── middleware/
│   │
│   ├── orchestrator/          (Person 5 - Platform Owner)
│   │   ├── graph.py
│   │   ├── workflow.py
│   │   └── state.py
│   │
│   ├── contracts/             (Person 5 - Platform Owner)
│   │   ├── startup.py
│   │   └── research.py        (Published by Person 2)
│   │
│   ├── database/              (Person 5 - Platform Owner)
│   ├── llm/                   (Person 5 - Platform Owner)
│   ├── config/                (Person 5 - Platform Owner)
│   ├── shared/
│   └── main.py
│
├── tests/
│   └── test_research.py       (All tests passing)
│
├── .env.example
├── PERSON_2_SPEC.md          (Person 2's complete specification)
└── README.md                  (This file)
```

## 👥 Team Distribution

| Role | Owner | Modules | Status |
|------|-------|---------|--------|
| **Person 1** | Frontend | frontend/ | Not started |
| **Person 2** | Research Intelligence | services/{tavily,firecrawl}, agents/research/ | ✅ **COMPLETE** |
| **Person 3** | Knowledge Intelligence | ingestion/, knowledge/ | Not started |
| **Person 4** | Agent Intelligence | agents/{bull,bear,reviewer,red_team,committee,digital_twin} | Not started |
| **Person 5** | Platform & Orchestration | api/, orchestrator/, contracts/, database/, llm/ | Not started |

## 🔍 Person 2: Research Intelligence Module

**Status: PHASE 1 COMPLETE** ✅

### What It Does
- Gathers intelligence about startups from external sources
- Profiles founders, competitors, market, funding, and industry
- Exposes findings through a standardized contract

### Public Interface
```python
from backend.agents.research.agent import run_research
from backend.contracts.startup import StartupInput
from backend.contracts.research import ResearchOutput

startup = StartupInput("Airbnb", "https://airbnb.com")
research: ResearchOutput = run_research(startup)

# Access research findings
print(research.founders)           # List of founders with credibility
print(research.competitors)        # Competitive landscape
print(research.market_summary)     # Market analysis
print(research.funding_summary)    # Funding history
print(research.industry_summary)   # Industry context
print(research.sources)            # All sources used
```

### 5 Research Agents
1. **Founder Intelligence Agent** - Founder backgrounds and credibility
2. **Competitor Discovery Agent** - Competitive landscape analysis
3. **Market Analyst Agent** - TAM, growth, trends
4. **Funding Tracker Agent** - Funding history and investor signals
5. **Industry Intelligence Agent** - Regulatory, macro trends

### Data Sources
- Tavily Search (web research)
- Firecrawl (website extraction)
- Crunchbase (funding data)
- LinkedIn (founder profiles)

### Testing
All 6 tests passing:
```bash
cd backend && python -m pytest tests/test_research.py
# or
python tests/test_research.py
```

## 📋 Person 2's Deliverables

### ✅ Completed in Phase 1

1. **Module Structure**
   - Correct folder organization
   - Module ownership boundaries
   - Contract-based interfaces

2. **Contracts**
   - `StartupInput` - Input contract
   - `ResearchOutput` - Output contract
   - `Founder` and `Competitor` data structures

3. **API Wrappers**
   - Tavily Search client
   - Firecrawl client
   - Crunchbase placeholder
   - LinkedIn placeholder

4. **Research Agents** (5 total)
   - Founder Intelligence
   - Competitor Discovery
   - Market Analysis
   - Funding Tracking
   - Industry Intelligence

5. **Public Function**
   - `run_research(startup_input) → ResearchOutput`
   - Singleton pattern for reusability
   - Error handling and fallbacks

6. **Mock Data**
   - Airbnb example research
   - Stripe example research
   - Generic fallback for testing

7. **Test Suite**
   - Contract structure validation
   - Data structure validation
   - Source attribution verification
   - JSON serialization testing
   - Multi-startup testing

8. **Documentation**
   - PERSON_2_SPEC.md (complete spec)
   - README.md in agents/research/
   - Code examples and integration patterns
   - .env.example configuration

## 🚀 Quick Start

### 1. Setup Environment
```bash
cd backend
cp ../.env.example ../.env
# Edit .env with your API keys
```

### 2. Install Dependencies
```bash
pip install tavily-python firecrawl-python python-crunchbase
```

### 3. Run Tests
```bash
python ../tests/test_research.py
```

### 4. Use in Your Code
```python
from backend.contracts.startup import StartupInput
from backend.agents.research.agent import run_research

startup = StartupInput("OpenAI", "https://openai.com")
research = run_research(startup)
print(f"Found {len(research.founders)} founders")
```

## 📊 Integration Points

### Person 3 (Knowledge Intelligence)
- **Receives**: ResearchOutput
- **Uses for**: Seeding knowledge base
- **Never**: Calls Tavily directly

### Person 4 (Agent Intelligence)
- **Receives**: ResearchOutput
- **Uses for**: Bull/Bear/Red Team analysis
- **Never**: Calls Tavily directly

### Person 5 (Platform & Orchestration)
- **Calls**: `run_research(startup_input) → ResearchOutput`
- **Stores**: In workflow state
- **Passes**: To Person 3 and Person 4
- **Never**: Imports internal Person 2 modules

## 🔐 Module Contract

### CRITICAL RULES

1. **No one else accesses Tavily directly**
   - Only Person 2's module calls Tavily
   - All other teams use ResearchOutput

2. **Module isolation**
   - Only import public functions: `run_research()`
   - Only import contracts: `StartupInput`, `ResearchOutput`
   - Never import internal modules (workflow, clients, etc.)

3. **Full source attribution**
   - Every finding has sources
   - Global sources list is comprehensive
   - Enables verification by other agents

4. **Contract stability**
   - ResearchOutput structure is frozen
   - Changes only with team agreement
   - Ensures downstream reliability

## 📈 Phase 2: API Integration (Next Week)

- Replace mock data with real Tavily calls
- Implement Firecrawl website scraping
- Integrate Crunchbase API
- Add error handling and retries
- Optimize for cost and speed
- Test with 10+ real startups

## 📈 Phase 3: Advanced Features (Week 3)

- CrewAI agent orchestration
- Parallel agent execution
- Caching and deduplication
- Confidence scoring
- Source novelty detection
- Performance optimization

## 🧪 Testing

### Current Test Coverage
```
✓ ResearchOutput contract structure
✓ Founder data structure
✓ Competitor data structure
✓ Source attribution
✓ JSON serialization
✓ Multiple startup handling
```

### Run Tests
```bash
python tests/test_research.py
```

### Expected Output
```
============================================================
RESEARCH INTELLIGENCE MODULE TEST SUITE
Person 2 - Research Intelligence Owner
============================================================

[PASS] Test 1: Research Output Contract Structure
[PASS] Test 2: Founder Data Structure
[PASS] Test 3: Competitor Data Structure
[PASS] Test 4: Source Attribution
[PASS] Test 5: JSON Serialization
[PASS] Test 6: Multiple Startups

============================================================
[PASS] ALL TESTS PASSED
============================================================
```

## 🛠️ Technologies

**Backend**
- Python 3.8+
- FastAPI (Person 5)
- LangChain / LangGraph (Person 4)
- Pydantic (contracts)

**Data Sources**
- Tavily Search API
- Firecrawl
- Crunchbase API
- LinkedIn API (future)

**Database**
- PostgreSQL (Person 5)
- Qdrant Vector DB (Person 3)

**Frontend**
- React
- TypeScript
- Tailwind CSS

## 📝 Documentation Files

- **PERSON_2_SPEC.md** - Complete Person 2 specification
- **backend/agents/research/README.md** - Research module docs
- **backend/examples/research_integration.py** - Integration examples
- **.env.example** - Environment configuration

## 🎯 Success Criteria (Phase 1)

- [x] Module structure correct
- [x] Contracts defined and stable
- [x] 5 research agents implemented
- [x] run_research() function works
- [x] Mock data covers test cases
- [x] All tests passing
- [x] Full documentation
- [ ] Real API integration
- [ ] Performance tested
- [ ] Integrated with Person 5 orchestrator

## 📞 Next Steps

1. **For Person 2**: Move to Phase 2 - API Integration
   - Replace mock data with Tavily API calls
   - Test with real startups
   - Optimize performance

2. **For Person 5**: Integrate research module
   - Import `run_research` function
   - Add to orchestrator workflow
   - Store research_output in AnalysisState

3. **For Person 4**: Prepare to consume research
   - Import ResearchOutput contract
   - Use for Bull/Bear agent prompts
   - Access founder credibility scores

4. **For Person 3**: Prepare to consume research
   - Import ResearchOutput contract
   - Seed knowledge base
   - Index sources in Qdrant

## 📧 Contact

**Person 2 - Research Intelligence Owner**
- Module: Research Intelligence
- Primary Contact: This README and PERSON_2_SPEC.md

---

**Created**: June 12, 2026  
**Phase**: 1 (Research Module) - COMPLETE ✅  
**Next Phase**: 2 (API Integration)
