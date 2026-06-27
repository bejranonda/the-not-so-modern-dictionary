"""
Validation tests for The Not-So-Modern Dictionary.

These tests cover the dependency-light, hardware-free parts of the refactored
``src/`` package so they can run in CI and on developer machines without PyQt5,
a camera, a printer or an audio device:

* the JSON-backed ``SlangDatabase``
* the probability-based ``EasterEggManager``
* the audio playback compatibility layer (``src.audio.player``)
* the headless ``ConsoleInterface`` used by debug mode

Run with:  ``python -m unittest discover -s tests``  or  ``pytest tests``
"""

import os
import sys
import tempfile
import unittest

# Make the project root importable when run directly.
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.core.database import SlangDatabase
from src.core.easter_eggs import EasterEggManager


class TestSlangDatabase(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.NamedTemporaryFile(
            suffix=".json", delete=False, mode="w", encoding="utf-8"
        )
        self.tmp.write("{}")
        self.tmp.close()
        self.db = SlangDatabase(db_file=self.tmp.name)

    def tearDown(self):
        if os.path.exists(self.tmp.name):
            os.remove(self.tmp.name)

    def test_add_and_get(self):
        self.assertTrue(self.db.add_entry("จาบ", "rude/cheeky", author="A"))
        entry = self.db.get_entry("จาบ")
        self.assertIsNotNone(entry)
        self.assertEqual(entry["meaning"], "rude/cheeky")

    def test_case_insensitive_lookup(self):
        self.db.add_entry("Pang", "awesome")
        self.assertIsNotNone(self.db.get_entry("pang"))
        self.assertIsNotNone(self.db.get_entry("PANG"))

    def test_duplicate_returns_false(self):
        self.assertTrue(self.db.add_entry("warp", "teleport"))
        self.assertFalse(self.db.add_entry("warp", "another meaning"))

    def test_merge_appends_meaning(self):
        self.db.add_entry("warp", "teleport")
        self.db.merge_entry("warp", "to move fast")
        entry = self.db.get_entry("warp")
        self.assertIn("teleport", entry["meaning"])
        self.assertIn("to move fast", entry["meaning"])

    def test_search_handles_malformed_entries(self):
        # Entry missing the "meaning" key must not raise KeyError.
        self.db._data["broken"] = {"word": "broken"}
        try:
            results = self.db.search_entries("broken")
        except KeyError:
            self.fail("search_entries raised KeyError on malformed entry")
        self.assertEqual(len(results), 1)

    def test_statistics_empty(self):
        self.assertEqual(self.db.get_statistics()["total_entries"], 0)

    def test_persistence_roundtrip(self):
        self.db.add_entry("เข้ม", "fierce")
        reloaded = SlangDatabase(db_file=self.tmp.name)
        self.assertIsNotNone(reloaded.get_entry("เข้ม"))


class TestEasterEggManager(unittest.TestCase):
    def setUp(self):
        self.mgr = EasterEggManager()

    def test_pages_count_valid(self):
        self.assertIn(self.mgr.get_pages_count(), (1, 8))

    def test_special_content_keys(self):
        flags = self.mgr.should_show_special_content()
        for key in ("jackpot", "system_hacked", "fortune_message"):
            self.assertIn(key, flags)
            self.assertIsInstance(flags[key], bool)

    def test_messages_are_strings(self):
        self.assertIsInstance(self.mgr.get_jackpot_message(), str)
        self.assertIsInstance(self.mgr.get_hacked_message(), str)
        self.assertIsInstance(self.mgr.generate_fortune_message("ปัง"), str)


class TestAudioCompat(unittest.TestCase):
    def test_player_importable_and_has_callable(self):
        # The whole point of the fix: importing audio playback must never fail
        # even when the legacy ``playsound`` package is absent.
        from src.audio import player
        self.assertTrue(callable(player.playsound))
        self.assertIn(player.audio_backend, ("playsound", "pygame", "none"))

    def test_missing_file_does_not_raise(self):
        from src.audio.player import playsound
        # Should warn and return rather than raise.
        playsound("/path/that/does/not/exist.mp3")


class TestConsoleInterface(unittest.TestCase):
    def test_constructable_without_gui(self):
        # ConsoleInterface must be importable/usable without PyQt5 or a display.
        from src.ui.console import ConsoleInterface
        db = SlangDatabase(db_file=tempfile.NamedTemporaryFile(
            suffix=".json", delete=False).name)
        console = ConsoleInterface(database=db)
        self.assertIsNotNone(console.easter_eggs)
        # show_statistics must run without error on an empty DB.
        console.show_statistics()


if __name__ == "__main__":
    unittest.main(verbosity=2)
