# Changelog

All notable changes to The Not-So-Modern Dictionary project will be documented in this file.

## [2.1.0] - 2025-10-08

### Major Reorganization

#### Added
- **New Directory Structure**: Organized project into logical directories
  - `assets/` - All media files (audio, fonts, templates)
  - `docs/` - Documentation and example files
  - `scripts/` - Utility scripts and deployment tools
  - `legacy/` - Archived experimental code
- **INSTALLATION.md**: Comprehensive installation and setup guide
- **test_reorganization.py**: Automated validation suite (62 tests)
- **audio_compat.py**: Cross-version audio compatibility wrapper
- **PyPDF2>=3.0.0**: PDF manipulation library (was missing)
- **pygame>=2.5.0**: Python 3.13+ compatible audio alternative

#### Changed
- **File Organization**:
  - Moved audio files to `assets/audio/`
  - Moved fonts to `assets/fonts/`
  - Moved templates to `assets/templates/`
  - Moved example PDFs to `docs/examples/`
  - Moved utility scripts to `scripts/`
  - Archived old code to `legacy/`
- **Path References**: Updated all file paths in codebase to match new structure
- **Requirements**: Updated `requirements.txt` with missing dependencies and Python 3.13+ support
- **Documentation**: Updated README.md and CLAUDE.md with new structure
- **.gitignore**: Added patterns for temporary files and logs

#### Fixed
- Python 3.13+ compatibility issues with audio libraries
- Missing PyPDF2 dependency causing import errors
- Incorrect path references after reorganization
- Temporary files being tracked by git

#### Preserved
- All exhibition functionality (normal and last-week editions)
- GUI emoji displays
- Console emoji output
- Database format and compatibility
- PDF generation features
- Motion detection and audio feedback

### Technical Details

**Files Changed**: 147 files
- 100+ file relocations
- 20+ path updates
- 4+ new files created
- 3 temporary files removed

**Testing**: All 62 validation tests passing
- Directory structure ✓
- File paths ✓
- Audio files ✓
- Fonts and templates ✓
- Python syntax ✓
- Dependencies ✓

**Compatibility**:
- Python 3.8 - 3.13+ ✓
- Windows / macOS / Linux ✓
- PyQt5 5.15+ ✓

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
