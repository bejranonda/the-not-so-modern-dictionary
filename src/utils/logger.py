"""
Logging utilities for The Not-So-Modern Dictionary application.
"""
import logging
import os
from datetime import datetime
from pathlib import Path
from typing import Optional

from ..config.settings import DATABASE_SETTINGS, BASE_DIR


class DictionaryLogger:
    """Custom logger for the dictionary application."""

    def __init__(self, name: str = "dictionary_app", log_file: Optional[str] = None):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.INFO)

        # Avoid duplicate handlers
        if not self.logger.handlers:
            self._setup_handlers(log_file)

    def _setup_handlers(self, log_file: Optional[str] = None):
        """Setup logging handlers for console and file output."""
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )

        # Console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        console_handler.setFormatter(formatter)
        self.logger.addHandler(console_handler)

        # File handler
        if log_file is None:
            log_file = str(BASE_DIR / "app.log")

        file_handler = logging.FileHandler(log_file, encoding='utf-8')
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(formatter)
        self.logger.addHandler(file_handler)

    def info(self, message: str):
        """Log info message."""
        self.logger.info(message)

    def error(self, message: str):
        """Log error message."""
        self.logger.error(message)

    def warning(self, message: str):
        """Log warning message."""
        self.logger.warning(message)

    def debug(self, message: str):
        """Log debug message."""
        self.logger.debug(message)


def log_request_message(message: str):
    """
    Log request messages to the request log file.
    Maintains compatibility with existing code.
    """
    log_file = DATABASE_SETTINGS["request_log_file"]
    with open(log_file, "a", encoding="utf-8") as f:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        f.write(f"[{timestamp}] {message}\n")


# Global logger instance
app_logger = DictionaryLogger()