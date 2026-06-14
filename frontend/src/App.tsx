/**
 * VentureMind AI - Research Intelligence Frontend
 * Person 1's UI for Person 2's research backend
 */

import React, { useEffect } from "react";
import { useResearch } from "./hooks/useResearch";
import { ResearchForm } from "./components/ResearchForm";
import { ResearchResults } from "./components/ResearchResults";
import researchApi from "./services/researchApi";
import "./App.css";

function App() {
  const { data, loading, error, progress, runResearch, clearResults } =
    useResearch();
  const [apiHealthy, setApiHealthy] = React.useState(false);

  // Check API health on mount
  useEffect(() => {
    researchApi
      .checkHealth()
      .then((healthy) => setApiHealthy(healthy))
      .catch(() => setApiHealthy(false));
  }, []);

  const handleResearchSubmit = async (startupName: string) => {
    try {
      await runResearch(startupName);
    } catch (err) {
      console.error("Research failed:", err);
    }
  };

  return (
    <div className="app">
      <header className="header">
        <div className="header-content">
          <h1>VentureMind AI</h1>
          <p className="subtitle">AI-Powered Startup Due Diligence</p>
          <div className="status-indicator">
            {apiHealthy ? (
              <span className="status-ok">Backend Connected</span>
            ) : (
              <span className="status-error">Backend Disconnected</span>
            )}
          </div>
        </div>
      </header>

      <main className="main-content">
        <div className="container">
          {/* Research Form */}
          <section className="section-form">
            <h2>Research a Startup</h2>
            <ResearchForm onSubmit={handleResearchSubmit} loading={loading} />

            {/* Progress Indicator */}
            {loading && (
              <div className="progress-container">
                <div className="spinner"></div>
                <p>{progress}</p>
              </div>
            )}

            {/* Error Message */}
            {error && (
              <div className="error-message">
                <p>Error: {error}</p>
                <button onClick={clearResults}>Clear</button>
              </div>
            )}
          </section>

          {/* Results */}
          {data && (
            <section className="section-results">
              <ResearchResults data={data} />
              <button className="clear-button" onClick={clearResults}>
                New Research
              </button>
            </section>
          )}

          {/* Empty State */}
          {!loading && !data && !error && (
            <section className="empty-state">
              <h3>Enter a startup name to begin research</h3>
              <p>
                We'll analyze founders, competitors, market, funding, and
                industry intelligence.
              </p>
            </section>
          )}
        </div>
      </main>

      <footer className="footer">
        <p>VentureMind AI - Powered by Person 2 Research Intelligence</p>
      </footer>
    </div>
  );
}

export default App;
