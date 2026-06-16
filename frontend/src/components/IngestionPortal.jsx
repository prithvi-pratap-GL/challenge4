import React, { useState, useRef, useCallback, useEffect } from 'react';
import { X, FileText, Globe, UploadCloud, Trash2, Loader2, CheckCircle2 } from 'lucide-react';
import './IngestionPortal.css';

const PIPELINE_PHASES = [
  {
    id: 'parse',
    label: 'Parsing pitch deck typography & layout structure...',
    duration: 2200,
  },
  {
    id: 'crawl',
    label: 'Crawling live website and extracting operational signatures...',
    duration: 2600,
  },
  {
    id: 'extract',
    label: 'Executing LangChain extraction agent against Qdrant vector space...',
    duration: 3000,
  },
  {
    id: 'synthesize',
    label: 'Synthesizing deterministic investment score matrix...',
    duration: 2400,
  },
];

function formatBytes(bytes) {
  if (bytes === 0) return '0 B';
  const k = 1024;
  const sizes = ['B', 'KB', 'MB', 'GB'];
  const i = Math.floor(Math.log(bytes) / Math.log(k));
  return `${(bytes / Math.pow(k, i)).toFixed(1)} ${sizes[i]}`;
}

export default function IngestionPortal({ isOpen, onClose, onComplete }) {
  const [file, setFile] = useState(null);
  const [companyUrl, setCompanyUrl] = useState('');
  const [isDragging, setIsDragging] = useState(false);
  const [isProcessing, setIsProcessing] = useState(false);
  const [activePhase, setActivePhase] = useState(-1);
  const [completedPhases, setCompletedPhases] = useState([]);
  const [error, setError] = useState(null);

  const fileInputRef = useRef(null);
  const dragCounter = useRef(0);

  useEffect(() => {
    if (!isOpen) {
      const timeout = setTimeout(() => {
        setFile(null);
        setCompanyUrl('');
        setIsProcessing(false);
        setActivePhase(-1);
        setCompletedPhases([]);
        setError(null);
      }, 300);
      return () => clearTimeout(timeout);
    }
  }, [isOpen]);

  const handleDragEnter = useCallback((e) => {
    e.preventDefault();
    dragCounter.current += 1;
    setIsDragging(true);
  }, []);

  const handleDragLeave = useCallback((e) => {
    e.preventDefault();
    dragCounter.current -= 1;
    if (dragCounter.current === 0) setIsDragging(false);
  }, []);

  const handleDragOver = useCallback((e) => {
    e.preventDefault();
  }, []);

  const handleDrop = useCallback((e) => {
    e.preventDefault();
    dragCounter.current = 0;
    setIsDragging(false);
    const dropped = e.dataTransfer.files?.[0];
    if (dropped && dropped.type === 'application/pdf') {
      setFile(dropped);
    }
  }, []);

  const handleFileSelect = (e) => {
    const selected = e.target.files?.[0];
    if (selected) setFile(selected);
  };

  const removeFile = (e) => {
    e.stopPropagation();
    setFile(null);
    if (fileInputRef.current) fileInputRef.current.value = '';
  };

  const runPipelineSequence = useCallback(() => {
    let cumulativeDelay = 0;
    const timeouts = [];

    PIPELINE_PHASES.forEach((phase, index) => {
      const startTimeout = setTimeout(() => {
        setActivePhase(index);
      }, cumulativeDelay);
      timeouts.push(startTimeout);

      cumulativeDelay += phase.duration;

      const completeTimeout = setTimeout(() => {
        setCompletedPhases((prev) => [...prev, index]);
      }, cumulativeDelay);
      timeouts.push(completeTimeout);
    });

    const finalTimeout = setTimeout(() => {
      submitToBackend();
    }, cumulativeDelay + 300);
    timeouts.push(finalTimeout);

    return timeouts;
  }, [file, companyUrl]);

  const submitToBackend = async () => {
    try {
      const formData = new FormData();
      if (file) formData.append('pitch_deck', file);
      if (companyUrl.trim()) formData.append('company_url', companyUrl.trim());

      const response = await fetch('http://localhost:8000/api/v1/ingest', {
        method: 'POST',
        body: formData,
      });

      if (!response.ok) {
        throw new Error(`Ingestion failed with status ${response.status}`);
      }

      const data = await response.json();

      if (onComplete) onComplete(data);
      onClose();
    } catch (err) {
      setError(err.message || 'Failed to process deal. Please try again.');
      setIsProcessing(false);
    }
  };

  const handleAnalyze = () => {
    if (!file && !companyUrl.trim()) {
      setError('Provide at least a pitch deck or a company URL.');
      return;
    }
    setError(null);
    setIsProcessing(true);
    setActivePhase(-1);
    setCompletedPhases([]);
    runPipelineSequence();
  };

  if (!isOpen) return null;

  return (
    <div className="ingestion-overlay" onClick={onClose}>
      <div className="ingestion-panel" onClick={(e) => e.stopPropagation()}>
        <button className="ingestion-close" onClick={onClose} aria-label="Close">
          <X size={18} />
        </button>

        <div className="ingestion-header">
          <span className="ingestion-eyebrow">New Diligence Evaluation</span>
          <h2 className="ingestion-title">Ingest Deal Materials</h2>
          <p className="ingestion-subtitle">
            Upload a pitch deck and link the company's website to begin a full
            evidence-linked diligence pass.
          </p>
        </div>

        {!isProcessing ? (
          <div className="ingestion-body">
            <div
              className={`dropzone ${isDragging ? 'dropzone--active' : ''} ${file ? 'dropzone--filled' : ''}`}
              onDragEnter={handleDragEnter}
              onDragLeave={handleDragLeave}
              onDragOver={handleDragOver}
              onDrop={handleDrop}
              onClick={() => !file && fileInputRef.current?.click()}
            >
              <input
                ref={fileInputRef}
                type="file"
                accept="application/pdf"
                onChange={handleFileSelect}
                className="dropzone-input"
              />

              {!file ? (
                <div className="dropzone-empty">
                  <div className="dropzone-icon">
                    <UploadCloud size={26} strokeWidth={1.5} />
                  </div>
                  <p className="dropzone-label">
                    Drop pitch deck here, or <span>browse files</span>
                  </p>
                  <p className="dropzone-hint">PDF format · up to 25MB</p>
                </div>
              ) : (
                <div className="file-card">
                  <div className="file-card-icon">
                    <FileText size={20} strokeWidth={1.5} />
                  </div>
                  <div className="file-card-meta">
                    <span className="file-card-name">{file.name}</span>
                    <span className="file-card-size">{formatBytes(file.size)}</span>
                  </div>
                  <button className="file-card-remove" onClick={removeFile} aria-label="Remove file">
                    <Trash2 size={16} strokeWidth={1.5} />
                  </button>
                </div>
              )}
            </div>

            <div className="ingestion-divider">
              <span>and / or</span>
            </div>

            <div className="url-field">
              <Globe size={18} strokeWidth={1.5} className="url-field-icon" />
              <input
                type="text"
                placeholder="https://company-website.com"
                value={companyUrl}
                onChange={(e) => setCompanyUrl(e.target.value)}
                className="url-field-input"
              />
            </div>

            {error && <div className="ingestion-error">{error}</div>}

            <button className="analyze-button" onClick={handleAnalyze}>
              Analyze Deal
            </button>
          </div>
        ) : (
          <div className="pipeline-body">
            {PIPELINE_PHASES.map((phase, index) => {
              const isActive = activePhase === index;
              const isComplete = completedPhases.includes(index);
              const isPending = !isActive && !isComplete;

              return (
                <div
                  key={phase.id}
                  className={`pipeline-step ${isActive ? 'pipeline-step--active' : ''} ${
                    isComplete ? 'pipeline-step--complete' : ''
                  } ${isPending ? 'pipeline-step--pending' : ''}`}
                >
                  <div className="pipeline-step-indicator">
                    {isComplete ? (
                      <CheckCircle2 size={18} strokeWidth={1.75} />
                    ) : isActive ? (
                      <Loader2 size={18} strokeWidth={1.75} className="spin-icon" />
                    ) : (
                      <div className="pipeline-step-dot" />
                    )}
                  </div>
                  <div className="pipeline-step-content">
                    <span className="pipeline-step-label">{phase.label}</span>
                    {isActive && (
                      <div className="pipeline-step-bar">
                        <div className="pipeline-step-bar-fill" />
                      </div>
                    )}
                  </div>
                </div>
              );
            })}

            {error && <div className="ingestion-error">{error}</div>}

            <p className="pipeline-footnote">
              This typically completes in under a minute. Scores will populate
              automatically once synthesis finishes.
            </p>
          </div>
        )}
      </div>
    </div>
  );
}