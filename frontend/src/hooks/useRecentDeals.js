import { useCallback, useEffect, useState } from "react";

const STORAGE_KEY = "venturemind.recent-deals";
const MAX_RECENT = 12;

function load() {
  try {
    const raw = window.localStorage.getItem(STORAGE_KEY);
    if (!raw) return [];
    const parsed = JSON.parse(raw);
    return Array.isArray(parsed) ? parsed : [];
  } catch {
    return [];
  }
}

function persist(items) {
  try {
    window.localStorage.setItem(STORAGE_KEY, JSON.stringify(items));
  } catch {
    // localStorage unavailable (private mode, etc.) - fail silently
  }
}

/**
 * Tracks recently-evaluated deals for the sidebar history rail.
 * Each entry: { dealId, status, aggregateHealth, evaluatedAt }
 */
export function useRecentDeals() {
  const [recent, setRecent] = useState(() => load());

  useEffect(() => {
    persist(recent);
  }, [recent]);

  const recordEvaluation = useCallback((entry) => {
    setRecent((prev) => {
      const withoutCurrent = prev.filter((item) => item.dealId !== entry.dealId);
      const next = [{ ...entry, evaluatedAt: Date.now() }, ...withoutCurrent];
      return next.slice(0, MAX_RECENT);
    });
  }, []);

  const removeDeal = useCallback((dealId) => {
    setRecent((prev) => prev.filter((item) => item.dealId !== dealId));
  }, []);

  const clearAll = useCallback(() => setRecent([]), []);

  return { recent, recordEvaluation, removeDeal, clearAll };
}
