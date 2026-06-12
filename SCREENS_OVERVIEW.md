# VentureMind AI - Screens Overview

## Screen 1: Landing Page
**File**: `src/screens/LandingPage.tsx`

### Components
- Navigation bar with VentureMind AI logo
- Hero section with gradient heading
- Feature highlights (4 cards)
- Statistics dashboard (3 metrics)
- Primary CTA button → Upload screen

### Features
- Gradient text effects
- Feature cards with icons
- Statistics: 50M data points, 5 AI agents, 30min analysis
- Responsive grid layout
- Hover effects on buttons

### Navigation
- "Start Analysis" button → Upload Startup screen

---

## Screen 2: Upload Startup
**File**: `src/screens/UploadStartup.tsx`

### Components
- Navigation back to landing
- Form with 2 sections
- Website URL input field
- Pitch deck file upload area
- Submit button
- Quick start example

### Features
- URL validation (required field)
- File drag-and-drop support
- Accepted formats: PDF, PPTX, DOC, DOCX
- Visual file selection feedback
- Error message display
- Loading state on submit

### Data Collection
- website_url: String (required)
- pitch_deck: File (optional)

### Navigation
- Back button → Landing Page
- Submit → Analysis Progress screen

---

## Screen 3: Analysis Progress
**File**: `src/screens/AnalysisProgress.tsx`

### Components
- Startup analysis header with ID
- Overall progress percentage display
- Progress bar with animation
- 6-stage timeline with icons
- Status indicators (completed/current/upcoming)
- Loading animation

### Stages
1. 🔍 Research (0-17%)
2. 📚 RAG & Context (17-34%)
3. 🤝 Committee Debate (34-51%)
4. 🔴 Red Team Challenge (51-68%)
5. 📄 Final Report (68-85%)
6. ✓ Completed (85-100%)

### Features
- Real-time progress simulation (500ms intervals)
- Animated progress bar
- Stage completion indicators
- Current agent display
- Estimated time remaining
- Bouncing animation elements
- Auto-navigation on completion

### Navigation
- Auto-advances to Committee Debate on completion

---

## Screen 4: Committee Debate
**File**: `src/screens/CommitteeDebate.tsx`

### Components
- Tab navigation (4 tabs)
- Content panels for each perspective
- Color-coded styling per agent
- Confidence score display
- Navigation buttons

### Tabs
1. **🐂 Bull Agent** (Green)
   - Investment case for the startup
   - Positive arguments
   - Market opportunity highlights

2. **🐻 Bear Agent** (Red)
   - Risk case against investment
   - Challenges and concerns
   - Market challenges

3. **🔴 Red Team** (Orange)
   - Adversarial perspective
   - Blind spots and assumptions
   - Critical feedback

4. **⚖️ Verdict** (Accent)
   - Final recommendation
   - Confidence percentage
   - Decision summary
   - Sentiment indicator

### Features
- Tabbed interface
- Long-form text content
- Confidence score with color coding
- Verdict with recommendation
- Progress through content
- Scroll support for long content

### Navigation
- Back button → Analysis Progress
- Next button → Final Report

---

## Screen 5: Final Report
**File**: `src/screens/FinalReport.tsx`

### Components
- Header with startup name and ID
- Investment recommendation banner
- Three score cards (Founder, Market, Risk)
- Detailed analysis section
- Summary statistics
- Action buttons (Download, Share)

### Key Metrics
- **Founder Score**: 0-10 (leadership quality)
- **Market Score**: 0-10 (market opportunity)
- **Risk Score**: 0-10 (inverted as Safety)

### Features
- Color-coded scores (green/yellow/red)
- Progress bars for each metric
- Comprehensive markdown-formatted report
- Recommendation statement with sentiment
- Download PDF (placeholder)
- Share functionality (placeholder)
- Summary stats cards

### Content Sections
- Executive Summary
- Key Metrics
- Investment Thesis
- Risk Mitigation
- Recommendation with valuation

### Navigation
- Back button → Committee Debate
- Next button → Digital Twin

---

## Screen 6: Digital Twin
**File**: `src/screens/DigitalTwin.tsx`

### Components
- Scenario selector (3 options)
- Interactive parameter sliders
- Run simulation button
- Results display table
- Valuation and probability cards

### Scenario Options
1. **Optimistic**
   - High growth (50%)
   - Low churn (2%)
   - High market penetration (25%)

2. **Realistic**
   - Medium growth (35%)
   - Medium churn (5%)
   - Medium market penetration (15%)

3. **Pessimistic**
   - Low growth (15%)
   - High churn (12%)
   - Low market penetration (8%)

### Adjustable Parameters
- Annual Growth Rate (0-100%)
- Monthly Churn Rate (0-30%)
- Market Penetration (0-50%)
- Customer Acquisition Cost ($20-200)
- Lifetime Value ($100-1000)
- LTV:CAC Ratio (calculated)

### Simulation Results
- 5-year revenue projections
- User growth projections
- LTV:CAC ratio over time
- Burn rate estimates
- Final valuation (revenue × 10)
- Success probability (heuristic)

### Features
- Real-time slider updates
- Scenario presets with descriptions
- Interactive table with year-by-year breakdown
- Success probability calculation
- Unit economics validation

### Navigation
- Back button → Final Report
- Next button → Startup Comparison

---

## Screen 7: Startup Comparison
**File**: `src/screens/StartupComparison.tsx`

### Components
- Startup selection grid
- Comparison table
- Detailed metrics cards
- Summary statistics

### Selection
- Multi-select startup checkboxes
- Visual feedback for selected startups
- Current analysis included by default

### Comparison Metrics
- Founder Score
- Market Score
- Risk Score
- Committee Confidence
- Recommendation (Buy/Pass)

### Additional Sections
- Founder Teams (names and roles)
- Competitor Count per startup
- Summary statistics:
  - Highest Founder Score
  - Strongest Market
  - Lowest Risk

### Features
- Side-by-side comparison table
- Color-coded metrics
- Historical analysis access
- Quick summary cards
- Comprehensive metrics view

### Navigation
- Back button → Digital Twin
- Return to Home → Landing Page

---

## Navigation Flow

```
Landing Page
    ↓
Upload Startup
    ↓
Analysis Progress (auto-advance)
    ↓
Committee Debate
    ↓
Final Report
    ↓
Digital Twin
    ↓
Startup Comparison
    ↓
Landing Page (home)
```

---

## Shared Features Across Screens

### Navigation
- All screens (except landing) have a back button
- Home button in navigation bar (Landing Page)
- Forward navigation buttons

### Styling
- Dark theme with purple/pink accents
- Consistent card layouts
- Responsive grid system
- Hover states on interactive elements
- Gradient backgrounds and text

### Data Management
- Mock data from `mockData.ts`
- Type-safe with TypeScript interfaces
- State managed in App.tsx
- Props passed down to screens

### Accessibility
- Semantic HTML
- Button focus states
- Form labels
- Color contrast ratios
- Keyboard navigation support

---

## Data Contracts

### Input (Upload Screen)
```typescript
{
  website_url: string;
  pitch_deck?: File;
}
```

### Output (Final Report)
```typescript
{
  founder_score: number;      // 0-10
  market_score: number;       // 0-10
  risk_score: number;         // 0-10
  recommendation: string;     // "BUY" | "PASS" | "STRONG BUY"
  report: string;             // Markdown formatted
}
```

### Committee Decision
```typescript
{
  bull_case: string;
  bear_case: string;
  red_team_feedback: string;
  verdict: string;
  confidence: number;         // 0-1
}
```

---

## Interactive Elements

### Forms
- URL input with validation
- File upload with drag-drop
- Submit button with loading state

### Sliders
- Growth rate
- Churn rate
- Market penetration
- CAC and LTV

### Tabs
- Bull case
- Bear case
- Red team feedback
- Verdict

### Tables
- Comparison metrics
- Financial projections
- Historical analyses

### Buttons
- Primary (gradient)
- Secondary (outline)
- Danger (red)
- Navigation (with arrows)

---

## Key UI Patterns

1. **Card Layout**: Content in cards with borders and shadows
2. **Tabbed Interface**: Multiple perspectives in tabs
3. **Progress Visualization**: Progress bars and percentages
4. **Score Display**: Visual scoring with color gradients
5. **Form Elements**: Inputs with validation feedback
6. **Table Display**: Sortable/comparable data
7. **Navigation**: Clear forward/back flow
8. **Animations**: Progress bars, bouncing elements, transitions

---

## Responsive Design

All screens are responsive with:
- Mobile-first approach
- Breakpoints: sm (640px), md (768px), lg (1024px)
- Flexible grid layouts
- Scrollable content areas
- Touch-friendly buttons and inputs
- Readable typography on all sizes
