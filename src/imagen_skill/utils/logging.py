"""Structured logging setup for Imagen skill."""

import logging
import sys
from typing import Any


def setup_logging(level: str = "INFO", debug: bool = False) -> logging.Logger:
    """Configure structured logging for the application.

    Args:
        level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        debug: Enable debug mode with verbose output

    Returns:
        Configured logger instance
    """
    # Override level if debug is enabled
    if debug:
        level = "DEBUG"

    # Create logger
    logger = logging.getLogger("imagen_skill")
    logger.setLevel(getattr(logging, level.upper()))

    # Remove existing handlers
    logger.handlers.clear()

    # Create console handler with formatting
    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(getattr(logging, level.upper()))

    # Create formatter
    if debug:
        # Detailed format for debugging
        formatter = logging.Formatter(
            fmt="%(asctime)s - %(name)s - %(levelname)s - %(funcName)s:%(lineno)d - %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )
    else:
        # Simpler format for production
        formatter = logging.Formatter(
            fmt="%(levelname)s - %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )

    handler.setFormatter(formatter)
    logger.addHandler(handler)

    return logger


def log_dict(logger: logging.Logger, level: int, message: str, data: dict[str, Any]) -> None:
    """Log a message with structured data.

    Args:
        logger: Logger instance
        level: Logging level (logging.INFO, logging.DEBUG, etc.)
        message: Log message
        data: Structured data to log
    """
    formatted_data = ", ".join(f"{k}={v}" for k, v in data.items())
    logger.log(level, f"{message} | {formatted_data}")
