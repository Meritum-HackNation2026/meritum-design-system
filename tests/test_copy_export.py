"""Checks the texts of the analyst export screen.

Features: US-OBS-03, F-36, meritum-frontend#32
Run: python3 -m unittest discover -s tests
"""

import json
import unittest
from pathlib import Path

EXPORT = json.loads((Path(__file__).parent.parent / "copy" / "pl.json").read_text(encoding="utf-8"))["export"]


class ExportCopy(unittest.TestCase):
    def test_every_format_has_a_name_and_a_hint(self) -> None:
        self.assertEqual(set(EXPORT["formats"]), {"json", "csv", "stix"})
        self.assertEqual(set(EXPORT["format_hints"]), set(EXPORT["formats"]))

    def test_disarm_codes_are_marked_for_the_analyst_to_confirm(self) -> None:
        self.assertIn("DISARM", EXPORT["disarm_notice"])
        self.assertIn("potwierdź", EXPORT["disarm_notice"])

    def test_done_names_the_file(self) -> None:
        self.assertIn("{file}", EXPORT["done"])


if __name__ == "__main__":
    unittest.main()
