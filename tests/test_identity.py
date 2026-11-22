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


WIDGET = (ROOT / "extension" / "widget.css").read_text(encoding="utf-8")
CARD_JS = (ROOT / "extension" / "reference" / "card.js").read_text(encoding="utf-8")


class ExtensionWidget(unittest.TestCase):
    """The widget and its framework-free card follow the same identity (design-system#129)."""

    def test_card_js_reads_from_the_verdict_without_a_pill(self) -> None:
        block = CARD_JS[CARD_JS.index("function claimBlock") :]
        order = [block.index(s) for s in ("m-verdict", "esc(c.claim)", "c.explanation", "${sources}")]
        self.assertEqual(order, sorted(order))
        self.assertNotIn("m-badge", CARD_JS)
        self.assertNotIn("explanation_hint", CARD_JS)

    def test_quote_comes_before_its_attribution(self) -> None:
        cite = CARD_JS[CARD_JS.index("const citation") : CARD_JS.index("const LEVEL")]
        self.assertLess(cite.index("m-frag"), cite.index("s.title"))

    def test_widget_css_has_a_verdict_scale_and_hanging_quote_mark(self) -> None:
        self.assertRegex(WIDGET, r"\.m-verdict\{[^}]*font:700 28px")
        self.assertRegex(WIDGET, r"\.m-frag:before\{content:\"\\201E\";position:absolute;left:-24px")
        self.assertNotIn(".m-badge", WIDGET)

    def test_widget_body_is_16px_and_claims_are_not_boxed(self) -> None:
        self.assertRegex(WIDGET, r"\.m-expl\{[^}]*font-size:16px")
        self.assertNotRegex(WIDGET, r"\.m-frag\{[^}]*background")
        self.assertNotRegex(WIDGET, r"\.m-claim\{[^}]*border")


class Idea(unittest.TestCase):
    def test_design_system_names_the_one_idea(self) -> None:
        self.assertRegex(DESIGN, r"(?m)^### Idea przewodnia: cytat jest dowodem")


if __name__ == "__main__":
    unittest.main()
