"""Checks the display settings in tokens/meritum.css: a text-size scale and a dark high-contrast theme.

Features: US-DST-01, F-01, design-system#147
Run: python3 -m unittest discover -s tests
"""

import re
import unittest
from pathlib import Path

from test_tokens_atrament import TOKENS as BASE
from test_tokens_atrament import contrast

TOKENS = (Path(__file__).parent.parent / "tokens" / "display.css").read_text(encoding="utf-8")
MAX_LINES = 250  # meritum-architecture rule 6; meritum-frontend relies on the limit being kept here

AAA_TEXT = 7.0  # WCAG 2.2 AAA, normal text: the bar for a theme people pick because AA is not enough
NON_TEXT = 3.0  # WCAG 2.2 1.4.11, borders of controls
ATTRIBUTE = ':is(.dark, [data-theme="dark"])[data-contrast="more"] {'
SYSTEM = ':is(.dark, [data-theme="dark"]):not([data-contrast]) {'
SCALE = {"l": "112.5%", "xl": "125%", "xxl": "150%"}


def declarations(selector: str) -> dict[str, str]:
    """Custom properties of the rule that opens with `selector`."""
    body = TOKENS[TOKENS.index(selector) + len(selector) :]
    return {name: value.strip() for name, value in re.findall(r"(--[a-z0-9-]+):\s*([^;]+);", body[: body.index("}")])}


CONTRAST = declarations(ATTRIBUTE)


class TextSize(unittest.TestCase):
    def test_each_step_is_a_percentage_on_the_root(self) -> None:
        # Gherkin "największy rozmiar tekstu": percent multiplies the size set in the browser, pixels would replace it
        for step, size in SCALE.items():
            with self.subTest(step=step):
                rule = re.search(rf':root\[data-text="{step}"\]\s*\{{\s*font-size:\s*([^;]+);', TOKENS)
                self.assertIsNotNone(rule, f'no rule for data-text="{step}"')
                self.assertEqual(rule.group(1).strip(), size)

    def test_no_text_size_token_is_in_pixels(self) -> None:
        for name, value in re.findall(r"(--text-[a-z0-9]+):\s*([^;]+);", BASE):
            self.assertTrue(value.strip().endswith("rem"), f"{name}: {value}")

    def test_file_says_layout_must_hold_at_the_largest_size(self) -> None:
        self.assertRegex(TOKENS, r"Breakpoints do not follow this scale[^*]*150%[^*]*320 px[^*]*WCAG 1\.4\.4, 1\.4\.10")


class Files(unittest.TestCase):
    def test_both_token_files_stay_within_the_line_limit(self) -> None:
        for text in (BASE, TOKENS):
            self.assertLessEqual(len(text.splitlines()), MAX_LINES)

    def test_base_file_points_at_the_display_file(self) -> None:
        self.assertIn("tokens/display.css", BASE)


class HighContrast(unittest.TestCase):
    def test_page_is_black_and_text_white(self) -> None:
        self.assertEqual(CONTRAST["--background"], "#000000")
        self.assertEqual(CONTRAST["--foreground"], "#FFFFFF")

    def test_secondary_text_and_verdicts_reach_seven_to_one(self) -> None:
        # Gherkin "tekst drugorzędny w wysokim kontraście"
        for name in ("--muted-foreground", "--verified-foreground", "--contested-foreground", "--scam-foreground", "--link"):
            for ground in ("--background", "--muted"):
                ratio = contrast(CONTRAST[name], CONTRAST[ground])
                self.assertGreaterEqual(ratio, AAA_TEXT, f"{name} on {ground}: {ratio:.2f}:1")

    def test_borders_reach_three_to_one(self) -> None:
        for name in ("--border", "--input", "--ring"):
            ratio = contrast(CONTRAST[name], CONTRAST["--background"])
            self.assertGreaterEqual(ratio, NON_TEXT, f"{name}: {ratio:.2f}:1")

    def test_popups_get_an_outline_and_focus_a_thick_ring(self) -> None:
        # the declaration is matched together with its high-contrast selector, so a rule elsewhere cannot satisfy it
        popup = r'\[data-contrast="more"\] :is\((?:\[data-slot="[a-z-]+-content"\](?:, )?)+\) \{ border: 1px solid var\(--border\); \}'
        focus = r'\[data-contrast="more"\] :focus-visible \{ outline: 3px solid var\(--ring\); outline-offset: 2px; \}'
        self.assertRegex(TOKENS, popup)
        self.assertRegex(TOKENS, focus)
        for slot in ("popover-content", "dropdown-menu-content", "tooltip-content", "dialog-content", "alert-dialog-content"):
            self.assertIn(f'[data-slot="{slot}"]', TOKENS)


def media_blocks() -> list[str]:
    """Bodies of every `@media (prefers-contrast: more) { ... }` block, cut out by matching braces."""
    blocks, marker, start = [], "@media (prefers-contrast: more) {", 0
    while (at := TOKENS.find(marker, start)) != -1:
        depth, end = 1, at + len(marker)
        while depth:
            depth += {"{": 1, "}": -1}.get(TOKENS[end], 0)
            end += 1
        blocks.append(TOKENS[at + len(marker) : end - 1])
        start = end
    return blocks


class FollowsTheSystem(unittest.TestCase):
    def test_system_preference_gives_the_same_tokens(self) -> None:
        # Gherkin "system prosi o większy kontrast": dark mode with no stored choice, inside the media query
        inside = "".join(media_blocks())
        self.assertIn(SYSTEM, inside)
        body = inside[inside.index(SYSTEM) + len(SYSTEM) :]
        tokens = {name: value.strip() for name, value in re.findall(r"(--[a-z0-9-]+):\s*([^;]+);", body[: body.index("}")])}
        self.assertEqual(tokens, CONTRAST)

    def test_without_the_system_setting_plain_dark_stays_plain(self) -> None:
        # the no-stored-choice selector may only stand inside the media query, never on its own
        outside = TOKENS
        for block in media_blocks():
            outside = outside.replace(block, "")
        self.assertNotIn(":not([data-contrast])", outside)

    def test_edges_apply_only_in_high_contrast(self) -> None:
        outside = TOKENS
        for block in media_blocks():
            outside = outside.replace(block, "")
        for rule in re.findall(r"^[^\n{}]*(?:border: 1px solid var\(--border\)|outline: 3px solid var\(--ring\))", outside, re.M):
            self.assertIn('[data-contrast="more"]', rule)
        self.assertIn(":focus-visible", "".join(media_blocks()))


if __name__ == "__main__":
    unittest.main()
