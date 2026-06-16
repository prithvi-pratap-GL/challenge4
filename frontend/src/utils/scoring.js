export const CATEGORY_META = {
  team: {
    label: "Team",
    short: "TEAM",
    description: "Founders, leadership track record, organizational depth",
    inverse: false,
  },
  market: {
    label: "Market",
    short: "MKT",
    description: "Size, growth trajectory, competitive position",
    inverse: false,
  },
  product: {
    label: "Product",
    short: "PROD",
    description: "Fit, differentiation, roadmap clarity",
    inverse: false,
  },
  financial: {
    label: "Financial",
    short: "FIN",
    description: "Revenue, unit economics, runway",
    inverse: false,
  },
  risk: {
    label: "Risk",
    short: "RISK",
    description: "Execution, market, and operational exposure",
    inverse: true, // lower is better
  },
};

export const CATEGORY_ORDER = ["team", "market", "product", "financial", "risk"];

export const STATUS_META = {
  invest: {
    label: "Invest",
    description: "Recommended for investment committee review",
    color: "var(--verified)",
    soft: "var(--verified-soft)",
  },
  watchlist: {
    label: "Watchlist",
    description: "Promising, but unresolved questions remain",
    color: "var(--signal)",
    soft: "var(--signal-soft)",
  },
  pass: {
    label: "Pass",
    description: "Does not currently meet the investment bar",
    color: "var(--risk)",
    soft: "var(--risk-soft)",
  },
};

/**
 * Returns a tier descriptor for a 0-100 score.
 * For inverse categories (risk), the tier meaning flips but the
 * numeric thresholds describing the *visual band* stay the same -
 * the caller should pass the already-correct "goodness" framing if needed.
 */
export function scoreTier(score) {
  if (score >= 76) return { label: "Excellent", color: "var(--verified)" };
  if (score >= 61) return { label: "Strong", color: "var(--signal)" };
  if (score >= 41) return { label: "Adequate", color: "var(--muted)" };
  return { label: "Weak", color: "var(--risk)" };
}

/**
 * Risk uses inverse framing: a LOW risk score is good.
 */
export function riskTier(score) {
  if (score <= 30) return { label: "Low", color: "var(--verified)" };
  if (score <= 50) return { label: "Moderate", color: "var(--signal)" };
  if (score <= 70) return { label: "Elevated", color: "var(--muted)" };
  return { label: "Severe", color: "var(--risk)" };
}

export function categoryTier(category, score) {
  return CATEGORY_META[category]?.inverse ? riskTier(score) : scoreTier(score);
}

/**
 * Composite "health" score across categories for headline display.
 * Risk is inverted (100 - risk) before averaging so all five
 * dimensions point in the same "higher is better" direction.
 */
export function compositeHealth(categoryScores) {
  if (!categoryScores?.length) return 0;
  const total = categoryScores.reduce((sum, c) => {
    const value = CATEGORY_META[c.category]?.inverse ? 100 - c.aggregate_score : c.aggregate_score;
    return sum + value;
  }, 0);
  return Math.round(total / categoryScores.length);
}

export function formatChunkId(id) {
  return id.replace(/-/g, " · ");
}

export function titleCase(value) {
  return value
    .split(/[\s_-]+/)
    .map((word) => word.charAt(0).toUpperCase() + word.slice(1))
    .join(" ");
}
