"""Checks the web page's own texts for confirming „Usuń moje sprawdzenia”.

Features: US-BEZ-05, F-20, design-system#74
Run: python3 -m unittest discover -s tests
"""

import json
import unittest
from pathlib import Path

FORM = json.loads((Path(__file__).parent.parent / "copy" / "pl.json").read_text(encoding="utf-8"))["form"]


class DeleteSessionConfirmation(unittest.TestCase):
    def test_page_has_its_own_confirmation_texts(self) -> None:
        # Gherkin "strona ma własne teksty potwierdzenia usunięcia" from design-system#74
        for key in ("title", "text", "yes", "cancel"):
            with self.subTest(key=key):
                text = FORM.get(f"delete_session_{key}")
                self.assertIsInstance(text, str)
                self.assertTrue(str(text).strip())
                self.assertNotIn("wtyczk", str(text).lower())


if __name__ == "__main__":
    unittest.main()
