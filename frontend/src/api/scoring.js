import { MOCK_DEALS } from "../data/mockDeals";

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || "";

export class EvaluationError extends Error {
  constructor(message, { status, detail } = {}) {
    super(message);
    this.name = "EvaluationError";
    this.status = status;
    this.detail = detail;
  }
}

/**
 * Calls POST /api/v1/scoring/evaluate with { deal_id }.
 * Falls back to bundled mock data when:
 *   - no API base URL is configured, or
 *   - the deal_id matches a bundled demo deal and the live request fails/404s.
 *
 * Returns the InvestmentRecommendation payload as defined in
 * backend/domain/schemas.py.
 */
export async function evaluateDeal(dealId, { signal } = {}) {
  const trimmedId = dealId.trim();
  if (!trimmedId) {
    throw new EvaluationError("Enter a deal ID to run an evaluation.");
  }

  const mock = MOCK_DEALS[trimmedId];

  if (!API_BASE_URL) {
    if (mock) return mock.recommendation;
    throw new EvaluationError(
      "No API connected. Try one of the sample deals, or set VITE_API_BASE_URL to connect a live backend.",
      { status: 0 }
    );
  }

  try {
    const response = await fetch(`${API_BASE_URL}/api/v1/scoring/evaluate`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ deal_id: trimmedId }),
      signal,
    });

    if (!response.ok) {
      let detail = null;
      try {
        const body = await response.json();
        detail = body?.detail ?? body?.message ?? null;
      } catch {
        // ignore body parse errors
      }

      if (mock) return mock.recommendation;

      throw new EvaluationError(
        response.status === 404
          ? `No analysis found for "${trimmedId}". Check the deal ID and try again.`
          : `Evaluation failed (HTTP ${response.status}).`,
        { status: response.status, detail }
      );
    }

    return await response.json();
  } catch (err) {
    if (err instanceof EvaluationError) throw err;
    if (err.name === "AbortError") throw err;

    if (mock) return mock.recommendation;

    throw new EvaluationError(
      "Could not reach the evaluation service. Confirm the API is running and reachable.",
      { status: 0, detail: err.message }
    );
  }
}

export function isMockDeal(dealId) {
  return Boolean(MOCK_DEALS[dealId?.trim()]);
}
