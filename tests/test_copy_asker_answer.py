"""Checks copy/pl.json texts of the page where an asker reads the moderator's answer.

Features: US-MOD-07, F-39
Run: python3 -m unittest discover -s tests
"""

import json
import unittest
from pathlib import Path

COPY = json.loads((Path(__file__).parent.parent / "copy" / "pl.json").read_text(encoding="utf-8"))
PAGE = COPY["moderation"]["asker_answer"]
KEYS = ("title", "loading", "citations_title", "note", "not_found_title", "not_found", "error", "retry")


class AskerAnswerCopy(unittest.TestCase):
    def test_every_key_is_a_polish_text(self) -> None:
        for key in KEYS:
            with self.subTest(key=key):
                self.assertIsInstance(PAGE.get(key), str)
                self.assertTrue(PAGE[key].strip())

    def test_note_says_the_answer_is_not_public(self) -> None:
        self.assertIn("Nie jest publiczna", PAGE["note"])

    def test_page_never_mentions_other_askers_a_channel_or_an_identifier(self) -> None:
        for key in KEYS:
            with self.subTest(key=key):
                self.assertNotRegex(PAGE[key].lower(), r"discord|sms|numer telefonu|identyfikator|inni pytali")


if __name__ == "__main__":
    unittest.main()
