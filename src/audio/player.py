"""
Audio playback compatibility layer.

The original exhibition code relied on the ``playsound`` library. ``playsound``
is no longer compatible with Python 3.13+ and has been removed from
``requirements.txt``. This module provides a single ``playsound()`` function
that transparently picks the best available backend at import time:

1. ``playsound``  – used when the legacy library is installed.
2. ``pygame``     – the Python 3.13+ compatible fallback (shipped in requirements).
3. no-op          – when no audio backend is available, a warning is logged and
                    playback is skipped so the application keeps running.

All application audio (speech and sound effects) must import ``playsound`` from
this module rather than importing the ``playsound`` package directly, otherwise
a fresh install that only has ``pygame`` will crash on startup with
``ModuleNotFoundError: No module named 'playsound'``.
"""

import os
import sys

# Backend currently in use ("playsound", "pygame" or "none"). Exposed for
# diagnostics and tests.
audio_backend = "none"


def _make_playsound():
    """Select the best available audio backend and return a playsound callable."""
    global audio_backend

    # 1. Legacy playsound library (if it happens to be installed).
    try:
        from playsound import playsound as _playsound_original

        audio_backend = "playsound"

        def _play(sound_path, block=True):
            if not os.path.exists(sound_path):
                print(f"Warning: Audio file not found: {sound_path}", file=sys.stderr)
                return
            _playsound_original(sound_path, block)

        return _play
    except Exception:
        pass

    # 2. pygame fallback (Python 3.13+ compatible, shipped in requirements.txt).
    try:
        import pygame

        if not pygame.mixer.get_init():
            pygame.mixer.init()
        audio_backend = "pygame"

        def _play(sound_path, block=True):
            if not os.path.exists(sound_path):
                print(f"Warning: Audio file not found: {sound_path}", file=sys.stderr)
                return
            try:
                sound = pygame.mixer.Sound(sound_path)
                sound.play()
                if block:
                    import time
                    while pygame.mixer.get_busy():
                        time.sleep(0.01)
            except Exception as exc:  # pragma: no cover - hardware dependent
                print(
                    f"Warning: Failed to play audio {sound_path}: {exc}",
                    file=sys.stderr,
                )

        return _play
    except Exception:
        pass

    # 3. No audio backend available – degrade gracefully instead of crashing.
    audio_backend = "none"

    def _play(sound_path, block=True):  # pragma: no cover - trivial
        print(
            f"Warning: No audio backend available. Skipping playback: {sound_path}",
            file=sys.stderr,
        )

    return _play


playsound = _make_playsound()

__all__ = ["playsound", "audio_backend"]
