# Frontend Project Structure

## 📁 Organized Directory Layout

```
frontend/
├── public/                          # Static assets
│   ├── index.html
│   ├── favicon.ico
│   └── ...
│
├── src/
│   ├── pages/                       # Full-screen pages/views
│   │   ├── LandingPage.tsx         # Home page
│   │   ├── UploadStartup.tsx       # Startup submission
│   │   ├── AnalysisProgress.tsx    # Real-time progress
│   │   ├── CommitteeDebate.tsx     # Agent debate
│   │   ├── FinalReport.tsx         # Investment report
│   │   ├── DigitalTwin.tsx         # Scenario modeling
│   │   ├── StartupComparison.tsx   # Multi-startup comparison
│   │   └── index.ts                # Page exports
│   │
│   ├── components/                 # Reusable UI components
│   │   ├── NavigationBar.tsx       # Top navigation
│   │   ├── ScoreCard.tsx           # Score display component
│   │   ├── ProgressBar.tsx         # Progress visualization
│   │   └── index.ts                # Component exports
│   │
│   ├── hooks/                      # Custom React hooks
│   │   ├── useNavigation.ts        # Navigation management
│   │   ├── useAnalysis.ts          # Analysis state management
│   │   └── index.ts                # Hook exports
│   │
│   ├── services/                   # API & data services
│   │   ├── mockData.ts             # Mock startup data
│   │   └── index.ts                # Service exports
│   │
│   ├── types/                      # TypeScript definitions
│   │   └── index.ts                # All type definitions
│   │
│   ├── utils/                      # Utility functions
│   │   ├── formatters.ts           # Format numbers, dates, etc
│   │   ├── validators.ts           # Form & data validation
│   │   └── index.ts                # Utility exports
│   │
│   ├── App.tsx                     # Main app component & routing
│   ├── App.css                     # Global app styles
│   ├── index.tsx                   # React entry point
│   ├── index.css                   # Tailwind directives
│   └── ...
│
├── package.json                    # Dependencies & scripts
├── tsconfig.json                   # TypeScript config
├── tailwind.config.js              # Tailwind CSS config
├── postcss.config.js               # PostCSS config
└── README.md                       # Project documentation
```

---

## 📋 Directory Purposes

### `pages/` - Full-Screen Views
Contains complete page/screen components. Each page represents a full route in the application.

**Files:**
- `LandingPage.tsx` - Homepage with features & CTA
- `UploadStartup.tsx` - Form to submit startup for analysis
- `AnalysisProgress.tsx` - Real-time progress visualization
- `CommitteeDebate.tsx` - Bull/Bear/Red Team perspectives
- `FinalReport.tsx` - Investment recommendation & scores
- `DigitalTwin.tsx` - Interactive scenario modeling
- `StartupComparison.tsx` - Compare multiple analyses
- `index.ts` - Exports all pages for cleaner imports

**Usage in App.tsx:**
```typescript
import { LandingPage, UploadStartup, ... } from './pages';
```

---

### `components/` - Reusable UI Components
Small, reusable components that are used across multiple pages.

**Files:**
- `NavigationBar.tsx` - Top navigation with home/back buttons
- `ScoreCard.tsx` - Display a score with progress bar
- `ProgressBar.tsx` - Generic progress bar component
- `index.ts` - Component exports

**Usage Example:**
```typescript
import { ScoreCard, ProgressBar } from './components';

<ScoreCard label="Founder Score" score={9.2} theme="blue" />
<ProgressBar value={75} label="Progress" />
```

---

### `hooks/` - Custom React Hooks
Custom hooks for state management and side effects.

**Files:**
- `useNavigation.ts` - Navigation state management
  - Manages screen state and analysis ID
  - Provides `navigate(screen, analysisId?)` function
  
- `useAnalysis.ts` - Analysis data management
  - Manages analyses collection
  - Provides `submitAnalysis()` and `getAnalysis()`

**Usage Example:**
```typescript
const { navigate } = useNavigation(setCurrentScreen, setAnalysisId);
const { analyses, submitAnalysis } = useAnalysis();
```

---

### `services/` - Data & API Services
External service integrations and data sources.

**Files:**
- `mockData.ts` - Mock startup analysis data
  - `mockStartupAnalysis` - Airbnb example
  - `mockPreviousStartups` - Uber example
  - `mockAnalysisStatuses` - Simulated progress
  
- `index.ts` - Service exports

**Future Addition:** Real API calls will go here.

---

### `types/` - TypeScript Definitions
All TypeScript interfaces and types for the application.

**Files:**
- `index.ts` - All type definitions
  - `Founder` - Founder information
  - `Competitor` - Competitor data
  - `ResearchOutput` - Research layer output
  - `RagOutput` - RAG pipeline output
  - `CommitteeDecision` - Agent debate decision
  - `FinalReport` - Investment recommendation
  - `AnalysisStatus` - Analysis progress
  - `StartupAnalysis` - Complete analysis record

**Usage Example:**
```typescript
import { StartupAnalysis, CommitteeDecision } from './types';

const analysis: StartupAnalysis = { ... };
```

---

### `utils/` - Utility Functions
Pure functions for formatting, validation, and helper logic.

**Files:**
- `formatters.ts` - Format data for display
  - `formatCurrency()` - Format numbers as currency
  - `formatPercentage()` - Format as percentage
  - `formatScore()` - Format 0-10 scores
  - `formatDate()` - Format date strings
  - `getScoreColorClass()` - Get color for score
  - `getScoreBgClass()` - Get background for score

- `validators.ts` - Validate user input & data
  - `isValidUrl()` - Validate URLs
  - `isValidEmail()` - Validate emails
  - `isValidScore()` - Validate 0-10 scores
  - `isValidPercentage()` - Validate 0-1 values
  - `isValidFileSize()` - Check file size limits
  - `isValidFileType()` - Check supported file types

**Usage Example:**
```typescript
import { formatCurrency, isValidUrl } from './utils';

const price = formatCurrency(1000); // "$1,000.00"
if (isValidUrl(input)) { ... }
```

---

## 🔄 Data Flow

```
App.tsx (Main Component)
    ├── State Management
    │   ├── currentScreen (useState)
    │   ├── currentAnalysisId (useState)
    │   └── analyses (useAnalysis hook)
    │
    ├── Navigation
    │   └── handleNavigate(screen, id)
    │
    └── Conditional Rendering
        ├── Landing Page
        ├── Upload Startup
        ├── Analysis Progress
        ├── Committee Debate
        ├── Final Report
        ├── Digital Twin
        └── Startup Comparison

Pages (Full-Screen Components)
    ├── Receive props from App
    ├── Use components (ScoreCard, ProgressBar, etc)
    ├── Call navigation callbacks
    └── Display data from services

Components (Reusable)
    ├── Accept data as props
    ├── Handle styling & layout
    └── Call parent callbacks

Utils (Pure Functions)
    └── Format & validate data
```

---

## 📦 Import Patterns

### Importing Pages
```typescript
import {
  LandingPage,
  UploadStartup,
  AnalysisProgress,
} from './pages';
```

### Importing Components
```typescript
import { ScoreCard, ProgressBar, NavigationBar } from './components';
```

### Importing Hooks
```typescript
import { useNavigation, useAnalysis } from './hooks';
```

### Importing Types
```typescript
import { StartupAnalysis, CommitteeDecision } from './types';
```

### Importing Services
```typescript
import { mockStartupAnalysis, mockPreviousStartups } from './services';
```

### Importing Utils
```typescript
import { formatCurrency, isValidUrl } from './utils';
```

---

## 🔐 Best Practices

### ✅ Do's
- Keep components in `components/` small and reusable
- Use TypeScript types from `types/`
- Put formatting logic in `utils/formatters.ts`
- Put validation logic in `utils/validators.ts`
- Use hooks for complex state management
- Import from barrel files (`index.ts`)

### ❌ Don'ts
- Don't put page logic in components
- Don't mix UI and business logic
- Don't create types in multiple places
- Don't import directly from folders (use `index.ts`)
- Don't put API calls in components (use hooks/services)

---

## 🎯 Adding New Features

### Add a New Page
1. Create `src/pages/NewPage.tsx`
2. Add export to `src/pages/index.ts`
3. Import in `App.tsx`
4. Add routing logic

### Add a New Component
1. Create `src/components/NewComponent.tsx`
2. Add export to `src/components/index.ts`
3. Import in pages as needed

### Add a New Hook
1. Create `src/hooks/useNewHook.ts`
2. Add export to `src/hooks/index.ts`
3. Use in components/pages

### Add a New Utility
1. Create `src/utils/newUtility.ts` (or add to existing file)
2. Add export to `src/utils/index.ts`
3. Import in components as needed

---

## 🔄 Migration Guide (from Old Structure)

### Old Structure → New Structure

| Old Path | New Path |
|----------|----------|
| `src/screens/LandingPage.tsx` | `src/pages/LandingPage.tsx` |
| `src/types.ts` | `src/types/index.ts` |
| `src/mockData.ts` | `src/services/mockData.ts` |
| N/A | `src/components/` |
| N/A | `src/hooks/` |
| N/A | `src/utils/` |

### Import Changes

**Old:**
```typescript
import { StartupAnalysis } from './types';
import LandingPage from './screens/LandingPage';
```

**New:**
```typescript
import { StartupAnalysis } from './types';
import { LandingPage } from './pages';
```

---

## 📊 Structure Benefits

✅ **Scalability** - Easy to add new pages, components, and features
✅ **Maintainability** - Clear separation of concerns
✅ **Reusability** - Components used across multiple pages
✅ **Testability** - Easy to unit test isolated utilities & hooks
✅ **Performance** - Code-splitting by page directory
✅ **Developer Experience** - Intuitive organization
✅ **Professional** - Follows industry best practices

---

## 🚀 Future Expansion

This structure supports:
- ✅ Adding new pages easily
- ✅ Creating shared components
- ✅ Building custom hooks
- ✅ Adding API integration layer
- ✅ Adding state management (Redux, Zustand, etc)
- ✅ Adding tests directory
- ✅ Adding config directory

---

**Version**: 1.0.0
**Last Updated**: 2026-06-12
