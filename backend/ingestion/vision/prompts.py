"""Vision analysis prompts - store prompts only, no business logic."""

PITCH_DECK_ANALYSIS_PROMPT = """Analyze this startup pitch deck slide and extract structured information.

Focus on extracting:
1. Startup summary - what the company does
2. Business model - how they make money
3. Risks - potential challenges or concerns
4. Financials - revenue, growth numbers, projections
5. Market claims - market size (TAM/SAM/SOM), customer claims, growth claims, competitive advantages
6. Evidence - references to specific claims (e.g., "Slide 3 shows ARR of $2M", "Team slide mentions 10+ years industry experience")
7. Founder/team information if visible
8. Competitor information if mentioned
9. Any graphs, charts, or tables with numerical data

Return response as JSON with these fields:
{
    "startup_summary": "...",
    "business_model": "...",
    "risks": ["...", "..."],
    "financials": ["...", "..."],
    "market_claims": ["...", "..."],
    "evidence": ["...", "..."],
    "founder_info": "...",
    "competitors": ["...", "..."],
    "charts_data": {"chart_type": "...", "data": "..."}
}

Be precise and extract actual numbers when visible.
Reference slide content in evidence field."""

DECK_CONTEXT_ASSEMBLY_PROMPT = """Given an analysis of all slides in a pitch deck, create a comprehensive searchable context string.

Combine:
- Startup summary
- Business model explanation
- Market and growth claims
- Financial figures
- Team and founder information
- Competitive landscape
- Risk factors

Create a single cohesive paragraph that a search engine could effectively index and retrieve from.
This context will be used for semantic search across the startup's information."""

WEBSITE_ANALYSIS_PROMPT = """Analyze the website content and extract structured information about the startup.

Focus on:
1. Company description and mission
2. Product/service explanation
3. Business model - how they make money
4. Pricing information if available
5. Customer/user information
6. Company claims about market position, growth, or capabilities
7. Team information if available
8. Financial information if disclosed
9. Risk factors or limitations mentioned

Return as JSON:
{
    "startup_summary": "...",
    "business_model": "...",
    "risks": ["...", "..."],
    "financials": ["...", "..."],
    "market_claims": ["...", "..."],
    "evidence": ["...", "..."]
}

Extract actual claims from the website content.
Be factual - only include what is explicitly stated."""
