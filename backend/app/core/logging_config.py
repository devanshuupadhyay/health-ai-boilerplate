# backend/app/core/logging_config.py
import logging
import sys
import structlog


def configure_logging():
    """Configures standard logging and Structlog."""

    # Basic configuration for standard logging (optional, but good practice)
    logging.basicConfig(
        format="%(message)s",
        stream=sys.stdout,
        level=logging.INFO,
    )

    # Configure Structlog
    structlog.configure(
        processors=[
            structlog.stdlib.add_logger_name,
            structlog.stdlib.add_log_level,
            structlog.processors.TimeStamper(fmt="iso"),
            structlog.processors.StackInfoRenderer(),
            structlog.processors.format_exc_info,
            structlog.processors.JSONRenderer(),
        ],
        # Use a standard library logger factory
        logger_factory=structlog.stdlib.LoggerFactory(),
        # Use a standard library wrapper class for compatibility
        wrapper_class=structlog.stdlib.BoundLogger,
        # Cache the logger factory for performance
        cache_logger_on_first_use=True,
    )
    print("Structlog configured.")  # Simple confirmation log


def get_logger(name: str) -> structlog.stdlib.BoundLogger:
    """Helper function to get a Structlog logger instance."""
    return structlog.get_logger(name)
