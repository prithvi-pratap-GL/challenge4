import IngestionPortal from "./components/IngestionPortal";
import { useCallback, useRef, useState } from "react";
import Sidebar from "./components/Sidebar";
import CommandBar from "./components/CommandBar";
import VerdictHero from "./components/VerdictHero";
import RadarOverview from "./components/RadarOverview";
import EvidenceLedger from "./components/EvidenceLedger";
import { EmptyState, LoadingSkeleton } from "./components/States";
import { evaluateDeal, EvaluationError } from "./api/scoring";
import { useRecentDeals } from "./hooks/useRecentDeals";
import { CATEGORY_ORDER, compositeHealth } from "./utils/scoring";
import { MOCK_DEALS } from "./data/mockDeals";
import { PanelRight } from "lucide-react";
import "./components/Shell.css";

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || "";

function buildPdfUrl(pdfPath) {
  if (!pdfPath) return null;
  if (pdfPath.startsWith("http://") || pdfPath.startsWith("https://")) {
    return pdfPath;
  }
  return `${API_BASE_URL}${pdfPath}`;
}

export default function App() {
  const [recommendation, setRecommendation] = useState(null);
  const [activeDealId, setActiveDealId] = useState("");
  const [activeCategory, setActiveCategory] = useState(CATEGORY_ORDER[0]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [pdfUrl, setPdfUrl] = useState(null);

  // New state for the split view
  const [isSplitView, setIsSplitView] = useState(false);
  const [isIngestionOpen, setIsIngestionOpen] = useState(false);
  const { recent, recordEvaluation, clearAll } = useRecentDeals();
  const abortRef = useRef(null);

  const runEvaluation = useCallback(
    async (dealId) => {
      if (abortRef.current) abortRef.current.abort();
      const controller = new AbortController();
      abortRef.current = controller;

      setLoading(true);
      setError(null);
      setRecommendation(null);

      try {
        const result = await evaluateDeal(dealId, { signal: controller.signal });
        setRecommendation(result);
        setActiveDealId(dealId);
        setActiveCategory(CATEGORY_ORDER[0]);
        setPdfUrl(result.pdf_url || null);

        recordEvaluation({
          dealId,
          label: MOCK_DEALS[dealId]?.label,
          status: result.status,
          aggregateHealth: compositeHealth(result.category_scores),
        });
      } catch (err) {
        if (err.name === "AbortError") return;
        if (err instanceof EvaluationError) {
          setError(err.message);
        } else {
          setError("Something went wrong running this evaluation. Please try again.");
        }
      } finally {
        setLoading(false);
      }
    },
    [recordEvaluation]
  );

  return (
    <div className="shell">
      <Sidebar
        recent={recent}
        activeDealId={activeDealId}
        onSelect={runEvaluation}
        onClear={clearAll}
        onNewDeal={() => setIsIngestionOpen(true)}
      />

      <main className="main">
        {/* Toggle between standard and split layout classes based on state */}
        <div className={isSplitView && recommendation ? "main-split" : "main-inner"}>
          
          {/* Left Column (or full width if not split) */}
          <div className="main-content-column">
            <CommandBar
              onEvaluate={runEvaluation}
              loading={loading}
              error={error}
              initialValue={activeDealId}
              isSplitView={isSplitView}
              onToggleSplit={() => setIsSplitView(!isSplitView)}
              hasRecommendation={!!recommendation}
            />
            {loading && <LoadingSkeleton />}

            {!loading && !recommendation && <EmptyState />}

            {!loading && recommendation && (
              <>
                <VerdictHero
                  recommendation={recommendation}
                  activeCategory={activeCategory}
                  onSelectCategory={setActiveCategory}
                />
                <RadarOverview categoryScores={recommendation.category_scores} />
                <EvidenceLedger
                  categoryScores={recommendation.category_scores}
                  activeCategory={activeCategory}
                  onSelectCategory={setActiveCategory}
                />
              </>
            )}
          </div>

          {/* Right Column (PDF Viewer) - Only renders when Split View is active */}
          {isSplitView && recommendation && (
              <div className="main-pdf-column">
                  <div className="pdf-viewer-container">
                      <div className="pdf-viewer-header">
                          <span className="pdf-header-title">Source Material: Pitch Deck</span>
                          <span className="pdf-header-badge">View Only</span>
                      </div>
                      {pdfUrl ? (
                          <iframe
                              src={`${buildPdfUrl(pdfUrl)}#toolbar=0&navpanes=0`}
                              title="Pitch Deck Viewer"
                              className="pdf-iframe"
                          />
                      ) : (
                          <div className="pdf-empty-state">
                              <p>No source document available.</p>
                          </div>
                      )}
                  </div>
              </div>
          )}

        </div>
      </main>
      <IngestionPortal 
        isOpen={isIngestionOpen} 
        onClose={() => setIsIngestionOpen(false)} 
        onComplete={(data) => {
          // If the backend returns a deal_id, automatically run the evaluation!
          if (data && data.deal_id) {
            runEvaluation(data.deal_id);
          }
        }}
      />
    </div>
  );
}