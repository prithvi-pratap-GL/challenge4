import React from 'react';
import { getScoreColorClass } from '../utils/formatters';

interface ScoreCardProps {
  label: string;
  score: number;
  max?: number;
  theme?: 'blue' | 'green' | 'orange';
  description?: string;
}

const ScoreCard: React.FC<ScoreCardProps> = ({
  label,
  score,
  max = 10,
  theme = 'blue',
  description,
}) => {
  const percentage = (score / max) * 100;

  const themeBg = {
    blue: 'bg-blue-500/10 border-blue-500/30',
    green: 'bg-green-500/10 border-green-500/30',
    orange: 'bg-orange-500/10 border-orange-500/30',
  };

  return (
    <div className={`${themeBg[theme]} border rounded-lg p-6`}>
      <p className="text-gray-400 text-sm mb-2">{label}</p>
      <div className="flex items-end justify-between">
        <div>
          <p className={`text-4xl font-bold ${getScoreColorClass(score)}`}>
            {score.toFixed(1)}
          </p>
          <p className="text-gray-500 text-sm mt-2">out of {max}</p>
        </div>
        <div className="flex-1 ml-4">
          <div className="w-full bg-gray-800/50 rounded-full h-3 border border-gray-700/30 overflow-hidden">
            <div
              className={`h-full transition-all ${
                theme === 'blue'
                  ? 'bg-gradient-to-r from-blue-500 to-blue-400'
                  : theme === 'green'
                    ? 'bg-gradient-to-r from-green-500 to-green-400'
                    : 'bg-gradient-to-r from-orange-500 to-orange-400'
              }`}
              style={{ width: `${percentage}%` }}
            />
          </div>
        </div>
      </div>
      {description && <p className="text-gray-400 text-sm mt-3">{description}</p>}
    </div>
  );
};

export default ScoreCard;
