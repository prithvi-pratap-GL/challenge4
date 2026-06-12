# VentureMind AI - Frontend

A comprehensive React + TypeScript frontend for AI-powered venture capital analysis. Built with Tailwind CSS and featuring 7 interactive screens.

## 🚀 Features

### Screens Implemented

1. **Landing Page** - Hero section with feature highlights and CTA
2. **Upload Startup** - Website URL and pitch deck submission form
3. **Analysis Progress** - Real-time progress visualization with stage timeline
4. **Committee Debate** - Bull agent, Bear agent, and Red team perspectives
5. **Final Report** - Comprehensive investment recommendation with scoring
6. **Digital Twin** - Interactive what-if scenario analysis with financial projections
7. **Startup Comparison** - Side-by-side comparison of multiple analyses

## 📋 Tech Stack

- **Framework**: React 19 + TypeScript
- **Styling**: Tailwind CSS v3
- **Icons**: Lucide React
- **UI Pattern**: Screen-based routing with mock data

## 🎯 Key Components

### Types (`src/types.ts`)
```typescript
- Founder
- Competitor
- ResearchOutput
- RagOutput
- CommitteeDecision
- FinalReport
- AnalysisStatus
- StartupAnalysis
```

### Mock Data (`src/mockData.ts`)
- Complete Airbnb analysis example
- Uber competitor analysis
- Mock analysis statuses

### Screens
- All screens are self-contained components
- Mock data flows through the app via state management
- Navigation between screens via handleNavigate callback

## 🔧 Running the App

```bash
# Install dependencies
npm install

# Start development server
PORT=3001 npm start

# Build for production
npm run build

# Run tests
npm test
```

The app runs on `http://localhost:3001` with hot reload enabled.

## 📁 File Structure

```
frontend/
├── public/
├── src/
│   ├── screens/
│   │   ├── LandingPage.tsx
│   │   ├── UploadStartup.tsx
│   │   ├── AnalysisProgress.tsx
│   │   ├── CommitteeDebate.tsx
│   │   ├── FinalReport.tsx
│   │   ├── DigitalTwin.tsx
│   │   └── StartupComparison.tsx
│   ├── App.tsx
│   ├── App.css
│   ├── index.css
│   ├── types.ts
│   ├── mockData.ts
│   └── index.tsx
├── package.json
├── tsconfig.json
├── tailwind.config.js
└── postcss.config.js
```

## 🎨 Design System

### Colors
- **Primary**: Purple (#6B46C1) & Pink (#EC4899)
- **Success**: Green (#10B981)
- **Warning**: Orange (#F59E0B)
- **Error**: Red (#EF4444)
- **Background**: Dark slate (#0F172A)

### Components
- Gradient buttons
- Card layouts with borders
- Progress bars
- Modal-like dialogs
- Table layouts

## 📊 Data Flow

1. **Landing Page** → User clicks "Start Analysis"
2. **Upload Startup** → User submits URL/pitch deck
3. **Analysis Progress** → Simulated progress animation
4. **Committee Debate** → Display bull/bear/red team cases
5. **Final Report** → Show scores and recommendation
6. **Digital Twin** → Run scenario simulations
7. **Startup Comparison** → Compare with previous analyses

## 🔄 State Management

Currently using React hooks with local state. The `App.tsx` maintains:
- `currentScreen`: Which screen to display
- `currentAnalysisId`: Active analysis
- `analyses`: Dictionary of all analyses

## 🚧 Integration Points

When connecting to the backend, the following APIs will be needed:

- `GET /analysis/{id}` - Get analysis status
- `GET /report/{id}` - Get final report
- `GET /committee/{id}` - Get committee decision
- `POST /analysis` - Submit new analysis

Currently uses mock data from `mockData.ts`.

## ✅ Features Showcase

### Landing Page
- Hero section with gradient text
- Feature cards explaining capabilities
- Statistics dashboard
- Clear CTA

### Upload Startup
- Form validation
- File drag-and-drop
- URL input with placeholder
- Error handling

### Analysis Progress
- Animated progress bar
- Stage-by-stage timeline
- Real-time status updates
- Bouncing animation indicators

### Committee Debate
- Tabbed interface for different perspectives
- Color-coded sentiment (bull = green, bear = red, red team = orange)
- Confidence score visualization

### Final Report
- Comprehensive scoring dashboard
- Three main metrics (Founder, Market, Risk)
- Detailed analysis text
- Download & share buttons

### Digital Twin
- Interactive parameter sliders
- Three preset scenarios (Optimistic, Realistic, Pessimistic)
- 5-year financial projections
- Success probability calculation

### Startup Comparison
- Multi-select startup comparison
- Score comparison table
- Summary statistics
- Team and competitor information

## 🎓 Learning Resources

The codebase demonstrates:
- Component composition with TypeScript
- Tailwind CSS utility-first styling
- React hooks (useState, useEffect)
- Screen-based navigation patterns
- Mock data integration
- Interactive form handling
- Data visualization patterns

## 📝 Notes

- All styling uses Tailwind CSS classes
- No additional CSS files except base index.css
- Icons from Lucide React library
- Responsive design with mobile-first approach
- Dark theme with purple/pink accents
