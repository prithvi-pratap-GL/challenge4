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
   * Start comprehensive analysis on a startup
   */
  async runResearch(startupName: string, websiteUrl?: string, pitchDeckPath?: string): Promise<any> {
    try {
      const response = await fetch(`${API_BASE_URL}/api/v1/analysis`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          startup_name: startupName,
          website_url: websiteUrl,
          pitch_deck_path: pitchDeckPath,
        }),
      });

      if (!response.ok) {
        const error = await response.json();
        throw new Error(error.detail || "Analysis failed");
      }

      return await response.json();
    } catch (error) {
      console.error("Analysis API error:", error);
      throw error;
    }
  }

  /**
   * Get analysis status and progress
   */
  async getAnalysisStatus(analysisId: string): Promise<any> {
    try {
      const response = await fetch(`${API_BASE_URL}/api/v1/analysis/${analysisId}`);
      if (!response.ok) throw new Error("Failed to get analysis status");
      return await response.json();
    } catch (error) {
      console.error("Status check error:", error);
      throw error;
    }
  }

  /**
   * Get final report for analysis
   */
  async getFinalReport(analysisId: string): Promise<any> {
    try {
      const response = await fetch(`${API_BASE_URL}/api/v1/report/${analysisId}`);
      if (!response.ok) throw new Error("Failed to get report");
      return await response.json();
    } catch (error) {
      console.error("Report fetch error:", error);
      throw error;
    }
  }

  /**
   * Check API health
   */
  async checkHealth(): Promise<boolean> {
    try {
      const response = await fetch(`${API_BASE_URL}/api/v1/health`);
      return response.ok;
    } catch {
      return false;
    }
  }
}

export default new ResearchApiService();
