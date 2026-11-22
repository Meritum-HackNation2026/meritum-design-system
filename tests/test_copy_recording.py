"""Checks the live recording copy in copy/pl.json: every control has a text, the limit is a placeholder.

Features: US-SPR-11, F-08, meritum-frontend#81
Run: python3 -m unittest discover -s tests
"""

import re
import unittest

from test_copy import lookup

KEYS = (
    "start", "stop", "recording_now", "elapsed", "level", "listen", "discard",
    "file_name", "limit_reached", "denied", "unsupported", "failed",
)


class RecordingCopy(unittest.TestCase):
    def test_every_control_and_error_has_a_text(self) -> None:
        for key in KEYS:
            with self.subTest(key=key):
                self.assertTrue(str(lookup(f"recording.{key}")).strip())

    def test_limit_text_takes_the_minutes(self) -> None:
        found = set(re.findall(r"\{(\w+)\}", str(lookup("recording.limit_reached"))))
        self.assertEqual(found, {"max_minutes"})

    def test_errors_still_offer_a_file(self) -> None:
        for key in ("denied", "unsupported", "failed"):
            self.assertIn("plik", str(lookup(f"recording.{key}")))


if __name__ == "__main__":
    unittest.main()
