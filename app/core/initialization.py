"""Application initialization and setup."""
import logging
import logging.config
from pathlib import Path
from typing import Optional

from app.core.config import settings

def setup_logging() -> None:
    """Configure logging for the application.
    
    This function sets up the logging directory and applies the logging configuration
    with process-specific log files.
    """
    import os
    
    # Get the current process ID
    process_id = os.getpid()
    
    # Configure logging with process-specific log files
    logging_config = settings.get_logging_config(process_id)
    logging.config.dictConfig(logging_config)
    
    # Log application startup
    logger = logging.getLogger(__name__)
    logger.info("Logging configured successfully for process %d", process_id)
    logger.debug("Debug logging enabled for process %d", process_id)
    
    # Log the log file paths
    log_dir = Path(settings.LOG_DIR)
    app_log = log_dir / f"app_{process_id}.log"
    error_log = log_dir / f"error_{process_id}.log"
    logger.info("Application logs: %s", app_log.absolute())
    logger.info("Error logs: %s", error_log.absolute())

def initialize_application() -> None:
    """Initialize the application with all required setup."""
    # Setup logging first
    setup_logging()
    
    # Import logger after setup to ensure proper configuration
    from app.core.logger import logger
    
    try:
        # Additional initialization can be added here
        logger.info("Application initialization complete")
    except Exception as e:
        logger.critical("Failed to initialize application", exc_info=True)
        raise
