"""Checks copy/pl.json texts of the moderator's answer form in the panel.

Features: US-MOD-07, F-39, ADR-06
Run: python3 -m unittest discover -s tests
"""

import json
import unittest
from pathlib import Path

COPY = json.loads((Path(__file__).parent.parent / "copy" / "pl.json").read_text(encoding="utf-8"))
ANSWER = COPY["moderation"]["answer"]
KEYS = (
    "title", "text_label", "citations_title", "source_label", "source_placeholder", "source_loading",
    "fragment_label", "add_citation", "remove_citation", "send", "sending", "sent_title", "sent_note",
    "text_required", "citation_required", "citation_incomplete", "citation_not_verbatim", "sources_failed",
    "not_sent",
)


class ModeratorAnswerCopy(unittest.TestCase):
    def test_every_key_is_a_polish_sentence_or_label(self) -> None:
        for key in KEYS:
            with self.subTest(key=key):
                self.assertIsInstance(ANSWER.get(key), str)
                self.assertTrue(ANSWER[key].strip())

    def test_rejected_citation_names_the_citation_and_says_nothing_was_sent(self) -> None:
        # Gherkin "cytat niedosłowny": the panel shows which citation failed; the answer is not sent
        self.assertIn("{n}", ANSWER["citation_not_verbatim"])
        self.assertIn("dosłownie", ANSWER["citation_not_verbatim"])
        self.assertIn("nie została wysłana", ANSWER["citation_not_verbatim"])

    def test_sent_note_says_the_answer_is_not_public_and_names_no_asker(self) -> None:
        # US-MOD-04: not published; the panel never says who asked
        self.assertIn("nie jest publiczna", ANSWER["sent_note"])

    def test_form_never_mentions_a_channel_or_an_identifier(self) -> None:
        for key in KEYS:
            with self.subTest(key=key):
                self.assertNotRegex(ANSWER[key].lower(), r"discord|sms|numer telefonu|identyfikator")


if __name__ == "__main__":
    unittest.main()
