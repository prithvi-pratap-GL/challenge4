/**
 * Research API Service
 * Calls Person 2's backend research endpoints
 */

export interface Founder {
  name: string;
  background: string;
  experience: string;
  credibility_score: number;
  sources: string[];
}

export interface Competitor {
  name: string;
  market_position: string;
  funding: string;
  key_differentiators: string;
  sources: string[];
}

export interface EnrichedSource {
  url: string;
  title: string;
  source_type: string;
  content_length: number;
  status: string;
}

export interface ResearchResponse {
  startup_name: string;
  founders: Founder[];
  competitors: Competitor[];
  market_summary: string;
  funding_summary: string;
  industry_summary: string;
  total_sources: number;
  enriched_sources: EnrichedSource[];
  timestamp: string;
}

const API_BASE_URL = process.env.REACT_APP_API_URL || "http://localhost:8000";

class ResearchApiService {
  /**
   * Run comprehensive research on a startup
   */
  async runResearch(startupName: string): Promise<ResearchResponse> {
    try {
      const response = await fetch(`${API_BASE_URL}/research`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          startup_name: startupName,
          research_type: "comprehensive",
        }),
      });

      if (!response.ok) {
        const error = await response.json();
        throw new Error(error.detail || "Research failed");
      }

      return await response.json();
    } catch (error) {
      console.error("Research API error:", error);
      throw error;
    }
  }

  /**
   * Check API health
   */
  async checkHealth(): Promise<boolean> {
    try {
      const response = await fetch(`${API_BASE_URL}/health`);
      return response.ok;
    } catch {
      return false;
    }
  }

  /**
   * Get service status
   */
  async getStatus() {
    try {
      const response = await fetch(`${API_BASE_URL}/status`);
      if (!response.ok) throw new Error("Failed to get status");
      return await response.json();
    } catch (error) {
      console.error("Status check error:", error);
      throw error;
    }
  }
}

export default new ResearchApiService();
