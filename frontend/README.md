# VentureMind — Diligence Terminal

A data-driven investor terminal for the VentureMind scoring API. Run a deal
through `POST /api/v1/scoring/evaluate` and get back a fully evidence-linked
breakdown: verdict, composite health, five scoring dimensions, and every
factor's findings traced to their source chunk IDs.

## Stack

- React 19 + Vite
- Recharts (radar chart)
- lucide-react (icons)
- No CSS framework — hand-built design system in `src/index.css` and
  per-component stylesheets

## Getting started

```bash
npm install
cp .env.example .env   # optional — see below
npm run dev
```

## Connecting to the backend

By default (`VITE_API_BASE_URL` unset), the dashboard runs entirely on three
bundled sample deals (`orbital-fleet-systems`, `vela-health-analytics`,
`northstar-fleet-fuel`) — useful for design review or demos without a live
backend.

To connect to a real VentureMind backend, set:

```
VITE_API_BASE_URL=http://localhost:8000
```

The dashboard calls `POST {VITE_API_BASE_URL}/api/v1/scoring/evaluate` with
`{ "deal_id": "<id>" }` and expects the `InvestmentRecommendation` shape
defined in `backend/domain/schemas.py`:

```jsonc
{
  "deal_id": "string",
  "status": "invest" | "watchlist" | "pass",
  "reasoning": "string",
  "category_scores": [
    {
      "category": "team" | "market" | "product" | "financial" | "risk",
      "aggregate_score": 0-100,
      "factors": [
        {
          "factor_name": "string",
          "score": 0-100,
          "findings": [
            { "finding_text": "string", "supporting_chunk_ids": ["string"] }
          ]
        }
      ]
    }
  ]
}
```

If a live request to a non-sample deal fails (network error, 404, 500), the
UI surfaces a clear error message rather than failing silently. If a live
request fails for one of the three *sample* deal IDs, the dashboard falls
back to the bundled mock so the demo always works.

## Project structure

```
src/
  api/scoring.js          fetch wrapper + mock fallback
  data/mockDeals.js        bundled sample InvestmentRecommendation payloads
  hooks/useRecentDeals.js   localStorage-backed evaluation history
  utils/scoring.js          tier thresholds, category metadata, formatting
  components/
    Sidebar                 recent evaluations rail
    CommandBar              deal ID input + sample chips
    VerdictHero             INVEST/WATCHLIST/PASS + reasoning + score strip
    RadarOverview           5-axis radar (risk plotted inverted)
    EvidenceLedger          category tabs → factors → findings → chunk IDs
    States                  empty state + loading skeleton
```

## Design notes

- **Risk is inverted everywhere it's displayed.** A risk score of 32/100
  is shown as "Low" risk (good), and on the radar chart it plots as 68
  ("outward = favorable" across all five axes).
- **Composite Health** is the simple average of the four core categories
  plus `(100 - risk)`, giving a single 0–100 number that always points the
  same direction as the individual tiers.
- **Evidence Ledger** is the load-bearing UI element: every factor expands
  to show its findings, and every finding lists the `supporting_chunk_ids`
  it was extracted from. This is what makes the scores auditable rather
  than opaque.
