"""Utility functions.

Person 5 owns this module.
"""

from datetime import datetime
from typing import Any, Dict
import json


def to_json_serializable(obj: Any) -> Any:
    """Convert object to JSON-serializable format."""
    if hasattr(obj, "dict"):
        return obj.dict()
    elif hasattr(obj, "__dict__"):
        return obj.__dict__
    elif isinstance(obj, datetime):
        return obj.isoformat()
    elif isinstance(obj, (list, tuple)):
        return [to_json_serializable(item) for item in obj]
    elif isinstance(obj, dict):
        return {k: to_json_serializable(v) for k, v in obj.items()}
    return obj


def safe_json_dumps(obj: Any, indent: int = 2) -> str:
    """Safely convert object to JSON string."""
    try:
        return json.dumps(to_json_serializable(obj), indent=indent)
    except Exception:
        return json.dumps({"error": f"Failed to serialize {type(obj)}"})


def format_error_response(error: Exception) -> Dict:
    """Format error as response."""
    return {
        "error": str(error),
        "type": type(error).__name__,
        "timestamp": datetime.utcnow().isoformat(),
    }


def calculate_progress(completed_stages: int, total_stages: int) -> int:
    """Calculate analysis progress percentage."""
    if total_stages == 0:
        return 0
    return min(100, int((completed_stages / total_stages) * 100))
