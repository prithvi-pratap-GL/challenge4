// Mock evaluation responses matching backend InvestmentRecommendation schema.
// Used when VITE_API_BASE_URL is not reachable, or for the bundled demo deals.
// Shape must mirror backend/domain/schemas.py exactly:
//   InvestmentRecommendation { deal_id, status, reasoning, category_scores[] }
//   CategoryScore { category, factors[], aggregate_score }
//   FactorScore { factor_name, score, findings[] }
//   Finding { finding_text, supporting_chunk_ids[] }

function finding(text, chunkPrefix, count = 2) {
  return {
    finding_text: text,
    supporting_chunk_ids: Array.from(
      { length: count },
      (_, i) => `${chunkPrefix}-${String(i + 1).padStart(3, "0")}`
    ),
  };
}

export const MOCK_DEALS = {
  "orbital-fleet-systems": {
    label: "Orbital Fleet Systems",
    subtitle: "Series A · Space logistics · SaaS B2B",
    recommendation: {
      deal_id: "orbital-fleet-systems",
      status: "invest",
      reasoning:
        "Founding team combines two prior exits in aerospace propulsion with deep domain credibility. Market sizing is conservative but the growth trajectory in commercial orbital logistics is well-substantiated by third-party reports. Product shows clear differentiation through proprietary docking telemetry, and revenue has scaled 4.2x year-over-year with improving unit economics. Primary watch item is execution risk tied to a thin operations bench during scale-up.",
      category_scores: [
        {
          category: "team",
          aggregate_score: 88,
          factors: [
            {
              factor_name: "Domain Expertise",
              score: 94,
              findings: [
                finding(
                  "CEO previously led propulsion systems engineering at a company acquired by a major aerospace prime, with eight years of direct orbital mechanics experience.",
                  "deck-p03"
                ),
                finding(
                  "CTO holds two patents in autonomous rendezvous and docking systems, both cited in subsequent industry literature.",
                  "deck-p04"
                ),
              ],
            },
            {
              factor_name: "Leadership Experience",
              score: 90,
              findings: [
                finding(
                  "Two of three co-founders have led prior ventures to acquisition, including one exit valued above $80M.",
                  "deck-p03"
                ),
                finding(
                  "Founding team has collectively managed engineering organizations exceeding 40 people at prior companies.",
                  "linkedin-founder-02",
                  1
                ),
              ],
            },
            {
              factor_name: "Team Composition",
              score: 80,
              findings: [
                finding(
                  "Current team of 22 spans propulsion engineering, flight software, and business development, but lacks a dedicated VP of Operations.",
                  "deck-p05"
                ),
                finding(
                  "Advisory board includes a former NASA program director and a logistics executive from a Fortune 500 shipping company.",
                  "website-about-01",
                  1
                ),
              ],
            },
          ],
        },
        {
          category: "market",
          aggregate_score: 81,
          factors: [
            {
              factor_name: "Market Size & TAM",
              score: 78,
              findings: [
                finding(
                  "TAM for commercial orbital logistics and last-mile satellite servicing is estimated at $4.6B by 2030 per a third-party industry report referenced in the deck.",
                  "deck-p08"
                ),
                finding(
                  "SAM is narrower at approximately $620M, focused on LEO constellation operators requiring servicing within the next five years.",
                  "deck-p09"
                ),
              ],
            },
            {
              factor_name: "Market Growth",
              score: 86,
              findings: [
                finding(
                  "Number of active LEO satellites requiring periodic servicing has grown at a 34% CAGR over the past three years according to cited tracking data.",
                  "benchmark-leo-01"
                ),
                finding(
                  "Regulatory tailwinds from new orbital debris mitigation mandates are expected to accelerate demand for servicing contracts starting next year.",
                  "news-regulatory-01",
                  1
                ),
              ],
            },
            {
              factor_name: "Competitive Position",
              score: 79,
              findings: [
                finding(
                  "Two direct competitors identified, both earlier-stage and focused on a different orbital regime (GEO vs. the company's LEO focus).",
                  "competitor-scan-01"
                ),
                finding(
                  "Proprietary docking telemetry stack is cited as a meaningful technical differentiator versus both competitors' published approaches.",
                  "deck-p11"
                ),
              ],
            },
          ],
        },
        {
          category: "product",
          aggregate_score: 84,
          factors: [
            {
              factor_name: "Product-Market Fit",
              score: 87,
              findings: [
                finding(
                  "Three signed letters of intent from constellation operators representing a combined contract value of $14M pending successful demo missions.",
                  "deck-p14"
                ),
                finding(
                  "First demonstration mission completed successfully with all primary telemetry objectives met.",
                  "press-release-01",
                  1
                ),
              ],
            },
            {
              factor_name: "Innovation & Differentiation",
              score: 85,
              findings: [
                finding(
                  "Docking telemetry approach reduces approach time by an estimated 40% versus published competitor benchmarks.",
                  "deck-p11"
                ),
                finding(
                  "Software stack is modular and designed for reuse across multiple spacecraft bus designs, reducing integration cost for future customers.",
                  "deck-p12"
                ),
              ],
            },
            {
              factor_name: "Roadmap Clarity",
              score: 80,
              findings: [
                finding(
                  "18-month roadmap includes expansion from single-satellite servicing to multi-satellite constellation contracts.",
                  "deck-p16"
                ),
                finding(
                  "Roadmap does not yet specify a clear plan for international regulatory approval in non-US jurisdictions.",
                  "deck-p17",
                  1
                ),
              ],
            },
          ],
        },
        {
          category: "financial",
          aggregate_score: 76,
          factors: [
            {
              factor_name: "Revenue & Growth",
              score: 80,
              findings: [
                finding(
                  "Annual recurring revenue grew from $1.1M to $4.6M year-over-year, a 4.2x increase driven primarily by two enterprise contracts.",
                  "deck-p20"
                ),
                finding(
                  "Pipeline of qualified opportunities totals approximately $22M across nine prospective customers.",
                  "deck-p21",
                  1
                ),
              ],
            },
            {
              factor_name: "Unit Economics",
              score: 74,
              findings: [
                finding(
                  "Reported LTV:CAC ratio of 3.4, supported by long contract durations averaging 36 months.",
                  "deck-p22"
                ),
                finding(
                  "CAC has trended upward over the past two quarters as the company expanded into less warm outbound channels.",
                  "deck-p23",
                  1
                ),
              ],
            },
            {
              factor_name: "Profitability Path",
              score: 73,
              findings: [
                finding(
                  "Current monthly burn of $480K against $6.2M cash on hand implies approximately 13 months of runway at the current rate.",
                  "deck-p24"
                ),
                finding(
                  "Management projects positive gross margin contribution per contract beginning in the next fiscal year, though this depends on planned manufacturing cost reductions.",
                  "deck-p25",
                  1
                ),
              ],
            },
          ],
        },
        {
          category: "risk",
          aggregate_score: 32,
          factors: [
            {
              factor_name: "Execution Risk",
              score: 38,
              findings: [
                finding(
                  "No dedicated operations leadership identified despite plans to scale active missions from one to six over the next 18 months.",
                  "deck-p05"
                ),
                finding(
                  "Hardware supply chain depends on a single propulsion component supplier with a six-month lead time.",
                  "deck-p27",
                  1
                ),
              ],
            },
            {
              factor_name: "Market Risk",
              score: 28,
              findings: [
                finding(
                  "Demand is partially dependent on continued growth of LEO satellite constellations, which could slow if launch costs rise materially.",
                  "benchmark-leo-01"
                ),
                finding(
                  "Pending orbital debris regulation that benefits the company's thesis has not yet been finalized and could be delayed.",
                  "news-regulatory-01",
                  1
                ),
              ],
            },
            {
              factor_name: "Operational Risk",
              score: 30,
              findings: [
                finding(
                  "Two of three founders hold dual roles spanning both technical and commercial functions, creating key-person concentration.",
                  "deck-p06"
                ),
                finding(
                  "No findings indicating an established incident response or mission-failure contingency process.",
                  "deck-p28",
                  1
                ),
              ],
            },
          ],
        },
      ],
    },
  },

  "vela-health-analytics": {
    label: "Vela Health Analytics",
    subtitle: "Seed · Clinical decision support · Healthtech",
    recommendation: {
      deal_id: "vela-health-analytics",
      status: "watchlist",
      reasoning:
        "Strong founding team with credible clinical backgrounds and a genuinely differentiated diagnostic model, but commercial traction remains early and unit economics are not yet demonstrated at scale. Market opportunity is large but highly regulated, and the company has not yet secured a clear reimbursement pathway. Recommend revisiting after the company closes its first two health-system pilots and produces initial retention data.",
      category_scores: [
        {
          category: "team",
          aggregate_score: 79,
          factors: [
            {
              factor_name: "Domain Expertise",
              score: 85,
              findings: [
                finding(
                  "Co-founder and Chief Medical Officer practiced as a board-certified radiologist for twelve years prior to founding the company.",
                  "deck-p02"
                ),
                finding(
                  "Founding data science lead previously published peer-reviewed research on diagnostic imaging models.",
                  "deck-p03",
                  1
                ),
              ],
            },
            {
              factor_name: "Leadership Experience",
              score: 72,
              findings: [
                finding(
                  "CEO has not previously held a chief executive role, though held VP-level product roles at two healthtech companies.",
                  "linkedin-founder-01",
                  1
                ),
                finding(
                  "No founder has previously led a company through an enterprise health-system sales cycle.",
                  "deck-p04",
                  1
                ),
              ],
            },
            {
              factor_name: "Team Composition",
              score: 80,
              findings: [
                finding(
                  "Team of nine includes a dedicated regulatory affairs hire with prior FDA submission experience.",
                  "deck-p05"
                ),
                finding(
                  "No commercial or sales hires have been made to date.",
                  "deck-p05",
                  1
                ),
              ],
            },
          ],
        },
        {
          category: "market",
          aggregate_score: 74,
          factors: [
            {
              factor_name: "Market Size & TAM",
              score: 76,
              findings: [
                finding(
                  "TAM for AI-assisted diagnostic imaging support in the US is estimated at $3.1B, citing a published market research report.",
                  "deck-p09"
                ),
                finding(
                  "SAM is concentrated among mid-sized health systems with existing PACS infrastructure compatible with the company's integration approach.",
                  "deck-p10",
                  1
                ),
              ],
            },
            {
              factor_name: "Market Growth",
              score: 70,
              findings: [
                finding(
                  "Adoption of AI diagnostic tools among radiology departments has grown steadily but remains below 15% penetration according to cited survey data.",
                  "benchmark-radiology-01"
                ),
                finding(
                  "Reimbursement codes for AI-assisted diagnostics remain limited, which the deck identifies as a current adoption bottleneck.",
                  "deck-p11",
                  1
                ),
              ],
            },
            {
              factor_name: "Competitive Position",
              score: 76,
              findings: [
                finding(
                  "Three larger competitors identified, each with existing FDA clearances; the company's model is differentiated by a narrower, higher-accuracy use case.",
                  "competitor-scan-02"
                ),
                finding(
                  "Reported model accuracy in internal validation exceeds the cited accuracy of one publicly disclosed competitor benchmark.",
                  "deck-p13",
                  1
                ),
              ],
            },
          ],
        },
        {
          category: "product",
          aggregate_score: 73,
          factors: [
            {
              factor_name: "Product-Market Fit",
              score: 62,
              findings: [
                finding(
                  "One health system has signed a letter of intent for a pilot program; no paid contracts are currently in place.",
                  "deck-p15"
                ),
                finding(
                  "Two additional pilot conversations are in progress but not yet documented with signed terms.",
                  "deck-p16",
                  1
                ),
              ],
            },
            {
              factor_name: "Innovation & Differentiation",
              score: 84,
              findings: [
                finding(
                  "Model architecture combines imaging data with structured EHR history, an approach the deck describes as distinct from single-modality competitors.",
                  "deck-p17"
                ),
                finding(
                  "Internal validation reports a sensitivity improvement over baseline radiologist review in a retrospective study of 1,200 cases.",
                  "deck-p18",
                  1
                ),
              ],
            },
            {
              factor_name: "Roadmap Clarity",
              score: 73,
              findings: [
                finding(
                  "Roadmap outlines FDA 510(k) submission planned within the next twelve months.",
                  "deck-p19"
                ),
                finding(
                  "No interim regulatory milestones are specified between the current state and submission.",
                  "deck-p19",
                  1
                ),
              ],
            },
          ],
        },
        {
          category: "financial",
          aggregate_score: 54,
          factors: [
            {
              factor_name: "Revenue & Growth",
              score: 35,
              findings: [
                finding(
                  "Company has not yet recognized revenue; current activity consists of pilot programs under negotiation.",
                  "deck-p21"
                ),
                finding(
                  "Pipeline includes five health systems in active discussion, representing a combined potential annual contract value of approximately $2.4M if converted.",
                  "deck-p22",
                  1
                ),
              ],
            },
            {
              factor_name: "Unit Economics",
              score: 50,
              findings: [
                finding(
                  "No LTV or CAC figures are available given the absence of paying customers.",
                  "deck-p23"
                ),
                finding(
                  "Projected per-health-system contract value is estimated at $480K annually based on comparable published deals in the sector.",
                  "benchmark-radiology-02",
                  1
                ),
              ],
            },
            {
              factor_name: "Profitability Path",
              score: 76,
              findings: [
                finding(
                  "Current monthly burn of $190K against $4.1M cash on hand implies approximately 21 months of runway.",
                  "deck-p24"
                ),
                finding(
                  "Burn rate is low relative to peer seed-stage companies in the same vertical, reflecting a lean current team.",
                  "benchmark-radiology-02",
                  1
                ),
              ],
            },
          ],
        },
        {
          category: "risk",
          aggregate_score: 52,
          factors: [
            {
              factor_name: "Execution Risk",
              score: 58,
              findings: [
                finding(
                  "No team member has previously executed an enterprise health-system sales cycle, which the company's go-to-market plan depends on.",
                  "deck-p04",
                  1
                ),
                finding(
                  "Pilot conversion timeline of three months assumed in the model has no comparable precedent cited in supporting materials.",
                  "deck-p16",
                  1
                ),
              ],
            },
            {
              factor_name: "Market Risk",
              score: 48,
              findings: [
                finding(
                  "Reimbursement pathway for the company's diagnostic category is not yet established, creating dependency on policy changes outside the company's control.",
                  "deck-p11",
                  1
                ),
                finding(
                  "Regulatory clearance timeline of twelve months is consistent with FDA's published median review times for comparable 510(k) submissions.",
                  "benchmark-radiology-01",
                  1
                ),
              ],
            },
            {
              factor_name: "Operational Risk",
              score: 50,
              findings: [
                finding(
                  "Chief Medical Officer remains the sole clinical validation resource; no redundancy exists if this individual becomes unavailable.",
                  "deck-p05",
                  1
                ),
                finding(
                  "No findings indicate a data governance or HIPAA compliance framework has been formally documented.",
                  "deck-p26",
                  1
                ),
              ],
            },
          ],
        },
      ],
    },
  },

  "northstar-fleet-fuel": {
    label: "Northstar Fleet Fuel",
    subtitle: "Series B · Fleet electrification · Climate",
    recommendation: {
      deal_id: "northstar-fleet-fuel",
      status: "pass",
      reasoning:
        "While the team has relevant logistics experience, the company faces severe unit economics challenges that have not improved across three consecutive quarters, and the competitive landscape has consolidated around two well-capitalized incumbents since the company's last raise. Burn rate implies fewer than five months of runway at current spend, and no committed bridge financing was identified. The core technology is sound but is no longer sufficiently differentiated to justify the capital required to compete at scale.",
      category_scores: [
        {
          category: "team",
          aggregate_score: 71,
          factors: [
            {
              factor_name: "Domain Expertise",
              score: 75,
              findings: [
                finding(
                  "CEO spent six years in fleet operations management at a large regional logistics company prior to founding.",
                  "deck-p02"
                ),
                finding(
                  "Engineering lead has a background in power electronics but no prior experience specific to EV charging infrastructure.",
                  "deck-p03",
                  1
                ),
              ],
            },
            {
              factor_name: "Leadership Experience",
              score: 68,
              findings: [
                finding(
                  "This is the founding team's first venture-backed company; no prior exits identified.",
                  "linkedin-founder-03",
                  1
                ),
                finding(
                  "CEO has managed teams of up to 60 people in prior operational roles.",
                  "deck-p02",
                  1
                ),
              ],
            },
            {
              factor_name: "Team Composition",
              score: 70,
              findings: [
                finding(
                  "Team has contracted from 48 to 31 employees over the past two quarters, primarily in commercial roles.",
                  "deck-p06"
                ),
                finding(
                  "Recent departures include the VP of Sales and two regional account managers, per the deck's organizational update.",
                  "deck-p06",
                  1
                ),
              ],
            },
          ],
        },
        {
          category: "market",
          aggregate_score: 62,
          factors: [
            {
              factor_name: "Market Size & TAM",
              score: 70,
              findings: [
                finding(
                  "TAM for commercial fleet electrification infrastructure remains large, cited at $11B by 2030 in an industry report.",
                  "deck-p08"
                ),
                finding(
                  "SAM has narrowed as several large fleet operators have signed multi-year contracts with the company's two largest competitors.",
                  "competitor-scan-03",
                  1
                ),
              ],
            },
            {
              factor_name: "Market Growth",
              score: 64,
              findings: [
                finding(
                  "Overall fleet electrification adoption continues to grow, though at a slower pace than the company's original projections cited in its prior round materials.",
                  "benchmark-fleet-01"
                ),
                finding(
                  "Two policy incentives the company's go-to-market plan relied on have since been reduced at the state level.",
                  "news-policy-01",
                  1
                ),
              ],
            },
            {
              factor_name: "Competitive Position",
              score: 52,
              findings: [
                finding(
                  "Two well-capitalized competitors have each raised over $150M in the past 18 months and now hold the majority of large fleet contracts identified in the competitive scan.",
                  "competitor-scan-03"
                ),
                finding(
                  "The company's hardware differentiation, cited in its prior pitch deck, is no longer mentioned as a distinguishing factor in current materials.",
                  "deck-p13",
                  1
                ),
              ],
            },
          ],
        },
        {
          category: "product",
          aggregate_score: 66,
          factors: [
            {
              factor_name: "Product-Market Fit",
              score: 60,
              findings: [
                finding(
                  "Existing customer base of fourteen fleet operators has remained stable but has not grown over the past three quarters.",
                  "deck-p15"
                ),
                finding(
                  "One existing customer has signaled intent to evaluate a competitor's offering at contract renewal, per deck commentary.",
                  "deck-p16",
                  1
                ),
              ],
            },
            {
              factor_name: "Innovation & Differentiation",
              score: 65,
              findings: [
                finding(
                  "Charging management software includes a route-optimization feature not present in one competitor's published product description.",
                  "deck-p17"
                ),
                finding(
                  "Hardware platform has not received a significant update in the past 18 months according to product changelog references in the deck.",
                  "deck-p18",
                  1
                ),
              ],
            },
            {
              factor_name: "Roadmap Clarity",
              score: 72,
              findings: [
                finding(
                  "Roadmap focuses on software-only expansion to reduce capital intensity, a shift from the prior hardware-led strategy.",
                  "deck-p19"
                ),
                finding(
                  "Roadmap timeline assumes securing bridge financing that has not yet been confirmed.",
                  "deck-p20",
                  1
                ),
              ],
            },
          ],
        },
        {
          category: "financial",
          aggregate_score: 31,
          factors: [
            {
              factor_name: "Revenue & Growth",
              score: 40,
              findings: [
                finding(
                  "Revenue has been roughly flat at approximately $3.8M ARR for three consecutive quarters.",
                  "deck-p22"
                ),
                finding(
                  "No new logo additions are reported in the most recent two quarters.",
                  "deck-p22",
                  1
                ),
              ],
            },
            {
              factor_name: "Unit Economics",
              score: 22,
              findings: [
                finding(
                  "LTV:CAC ratio has declined from 2.1 to 1.3 over the past three quarters, falling below the threshold the deck itself identifies as sustainable.",
                  "deck-p23"
                ),
                finding(
                  "Gross margin remains negative on hardware-inclusive contracts according to the most recent unit economics breakdown.",
                  "deck-p24",
                  1
                ),
              ],
            },
            {
              factor_name: "Profitability Path",
              score: 28,
              findings: [
                finding(
                  "Current monthly burn of $1.1M against $4.7M cash on hand implies approximately 4.3 months of runway at the current rate.",
                  "deck-p25"
                ),
                finding(
                  "No committed bridge financing or term sheet is referenced in the materials provided.",
                  "deck-p26",
                  1
                ),
              ],
            },
          ],
        },
        {
          category: "risk",
          aggregate_score: 78,
          factors: [
            {
              factor_name: "Execution Risk",
              score: 80,
              findings: [
                finding(
                  "Recent departure of the VP of Sales during an active fundraising process represents a significant continuity risk.",
                  "deck-p06"
                ),
                finding(
                  "Pivot to a software-only model is recent and unproven, with no customer commitments confirmed under the new model.",
                  "deck-p19",
                  1
                ),
              ],
            },
            {
              factor_name: "Market Risk",
              score: 75,
              findings: [
                finding(
                  "Reduction in state-level policy incentives directly affects the addressable portion of the company's pipeline.",
                  "news-policy-01",
                  1
                ),
                finding(
                  "Two dominant competitors now control contracts with the largest fleet operators identified in the competitive scan.",
                  "competitor-scan-03",
                  1
                ),
              ],
            },
            {
              factor_name: "Operational Risk",
              score: 80,
              findings: [
                finding(
                  "Runway of approximately 4.3 months without confirmed bridge financing represents an acute near-term operational risk.",
                  "deck-p25",
                  1
                ),
                finding(
                  "Team contraction of 35% over two quarters raises continuity concerns for existing customer support commitments.",
                  "deck-p06",
                  1
                ),
              ],
            },
          ],
        },
      ],
    },
  },
};

export const MOCK_DEAL_ORDER = [
  "orbital-fleet-systems",
  "vela-health-analytics",
  "northstar-fleet-fuel",
];
