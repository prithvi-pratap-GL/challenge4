import { StartupAnalysis, AnalysisStatus } from '../types/index';

export const mockStartupAnalysis: StartupAnalysis = {
  id: 'airbnb-001',
  startup_name: 'Airbnb',
  website_url: 'https://www.airbnb.com',
  research_data: {
    founders: [
      {
        name: 'Brian Chesky',
        role: 'CEO & Co-founder',
        experience: 'Designer, previously worked on startups',
        education: 'RISD School of Design',
      },
      {
        name: 'Joe Gebbia',
        role: 'Chief Product Officer',
        experience: 'Designer, product innovator',
        education: 'RISD',
      },
      {
        name: 'Nate Blecharczyk',
        role: 'Chief Strategy Officer',
        experience: 'Software engineer, data scientist',
        education: 'Harvard University',
      },
    ],
    competitors: [
      {
        name: 'Booking.com',
        market_cap: '$100B',
        funding: 'Public',
        description: 'Online travel and accommodation platform',
      },
      {
        name: 'Expedia',
        market_cap: '$20B',
        funding: 'Public',
        description: 'Travel booking and accommodation platform',
      },
      {
        name: 'VRBO',
        funding: 'Expedia subsidiary',
        description: 'Vacation rental platform',
      },
    ],
    market_analysis:
      'The short-term rental market is experiencing significant growth with increasing demand for alternative accommodations. Market size is estimated at $100B+ globally with 15-20% annual growth. Key trends include increasing mobile adoption, personalization, and experience-focused travel.',
  },
  rag_data: {
    context:
      "Airbnb's business model disrupted the hospitality industry by enabling peer-to-peer short-term rentals. The platform benefits from network effects where more hosts attract more guests and vice versa. Key success factors include community trust, reliable payment systems, and consistent brand experience.",
    sources: [
      'https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=1816661&type=&dateb=&owner=exclude&count=100',
      'https://www.airbnb.com/press/news',
    ],
  },
  committee_decision: {
    bull_case:
      'Massive TAM with strong market fundamentals. Proven business model with consistent growth. Strong founder team with execution track record. Network effects create defensible moat. Multiple expansion opportunities including experiences and long-term stays.',
    bear_case:
      'Heavy regulatory scrutiny across markets. Increasing competition from established players. High customer acquisition costs. Dependency on host supply and quality. Susceptible to economic downturns.',
    red_team_feedback:
      'Unit economics assumptions may be too optimistic. Regulatory risks underestimated. International expansion more difficult than projections. Competition from hotels adapting to market changes.',
    verdict: 'STRONG BUY - Excellent investment opportunity',
    confidence: 0.92,
  },
  final_report: {
    founder_score: 9.2,
    market_score: 9.5,
    risk_score: 3.8,
    recommendation: 'STRONG BUY - Proceed with investment',
    report: `
## Investment Recommendation: Airbnb

### Executive Summary
Airbnb represents an exceptional investment opportunity at the intersection of a massive TAM, proven business model, and exceptional founder team.

### Key Metrics
- **Founder Score: 9.2/10** - Brian Chesky, Joe Gebbia, and Nate Blecharczyk demonstrate exceptional execution capability with complementary skills
- **Market Score: 9.5/10** - Multi-billion dollar TAM with strong secular tailwinds
- **Risk Score: 3.8/10** - Primary risks are regulatory and competitive, both manageable

### Investment Thesis
1. **Massive TAM**: Global accommodation market is $500B+ with significant digital penetration opportunity
2. **Defensible Moat**: Network effects, community trust, and brand strength create sustainable competitive advantage
3. **Exceptional Team**: Proven ability to execute through cycles with strong design and technical expertise
4. **Multiple Expansion**: Beyond core short-term rentals, opportunities in experiences, long-term stays, and adjacent categories

### Risk Mitigation
- Diverse geographic revenue reduces regulatory concentration risk
- Strong capital position allows for geographic expansion
- Experienced team has navigated previous crises
- Multiple revenue streams reduce concentration risk

### Recommendation
**STRONG BUY** - Allocate $50-100M for Series B+ round. Expected 10x+ return potential over 7-10 year horizon.
    `,
  },
  created_at: new Date().toISOString(),
};

export const mockAnalysisStatuses: AnalysisStatus[] = [
  {
    id: 'airbnb-001',
    status: 'research',
    current_agent: 'Research Agent',
    progress: 25,
    startup_name: 'Airbnb',
  },
  {
    id: 'uber-001',
    status: 'rag',
    current_agent: 'RAG Agent',
    progress: 50,
    startup_name: 'Uber',
  },
  {
    id: 'stripe-001',
    status: 'committee',
    current_agent: 'Bull Agent',
    progress: 75,
    startup_name: 'Stripe',
  },
];

export const mockPreviousStartups: StartupAnalysis[] = [
  {
    id: 'uber-001',
    startup_name: 'Uber',
    website_url: 'https://www.uber.com',
    research_data: {
      founders: [
        {
          name: 'Travis Kalanick',
          role: 'CEO & Co-founder',
          experience: 'Serial entrepreneur',
          education: 'UCLA',
        },
        {
          name: 'Garrett Camp',
          role: 'Co-founder',
          experience: 'StumbleUpon founder',
          education: 'University of Waterloo',
        },
      ],
      competitors: [
        {
          name: 'Lyft',
          market_cap: '$5B',
          description: 'Ride-sharing platform',
        },
        {
          name: 'Local Taxis',
          description: 'Traditional taxi services',
        },
      ],
      market_analysis: 'Global ride-sharing market worth $100B+ with room for growth',
    },
    rag_data: {
      context: 'Uber pioneered the ride-sharing economy with strong network effects',
      sources: ['https://www.uber.com/newsroom'],
    },
    committee_decision: {
      bull_case: 'Massive market opportunity with first-mover advantage',
      bear_case: 'Regulatory challenges and driver classification issues',
      red_team_feedback: 'Profitability timeline extended further than expected',
      verdict: 'BUY',
      confidence: 0.85,
    },
    final_report: {
      founder_score: 8.5,
      market_score: 9.0,
      risk_score: 5.2,
      recommendation: 'BUY - Strong opportunity despite regulatory risks',
      report: 'Uber represents a transformative opportunity in transportation',
    },
    created_at: new Date(Date.now() - 30 * 24 * 60 * 60 * 1000).toISOString(),
  },
];
