// Currency formatter
export const formatCurrency = (value: number): string => {
  return new Intl.NumberFormat('en-US', {
    style: 'currency',
    currency: 'USD',
    minimumFractionDigits: 0,
    maximumFractionDigits: 2,
  }).format(value);
};

// Percentage formatter
export const formatPercentage = (value: number): string => {
  return `${(value * 100).toFixed(1)}%`;
};

// Score formatter (0-10)
export const formatScore = (value: number): string => {
  return value.toFixed(1);
};

// Date formatter
export const formatDate = (dateString: string): string => {
  return new Date(dateString).toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'short',
    day: 'numeric',
  });
};

// Get score color class
export const getScoreColorClass = (score: number): string => {
  if (score >= 8) return 'text-green-400';
  if (score >= 6) return 'text-yellow-400';
  return 'text-orange-400';
};

// Get score background class
export const getScoreBgClass = (score: number): string => {
  if (score >= 8) return 'bg-green-500/20 text-green-400';
  if (score >= 6) return 'bg-yellow-500/20 text-yellow-400';
  return 'bg-red-500/20 text-red-400';
};
