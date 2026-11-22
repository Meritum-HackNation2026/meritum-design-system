"""Checks that the composer's attachment serves a recording and an image, each with its own icon and texts.

Features: US-SPR-08, US-SPR-11, F-08, F-33, meritum-frontend#98
Run: python3 -m unittest discover -s tests
"""

import json
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).parent.parent
SOURCE = (ROOT / "components" / "meritum" / "conversation.tsx").read_text(encoding="utf-8")
FORM = json.loads((ROOT / "copy" / "pl.json").read_text(encoding="utf-8"))["form"]


class AttachmentKind(unittest.TestCase):
    """`Attachment` takes `kind` and an optional `preview`, and the image has cost and retention notes."""

    def test_icon_and_remove_label_follow_the_kind(self) -> None:
        body = SOURCE[SOURCE.index("export function Attachment") :]
        self.assertIn('kind?: "audio" | "image"', body)
        self.assertIn("preview?: ReactNode", body)
        self.assertIn("t.conversation.remove_image", body)
        self.assertIn("t.conversation.remove_audio", body)
        self.assertRegex(body, re.compile(r"ImageIcon"))

    def test_image_notes_match_the_recording(self) -> None:
        self.assertIn("bezpłatne", FORM["image_cost"])
        self.assertIn("{days}", FORM["image_retention"])
        self.assertIn("obraz", FORM["image_retention"].lower())


if __name__ == "__main__":
    unittest.main()
