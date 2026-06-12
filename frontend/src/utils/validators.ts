// URL validation
export const isValidUrl = (url: string): boolean => {
  try {
    new URL(url);
    return true;
  } catch {
    return false;
  }
};

// Email validation
export const isValidEmail = (email: string): boolean => {
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  return emailRegex.test(email);
};

// Score validation (0-10)
export const isValidScore = (score: number): boolean => {
  return score >= 0 && score <= 10;
};

// Percentage validation (0-1)
export const isValidPercentage = (value: number): boolean => {
  return value >= 0 && value <= 1;
};

// File size validation (in bytes)
export const isValidFileSize = (size: number, maxSizeInMB: number): boolean => {
  return size <= maxSizeInMB * 1024 * 1024;
};

// Supported file types
export const SUPPORTED_FILE_TYPES = ['application/pdf', 'application/vnd.ms-powerpoint', 'application/msword'];

export const isValidFileType = (mimeType: string): boolean => {
  return SUPPORTED_FILE_TYPES.includes(mimeType);
};
