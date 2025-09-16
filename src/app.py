"""
Main application module for The Not-So-Modern Dictionary.
"""
import sys
import os
import signal
import subprocess
import platform
from typing import Optional

from PyQt5.QtWidgets import QApplication

from .config.settings import AppMode, KIOSK_SETTINGS
from .core.database import SlangDatabase
from .core.easter_eggs import EasterEggManager
from .audio.speech import SpeechEngine
from .audio.sound_effects import SoundManager
from .utils.logger import app_logger, log_request_message
from .ui.kiosk import SlangKiosk


class DictionaryApp:
    """Main application class for The Not-So-Modern Dictionary."""

    def __init__(self, mode: str = AppMode.NORMAL):
        self.mode = mode
        self.database = SlangDatabase()
        self.easter_eggs = EasterEggManager()
        self.speech_engine = SpeechEngine()
        self.sound_manager = SoundManager()

        # Validate audio files on startup
        missing_files = self.sound_manager.validate_audio_files()
        if missing_files:
            app_logger.warning(f"Missing audio files: {missing_files}")

    def kill_previous_instance(self) -> None:
        """Kill any previous instances of the application."""
        current_pid = os.getpid()
        script_name = os.path.basename(sys.argv[0])
        script_path = os.path.abspath(sys.argv[0])
        system_platform = platform.system()

        app_logger.info(f"Checking for duplicate instances on {system_platform}")
        app_logger.debug(f"Current PID: {current_pid}, Script: {script_name}")

        try:
            if system_platform == "Windows":
                self._kill_windows_instances(current_pid, script_name)
            else:
                self._kill_unix_instances(current_pid, script_path)

        except Exception as e:
            app_logger.error(f"Error while killing previous instances: {e}")

    def _kill_windows_instances(self, current_pid: int, script_name: str) -> None:
        """Kill previous instances on Windows."""
        try:
            result = subprocess.run(
                ["wmic", "process", "get", "ProcessId,CommandLine"],
                capture_output=True, text=True, check=True
            )

            for line in result.stdout.splitlines():
                if ("python" in line and script_name in line and
                    str(current_pid) not in line):
                    parts = line.strip().split()
                    if parts and parts[-1].isdigit():
                        pid = parts[-1]
                        app_logger.info(f"🛑 Killing PID (Windows): {pid}")
                        subprocess.run(["taskkill", "/F", "/PID", pid])

            app_logger.info("✅ No previous instances found (Windows)")

        except subprocess.CalledProcessError as e:
            app_logger.error(f"Error checking Windows processes: {e}")

    def _kill_unix_instances(self, current_pid: int, script_path: str) -> None:
        """Kill previous instances on Unix/macOS."""
        try:
            result = subprocess.run(
                ["lsof", "+D", os.path.dirname(script_path)],
                capture_output=True, text=True
            )

            found = False
            for line in result.stdout.strip().split("\n"):
                if script_path in line and f"{current_pid}" not in line:
                    try:
                        parts = line.split()
                        pid = int(parts[1])
                        app_logger.info(f"🛑 Killing PID (Unix/macOS): {pid}")
                        os.kill(pid, signal.SIGKILL)
                        found = True
                    except (ValueError, IndexError, ProcessLookupError) as e:
                        app_logger.warning(f"Failed to parse or kill process: {e}")

            if not found:
                app_logger.info("✅ No previous instances found (Unix/macOS)")

        except subprocess.CalledProcessError:
            # lsof command failed, which is not critical
            app_logger.debug("lsof command failed (not critical)")

    def run_kiosk_mode(self) -> None:
        """Run the application in kiosk mode."""
        app_logger.info("🚀 Starting kiosk mode")

        # Play startup sound
        self.sound_manager.play_system_start_sound()

        # Kill previous instances
        self.kill_previous_instance()

        # Generate initial PDF
        from .pdf.generator import PDFGenerator
        pdf_gen = PDFGenerator(mode=self.mode)
        pdf_gen.generate_dictionary_pdf()

        # Start Qt application
        qt_app = QApplication(sys.argv)

        # Create and show kiosk
        kiosk = SlangKiosk(
            database=self.database,
            easter_eggs=self.easter_eggs,
            speech_engine=self.speech_engine,
            sound_manager=self.sound_manager,
            mode=self.mode
        )

        if KIOSK_SETTINGS["fullscreen"]:
            kiosk.showFullScreen()
        else:
            kiosk.show()

        # Run the application
        try:
            sys.exit(qt_app.exec_())
        except Exception as e:
            app_logger.error(f"Kiosk mode error: {e}")
            self.restart_application()

    def run_console_mode(self) -> None:
        """Run the application in console mode for testing."""
        from .ui.console import ConsoleInterface

        app_logger.info("🖥️ Starting console mode")
        console = ConsoleInterface(
            database=self.database,
            speech_engine=self.speech_engine,
            sound_manager=self.sound_manager
        )
        console.run()

    def restart_application(self) -> None:
        """Restart the application."""
        app_logger.info("🔄 Restarting application...")
        self.speech_engine.speak_thai("ระบบเกิดข้อผิดพลาด จะเริ่มใหม่ให้อัตโนมัติค่ะ")

        try:
            subprocess.run([sys.executable] + sys.argv)
        except Exception as e:
            app_logger.error(f"Failed to restart application: {e}")

    def run(self) -> None:
        """Run the application based on the configured mode."""
        # Log startup
        log_request_message("🛫 Starting App...")

        # Check for special requests
        from .utils.requests import check_special_requests, check_routine_requests
        check_special_requests()
        check_routine_requests()

        # Run in appropriate mode
        if self.mode == AppMode.KIOSK:
            self.run_kiosk_mode()
        elif self.mode == AppMode.DEBUG:
            self.run_console_mode()
        else:
            self.run_kiosk_mode()  # Default to kiosk mode

    def cleanup(self) -> None:
        """Clean up resources before shutdown."""
        app_logger.info("🧹 Cleaning up application resources...")

        # Clean up temporary audio files
        self.speech_engine.cleanup_all_temp_files()

        # Save database
        self.database.save_database()

        app_logger.info("✅ Cleanup completed")


def create_app(mode: str = AppMode.NORMAL) -> DictionaryApp:
    """
    Create and configure the dictionary application.

    Args:
        mode: Application mode (normal, lastweek, kiosk, debug)

    Returns:
        Configured DictionaryApp instance
    """
    app = DictionaryApp(mode=mode)
    return app


def main(mode: str = AppMode.KIOSK) -> None:
    """
    Main entry point for the application.

    Args:
        mode: Application mode to run in
    """
    app = None
    try:
        app = create_app(mode)
        app.run()
    except KeyboardInterrupt:
        app_logger.info("Application interrupted by user")
    except Exception as e:
        app_logger.error(f"Fatal application error: {e}")
        raise
    finally:
        if app:
            app.cleanup()


if __name__ == "__main__":
    # Determine mode from command line arguments or default to kiosk
    mode = AppMode.KIOSK
    if len(sys.argv) > 1:
        mode = sys.argv[1]

    main(mode)