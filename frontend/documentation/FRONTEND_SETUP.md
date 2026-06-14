# Frontend Integration Guide

## Overview

The frontend is a React TypeScript application that displays Person 2's research intelligence through a web UI.

**Architecture:**
```
Frontend (Person 1)
    ↓ (REST API calls)
Backend API (FastAPI)
    ↓ (orchestrates)
Research Workflow (Person 2)
    ├─ Tavily Search
    ├─ Firecrawl Enrichment
    └─ Data Extraction
    ↓
ResearchOutput Contract
    ↓
Frontend displays results
```

---

## Setup Instructions

### 1. Backend API Setup

Start the FastAPI server:

```bash
cd "c:\Users\j.sebastian\Documents\Tavily Search"
pip install fastapi uvicorn pydantic
python -m uvicorn backend.api.main:app --reload --host 0.0.0.0 --port 8000
```

Server runs on: `http://localhost:8000`

**Test the API:**
```bash
curl http://localhost:8000/health
curl http://localhost:8000/status
```

### 2. Frontend Setup

Install dependencies:

```bash
cd frontend
npm install
# or
yarn install
```

Create `.env.local` file:

```
REACT_APP_API_URL=http://localhost:8000
```

Start the development server:

```bash
npm start
# or
yarn start
```

Frontend runs on: `http://localhost:3000`

---

## Project Structure

```
frontend/
├── src/
│   ├── components/
│   │   ├── ResearchForm.tsx      # Input form for startup name
│   │   └── ResearchResults.tsx   # Display research findings
│   ├── hooks/
│   │   └── useResearch.ts        # React hook for research state
│   ├── services/
│   │   └── researchApi.ts        # API client for backend
│   ├── App.tsx                   # Main app component
│   ├── App.css                   # Styling
│   └── index.tsx                 # Entry point
├── public/
│   └── index.html
├── package.json
└── tsconfig.json
```

---

## API Endpoints

### Health Check
```
GET /health
Response: {"status": "healthy", "timestamp": "...", "services": {...}}
```

### Service Status
```
GET /status
Response: {"status": "running", "service": "...", "features": [...]}
```

### Run Research
```
POST /research
Content-Type: application/json

Request:
{
  "startup_name": "OpenAI",
  "research_type": "comprehensive"
}

Response:
{
  "startup_name": "OpenAI",
  "founders": [...],
  "competitors": [...],
  "market_summary": "...",
  "funding_summary": "...",
  "industry_summary": "...",
  "total_sources": 33,
  "enriched_sources": [...],
  "timestamp": "2026-06-12T15:15:09..."
}
```

### Quick Research (GET variant)
```
GET /research/OpenAI
Response: (same as POST /research)
```

---

## Frontend Features

### 1. Research Form
- Input startup name
- Submit for comprehensive research
- Loading indicator during processing
- Error handling

### 2. Results Display
- **Founders**: Cards with background, experience, credibility score
- **Competitors**: Table with positioning, funding, differentiators
- **Market Analysis**: Full market assessment
- **Funding History**: Funding rounds and investor info
- **Industry Intelligence**: Market trends and regulatory context
- **Sources**: Total and enriched source count

### 3. Status Indicator
- Shows backend connection status
- Updates on component mount

---

## Data Flow

### User Interaction
```
User enters startup name
    ↓
Click "Start Research"
    ↓
ResearchForm.onSubmit()
    ↓
useResearch.runResearch()
    ↓
researchApi.runResearch()
    ↓
POST /research (backend)
```

### Backend Processing
```
POST /research
    ↓
FastAPI endpoint
    ↓
ResearchWorkflow.run_research()
    ├─ _research_founders()
    ├─ _research_competitors()
    ├─ _research_market()
    ├─ _research_funding()
    └─ _research_industry()
    ↓
ResearchOutput
    ↓
ResearchResponse (JSON)
```

### Frontend Display
```
researchApi.runResearch() → Promise<ResearchResponse>
    ↓
useResearch state update
    ↓
ResearchResults component renders
    ├─ Founders grid
    ├─ Competitors table
    ├─ Analysis summaries
    └─ Source info
```

---

## Environment Variables

### Frontend (.env.local)
```
REACT_APP_API_URL=http://localhost:8000  # Backend API URL
```

### Backend (.env)
```
TAVILY_API_KEY=...           # Tavily search API key
FIRECRAWL_API_KEY=...        # Firecrawl API key
```

---

## Development Workflow

### 1. Make API changes
- Edit `backend/api/main.py`
- Server reloads automatically (--reload)

### 2. Make frontend changes
- Edit components in `frontend/src/`
- Frontend reloads automatically

### 3. Test integration
- Open browser to `http://localhost:3000`
- Enter startup name
- See research results

### 4. Debug
- Browser DevTools (F12) for frontend
- Terminal for API logs
- Check Network tab for API calls

---

## Testing

### Test Backend API Directly
```bash
# Test health
curl http://localhost:8000/health

# Test research
curl -X POST http://localhost:8000/research \
  -H "Content-Type: application/json" \
  -d '{"startup_name": "OpenAI"}'
```

### Test Frontend in Browser
1. Open `http://localhost:3000`
2. Enter startup name (e.g., "Stripe")
3. Click "Start Research"
4. Wait for results
5. Verify data displays correctly

---

## Troubleshooting

### Backend not responding
- Check: `http://localhost:8000/health`
- Verify FastAPI is running: `python -m uvicorn backend.api.main:app --reload`
- Check port 8000 is available

### Frontend can't reach backend
- Check REACT_APP_API_URL in .env.local
- Check CORS configuration in backend/api/main.py
- Open DevTools → Network tab to see requests

### Missing dependencies
- Backend: `pip install fastapi uvicorn pydantic`
- Frontend: `npm install`

### API returns 500 error
- Check backend terminal for error messages
- Verify Tavily and Firecrawl API keys in .env
- Check research workflow logs

---

## Next Steps

### For Person 1 (Frontend)
- [ ] Add dark mode toggle
- [ ] Implement export to PDF
- [ ] Add charts for market analysis
- [ ] Implement real-time progress streaming

### For Person 2 (Research)
- [ ] Add more research agents
- [ ] Implement caching for repeated searches
- [ ] Add historical comparison
- [ ] Implement async research processing

### For Person 3 (Knowledge/RAG)
- [ ] Implement RAG pipeline integration
- [ ] Add vector store connection
- [ ] Implement semantic search on research results

### For Person 4 (Investment Committee)
- [ ] Connect bull/bear agents
- [ ] Implement debate visualization
- [ ] Add red team review interface

### For Person 5 (Orchestration)
- [ ] Implement full workflow orchestration
- [ ] Add PostgreSQL for results persistence
- [ ] Implement user authentication

---

## Performance Optimization

### Research Processing
- Current: ~13 seconds per research run
- Optimization: Implement async processing and WebSocket for real-time updates

### Frontend
- Implement code splitting for faster initial load
- Add caching for research results
- Implement pagination for large result sets

### Backend
- Implement request caching
- Add rate limiting
- Implement async Firecrawl batch processing

---

## Deployment

### Backend (FastAPI)
```bash
# Production server
gunicorn --workers 4 -k uvicorn.workers.UvicornWorker backend.api.main:app
```

### Frontend (React)
```bash
# Build
npm run build

# Serve with static server
npm install -g serve
serve -s build -l 3000
```

---

**Integration Complete!** Frontend is connected to Person 2's research backend. 🚀
