/**
 * ResearchForm Component
 * Input form for startup research
 */

import React, { useState } from "react";

interface ResearchFormProps {
  onSubmit: (startupName: string) => void;
  loading?: boolean;
}

export function ResearchForm({ onSubmit, loading }: ResearchFormProps) {
  const [startupName, setStartupName] = useState("");

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (startupName.trim()) {
      onSubmit(startupName.trim());
      setStartupName("");
    }
  };

  return (
    <form onSubmit={handleSubmit} className="research-form">
      <div className="form-group">
        <label htmlFor="startup-name">Startup Name</label>
        <input
          id="startup-name"
          type="text"
          value={startupName}
          onChange={(e) => setStartupName(e.target.value)}
          placeholder="Enter startup name (e.g., OpenAI, Stripe)"
          disabled={loading}
          autoFocus
        />
      </div>
      <button type="submit" disabled={loading || !startupName.trim()}>
        {loading ? "Researching..." : "Start Research"}
      </button>
    </form>
  );
}
