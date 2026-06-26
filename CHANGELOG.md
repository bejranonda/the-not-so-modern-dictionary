# Changelog

All notable changes to The Not-So-Modern Dictionary project will be documented in this file.

## [3.1.2] - 2026-06-26

### Bug Fixes - Startup Crashes, Debug Mode & Documentation

A bug-hunting and validation pass on the refactored `src/` codebase, with new
documentation and a headless test suite.

#### Fixed

**Critical: startup crash on clean install (`ModuleNotFoundError: playsound`)**
- `src/audio/speech.py` and `src/audio/sound_effects.py` hard-imported
  `playsound`, which is commented out of `requirements.txt` (incompatible with
  Python 3.13+). Importing `SpeechEngine`/`SoundManager` at startup therefore
  crashed on a clean install. The advertised `audio_compat.py` fallback was never
  imported by `src/`.
- Added `src/audio/player.py`, a backend-selecting compatibility layer
  (`playsound` → `pygame` → silent no-op), and redirected both modules to it.
- Made `src/audio/__init__.py` lazy so the player imports without gTTS/SpeechRecognition.

**High: debug/console mode crashed (missing `ConsoleInterface`)**
- `src/app.py::run_console_mode()` imported `src/ui/console.py`, which did not
  exist; `run_debug_mode()` was broken.
- Added `src/ui/console.py` (headless `ConsoleInterface`) and made
  `src/ui/__init__.py` lazy so console mode works without PyQt5/OpenCV.

**Low: `SlangDatabase.search_entries` could raise `KeyError`**
- Now uses `entry.get(...)` for `word`/`meaning` to tolerate malformed entries.

**Documentation corrections**
- README: database described as JSON (not SQLite); asset paths corrected to
  `assets/templates/` and `assets/fonts/`; dead links to `REFACTORING.md`/
  `CLAUDE.md` replaced.
- INSTALLATION: audio-compatibility section now documents `src/audio/player.py`.

#### Added
- `tests/test_validation.py` — headless validation suite (database, easter eggs,
  audio compatibility, console). No GUI/camera/printer/audio device required.
- `CLAUDE.md` — AI-assistant and developer guidance.
- `docs/KNOWLEDGE_BASE.md`, `docs/KNOWN_ISSUES.md`,
  `docs/DEVELOPMENT_GUIDELINES.md`, `docs/APPROACH_AND_METHOD.md`.

#### Affected files
- `src/audio/player.py` (new), `src/audio/speech.py`, `src/audio/sound_effects.py`,
  `src/audio/__init__.py`
- `src/ui/console.py` (new), `src/ui/__init__.py`
- `src/core/database.py`
- `README.md`, `INSTALLATION.md`, `CHANGELOG.md`
- `tests/test_validation.py` (new), `CLAUDE.md` (new), `docs/*` (new)

## [3.1.1] - 2025-10-08

### Bug Fixes - Windows Compatibility & Critical Errors

This patch release addresses critical bugs affecting Windows deployment and PDF generation that were discovered after the v3.1.0 release.

#### Fixed

**PDF Generation Errors**:
- Fixed `ValueError: empty range in randrange(7, 6)` and `empty range in randrange(7, 7)` errors
- Corrected page calculation logic in all PDF generators:
  - Changed condition from `total_pages > 6` to `total_pages > 8`
  - Changed fallback page value from `6` to `7` to ensure valid page index
- Affected files:
  - `slang_pdf_generator.py` (2 locations)
  - `slang_pdf_generator_lastweek.py` (2 locations)
  - `src/pdf/generator.py` (2 locations)

**Windows Console Encoding**:
- Added UTF-8 encoding support for Windows console output
- Fixed Unicode character display errors for Thai text and emojis
- Configured `stdout` and `stderr` encoding at application startup:
  - `thai_slang_dict_main.py`
  - `thai_slang_dict_main_lastweek.py`
- Updated logger to handle Unicode characters gracefully:
  - `src/utils/logger.py` - Added UTF-8 stream reconfiguration with fallback

**File System Issues**:
- Fixed missing font file path for `NotoSansKhmer-Regular.ttf`:
  - Changed from `"NotoSansKhmer-Regular.ttf"` to `"assets/fonts/NotoSansKhmer-Regular.ttf"`
  - `slang_pdf_generator.py:708`
  - `slang_pdf_generator_lastweek.py:718`
- Added automatic output directory creation to prevent `FileNotFoundError`:
  - `thai_slang_kiosk.py` - Added `os.makedirs("output", exist_ok=True)` in `save_data()` and `save_author_to_latest_entry()`
  - `thai_slang_kiosk_lastweek.py` - Same fixes

#### Added

**New Module**:
- `src/utils/requests.py` - Remote script execution utilities for live debugging
  - `check_special_requests()` - Executes code from `request_script.txt`
  - `check_routine_requests()` - Executes periodic tasks from `request_routine_script.txt`

#### Technical Details

**Files Modified**: 8 files
- `slang_pdf_generator.py` - Font path + randrange fixes (2 locations)
- `slang_pdf_generator_lastweek.py` - Font path + randrange fixes (2 locations)
- `src/pdf/generator.py` - Randrange fixes (2 locations)
- `src/utils/logger.py` - UTF-8 console encoding
- `thai_slang_dict_main.py` - UTF-8 setup at startup
- `thai_slang_dict_main_lastweek.py` - UTF-8 setup at startup
- `thai_slang_kiosk.py` - Directory creation (2 methods)
- `thai_slang_kiosk_lastweek.py` - Directory creation (2 methods)

**Files Added**: 1 file
- `src/utils/requests.py` (new module)

**Impact**:
- ✅ Application now runs on Windows without encoding errors
- ✅ PDF generation works with any number of pages
- ✅ All Thai text and emojis display correctly in console
- ✅ No manual directory creation required

**Testing**:
- Tested on Windows with Python 3.13
- Verified both refactored (`main.py`) and legacy versions work correctly
- Confirmed UTF-8 characters display properly
- Validated PDF generation with various page counts

---

## [3.1.0] - 2025-10-08

### Refactored Architecture Completion & Project Reorganization

This release completes the refactored modular architecture (v2.0) and reorganizes the project structure for better maintainability while preserving the legacy code for production stability.

#### Added

**Refactored Modules Completed**:
- **`src/ui/kiosk.py`**: Complete refactored kiosk UI module (865 lines)
  - Dependency injection for database, easter_eggs, speech_engine, sound_manager
  - Settings integration from `src.config.settings`
  - Structured logging with app_logger
  - Full 7-step workflow preserved
- **`src/pdf/generator.py`**: Complete refactored PDF generator (1046 lines)
  - PDFGenerator class with mode support (normal/lastweek)
  - All helper functions from legacy code preserved
  - Template merging, booklet layout, printer integration
  - Locale handling for Thai text collation

**Project Organization**:
- **New Directory Structure**: Organized project into logical directories
  - `assets/` - All media files (audio, fonts, templates)
  - `docs/` - Documentation and example files
  - `scripts/` - Utility scripts and deployment tools
  - `legacy/` - Archived experimental code
  - `src/ui/` - User interface modules
  - `src/pdf/` - PDF generation modules
- **CHANGELOG.md**: Comprehensive version history tracking
- **INSTALLATION.md**: Comprehensive installation and setup guide
- **test_reorganization.py**: Automated validation suite (62 tests)
- **audio_compat.py**: Cross-version audio compatibility wrapper
- **PyPDF2>=3.0.0**: PDF manipulation library (was missing)
- **pygame>=2.5.0**: Python 3.13+ compatible audio alternative

**Enhanced Documentation**:
- Added development history and acknowledgments
- Included exhibition photos and booklet samples
- Added fortune teller feature explanation
- Created non-technical visitor guide
- Improved README.md formatting and visual documentation

#### Changed

**Refactored Architecture**:
- **Modular imports**: All new modules use dependency injection
- **Centralized settings**: All constants moved to `src.config.settings`
- **Type hints**: Added throughout refactored modules
- **Logging**: Replaced print() with structured app_logger
- **Code quality**: Comprehensive docstrings and error handling

**File Organization**:
- Moved audio files to `assets/audio/`
- Moved fonts to `assets/fonts/`
- Moved templates to `assets/templates/`
- Moved example PDFs to `docs/examples/`
- Moved utility scripts to `scripts/`
- Archived old code to `legacy/`
- Updated all file paths in codebase to match new structure

**Configuration & Requirements**:
- Updated `requirements.txt` with missing dependencies and Python 3.13+ support
- Updated CLAUDE.md with complete architecture documentation
- Enhanced .gitignore to protect privacy and temporary files

#### Fixed
- **Module imports**: Fixed missing `src.ui.kiosk` and `src.pdf.generator` modules
- Python 3.13+ compatibility issues with audio libraries
- Missing PyPDF2 dependency causing import errors
- Incorrect path references after reorganization
- Temporary files being tracked by git
- Version numbering consistency in documentation

#### Preserved

**Legacy Code** (maintained for production stability):
- All original exhibition code in root directory remains functional
- `thai_slang_dict_main.py` - Normal edition (executable)
- `thai_slang_dict_main_lastweek.py` - Last week edition (executable)
- `thai_slang_kiosk.py` - Normal edition UI
- `thai_slang_kiosk_lastweek.py` - Last week edition UI
- `slang_pdf_generator.py` - Normal edition PDF generator
- `slang_pdf_generator_lastweek.py` - Last week edition PDF generator

**Functionality**:
- All exhibition functionality (normal and last-week editions)
- GUI emoji displays
- Console emoji output
- Database format and compatibility (`user_added_slang.json`)
- PDF generation features
- Motion detection and audio feedback
- Easter eggs (jackpot, system hacked, fortune telling)
- 7-step kiosk workflow
- Automatic printing functionality

### Technical Details

**Refactored Modules Statistics**:
- `src/ui/kiosk.py`: 865 lines
- `src/pdf/generator.py`: 1046 lines
- Full feature parity with legacy code
- 100% backward compatible

**Files Changed**: 150+ files
- 100+ file relocations
- 20+ path updates
- 8+ new modules created
- 3 temporary files removed

**Testing**: All 62 validation tests passing
- Directory structure ✓
- File paths ✓
- Audio files ✓
- Fonts and templates ✓
- Python syntax ✓
- Dependencies ✓
- Module imports ✓

**Compatibility**:
- Python 3.8 - 3.13+ ✓
- Windows / macOS / Linux ✓
- PyQt5 5.15+ ✓

### Running the Application

**Refactored Version** (recommended for development):
```bash
python main.py  # Kiosk mode (default)
```

**Legacy Version** (preserved for production):
```bash
python thai_slang_dict_main.py              # Normal edition
python thai_slang_dict_main_lastweek.py     # Last week edition
```

---

## [2.0] - 2024-09-16

### Refactoring Release

#### Added
- Modular architecture in `src/` directory
- Centralized configuration in `src/config/settings.py`
- Structured logging system
- Separation of concerns (audio, PDF, UI, core logic)

#### Changed
- Split monolithic files into modules
- Consolidated duplicate code between editions
- Improved code maintainability

#### Maintained
- Original exhibition code in root for stability
- Backward compatibility with existing data

---

## [1.4] - 2024-08-14

### Exhibition Last Week Edition

#### Added
- Special features for final exhibition week
- Enhanced easter eggs and special messages
- Last week specific fortune predictions

---

## [1.0] - 2024-06-13

### Initial Exhibition Release

#### Features
- Interactive kiosk interface with PyQt5
- Motion detection for automatic greeting
- Thai/English bilingual support
- PDF mini-dictionary generation
- Audio feedback system
- Database of user-contributed slang
- Easter eggs (jackpot, system hacked, fortune telling)
- Automatic printing functionality

#### Exhibition Details
- Venue: Bangkok Kunsthalle
- Duration: June 13 - August 17, 2024
- Contributions: 534 unique terms from 462 visitors
- Booklets printed: 544

---

## Release Notes

### Upgrading from v2.0 or earlier

If you're upgrading from an earlier version:

1. **Backup your data**:
   ```bash
   cp user_added_slang.json user_added_slang.json.backup
   cp output/ output_backup/
   ```

2. **Pull latest changes**:
   ```bash
   git pull origin main
   ```

3. **Update dependencies**:
   ```bash
   pip install -r requirements.txt --upgrade
   ```

4. **Run validation**:
   ```bash
   python test_reorganization.py
   ```

5. **Test the application**:
   ```bash
   python main.py
   ```

### Migration Notes

- **Asset files**: Now located in `assets/` directory
- **Scripts**: Now located in `scripts/` directory
- **Old code**: Archived in `legacy/` directory
- **Examples**: Moved to `docs/examples/`

All paths are automatically updated in the code. No manual configuration needed.

### Known Issues

None reported for v2.1.0

### Support

For issues or questions:
- GitHub Issues: https://github.com/bejranonda/the-not-so-modern-dictionary/issues
- Documentation: See INSTALLATION.md and README.md

---

**Version Format**: MAJOR.MINOR.PATCH
- MAJOR: Incompatible API changes
- MINOR: New features, backward compatible
- PATCH: Bug fixes, backward compatible
