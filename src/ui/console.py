"""
Console (headless) interface for The Not-So-Modern Dictionary.

This lightweight, GUI-free interface backs the ``debug`` application mode. It is
intended for development and testing on machines without a display, camera or
printer: it exercises the database, easter-egg and (optionally) audio subsystems
through a simple text menu.

``DictionaryApp.run_console_mode`` constructs this class with the shared
``database``, ``speech_engine`` and ``sound_manager`` instances, then calls
``run()``.
"""

from typing import Optional

from ..core.database import SlangDatabase
from ..core.easter_eggs import EasterEggManager
from ..utils.logger import app_logger


class ConsoleInterface:
    """A minimal text-based interface used by debug/console mode."""

    def __init__(self, database: SlangDatabase, speech_engine=None,
                 sound_manager=None, easter_eggs: Optional[EasterEggManager] = None):
        self.database = database
        self.speech_engine = speech_engine
        self.sound_manager = sound_manager
        self.easter_eggs = easter_eggs or EasterEggManager()

    # ------------------------------------------------------------------ #
    # Menu actions
    # ------------------------------------------------------------------ #
    def show_statistics(self) -> None:
        """Print database statistics."""
        stats = self.database.get_statistics()
        print("\n=== Dictionary Statistics ===")
        for key, value in stats.items():
            print(f"  {key}: {value}")
        print()

    def add_word(self) -> None:
        """Prompt for and add a new word to the database."""
        word = input("Word: ").strip()
        if not word:
            print("No word entered; aborting.\n")
            return
        meaning = input("Meaning: ").strip()
        example = input("Example (optional): ").strip()
        author = input("Author (optional): ").strip() or "Anonymous"

        added = self.database.add_entry(word, meaning, example, author)
        if added:
            print(f"✅ Added '{word}'.\n")
        else:
            # Word already exists - merge instead so multiple meanings coexist.
            self.database.merge_entry(word, meaning, example, author)
            print(f"➕ '{word}' already existed; merged the new meaning.\n")

    def search_word(self) -> None:
        """Search for entries matching a query."""
        query = input("Search: ").strip()
        if not query:
            print("Empty query.\n")
            return
        results = self.database.search_entries(query)
        if not results:
            print("No matches found.\n")
            return
        print(f"\n=== {len(results)} match(es) ===")
        for entry in results:
            print(f"  {entry.get('word', '?')}: {entry.get('meaning', '')}")
        print()

    def roll_easter_egg(self) -> None:
        """Show the result of a single easter-egg evaluation."""
        flags = self.easter_eggs.should_show_special_content()
        print("\n=== Easter-egg roll ===")
        for key, value in flags.items():
            print(f"  {key}: {value}")
        print()

    # ------------------------------------------------------------------ #
    # Main loop
    # ------------------------------------------------------------------ #
    def _print_menu(self) -> None:
        print("=" * 40)
        print(" The Not-So-Modern Dictionary (console)")
        print("=" * 40)
        print(" 1) Show statistics")
        print(" 2) Add a word")
        print(" 3) Search words")
        print(" 4) Roll easter eggs")
        print(" q) Quit")

    def run(self) -> None:
        """Run the interactive console loop."""
        app_logger.info("Console interface started")
        actions = {
            "1": self.show_statistics,
            "2": self.add_word,
            "3": self.search_word,
            "4": self.roll_easter_egg,
        }
        try:
            while True:
                self._print_menu()
                choice = input("> ").strip().lower()
                if choice in ("q", "quit", "exit"):
                    break
                action = actions.get(choice)
                if action:
                    try:
                        action()
                    except Exception as exc:  # keep the loop alive on errors
                        app_logger.error(f"Console action error: {exc}")
                        print(f"Error: {exc}\n")
                else:
                    print("Unknown option.\n")
        except (EOFError, KeyboardInterrupt):
            print()
        finally:
            app_logger.info("Console interface stopped")
