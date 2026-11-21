"""Checks the audio field copy in copy/pl.json: provider, cost and retention, one key each.

Features: US-SPR-11, F-08, design-system#69
Run: python3 -m unittest discover -s tests
"""

import re
import unittest

from test_copy import lookup


def placeholders(key: str) -> set[str]:
    return set(re.findall(r"\{(\w+)\}", str(lookup(key))))


class AudioFieldCopy(unittest.TestCase):
    # Gherkin "teksty przy polu nagrania" from design-system#69
    def test_provider_names_the_vendor_and_region(self) -> None:
        self.assertEqual(placeholders("form.audio_provider"), {"name", "region"})

    def test_cost_says_transcription_is_free(self) -> None:
        text = str(lookup("form.audio_cost"))
        self.assertIn("bezpłatn", text)
        self.assertEqual(placeholders("form.audio_cost"), set())

    def test_retention_covers_file_and_transcript_for_the_check_record_days(self) -> None:
        text = str(lookup("form.audio_retention"))
        self.assertIn("nagrani", text)
        self.assertIn("transkrypcj", text)
        self.assertEqual(placeholders("form.audio_retention"), {"days"})


if __name__ == "__main__":
    unittest.main()
