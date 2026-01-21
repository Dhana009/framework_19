"""
Centralized Logger

Provides consistent logging across the framework.

Responsibilities:
- Configure Python logging
- Provide structured log format
- Support different log levels
"""

import logging
import sys
from pathlib import Path
from datetime import datetime


def setup_logger(
    name: str = "automation_framework",
    log_level: str = "INFO",
    log_file: str = None,
    log_format: str = None
) -> logging.Logger:
    """
    Set up and configure logger.
    
    Args:
        name: Logger name
        log_level: Log level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        log_file: Optional log file path
        log_format: Optional custom log format
    
    Returns:
        Configured logger instance
    """
    logger = logging.getLogger(name)
    logger.setLevel(getattr(logging, log_level.upper()))
    
    # Clear existing handlers
    logger.handlers = []
    
    # Default format
    if not log_format:
        log_format = "%(asctime)s [%(levelname)8s] [%(name)s] %(message)s"
    
    formatter = logging.Formatter(
        log_format,
        datefmt="%Y-%m-%d %H:%M:%S"
    )
    
    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    # File handler (if specified)
    if log_file:
        log_path = Path(log_file)
        log_path.parent.mkdir(parents=True, exist_ok=True)
        
        file_handler = logging.FileHandler(log_file)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    
    return logger


def get_logger(name: str = None) -> logging.Logger:
    """
    Get logger instance.
    
    Args:
        name: Logger name (defaults to root automation framework logger)
    
    Returns:
        Logger instance
    """
    if name:
        return logging.getLogger(f"automation_framework.{name}")
    return logging.getLogger("automation_framework")


# Initialize default logger
default_logger = setup_logger()
