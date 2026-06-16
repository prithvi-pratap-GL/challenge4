import { Plus } from "lucide-react";
import { STATUS_META } from "../utils/scoring";
import "./Shell.css";

export default function Sidebar({ recent, activeDealId, onSelect, onClear, onNewDeal }) {
  return (
    <aside className="sidebar">
      <div className="brand">
        <div className="brand-mark">V</div>
        <div className="brand-name">VentureMind</div>
      </div>
      <p className="brand-tagline">Diligence Terminal</p>

      {/* NEW: The primary action button for the portal */}
      <div className="sidebar-section" style={{ marginBottom: "32px", marginTop: "12px" }}>
        <button
          onClick={onNewDeal}
          style={{
            width: "100%",
            display: "flex",
            alignItems: "center",
            justifyContent: "center",
            gap: "8px",
            background: "var(--signal)",
            color: "var(--ink)",
            border: "none",
            borderRadius: "var(--radius-md)",
            padding: "12px",
            fontFamily: "var(--font-body)",
            fontWeight: "600",
            fontSize: "14px",
            cursor: "pointer",
            transition: "filter 0.15s ease, transform 0.05s ease",
          }}
          onMouseOver={(e) => (e.currentTarget.style.filter = "brightness(1.08)")}
          onMouseOut={(e) => (e.currentTarget.style.filter = "none")}
          onMouseDown={(e) => (e.currentTarget.style.transform = "translateY(1px)")}
          onMouseUp={(e) => (e.currentTarget.style.transform = "none")}
        >
          <Plus size={18} strokeWidth={2.5} />
          Analyze New Deal
        </button>
      </div>

      <div className="sidebar-section">
        <p className="sidebar-label">
          <span>Recent Evaluations</span>
          {recent.length > 0 && <button onClick={onClear}>Clear</button>}
        </p>

        {recent.length === 0 ? (
          <p className="recent-empty">
            Evaluations you run will appear here for quick comparison.
          </p>
        ) : (
          <div className="recent-list">
            {recent.map((item) => {
              const meta = STATUS_META[item.status] ?? STATUS_META.watchlist;
              return (
                <button
                  key={item.dealId}
                  className={`recent-item${item.dealId === activeDealId ? " active" : ""}`}
                  onClick={() => onSelect(item.dealId)}
                  title={item.dealId}
                >
                  <span className="recent-dot" style={{ background: meta.color }} />
                  <span className="recent-item-text">
                    <span className="recent-item-name">{item.label || item.dealId}</span>
                    <span className="recent-item-meta">
                      {meta.label} · {item.aggregateHealth}/100
                    </span>
                  </span>
                </button>
              );
            })}
          </div>
        )}
      </div>

      <div className="sidebar-footer">
        Evidence-linked scoring across Team, Market, Product, Financial and
        Risk. Every factor traces to source <code>chunk_ids</code>.
      </div>
    </aside>
  );
}