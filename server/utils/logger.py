"""Logging configuration for SparkRepo application."""
import logging
import os
from logging.handlers import RotatingFileHandler

# Log level from environment or default to INFO
LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO').upper()


def setup_logger(name: str = 'sparkrepo', log_file: str = 'sparkrepo.log') -> logging.Logger:
    """
    Setup and configure logger for the application.
    
    Args:
        name: Logger name
        log_file: Path to log file
        
    Returns:
        Configured logger instance
    """
    logger = logging.getLogger(name)
    
    # Only configure if not already configured
    if logger.handlers:
        return logger
    
    logger.setLevel(getattr(logging, LOG_LEVEL))
    
    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(getattr(logging, LOG_LEVEL))
    
    # File handler with rotation
    try:
        file_handler = RotatingFileHandler(
            log_file,
            maxBytes=10485760,  # 10MB
            backupCount=10
        )
        file_handler.setLevel(getattr(logging, LOG_LEVEL))
    except Exception as e:
        print(f"Warning: Could not setup file logging: {e}")
        file_handler = None
    
    # Formatter
    formatter = logging.Formatter(
        fmt='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    if file_handler:
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    
    return logger


def get_logger(name: str) -> logging.Logger:
    """Get a logger instance."""
    return logging.getLogger(name)
