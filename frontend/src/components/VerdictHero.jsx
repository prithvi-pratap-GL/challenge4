import {
  CATEGORY_META,
  CATEGORY_ORDER,
  STATUS_META,
  categoryTier,
  compositeHealth,
} from "../utils/scoring";
import "./VerdictHero.css";

export default function VerdictHero({ recommendation, activeCategory, onSelectCategory }) {
  const { deal_id, status, reasoning, category_scores } = recommendation;
  const meta = STATUS_META[status] ?? STATUS_META.watchlist;
  const health = compositeHealth(category_scores);

  const glow =
    status === "invest"
      ? "var(--verified-soft)"
      : status === "pass"
        ? "var(--risk-soft)"
        : "var(--signal-soft)";

  const scoresByCategory = Object.fromEntries(
    category_scores.map((c) => [c.category, c])
  );

  return (
    <>
      <div className="verdict-hero" style={{ "--verdict-glow": glow }}>
        <div className="verdict-top">
          <div>
            <p className="verdict-deal">{deal_id}</p>
            <div className="verdict-title">
              <h1 className="verdict-status" style={{ color: meta.color }}>
                {meta.label}
              </h1>
              <p className="verdict-status-desc">{meta.description}</p>
            </div>
          </div>
          <div className="verdict-health">
            <div className="verdict-health-value">
              {health}
              <span>/100</span>
            </div>
            <p className="verdict-health-label">Composite Health</p>
          </div>
        </div>

        <p className="verdict-reasoning">{reasoning}</p>
      </div>

      <div className="score-strip">
        {CATEGORY_ORDER.map((key) => {
          const score = scoresByCategory[key];
          if (!score) return null;
          const catMeta = CATEGORY_META[key];
          const tier = categoryTier(key, score.aggregate_score);
          const isActive = activeCategory === key;

          return (
            <button
              key={key}
              className={`score-card${isActive ? " active" : ""}`}
              style={{ "--score-color": tier.color }}
              onClick={() => onSelectCategory(key)}
              type="button"
            >
              <div className="score-card-head">
                <span className="score-card-label">{catMeta.short}</span>
                <span
                  className="score-card-tier"
                  style={{ color: tier.color, background: "transparent", border: `1px solid ${tier.color}` }}
                >
                  {tier.label}
                </span>
              </div>
              <div>
                <span className="score-card-name">{catMeta.label}</span>
              </div>
              <div className="score-card-value-row">
                <span className="score-card-value" style={{ color: tier.color }}>
                  {score.aggregate_score}
                </span>
                <span className="score-card-max">/ 100</span>
              </div>
              <div className="score-card-bar-track">
                <div
                  className="score-card-bar-fill"
                  style={{
                    width: `${score.aggregate_score}%`,
                    background: tier.color,
                  }}
                />
              </div>
            </button>
          );
        })}
      </div>
    </>
  );
}
