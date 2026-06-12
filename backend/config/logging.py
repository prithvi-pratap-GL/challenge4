"""Logging configuration."""

import logging
import sys
from backend.config.settings import settings


def setup_logging():
    """Configure application logging."""
    log_level = getattr(logging, settings.LOG_LEVEL.upper(), logging.INFO)

    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(log_level)
    console_handler.setFormatter(formatter)

    # Root logger configuration
    root_logger = logging.getLogger()
    root_logger.setLevel(log_level)
    root_logger.addHandler(console_handler)

    # Suppress verbose logs
    logging.getLogger('httpx').setLevel(logging.WARNING)
    logging.getLogger('openai').setLevel(logging.WARNING)

    return root_logger


def get_logger(name: str) -> logging.Logger:
    """Get logger instance."""
    return logging.getLogger(name)
