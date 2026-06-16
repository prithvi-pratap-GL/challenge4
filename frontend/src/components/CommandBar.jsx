import { useState } from "react";
import { Search, AlertTriangle, ArrowRight, PanelRight } from "lucide-react";
import { MOCK_DEAL_ORDER, MOCK_DEALS } from "../data/mockDeals";
import "./CommandBar.css";

export default function CommandBar({ 
  onEvaluate, 
  loading, 
  error, 
  initialValue = "",
  isSplitView,
  onToggleSplit,
  hasRecommendation
}) {
  const [value, setValue] = useState(initialValue);

  function handleSubmit(e) {
    e.preventDefault();
    if (!value.trim() || loading) return;
    onEvaluate(value.trim());
  }

  function handleSample(dealId) {
    setValue(dealId);
    onEvaluate(dealId);
  }

  return (
    <div className="command-bar">
      <p className="command-eyebrow">Run Diligence Evaluation</p>
      <form className="command-form" onSubmit={handleSubmit}>
        <div className="command-input-wrap">
          <span className="command-input-icon">
            <Search size={16} />
          </span>
          <input
            className="command-input"
            type="text"
            placeholder="Enter deal ID — e.g. orbital-fleet-systems"
            value={value}
            onChange={(e) => setValue(e.target.value)}
            autoComplete="off"
            spellCheck={false}
          />
        </div>
        <button className="command-submit" type="submit" disabled={loading}>
          {loading ? (
            <span className="command-spinner" aria-hidden="true" />
          ) : (
            <ArrowRight size={16} />
          )}
          {loading ? "Evaluating" : "Evaluate"}
        </button>

        {/* The Split View Toggle Button cleanly aligned in the flex row */}
        {hasRecommendation && (
          <button 
            type="button"
            onClick={onToggleSplit}
            className={`split-toggle-btn ${isSplitView ? 'active' : ''}`}
            title="Toggle Split View"
          >
            <PanelRight size={18} />
          </button>
        )}
      </form>

      <div className="sample-deals">
        <span className="sample-deals-label">Sample deals:</span>
        {MOCK_DEAL_ORDER.map((id) => (
          <button key={id} className="sample-chip" onClick={() => handleSample(id)} type="button">
            {MOCK_DEALS[id].label}
          </button>
        ))}
      </div>

      {error && (
        <div className="command-error">
          <AlertTriangle size={16} />
          <span>{error}</span>
        </div>
      )}
    </div>
  );
}