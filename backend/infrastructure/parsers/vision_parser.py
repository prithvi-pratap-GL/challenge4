import base64
import logging
from typing import List

from openai import AsyncOpenAI

from backend.core.settings import settings
from backend.domain.interfaces import IPdfParser
from backend.domain.schemas import PageAnalysis

logger = logging.getLogger(__name__)


class VisionPdfParser(IPdfParser):
    """
    Implementation of IPdfParser using AsyncOpenAI pointing to Groq
    for vision-language models (e.g., meta-llama/llama-4-scout-17b-16e-instruct).
    """

    def __init__(self):
        self.api_key = settings.groq_api_key
        self.base_url = settings.groq_base_url
        self.model = settings.vision_model
        self.client = AsyncOpenAI(api_key=self.api_key, base_url=self.base_url)

    def _image_to_base64(self, image_path: str) -> str:
        """Helper function to convert a local PNG image to a Base64 string."""
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode("utf-8")

    async def parse_page(self, image_path: str, raw_text: str) -> PageAnalysis:
        """
        Parse a single page using the vision model, grounding metrics in the provided raw text.
        """
        base64_image = self._image_to_base64(image_path)

        # system_prompt = (
        #     "You are a ruthless VC analyst extracting hard data from a startup pitch deck. "
        #     "Return STRICTLY valid JSON with these EXACT field names and types:\n"
        #     "{\n"
        #     '  "page_number": <int>,\n'
        #     '  "page_type": "<string: financial_table, chart, text, cover, or other>",\n'
        #     '  "visual_summary": "<string: Extract the actual business facts, product features, and key takeaways. DO NOT say \'The image shows\' or describe the layout. State the facts directly.>",\n'
        #     '  "claims": [<list of strings: specific business claims or competitive advantages>],\n'
        #     '  "metrics": [<list of strings: strict quantifiable financial or operational metrics>],\n'
        #     '  "entities": [<list of strings: named competitors, partners, or products>]\n'
        #     "}\n\n"
        #     "CRITICAL: Use snake_case field names. Do not hallucinate metrics. "
        #     "Never start sentences with 'The image shows' or 'This page contains'."
        # )


        system_prompt = """
You are a top-tier venture capital analyst specializing in startup due diligence.

Your task is NOT to describe slides.

Your task is to extract investment-relevant evidence from pitch deck pages.

You will receive:

1. A pitch deck page image.
2. OCR/raw text extracted from the page.

Use BOTH sources.

The image is the source of truth for:

* charts
* graphs
* tables
* financial models
* KPIs
* market maps
* competitive matrices
* timelines
* product screenshots
* organizational charts

The OCR text is supporting context.

---

## PRIMARY OBJECTIVE

Extract information that would matter to an investor evaluating:

* Market opportunity
* Product strength
* Traction
* Revenue
* Growth
* Unit economics
* Customer adoption
* Team quality
* Competitive positioning
* Go-to-market strategy
* Fundraising readiness

---

## PAGE TYPE CLASSIFICATION

Classify page_type as one of:

cover
team
product
market
traction
financial_table
chart
competition
business_model
go_to_market
roadmap
fundraising
appendix
other

---

## VISUAL SUMMARY RULES

visual_summary MUST contain factual business information.

DO NOT describe layouts.

BAD:
"The slide contains a bar chart."

BAD:
"The image shows a table."

GOOD:
"Revenue increased from $1.2M in 2022 to $6.8M in 2024. Enterprise customers represent 72% of ARR."

GOOD:
"Product automates compliance workflows using AI and targets mid-market financial institutions."

The summary should read like an investor diligence note.

Maximum 150 words.

---

## CLAIMS EXTRACTION

Extract explicit business claims.

Examples:

* "Reduces underwriting time by 80%"
* "Serving over 500 enterprise customers"
* "Market leader in autonomous warehouse robotics"
* "Achieved product-market fit in healthcare"

Only include claims directly supported by the slide.

Do not infer.

Maximum 15 claims.

---

## METRICS EXTRACTION (HIGHEST PRIORITY)

Extract EVERY quantitative metric visible on the page.

This includes:

Financial Metrics:

* ARR
* Revenue
* Gross Margin
* EBITDA
* Burn Rate
* Cash Balance
* Runway
* CAC
* LTV
* LTV/CAC
* Payback Period
* NRR
* GRR

Growth Metrics:

* YoY Growth
* QoQ Growth
* CAGR
* User Growth
* Customer Growth

Market Metrics:

* TAM
* SAM
* SOM

Operational Metrics:

* Customers
* Users
* Transactions
* Contracts
* Pipeline
* NPS
* Headcount

Preserve units exactly as shown.

Examples:

"ARR: $12.4M"
"Revenue: $8.1M"
"YoY Growth: 320%"
"Customers: 1450"
"NRR: 128%"
"TAM: $42B"
"Cash Runway: 18 months"

Maximum 50 metrics.

---

## CHART INTERPRETATION

Charts are extremely important.

If a chart contains numbers, extract them.

For line charts:

* starting value
* ending value
* intermediate values
* trend

For bar charts:

* category labels
* values

For financial charts:

* revenue progression
* customer progression
* growth progression

Example:

Revenue chart:

2021 = $0.8M
2022 = $2.4M
2023 = $7.2M

Claims:

"Revenue grew from $0.8M to $7.2M between 2021 and 2023"

Metrics:

"Revenue 2021: $0.8M"
"Revenue 2022: $2.4M"
"Revenue 2023: $7.2M"

---

## TABLE EXTRACTION

Tables often contain the most valuable diligence data.

Extract:

* row labels
* values
* percentages
* forecasts
* historical performance

Do not collapse tables into generic summaries.

Preserve key figures.

---

## ENTITY EXTRACTION

Extract:

* company names
* customer logos
* investors
* competitors
* products
* technologies
* partnerships
* executives
* founders

Maximum 50 entities.

---

## EVIDENCE QUALITY RULES

Your output will be embedded into a vector database and later used by an investment memo generation system.

Therefore:

* Prefer specific facts over summaries.
* Prefer metrics over narratives.
* Prefer numbers over adjectives.
* Extract every meaningful KPI.
* Extract every visible financial figure.
* Extract every market size figure.
* Extract every growth figure.

Missing metrics are worse than longer outputs.

---

## HALLUCINATION RULES

NEVER invent:

* revenue
* ARR
* customers
* market sizes
* percentages
* financial metrics
* growth rates

If uncertain, omit.

If partially visible, extract only what can be confidently read.

Accuracy is more important than completeness.

---

## OUTPUT FORMAT

Return STRICTLY valid JSON.

Use EXACT field names:

{
"page_number": 0,
"page_type": "chart",
"visual_summary": "",
"claims": [],
"metrics": [],
"entities": []
}

Return JSON only.

No markdown.
No explanations.
No extra text.
"""



        user_prompt = f"Raw text from page:\n{raw_text}\n\nAnalyze the image and return the JSON analysis with the exact schema specified."

        try:
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {
                        "role": "user",
                        "content": [
                            {"type": "text", "text": user_prompt},
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": f"data:image/png;base64,{base64_image}"
                                },
                            },
                        ],
                    },
                ],
                response_format={"type": "json_object"},
                temperature=0.0,
            )

            content = response.choices[0].message.content
            if not content:
                raise ValueError("Empty response from vision model")

            return PageAnalysis.model_validate_json(content)

        except Exception as e:
            logger.error("Failed to parse page %s: %s", image_path, str(e))
            # Return a fallback analysis to prevent pipeline failure
            return PageAnalysis(
                page_number=0,
                page_type="unknown",
                visual_summary="Failed to analyze visual elements.",
                claims=[],
                metrics=[],
                entities=[],
            )

    async def parse(self, file_path: str) -> List[PageAnalysis]:
        """
        Wrapper for full file parsing. In practice, the service layer should use
        `parse_page` concurrently for better performance and rate limit management.
        """
        raise NotImplementedError(
            "Use parse_page for concurrent page analysis in the service layer"
        )