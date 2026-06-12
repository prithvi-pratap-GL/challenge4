import { useState, useCallback } from 'react';
import { StartupAnalysis } from '../types/index';
import { mockStartupAnalysis, mockPreviousStartups } from '../services/mockData';

export const useAnalysis = () => {
  const [analyses, setAnalyses] = useState<{ [key: string]: StartupAnalysis }>({
    'airbnb-001': mockStartupAnalysis,
    'uber-001': mockPreviousStartups[0],
  });

  const submitAnalysis = useCallback(
    (data: { website_url: string; pitch_deck?: File }): string => {
      const newAnalysisId = `analysis-${Date.now()}`;
      const newAnalysis: StartupAnalysis = {
        ...mockStartupAnalysis,
        id: newAnalysisId,
        website_url: data.website_url,
        startup_name: data.website_url
          .replace('https://', '')
          .replace('http://', '')
          .split('/')[0],
      };
      setAnalyses((prev) => ({
        ...prev,
        [newAnalysisId]: newAnalysis,
      }));
      return newAnalysisId;
    },
    []
  );

  const getAnalysis = useCallback(
    (id: string): StartupAnalysis => {
      return analyses[id] || mockStartupAnalysis;
    },
    [analyses]
  );

  return { analyses, submitAnalysis, getAnalysis };
};
