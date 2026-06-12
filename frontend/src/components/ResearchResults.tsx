/**
 * ResearchResults Component
 * Display research findings
 */

import React from "react";
import { ResearchResponse } from "../services/researchApi";

interface ResearchResultsProps {
  data: ResearchResponse;
}

export function ResearchResults({ data }: ResearchResultsProps) {
  return (
    <div className="research-results">
      <h2>{data.startup_name} - Research Report</h2>

      {/* Founders Section */}
      <section className="section">
        <h3>Founders ({data.founders.length})</h3>
        <div className="founders-grid">
          {data.founders.map((founder, idx) => (
            <div key={idx} className="founder-card">
              <h4>{founder.name}</h4>
              <p className="background">{founder.background}</p>
              <p className="experience">{founder.experience}</p>
              <div className="credibility">
                <span className="score">{founder.credibility_score}%</span>
                <div className="score-bar">
                  <div
                    className="score-fill"
                    style={{ width: `${founder.credibility_score}%` }}
                  ></div>
                </div>
              </div>
              <div className="sources">
                <small>{founder.sources.length} sources</small>
              </div>
            </div>
          ))}
        </div>
      </section>

      {/* Competitors Section */}
      <section className="section">
        <h3>Competitors ({data.competitors.length})</h3>
        <div className="competitors-table">
          {data.competitors.map((competitor, idx) => (
            <div key={idx} className="competitor-row">
              <div className="competitor-name">
                <h4>{competitor.name}</h4>
              </div>
              <div className="competitor-details">
                <div className="detail">
                  <label>Market Position</label>
                  <p>{competitor.market_position}</p>
                </div>
                <div className="detail">
                  <label>Funding</label>
                  <p>{competitor.funding}</p>
                </div>
                <div className="detail">
                  <label>Differentiators</label>
                  <p>{competitor.key_differentiators}</p>
                </div>
              </div>
            </div>
          ))}
        </div>
      </section>

      {/* Market Analysis */}
      <section className="section">
        <h3>Market Analysis</h3>
        <div className="analysis-box">
          {data.market_summary}
        </div>
      </section>

      {/* Funding Analysis */}
      <section className="section">
        <h3>Funding History</h3>
        <div className="analysis-box">
          {data.funding_summary}
        </div>
      </section>

      {/* Industry Analysis */}
      <section className="section">
        <h3>Industry Intelligence</h3>
        <div className="analysis-box">
          {data.industry_summary}
        </div>
      </section>

      {/* Sources */}
      <section className="section">
        <h3>Sources ({data.total_sources} total)</h3>
        <div className="sources-info">
          <p>Total sources analyzed: {data.total_sources}</p>
          <p>Enriched with full content: {data.enriched_sources.length}</p>
          <p>Generated: {new Date(data.timestamp).toLocaleString()}</p>
        </div>
      </section>
    </div>
  );
}
