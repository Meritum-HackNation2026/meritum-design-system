"""Checks the image upload texts: attach control, limits, upload errors, OCR heading and warning.

Features: US-SPR-01, F-01, design-system#113, meritum-frontend#29
Run: python3 -m unittest discover -s tests
"""

import json
import unittest
from pathlib import Path

COPY = json.loads((Path(__file__).parent.parent / "copy" / "pl.json").read_text(encoding="utf-8"))
KEYS = (
    ("form", "image_label"),
    ("form", "image_limits"),
    ("form", "image_note"),
    ("conversation", "attach_image"),
    ("conversation", "remove_image"),
    ("conversation", "image_question"),
    ("errors", "image_too_large"),
    ("errors", "image_format_unsupported"),
    ("result", "image_text"),
    ("result", "image_text_hint"),
    ("limitation_code", "image_search_not_run"),
)


class ImageTexts(unittest.TestCase):
    def test_every_image_key_has_text(self) -> None:
        for section, key in KEYS:
            with self.subTest(key=f"{section}.{key}"):
                self.assertTrue(str(COPY[section].get(key) or "").strip())

    def test_ocr_heading_and_warning_say_it_can_misread(self) -> None:
        self.assertEqual(COPY["result"]["image_text"], "Tekst odczytany z obrazu")
        self.assertIn("pomylić", COPY["result"]["image_text_hint"])

    def test_limits_and_errors_keep_placeholders(self) -> None:
        self.assertIn("{max_mb}", COPY["form"]["image_limits"])
        self.assertIn("{formats}", COPY["form"]["image_limits"])
        self.assertIn("{max_mb}", COPY["errors"]["image_too_large"])
        self.assertIn("{formats}", COPY["errors"]["image_format_unsupported"])


if __name__ == "__main__":
    unittest.main()
