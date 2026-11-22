"""Checks the identity pass of design-system#108: verdict first, quotes as evidence, mono only for IDs, AI notice once.

Features: US-SPR-04, F-17, design-system#108
Run: python3 -m unittest discover -s tests
"""

import json
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).parent.parent
COPY = json.loads((ROOT / "copy" / "pl.json").read_text(encoding="utf-8"))
CARD = (ROOT / "components" / "meritum" / "result-card.tsx").read_text(encoding="utf-8")
CONVERSATION = (ROOT / "components" / "meritum" / "conversation.tsx").read_text(encoding="utf-8")
TOKENS = (ROOT / "tokens" / "meritum.css").read_text(encoding="utf-8")
DESIGN = (ROOT / "DESIGN_SYSTEM.md").read_text(encoding="utf-8")


class VerdictFirst(unittest.TestCase):
    # shortcut: no TS test runner in this repo, so the card is checked by source; render it once one exists
    def test_claim_block_reads_from_the_verdict(self) -> None:
        # Gherkin "wynik czyta się od werdyktu": verdict, then the claim, then the explanation, then the quotes
        block = CARD[CARD.index("function ClaimBlock") :]
        order = [block.index(s) for s in ('size="lg"', "{c.claim}", "{c.explanation}", "<CitationItem")]
        self.assertEqual(order, sorted(order))

    def test_verdict_has_its_own_large_size(self) -> None:
        self.assertRegex(TOKENS, r"--text-verdict:\s*[0-9.]+rem")
        badge = (ROOT / "components" / "meritum" / "verdict-badge.tsx").read_text(encoding="utf-8")
        self.assertIn("text-verdict", badge)

    def test_body_text_is_at_least_16px(self) -> None:
        self.assertRegex(TOKENS, r"--text-body:\s*1rem")


class AiNoticeOnce(unittest.TestCase):
    def test_claim_block_drops_the_per_claim_ai_line(self) -> None:
        self.assertNotIn("explanation_hint", CARD)

    def test_card_in_a_reply_leaves_the_ai_line_to_the_thread(self) -> None:
        line = next(l for l in CARD.splitlines() if "ai_disclosure" in l)
        self.assertIn("in-data-reply:hidden", line)


class MonoOnlyForIds(unittest.TestCase):
    def test_conversation_sets_times_and_counts_in_the_interface_face(self) -> None:
        self.assertNotIn("font-mono", CONVERSATION)


class Examples(unittest.TestCase):
    def test_examples_are_claims_the_system_checks(self) -> None:
        # the cash example came back "Nie podlega weryfikacji" on dev (design-system#108)
        examples = COPY["conversation"]["examples"]
        self.assertFalse(any("gotówk" in e for e in examples))
        self.assertTrue(any("płaca minimalna" in e for e in examples))
        self.assertNotIn("gotówk", COPY["form"]["input_placeholder"])


class Idea(unittest.TestCase):
    def test_design_system_names_the_one_idea(self) -> None:
        self.assertRegex(DESIGN, r"(?m)^### Idea przewodnia: cytat jest dowodem")


if __name__ == "__main__":
    unittest.main()
