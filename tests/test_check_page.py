"""Checks the page of one check that replaces the conversation view (DESIGN_SYSTEM.md 6.8).

Features: US-SPR-01, US-SPR-09, US-BEZ-05, F-01, F-20, design-system#150
Run: python3 -m unittest discover -s tests
"""

import re
import unittest
from pathlib import Path

ROOT = Path(__file__).parent.parent
MERITUM = ROOT / "components" / "meritum"
CONVERSATION = (MERITUM / "conversation.tsx").read_text(encoding="utf-8")
HISTORY = (MERITUM / "check-history.tsx").read_text(encoding="utf-8")
MARK = (MERITUM / "meritum-mark.tsx").read_text(encoding="utf-8")


def body(source: str, name: str) -> str:
    """Return the source of one exported function, up to the next export."""
    start = source.index(f"export function {name}")
    end = source.find("\nexport ", start + 1)
    return source[start : end if end != -1 else len(source)]


# shortcut: this repo has no TS test runner, so the components are checked by source; render them once one exists
class ClaimIsThePageHeading(unittest.TestCase):
    """Scenario: twierdzenie jest nagłówkiem strony."""

    def test_question_is_a_left_aligned_h1_with_a_hanging_ink_quote_mark(self) -> None:
        quoted = body(CONVERSATION, "QuotedClaim")
        self.assertIn("<h1", quoted)
        self.assertIn("text-title", quoted)
        self.assertRegex(quoted, r'aria-hidden="true" className="[^"]*absolute[^"]*text-foreground[^"]*"\s*>\s*„')
        for bubble in ("bg-secondary", "rounded-xl", "justify-items-end", "ml-auto", "text-right", "<blockquote"):
            self.assertNotIn(bubble, quoted, bubble)

    def test_recording_and_image_stand_in_the_heading_with_their_file_name(self) -> None:
        quoted = body(CONVERSATION, "QuotedClaim")
        self.assertIn("t.conversation.audio_question", quoted)
        self.assertIn("t.conversation.image_question", quoted)

    def test_conversation_pieces_are_gone(self) -> None:
        for name in ("Question", "Reply", "Welcome"):
            self.assertNotIn(f"export function {name}", CONVERSATION, name)
        self.assertNotIn("data-reply", CONVERSATION)


class FieldScrollsWithThePage(unittest.TestCase):
    """Scenario: pole nie jest przyklejone do ekranu."""

    def test_field_has_a_thin_outline_and_no_shadow(self) -> None:
        composer = body(CONVERSATION, "Composer")
        self.assertIn("border border-input", composer)
        self.assertIn("rounded-lg", composer)
        self.assertNotIn("shadow-float", composer)

    def test_field_is_not_docked_to_the_screen(self) -> None:
        composer = body(CONVERSATION, "Composer")
        for docked in ("sticky", "fixed", "bottom-0", "docked"):
            self.assertNotIn(docked, composer, docked)

    def test_field_keeps_validation_counter_keys_attachment_and_tools(self) -> None:
        composer = body(CONVERSATION, "Composer")
        for kept in ("toRequest(value)", "{tools}", "e.shiftKey", "requestSubmit()", "onSendAttachment", "MAX.toLocaleString"):
            self.assertIn(kept, composer, kept)


class HistoryInTheRail(unittest.TestCase):
    """Scenario: historia w szynie."""

    def test_row_has_the_question_on_two_lines_then_verdict_and_time(self) -> None:
        row = HISTORY[HISTORY.index("<li") : HISTORY.index("</li>")]
        order = [row.index(s) for s in ("line-clamp-2", "<VerdictBadge", "<time")]
        self.assertEqual(order, sorted(order))
        self.assertNotIn("truncate", row)

    def test_check_in_progress_shows_its_state_as_a_word(self) -> None:
        self.assertRegex(HISTORY, r"pending\?: boolean")
        self.assertIn("t.analysis.step_status.active", HISTORY)

    def test_rows_have_no_rules_and_highlight_on_hover(self) -> None:
        for rule in ("divide-y", "border-y", "border-b", "border-t"):
            self.assertNotIn(rule, HISTORY, rule)
        self.assertRegex(HISTORY, r"hover:bg-muted")

    def test_time_is_set_in_the_interface_face(self) -> None:
        self.assertNotIn("font-mono", HISTORY)
        self.assertIn("tabular-nums", HISTORY)

    def test_new_check_button_stands_above_the_list(self) -> None:
        self.assertLess(HISTORY.index("t.check_page.new"), HISTORY.index("<ul"))


class MarkIsInkOnThePage(unittest.TestCase):
    """DESIGN_SYSTEM.md section 2: stem and dot in ink on the page, sea only in platform skins."""

    def test_stem_and_dot_follow_the_text_colour_outside_platform_skins(self) -> None:
        self.assertNotRegex(MARK, r'(stroke|fill)="var\(--verified\)"')
        group = re.search(r'<g className="in-data-host:text-verified">(.*?)</g>', MARK, re.DOTALL)
        assert group, "stem and dot are not grouped under the platform-skin colour"
        self.assertIn('d="M24 25v15"', group.group(1))
        self.assertIn('fill="currentColor"', group.group(1))


if __name__ == "__main__":
    unittest.main()
