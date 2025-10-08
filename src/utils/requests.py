"""Remote request management utilities.

This module provides functionality for checking and executing special/routine
requests for live debugging and updates during exhibition.
"""

import os
from pathlib import Path
from ..utils.logger import app_logger


def check_special_requests() -> None:
    """Check for and execute special request scripts.

    Looks for 'do_request_special_routine' file and executes Python code
    from 'request_script.txt' if found.
    """
    special_flag = Path("do_request_special_routine")
    script_path = Path("request_script.txt")

    if special_flag.exists():
        app_logger.info("🔧 Special request flag detected")
        if script_path.exists():
            try:
                with open(script_path, 'r', encoding='utf-8') as f:
                    script_code = f.read()
                app_logger.info("Executing special request script...")
                exec(script_code)
                app_logger.info("✅ Special request completed")
            except Exception as e:
                app_logger.error(f"Failed to execute special request: {e}")
        else:
            app_logger.warning("Special request flag found but no script file")


def check_routine_requests() -> None:
    """Check for and execute routine request scripts.

    Executes periodic tasks defined in 'request_routine_script.txt'.
    """
    routine_script = Path("request_routine_script.txt")

    if routine_script.exists():
        try:
            with open(routine_script, 'r', encoding='utf-8') as f:
                script_code = f.read()
            if script_code.strip():  # Only execute if not empty
                app_logger.info("Executing routine request script...")
                exec(script_code)
                app_logger.debug("✅ Routine request completed")
        except Exception as e:
            app_logger.error(f"Failed to execute routine request: {e}")
