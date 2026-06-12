import React, { useState, useEffect } from 'react';
import { CheckCircle, Clock, Zap } from 'lucide-react';
import { AnalysisStatus } from '../types/index';

interface AnalysisProgressProps {
  analysisId: string;
  onAnalysisComplete: () => void;
  mockStatus?: AnalysisStatus;
}

const AnalysisProgress: React.FC<AnalysisProgressProps> = ({
  analysisId,
  onAnalysisComplete,
  mockStatus,
}) => {
  const [status, setStatus] = useState<AnalysisStatus>(
    mockStatus || {
      id: analysisId,
      status: 'research',
      current_agent: 'Research Agent',
      progress: 0,
      startup_name: 'Startup',
    }
  );

  const stages = [
    { key: 'research', label: 'Research', icon: '🔍' },
    { key: 'rag', label: 'RAG & Context', icon: '📚' },
    { key: 'committee', label: 'Committee Debate', icon: '🤝' },
    { key: 'red_team', label: 'Red Team Challenge', icon: '🔴' },
    { key: 'final', label: 'Final Report', icon: '📄' },
    { key: 'completed', label: 'Completed', icon: '✓' },
  ];

  useEffect(() => {
    // Simulate progress
    const interval = setInterval(() => {
      setStatus((prev) => {
        let nextProgress = prev.progress + 1;
        let nextStatus = prev.status;
        let nextAgent = prev.current_agent;

        if (nextProgress > 100) {
          nextProgress = 100;
          nextStatus = 'completed';
          nextAgent = 'All Complete';
        } else if (nextProgress > 80) {
          nextStatus = 'final';
          nextAgent = 'Report Generator';
        } else if (nextProgress > 60) {
          nextStatus = 'red_team';
          nextAgent = 'Red Team Agent';
        } else if (nextProgress > 40) {
          nextStatus = 'committee';
          nextAgent = 'Bull & Bear Agents';
        } else if (nextProgress > 20) {
          nextStatus = 'rag';
          nextAgent = 'RAG Agent';
        }

        return {
          ...prev,
          progress: nextProgress,
          status: nextStatus,
          current_agent: nextAgent,
        };
      });
    }, 500);

    return () => clearInterval(interval);
  }, []);

  useEffect(() => {
    if (status.status === 'completed') {
      setTimeout(() => onAnalysisComplete(), 2000);
    }
  }, [status.status, onAnalysisComplete]);

  const getCurrentStageIndex = () => {
    return Math.min(Math.floor(status.progress / 17), stages.length - 1);
  };

  const currentStageIndex = getCurrentStageIndex();

  return (
    <div className="min-h-screen bg-bg-light">
      <nav className="sticky top-0 z-50 bg-white border-b border-border shadow-xs">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
          <div className="text-3xl font-bold text-accent tracking-wide">
            ✦ VentureMind AI - Analysis
          </div>
        </div>
      </nav>

      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-24">
        {/* Startup Info */}
        <div className="card bg-bg-card mb-12">
          <h1 className="text-4xl font-bold text-text-primary mb-2">
            Analyzing: <span className="text-accent">{status.startup_name}</span>
          </h1>
          <p className="text-text-secondary text-sm">ID: {analysisId}</p>
        </div>

        {/* Progress Bar */}
        <div className="mb-12">
          <div className="flex justify-between items-center mb-4">
            <div>
              <p className="text-text-primary font-semibold text-base">Overall Progress</p>
              <p className="text-text-secondary text-sm">{status.current_agent}</p>
            </div>
            <div className="text-right">
              <div className="text-4xl font-bold text-accent">{status.progress}%</div>
              <div className="text-sm text-text-secondary">
                {status.status === 'completed' ? 'Complete!' : 'In progress...'}
              </div>
            </div>
          </div>
          <div className="w-full bg-bg-card rounded-full h-4 border border-border overflow-hidden shadow-xs">
            <div
              className="bg-accent h-full transition-all duration-300"
              style={{ width: `${status.progress}%` }}
            />
          </div>
        </div>

        {/* Stage Timeline */}
        <div className="space-y-4 mb-12">
          {stages.map((stage, index) => {
            const isCompleted = index < currentStageIndex;
            const isCurrent = index === currentStageIndex;

            return (
              <div
                key={stage.key}
                className={`flex items-center space-x-4 p-4 rounded-lg transition ${
                  isCompleted
                    ? 'bg-success/10 border border-success/30'
                    : isCurrent
                      ? 'bg-accent/10 border border-accent/30'
                      : 'bg-bg-card border border-border'
                }`}
              >
                <div className="text-2xl">{stage.icon}</div>
                <div className="flex-1">
                  <p
                    className={`font-semibold ${
                      isCompleted
                        ? 'text-success'
                        : isCurrent
                          ? 'text-accent'
                          : 'text-text-secondary'
                    }`}
                  >
                    {stage.label}
                  </p>
                </div>
                <div>
                  {isCompleted ? (
                    <CheckCircle className="w-6 h-6 text-success" />
                  ) : isCurrent ? (
                    <Zap className="w-6 h-6 text-accent animate-pulse" />
                  ) : (
                    <Clock className="w-6 h-6 text-text-tertiary" />
                  )}
                </div>
              </div>
            );
          })}
        </div>

        {/* Status Cards */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div className="card bg-bg-card">
            <p className="text-text-secondary text-sm">Current Stage</p>
            <p className="text-text-primary font-semibold text-xl mt-3">
              {stages[currentStageIndex].label}
            </p>
          </div>
          <div className="card bg-bg-card">
            <p className="text-text-secondary text-sm">Estimated Time Remaining</p>
            <p className="text-success font-semibold text-xl mt-3">
              ~{Math.max(1, Math.round((100 - status.progress) / 2))} seconds
            </p>
          </div>
        </div>

        {/* Animation */}
        <div className="mt-12 text-center">
          <div className="inline-flex space-x-2">
            <div className="w-2 h-2 bg-accent rounded-full animate-bounce" />
            <div className="w-2 h-2 bg-success rounded-full animate-bounce" style={{ animationDelay: '0.1s' }} />
            <div className="w-2 h-2 bg-warning rounded-full animate-bounce" style={{ animationDelay: '0.2s' }} />
          </div>
        </div>
      </div>
    </div>
  );
};

export default AnalysisProgress;
