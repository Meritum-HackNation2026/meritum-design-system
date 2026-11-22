"""Checks the display settings in tokens/meritum.css: a text-size scale and a dark high-contrast theme.

Features: US-DST-01, F-01, design-system#147
Run: python3 -m unittest discover -s tests
"""

import re
import unittest

from test_tokens_atrament import TOKENS, contrast

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
        for name, value in re.findall(r"(--text-[a-z]+):\s*([^;]+);", TOKENS):
            self.assertTrue(value.strip().endswith("rem"), f"{name}: {value}")

    def test_file_says_layout_must_hold_at_the_largest_size(self) -> None:
        self.assertRegex(TOKENS, r"150%[^*]*320 px")


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
        rules = TOKENS[TOKENS.index("/* high contrast: edges") :]
        self.assertRegex(rules, r"border:\s*1px solid var\(--border\)")
        self.assertRegex(rules, r":focus-visible[^{]*\{\s*outline:\s*3px solid var\(--ring\)")


class FollowsTheSystem(unittest.TestCase):
    def test_system_preference_gives_the_same_tokens(self) -> None:
        # Gherkin "system prosi o większy kontrast": dark mode with no stored choice
        media = TOKENS[TOKENS.index("@media (prefers-contrast: more)") :]
        self.assertIn(SYSTEM, media)
        self.assertEqual(declarations(SYSTEM), CONTRAST)

    def test_a_stored_choice_beats_the_system(self) -> None:
        # the app writes data-contrast="more" or "normal" once the person picks a theme
        self.assertIn(":not([data-contrast])", SYSTEM)


if __name__ == "__main__":
    unittest.main()
