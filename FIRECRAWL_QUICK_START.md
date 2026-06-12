# Firecrawl + Tavily Integration - Quick Start

## ✅ Status: WORKING & VERIFIED

Firecrawl enrichment is **automatically integrated** with Tavily search. All research results include full page content.

---

## 🎯 What Happens

```
Your Research Request
    ↓
Tavily searches (gets snippets)
    ↓
Firecrawl enriches top 3 URLs (gets full content)
    ↓
Results merged and analyzed
    ↓
Everything saved to JSON automatically
```

---

## 📊 Example Output

**File**: `research_results/openai_20260612_151509.json` (673 KB)

```json
{
  "startup_name": "OpenAI",
  "research_data": {
    "founders": [
      {"name": "Sam Altman", "credibility_score": 85, ...},
      {"name": "Greg Brockman", "credibility_score": 80, ...}
    ],
    "enriched_sources": {
      "https://en.wikipedia.org/wiki/OpenAI": {
        "status": "success",
        "markdown": "Full page content (306 KB)..."
      },
      "https://en.wikipedia.org/wiki/Sam_Altman": {
        "status": "success", 
        "markdown": "Full biography (160 KB)..."
      }
    }
  }
}
```

---

## 🚀 Usage

### Run Research (Enrichment is Automatic)
```python
from backend.agents.research.workflow import ResearchWorkflow
from backend.contracts.startup import StartupInput

startup = StartupInput(startup_name="OpenAI")
workflow = ResearchWorkflow()
result = workflow.run_research(startup)

# Firecrawl enrichment happened automatically!
print(f"Enriched {len(result.enriched_sources)} sources")
```

### Access Enriched Content
```python
# From the result object
for url, data in result.enriched_sources.items():
    if data["status"] == "success":
        content = data["markdown"]  # Full page content

# Or read from JSON file
import json
with open("research_results/openai_20260612_151509.json") as f:
    data = json.load(f)
    enriched = data["research_data"]["enriched_sources"]
```

---

## 📈 Real Data

From OpenAI research run:

| Metric | Value |
|--------|-------|
| File Size | 673 KB |
| Enriched URLs | 15 |
| Successful | 12 |
| Failed | 3 |
| Largest | Wikipedia OpenAI (306 KB) |

---

## ⚙️ Configuration

### Increase Enrichment URLs (More Content)
```python
# In _research_founders(), change:
enriched = self.enricher.enrich_sources(urls, max_urls=5)  # from 3 to 5
```

### Disable Enrichment (Tavily Only)
```python
# In _research_founders(), change:
enriched = {}  # Skip enrichment
```

---

## 🛡️ Handles Failures Gracefully

```
Unsupported site (Reddit, Facebook, etc.)
  → Uses Tavily snippet instead
  → Research continues normally
  → Failure logged in JSON

Firecrawl API down
  → Research runs with Tavily only
  → No enriched_sources in output
  → No data loss
```

---

## 📁 Files Modified

| File | Change |
|------|--------|
| `backend/contracts/research.py` | Added `enriched_sources` field |
| `backend/agents/research/workflow.py` | All 5 agents call enricher |
| `backend/services/enrichment/enricher.py` | NEW - Coordinates Firecrawl |
| `backend/services/enrichment/__init__.py` | NEW - Module export |

---

## ✨ Key Points

✅ **Automatic** - Happens without code changes  
✅ **Smart** - Caches results, avoids duplicate scrapes  
✅ **Selective** - Only top 3 URLs per agent (controls costs)  
✅ **Resilient** - Continues if Firecrawl fails  
✅ **Tracked** - All enriched content in JSON  
✅ **Backward Compatible** - Existing code still works  

---

## 🎉 Result

**File size increased 82x**: From 8 KB (Tavily only) to 673 KB (with enrichment)

More data = Better insights for Person 3

---

**Phase 3 Complete: Firecrawl + Tavily Integration**
