"""
JSON Storage Service - Person 2
Stores ResearchOutput to JSON files for persistence and caching
"""

import json
import os
from datetime import datetime
from pathlib import Path
from typing import Optional
from backend.contracts.research import ResearchOutput


class JSONStorageService:
    """Store and retrieve research results in JSON format"""

    def __init__(self, storage_dir: str = "backend/research_results"):
        self.storage_dir = Path(storage_dir)
        self.storage_dir.mkdir(parents=True, exist_ok=True)

    def save_research(self, startup_name: str, research_output: ResearchOutput) -> str:
        """
        Save research output to JSON file
        Returns the file path where data was saved
        """
        try:
            # Create filename with timestamp
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{startup_name.lower().replace(' ', '_')}_{timestamp}.json"
            filepath = self.storage_dir / filename

            # Convert ResearchOutput to dict and add metadata
            data = {
                "startup_name": startup_name,
                "timestamp": datetime.now().isoformat(),
                "research_data": research_output.to_dict()
            }

            # Write to JSON file
            with open(filepath, 'w') as f:
                json.dump(data, f, indent=2)

            print(f"[STORAGE] Research saved to {filepath}")
            return str(filepath)

        except Exception as e:
            print(f"[ERROR] Failed to save research: {e}")
            raise

    def load_research(self, filepath: str) -> Optional[dict]:
        """Load research data from JSON file"""
        try:
            with open(filepath, 'r') as f:
                data = json.load(f)
            return data
        except Exception as e:
            print(f"[ERROR] Failed to load research from {filepath}: {e}")
            return None

    def get_latest_research(self, startup_name: str) -> Optional[dict]:
        """Get the most recent research for a startup"""
        try:
            search_prefix = startup_name.lower().replace(' ', '_')
            matching_files = sorted(
                self.storage_dir.glob(f"{search_prefix}_*.json"),
                reverse=True
            )

            if matching_files:
                return self.load_research(str(matching_files[0]))
            return None

        except Exception as e:
            print(f"[ERROR] Failed to get latest research: {e}")
            return None

    def list_all_research(self) -> list:
        """List all stored research files"""
        try:
            return sorted(self.storage_dir.glob("*.json"), reverse=True)
        except Exception as e:
            print(f"[ERROR] Failed to list research: {e}")
            return []
