export interface Founder {
  name: string;
  role: string;
  experience: string;
  education: string;
}

export interface Competitor {
  name: string;
  market_cap?: string;
  funding?: string;
  description: string;
}

export interface ResearchOutput {
  founders: Founder[];
  competitors: Competitor[];
  market_analysis: string;
}

export interface RagOutput {
  context: string;
  sources: string[];
}

export interface CommitteeDecision {
  bull_case: string;
  bear_case: string;
  red_team_feedback: string;
  verdict: string;
  confidence: number;
}

export interface FinalReport {
  founder_score: number;
  market_score: number;
  risk_score: number;
  recommendation: string;
  report: string;
}

export interface AnalysisStatus {
  id: string;
  status: 'submitted' | 'research' | 'rag' | 'committee' | 'red_team' | 'final' | 'completed';
  current_agent: string;
  progress: number;
  startup_name?: string;
}

export interface StartupAnalysis {
  id: string;
  startup_name: string;
  website_url: string;
  pitch_deck_url?: string;
  research_data: ResearchOutput;
  rag_data: RagOutput;
  committee_decision: CommitteeDecision;
  final_report: FinalReport;
  created_at: string;
}
