#!/usr/bin/env python3
"""
Entry point for The Not-So-Modern Dictionary application.

This is the main entry point that maintains compatibility with the original
application while using the refactored codebase.
"""
import sys
import os
from pathlib import Path

# Add src directory to Python path
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

from src.app import main
from src.config.settings import AppMode


def run_normal_edition():
    """Run the normal edition of the application."""
    main(AppMode.NORMAL)


def run_lastweek_edition():
    """Run the last week edition of the application."""
    main(AppMode.LAST_WEEK)


def run_kiosk_mode():
    """Run the application in kiosk mode."""
    main(AppMode.KIOSK)


def run_debug_mode():
    """Run the application in debug/console mode."""
    main(AppMode.DEBUG)


if __name__ == "__main__":
    # Default to kiosk mode (matches original behavior)
    run_kiosk_mode()