import React, { useState } from 'react';
import { Upload, Link as LinkIcon, ArrowRight } from 'lucide-react';

interface UploadStartupProps {
  onNavigate: (screen: string, analysisId?: string) => void;
  onSubmit: (data: { website_url: string; pitch_deck?: File }) => string;
}

const UploadStartup: React.FC<UploadStartupProps> = ({ onNavigate, onSubmit }) => {
  const [websiteUrl, setWebsiteUrl] = useState('');
  const [pitchDeck, setPitchDeck] = useState<File | null>(null);
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      setPitchDeck(e.target.files[0]);
      setError('');
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');

    if (!websiteUrl.trim()) {
      setError('Please enter a website URL');
      return;
    }

    try {
      setLoading(true);
      const analysisId = onSubmit({
        website_url: websiteUrl,
        pitch_deck: pitchDeck || undefined,
      });
      onNavigate('progress', analysisId);
    } catch (err) {
      setError('Failed to submit analysis');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-bg-light">
      <nav className="sticky top-0 z-50 bg-white border-b border-border shadow-xs">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
          <button
            onClick={() => onNavigate('landing')}
            className="text-3xl font-bold text-accent hover:opacity-80 transition tracking-wide"
          >
            ✦ VentureMind AI
          </button>
        </div>
      </nav>

      <div className="max-w-2xl mx-auto px-4 sm:px-6 lg:px-8 py-24">
        <div className="mb-16">
          <h1 className="text-5xl font-bold text-text-primary mb-4">Analyze a Startup</h1>
          <p className="text-text-secondary text-lg">
            Submit a startup for comprehensive AI-powered analysis. Provide the website URL and
            optionally upload the pitch deck.
          </p>
        </div>

        <form onSubmit={handleSubmit} className="space-y-8">
          {/* Website URL */}
          <div>
            <label className="block text-text-primary font-semibold mb-3 text-base">Website URL *</label>
            <div className="relative">
              <LinkIcon className="absolute left-4 top-3.5 text-text-secondary w-5 h-5" />
              <input
                type="url"
                placeholder="https://example.com"
                value={websiteUrl}
                onChange={(e) => {
                  setWebsiteUrl(e.target.value);
                  setError('');
                }}
                className="input-primary w-full pl-12"
              />
            </div>
          </div>

          {/* Pitch Deck Upload */}
          <div>
            <label className="block text-text-primary font-semibold mb-3 text-base">Pitch Deck (Optional)</label>
            <div
              className="border-2 border-dashed border-accent/30 hover:border-accent/60 hover:bg-accent/5 rounded-lg p-8 transition cursor-pointer shadow-xs"
              onClick={() => document.getElementById('pitch-deck-input')?.click()}
            >
              <div className="text-center">
                <Upload className="w-12 h-12 text-accent mx-auto mb-4" />
                <p className="text-text-primary font-semibold mb-2 text-base">
                  {pitchDeck ? pitchDeck.name : 'Drop your pitch deck here'}
                </p>
                <p className="text-text-secondary text-sm">
                  {pitchDeck ? (
                    <span className="text-success">✓ File selected</span>
                  ) : (
                    'PDF, PPTX, or DOC files supported'
                  )}
                </p>
              </div>
              <input
                id="pitch-deck-input"
                type="file"
                accept=".pdf,.pptx,.doc,.docx"
                onChange={handleFileChange}
                className="hidden"
              />
            </div>
          </div>

          {/* Error Message */}
          {error && (
            <div className="bg-error/10 border border-error/30 rounded-lg p-4">
              <p className="text-error">{error}</p>
            </div>
          )}

          {/* Submit Button */}
          <button
            type="submit"
            disabled={loading}
            className="btn-primary w-full flex items-center justify-center space-x-2 disabled:opacity-50"
          >
            <span>{loading ? 'Submitting...' : 'Start Analysis'}</span>
            {!loading && <ArrowRight className="w-5 h-5" />}
          </button>

          {/* Quick Start Example */}
          <div className="bg-bg-card border border-border rounded-lg p-4 shadow-xs">
            <p className="text-text-secondary text-sm">
              💡 <strong className="text-accent">Quick Start:</strong> Try analyzing Airbnb with URL{' '}
              <span className="text-accent font-semibold">https://www.airbnb.com</span>
            </p>
          </div>
        </form>
      </div>
    </div>
  );
};

export default UploadStartup;
