"""
Audio package for The Not-So-Modern Dictionary.

Symbols are exposed lazily so that lightweight consumers (for example the
``player`` playback compatibility layer, or tests) can be imported without
eagerly pulling in optional dependencies such as gTTS, SpeechRecognition,
sounddevice or scipy that ``SpeechEngine``/``SoundManager`` require.
"""

__all__ = ["SpeechEngine", "SoundManager"]


def __getattr__(name):
    if name == "SpeechEngine":
        from .speech import SpeechEngine
        return SpeechEngine
    if name == "SoundManager":
        from .sound_effects import SoundManager
        return SoundManager
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
