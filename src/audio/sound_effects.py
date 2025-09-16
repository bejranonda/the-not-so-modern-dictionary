"""
Sound effects management for the dictionary application.
"""
import random
from typing import List

import playsound

from ..config.settings import AUDIO_PATHS
from ..utils.logger import app_logger


class SoundManager:
    """Manages sound effects for the application."""

    def __init__(self):
        self.audio_paths = AUDIO_PATHS

    def play_flipping_sound(self) -> None:
        """Play a random page flipping sound."""
        try:
            sound_file = random.choice(self.audio_paths["flipping"])
            app_logger.info(f"Playing flipping sound: {sound_file}")
            playsound.playsound(sound_file)
        except Exception as e:
            app_logger.error(f"Error playing flipping sound: {e}")

    def play_invalid_sound(self) -> None:
        """Play an invalid input sound."""
        try:
            sound_file = random.choice(self.audio_paths["invalid"])
            app_logger.info(f"Playing invalid sound: {sound_file}")
            playsound.playsound(sound_file)
        except Exception as e:
            app_logger.error(f"Error playing invalid sound: {e}")

    def play_correct_sound(self) -> None:
        """Play a correct input sound."""
        try:
            playsound.playsound(self.audio_paths["correct"])
        except Exception as e:
            app_logger.error(f"Error playing correct sound: {e}")

    def play_system_start_sound(self) -> None:
        """Play system startup sound."""
        try:
            playsound.playsound(self.audio_paths["system_start"])
        except Exception as e:
            app_logger.error(f"Error playing system start sound: {e}")

    def play_start_beep(self) -> None:
        """Play start recording beep."""
        try:
            playsound.playsound(self.audio_paths["start_beep"])
        except Exception as e:
            app_logger.error(f"Error playing start beep: {e}")

    def play_end_beep(self) -> None:
        """Play end recording beep."""
        try:
            playsound.playsound(self.audio_paths["end_beep"])
        except Exception as e:
            app_logger.error(f"Error playing end beep: {e}")

    def play_sound(self, sound_type: str) -> None:
        """
        Play a sound by type.

        Args:
            sound_type: Type of sound to play ('flipping', 'invalid', 'correct', etc.)
        """
        sound_methods = {
            'flipping': self.play_flipping_sound,
            'invalid': self.play_invalid_sound,
            'correct': self.play_correct_sound,
            'system_start': self.play_system_start_sound,
            'start_beep': self.play_start_beep,
            'end_beep': self.play_end_beep,
        }

        method = sound_methods.get(sound_type)
        if method:
            method()
        else:
            app_logger.warning(f"Unknown sound type: {sound_type}")

    def validate_audio_files(self) -> List[str]:
        """
        Validate that all audio files exist.

        Returns:
            List of missing audio files
        """
        import os
        missing_files = []

        for sound_type, paths in self.audio_paths.items():
            if isinstance(paths, list):
                for path in paths:
                    if not os.path.exists(path):
                        missing_files.append(path)
            else:
                if not os.path.exists(paths):
                    missing_files.append(paths)

        if missing_files:
            app_logger.warning(f"Missing audio files: {missing_files}")

        return missing_files