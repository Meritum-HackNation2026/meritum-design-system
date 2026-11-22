"""Checks the texts of the evaluation page: file refusal, case results and run comparison, so the page
does not fall back to generic texts or to keys of another screen.

Features: US-OBS-06, US-OBS-05, F-28, meritum-frontend#27
Run: python3 -m unittest discover -s tests
"""

import json
import unittest
from pathlib import Path

EVAL = json.loads((Path(__file__).parent.parent / "copy" / "pl.json").read_text(encoding="utf-8"))["evaluation"]

KEYS = (
    "upload_rejected", "start_failed", "cases", "case_id", "expected", "actual",
    "show_cases", "hide_cases", "compare_hint", "no_runs", "no_changed_cases", "delta",
)


class EvaluationPageCopy(unittest.TestCase):
    def test_every_key_the_page_needs_has_a_text(self) -> None:
        for key in KEYS:
            with self.subTest(key=key):
                self.assertTrue(EVAL.get(key, "").strip())

    def test_rejected_file_names_the_format_and_the_minimum(self) -> None:
        # Gherkin "odrzucony plik z przypadkami": says what is wrong with the file
        self.assertIn("30", EVAL["upload_rejected"])

    def test_start_failure_is_not_the_network_error(self) -> None:
        self.assertNotIn("połączenia", EVAL["start_failed"].lower())

    def test_screen_reader_delta_takes_both_values(self) -> None:
        self.assertIn("{a}", EVAL["delta"])
        self.assertIn("{b}", EVAL["delta"])


if __name__ == "__main__":
    unittest.main()
