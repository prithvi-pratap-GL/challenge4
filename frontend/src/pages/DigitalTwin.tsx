import React, { useState } from 'react';
import { Play } from 'lucide-react';

interface DigitalTwinProps {
  analysisId: string;
  startupName: string;
  onNavigate: (screen: string) => void;
}

const DigitalTwin: React.FC<DigitalTwinProps> = ({ analysisId, startupName, onNavigate }) => {
  const [scenario, setScenario] = useState('optimistic');
  const [customParams, setCustomParams] = useState({
    growth_rate: 0.35,
    churn_rate: 0.05,
    market_penetration: 0.15,
    unit_economics_cac: 50,
    unit_economics_ltv: 500,
  });
  const [simulationResults, setSimulationResults] = useState<any>(null);

  const scenarios = {
    optimistic: {
      label: 'Optimistic',
      description: 'Best-case scenario with high growth and low churn',
      params: {
        growth_rate: 0.5,
        churn_rate: 0.02,
        market_penetration: 0.25,
        unit_economics_cac: 40,
        unit_economics_ltv: 600,
      },
    },
    realistic: {
      label: 'Realistic',
      description: 'Expected scenario based on current market trends',
      params: {
        growth_rate: 0.35,
        churn_rate: 0.05,
        market_penetration: 0.15,
        unit_economics_cac: 50,
        unit_economics_ltv: 500,
      },
    },
    pessimistic: {
      label: 'Pessimistic',
      description: 'Conservative scenario with slower growth',
      params: {
        growth_rate: 0.15,
        churn_rate: 0.12,
        market_penetration: 0.08,
        unit_economics_cac: 70,
        unit_economics_ltv: 350,
      },
    },
  };

  const runSimulation = () => {
    const params = customParams;

    // Simulate 5-year projection
    const projections = [];
    let currentYear = new Date().getFullYear();
    let revenue = 1000000; // Starting revenue
    let users = 1000;
    let ltv = params.unit_economics_ltv;
    let cac = params.unit_economics_cac;

    for (let year = 0; year < 5; year++) {
      revenue = revenue * (1 + params.growth_rate);
      users = users * (1 + params.growth_rate) * (1 - params.churn_rate);

      projections.push({
        year: currentYear + year,
        revenue: Math.round(revenue),
        users: Math.round(users),
        ltv_cac_ratio: (ltv / cac).toFixed(2),
        burn_rate: Math.round(revenue * 0.3),
      });
    }

    setSimulationResults({
      scenario,
      params,
      projections,
      final_valuation: Math.round(revenue * 10), // Simple 10x revenue multiple
      probability_of_success: calculateSuccessProbability(params),
    });
  };

  const calculateSuccessProbability = (params: any) => {
    // Simple heuristic
    let score = 50;
    if (params.growth_rate > 0.3) score += 15;
    if (params.churn_rate < 0.08) score += 15;
    if (params.unit_economics_ltv > params.unit_economics_cac * 3) score += 10;
    return Math.min(95, score);
  };

  const handleScenarioChange = (scenarioKey: string) => {
    setScenario(scenarioKey);
    const newParams = scenarios[scenarioKey as keyof typeof scenarios].params;
    setCustomParams(newParams);
  };

  return (
    <div className="min-h-screen bg-bg-light">
      <nav className="sticky top-0 z-50 bg-white border-b border-border shadow-xs">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
          <button
            onClick={() => onNavigate('landing')}
            className="text-2xl font-bold text-accent hover:opacity-80 transition tracking-wide"
          >
            ✦ VentureMind AI
          </button>
        </div>
      </nav>

      <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 py-16">
        <div className="mb-12">
          <h1 className="text-4xl font-bold text-text-primary mb-2">
            Digital Twin: <span className="text-accent">{startupName}</span>
          </h1>
          <p className="text-text-secondary">What-if scenario analysis and financial projections</p>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* Scenario Selector */}
          <div className="lg:col-span-1">
            <h2 className="text-xl font-bold text-text-primary mb-6">Scenarios</h2>
            <div className="space-y-3">
              {Object.entries(scenarios).map(([key, data]) => (
                <button
                  key={key}
                  onClick={() => handleScenarioChange(key)}
                  className={`w-full text-left p-4 rounded-lg transition border ${
                    scenario === key
                      ? 'bg-accent text-white shadow-sm'
                      : 'bg-bg-card border-border hover:bg-bg-light'
                  }`}
                >
                  <p className="font-semibold text-text-primary">{data.label}</p>
                  <p className="text-sm text-text-secondary mt-1">{data.description}</p>
                </button>
              ))}
            </div>

            {/* Run Simulation Button */}
            <button
              onClick={runSimulation}
              className="btn-primary w-full mt-6 flex items-center justify-center space-x-2"
            >
              <Play className="w-5 h-5" />
              <span>Run Simulation</span>
            </button>
          </div>

          {/* Parameters */}
          <div className="lg:col-span-2">
            <h2 className="text-xl font-bold text-text-primary mb-6">Parameters</h2>
            <div className="card bg-bg-card space-y-6">
              {/* Growth Rate */}
              <div>
                <label className="block text-text-primary font-semibold mb-3">
                  Annual Growth Rate
                </label>
                <div className="flex items-center space-x-4">
                  <input
                    type="range"
                    min="0"
                    max="1"
                    step="0.05"
                    value={customParams.growth_rate}
                    onChange={(e) =>
                      setCustomParams({
                        ...customParams,
                        growth_rate: parseFloat(e.target.value),
                      })
                    }
                    className="flex-1"
                  />
                  <span className="text-accent font-bold text-lg w-16">
                    {(customParams.growth_rate * 100).toFixed(0)}%
                  </span>
                </div>
              </div>

              {/* Churn Rate */}
              <div>
                <label className="block text-text-primary font-semibold mb-3">Monthly Churn Rate</label>
                <div className="flex items-center space-x-4">
                  <input
                    type="range"
                    min="0"
                    max="0.3"
                    step="0.01"
                    value={customParams.churn_rate}
                    onChange={(e) =>
                      setCustomParams({
                        ...customParams,
                        churn_rate: parseFloat(e.target.value),
                      })
                    }
                    className="flex-1"
                  />
                  <span className="text-warning font-bold text-lg w-16">
                    {(customParams.churn_rate * 100).toFixed(1)}%
                  </span>
                </div>
              </div>

              {/* Market Penetration */}
              <div>
                <label className="block text-text-primary font-semibold mb-3">
                  Market Penetration (5yr)
                </label>
                <div className="flex items-center space-x-4">
                  <input
                    type="range"
                    min="0"
                    max="0.5"
                    step="0.01"
                    value={customParams.market_penetration}
                    onChange={(e) =>
                      setCustomParams({
                        ...customParams,
                        market_penetration: parseFloat(e.target.value),
                      })
                    }
                    className="flex-1"
                  />
                  <span className="text-success font-bold text-lg w-16">
                    {(customParams.market_penetration * 100).toFixed(1)}%
                  </span>
                </div>
              </div>

              {/* CAC */}
              <div>
                <label className="block text-text-primary font-semibold mb-3">
                  Customer Acquisition Cost
                </label>
                <div className="flex items-center space-x-4">
                  <input
                    type="range"
                    min="20"
                    max="200"
                    step="10"
                    value={customParams.unit_economics_cac}
                    onChange={(e) =>
                      setCustomParams({
                        ...customParams,
                        unit_economics_cac: parseFloat(e.target.value),
                      })
                    }
                    className="flex-1"
                  />
                  <span className="text-accent font-bold text-lg w-16">
                    ${customParams.unit_economics_cac}
                  </span>
                </div>
              </div>

              {/* LTV */}
              <div>
                <label className="block text-text-primary font-semibold mb-3">
                  Lifetime Value
                </label>
                <div className="flex items-center space-x-4">
                  <input
                    type="range"
                    min="100"
                    max="1000"
                    step="50"
                    value={customParams.unit_economics_ltv}
                    onChange={(e) =>
                      setCustomParams({
                        ...customParams,
                        unit_economics_ltv: parseFloat(e.target.value),
                      })
                    }
                    className="flex-1"
                  />
                  <span className="text-success font-bold text-lg w-16">
                    ${customParams.unit_economics_ltv}
                  </span>
                </div>
              </div>

              {/* Unit Economics Ratio */}
              <div className="bg-bg-light rounded-lg p-4 border border-border">
                <p className="text-text-secondary text-sm mb-2">LTV:CAC Ratio</p>
                <p className="text-2xl font-bold text-text-primary">
                  {(customParams.unit_economics_ltv / customParams.unit_economics_cac).toFixed(1)}
                  <span className="text-sm text-text-secondary ml-2">
                    {customParams.unit_economics_ltv / customParams.unit_economics_cac > 3
                      ? '✓ Healthy'
                      : '⚠ Below Target'}
                  </span>
                </p>
              </div>
            </div>
          </div>
        </div>

        {/* Simulation Results */}
        {simulationResults && (
          <div className="mt-12">
            <h2 className="text-2xl font-bold text-text-primary mb-6">Simulation Results</h2>

            {/* Key Metrics */}
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-8">
              <div className="card bg-success/10">
                <p className="text-text-secondary text-sm mb-3">Projected 5-Year Valuation</p>
                <p className="text-3xl font-bold text-success">
                  ${(simulationResults.final_valuation / 1000000).toFixed(1)}M
                </p>
              </div>
              <div className="card bg-accent/10">
                <p className="text-text-secondary text-sm mb-3">Success Probability</p>
                <p className="text-3xl font-bold text-accent">
                  {simulationResults.probability_of_success}%
                </p>
              </div>
            </div>

            {/* Projections Table */}
            <div className="card bg-bg-card overflow-hidden">
              <div className="overflow-x-auto">
                <table className="w-full">
                  <thead className="bg-bg-light border-b border-border">
                    <tr>
                      <th className="px-6 py-4 text-left text-text-primary font-semibold">Year</th>
                      <th className="px-6 py-4 text-left text-text-primary font-semibold">Revenue</th>
                      <th className="px-6 py-4 text-left text-text-primary font-semibold">Users</th>
                      <th className="px-6 py-4 text-left text-text-primary font-semibold">LTV:CAC</th>
                      <th className="px-6 py-4 text-left text-text-primary font-semibold">Burn Rate</th>
                    </tr>
                  </thead>
                  <tbody className="divide-y divide-border">
                    {simulationResults.projections.map((proj: any, idx: number) => (
                      <tr key={idx} className="hover:bg-bg-light transition">
                        <td className="px-6 py-4 text-text-primary/80">{proj.year}</td>
                        <td className="px-6 py-4 text-text-primary">${(proj.revenue / 1000000).toFixed(1)}M</td>
                        <td className="px-6 py-4 text-text-primary">{(proj.users / 1000).toFixed(0)}K</td>
                        <td className="px-6 py-4">
                          <span
                            className={
                              proj.ltv_cac_ratio > 3 ? 'text-success' : 'text-accent'
                            }
                          >
                            {proj.ltv_cac_ratio}
                          </span>
                        </td>
                        <td className="px-6 py-4 text-text-primary/80">${(proj.burn_rate / 1000).toFixed(0)}K</td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>
          </div>
        )}

        {/* Navigation */}
        <div className="flex justify-between mt-12 pt-8 border-t border-border">
          <button
            onClick={() => onNavigate('report')}
            className="btn-secondary"
          >
            ← Back to Report
          </button>
          <button
            onClick={() => onNavigate('comparison')}
            className="btn-primary flex items-center space-x-2"
          >
            <span>Compare Startups</span>
          </button>
        </div>
      </div>
    </div>
  );
};

export default DigitalTwin;
