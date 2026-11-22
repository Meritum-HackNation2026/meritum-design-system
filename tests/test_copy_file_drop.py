"""Checks the texts for files pasted or dropped onto the check field.

Features: US-SPR-08, US-SPR-11, F-08, F-33, design-system#163, meritum-frontend#144
Run: python3 -m unittest discover -s tests
"""

import json
import unittest
from pathlib import Path

COPY = json.loads((Path(__file__).parent.parent / "copy" / "pl.json").read_text(encoding="utf-8"))


class FileDropTexts(unittest.TestCase):
    def test_drop_hint_names_both_kinds_of_file(self) -> None:
        hint = COPY["conversation"]["drop_hint"]
        self.assertIn("obraz", hint)
        self.assertIn("nagranie", hint)

    def test_unsupported_file_lists_the_formats_that_work(self) -> None:
        text = COPY["errors"]["file_unsupported"]
        self.assertIn("{image_formats}", text)
        self.assertIn("{audio_formats}", text)

    def test_one_file_names_the_file_that_was_taken(self) -> None:
        self.assertIn("{name}", COPY["errors"]["one_file"])


if __name__ == "__main__":
    unittest.main()
