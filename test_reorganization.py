#!/usr/bin/env python3
"""
Test script to validate that all file reorganization changes work correctly.
This tests path references without requiring PyQt5 or other heavy dependencies.
"""

import os
import sys
import json
from pathlib import Path

def test_section(name):
    """Print test section header"""
    print(f"\n{'='*60}")
    print(f"  {name}")
    print('='*60)

def test_result(test_name, passed, details=""):
    """Print test result"""
    status = "[PASS]" if passed else "[FAIL]"
    print(f"{status:8} | {test_name}")
    if details and not passed:
        print(f"         | Details: {details}")
    return passed

def main():
    print("\n" + "="*60)
    print("  REORGANIZATION VALIDATION TEST")
    print("="*60)

    all_passed = True

    # Test 1: Directory Structure
    test_section("Directory Structure")

    required_dirs = [
        ('assets', 'Assets directory'),
        ('assets/audio', 'Audio directory'),
        ('assets/fonts', 'Fonts directory'),
        ('assets/templates', 'Templates directory'),
        ('docs', 'Docs directory'),
        ('docs/examples', 'Examples directory'),
        ('scripts', 'Scripts directory'),
        ('legacy', 'Legacy directory'),
        ('src', 'Source directory'),
    ]

    for dir_path, desc in required_dirs:
        exists = os.path.isdir(dir_path)
        all_passed &= test_result(desc, exists, f"Missing: {dir_path}")

    # Test 2: Audio Files
    test_section("Audio Files (Exhibition Code)")

    audio_files = [
        'assets/audio/correct sound/correct-6033.mp3',
        'assets/audio/systemstart sound/game-start-6104.mp3',
        'assets/audio/beep sound/point-smooth-beep-230573.mp3',
        'assets/audio/beep sound/short-beep-tone-47916.mp3',
        'assets/audio/flipping sound/pageturn-102978.mp3',
        'assets/audio/error sound/error-call-to-attention-129258.mp3',
    ]

    for audio_file in audio_files:
        exists = os.path.isfile(audio_file)
        all_passed &= test_result(
            os.path.basename(audio_file),
            exists,
            f"Missing: {audio_file}"
        )

    # Test 3: Font Files
    test_section("Font Files (PDF Generation)")

    font_files = [
        'assets/fonts/Kinnari.ttf',
        'assets/fonts/Kinnari-Bold.ttf',
        'assets/fonts/Kinnari-Italic.ttf',
        'assets/fonts/NotoEmoji-Regular.ttf',
    ]

    for font_file in font_files:
        exists = os.path.isfile(font_file)
        all_passed &= test_result(
            os.path.basename(font_file),
            exists,
            f"Missing: {font_file}"
        )

    # Test 4: Template Files
    test_section("Template Files")

    template_files = [
        'assets/templates/PNGYOONGLAI.png',
        'assets/templates/pp1.pdf',
        'assets/templates/pp2.pdf',
        'assets/templates/pp3.pdf',
        'assets/templates/pp4.pdf',
        'assets/templates/PP1-4.pdf',
        'assets/templates/th-en-ln_slang_predictions_99.json',
        'assets/templates/th-en-ln_slang_predictions_lastweek.json',
    ]

    for template_file in template_files:
        exists = os.path.isfile(template_file)
        all_passed &= test_result(
            os.path.basename(template_file),
            exists,
            f"Missing: {template_file}"
        )

    # Test 5: Scripts Directory
    test_section("Scripts Directory")

    script_files = [
        'scripts/request_routine.py',
        'scripts/request_special.py',
        'scripts/run_dict_app.sh',
        'scripts/run_gui_wrapper.sh',
    ]

    for script_file in script_files:
        exists = os.path.isfile(script_file)
        all_passed &= test_result(
            os.path.basename(script_file),
            exists,
            f"Missing: {script_file}"
        )

    # Test 6: Refactored Code Settings
    test_section("Refactored Code (src/) - Path Configuration")

    try:
        from src.config import settings

        # Check ASSETS_DIR
        has_assets = hasattr(settings, 'ASSETS_DIR')
        all_passed &= test_result(
            "ASSETS_DIR defined",
            has_assets,
            "ASSETS_DIR not found in settings"
        )

        if has_assets:
            assets_path = str(settings.ASSETS_DIR)
            correct_path = assets_path.endswith('assets')
            all_passed &= test_result(
                f"ASSETS_DIR = .../{os.path.basename(assets_path)}",
                correct_path,
                f"Wrong path: {assets_path}"
            )

        # Check FONTS_DIR
        fonts_exists = os.path.isdir(settings.FONTS_DIR)
        all_passed &= test_result(
            f"FONTS_DIR exists",
            fonts_exists,
            f"Path: {settings.FONTS_DIR}"
        )

        # Check TEMPLATE_DIR
        template_exists = os.path.isdir(settings.TEMPLATE_DIR)
        all_passed &= test_result(
            f"TEMPLATE_DIR exists",
            template_exists,
            f"Path: {settings.TEMPLATE_DIR}"
        )

        # Check SOUNDS_DIR
        sounds_exists = os.path.isdir(settings.SOUNDS_DIR)
        all_passed &= test_result(
            f"SOUNDS_DIR exists",
            sounds_exists,
            f"Path: {settings.SOUNDS_DIR}"
        )

        # Check AUDIO_PATHS
        audio_ok = True
        for key, path_val in settings.AUDIO_PATHS.items():
            path = path_val if isinstance(path_val, str) else path_val[0]
            if not os.path.exists(path):
                audio_ok = False
                all_passed &= test_result(
                    f"Audio path: {key}",
                    False,
                    f"Missing: {path}"
                )

        if audio_ok:
            all_passed &= test_result(
                "All AUDIO_PATHS exist",
                True
            )

        # Check PDF_SETTINGS fonts
        thai_font_exists = os.path.isfile(settings.PDF_SETTINGS['thai_font_path'])
        all_passed &= test_result(
            "Thai font path exists",
            thai_font_exists,
            f"Path: {settings.PDF_SETTINGS['thai_font_path']}"
        )

        emoji_font_exists = os.path.isfile(settings.PDF_SETTINGS['emoji_font_path'])
        all_passed &= test_result(
            "Emoji font path exists",
            emoji_font_exists,
            f"Path: {settings.PDF_SETTINGS['emoji_font_path']}"
        )

    except Exception as e:
        all_passed = False
        test_result("Import src.config.settings", False, str(e))

    # Test 7: Exhibition Code - Path References
    test_section("Exhibition Code - Path Validation")

    # Read and parse path references from exhibition files
    exhibition_files = [
        'thai_slang_kiosk.py',
        'thai_slang_kiosk_lastweek.py',
        'slang_pdf_generator.py',
        'slang_pdf_generator_lastweek.py',
        'thai_slang_dict_main.py',
        'thai_slang_dict_main_lastweek.py',
        'thai_slang_dict_generator.py',
    ]

    old_path_patterns = [
        'fonts/',
        'template/',
        'flipping sound/',
        'correct sound/',
        'error sound/',
        'beep sound/',
        'systemstart sound/',
    ]

    # Exclude patterns that are expected (assets/audio/...)
    for file_name in exhibition_files:
        if not os.path.isfile(file_name):
            continue

        with open(file_name, 'r', encoding='utf-8') as f:
            content = f.read()

        # Check for old paths (not starting with assets/)
        has_old_paths = False
        for pattern in old_path_patterns:
            # Look for pattern NOT preceded by assets/audio/ or assets/
            if f'= "{pattern}' in content or f'= ["{pattern}' in content:
                # Found old path pattern
                has_old_paths = True
                break

        all_passed &= test_result(
            f"{file_name}",
            not has_old_paths,
            "Still contains old path references"
        )

    # Test 8: Python Syntax Check
    test_section("Python Syntax Validation")

    python_files = exhibition_files + [
        'main.py',
        'greetings.py',
        'greetings_lastweek.py',
        'input_slang_utils.py',
    ]

    import py_compile

    for py_file in python_files:
        if not os.path.isfile(py_file):
            continue

        try:
            py_compile.compile(py_file, doraise=True)
            all_passed &= test_result(f"Compile {py_file}", True)
        except py_compile.PyCompileError as e:
            all_passed &= test_result(f"Compile {py_file}", False, str(e))

    # Test 9: Legacy Files Preserved
    test_section("Legacy Files Preservation")

    legacy_files = [
        'legacy/Archive',
        'legacy/kiosk',
    ]

    for legacy_path in legacy_files:
        exists = os.path.exists(legacy_path)
        all_passed &= test_result(
            os.path.basename(legacy_path),
            exists,
            f"Missing: {legacy_path}"
        )

    # Test 10: Documentation
    test_section("Documentation")

    doc_files = [
        'README.md',
        'LICENSE',
        '.claude/CLAUDE.md',
        'docs/examples',
    ]

    for doc_file in doc_files:
        exists = os.path.exists(doc_file)
        all_passed &= test_result(
            doc_file,
            exists,
            f"Missing: {doc_file}"
        )

    # Final Summary
    print("\n" + "="*60)
    if all_passed:
        print("  [SUCCESS] ALL TESTS PASSED")
        print("  The reorganization is complete and working!")
    else:
        print("  [ERROR] SOME TESTS FAILED")
        print("  Please review the errors above")
    print("="*60 + "\n")

    return 0 if all_passed else 1

if __name__ == '__main__':
    sys.exit(main())
