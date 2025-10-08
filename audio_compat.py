"""
Audio compatibility layer for playing sound files.
Provides fallback support for different audio libraries.
"""

import os
import sys

# Try to import playsound first (legacy support)
try:
    from playsound import playsound as _playsound_original
    _audio_backend = "playsound"

    def playsound(sound_path, block=True):
        """Play sound using playsound library"""
        if os.path.exists(sound_path):
            _playsound_original(sound_path, block)
        else:
            print(f"Warning: Audio file not found: {sound_path}", file=sys.stderr)

except ImportError:
    # Fallback to pygame
    try:
        import pygame
        pygame.mixer.init()
        _audio_backend = "pygame"

        def playsound(sound_path, block=True):
            """Play sound using pygame library"""
            if not os.path.exists(sound_path):
                print(f"Warning: Audio file not found: {sound_path}", file=sys.stderr)
                return

            try:
                sound = pygame.mixer.Sound(sound_path)
                sound.play()

                if block:
                    # Wait for sound to finish
                    import time
                    while pygame.mixer.get_busy():
                        time.sleep(0.01)
            except Exception as e:
                print(f"Warning: Failed to play audio {sound_path}: {e}", file=sys.stderr)

    except ImportError:
        # No audio library available
        _audio_backend = "none"

        def playsound(sound_path, block=True):
            """Dummy playsound function when no audio library is available"""
            print(f"Warning: No audio library available. Would play: {sound_path}", file=sys.stderr)


# Print backend info on first import (optional, can be removed)
if __name__ != "__main__":
    print(f"Audio backend: {_audio_backend}", file=sys.stderr)


__all__ = ['playsound']
