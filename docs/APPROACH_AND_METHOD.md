# Approach & Method: Bug Hunting and Validation

This document records the **method** used to bug-hunt, test and validate
**The Not-So-Modern Dictionary**, so the process is repeatable by anyone
(human or AI) returning to the project.

---

## 1. Goal

Find real, reproducible defects in the maintained `src/` codebase, fix them with
minimal risk, validate the fixes without the full kiosk hardware, and bring the
documentation back into agreement with the code.

## 2. Constraints of the environment

The full kiosk needs PyQt5, OpenCV, a camera, a printer and an audio device —
none guaranteed in a dev/CI box. So the method deliberately separates:
- **pure logic** (database, easter eggs, audio backend selection, console) —
  testable headlessly, and
- **hardware/GUI surface** (kiosk, camera, printing, live audio) — validated by
  reasoning + import/compile checks rather than execution.

## 3. Method (step by step)

### Step 1 — Map the codebase
List the tree; identify the two codebases (`src/` vs legacy root scripts); read
`README`, `INSTALLATION`, `CHANGELOG` to learn intended behaviour and claims.

### Step 2 — Static checks first (cheap, high-signal)
```bash
python -m py_compile $(git ls-files '*.py')      # everything must compile
```
Then grep for risk patterns:
- hard imports of optional/removed packages (`import playsound`),
- imports of modules that may not exist (`from .ui.console import ...`),
- direct dict subscripting on external data (`entry["meaning"]`),
- doc claims vs reality (paths, database type, dead doc links).

### Step 3 — Cross-check docs against code
Every concrete claim in the docs is a testable assertion: file paths
(`assets/templates/` vs `template/`), database type (JSON vs SQLite), referenced
files (`CLAUDE.md`, `REFACTORING.md`), and feature behaviour (the advertised
audio fallback). Each mismatch is logged as a bug.

### Step 4 — Reproduce / confirm each candidate
- Confirmed the audio crash by checking `requirements.txt` (playsound commented
  out) against the hard `import playsound` in `src/audio/*` and that
  `audio_compat.py` was imported nowhere.
- Confirmed the debug-mode crash by checking that `src/ui/console.py` did not
  exist while `app.py` imported it.

### Step 5 — Fix with the smallest safe change
- Add a focused compatibility layer (`src/audio/player.py`) and redirect imports.
- Add the missing module (`src/ui/console.py`).
- Make package `__init__` lazy so fixes are importable headlessly.
- Harden the one fragile lookup (`.get()` in `search_entries`).
- Leave the frozen legacy scripts untouched; document their limitation instead.

### Step 6 — Validate
- Write `tests/test_validation.py` covering database CRUD/merge/search/stats,
  easter-egg outputs, audio-backend import safety, and headless console
  construction.
- Run `python -m unittest discover -s tests` → all green.
- Re-run `py_compile` across the repo.

### Step 7 — Reconcile documentation
Update `README`, `INSTALLATION`, `CHANGELOG`; create the knowledge/known-issues/
guideline/approach docs; fix dead links. A fix isn't done until the docs match.

## 4. Findings from this pass

| # | Severity | Issue | Fix |
|---|---|---|---|
| 1 | Critical | `import playsound` crashed startup (playsound removed from requirements) | `src/audio/player.py` compat layer; redirected imports; lazy audio `__init__` |
| 2 | High | Debug mode imported non-existent `ConsoleInterface` | Added `src/ui/console.py`; lazy ui `__init__` |
| 3 | Low | `search_entries` could `KeyError` on malformed entries | Use `.get()` |
| 4 | Docs | SQLite vs JSON; wrong asset paths; dead doc links | Corrected README/INSTALLATION; added docs |

## 5. Validation matrix

| Subsystem | How validated | Result |
|---|---|---|
| `SlangDatabase` | Unit tests (add/get/dupe/merge/search/stats/persistence) | ✅ |
| `EasterEggManager` | Unit tests (page count, flags, message types) | ✅ |
| `src/audio/player` | Import-safety + missing-file no-raise test | ✅ |
| `ConsoleInterface` | Headless construction + `show_statistics` | ✅ |
| Whole repo | `py_compile` on all tracked `.py` | ✅ |
| Kiosk/camera/printer/live audio | Static review only (no hardware) | ⚠️ not executed |

## 6. Principles applied

1. **Cheapest signal first** — compile and grep before running anything.
2. **Reproduce before fixing** — every fix maps to a confirmed defect.
3. **Smallest safe change** — focused fixes; freeze the legacy build.
4. **Make it testable** — lazy imports so logic runs without hardware.
5. **Docs are part of the fix** — code and documentation must agree.

## 7. Re-running this method later

```bash
python -m py_compile $(git ls-files '*.py')
python -m unittest discover -s tests
grep -rn "import playsound" src/        # should return nothing
python -c "from src.audio.player import audio_backend; print(audio_backend)"
```
