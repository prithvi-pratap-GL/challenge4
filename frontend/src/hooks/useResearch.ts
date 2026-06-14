/**
 * useResearch Hook
 * Manages research state and loading for React components
 */

import { useState, useCallback } from "react";
import researchApi, { ResearchResponse } from "../services/researchApi";

interface UseResearchState {
  data: ResearchResponse | null;
  loading: boolean;
  error: string | null;
  progress: string;
}

export function useResearch() {
  const [state, setState] = useState<UseResearchState>({
    data: null,
    loading: false,
    error: null,
    progress: "",
  });

  const runResearch = useCallback(async (startupName: string) => {
    setState({
      data: null,
      loading: true,
      error: null,
      progress: "Initializing research...",
    });

    try {
      setState((prev) => ({ ...prev, progress: "Researching founders..." }));
      const result = await researchApi.runResearch(startupName);

      setState({
        data: result,
        loading: false,
        error: null,
        progress: "Research complete!",
      });

      return result;
    } catch (err) {
      const error = err instanceof Error ? err.message : "Unknown error";
      setState({
        data: null,
        loading: false,
        error,
        progress: "",
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
