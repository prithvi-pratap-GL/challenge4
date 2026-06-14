/**
 * useResearch Hook
 * Manages research state and loading for React components
 */

import { useState, useCallback } from "react";
import researchApi, { ResearchResponse } from "../services/researchApi";

interface UseResearchState {
  data: any | null;
  loading: boolean;
  error: string | null;
  progress: string;
  analysisId: string | null;
}

export function useResearch() {
  const [state, setState] = useState<UseResearchState>({
    data: null,
    loading: false,
    error: null,
    progress: "",
    analysisId: null,
  });

  const runResearch = useCallback(async (startupName: string, websiteUrl?: string, pitchDeckPath?: string) => {
    setState({
      data: null,
      loading: true,
      error: null,
      progress: "Starting analysis...",
      analysisId: null,
    });

    try {
      const result = await researchApi.runResearch(startupName, websiteUrl, pitchDeckPath);
      const analysisId = result.id;

      setState({
        data: result,
        loading: false,
        error: null,
        progress: "Analysis started",
        analysisId,
      });

      // Poll for status
      let isComplete = false;
      let pollCount = 0;
      while (!isComplete && pollCount < 120) {
        await new Promise(resolve => setTimeout(resolve, 1000));
        const status = await researchApi.getAnalysisStatus(analysisId);

        setState((prev) => ({
          ...prev,
          progress: `${status.current_agent} - ${status.progress}%`,
        }));

        if (status.status === "completed") {
          const report = await researchApi.getFinalReport(analysisId);
          setState({
            data: report,
            loading: false,
            error: null,
            progress: "Analysis complete!",
            analysisId,
          });
          isComplete = true;
        }
        pollCount++;
      }

      return result;
    } catch (err) {
      const error = err instanceof Error ? err.message : "Unknown error";
      setState({
        data: null,
        loading: false,
        error,
        progress: "",
        analysisId: null,
      });
      throw err;
    }
  }, []);

  const clearResults = useCallback(() => {
    setState({
      data: null,
      loading: false,
      error: null,
      progress: "",
    });
  }, []);

  return {
    ...state,
    runResearch,
    clearResults,
  };
}
