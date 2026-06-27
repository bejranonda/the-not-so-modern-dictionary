# Development Guidelines

Conventions and rules for contributing to **The Not-So-Modern Dictionary**.
Read [KNOWLEDGE_BASE.md](KNOWLEDGE_BASE.md) first for the lay of the land.

---

## 1. Where to make changes

- **Do new work in `src/`.** The root-level `thai_slang_*.py` scripts are the
  frozen legacy exhibition build kept as a deployment fallback — do not refactor
  them unless explicitly asked.
- Keep the two codebases behaviourally compatible where they share data
  (`user_added_slang.json`, `assets/`).

## 2. Imports & dependencies

- **Audio:** import playback via `from src.audio.player import playsound`.
  Never `import playsound` directly inside `src/` — `playsound` is not a
  guaranteed dependency (removed from `requirements.txt` for Python 3.13+).
- **Keep package `__init__` light.** `src/ui` and `src/audio` use lazy
  `__getattr__` exports so headless consumers don't import PyQt5/OpenCV/gTTS.
  Preserve that — don't add eager heavy imports to those `__init__.py` files.
- Add any new third-party dependency to `requirements.txt` with a minimum
  version, and note Python-version caveats inline (as done for `playsound`).

## 3. Config over constants

- Paths, probabilities, timings and message banks belong in
  `src/config/settings.py`, not scattered as literals. When you find a hard-coded
  value that belongs there (e.g. the greeting/fortune probabilities in
  `easter_eggs.py`), prefer moving it.
- Use `pathlib.Path` for all filesystem paths (cross-platform). Never hard-code
  `/` or `\` separators.

## 4. Robustness

- Treat database entries as possibly-incomplete dicts: use `entry.get(key, default)`
  rather than `entry[key]`.
- Wrap I/O, audio, camera and subprocess calls in `try/except` and log via
  `app_logger`; the kiosk must keep running through transient failures.
- Never let TTS/audio block the PyQt5 UI thread. Use daemon threads
  (`SpeechEngine` already does) or `QTimer.singleShot()` in the kiosk.

## 5. Logging

- Use the shared `app_logger` (`from ..utils.logger import app_logger`).
- Levels: `info` for lifecycle/flow, `warning` for recoverable problems,
  `error` for failures, `debug` for detail. The file handler captures `DEBUG`;
  the console handler shows `INFO`+ and is UTF-8 safe for Thai/emoji.

## 6. Testing

- Add tests to `tests/` for any logic that can run without GUI/hardware
  (database, easter eggs, audio compat, console, PDF helpers that don't print).
- Tests must not require PyQt5, OpenCV, a camera, a printer or an audio device.
  If a unit needs them, isolate the pure logic so it can be tested headlessly.
- Run before every commit:
  ```bash
  python -m unittest discover -s tests
  python -m py_compile $(git ls-files '*.py')
  ```

## 7. Commits & branches

- Develop on the assigned feature branch; do not push to `main` without
  permission.
- Write clear, imperative commit subjects ("Fix audio import crash"), with a
  body explaining the *why* when non-obvious.
- Keep functional fixes and documentation in coherent, reviewable commits.

## 8. Documentation duty

When you change behaviour, update the relevant docs in the same change:
- `README.md` — user-facing behaviour, setup, architecture summary.
- `CHANGELOG.md` — a dated entry under a new version.
- `docs/KNOWN_ISSUES.md` — move fixed items to Resolved; add new caveats.
- `docs/KNOWLEDGE_BASE.md` — keep the module map and facts accurate.
- `CLAUDE.md` — keep AI-assistant guidance in sync.

Broken cross-references are bugs: if you reference a file, make sure it exists.

## 9. Security-sensitive areas

- `src/utils/requests.py` runs arbitrary Python via `exec`. It is a deliberate
  live-debug hook for a trusted kiosk only. Do not broaden its surface, and never
  ship the trigger/script files to untrusted deployments.

## 10. Style

- Match the surrounding code: type hints on public methods, module/class/method
  docstrings, descriptive names.
- Prefer small, single-purpose methods. Keep the kiosk's step flow readable.
