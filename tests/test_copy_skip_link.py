"""Checks the text of the link that skips the page header.

Features: US-DST-01, F-01, meritum-frontend#89
Run: python3 -m unittest discover -s tests
"""

import json
import unittest
from pathlib import Path

COPY = json.loads((Path(__file__).parent.parent / "copy" / "pl.json").read_text(encoding="utf-8"))


class SkipLink(unittest.TestCase):
    def test_skip_to_content_text(self) -> None:
        self.assertEqual(COPY["layout"]["skip_to_content"], "Przejdź do treści")


if __name__ == "__main__":
    unittest.main()
