"""Ingestion module for startup data.

Handles ingestion of pitch decks and websites.
"""

from .pdf.pipeline import ingest_pitch_deck
from .website.pipeline import ingest_website

__all__ = ["ingest_pitch_deck", "ingest_website"]
