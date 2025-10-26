import logging
import os
import sys
from logging.handlers import RotatingFileHandler

# Global logger configuration
_loggers_configured = set()
_app_log_file = "./logs/tubentor.log"


def setup_logger(
    name: str,
    level: int = logging.INFO,
    max_size: int = 50 * 1024 * 1024,  # 50MB for centralized log
    backup_count: int = 10,
) -> logging.Logger:
    """
    Configure logger with consistent formatting for centralized logging.
    All modules will log to the same application log file.
    """
    logger = logging.getLogger(name)

    # Avoid duplicate handlers
    if name in _loggers_configured:
        return logger

    logger.setLevel(level)

    # Create formatter with module name for better tracing
    formatter = logging.Formatter(
        "%(asctime)s - [%(name)s] - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    # Console handler for development
    if not any(isinstance(h, logging.StreamHandler) for h in logger.handlers):
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(formatter)
        console_handler.setLevel(logging.INFO)  # Only INFO and above to console
        logger.addHandler(console_handler)

    # File handler for centralized logging
    if not any(isinstance(h, RotatingFileHandler) for h in logger.handlers):
        # Ensure directory exists
        os.makedirs(os.path.dirname(_app_log_file), exist_ok=True)

        file_handler = RotatingFileHandler(
            _app_log_file, maxBytes=max_size, backupCount=backup_count
        )
        file_handler.setFormatter(formatter)
        file_handler.setLevel(logging.DEBUG)  # Capture all levels in file
        logger.addHandler(file_handler)

    # Prevent propagation to root logger to avoid duplicate logs
    logger.propagate = False
    _loggers_configured.add(name)

    return logger


def get_app_logger(component: str = "app") -> logging.Logger:
    """
    Get a logger for a specific component.
    This is the preferred way to get loggers in the application.
    """
    return setup_logger(f"incident_mgmt.{component}")


# Convenience functions for common components
def get_controller_logger(controller_name: str) -> logging.Logger:
    return get_app_logger(f"controller.{controller_name}")


def get_service_logger(service_name: str) -> logging.Logger:
    return get_app_logger(f"service.{service_name}")


def get_task_logger(task_name: str) -> logging.Logger:
    return get_app_logger(f"task.{task_name}")


def get_middleware_logger() -> logging.Logger:
    return get_app_logger("middleware")
