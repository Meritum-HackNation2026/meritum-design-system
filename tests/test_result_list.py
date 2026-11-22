"""Checks the result card as a summary and an open list of claims with labels that explain themselves.

Features: US-SPR-04, US-SPR-05, US-ZRD-01, US-ZRD-02, US-ZRD-03, F-17, design-system#148
Run: python3 -m unittest discover -s tests
"""

import json
import unittest
from pathlib import Path

ROOT = Path(__file__).parent.parent
MERITUM = ROOT / "components" / "meritum"
COPY = json.loads((ROOT / "copy" / "pl.json").read_text(encoding="utf-8"))


def source(name: str) -> str:
    return (MERITUM / name).read_text(encoding="utf-8")


CARD = source("result-card.tsx")
ROW = source("claim-row.tsx")
EXPLAIN = source("explain.tsx")
BADGE = source("verdict-badge.tsx")
CITATION = source("citation-item.tsx")
STRENGTH = source("strength-meter.tsx")
INDEX = source("index.ts")


# shortcut: this repo has no TS test runner, so the scenarios are checked by source; render them once one exists
class ResultWithThreeClaims(unittest.TestCase):
    """Scenario: wynik z trzema twierdzeniami."""

    def test_summary_counts_claims_and_verdicts(self) -> None:
        self.assertIn("t.result.claims_title", CARD)
        self.assertIn("plural(t.result.claims_count", CARD)
        self.assertRegex(CARD, r"<VerdictBadge verdict=\{\w+\} size=\"sm\" explain")

    def test_claims_are_an_accordion_open_by_default(self) -> None:
        self.assertIn('from "@/components/ui/accordion"', ROW + CARD)
        self.assertRegex(CARD, r'<Accordion\s+type="multiple"\s+defaultValue=\{claims\.map\(')
        self.assertIn("<ClaimRow", CARD)

    def test_badge_sits_in_a_fixed_column_beside_the_trigger(self) -> None:
        row = ROW[ROW.index("<AccordionItem") :]
        badge, trigger = row.index("<VerdictBadge"), row.index("<AccordionTrigger")
        self.assertLess(badge, trigger)
        self.assertRegex(row[:trigger], r"@xl:grid-cols-\[\d+rem_1fr\]")
        self.assertIn('size="sm" explain', row[badge:trigger])

    def test_rows_highlight_with_no_rules_and_no_frame_on_the_page(self) -> None:
        self.assertIn("hover:bg-muted", ROW)
        self.assertIn("cursor-pointer", ROW)
        self.assertIn("border-none", ROW)
        self.assertNotIn("border-t", ROW)
        self.assertIn("border-transparent in-data-host:border-border", CARD)

    def test_limitations_and_ai_note_share_one_toggle(self) -> None:
        self.assertIn('from "@/components/ui/collapsible"', CARD)
        toggle = CARD[CARD.index("<Collapsible") : CARD.index("</Collapsible>")]
        self.assertIn("t.result.limitations", toggle)
        self.assertIn("t.result.ai_disclosure", toggle)

    def test_report_and_how_it_works_are_buttons_with_icons(self) -> None:
        self.assertIn("t.result.report_error", CARD)
        self.assertIn("t.result.how_it_works", CARD)
        self.assertIn('from "lucide-react"', CARD)
        self.assertIn('from "@/components/ui/button"', CARD)


class LabelExplainsItselfOnPhone(unittest.TestCase):
    """Scenario: etykieta objaśnia się na telefonie."""

    def test_explain_is_a_popover_button_with_help_cursor(self) -> None:
        self.assertIn('from "@/components/ui/popover"', EXPLAIN)
        self.assertIn('type="button"', EXPLAIN)
        self.assertIn("cursor-help", EXPLAIN)
        self.assertIn("export function Explain", INDEX + EXPLAIN)
        self.assertRegex(INDEX, r"export \{ Explain \} from \"\./explain\"")

    def test_opens_on_tap_hover_and_focus(self) -> None:
        for handler in ("onClick", "onPointerEnter", "onFocus"):
            self.assertIn(handler, EXPLAIN)

    def test_closes_on_leave_esc_and_tap_outside(self) -> None:
        # Radix Popover reports Esc and a tap outside through onOpenChange(false)
        self.assertIn("onOpenChange={setOpen}", EXPLAIN)
        self.assertIn("onPointerLeave", EXPLAIN)
        self.assertIn("onBlur", EXPLAIN)

    def test_note_stays_open_under_the_pointer(self) -> None:
        # WCAG 1.4.13: the note itself keeps the popover open
        content = EXPLAIN[EXPLAIN.index("<PopoverContent") :]
        self.assertIn("onPointerEnter", content)
        self.assertNotIn("pointer-events-none", content)

    def test_source_kind_and_tier_labels_explain_themselves(self) -> None:
        self.assertIn("t.source_kind_hint[s.kind]", CITATION)
        self.assertIn("t.source_tier_hint[s.tier]", CITATION)
        self.assertGreaterEqual(CITATION.count("<Explain"), 2)
        self.assertIn(COPY["source_tier"]["primary"], "źródło urzędowe lub pierwotne")

    def test_verdict_and_strength_use_the_same_label(self) -> None:
        self.assertIn("t.verdict_hint[verdict]", BADGE)
        self.assertIn("<Explain", BADGE)
        self.assertIn("t.strength_hint[level]", STRENGTH)
        self.assertIn("<Explain", STRENGTH)

    def test_quote_mark_and_link_are_ink_not_the_verdict_green(self) -> None:
        self.assertNotIn("verified", CITATION)
        self.assertIn("text-link", CITATION)


class ClaimWithoutEvidence(unittest.TestCase):
    """Scenario: twierdzenie bez dowodów."""

    def test_insufficient_evidence_always_says_what_was_not_established(self) -> None:
        self.assertRegex(ROW, r'verdict === "insufficient_evidence"')
        self.assertIn("t.result.unresolved", ROW)

    def test_strength_only_for_settling_verdicts(self) -> None:
        self.assertRegex(ROW, r"SETTLING\.has\(c\.verdict\)")
        self.assertRegex(ROW, r"settles && c\.strength && <StrengthMeter")

    def test_strength_meter_has_three_bars_a_word_and_the_premises_in_its_note(self) -> None:
        self.assertIn("[1, 2, 3]", STRENGTH)
        self.assertIn("t.strength[level]", STRENGTH)
        for key in ("independent", "primary", "newest"):
            self.assertIn(f"t.result.strength_facts.{key}", STRENGTH)
        self.assertIn("t.result.agreement", STRENGTH)


class CardKeepsItsContent(unittest.TestCase):
    """The list keeps everything 6.4 asks the card to show."""

    def test_row_keeps_context_warnings_and_technique(self) -> None:
        for needle in ("t.result.conflict", "c.archival", "c.incident", "c.technique", "<CitationItem"):
            self.assertIn(needle, ROW)

    def test_card_keeps_warning_escalation_and_non_verdict_states(self) -> None:
        for needle in ("source_warning", "result.escalation", "statusText(result)", "limitationTexts(result)"):
            self.assertIn(needle, CARD)

    def test_files_stay_under_250_lines(self) -> None:
        for name in ("result-card.tsx", "claim-row.tsx", "explain.tsx", "citation-item.tsx", "strength-meter.tsx"):
            self.assertLessEqual(len(source(name).splitlines()), 250, name)

    def test_public_components_name_their_features(self) -> None:
        for text in (CARD, ROW, EXPLAIN, BADGE, CITATION, STRENGTH):
            self.assertRegex(text, r"@feature (US-[A-Z]{3}-\d{2}|F-\d{2})")


if __name__ == "__main__":
    unittest.main()
