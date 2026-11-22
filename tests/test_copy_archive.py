"""Checks the texts of archiving a page and of the archive view.

Features: US-KOR-07, F-38, meritum-frontend#103
Run: python3 -m unittest discover -s tests
"""

import json
import unittest
from pathlib import Path

ARCHIVE = json.loads((Path(__file__).parent.parent / "copy" / "pl.json").read_text(encoding="utf-8"))["archive"]
REFUSALS = {"login_wall", "robots_or_tdm", "fetch_failed", "rate_limited"}


class ArchiveCopy(unittest.TestCase):
    def test_every_worker_refusal_has_a_text(self) -> None:
        self.assertEqual(set(ARCHIVE["refusal"]), REFUSALS)

    def test_the_action_and_the_view_have_their_texts(self) -> None:
        for key in ("action", "action_hint", "pending", "title", "sha256", "archived_at", "expires_at", "download", "delete", "deleted", "failed", "not_found"):
            with self.subTest(key=key):
                self.assertTrue(ARCHIVE[key])

    def test_the_hint_says_who_sees_the_copy_and_for_how_long(self) -> None:
        self.assertIn("30 dni", ARCHIVE["action_hint"])
        self.assertIn("moderatorzy", ARCHIVE["action_hint"])


if __name__ == "__main__":
    unittest.main()
