import { useCallback } from 'react';

export type ScreenType = 'landing' | 'upload' | 'progress' | 'debate' | 'report' | 'digital-twin' | 'comparison';

interface UseNavigationReturn {
  navigate: (screen: ScreenType, analysisId?: string) => void;
}

export const useNavigation = (
  setCurrentScreen: (screen: ScreenType) => void,
  setCurrentAnalysisId: (id: string) => void
): UseNavigationReturn => {
  const navigate = useCallback(
    (screen: ScreenType, analysisId?: string) => {
      setCurrentScreen(screen);
      if (analysisId) {
        setCurrentAnalysisId(analysisId);
      }
    },
    [setCurrentScreen, setCurrentAnalysisId]
  );

  return { navigate };
};
