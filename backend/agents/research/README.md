# Research Intelligence Module - Person 2

## Overview

This module is owned by **Person 2 - Research Intelligence Owner** and provides the core research pipeline for VentureMind AI.

## Public Interface

```python
from backend.contracts.startup import StartupInput
from backend.contracts.research import ResearchOutput
from backend.agents.research.agent import run_research

# Input contract
startup = StartupInput(
    startup_name="Airbnb",
    website_url="https://www.airbnb.com",
    pitch_deck_path=None
)

# Call research function
research_output: ResearchOutput = run_research(startup)

# Output structure
print(research_output.founders)        # List[Founder]
print(research_output.competitors)     # List[Competitor]
print(research_output.market_summary)  # str
print(research_output.funding_summary) # str
print(research_output.industry_summary)# str
print(research_output.sources)         # List[str]
```

## Module Structure

```
backend/agents/research/
├── __init__.py           # Module exports
├── agent.py              # Main research agent (PUBLIC INTERFACE)
├── workflow.py           # Research workflow orchestration
├── prompts.py            # Agent prompts
├── mock_data.py          # Mock data for testing
└── README.md             # This file

backend/services/tavily/
├── __init__.py
└── client.py             # Tavily API wrapper

backend/services/firecrawl/
├── __init__.py
└── client.py             # Firecrawl API wrapper

backend/contracts/
├── startup.py            # StartupInput contract
└── research.py           # ResearchOutput contract (PERSON 2 PUBLISHES THIS)
```

## Key Contracts

### Input: StartupInput
```python
@dataclass
class StartupInput:
    startup_name: str
    website_url: Optional[str] = None
    pitch_deck_path: Optional[str] = None
```

### Output: ResearchOutput
```python
@dataclass
class ResearchOutput:
    founders: List[Founder]            # Founder profiles and credibility
    competitors: List[Competitor]      # Competitive landscape
    market_summary: str                # Market size, trends, dynamics
    funding_summary: str               # Funding history and trajectory
    industry_summary: str              # Industry context, regulations, trends
    sources: List[str]                 # All URLs used in research
```

## Research Agents (5 Total)

1. **Founder Intelligence Agent**
   - Research founder backgrounds and credibility
   - Output: `founders: List[Founder]`

2. **Competitor Discovery Agent**
   - Identify and analyze competitors
   - Output: `competitors: List[Competitor]`

3. **Market Analyst Agent**
   - Estimate market size (TAM/SAM/SOM)
   - Output: `market_summary: str`

4. **Funding Tracker Agent**
   - Research funding history and investor signals
   - Output: `funding_summary: str`

5. **Industry Intelligence Agent**
   - Analyze industry dynamics, regulations, trends
   - Output: `industry_summary: str`

## Data Sources

| Source | Purpose | Ownership |
|--------|---------|-----------|
| **Tavily Search API** | Web search for all research | Person 2 |
| **Firecrawl** | Website data extraction | Person 2 |
| **Crunchbase API** | Funding and company data | Person 2 |
| **LinkedIn** | Founder profiles | Person 2 |

## CRITICAL RULES (Person 2 Contract)

1. **No other team accesses Tavily directly**
   - Only Person 2's module calls Tavily API
   - All other teams use ResearchOutput

2. **ResearchOutput is the interface**
   - Everyone consumes ResearchOutput only
   - No imports of internal Person 2 implementations

3. **Full source attribution**
   - Every finding must be traceable to a source URL
   - Sources list aggregates all URLs used

4. **Module isolation**
   - No imports from other people's internal modules
   - Only import shared contracts

## Usage Examples

### Example 1: Research a Startup
```python
from backend.contracts.startup import StartupInput
from backend.agents.research.agent import run_research

input_data = StartupInput(
    startup_name="OpenAI",
    website_url="https://openai.com"
)

research = run_research(input_data)

print(f"Founders: {[f.name for f in research.founders]}")
print(f"Competitors: {[c.name for c in research.competitors]}")
```

### Example 2: Serialize to JSON
```python
import json

research = run_research(startup_input)
research_dict = research.to_dict()
json_str = json.dumps(research_dict, indent=2)
print(json_str)
```

### Example 3: Person 4 (Bull Agent) Consumes ResearchOutput
```python
# Person 4's code
from backend.contracts.research import ResearchOutput
from backend.agents.research.agent import run_research

research: ResearchOutput = run_research(startup_input)

# Person 4 uses the research output
for founder in research.founders:
    print(f"Founder: {founder.name}, Credibility: {founder.credibility_score}")
```

## Testing

Run the test suite:
```bash
python tests/test_research.py
```

Tests verify:
- ResearchOutput contract structure
- Founder data structure and sources
- Competitor data structure and sources
- Source attribution completeness
- JSON serialization
- Multiple startup handling

## Environment Variables

```env
TAVILY_API_KEY=xxx
FIRECRAWL_API_KEY=xxx
CRUNCHBASE_API_KEY=xxx
LINKEDIN_API_KEY=xxx
```

## Integration Points

### Person 3 (Knowledge Intelligence)
- Receives: ResearchOutput
- Uses for: Initial knowledge base seeding
- Never calls Tavily directly

### Person 4 (Agent Intelligence)
- Receives: ResearchOutput
- Uses for: Bull/Bear/Red Team reasoning
- Never calls Tavily directly

### Person 5 (Platform & Orchestration)
- Calls: `run_research(startup_input: StartupInput) -> ResearchOutput`
- Never accesses internal Person 2 modules

## Development Workflow

1. **Week 1**: API integration + mock data
2. **Week 2**: Implement 5 research agents
3. **Week 3**: Refine and optimize

All development uses mock data until final integration week.

## Future Enhancements

- [ ] Implement CrewAI agents (currently basic implementation)
- [ ] Add Crawl4AI for structured web extraction
- [ ] Implement LLM-based analysis for each agent
- [ ] Add caching to avoid redundant research
- [ ] Implement async parallel research
- [ ] Add confidence scores to findings
- [ ] Implement novelty detection (new vs. seen sources)
