"""Application package constructor."""
import logging

# Import settings to ensure they're loaded
from app.core.config import settings  # noqa: F401

# Initialize application
from app.core.initialization import initialize_application

# Set up logging and other initializations
initialize_application()

# Create logger for this module
logger = logging.getLogger(__name__)
logger.info("Application package initialized")

# Import all modules to register models and routes
# This must be after the app is created to avoid circular imports
from .api import auth, users, documents, ingestion  # noqa: F401

__all__ = [
    'auth',
    'users',
    'documents',
    'ingestion',
]