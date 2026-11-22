"""Checks copy/pl.json texts for hand-off and error-report failures on the result card.

Features: US-MOD-03, US-MOD-06, F-24, F-17, design-system#64, design-system#80, design-system#91
Run: python3 -m unittest discover -s tests
"""

import json
import re
import unittest
from pathlib import Path

COPY = json.loads((Path(__file__).parent.parent / "copy" / "pl.json").read_text(encoding="utf-8"))


def lookup(key: str) -> object:
    """Returns the value under a dotted key, or None when a part is missing."""
    node: object = COPY
    for part in key.split("."):
        node = node.get(part) if isinstance(node, dict) else None
    return node


class HandoffCopy(unittest.TestCase):
    def test_handoff_errors_name_their_own_cause(self) -> None:
        # Gherkin "limit przekazań ma własny tekst" and "sprawdzenie, którego nie ma"
        borrowed = (lookup("errors.rate_limited"), lookup("errors.busy"))
        for key in ("errors.rate_limited_handoff", "errors.handoff_not_found", "errors.handoff_rejected"):
            with self.subTest(key=key):
                text = lookup(key)
                self.assertIsInstance(text, str)
                self.assertNotIn(text, borrowed)
                self.assertLessEqual(len(re.split(r"(?<=[.?])\s+", str(text))), 2)
                self.assertNotRegex(str(text), r"dużo pytań")
        self.assertRegex(str(lookup("errors.rate_limited_handoff")), r"zgłosze.*minut")
        self.assertNotRegex(str(lookup("errors.rate_limited_handoff")), r"sprawdze")
        self.assertRegex(str(lookup("errors.handoff_not_found")), r"nie da się już przekazać")

    def test_handoff_rejected_fits_escalation_and_report(self) -> None:
        # Gherkin "odrzucone przekazanie mówi, co zrobić" (design-system#80)
        text = str(lookup("errors.handoff_rejected"))
        self.assertNotRegex(text, r"znak|skró|uzasadnieni|4000")
        self.assertRegex(text, r"[Nn]ie udało się wysłać")
        self.assertRegex(text, r"ponownie|jeszcze raz")
        self.assertRegex(text, r"odśwież")

    def test_report_send_button_differs_from_opening_button(self) -> None:
        # Gherkin "osobny napis przycisku wysyłki"
        send = lookup("result.report_error_send")
        self.assertIsInstance(send, str)
        self.assertNotEqual(send, lookup("result.report_error"))

    def test_escalation_updated_does_not_reveal_other_askers(self) -> None:
        # Gherkin "dołączenie do sprawy nie zdradza innych pytających"
        self.assertEqual(lookup("escalation.updated"), lookup("escalation.created"))
        self.assertIn("shows created in both states", COPY["escalation"]["$comment"])

    def test_not_saved_comment_covers_every_server_failure(self) -> None:
        # Gherkin "komentarz opisuje, kiedy pada not_saved" (design-system#91)
        comment = COPY["escalation"]["$comment"]
        for part in ("5xx", "unreadable response", "without a case number"):
            with self.subTest(part=part):
                self.assertIn(part, comment)
        self.assertNotIn("on HTTP 503", comment)


if __name__ == "__main__":
    unittest.main()
