import os
import logging
import logging.handlers
from pathlib import Path
import os
import sys
from typing import Optional

def setup_logger(name: str = None, log_level: str = "INFO") -> logging.Logger:
    """
    Setup and configure a logger with file and console handlers.
    
    Args:
        name: Name of the logger (usually __name__)
        log_level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        
    Returns:
        Configured logger instance
    """
    # Create logs directory if it doesn't exist
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)
    
    # Get the root logger if no name is provided
    logger = logging.getLogger(name) if name else logging.getLogger()
    
    # Clear any existing handlers to avoid duplicate logs
    logger.handlers.clear()
    
    # Set log level
    level = getattr(logging, log_level.upper(), logging.INFO)
    logger.setLevel(level)
    
    # Prevent log propagation to parent loggers
    logger.propagate = False
    
    # Create formatters
    file_formatter = logging.Formatter(
        '%(asctime)s - %(process)d - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    console_formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # Create file handler for all logs
    all_logs_handler = logging.handlers.RotatingFileHandler(
        log_dir / 'app.log',
        maxBytes=10*1024*1024,  # 10MB
        backupCount=5,
        encoding='utf-8'
    )
    all_logs_handler.setLevel(level)
    all_logs_handler.setFormatter(file_formatter)
    
    # Create file handler for errors only
    error_logs_handler = logging.handlers.RotatingFileHandler(
        log_dir / 'error.log',
        maxBytes=10*1024*1024,  # 10MB
        backupCount=5,
        encoding='utf-8'
    )
    error_logs_handler.setLevel(logging.ERROR)
    error_logs_handler.setFormatter(file_formatter)
    
    # Create console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(level)
    console_handler.setFormatter(console_formatter)
    
    # Add handlers to logger
    logger.addHandler(all_logs_handler)
    logger.addHandler(error_logs_handler)
    logger.addHandler(console_handler)
    
    return logger

# Create a default logger instance
logger = setup_logger()

def get_logger(name: str = None) -> logging.Logger:
    """
    Get a logger instance with the given name.
    If no name is provided, returns the root logger.
    """
    return logging.getLogger(name) if name else logger
