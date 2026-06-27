"""
UI module for The Not-So-Modern Dictionary application.

Symbols are exposed lazily so that importing the headless ``ConsoleInterface``
(used by debug mode and tests) does not pull in heavy GUI/vision dependencies
(PyQt5, OpenCV) required only by ``SlangKiosk``.
"""

__all__ = ["SlangKiosk", "ConsoleInterface"]


def __getattr__(name):
    if name == "SlangKiosk":
        from .kiosk import SlangKiosk
        return SlangKiosk
    if name == "ConsoleInterface":
        from .console import ConsoleInterface
        return ConsoleInterface
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
