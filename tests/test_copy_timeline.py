"""Checks the copy of the evidence timeline in copy/pl.json: group headings and superseded evidence.

Features: US-ZRD-04, US-ZRD-11, F-17, design-system#66, design-system#71
Run: python3 -m unittest discover -s tests
"""

import unittest

from test_copy import COPY, lookup


class EvidenceTimeline(unittest.TestCase):
    def test_stance_headings_are_short_and_never_a_verdict(self) -> None:
        # Gherkin "nagłówki grup cytatów na osi czasu" from design-system#66
        verdicts = [str(v).lower() for k, v in COPY["verdict"].items() if not k.startswith("$")]
        for stance in ("supports", "refutes", "context"):
            text = lookup(f"result.stance.{stance}")
            self.assertIsInstance(text, str)
            self.assertLessEqual(len(str(text).split()), 3)
            self.assertNotIn(str(text).lower(), verdicts)

    def test_superseded_without_date_reads_like_the_dated_text(self) -> None:
        # Gherkin "dowód zastąpiony bez daty nowszego dokumentu" from design-system#71
        text = lookup("result.superseded_undated")
        self.assertIsInstance(text, str)
        self.assertNotIn("{", str(text))
        self.assertEqual(text, str(lookup("result.superseded")).replace(" z {date}", ""))


if __name__ == "__main__":
    unittest.main()
