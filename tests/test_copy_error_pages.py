"""Checks the texts of the error page, the 404 page, the demo account note and the archive number.

Features: US-DST-01, US-SPR-10, US-KOR-07, meritum-frontend#115
Run: python3 -m unittest discover -s tests
"""

import json
import unittest
from pathlib import Path

COPY = json.loads((Path(__file__).parent.parent / "copy" / "pl.json").read_text(encoding="utf-8"))


class ErrorPages(unittest.TestCase):
    def test_both_pages_have_a_title_a_text_and_a_way_back(self) -> None:
        for key in ("error_title", "error_text", "error_retry", "not_found_title", "not_found_text", "back_home"):
            with self.subTest(key=key):
                self.assertTrue(COPY["layout"][key])

    def test_the_error_text_says_it_is_not_a_verdict(self) -> None:
        self.assertIn("nie jest ocena", COPY["layout"]["error_text"])


class DemoAccount(unittest.TestCase):
    def test_the_demo_note_does_not_claim_data_from_google_or_microsoft(self) -> None:
        note = COPY["account"]["stored_demo"]
        self.assertIn("demonstracyjne", note)
        self.assertIn("Nie zapisujemy", note)
        self.assertNotEqual(note, COPY["account"]["stored"])


class ArchiveNumber(unittest.TestCase):
    def test_the_number_has_a_label_a_copy_action_and_a_confirmation(self) -> None:
        for key in ("id", "copy_id", "copied_id"):
            with self.subTest(key=key):
                self.assertTrue(COPY["archive"][key])


if __name__ == "__main__":
    unittest.main()
