# VentureMind AI - Professional Design System

## Color Palette

### Core Colors
- **Primary Navy:** #0F172A
- **Accent Indigo:** #4F46E5
- **Success Emerald:** #10B981
- **Warning Amber:** #F59E0B
- **Error Red:** #EF4444
- **Background Light:** #F8FAFC
- **Card White:** #FFFFFF
- **Text Primary:** #0F172A
- **Text Secondary:** #64748B
- **Border Light:** #E2E8F0

## Typography

### Font Family
- **Primary:** Inter (400, 500, 600, 700, 800, 900)
- **Monospace:** JetBrains Mono

### Type Scale
- **H1:** 48px | 700 bold | -0.03em spacing
- **H2:** 36px | 700 bold | -0.01em spacing
- **H3:** 24px | 600 semibold | -0.01em spacing
- **H4:** 20px | 600 semibold
- **Body:** 16px | 400 regular | 1.5 line height
- **Small:** 14px | 400 regular
- **Caption:** 12px | 500 medium

## Spacing System

- **xs:** 4px
- **sm:** 8px
- **md:** 12px
- **lg:** 16px
- **xl:** 20px
- **2xl:** 24px
- **3xl:** 32px
- **4xl:** 40px

## Border Radius

- **xs:** 6px (small elements)
- **sm:** 8px
- **md:** 12px
- **lg:** 14px
- **xl:** 16px (cards, large elements)

## Shadow System

- **xs:** 0 1px 2px 0 rgba(0,0,0,0.05)
- **sm:** 0 1px 3px 0 rgba(0,0,0,0.1)
- **md:** 0 4px 6px -1px rgba(0,0,0,0.1)
- **lg:** 0 10px 15px -3px rgba(0,0,0,0.1)
- **xl:** 0 20px 25px -5px rgba(0,0,0,0.1)

## Component Classes

### Buttons
- `.btn-primary` - Navy background, white text, hover shadow-md
- `.btn-secondary` - Light background, navy text, border
- `.btn-accent` - Indigo background, white text
- `.btn-success` - Emerald background, white text

### Cards
- `.card` - White background, light border, shadow-sm, hover shadow-md
- `.card-elevated` - White background, shadow-lg, hover shadow-xl

### Inputs
- `.input-primary` - Light background, light border, indigo focus ring

### Badges
- `.badge-success` - Emerald background/10, emerald text
- `.badge-warning` - Amber background/10, amber text
- `.badge-error` - Red background/10, red text

## Design Principles

1. **Professional:** Enterprise-grade, suitable for investors and stakeholders
2. **Clean:** Minimal, uncluttered layouts with clear hierarchy
3. **Data-Driven:** High contrast, readable typography, clear metrics
4. **Accessible:** WCAG AA compliance, keyboard navigation, clear focus states
5. **Consistent:** Unified design language across all pages
6. **Modern:** Contemporary SaaS aesthetics (Stripe, Linear, Vercel style)

## Usage Examples

### Header
```tsx
<h1 className="text-6xl font-bold text-primary mb-6">
  Investment Due Diligence at Scale
</h1>
```

### Feature Card
```tsx
<div className="card hover:shadow-lg">
  <div className="w-12 h-12 rounded-lg bg-accent/10 flex items-center justify-center">
    <Icon className="w-6 h-6 text-accent" />
  </div>
  <h3 className="font-semibold text-primary mt-4">Feature</h3>
  <p className="text-sm text-text-secondary mt-2">Description</p>
</div>
```

### Button
```tsx
<button className="btn-accent px-8 py-4">Action</button>
```

### Table
```tsx
<table className="w-full">
  <thead className="bg-bg-light border-b border-border">
    <tr>
      <th className="text-left text-sm font-semibold text-primary p-4">Column</th>
    </tr>
  </thead>
  <tbody className="divide-y divide-border">
    <tr className="hover:bg-bg-light">
      <td className="p-4 text-text-primary">Data</td>
    </tr>
  </tbody>
</table>
```

## Key Improvements

✅ **Light background** - Better readability for data dashboards
✅ **Indigo accent** - Professional, modern color (used by top SaaS)
✅ **Single font family** - Improved consistency and performance
✅ **Clear hierarchy** - Proper size and weight relationships
✅ **Accessible contrast** - WCAG AA compliant
✅ **Shadow system** - Clear elevation and depth perception
✅ **No blur effects** - Better performance
✅ **Semantic colors** - Green for success, amber for warnings, red for errors

## Files Modified

- `tailwind.config.js` - Color palette, typography, spacing
- `src/index.css` - Component utility classes
- `src/pages/LandingPage.tsx` - Redesigned with new theme
- `src/pages/UploadStartup.tsx` - Professional styling
- `src/pages/AnalysisProgress.tsx` - Data visualization updates
- `src/pages/CommitteeDebate.tsx` - Component redesign
- `src/pages/FinalReport.tsx` - Report styling
- `src/pages/DigitalTwin.tsx` - Scenario modeling UI
- `src/pages/StartupComparison.tsx` - Comparison table styling

## References

Inspired by design systems from:
- Stripe (stripe.com)
- Linear (linear.app)
- Vercel (vercel.com)
- Notion (notion.so)
- Bloomberg Terminal
