"""Checks that the note under the web history says where the history really lives.

Features: US-SPR-09, F-01, design-system#84
Run: python3 -m unittest discover -s tests
"""

import json
import unittest
from pathlib import Path

HISTORY = json.loads((Path(__file__).parent.parent / "copy" / "pl.json").read_text(encoding="utf-8"))["history"]


class HistoryNote(unittest.TestCase):
    def test_note_does_not_promise_a_single_tab(self) -> None:
        # Gherkin "notatka pod historią mówi prawdę o tym, gdzie żyje historia" from design-system#84:
        # the browser copies sessionStorage into tabs opened from the page and restores closed tabs
        note = HISTORY["session_note"].lower()
        self.assertNotIn("tylko w tej karcie", note)
        self.assertNotIn("zniknie", note)
        self.assertIn("przeglądar", note)
        self.assertIn("kart", note)


if __name__ == "__main__":
    unittest.main()
