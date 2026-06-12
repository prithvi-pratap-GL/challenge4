import React, { useState } from 'react';
import { ThumbsUp, ThumbsDown, AlertCircle } from 'lucide-react';
import { CommitteeDecision } from '../types/index';

interface CommitteeDebateProps {
  analysisId: string;
  decision: CommitteeDecision;
  onNavigate: (screen: string) => void;
}

const CommitteeDebate: React.FC<CommitteeDebateProps> = ({ analysisId, decision, onNavigate }) => {
  const [selectedTab, setSelectedTab] = useState<'bull' | 'bear' | 'red_team' | 'verdict'>(
    'bull'
  );

  const tabs = [
    { id: 'bull', label: '🐂 Bull Agent', icon: '📈' },
    { id: 'bear', label: '🐻 Bear Agent', icon: '📉' },
    { id: 'red_team', label: '🔴 Red Team', icon: '⚠️' },
    { id: 'verdict', label: '⚖️ Verdict', icon: '✓' },
  ];

  const getConfidenceColor = (confidence: number) => {
    if (confidence >= 0.8) return 'text-success';
    if (confidence >= 0.6) return 'text-warning';
    return 'text-error';
  };

  const getConfidenceBg = (confidence: number) => {
    if (confidence >= 0.8) return 'bg-success/10 border-success/30';
    if (confidence >= 0.6) return 'bg-warning/10 border-warning/30';
    return 'bg-error/10 border-error/30';
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

      <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 py-16">
        <div className="mb-12">
          <h1 className="text-4xl font-bold text-text-primary mb-2">Committee Debate</h1>
          <p className="text-text-secondary">Analysis ID: {analysisId}</p>
        </div>

        {/* Tab Navigation */}
        <div className="flex space-x-2 mb-8 overflow-x-auto">
          {tabs.map((tab) => (
            <button
              key={tab.id}
              onClick={() => setSelectedTab(tab.id as any)}
              className={`px-6 py-3 rounded-lg font-semibold whitespace-nowrap transition ${
                selectedTab === tab.id
                  ? 'bg-accent text-white shadow-sm'
                  : 'bg-bg-card text-text-secondary hover:bg-bg-light border border-border'
              }`}
            >
              {tab.icon} {tab.label}
            </button>
          ))}
        </div>

        {/* Bull Case */}
        {selectedTab === 'bull' && (
          <div className="bg-success/10 border border-success/30 rounded-lg p-8 mb-8">
            <div className="flex items-start space-x-4 mb-6">
              <div className="text-4xl">🐂</div>
              <div>
                <h2 className="text-2xl font-bold text-success">Bull Agent - Investment Case</h2>
                <p className="text-text-secondary">Why this startup is worth investing in</p>
              </div>
            </div>
            <div className="bg-bg-card rounded-lg p-6 border border-success/20">
              <p className="text-text-primary/80 whitespace-pre-wrap leading-relaxed">{decision.bull_case}</p>
            </div>
          </div>
        )}

        {/* Bear Case */}
        {selectedTab === 'bear' && (
          <div className="bg-warning/10 border border-warning/30 rounded-lg p-8 mb-8">
            <div className="flex items-start space-x-4 mb-6">
              <div className="text-4xl">🐻</div>
              <div>
                <h2 className="text-2xl font-bold text-warning">Bear Agent - Risk Case</h2>
                <p className="text-text-secondary">Why this investment carries significant risks</p>
              </div>
            </div>
            <div className="bg-bg-card rounded-lg p-6 border border-warning/20">
              <p className="text-text-primary/80 whitespace-pre-wrap leading-relaxed">{decision.bear_case}</p>
            </div>
          </div>
        )}

        {/* Red Team */}
        {selectedTab === 'red_team' && (
          <div className="bg-error/10 border border-error/30 rounded-lg p-8 mb-8">
            <div className="flex items-start space-x-4 mb-6">
              <AlertCircle className="w-8 h-8 text-error mt-1 flex-shrink-0" />
              <div>
                <h2 className="text-2xl font-bold text-error">Red Team - Challenge Analysis</h2>
                <p className="text-text-secondary">Critical feedback and blind spots identified</p>
              </div>
            </div>
            <div className="bg-bg-card rounded-lg p-6 border border-error/20">
              <p className="text-text-primary/80 whitespace-pre-wrap leading-relaxed">
                {decision.red_team_feedback}
              </p>
            </div>
          </div>
        )}

        {/* Verdict */}
        {selectedTab === 'verdict' && (
          <div className={`border rounded-lg p-8 mb-8 ${getConfidenceBg(decision.confidence)}`}>
            <div className="mb-6">
              <h2 className="text-3xl font-bold text-accent mb-4">Final Verdict</h2>

              {/* Verdict Statement */}
              <div className="bg-bg-card rounded-lg p-6 border border-border mb-6">
                <p className="text-xl text-text-primary font-semibold">{decision.verdict}</p>
              </div>

              {/* Confidence Score */}
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div className="bg-bg-card rounded-lg p-6 border border-border">
                  <p className="text-text-secondary text-sm mb-3">Confidence Level</p>
                  <div className="flex items-end space-x-4">
                    <div className={`text-4xl font-bold ${getConfidenceColor(decision.confidence)}`}>
                      {(decision.confidence * 100).toFixed(0)}%
                    </div>
                    <div className="flex-1">
                      <div className="w-full bg-bg-light rounded-full h-2 border border-border overflow-hidden">
                        <div
                          className={`h-full transition-all ${
                            decision.confidence >= 0.8
                              ? 'bg-success'
                              : decision.confidence >= 0.6
                                ? 'bg-accent'
                                : 'bg-warning'
                          }`}
                          style={{ width: `${decision.confidence * 100}%` }}
                        />
                      </div>
                    </div>
                  </div>
                </div>

                <div className="bg-bg-card rounded-lg p-6 border border-border">
                  <p className="text-text-secondary text-sm mb-4">Decision Summary</p>
                  <div className="space-y-2">
                    <div className="flex items-center space-x-2">
                      {decision.verdict.toLowerCase().includes('buy') ? (
                        <ThumbsUp className="w-5 h-5 text-success" />
                      ) : (
                        <ThumbsDown className="w-5 h-5 text-warning" />
                      )}
                      <span className="text-text-primary">
                        {decision.verdict.toLowerCase().includes('buy')
                          ? 'Positive Recommendation'
                          : 'Negative Recommendation'}
                      </span>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        )}

        {/* Navigation */}
        <div className="flex justify-between mt-12">
          <button
            onClick={() => onNavigate('progress')}
            className="btn-secondary"
          >
            ← Back to Progress
          </button>
          <button
            onClick={() => onNavigate('report')}
            className="btn-primary"
          >
            View Final Report →
          </button>
        </div>
      </div>
    </div>
  );
};

export default CommitteeDebate;
