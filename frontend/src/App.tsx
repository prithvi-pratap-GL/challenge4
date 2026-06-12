import React, { useState } from 'react';
import './App.css';
import {
  LandingPage,
  UploadStartup,
  AnalysisProgress,
  CommitteeDebate,
  FinalReport,
  DigitalTwin,
  StartupComparison,
} from './pages';
import { mockStartupAnalysis, mockPreviousStartups, mockAnalysisStatuses } from './services';
import { StartupAnalysis } from './types';

function App() {
  const [currentScreen, setCurrentScreen] = useState('landing');
  const [currentAnalysisId, setCurrentAnalysisId] = useState<string>('');
  const [analyses, setAnalyses] = useState<{ [key: string]: StartupAnalysis }>({
    'airbnb-001': mockStartupAnalysis,
    'uber-001': mockPreviousStartups[0],
  });

  const handleNavigate = (screen: string, analysisId?: string) => {
    setCurrentScreen(screen);
    if (analysisId) {
      setCurrentAnalysisId(analysisId);
    }
  };

  const handleSubmitAnalysis = (data: {
    website_url: string;
    pitch_deck?: File;
  }): string => {
    const newAnalysisId = `analysis-${Date.now()}`;
    const newAnalysis: StartupAnalysis = {
      ...mockStartupAnalysis,
      id: newAnalysisId,
      website_url: data.website_url,
      startup_name: data.website_url.replace('https://', '').replace('http://', '').split('/')[0],
    };
    setAnalyses({
      ...analyses,
      [newAnalysisId]: newAnalysis,
    });
    return newAnalysisId;
  };

  const currentAnalysis = analyses[currentAnalysisId] || mockStartupAnalysis;
  const mockStatus = mockAnalysisStatuses[0];

  return (
    <div className="App">
      {currentScreen === 'landing' && <LandingPage onNavigate={handleNavigate} />}

      {currentScreen === 'upload' && (
        <UploadStartup onNavigate={handleNavigate} onSubmit={handleSubmitAnalysis} />
      )}

      {currentScreen === 'progress' && (
        <AnalysisProgress
          analysisId={currentAnalysisId}
          onAnalysisComplete={() => handleNavigate('debate', currentAnalysisId)}
          mockStatus={mockStatus}
        />
      )}

      {currentScreen === 'debate' && (
        <CommitteeDebate
          analysisId={currentAnalysisId}
          decision={currentAnalysis.committee_decision}
          onNavigate={handleNavigate}
        />
      )}

      {currentScreen === 'report' && (
        <FinalReport
          analysisId={currentAnalysisId}
          report={currentAnalysis.final_report}
          startupName={currentAnalysis.startup_name}
          onNavigate={handleNavigate}
        />
      )}

      {currentScreen === 'digital-twin' && (
        <DigitalTwin
          analysisId={currentAnalysisId}
          startupName={currentAnalysis.startup_name}
          onNavigate={handleNavigate}
        />
      )}

      {currentScreen === 'comparison' && (
        <StartupComparison
          currentAnalysis={currentAnalysis}
          previousStartups={mockPreviousStartups}
          onNavigate={handleNavigate}
        />
      )}
    </div>
  );
}

export default App;
