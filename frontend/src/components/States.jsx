import { Link2, ScanSearch, ShieldCheck } from "lucide-react";
import "./States.css";

export function EmptyState() {
  return (
    <div className="empty-state">
      <p className="empty-state-mark">Evidence-Linked Investment Analysis</p>
      <h1>Every score traces back to a source.</h1>
      <p>
        Enter a deal ID above to run a full diligence pass across Team, Market,
        Product, Financial, and Risk. Each factor score is backed by specific
        findings, and every finding cites the source chunks it was extracted from.
      </p>
      <p>No black boxes — if a score moves, you can see exactly why.</p>

      <div className="empty-state-pillars">
        <div className="empty-pillar">
          <div className="empty-pillar-icon">
            <ScanSearch size={20} />
          </div>
          <h3>Deterministic Scoring</h3>
          <p>
            LLM extraction is separated from scoring logic — rules are
            transparent, auditable, and reproducible.
          </p>
        </div>
        <div className="empty-pillar">
          <div className="empty-pillar-icon">
            <Link2 size={20} />
          </div>
          <h3>Full Evidence Chain</h3>
          <p>
            Score → factor → finding → source chunk. Drill into any number
            to see what produced it.
          </p>
        </div>
        <div className="empty-pillar">
          <div className="empty-pillar-icon">
            <ShieldCheck size={20} />
          </div>
          <h3>Risk-Adjusted Verdict</h3>
          <p>
            INVEST / WATCHLIST / PASS reflects core strength weighed against
            execution, market, and operational risk.
          </p>
        </div>
      </div>
    </div>
  );
}

export function LoadingSkeleton() {
  return (
    <div>
      <div className="skeleton-hero" />
      <div className="skeleton-strip">
        {Array.from({ length: 5 }).map((_, i) => (
          <div className="skeleton-card" key={i} />
        ))}
      </div>
      <div className="skeleton-body" />
    </div>
  );
}
