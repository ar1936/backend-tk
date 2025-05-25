"""Test script to verify per-process logging configuration."""
import logging
import os
import sys
import time
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path

# Add the project root to the Python path
project_root = str(Path(__file__).parent.parent)
if project_root not in sys.path:
    sys.path.append(project_root)

# Import the application to initialize logging
from app import logger as app_logger  # noqa: F401
from app.core.config import settings
from app.core.initialization import setup_logging

def test_logging(process_num: int = 0):
    """Test different log levels and verify per-process log files are created."""
    # Get the current process ID
    process_id = os.getpid()
    
    # Configure logging for this process
    setup_logging()
    
    # Get logger for this test
    logger = logging.getLogger(f"test.process{process_num}")
    
    # Log process information
    logger.info("Starting test in process %d (PID: %d)", process_num, process_id)
    
    # Test different log levels
    logger.debug("Debug message from process %d", process_num)
    logger.info("Info message from process %d", process_num)
    logger.warning("Warning message from process %d", process_num)
    logger.error("Error message from process %d", process_num)
    logger.critical("Critical message from process %d", process_num)
    
    # Log some structured data
    logger.info(
        "User login attempt from process %d", process_num,
        extra={
            "user_id": 100 + process_num,
            "ip": f"192.168.1.{process_num}",
            "status": "success"
        }
    )
    
    # Get the log file paths
    log_dir = Path(settings.LOG_DIR)
    app_log_path = log_dir / f"app_{process_id}.log"
    error_log_path = log_dir / f"error_{process_id}.log"
    
    # Make sure the files exist
    app_log_path.parent.mkdir(exist_ok=True, parents=True)
    
    # Verify log files were created
    print(f"\nProcess {process_num} (PID: {process_id}) log files:")
    print(f"- Application logs: {app_log_path.absolute()}")
    print(f"- Error logs: {error_log_path.absolute()}")
    
    # Flush logs to ensure they're written to disk
    for handler in logging.root.handlers:
        handler.flush()
    
    # Return the paths for verification
    return {
        "process_num": process_num,
        "process_id": process_id,
        "app_log": app_log_path,
        "error_log": error_log_path
    }

def test_multiprocess_logging():
    """Test logging from multiple processes."""
    print("Testing logging from multiple processes...")
    
    # Test logging from multiple processes
    with ProcessPoolExecutor(max_workers=3) as executor:
        futures = [
            executor.submit(test_logging, i)
            for i in range(3)
        ]
        
        # Wait for all processes to complete
        results = [future.result() for future in futures]
    
    # Print summary
    print("\nTest completed for all processes. Log files created:")
    for result in results:
        print(f"\nProcess {result['process_num']} (PID: {result['process_id']}):")
        print(f"- App log: {result['app_log']}")
        print(f"- Error log: {result['error_log']}")
        
        # Print last 3 lines of each log file
        for log_type in ['app_log', 'error_log']:
            log_path = result[log_type]
            if log_path.exists():
                print(f"\nLast 3 lines of {log_type} for process {result['process_num']}:")
                try:
                    with open(log_path, 'r') as f:
                        lines = f.readlines()[-3:]
                        print(''.join(lines).strip())
                except Exception as e:
                    print(f"Error reading {log_path}: {e}")

if __name__ == "__main__":
    # Test single process logging
    print("Testing single process logging...")
    test_logging()
    
    # Test multi-process logging
    test_multiprocess_logging()
