import { useState } from "react";
import { ChevronRight, FileText, ShieldAlert } from "lucide-react";
import {
  CATEGORY_META,
  CATEGORY_ORDER,
  categoryTier,
  formatChunkId,
} from "../utils/scoring";
import "./EvidenceLedger.css";

function FactorRow({ factor, color, defaultOpen, inverse }) {
  const [open, setOpen] = useState(defaultOpen);
  const evidenceCount = factor.findings.reduce(
    (sum, f) => sum + (f.supporting_chunk_ids?.length ?? 0),
    0
  );
  const tier = categoryTier(inverse ? "risk" : "team", factor.score);

  return (
    <div className="factor">
      <button className="factor-toggle" onClick={() => setOpen((o) => !o)}>
        <span className={`factor-toggle-chevron${open ? " open" : ""}`}>
          <ChevronRight size={16} />
        </span>
        <span className="factor-toggle-main">
          <span className="factor-name">{factor.factor_name}</span>
          <span className="factor-evidence-count">
            {factor.findings.length} finding{factor.findings.length === 1 ? "" : "s"} ·{" "}
            {evidenceCount} source{evidenceCount === 1 ? "" : "s"}
          </span>
        </span>
        <span className="factor-bar-track">
          <span
            className="factor-bar-fill"
            style={{ width: `${factor.score}%`, background: tier.color }}
          />
        </span>
        <span className="factor-tier" style={{ color: tier.color }}>
          {tier.label}
        </span>
        <span className="factor-score" style={{ color: tier.color }}>
          {factor.score}
        </span>
      </button>

      {open && (
        <div className="findings">
          {factor.findings.length === 0 ? (
            <div className="findings-empty">No findings extracted for this factor.</div>
          ) : (
            factor.findings.map((finding, idx) => (
              <div className="finding-row" key={idx}>
                <span
                  className="finding-glyph"
                  style={{
                    "--finding-color": color,
                    "--finding-color-soft": `color-mix(in srgb, ${color} 16%, transparent)`,
                  }}
                >
                  {inverse ? <ShieldAlert size={12} /> : <FileText size={12} />}
                </span>
                <div className="finding-body">
                  <p className="finding-text">{finding.finding_text}</p>
                  {finding.supporting_chunk_ids?.length > 0 && (
                    <div className="finding-sources">
                      <span className="finding-sources-label">Evidence</span>
                      {finding.supporting_chunk_ids.map((chunkId) => (
                        <span className="chunk-tag" key={chunkId} title={`Chunk ID: ${chunkId}`}>
                          {formatChunkId(chunkId)}
                        </span>
                      ))}
                    </div>
                  )}
                </div>
              </div>
            ))
          )}
        </div>
      )}
    </div>
  );
}

export default function EvidenceLedger({ categoryScores, activeCategory, onSelectCategory }) {
  const active =
    categoryScores.find((c) => c.category === activeCategory) ?? categoryScores[0];

  if (!active) return null;

  const meta = CATEGORY_META[active.category];
  const tier = categoryTier(active.category, active.aggregate_score);

  return (
    <div className="ledger">
      <div className="ledger-tabs">
        {CATEGORY_ORDER.map((key) => {
          const score = categoryScores.find((c) => c.category === key);
          if (!score) return null;
          const m = CATEGORY_META[key];
          const t = categoryTier(key, score.aggregate_score);
          const isActive = key === active.category;
          return (
            <button
              key={key}
              className={`ledger-tab${isActive ? " active" : ""}`}
              style={{ "--tab-color": t.color }}
              onClick={() => onSelectCategory(key)}
            >
              {m.label}
              <span className="ledger-tab-badge">{score.aggregate_score}</span>
            </button>
          );
        })}
      </div>

      <div className="ledger-header">
        <div className="ledger-header-text">
          <h2>{meta.label}</h2>
          <p>{meta.description}</p>
        </div>
        <div className="ledger-header-score">
          <div className="ledger-header-score-value" style={{ color: tier.color }}>
            {active.aggregate_score}
          </div>
          <p className="ledger-header-score-label">{tier.label}</p>
        </div>
      </div>

      <div>
        {active.factors.map((factor, idx) => (
          <FactorRow
            key={factor.factor_name}
            factor={factor}
            color={tier.color}
            inverse={meta.inverse}
            defaultOpen={idx === 0}
          />
        ))}
      </div>
    </div>
  );
}
