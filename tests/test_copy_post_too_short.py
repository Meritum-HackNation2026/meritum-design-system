"""Checks the widget's own text for a post with too little text.

Features: US-WTY-01, F-02, meritum-extension#29
Run: python3 -m unittest discover -s tests
"""

import json
import unittest
from pathlib import Path

COPY = json.loads((Path(__file__).parent.parent / "copy" / "pl.json").read_text(encoding="utf-8"))


class PostTooShort(unittest.TestCase):
    def test_extension_has_its_own_text_not_the_image_one(self) -> None:
        text = COPY["extension"].get("post_too_short")
        self.assertIsInstance(text, str)
        self.assertTrue(str(text).strip())
        self.assertNotEqual(text, COPY["status_hint"]["out_of_scope_image"])


if __name__ == "__main__":
    unittest.main()
