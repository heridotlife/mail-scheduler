"""Logging configuration for the application.

This module provides centralized logging configuration following best practices.
"""

import logging
import sys
from typing import Optional


def configure_logging(
    level: str = "INFO",
    log_file: Optional[str] = None,
    log_format: Optional[str] = None,
) -> None:
    """
    Configure application logging.

    Args:
        level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        log_file: Optional file path for logging to file
        log_format: Optional custom log format

    Example:
        >>> configure_logging(level="DEBUG", log_file="app.log")
    """
    # Default format if not provided
    if log_format is None:
        log_format = (
            "%(asctime)s - %(name)s - %(levelname)s - "
            "%(filename)s:%(lineno)d - %(message)s"
        )

    # Convert string level to logging constant
    numeric_level = getattr(logging, level.upper(), logging.INFO)

    # Configure root logger
    logging.basicConfig(
        level=numeric_level, format=log_format, handlers=[]  # Clear default handlers
    )

    # Get root logger
    root_logger = logging.getLogger()

    # Console handler (stderr for errors, stdout for info)
    console_handler = logging.StreamHandler(sys.stderr)
    console_handler.setLevel(numeric_level)
    console_formatter = logging.Formatter(log_format)
    console_handler.setFormatter(console_formatter)
    root_logger.addHandler(console_handler)

    # File handler (if specified)
    if log_file:
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(numeric_level)
        file_formatter = logging.Formatter(log_format)
        file_handler.setFormatter(file_formatter)
        root_logger.addHandler(file_handler)

    # Set specific loggers to appropriate levels
    # Suppress noisy third-party loggers
    logging.getLogger("werkzeug").setLevel(logging.WARNING)
    logging.getLogger("urllib3").setLevel(logging.WARNING)
    logging.getLogger("rq.worker").setLevel(logging.INFO)


def get_logger(name: str) -> logging.Logger:
    """
    Get a logger instance with the given name.

    Args:
        name: Logger name (typically __name__)

    Returns:
        logging.Logger: Configured logger instance

    Example:
        >>> logger = get_logger(__name__)
        >>> logger.info("Application started")
    """
    return logging.getLogger(name)


# Application-specific loggers
def get_app_logger() -> logging.Logger:
    """Get the main application logger."""
    return logging.getLogger("mail_scheduler")


def get_job_logger() -> logging.Logger:
    """Get the background job logger."""
    return logging.getLogger("mail_scheduler.jobs")


def get_api_logger() -> logging.Logger:
    """Get the API logger."""
    return logging.getLogger("mail_scheduler.api")


def get_security_logger() -> logging.Logger:
    """Get the security logger for authentication/authorization events."""
    return logging.getLogger("mail_scheduler.security")
