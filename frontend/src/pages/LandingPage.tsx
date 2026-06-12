import React from 'react';
import { ArrowRight, BarChart3, Brain, Zap, TrendingUp, Shield } from 'lucide-react';

interface LandingPageProps {
  onNavigate: (screen: string) => void;
}

const LandingPage: React.FC<LandingPageProps> = ({ onNavigate }) => {
  return (
    <div className="min-h-screen bg-bg-light">
      {/* Navigation */}
      <nav className="sticky top-0 z-50 bg-bg-card border-b border-border shadow-sm backdrop-blur-sm bg-opacity-95">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4 flex justify-between items-center">
          <div className="text-2xl font-bold text-primary">VentureMind AI</div>
          <div className="text-sm font-medium text-text-tertiary">AI-Powered Startup Analysis</div>
        </div>
      </nav>

      {/* Hero Section */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-20">
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-16 items-center">
          {/* Left Content */}
          <div>
            <h1 className="text-6xl lg:text-7xl font-bold text-primary mb-6 leading-tight">
              Investment Due Diligence at Scale
            </h1>
            <p className="text-xl text-text-secondary mb-8 leading-relaxed font-light">
              Enterprise-grade AI analysis for startup evaluation. Get comprehensive investment recommendations in 30 minutes.
            </p>

            <div className="space-y-3 mb-10">
              <div className="flex items-start space-x-3">
                <div className="flex-shrink-0 w-6 h-6 mt-1">
                  <Brain className="w-6 h-6 text-accent" />
                </div>
                <div>
                  <p className="font-semibold text-primary">Multi-Agent Intelligence</p>
                  <p className="text-sm text-text-secondary">Bull, bear, and red team perspectives</p>
                </div>
              </div>
              <div className="flex items-start space-x-3">
                <div className="flex-shrink-0 w-6 h-6 mt-1">
                  <BarChart3 className="w-6 h-6 text-success" />
                </div>
                <div>
                  <p className="font-semibold text-primary">Data-Driven Analysis</p>
                  <p className="text-sm text-text-secondary">50M+ data points analyzed daily</p>
                </div>
              </div>
              <div className="flex items-start space-x-3">
                <div className="flex-shrink-0 w-6 h-6 mt-1">
                  <Shield className="w-6 h-6 text-warning" />
                </div>
                <div>
                  <p className="font-semibold text-primary">Risk Assessment</p>
                  <p className="text-sm text-text-secondary">Comprehensive red flag identification</p>
                </div>
              </div>
            </div>

            <div className="flex gap-4">
              <button
                onClick={() => onNavigate('upload')}
                className="btn-accent px-8 py-4 text-lg font-semibold flex items-center gap-2"
              >
                Start Analysis
                <ArrowRight className="w-5 h-5" />
              </button>
              <button className="btn-secondary px-8 py-4 text-lg font-semibold">
                View Demo
              </button>
            </div>
          </div>

          {/* Right Features */}
          <div className="space-y-4">
            <div className="card hover:shadow-lg">
              <div className="flex items-start gap-4">
                <div className="w-12 h-12 rounded-lg bg-accent/10 flex items-center justify-center flex-shrink-0">
                  <Brain className="w-6 h-6 text-accent" />
                </div>
                <div>
                  <h3 className="font-semibold text-primary mb-1">Research Engine</h3>
                  <p className="text-sm text-text-secondary">Automated founder, competitor, and market analysis</p>
                </div>
              </div>
            </div>

            <div className="card hover:shadow-lg">
              <div className="flex items-start gap-4">
                <div className="w-12 h-12 rounded-lg bg-success/10 flex items-center justify-center flex-shrink-0">
                  <TrendingUp className="w-6 h-6 text-success" />
                </div>
                <div>
                  <h3 className="font-semibold text-primary mb-1">Committee Debate</h3>
                  <p className="text-sm text-text-secondary">AI agents argue both sides of the investment</p>
                </div>
              </div>
            </div>

            <div className="card hover:shadow-lg">
              <div className="flex items-start gap-4">
                <div className="w-12 h-12 rounded-lg bg-warning/10 flex items-center justify-center flex-shrink-0">
                  <Zap className="w-6 h-6 text-warning" />
                </div>
                <div>
                  <h3 className="font-semibold text-primary mb-1">Digital Twin</h3>
                  <p className="text-sm text-text-secondary">Scenario modeling and sensitivity analysis</p>
                </div>
              </div>
            </div>

            <div className="card hover:shadow-lg">
              <div className="flex items-start gap-4">
                <div className="w-12 h-12 rounded-lg bg-accent/10 flex items-center justify-center flex-shrink-0">
                  <BarChart3 className="w-6 h-6 text-accent" />
                </div>
                <div>
                  <h3 className="font-semibold text-primary mb-1">Final Report</h3>
                  <p className="text-sm text-text-secondary">Investment recommendation with confidence scoring</p>
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* Stats Section */}
        <div className="mt-24 grid grid-cols-3 gap-8">
          <div className="card text-center">
            <div className="text-4xl font-bold text-accent mb-2">50M+</div>
            <p className="text-text-secondary font-medium">Data Points Analyzed</p>
          </div>
          <div className="card text-center">
            <div className="text-4xl font-bold text-success mb-2">5</div>
            <p className="text-text-secondary font-medium">AI Agents in Debate</p>
          </div>
          <div className="card text-center">
            <div className="text-4xl font-bold text-warning mb-2">30min</div>
            <p className="text-text-secondary font-medium">Complete Analysis</p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default LandingPage;
