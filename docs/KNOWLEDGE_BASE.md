# Knowledge Base

A reference for understanding **The Not-So-Modern Dictionary** codebase: how the
pieces fit together, where state lives, and the facts a developer needs before
changing anything.

---

## 1. What the project is

A participatory art installation (Bangkok Kunsthalle, June–August 2025). A
motion-activated kiosk invites visitors to contribute slang words; each visitor
takes home a freshly printed, personalized mini-dictionary booklet. The software
collected 534 unique slang terms from 462 contributors.

## 2. Two parallel codebases

| | Location | Purpose |
|---|---|---|
| **Refactored** (v2.0+) | `src/` | Modular, maintained code. Entry point: `main.py`. **All new work goes here.** |
| **Legacy** | root-level `thai_slang_*.py`, `greetings*.py`, `slang_pdf_generator*.py`, `input_slang_utils.py` | Original exhibition code, frozen as a deployment fallback. |

Both share the same `assets/`, the same JSON database, and the same templates.

## 3. Module map (`src/`)

```
src/
├── app.py                 # DictionaryApp orchestrator; mode dispatch; instance-kill; restart
├── config/settings.py     # All paths, probabilities, timings, greeting strings, AppMode
├── core/
│   ├── database.py        # SlangDatabase: JSON CRUD, search, stats, merge
│   └── easter_eggs.py     # EasterEggManager: probability rolls + message banks
├── audio/
│   ├── player.py          # playsound→pygame→no-op compatibility layer (import this!)
│   ├── speech.py          # SpeechEngine: gTTS TTS + speech recognition (threaded)
│   └── sound_effects.py   # SoundManager: sound-effect playback + asset validation
├── ui/
│   ├── kiosk.py           # SlangKiosk: PyQt5 full-screen 7-step interface + camera
│   └── console.py         # ConsoleInterface: headless text UI for debug mode/tests
├── pdf/generator.py       # PDFGenerator: ReportLab booklet, fonts, templates, fortunes
└── utils/
    ├── logger.py          # DictionaryLogger (console+file, UTF-8 safe) + request log
    └── requests.py        # check_special_requests/check_routine_requests (live exec)
```

The package `__init__` files for `src/ui` and `src/audio` use **lazy** `__getattr__`
exports so lightweight consumers (console mode, the player, tests) don't drag in
PyQt5 / OpenCV / gTTS.

## 4. Application modes (`AppMode` in `config/settings.py`)

| Mode | Constant | Behaviour |
|---|---|---|
| Kiosk | `"kiosk"` | Full-screen GUI, camera motion detection (default; `main.py`) |
| Normal | `"normal"` | Falls through to kiosk in the current implementation |
| Last week | `"lastweek"` | Special final-week edition content |
| Debug | `"debug"` | Headless `ConsoleInterface`, no GUI/camera/printer |

Helpers in `main.py`: `run_kiosk_mode`, `run_normal_edition`,
`run_lastweek_edition`, `run_debug_mode`.

## 5. Data & state

- **Live database:** `user_added_slang.json` (project root), auto-saved after
  every add/merge. Schema:
  ```json
  {
    "word_lowercase": {
      "word": "Original Case",
      "meaning": "Definition text",
      "example": "Usage example",
      "author": "Contributor",
      "timestamp": "ISO-8601",
      "usage_count": 0
    }
  }
  ```
  Keys are `word.lower()`, giving case-insensitive lookup. `merge_entry`
  concatenates meanings with `"; "` so multiple definitions of one word coexist.
- **Seed data:** `assets/templates/initial_slang_database.json`.
- **Fortunes:** `assets/templates/th-en-ln_slang_predictions_99.json` (standard)
  and `..._lastweek.json` (final week); trilingual Thai/English/Lao-Khmer.
- **Logs:** `app.log` (root) for application logging; `request_log.txt` for the
  request-message stream.

## 6. Easter-egg probabilities

Configured in `config/settings.py::EASTER_EGG_SETTINGS` and
`core/easter_eggs.py`:

| Egg | Probability | Effect |
|---|---|---|
| Jackpot | 10% | 8-page booklet instead of 1 |
| System hacked | 5% | Full-database dump page |
| AI fortune / special content | 15% (fortune), 10%/5% (greetings) | Extra fortune/greeting flavour |

> Note: jackpot/hacked probabilities live in `EASTER_EGG_SETTINGS`; the
> greeting/fortune probabilities are currently hard-coded in
> `should_show_special_content()`. Centralising them is a good future cleanup.

## 7. Audio architecture (important)

- `playsound` is **removed** from `requirements.txt` (Python 3.13+ incompatible).
- Always import playback via `from src.audio.player import playsound`.
- `player.audio_backend` reports the active backend: `"playsound"`, `"pygame"`,
  or `"none"`.
- TTS/audio must never block the PyQt5 UI thread — `SpeechEngine` plays in daemon
  threads; in the kiosk use `QTimer.singleShot()` to defer audio.

## 8. PDF generation pipeline (`pdf/generator.py`)

1. Select template assets from `assets/templates/`.
2. Assemble content: the visitor's word as "Latest Entry" + random DB entries
   (count influenced by easter eggs) + statistics footer.
3. Register fonts from `assets/fonts/` (Kinnari for Thai, Noto Emoji, Noto Sans
   Khmer). Missing fonts → glyphs silently dropped.
4. Append a fortune page from the prediction templates.
5. Output `output/slang_dictionary.pdf` and send to the platform printer.

## 9. Hardware integration

- **Motion detection:** OpenCV frame-differencing in standby triggers greeting.
- **Idle timers:** 30 s → "are you still there?" warning; 60 s → return to
  standby (`KIOSK_SETTINGS`).
- **Printing:** platform-specific print command branches by `platform.system()`.

## 10. Quick commands

```bash
python main.py                                   # kiosk (default)
python -c "from main import run_debug_mode; run_debug_mode()"   # headless console
python -m unittest discover -s tests             # validation suite
python -m py_compile $(git ls-files '*.py')      # syntax check everything
```
