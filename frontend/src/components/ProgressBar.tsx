import React from 'react';

interface ProgressBarProps {
  value: number;
  max?: number;
  showPercentage?: boolean;
  animated?: boolean;
  label?: string;
}

const ProgressBar: React.FC<ProgressBarProps> = ({
  value,
  max = 100,
  showPercentage = true,
  animated = true,
  label,
}) => {
  const percentage = (value / max) * 100;

  return (
    <div>
      <div className="flex justify-between items-center mb-2">
        {label && <p className="text-white font-semibold">{label}</p>}
        {showPercentage && <p className="text-purple-400 font-bold">{percentage.toFixed(0)}%</p>}
      </div>
      <div className="w-full bg-gray-800/50 rounded-full h-4 border border-purple-500/30 overflow-hidden">
        <div
          className={`bg-gradient-to-r from-purple-500 to-pink-600 h-full ${
            animated ? 'transition-all duration-300' : ''
          }`}
          style={{ width: `${percentage}%` }}
        />
      </div>
    </div>
  );
};

export default ProgressBar;
