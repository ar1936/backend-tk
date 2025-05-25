from pydantic_settings import BaseSettings
from typing import List, Optional
import secrets
import os
from pathlib import Path
from typing import Dict, Any
import logging

class Settings(BaseSettings):
    # Application
    PROJECT_NAME: str = "Document Management System"
    API_V1_STR: str = "/api/v1"
    DEBUG: bool = False
    
    # Security
    SECRET_KEY: str = secrets.token_urlsafe(32)
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 7 days
    
    # Database
    POSTGRES_SERVER: str = "localhost"
    POSTGRES_USER: str = "newuser"
    POSTGRES_PASSWORD: str = "StrongPass123"
    POSTGRES_DB: str = "newdb"
    
    # CORS
    CORS_ALLOWED_ORIGINS: str = "http://localhost:4200,http://127.0.0.1:4200"
    
    # Logging
    LOG_LEVEL: str = "INFO"
    LOG_DIR: str = "logs"
    LOG_MAX_BYTES: int = 10 * 1024 * 1024  # 10MB
    LOG_BACKUP_COUNT: int = 5
    
    @property
    def SQLALCHEMY_DATABASE_URI(self) -> str:
        return f"postgresql://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_SERVER}/{self.POSTGRES_DB}"
    
    @property
    def CORS_ORIGINS(self) -> List[str]:
        return [origin.strip() for origin in self.CORS_ALLOWED_ORIGINS.split(",")]
    
    def get_logging_config(self, process_id: int = None) -> Dict[str, Any]:
        """Get logging configuration for the current process.
        
        Args:
            process_id: The process ID. If None, uses the current process ID.
        """
        if process_id is None:
            import os
            process_id = os.getpid()
            
        log_dir = Path(self.LOG_DIR)
        log_dir.mkdir(exist_ok=True, parents=True)
        
        return {
            "version": 1,
            "disable_existing_loggers": False,
            "formatters": {
                "standard": {
                    "format": "%(asctime)s - %(process)d - %(name)s - %(levelname)s - %(message)s",
                    "datefmt": "%Y-%m-%d %H:%M:%S"
                },
                "console": {
                    "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
                    "datefmt": "%Y-%m-%d %H:%M:%S"
                }
            },
            "handlers": {
                "console": {
                    "level": self.LOG_LEVEL,
                    "class": "logging.StreamHandler",
                    "formatter": "console",
                    "stream": "ext://sys.stdout"
                },
                "file": {
                    "level": self.LOG_LEVEL,
                    "class": "logging.handlers.RotatingFileHandler",
                    "filename": str(log_dir / f"app_{process_id}.log"),
                    "maxBytes": self.LOG_MAX_BYTES,
                    "backupCount": self.LOG_BACKUP_COUNT,
                    "formatter": "standard",
                    "encoding": "utf-8"
                },
                "error_file": {
                    "level": "ERROR",
                    "class": "logging.handlers.RotatingFileHandler",
                    "filename": str(log_dir / f"error_{process_id}.log"),
                    "maxBytes": self.LOG_MAX_BYTES,
                    "backupCount": self.LOG_BACKUP_COUNT,
                    "formatter": "standard",
                    "encoding": "utf-8"
                }
            },
            "loggers": {
                "": {  # root logger
                    "handlers": ["console", "file", "error_file"],
                    "level": self.LOG_LEVEL,
                    "propagate": False
                },
                "app": {
                    "handlers": ["console", "file", "error_file"],
                    "level": self.LOG_LEVEL,
                    "propagate": False
                },
                "uvicorn": {
                    "handlers": ["console", "file"],
                    "level": self.LOG_LEVEL,
                    "propagate": False
                },
                "uvicorn.error": {
                    "handlers": ["console", "file"],
                    "level": self.LOG_LEVEL,
                    "propagate": False
                }
            }
        }
    
    class Config:
        case_sensitive = True
        env_file = ".env"
        env_file_encoding = 'utf-8'
        
        @classmethod
        def customise_sources(
            cls,
            init_settings,
            env_settings,
            file_secret_settings,
        ):
            # This changes the priority order of configuration sources
            return (
                init_settings,
                env_settings,
                file_secret_settings,
            )

settings = Settings() 