# Person 2 - Quick Reference Guide

## One-Minute Overview

**You are**: Research Intelligence Owner  
**Your job**: Gather startup intelligence and expose via `ResearchOutput` contract  
**Your function**: `run_research(startup_input: StartupInput) → ResearchOutput`  
**Your team**: No one else calls Tavily directly

## Public API (What Others Call)

```python
from backend.agents.research.agent import run_research
from backend.contracts.startup import StartupInput
from backend.contracts.research import ResearchOutput

result: ResearchOutput = run_research(
    StartupInput("Airbnb", "https://airbnb.com", None)
)
```

## Your Output Contract (ResearchOutput)

```python
ResearchOutput(
    founders=[Founder(name, background, experience, credibility_score, sources)],
    competitors=[Competitor(name, market_position, funding, differentiators, sources)],
    market_summary="str",      # 200-500 words
    funding_summary="str",     # 200-500 words
    industry_summary="str",    # 200-500 words
    sources=["url1", "url2", ...]  # All URLs used
)
```

## Your 5 Research Agents

| # | Agent | Output |
|---|-------|--------|
| 1 | Founder Intelligence | List[Founder] with credibility scores |
| 2 | Competitor Discovery | List[Competitor] with differentiators |
| 3 | Market Analysis | market_summary: str |
| 4 | Funding Tracker | funding_summary: str |
| 5 | Industry Intelligence | industry_summary: str |

## Your Data Sources (YOU OWN)

```python
TavilySearchService()    # Web search
FirecrawlService()       # Website extraction
CrunchbaseAPI()          # Funding data
LinkedInAPI()            # Founder profiles
```

## Your Module Files

```
backend/
├── services/tavily/client.py         ← You own
├── services/firecrawl/client.py      ← You own
├── agents/research/
│   ├── agent.py                      ← PUBLIC FUNCTION
│   ├── workflow.py                   ← You own
│   ├── prompts.py                    ← You own
│   └── mock_data.py                  ← You own
└── contracts/
    └── research.py                   ← You publish this
```

## What NOT to Do

```python
# WRONG - Don't let others do this:
from backend.agents.research.workflow import ResearchWorkflow
from backend.services.tavily.client import TavilySearchService

# WRONG - Don't call Tavily directly:
tavily = TavilySearchService()
results = tavily.search(query)

# WRONG - Don't change ResearchOutput without team agreement
```

## What Others Should Do

```python
# CORRECT - Person 5 does this:
from backend.agents.research.agent import run_research
from backend.contracts.research import ResearchOutput

research = run_research(startup_input)

# CORRECT - Person 4 does this:
from backend.contracts.research import ResearchOutput
research: ResearchOutput = run_research(startup_input)
for founder in research.founders:
    print(founder.credibility_score)
```

## Testing

```bash
# Run all tests
python tests/test_research.py

# Expected: ALL TESTS PASSED
```

## Current Status

```
✅ Phase 1 Complete
   - Module structure correct
   - Contracts defined
   - 5 agents implemented
   - Mock data works
   - All tests passing

⏳ Phase 2: Next (API Integration)
   - Real Tavily calls
   - Real Firecrawl calls
   - Real API testing
```

## API Keys Needed

```env
TAVILY_API_KEY=xxxx
FIRECRAWL_API_KEY=xxxx
CRUNCHBASE_API_KEY=xxxx
LINKEDIN_API_KEY=xxxx
```

## Common Tasks

### Use Mock Data (No API calls)
```python
from backend.agents.research.mock_data import get_mock_research_by_startup
research = get_mock_research_by_startup("Airbnb")
```

### Use Real Data (With API calls)
```python
from backend.agents.research.agent import run_research
from backend.contracts.startup import StartupInput
research = run_research(StartupInput("Airbnb"))
```

### Serialize to JSON
```python
research = run_research(startup)
data = research.to_dict()
import json
json.dumps(data)
```

### Check Sources
```python
research = run_research(startup)
for url in research.sources:
    print(url)
```

## Integration Checklist

For **Person 5** integrating with you:

- [ ] Import `run_research` from `backend.agents.research.agent`
- [ ] Create StartupInput with startup data
- [ ] Call `run_research(startup_input)`
- [ ] Store result in workflow state
- [ ] Pass ResearchOutput to Person 3 and Person 4
- [ ] Never call Tavily directly
- [ ] Never import internal modules

For **Person 4** using your research:

- [ ] Import ResearchOutput from `backend.contracts.research`
- [ ] Receive research from Person 5's orchestrator
- [ ] Use `research.founders` for founder analysis
- [ ] Use `research.competitors` for competitive positioning
- [ ] Use `research.market_summary` for market context
- [ ] Use `research.sources` for claim verification
- [ ] Never call Tavily directly

For **Person 3** using your research:

- [ ] Import ResearchOutput from `backend.contracts.research`
- [ ] Receive research from Person 5's orchestrator
- [ ] Use research to seed knowledge base
- [ ] Index sources in Qdrant
- [ ] Never call Tavily directly

## Troubleshooting

### Tests Failing?
1. Check Python path is correct
2. Ensure all `__init__.py` files exist
3. Run from project root directory
4. Check file encoding (Windows UTF-8 issue)

### API Key Not Found?
1. Create `.env` file from `.env.example`
2. Fill in your API keys
3. Ensure TAVILY_API_KEY is set
4. Ensure FIRECRAWL_API_KEY is set

### Contract Changed?
1. Never change ResearchOutput without agreement
2. Contact team immediately if change needed
3. Work through Person 5 for contract updates
4. All dependent modules must update

## Key Files to Know

| File | Purpose |
|------|---------|
| PERSON_2_SPEC.md | Complete specification |
| QUICK_REFERENCE.md | This file |
| README.md | Project overview |
| backend/agents/research/README.md | Module documentation |
| .env.example | Configuration template |
| tests/test_research.py | Test suite |

## Success Metrics

- [x] Tests pass
- [x] Contract is stable
- [x] Mock data works
- [ ] Real APIs integrated
- [ ] Sub-30 second per research
- [ ] Integrated with all teams

---

**Print this out and keep it handy!**
