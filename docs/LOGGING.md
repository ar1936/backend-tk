# Logging System

This document outlines the logging system implemented in the Document Management System.

## Overview

The logging system is built on Python's built-in `logging` module and includes:

- **Structured Logging**: Logs include timestamps, process IDs, log levels, and structured data
- **Multiple Handlers**: Logs are written to both console and files
- **Rotation**: Log files rotate at 10MB, keeping up to 5 backup files
- **Error Separation**: Error-level logs are stored in a separate file
- **Environment Configuration**: Logging behavior is configurable via environment variables

## Log Files

Logs are stored in the `logs/` directory with these files:

- `app.log`: All application logs (INFO level and above by default)
- `error.log`: Only ERROR level and above logs

## Configuration

Configure logging using these environment variables in your `.env` file:

```ini
# Logging configuration
LOG_LEVEL=INFO  # DEBUG, INFO, WARNING, ERROR, CRITICAL
LOG_DIR=logs
LOG_MAX_BYTES=10485760  # 10MB
LOG_BACKUP_COUNT=5
```

## Usage

### Basic Logging

```python
import logging

# Get a logger for your module
logger = logging.getLogger(__name__)


# Log messages at different levels
logger.debug("Debug message")
logger.info("Informational message")
logger.warning("Warning message")
logger.error("Error message")
logger.critical("Critical message")
```

### Structured Logging

```python
# Log structured data using the extra parameter
logger.info(
    "User login attempt",
    extra={
        "user_id": 123,
        "ip": "192.168.1.1",
        "status": "success"
    }
)
```

### Request Logging

Request logging is automatically handled by the middleware in `main.py`, logging:

- HTTP method
- Request path
- Query parameters
- Client IP
- Response status code
- Processing time

## Testing the Logging System

To test logging, run:

```bash
python scripts/test_logging.py
```

This generates test log messages and shows log file locations.

## Best Practices

1. **Use Appropriate Log Levels**:
   - DEBUG: Detailed diagnostic information
   - INFO: Confirmation of expected behavior
   - WARNING: Unexpected but handled events
   - ERROR: Serious problems that affect functionality
   - CRITICAL: Critical errors that may stop the application

2. **Include Context**: Provide enough information in log messages for effective debugging.

3. **Use Structured Logging**: Log structured data for easier analysis.

4. **Protect Sensitive Data**: Never log passwords, API keys, or personal information.

## Troubleshooting

- **No Logs Appearing**:
  - Verify the `logs` directory exists and is writable
  - Check the log level setting
  - Confirm proper permissions

- **Log Rotation Issues**:
  - Ensure write permissions for log files
  - Check available disk space
  - Verify `LOG_MAX_BYTES` and `LOG_BACKUP_COUNT` settings
