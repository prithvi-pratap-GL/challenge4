# Firecrawl Guide - Website Content Extraction

## 🎯 **What is Firecrawl Used For?**

Firecrawl extracts **structured data from websites** (HTML → Clean Markdown/JSON).

---

## 📊 **Firecrawl vs Tavily**

| Aspect | Tavily | Firecrawl |
|--------|--------|-----------|
| **Purpose** | Web search (find URLs) | Website extraction (get content) |
| **Input** | Query string | URL |
| **Output** | Search results + snippets | Full page content |
| **Use Case** | Finding information | Extracting detailed content |
| **Speed** | Fast (1-2 sec) | Slower (3-5 sec per page) |

---

## 🔄 **Data Flow: Tavily → Firecrawl**

```
Person 3 needs startup research
    ↓
Person 2 Tavily Agent
    → Searches: "Stripe founders"
    → Returns: 8 search results with URLs
    ↓
Person 2 Firecrawl Agent (Optional)
    → Takes top URL from Tavily
    → Extracts full page content
    → Returns: Clean markdown + metadata
    ↓
Person 3 gets enriched data
```

---

## 💡 **What Firecrawl Can Extract**

### From Company Website
- ✅ Team members (from /team page)
- ✅ Product descriptions (from /products)
- ✅ Pricing information (from /pricing)
- ✅ About company (from /about)
- ✅ Press releases (from /blog or /news)
- ✅ Contact information
- ✅ All links on the page

### Output Format
```python
{
    "url": "https://stripe.com/team",
    "markdown": "# Our Team\nPatrick Collison...",
    "metadata": {
        "title": "Stripe - Our Team",
        "description": "Meet the team...",
        "image": "https://..."
    },
    "links": ["https://stripe.com/...", ...],
    "has_team_page": True,
    "has_pricing": True,
    "has_about": True
}
```

---

## 🚀 **When to Use Firecrawl**

### ✅ USE Firecrawl When:
1. You need **full page content** (not just snippets)
2. You want to extract **specific sections** (team, pricing, about)
3. You need **high-quality text** (HTML → clean Markdown)
4. You're analyzing **website structure**
5. You want **metadata** (title, description, images)

### ❌ DON'T USE When:
1. You just need to **find URLs** (use Tavily)
2. You need **real-time search results** (use Tavily)
3. You want **quick searches** (Firecrawl is slower)
4. Analyzing many pages (expensive API calls)

---

## 📝 **Current Status in Person 2**

### Currently
- ✅ **Tavily** is fully integrated and working
- ⏸️ **Firecrawl** is defined but NOT used yet
- ❌ No agents call Firecrawl in Phase 2

### Why Not Used Yet?
1. Tavily alone provides 30-40 sources per research
2. Web snippets from Tavily are sufficient for Phase 2
3. Firecrawl is expensive (per URL)
4. Better for Phase 3+ when we need enrichment

---

## 🔧 **How Firecrawl Works (Technical)**

### Method 1: Simple URL Scrape
```python
from backend.services.firecrawl.client import FirecrawlService

firecrawl = FirecrawlService()

# Scrape a URL
result = firecrawl.scrape_url("https://stripe.com/team")

print(result["markdown"])  # Full page content as markdown
print(result["metadata"])   # Title, description, etc.
print(result["links"])      # All links on page
```

### Method 2: Company Website Extraction
```python
firecrawl = FirecrawlService()

# Scrape company website for key sections
result = firecrawl.scrape_company_website("https://stripe.com")

print(result["has_team_page"])   # True/False
print(result["has_pricing"])     # True/False
print(result["has_about"])       # True/False
print(result["content"])         # Full markdown content
```

---

## 💰 **Firecrawl Pricing**

| Plan | Requests/Month | Cost |
|------|---|---|
| Free | 100 | FREE |
| Starter | 1,000 | $29/month |
| Pro | 10,000 | $99/month |
| Enterprise | Custom | Custom |

**Cost Estimate for Person 2:**
- Tavily: 30-40 requests per startup (cheap/free)
- Firecrawl: 1-3 requests per startup (expensive)
- If researching 10 startups: ~30 Firecrawl calls = ~$3 (Starter plan)

---

## 🎯 **Use Case Example**

### Scenario: Deep Dive on Top Competitor

```
Step 1: Tavily finds competitor "Square"
  Result: 8 URLs, snippets about Square

Step 2: Firecrawl extracts from top URL
  Input: https://square.com/
  Output: Full website content + team info

Step 3: Extract enriched data
  - Team members from /team page
  - Products from /products
  - Pricing from /pricing
  - Press releases from /news

Step 4: Combine with Tavily data
  - Tavily: "Square is a competitor"
  - Firecrawl: "Square has 200+ team members, $X pricing"
```

---

## 🔄 **Phase 3 Plan: Using Firecrawl**

When to integrate Firecrawl:

### Phase 3 Enhancement
```python
# After Tavily finds competitors
competitors = tavily_search("Stripe competitors")

# Use Firecrawl to enrich top competitors
for competitor in competitors[:3]:  # Top 3 only
    enriched = firecrawl.scrape_company_website(competitor.url)
    competitor.team_members = extract_team(enriched)
    competitor.pricing = extract_pricing(enriched)
```

### Cost Optimization
- Only scrape **top 3 competitors** (not all 5-7)
- Cache results (don't scrape same URL twice)
- Use free tier for testing (100 requests/month)

---

## 🚨 **Common Issues & Solutions**

### "FIRECRAWL_API_KEY not found"
```bash
# Solution: Add to .env
echo "FIRECRAWL_API_KEY=fc_xxxxx" >> .env
```

### "Firecrawl returned empty content"
- Website may be blocked from scraping
- JavaScript-heavy sites may not render
- Try another URL (homepage instead of /team page)

### "Too expensive / Rate limited"
- Only scrape critical URLs
- Cache results for 24 hours
- Use free tier for testing

---

## 📊 **Firecrawl vs Other Options**

| Tool | Purpose | Cost | Speed | Quality |
|------|---------|------|-------|---------|
| **Tavily** | Web search | Free (100/day) | Fast | Good snippets |
| **Firecrawl** | Website extraction | Paid | Medium | Excellent |
| **Selenium** | Browser automation | Free | Slow | Excellent |
| **BeautifulSoup** | HTML parsing | Free | Medium | Good |

**Recommendation**: Tavily + Firecrawl = Perfect combo for Phase 2+3

---

## 🎓 **When Firecrawl Becomes Useful**

### Not Needed Now (Phase 2)
- Tavily snippets are enough
- 30-40 sources per research is excellent
- No need for deep website analysis

### Will Need Later (Phase 3+)
- Competitor team member extraction
- Pricing analysis
- Product feature comparison
- Website structure analysis
- Press release extraction

---

## ✅ **Summary**

| Aspect | Details |
|--------|---------|
| **Purpose** | Extract structured data from websites |
| **Input** | URL |
| **Output** | Markdown, metadata, links |
| **Current Status** | Defined but not used (Phase 2) |
| **When to Use** | Phase 3+ for deep website analysis |
| **Cost** | $29-99/month (not free like Tavily) |
| **Speed** | 3-5 seconds per URL |
| **Integration** | Simple wrapper in backend/services/firecrawl/ |

---

## 🚀 **Next Steps**

**Phase 2 (Current)**: ✅ Complete with Tavily only
**Phase 3 (Future)**: Add Firecrawl for competitor enrichment

When ready for Phase 3, integrate:
```python
# In workflow.py research_competitors()
for competitor in competitors[:3]:
    enriched = firecrawl.scrape_company_website(competitor.url)
    competitor.team_details = enrich_competitor(enriched)
```

---

**Status**: Firecrawl ready when needed  
**Current**: Not required for Phase 2  
**Future**: Phase 3+ integration planned

