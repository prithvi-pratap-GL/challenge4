import React from 'react';

interface NavigationBarProps {
  onHome: () => void;
  showBackButton?: boolean;
  onBack?: () => void;
}

const NavigationBar: React.FC<NavigationBarProps> = ({ onHome, showBackButton = false, onBack }) => {
  return (
    <nav className="border-b border-purple-500/20 backdrop-blur-md">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
        <div className="flex justify-between items-center">
          <button
            onClick={onHome}
            className="text-2xl font-bold bg-gradient-to-r from-purple-400 to-pink-600 bg-clip-text text-transparent hover:opacity-80 transition"
          >
            VentureMind AI
          </button>
          {showBackButton && onBack && (
            <button
              onClick={onBack}
              className="px-4 py-2 text-gray-400 hover:text-white transition"
            >
              ← Back
            </button>
          )}
        </div>
      </div>
    </nav>
  );
};

export default NavigationBar;
