# Changelog

All notable changes to The Not-So-Modern Dictionary project will be documented in this file.

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
