# Known Issues

This document tracks known issues, limitations, and their workarounds for
**The Not-So-Modern Dictionary**. Issues are grouped by status.

Last reviewed: 2026-06-26

---

## ✅ Resolved

### 1. Startup crash: `ModuleNotFoundError: No module named 'playsound'`
- **Severity:** Critical (application would not start on a clean install)
- **Affected:** `src/audio/speech.py`, `src/audio/sound_effects.py`
- **Cause:** Both modules did `import playsound` at module load, but `playsound`
  is intentionally **commented out** of `requirements.txt` because it is
  incompatible with Python 3.13+. A clean `pip install -r requirements.txt`
  therefore left `playsound` uninstalled, and importing `SpeechEngine` /
  `SoundManager` (which `src/app.py` does on startup) raised
  `ModuleNotFoundError`. The documented "automatic pygame fallback"
  (`audio_compat.py`) existed but was **never imported** by the `src/` package.
- **Fix:** Added `src/audio/player.py`, a compatibility layer that selects
  `playsound` → `pygame` → silent no-op at import time. `speech.py` and
  `sound_effects.py` now import `playsound` from this layer. The audio package
  `__init__` was also made lazy so the player can be imported without pulling in
  gTTS/SpeechRecognition.
- **Verify:** `python -c "from src.audio.player import playsound, audio_backend; print(audio_backend)"`

### 2. Debug/console mode crash: missing `ConsoleInterface`
- **Severity:** High (documented `run_debug_mode()` did not work)
- **Affected:** `src/app.py` → `run_console_mode()`
- **Cause:** `run_console_mode()` imported `from .ui.console import ConsoleInterface`
  but `src/ui/console.py` did not exist.
- **Fix:** Added `src/ui/console.py` providing a headless `ConsoleInterface`
  (add/search/statistics/easter-egg menu). The UI package `__init__` was made
  lazy so the console can be imported without PyQt5/OpenCV.
- **Verify:** `python -m unittest tests.test_validation.TestConsoleInterface`

### 3. `search_entries` could raise `KeyError`
- **Severity:** Low
- **Affected:** `src/core/database.py`
- **Cause:** `search_entries()` indexed `entry["word"]` / `entry["meaning"]`
  directly, so an entry missing either key raised `KeyError`.
- **Fix:** Switched to `entry.get("word", "")` / `entry.get("meaning", "")`.

### 4. Documentation inaccuracies
- README described the database as **SQLite** in one diagram; it is JSON
  (`user_added_slang.json`). Corrected.
- README referenced asset paths as `template/` and `fonts/`; the real paths are
  `assets/templates/` and `assets/fonts/`. Corrected.
- README "Further Reading" linked to non-existent `REFACTORING.md` and
  `CLAUDE.md`. Links updated to the docs that exist (`CLAUDE.md` added; the
  `docs/` set created).

---

## ⚠️ Open / By design

### A. Legacy root scripts still hard-import `playsound`
- **Affected:** `thai_slang_kiosk*.py`, `thai_slang_dict_main*.py`,
  `thai_slang_dict_generator.py`, `input_slang_utils.py`
- **Status:** Intentionally **not** changed. These root-level files are the
  original exhibition code, preserved verbatim as a deployment fallback (see the
  "Architecture Overview" in the README). They predate the `src/` refactor.
- **Workaround:** Run the application through `main.py` (the refactored `src/`
  entry point), which is unaffected. If you must run a legacy script on
  Python 3.13+, install `playsound` into that environment, or route its imports
  through the root-level `audio_compat.py`.

### B. PDF generation fails silently if Thai fonts are missing
- **Affected:** `src/pdf/generator.py`
- **Status:** Known limitation. ReportLab silently skips glyphs when a font is
  not registered. The required fonts ship in `assets/fonts/` (Kinnari, Noto
  Emoji, Noto Sans Khmer), so this only bites if assets are deleted or moved.
- **Workaround:** Keep `assets/fonts/` intact; check logs for font-registration
  warnings during PDF generation.

### C. Remote request feature executes arbitrary code (`exec`)
- **Affected:** `src/utils/requests.py`
- **Status:** By design, for live debugging during the exhibition. It runs
  Python from `request_script.txt` / `request_routine_script.txt` when a flag
  file is present.
- **Security note:** Only enable on a trusted, physically controlled kiosk.
  Never ship those flag/script files to an untrusted deployment. Treat this as a
  remote-code-execution surface.

### D. Heavy runtime dependencies required for the full kiosk
- The full GUI kiosk needs PyQt5, OpenCV, gTTS, SpeechRecognition, sounddevice,
  scipy, ReportLab, PyMuPDF and PyPDF2. On headless/CI machines, use the
  validation suite (`tests/`) or console/debug mode instead, both of which avoid
  the GUI/vision/audio stacks.

---

## Reporting a new issue

When filing a new issue, please include:
1. Python version and OS.
2. The exact command run (`python main.py`, a `run_*` helper, or a test).
3. The full traceback or log excerpt (`app.log`).
4. Whether you are on the refactored `src/` path or a legacy root script.
