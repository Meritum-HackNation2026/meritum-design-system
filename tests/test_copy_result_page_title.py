"""Checks that the result page has its own name, different from the check form.

Features: US-SPR-01, F-01, meritum-frontend#87
Run: python3 -m unittest discover -s tests
"""

import json
import unittest
from pathlib import Path

COPY = json.loads((Path(__file__).parent.parent / "copy" / "pl.json").read_text(encoding="utf-8"))


class ResultPageTitle(unittest.TestCase):
    """The heading of the result page (`result.page_title`), also used in the browser tab."""

    def test_result_page_has_a_name_other_than_the_form(self) -> None:
        # WCAG 2.4.2 and 2.4.6: the result tab and heading must differ from the form's
        title = COPY["result"]["page_title"]
        self.assertEqual(title, "Wynik sprawdzenia")
        self.assertNotEqual(title, COPY["form"]["title"])


if __name__ == "__main__":
    unittest.main()
