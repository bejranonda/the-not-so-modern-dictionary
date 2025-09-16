"""
Database management for the slang dictionary.
"""
import json
import os
from typing import Dict, List, Optional, Any
from datetime import datetime

from ..config.settings import DATABASE_SETTINGS
from ..utils.logger import app_logger


class SlangDatabase:
    """Manages the slang dictionary database."""

    def __init__(self, db_file: Optional[str] = None):
        self.db_file = db_file or DATABASE_SETTINGS["user_slang_file"]
        self._data: Dict[str, Any] = {}
        self.load_database()

    def load_database(self) -> None:
        """Load the database from file."""
        try:
            if os.path.exists(self.db_file):
                with open(self.db_file, "r", encoding="utf-8") as f:
                    self._data = json.load(f)
                app_logger.info(f"Loaded {len(self._data)} entries from database")
            else:
                self._data = {}
                app_logger.info("Created new database")
        except Exception as e:
            app_logger.error(f"Error loading database: {e}")
            self._data = {}

    def save_database(self) -> None:
        """Save the database to file."""
        try:
            # Ensure output directory exists
            os.makedirs(os.path.dirname(self.db_file) or ".", exist_ok=True)

            with open(self.db_file, "w", encoding="utf-8") as f:
                json.dump(self._data, f, ensure_ascii=False, indent=2)
            app_logger.info(f"Saved {len(self._data)} entries to database")
        except Exception as e:
            app_logger.error(f"Error saving database: {e}")

    def add_entry(self, word: str, meaning: str, example: str = "",
                  author: str = "Anonymous") -> bool:
        """
        Add a new entry to the database.

        Args:
            word: The slang word
            meaning: Definition of the word
            example: Example usage
            author: Author who added the entry

        Returns:
            True if entry was added, False if word already exists
        """
        try:
            if word.lower() in self._data:
                app_logger.warning(f"Word '{word}' already exists in database")
                return False

            entry = {
                "word": word,
                "meaning": meaning,
                "example": example,
                "author": author,
                "timestamp": datetime.now().isoformat(),
                "usage_count": 0
            }

            self._data[word.lower()] = entry
            self.save_database()
            app_logger.info(f"Added new entry: {word}")
            return True

        except Exception as e:
            app_logger.error(f"Error adding entry '{word}': {e}")
            return False

    def get_entry(self, word: str) -> Optional[Dict[str, Any]]:
        """
        Get an entry from the database.

        Args:
            word: The word to look up

        Returns:
            Dictionary containing entry data or None if not found
        """
        return self._data.get(word.lower())

    def update_entry(self, word: str, **kwargs) -> bool:
        """
        Update an existing entry.

        Args:
            word: The word to update
            **kwargs: Fields to update

        Returns:
            True if updated successfully, False if word not found
        """
        try:
            key = word.lower()
            if key not in self._data:
                return False

            for field, value in kwargs.items():
                if field in self._data[key]:
                    self._data[key][field] = value

            self._data[key]["last_modified"] = datetime.now().isoformat()
            self.save_database()
            app_logger.info(f"Updated entry: {word}")
            return True

        except Exception as e:
            app_logger.error(f"Error updating entry '{word}': {e}")
            return False

    def delete_entry(self, word: str) -> bool:
        """
        Delete an entry from the database.

        Args:
            word: The word to delete

        Returns:
            True if deleted successfully, False if word not found
        """
        try:
            key = word.lower()
            if key in self._data:
                del self._data[key]
                self.save_database()
                app_logger.info(f"Deleted entry: {word}")
                return True
            return False

        except Exception as e:
            app_logger.error(f"Error deleting entry '{word}': {e}")
            return False

    def search_entries(self, query: str) -> List[Dict[str, Any]]:
        """
        Search for entries containing the query.

        Args:
            query: Search term

        Returns:
            List of matching entries
        """
        query_lower = query.lower()
        results = []

        for entry in self._data.values():
            if (query_lower in entry["word"].lower() or
                query_lower in entry["meaning"].lower() or
                query_lower in entry.get("example", "").lower()):
                results.append(entry)

        return results

    def get_all_entries(self) -> List[Dict[str, Any]]:
        """
        Get all entries in the database.

        Returns:
            List of all entries
        """
        return list(self._data.values())

    def get_random_entries(self, count: int = 1) -> List[Dict[str, Any]]:
        """
        Get random entries from the database.

        Args:
            count: Number of random entries to return

        Returns:
            List of random entries
        """
        import random
        entries = list(self._data.values())
        if not entries:
            return []

        count = min(count, len(entries))
        return random.sample(entries, count)

    def get_statistics(self) -> Dict[str, Any]:
        """
        Get database statistics.

        Returns:
            Dictionary containing statistics
        """
        entries = list(self._data.values())
        total_entries = len(entries)

        if not entries:
            return {"total_entries": 0}

        # Calculate statistics
        total_usage = sum(entry.get("usage_count", 0) for entry in entries)
        authors = set(entry.get("author", "Anonymous") for entry in entries)

        # Most recent entry
        most_recent = max(entries,
                         key=lambda x: x.get("timestamp", ""),
                         default=None)

        return {
            "total_entries": total_entries,
            "total_usage": total_usage,
            "unique_authors": len(authors),
            "most_recent_word": most_recent.get("word") if most_recent else None,
            "most_recent_author": most_recent.get("author") if most_recent else None,
        }

    def merge_entry(self, word: str, meaning: str, example: str = "",
                   author: str = "Anonymous") -> bool:
        """
        Merge an entry with existing data or create new one.

        Args:
            word: The slang word
            meaning: Definition of the word
            example: Example usage
            author: Author who added the entry

        Returns:
            True if merged/added successfully
        """
        try:
            key = word.lower()

            if key in self._data:
                # Update existing entry
                existing = self._data[key]
                existing["meaning"] = f"{existing['meaning']}; {meaning}"
                if example and example not in existing.get("example", ""):
                    existing["example"] = f"{existing.get('example', '')}; {example}"
                existing["last_modified"] = datetime.now().isoformat()
                existing["usage_count"] = existing.get("usage_count", 0) + 1
                app_logger.info(f"Merged entry: {word}")
            else:
                # Create new entry
                return self.add_entry(word, meaning, example, author)

            self.save_database()
            return True

        except Exception as e:
            app_logger.error(f"Error merging entry '{word}': {e}")
            return False