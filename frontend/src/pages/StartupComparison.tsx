import React, { useState } from 'react';
import { BarChart3 } from 'lucide-react';
import { StartupAnalysis } from '../types/index';

interface StartupComparisonProps {
  previousStartups: StartupAnalysis[];
  currentAnalysis: StartupAnalysis;
  onNavigate: (screen: string) => void;
}

const StartupComparison: React.FC<StartupComparisonProps> = ({
  previousStartups,
  currentAnalysis,
  onNavigate,
}) => {
  const [selectedStartups, setSelectedStartups] = useState<string[]>([currentAnalysis.id]);

  const allStartups = [currentAnalysis, ...previousStartups];

  const handleStartupToggle = (id: string) => {
    setSelectedStartups((prev) =>
      prev.includes(id) ? prev.filter((s) => s !== id) : [...prev, id]
    );
  };

  const comparisonData = allStartups.filter((s) => selectedStartups.includes(s.id));

  const getScoreColor = (score: number) => {
    if (score >= 8) return 'bg-success/10 text-success';
    if (score >= 6) return 'bg-warning/10 text-warning';
    return 'bg-error/10 text-error';
  };

  return (
    <div className="min-h-screen bg-bg-light">
      <nav className="sticky top-0 z-50 bg-white border-b border-border shadow-xs">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
          <button
            onClick={() => onNavigate('landing')}
            className="text-2xl font-bold text-accent hover:opacity-80 transition tracking-wide"
          >
            ✦ VentureMind AI
          </button>
        </div>
      </nav>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-16">
        <div className="mb-12">
          <h1 className="text-4xl font-bold text-text-primary mb-2">Startup Comparison</h1>
          <p className="text-text-secondary">Compare multiple startup analyses side-by-side</p>
        </div>

        {/* Startup Selection */}
        <div className="card bg-bg-card mb-12">
          <h2 className="text-xl font-bold text-text-primary mb-6">Select Startups to Compare</h2>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            {allStartups.map((startup) => (
              <button
                key={startup.id}
                onClick={() => handleStartupToggle(startup.id)}
                className={`p-4 rounded-lg border-2 transition text-left ${
                  selectedStartups.includes(startup.id)
                    ? 'border-accent bg-accent/10'
                    : 'border-border bg-bg-light hover:bg-bg-light/80'
                }`}
              >
                <div className="flex items-center justify-between">
                  <div>
                    <p className="font-semibold text-text-primary">{startup.startup_name}</p>
                    <p className="text-sm text-text-secondary">{startup.website_url}</p>
                  </div>
                  {selectedStartups.includes(startup.id) && (
                    <span className="text-accent font-bold">✓</span>
                  )}
                </div>
              </button>
            ))}
          </div>
        </div>

        {/* Comparison Table */}
        {comparisonData.length > 0 && (
          <>
            {/* Scores */}
            <div className="card bg-bg-card mb-8">
              <h2 className="text-xl font-bold text-text-primary mb-6 flex items-center space-x-2">
                <BarChart3 className="w-6 h-6 text-accent" />
                <span>Score Comparison</span>
              </h2>

              <div className="overflow-x-auto">
                <table className="w-full">
                  <thead className="border-b border-border">
                    <tr>
                      <th className="px-4 py-3 text-left text-text-secondary font-semibold">Metric</th>
                      {comparisonData.map((startup) => (
                        <th
                          key={startup.id}
                          className="px-4 py-3 text-center text-text-primary font-semibold"
                        >
                          {startup.startup_name}
                        </th>
                      ))}
                    </tr>
                  </thead>
                  <tbody className="divide-y divide-border">
                    {/* Founder Score */}
                    <tr className="hover:bg-bg-light transition">
                      <td className="px-4 py-4 text-text-secondary font-semibold">Founder Score</td>
                      {comparisonData.map((startup) => (
                        <td
                          key={startup.id}
                          className="px-4 py-4 text-center"
                        >
                          <span
                            className={`badge ${getScoreColor(
                              startup.final_report.founder_score
                            )}`}
                          >
                            {startup.final_report.founder_score.toFixed(1)}/10
                          </span>
                        </td>
                      ))}
                    </tr>

                    {/* Market Score */}
                    <tr className="hover:bg-bg-light transition">
                      <td className="px-4 py-4 text-text-secondary font-semibold">Market Score</td>
                      {comparisonData.map((startup) => (
                        <td key={startup.id} className="px-4 py-4 text-center">
                          <span
                            className={`badge ${getScoreColor(
                              startup.final_report.market_score
                            )}`}
                          >
                            {startup.final_report.market_score.toFixed(1)}/10
                          </span>
                        </td>
                      ))}
                    </tr>

                    {/* Risk Score */}
                    <tr className="hover:bg-bg-light transition">
                      <td className="px-4 py-4 text-text-secondary font-semibold">Risk Score (0=safe)</td>
                      {comparisonData.map((startup) => (
                        <td key={startup.id} className="px-4 py-4 text-center">
                          <span
                            className={`badge ${
                              startup.final_report.risk_score <= 3
                                ? 'badge-success'
                                : startup.final_report.risk_score <= 6
                                  ? 'bg-accent/10 text-accent'
                                  : 'badge-warning'
                            }`}
                          >
                            {startup.final_report.risk_score.toFixed(1)}/10
                          </span>
                        </td>
                      ))}
                    </tr>

                    {/* Recommendation */}
                    <tr className="hover:bg-bg-light transition">
                      <td className="px-4 py-4 text-text-secondary font-semibold">Recommendation</td>
                      {comparisonData.map((startup) => (
                        <td key={startup.id} className="px-4 py-4 text-center">
                          <span
                            className={`badge ${
                              startup.final_report.recommendation.toLowerCase().includes('buy')
                                ? 'badge-success'
                                : 'badge-warning'
                            }`}
                          >
                            {startup.final_report.recommendation.includes('STRONG')
                              ? '✓ Buy'
                              : startup.final_report.recommendation.includes('BUY')
                                ? 'Buy'
                                : 'Pass'}
                          </span>
                        </td>
                      ))}
                    </tr>

                    {/* Committee Confidence */}
                    <tr className="hover:bg-bg-light transition">
                      <td className="px-4 py-4 text-text-secondary font-semibold">Committee Confidence</td>
                      {comparisonData.map((startup) => (
                        <td key={startup.id} className="px-4 py-4 text-center">
                          <span className="text-text-primary font-bold">
                            {(startup.committee_decision.confidence * 100).toFixed(0)}%
                          </span>
                        </td>
                      ))}
                    </tr>
                  </tbody>
                </table>
              </div>
            </div>

            {/* Detailed Metrics */}
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-12">
              {/* Founders */}
              <div className="card bg-bg-card">
                <h3 className="text-lg font-bold text-text-primary mb-4">Founder Teams</h3>
                <div className="space-y-6">
                  {comparisonData.map((startup) => (
                    <div key={startup.id} className="border-t border-border pt-4 first:border-t-0 first:pt-0">
                      <p className="text-accent font-semibold mb-2">{startup.startup_name}</p>
                      <div className="space-y-1 text-sm">
                        {startup.research_data.founders.map((founder, idx) => (
                          <p key={idx} className="text-text-secondary">
                            {founder.name} - {founder.role}
                          </p>
                        ))}
                      </div>
                    </div>
                  ))}
                </div>
              </div>

              {/* Competitors */}
              <div className="card bg-bg-card">
                <h3 className="text-lg font-bold text-text-primary mb-4">Competitor Count</h3>
                <div className="space-y-4">
                  {comparisonData.map((startup) => (
                    <div
                      key={startup.id}
                      className="flex items-center justify-between p-4 bg-bg-light rounded-lg border border-border"
                    >
                      <span className="text-text-primary">{startup.startup_name}</span>
                      <span className="text-accent font-bold">
                        {startup.research_data.competitors.length} competitors
                      </span>
                    </div>
                  ))}
                </div>
              </div>
            </div>

            {/* Summary */}
            <div className="card bg-accent/10 mb-12">
              <h3 className="text-lg font-bold text-text-primary mb-4">Comparison Summary</h3>
              <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                <div>
                  <p className="text-text-secondary text-sm mb-2">Highest Founder Score</p>
                  <p className="text-text-primary font-bold">
                    {
                      comparisonData.reduce((prev, curr) =>
                        curr.final_report.founder_score > prev.final_report.founder_score
                          ? curr
                          : prev
                      ).startup_name
                    }
                  </p>
                </div>
                <div>
                  <p className="text-text-secondary text-sm mb-2">Strongest Market</p>
                  <p className="text-text-primary font-bold">
                    {
                      comparisonData.reduce((prev, curr) =>
                        curr.final_report.market_score > prev.final_report.market_score
                          ? curr
                          : prev
                      ).startup_name
                    }
                  </p>
                </div>
                <div>
                  <p className="text-text-secondary text-sm mb-2">Lowest Risk</p>
                  <p className="text-text-primary font-bold">
                    {
                      comparisonData.reduce((prev, curr) =>
                        curr.final_report.risk_score < prev.final_report.risk_score
                          ? curr
                          : prev
                      ).startup_name
                    }
                  </p>
                </div>
              </div>
            </div>
          </>
        )}

        {/* Navigation */}
        <div className="flex justify-between pt-8 border-t border-border">
          <button
            onClick={() => onNavigate('digital-twin')}
            className="btn-secondary"
          >
            ← Back
          </button>
          <button
            onClick={() => onNavigate('landing')}
            className="btn-primary"
          >
            Return to Home
          </button>
        </div>
      </div>
    </div>
  );
};

export default StartupComparison;
