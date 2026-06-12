# JSON Storage Guide - Phase 3 Enhancement

## 🎯 **What is JSON Storage?**

JSON Storage automatically saves all research results to JSON files for:
- ✅ Persistence (don't lose research data)
- ✅ Caching (retrieve previous research without re-running)
- ✅ Audit trail (historical research records)
- ✅ Easy sharing (JSON format works everywhere)

---

## 📂 **File Structure**

```
research_results/
├── stripe_20260612_143022.json      # First research for Stripe
├── stripe_20260612_145530.json      # Second research for Stripe
├── paypal_20260612_150000.json      # Research for PayPal
└── square_20260612_151500.json      # Research for Square
```

Each file contains:
- Startup name
- Timestamp of research
- All founders, competitors, market analysis, funding, industry data
- 30-40 sources used in research

---

## 💾 **How It Works**

### **Automatic Saving**

```python
# In workflow.py - run_research()
output = ResearchOutput(...)  # Create research
self.storage.save_research(startup_name, output)  # Auto-saved to JSON
```

**Example JSON output:**

```json
{
  "startup_name": "Stripe",
  "timestamp": "2026-06-12T14:30:22.123456",
  "research_data": {
    "founders": [
      {
        "name": "Patrick Collison",
        "background": "Ivy League / Top University graduate",
        "experience": "Founder and startup experience",
        "credibility_score": 85,
        "sources": ["https://..."]
      }
    ],
    "competitors": [
      {
        "name": "Square",
        "market_position": "Market leader with significant share",
        "funding": "Public company",
        "key_differentiators": "Unique value proposition and market approach",
        "sources": ["https://..."]
      }
    ],
    "market_summary": "Market Analysis for Stripe: ...",
    "funding_summary": "Funding History for Stripe: ...",
    "industry_summary": "Industry Analysis for Stripe: ...",
    "sources": ["https://...", "https://...", ...]
  }
}
```

---

## 🔍 **Using JSON Storage**

### **Load Latest Research**

```python
from backend.services.storage.json_storage import JSONStorageService

storage = JSONStorageService()

# Get the most recent research for Stripe
latest = storage.get_latest_research("Stripe")
if latest:
    print(latest["research_data"]["founders"])
```

### **Load Specific File**

```python
# Load a specific research file
data = storage.load_research("research_results/stripe_20260612_143022.json")
print(data["research_data"]["competitors"])
```

### **List All Research**

```python
# List all stored research files
all_files = storage.list_all_research()
for file in all_files:
    print(file)  # Prints file paths
```

---

## 📊 **Data Access from JSON**

### **From Person 3's Perspective**

```python
import json

# Read stored research directly
with open("research_results/stripe_20260612_143022.json") as f:
    data = json.load(f)

# Access research data
startup_name = data["startup_name"]
founders = data["research_data"]["founders"]
competitors = data["research_data"]["competitors"]
sources = data["research_data"]["sources"]

print(f"Found {len(founders)} founders for {startup_name}")
print(f"Used {len(sources)} sources")
```

---

## 🔄 **Phase 3 Enhancement: Caching**

JSON storage enables intelligent caching:

```python
# Future enhancement (Phase 3)
def run_research_with_cache(startup_name):
    # Check if we already researched this startup today
    latest = storage.get_latest_research(startup_name)
    
    if latest and is_recent(latest["timestamp"]):
        print(f"Using cached research from {latest['timestamp']}")
        return latest["research_data"]
    else:
        print("Running fresh research...")
        return run_research(startup_name)
```

**Benefits:**
- Reduce API calls by 80%+ when researching same startup multiple times
- Speed up research: cached results return instantly
- Cost savings: fewer Tavily searches

---

## 📈 **Monitoring & Metrics**

### **Check Storage Size**

```bash
# List all research files with sizes
ls -lah research_results/

# Total files
find research_results -name "*.json" | wc -l
```

### **Sample Data Extraction**

```python
import json

# Count all research records
import os
count = len([f for f in os.listdir("research_results") if f.endswith(".json")])
print(f"Total research records: {count}")
```

---

## 🔧 **Storage Configuration**

### **Change Storage Directory**

```python
# Default: research_results/
storage = JSONStorageService(storage_dir="custom_path/results")

# Now saves to: custom_path/results/stripe_20260612_143022.json
```

### **Custom Storage Location**

```python
# In workflow.py
def __init__(self):
    self.storage = JSONStorageService(storage_dir="/data/research_archive")
```

---

## 📝 **File Naming Convention**

```
{startup_name}_{YYYYMMDD}_{HHMMSS}.json

Examples:
- stripe_20260612_143022.json
- paypal_20260612_143022.json
- square_20260612_143022.json
```

**Naming Rules:**
- Startup name in lowercase
- Spaces replaced with underscores
- ISO 8601 timestamp (sortable by date/time)
- Always ends with .json

---

## ✅ **Features Included**

| Feature | Status | Details |
|---------|--------|---------|
| **Auto-save** | ✅ Active | Saves after every research run |
| **Load latest** | ✅ Active | Get most recent research for startup |
| **Load by file** | ✅ Active | Load specific research file |
| **List all** | ✅ Active | See all stored research |
| **Caching** | ⏸️ Phase 3 | Planned for optimization |
| **Incremental** | ⏸️ Phase 3 | Planned for large datasets |

---

## 🚀 **Usage in Production**

### **Step 1: Run Research (Auto-saves)**

```python
from backend.agents.research.workflow import ResearchWorkflow
from backend.contracts.startup import StartupInput

workflow = ResearchWorkflow()
startup_input = StartupInput(startup_name="Stripe")
result = workflow.run_research(startup_input)

# JSON automatically saved to research_results/stripe_YYYYMMDD_HHMMSS.json
```

### **Step 2: Person 3 Retrieves Data**

```python
from backend.services.storage.json_storage import JSONStorageService

storage = JSONStorageService()
latest_research = storage.get_latest_research("Stripe")
founders = latest_research["research_data"]["founders"]
competitors = latest_research["research_data"]["competitors"]
```

### **Step 3: Use in Downstream Analysis**

```python
# Person 3 or 4 can process the JSON data
for founder in founders:
    print(f"- {founder['name']} ({founder['credibility_score']}/100)")
    
for competitor in competitors:
    print(f"- {competitor['name']} ({competitor['market_position']})")
```

---

## 🎯 **When to Use Each Method**

| Use Case | Method | Example |
|----------|--------|---------|
| **Latest research** | `get_latest_research()` | "Show me the most recent analysis" |
| **Specific file** | `load_research()` | "Load this archived research" |
| **All records** | `list_all_research()` | "Show research history for this startup" |
| **Raw JSON** | `os.listdir()` + `json.load()` | "Custom analysis on stored data" |

---

## 🔐 **Data Privacy & Backup**

**Current Setup:**
- ✅ JSON stored locally (research_results/)
- ✅ Plain text format (human-readable)
- ✅ Timestamped (no overwrites)
- ⚠️ No encryption (add in Phase 3 if needed)

**Backup Recommendation:**
```bash
# Backup all research
cp -r research_results research_results_backup_$(date +%Y%m%d)

# Archive old research
tar -czf research_results_archive_2026.tar.gz research_results/
```

---

## 📊 **Integration with Phase 3**

**Planned enhancements:**
1. **Caching layer** - Check cache before searching
2. **Database export** - Bulk load JSON to PostgreSQL
3. **Versioning** - Track changes to research over time
4. **Deduplication** - Identify and merge duplicate research
5. **Analytics** - Trends in startup research patterns

---

## ✨ **Summary**

| Aspect | Details |
|--------|---------|
| **What** | Auto-save research to JSON files |
| **Where** | `research_results/` directory |
| **When** | After every research run |
| **Why** | Persistence, caching, audit trail |
| **How** | `JSONStorageService.save_research()` |
| **Status** | ✅ Phase 3 - Implemented |
| **Cost** | Free (no new dependencies) |

---

## 🔗 **Related Files**

- [backend/services/storage/json_storage.py](backend/services/storage/json_storage.py) - Storage service
- [backend/agents/research/workflow.py](backend/agents/research/workflow.py) - Integration point
- [backend/contracts/research.py](backend/contracts/research.py) - Data structure
