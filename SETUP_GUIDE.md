# Person 2: Setup Guide for Research Intelligence Module

## 🚀 Quick Setup (5 minutes)

### Step 1: Install Dependencies

```bash
pip install -r requirements.txt
```

This installs:
- ✅ `tavily-python` - Tavily Search API
- ✅ `firecrawl-py` - Website scraping
- ✅ `python-dotenv` - Environment variables
- ✅ `pytest` - Testing framework (optional)

---

### Step 2: Get API Keys

#### **Tavily API Key** (Required)
1. Go to https://tavily.com/
2. Sign up for free account
3. Copy your API key from dashboard
4. Add to `.env` file

#### **Firecrawl API Key** (Optional, for Phase 3)
1. Go to https://firecrawl.dev/
2. Sign up for account
3. Get API key
4. Add to `.env` file (optional for now)

---

### Step 3: Create Environment File

Create `.env` file in project root:

```env
# Required for Phase 2
TAVILY_API_KEY=tvly_xxxxxxxxxxxxxxxxxxxxx

# Optional for Phase 3
FIRECRAWL_API_KEY=fc_xxxxxxxxxxxxxxxxxxxxx
CRUNCHBASE_API_KEY=your_key_here
LINKEDIN_API_KEY=your_key_here
```

**⚠️ Important**: Never commit `.env` to git!

```bash
echo ".env" >> .gitignore
```

---

## 📦 Complete Installation Steps

### Option A: One Command (Recommended)

```bash
# Navigate to project
cd "c:\Users\j.sebastian\Documents\Tavily Search"

# Install all dependencies
pip install -r requirements.txt

# Create .env file
echo TAVILY_API_KEY=your_key_here > .env

# Verify installation
python -c "from tavily import TavilyClient; print('[OK] Tavily installed')"
```

### Option B: Manual Installation

```bash
# Install each package
pip install tavily-python>=0.3.0
pip install firecrawl-py>=0.0.59
pip install python-dotenv>=1.0.0
pip install pytest>=7.0.0

# Create .env
copy .env.example .env
# Edit .env and add your API key
```

---

## ✅ Verify Installation

### Test 1: Import Check
```bash
python -c "
from tavily import TavilyClient
from firecrawl import FirecrawlApp
from backend.agents.research.agent import run_research
print('[OK] All imports working')
"
```

### Test 2: API Key Check
```bash
python -c "
import os
from dotenv import load_dotenv
load_dotenv()
api_key = os.getenv('TAVILY_API_KEY')
print(f'[OK] API Key loaded: {bool(api_key)}')
"
```

### Test 3: Full Module Test
```bash
python -c "
from backend.contracts.startup import StartupInput
from backend.agents.research.agent import run_research

startup = StartupInput('Stripe', 'https://stripe.com')
research = run_research(startup)
print(f'[OK] Module working: {len(research.founders)} founders found')
"
```

---

## 🧪 Run Tests

### Run All Tests
```bash
python tests/test_research_real_api.py
```

### Run Specific Test
```bash
python -m pytest tests/test_research_real_api.py::test_research_with_real_api -v
```

### Run Demo
```bash
python backend/examples/demo_real_api.py
```

---

## 📋 Dependency Details

### Required Packages

| Package | Version | Purpose | Usage |
|---------|---------|---------|-------|
| `tavily-python` | >=0.3.0 | Web search API | `from tavily import TavilyClient` |
| `python-dotenv` | >=1.0.0 | Load .env files | `from dotenv import load_dotenv` |

### Optional Packages

| Package | Version | Purpose | When |
|---------|---------|---------|------|
| `firecrawl-py` | >=0.0.59 | Website scraping | Phase 3+ |
| `pytest` | >=7.0.0 | Testing framework | Running tests |

### Built-in (No Install)

These come with Python, no pip install needed:
- `dataclasses` - Contract definitions
- `typing` - Type hints
- `json` - JSON serialization
- `os` - Environment variables
- `time` - Performance timing
- `re` - Regex for data extraction

---

## 🔍 Troubleshooting

### Error: "No module named 'tavily'"
```bash
# Solution: Install tavily
pip install tavily-python
```

### Error: "TAVILY_API_KEY not found"
```bash
# Solution: Create .env file with your key
echo "TAVILY_API_KEY=your_key_here" > .env

# Verify
python -c "import os; from dotenv import load_dotenv; load_dotenv(); print(os.getenv('TAVILY_API_KEY'))"
```

### Error: "Connection timeout"
```bash
# This means API is unreachable
# 1. Check internet connection
# 2. Verify API key is valid
# 3. Check Tavily API status at https://tavily.com/status
```

### Error: "Import error in agent.py"
```bash
# Solution: Install in project root
cd "c:\Users\j.sebastian\Documents\Tavily Search"
pip install -r requirements.txt
```

---

## 💻 System Requirements

- **Python**: 3.8+
- **OS**: Windows, Mac, Linux
- **Internet**: Required for API calls
- **Disk**: ~500MB (for dependencies)

---

## 🚀 After Setup

1. ✅ Create `.env` file with API key
2. ✅ Run `pip install -r requirements.txt`
3. ✅ Run tests: `python tests/test_research_real_api.py`
4. ✅ Ready to use!

---

## 📚 Next Steps

- **Quick Start**: See `START_HERE.md`
- **API Details**: See `TAVILY_INPUT_OUTPUT_ANALYSIS.md`
- **Integration**: See `PHASE_2_REAL_API.md`
- **Commands**: See `QUICK_REFERENCE.md`

---

## 🆘 Need Help?

1. Check `QUICK_REFERENCE.md` for common commands
2. Run `python tests/test_research_real_api.py` for detailed error messages
3. See `PHASE_2_REAL_API.md` troubleshooting section
4. Check `.env` file has TAVILY_API_KEY set

---

**Status**: Ready to use after setup  
**Time to setup**: ~5 minutes  
**Verification**: Run test_research_real_api.py

