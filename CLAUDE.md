# CLAUDE.md

Guidance for AI assistants (and humans) working in this repository.

## Project in one paragraph

**The Not-So-Modern Dictionary** is a participatory art installation: a
motion-activated PyQt5 kiosk where visitors contribute slang definitions and
receive a freshly printed, personalized mini-dictionary booklet (with easter
eggs and a fortune page). It ran at Bangkok Kunsthalle, June–August 2025, and
collected 534 slang terms from 462 contributors.

## Repository layout

- `main.py` — entry point into the **refactored** code in `src/`.
- `src/` — **the maintained codebase. Do new work here.**
- Root `thai_slang_*.py`, `greetings*.py`, `slang_pdf_generator*.py`,
  `input_slang_utils.py` — **frozen legacy** exhibition code (deployment
  fallback). Do not refactor unless asked.
- `assets/` — fonts (`assets/fonts/`), audio, and templates (`assets/templates/`).
- `tests/` — headless validation suite.
- `docs/` — knowledge base, known issues, guidelines, approach & method.

See `docs/KNOWLEDGE_BASE.md` for the full module map.

## Golden rules

1. **Audio imports:** inside `src/`, use `from src.audio.player import playsound`.
   Never `import playsound` directly — it is not installed (removed from
   `requirements.txt` for Python 3.13+).
2. **Keep `src/ui` and `src/audio` `__init__` lazy** (`__getattr__`). Don't add
   eager PyQt5/OpenCV/gTTS imports there, or headless/console/test paths break.
3. **Database entries are external data** — use `entry.get(key, default)`.
4. **Never block the PyQt5 UI thread** with TTS/audio; use threads or
   `QTimer.singleShot()`.
5. **Leave the legacy root scripts alone** unless explicitly instructed.
6. **`src/utils/requests.py` runs `exec`** — a trusted-kiosk live-debug hook.
   Don't broaden it; treat it as an RCE surface.

## Before you commit

```bash
python -m py_compile $(git ls-files '*.py')   # syntax check
python -m unittest discover -s tests          # validation suite (must be green)
```

Update docs alongside code: `README.md`, `CHANGELOG.md`,
`docs/KNOWN_ISSUES.md`, `docs/KNOWLEDGE_BASE.md`. Broken file references are bugs.

## Running

```bash
python main.py                                                   # kiosk (default)
python -c "from main import run_debug_mode; run_debug_mode()"    # headless console
python -c "from main import run_lastweek_edition; run_lastweek_edition()"
```

## Where to read more

- `docs/KNOWLEDGE_BASE.md` — architecture, data, probabilities, pipelines.
- `docs/KNOWN_ISSUES.md` — current limitations and workarounds.
- `docs/DEVELOPMENT_GUIDELINES.md` — coding standards.
- `docs/APPROACH_AND_METHOD.md` — bug-hunting & validation methodology.
- `CHANGELOG.md` — version history.
