"""
Mock data for testing research module without API calls
Person 2 uses this for development and testing
"""

from backend.contracts.research import ResearchOutput, Founder, Competitor


def get_mock_airbnb_research() -> ResearchOutput:
    """Mock research output for Airbnb"""
    return ResearchOutput(
        founders=[
            Founder(
                name="Brian Chesky",
                background="Art school graduate, design background",
                experience="Co-founder and CEO, previously worked at various startups",
                credibility_score=95,
                sources=["https://www.crunchbase.com/person/brian-chesky"]
            ),
            Founder(
                name="Joe Gebbia",
                background="Rhode Island School of Design graduate",
                experience="Co-founder and Chief Product Officer, design expertise",
                credibility_score=92,
                sources=["https://www.crunchbase.com/person/joe-gebbia"]
            ),
            Founder(
                name="Nate Blecharczyk",
                background="Harvard graduate, computer science",
                experience="Co-founder and Chief Strategy Officer, technology expertise",
                credibility_score=90,
                sources=["https://www.crunchbase.com/person/nate-blecharczyk"]
            )
        ],
        competitors=[
            Competitor(
                name="Booking.com",
                market_position="Global travel accommodation leader",
                funding="Public company (BKNG), valued at $100B+",
                key_differentiators="Larger inventory, established brand, OTA model",
                sources=["https://www.booking.com"]
            ),
            Competitor(
                name="Expedia",
                market_position="Major online travel agency",
                funding="Public company (EXPE), $30B+ market cap",
                key_differentiators="Full travel ecosystem, traditional OTA",
                sources=["https://www.expedia.com"]
            ),
            Competitor(
                name="Vrbo (HomeAway)",
                market_position="Vacation rental specialist",
                funding="Acquired by Expedia for $3.6B",
                key_differentiators="Focus on full homes, established community",
                sources=["https://www.vrbo.com"]
            )
        ],
        market_summary="""
        The short-term rental and alternative accommodation market is experiencing rapid growth.
        Global TAM estimated at $150-200B with 15-20% annual growth.
        Key trends: increased remote work enabling longer stays, post-pandemic travel surge,
        younger demographic preference for authentic experiences over hotels.
        Market is mature in developed countries (US, EU) but rapidly growing in emerging markets.
        SAM approximately $50-80B focused on urban and leisure destinations.
        """,
        funding_summary="""
        Airbnb has raised significant capital through its journey:
        - Series A-D: $100M+ total raised before IPO
        - IPO in December 2020 at $68/share
        - Current market cap: $70-90B depending on market conditions
        - Investor profile: Strong institutional backing including top-tier VCs and corporate investors
        - Post-IPO performance has been strong with consistent revenue growth
        - Demonstrates strong product-market fit and investor confidence
        """,
        industry_summary="""
        The hospitality and travel industry is undergoing significant transformation.
        Regulatory landscape: Mixed - supportive in some cities (US, EU), restrictive in others (NYC, Barcelona)
        Key macro trends:
        - Shift from traditional hotel stays to alternative accommodations
        - Digitalization of travel booking
        - Increased focus on authentic local experiences
        - Sharing economy normalized post-COVID
        Technology trends: Mobile-first approach, AI for matching, blockchain for trust
        Industry consolidation continues with major OTAs acquiring competitors
        """,
        sources=[
            "https://www.crunchbase.com",
            "https://www.booking.com",
            "https://www.expedia.com",
            "https://www.vrbo.com",
            "https://ir.airbnb.com",
            "https://en.wikipedia.org/wiki/Airbnb"
        ]
    )


def get_mock_stripe_research() -> ResearchOutput:
    """Mock research output for Stripe"""
    return ResearchOutput(
        founders=[
            Founder(
                name="Patrick Collison",
                background="Irish entrepreneur, mathematics background",
                experience="Multiple successful startups before Stripe, strong technical knowledge",
                credibility_score=98,
                sources=["https://www.crunchbase.com/person/patrick-collison"]
            ),
            Founder(
                name="John Collison",
                background="Irish entrepreneur",
                experience="Co-founder Stripe, experienced in building scalable systems",
                credibility_score=96,
                sources=["https://www.crunchbase.com/person/john-collison"]
            )
        ],
        competitors=[
            Competitor(
                name="Square",
                market_position="Payment processing and POS leader",
                funding="Public company (SQ), $125B+ market cap",
                key_differentiators="Strong retail POS presence, banking services",
                sources=["https://www.square.com"]
            ),
            Competitor(
                name="PayPal",
                market_position="Legacy payment platform",
                funding="Public company (PYPL), $50B+ market cap",
                key_differentiators="Massive user base, global reach, established brand",
                sources=["https://www.paypal.com"]
            )
        ],
        market_summary="""
        Global payment processing market is worth $300B+ annually with 10-12% growth.
        Digital payments adoption accelerating post-COVID (contactless, online, mobile).
        TAM expanding as more SMBs move online and e-commerce grows.
        SAM: $50-100B focused on online merchants and payment infrastructure.
        Key trend: API-first payment solutions replacing legacy systems.
        """,
        funding_summary="""
        Stripe has raised substantial private capital:
        - Multiple funding rounds totaling $1B+ before IPO
        - Valuations: $95B (2021), $50B (down round 2022), current private valuation $25-30B
        - Recent shift to profitability focus instead of growth at all costs
        - Investor confidence remains high despite market corrections
        - Has resisted IPO despite multiple opportunities
        """,
        industry_summary="""
        Payment processing industry consolidation accelerating.
        Regulatory landscape: Increasingly complex with PSD2 (EU), various country regulations.
        Key macro trends:
        - Crypto and blockchain disruption potential (uncertain)
        - Open banking APIs changing competitive dynamics
        - Real-time payments becoming standard expectation
        - Cross-border payments still major pain point
        Technology: Cloud-native, API-first architecture becoming standard.
        Competition intensifying from both traditional and fintech players.
        """,
        sources=[
            "https://www.crunchbase.com",
            "https://www.square.com",
            "https://www.paypal.com",
            "https://stripe.com",
            "https://en.wikipedia.org/wiki/Stripe_(company)"
        ]
    )


def get_mock_research_by_startup(startup_name: str) -> ResearchOutput:
    """Get mock data based on startup name"""
    if "airbnb" in startup_name.lower():
        return get_mock_airbnb_research()
    elif "stripe" in startup_name.lower():
        return get_mock_stripe_research()
    else:
        # Return generic mock
        return get_mock_airbnb_research()
