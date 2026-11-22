"""Checks copy/pl.json texts of the conversation view of the web page.

Features: US-SPR-01, US-SPR-09, F-01, design-system#79, design-system#103
Run: python3 -m unittest discover -s tests
"""

import json
import unittest
from pathlib import Path

COPY = json.loads((Path(__file__).parent.parent / "copy" / "pl.json").read_text(encoding="utf-8"))
MAX_EXAMPLE_WORDS = 12  # an example claim fits on one tap target on a 360 px phone


class ConversationCopy(unittest.TestCase):
    def test_conversation_has_its_labels(self) -> None:
        conversation = COPY.get("conversation", {})
        for key in ("label", "you", "examples_lead", "attach_audio", "remove_audio", "audio_question"):
            with self.subTest(key=key):
                self.assertIsInstance(conversation.get(key), str)
                self.assertTrue(conversation[key].strip())

    def test_welcome_offers_two_or_three_short_example_claims(self) -> None:
        # Gherkin "puste wejście": 2–3 przykładowe twierdzenia do kliknięcia
        examples = COPY.get("conversation", {}).get("examples")
        self.assertIsInstance(examples, list)
        self.assertIn(len(examples), (2, 3))
        for example in examples:
            with self.subTest(example=example):
                self.assertLessEqual(len(example.split()), MAX_EXAMPLE_WORDS)
                self.assertNotIn("!", example)
                self.assertNotIn("?", example)

    def test_next_placeholder_asks_for_another_claim_without_an_example(self) -> None:
        # design-system#103: after the first check the field no longer repeats the example
        text = COPY.get("conversation", {}).get("next_placeholder", "")
        self.assertTrue(text.strip())
        self.assertNotIn("Np.", text)
        self.assertNotIn("!", text)

    def test_audio_question_names_the_file(self) -> None:
        self.assertIn("{name}", COPY.get("conversation", {}).get("audio_question", ""))


if __name__ == "__main__":
    unittest.main()
