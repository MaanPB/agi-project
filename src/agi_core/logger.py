"""
Structured Logging

Provides JSON-based structured logging with correlation IDs and metadata.
"""

import json
import logging
import sys
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Optional
import uuid


class JSONFormatter(logging.Formatter):
    """
    Custom formatter that outputs logs in JSON format.
    """
    
    def format(self, record: logging.LogRecord) -> str:
        """
        Format a log record as JSON.
        
        Args:
            record: LogRecord to format
        
        Returns:
            JSON-formatted log string
        """
        log_data = {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "level": record.levelname,
            "name": record.name,
            "message": record.getMessage(),
            "module": record.module,
            "function": record.funcName,
            "line": record.lineno,
        }
        
        # Add correlation ID if present
        if hasattr(record, "correlation_id"):
            log_data["correlation_id"] = record.correlation_id
        
        # Add extra fields
        if hasattr(record, "extra_fields"):
            log_data.update(record.extra_fields)
        
        # Add exception info if present
        if record.exc_info:
            log_data["exception"] = self.formatException(record.exc_info)
        
        return json.dumps(log_data)


def get_logger(
    name: str,
    level: str = "INFO",
    log_file: Optional[str] = None,
    format_type: str = "json"
) -> logging.Logger:
    """
    Get or create a logger with structured JSON output.
    
    Args:
        name: Logger name (typically __name__ of the calling module)
        level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        log_file: Optional file path to write logs
        format_type: Format type ("json" or "text")
    
    Returns:
        Configured logger instance
    
    Examples:
        >>> logger = get_logger(__name__)
        >>> logger.info("Application started")
        >>> logger.error("Something went wrong", extra={"user_id": 123})
    """
    logger = logging.getLogger(name)
    
    # Only configure if not already configured
    if not logger.handlers:
        logger.setLevel(getattr(logging, level.upper()))
        
        # Console handler
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(getattr(logging, level.upper()))
        
        if format_type == "json":
            formatter = JSONFormatter()
        else:
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
        
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)
        
        # File handler (if specified)
        if log_file:
            log_path = Path(log_file)
            log_path.parent.mkdir(parents=True, exist_ok=True)
            
            file_handler = logging.FileHandler(log_file)
            file_handler.setLevel(getattr(logging, level.upper()))
            file_handler.setFormatter(formatter)
            logger.addHandler(file_handler)
        
        # Prevent propagation to avoid duplicate logs
        logger.propagate = False
    
    return logger


class ContextLogger:
    """
    Logger wrapper that adds context (correlation ID, extra fields) to all log calls.
    """
    
    def __init__(self, logger: logging.Logger, correlation_id: Optional[str] = None, **extra_fields):
        """
        Initialize context logger.
        
        Args:
            logger: Base logger to wrap
            correlation_id: Optional correlation ID for tracking related log entries
            **extra_fields: Additional fields to include in all logs
        """
        self.logger = logger
        self.correlation_id = correlation_id or str(uuid.uuid4())
        self.extra_fields = extra_fields
    
    def _add_context(self, extra: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Add context to log record."""
        context = {
            "correlation_id": self.correlation_id,
            "extra_fields": {**self.extra_fields, **(extra or {})}
        }
        return context
    
    def debug(self, message: str, **extra):
        """Log debug message with context."""
        self.logger.debug(message, extra=self._add_context(extra))
    
    def info(self, message: str, **extra):
        """Log info message with context."""
        self.logger.info(message, extra=self._add_context(extra))
    
    def warning(self, message: str, **extra):
        """Log warning message with context."""
        self.logger.warning(message, extra=self._add_context(extra))
    
    def error(self, message: str, **extra):
        """Log error message with context."""
        self.logger.error(message, extra=self._add_context(extra))
    
    def critical(self, message: str, **extra):
        """Log critical message with context."""
        self.logger.critical(message, extra=self._add_context(extra))


def get_context_logger(
    name: str,
    correlation_id: Optional[str] = None,
    **extra_fields
) -> ContextLogger:
    """
    Get a context logger with correlation ID and extra fields.
    
    Args:
        name: Logger name
        correlation_id: Optional correlation ID
        **extra_fields: Additional fields to include in all logs
    
    Returns:
        ContextLogger instance
    
    Examples:
        >>> logger = get_context_logger(__name__, user_id=123, session="abc")
        >>> logger.info("User action performed")
    """
    base_logger = get_logger(name)
    return ContextLogger(base_logger, correlation_id, **extra_fields)


# Convenience function for quick logging setup
def setup_logging(config: Optional[Dict[str, Any]] = None) -> None:
    """
    Set up logging configuration from config dictionary.
    
    Args:
        config: Configuration dictionary with logging settings
    """
    if config is None:
        config = {}
    
    log_config = config.get("logging", {})
    level = log_config.get("level", "INFO")
    log_file = log_config.get("file")

    # Clear existing handlers to avoid conflicts in tests
    logger = logging.getLogger("agi_core")
    logger.handlers.clear()
    
    # Configure root logger
    root_logger = get_logger("agi_core", level=level, log_file=log_file)
    root_logger.info("Logging initialized", extra={"extra_fields": {"config": log_config}})
