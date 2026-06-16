import {
  Radar,
  RadarChart,
  PolarGrid,
  PolarAngleAxis,
  PolarRadiusAxis,
  ResponsiveContainer,
  Tooltip,
} from "recharts";
import { CATEGORY_META, CATEGORY_ORDER, categoryTier } from "../utils/scoring";
import "./RadarOverview.css";

function CustomTooltip({ active, payload }) {
  if (!active || !payload?.length) return null;
  const point = payload[0].payload;
  return (
    <div
      style={{
        background: "var(--ink)",
        border: "1px solid var(--line-strong)",
        borderRadius: 8,
        padding: "8px 12px",
        fontSize: 12.5,
        fontFamily: "var(--font-mono)",
        color: "var(--text-primary)",
      }}
    >
      <div style={{ fontWeight: 600, marginBottom: 2 }}>{point.fullLabel}</div>
      <div style={{ color: "var(--text-secondary)" }}>{point.displayScore} / 100</div>
    </div>
  );
}

export default function RadarOverview({ categoryScores }) {
  const data = CATEGORY_ORDER.map((key) => {
    const score = categoryScores.find((c) => c.category === key);
    const meta = CATEGORY_META[key];
    const raw = score?.aggregate_score ?? 0;
    // For risk, plot inverted so "outward" always means "favorable" on the radar.
    const plotted = meta.inverse ? 100 - raw : raw;
    return {
      label: meta.short,
      fullLabel: meta.label,
      value: plotted,
      displayScore: raw,
    };
  });

  return (
    <div className="radar-panel">
      <div className="radar-panel-head">
        <h2 className="radar-panel-title">Dimensional Profile</h2>
        <p className="radar-panel-sub">Outward = favorable</p>
      </div>

      <div className="radar-grid">
        <div style={{ width: "100%", height: 280 }}>
          <ResponsiveContainer>
            <RadarChart data={data} outerRadius="75%">
              <PolarGrid stroke="var(--line)" />
              <PolarAngleAxis
                dataKey="label"
                tick={{ fill: "var(--text-secondary)", fontSize: 12, fontFamily: "var(--font-mono)" }}
              />
              <PolarRadiusAxis
                domain={[0, 100]}
                tick={false}
                axisLine={false}
                tickCount={5}
              />
              <Radar
                dataKey="value"
                stroke="var(--signal)"
                fill="var(--signal)"
                fillOpacity={0.18}
                strokeWidth={2}
                dot={{ r: 3, fill: "var(--signal)", strokeWidth: 0 }}
              />
              <Tooltip content={<CustomTooltip />} />
            </RadarChart>
          </ResponsiveContainer>
        </div>

        <div className="radar-legend">
          {CATEGORY_ORDER.map((key) => {
            const score = categoryScores.find((c) => c.category === key);
            if (!score) return null;
            const meta = CATEGORY_META[key];
            const tier = categoryTier(key, score.aggregate_score);
            return (
              <div className="radar-legend-row" key={key}>
                <span className="radar-legend-name">{meta.label}</span>
                <div className="radar-legend-track">
                  <div
                    className="radar-legend-fill"
                    style={{ width: `${score.aggregate_score}%`, background: tier.color }}
                  />
                </div>
                <span className="radar-legend-value">{score.aggregate_score}</span>
              </div>
            );
          })}
        </div>
      </div>
    </div>
  );
}
