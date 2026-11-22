"""Checks the Atrament theme in tokens/meritum.css: one white surface, a black dark mode, green "Potwierdzone".

Features: US-SPR-01, US-DST-01, F-01, design-system#144
Run: python3 -m unittest discover -s tests
"""

import re
import unittest
from pathlib import Path

TOKENS = (Path(__file__).parent.parent / "tokens" / "meritum.css").read_text(encoding="utf-8")


def block(selector: str) -> dict[str, str]:
    """Custom properties declared in the first rule whose selector line starts with `selector`."""
    body = TOKENS[TOKENS.index("\n" + selector) :]
    body = body[body.index("{") + 1 : body.index("}")]
    return {name: value.strip() for name, value in re.findall(r"(--[a-z0-9-]+):\s*([^;]+);", body)}


LIGHT = block(":root {")
DARK = block(".dark,")
THEME = block("@theme inline {")
GROUNDS = ("--background", "--card", "--popover", "--secondary", "--muted", "--accent", "--sidebar")


def rgb(colour: str) -> tuple[int, int, int]:
    return tuple(int(colour[i : i + 2], 16) for i in (1, 3, 5))  # type: ignore[return-value]


def luminance(colour: str) -> float:
    channels = [c / 255 for c in rgb(colour)]
    r, g, b = (c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4 for c in channels)
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def contrast(text: str, ground: str) -> float:
    lighter, darker = sorted((luminance(text), luminance(ground)), reverse=True)
    return (lighter + 0.05) / (darker + 0.05)


class OneWhiteSurface(unittest.TestCase):
    def test_page_and_card_are_the_same_white(self) -> None:
        # Gherkin "strona i karta mają jedną białą powierzchnię"
        self.assertEqual(LIGHT["--background"], "#FFFFFF")
        self.assertEqual(LIGHT["--card"], "#FFFFFF")

    def test_light_greys_have_no_warm_tint(self) -> None:
        for name in ("--muted", "--secondary", "--border", "--input"):
            red, _, blue = rgb(LIGHT[name])
            self.assertLessEqual(red, blue, f"{name} {LIGHT[name]} leans warm")


class BlackDarkMode(unittest.TestCase):
    def test_dark_page_is_black(self) -> None:
        # Gherkin "tryb ciemny jest czarny, nie granatowy"
        self.assertEqual(DARK["--background"], "#0A0A0A")

    def test_no_dark_ground_leans_blue(self) -> None:
        for name in GROUNDS:
            red, green, blue = rgb(DARK[name])
            self.assertLessEqual(blue, max(red, green), f"{name} {DARK[name]} leans blue")


class GreenConfirmed(unittest.TestCase):
    def test_verified_is_green_in_both_modes(self) -> None:
        # Gherkin "Potwierdzone jest zielone"
        for mode in (LIGHT, DARK):
            for name in ("--verified", "--verified-foreground"):
                red, green, blue = rgb(mode[name])
                self.assertGreater(green, max(red, blue), f"{name} {mode[name]} is not green")


class Contrast(unittest.TestCase):
    PAIRS = (
        ("--foreground", "--background"),
        ("--muted-foreground", "--background"),
        ("--muted-foreground", "--muted"),
        ("--secondary-foreground", "--secondary"),
        ("--primary-foreground", "--primary"),
        ("--verified-foreground", "--verified-surface"),
        ("--contested-foreground", "--contested-surface"),
        ("--scam-foreground", "--scam-surface"),
    )

    def test_text_pairs_meet_wcag_aa(self) -> None:
        for label, mode in (("light", LIGHT), ("dark", DARK)):
            for text, ground in self.PAIRS:
                ratio = contrast(mode[text], mode[ground])
                self.assertGreaterEqual(ratio, 4.5, f"{label} {text} on {ground}: {ratio:.2f}:1")

    def test_verdict_words_read_on_the_page(self) -> None:
        # the verdict word is set in the *-foreground colour straight on the page (DESIGN_SYSTEM.md 6.4)
        for label, mode in (("light", LIGHT), ("dark", DARK)):
            for name in ("--verified-foreground", "--contested-foreground", "--scam-foreground"):
                ratio = contrast(mode[name], mode["--background"])
                self.assertGreaterEqual(ratio, 4.5, f"{label} {name} on the page: {ratio:.2f}:1")


class InkInsteadOfAccent(unittest.TestCase):
    def test_primary_action_and_focus_ring_are_ink(self) -> None:
        for mode in (LIGHT, DARK):
            self.assertEqual(mode["--primary"], mode["--foreground"])
            self.assertEqual(mode["--ring"], mode["--foreground"])

    def test_links_have_their_own_ink_token(self) -> None:
        # --verified is a verdict colour again, not the colour of links and focus
        for mode in (LIGHT, DARK):
            self.assertEqual(mode["--link"], mode["--foreground"])
        self.assertEqual(THEME["--color-link"], "var(--link)")


class Typeface(unittest.TestCase):
    def test_interface_face_is_schibsted_grotesk(self) -> None:
        self.assertTrue(THEME["--font-sans"].startswith('"Schibsted Grotesk"'), THEME["--font-sans"])

    def test_archivo_stays_for_the_logotype_only(self) -> None:
        self.assertTrue(THEME["--font-logo"].startswith('"Archivo"'), THEME["--font-logo"])

    def test_mono_is_unchanged(self) -> None:
        self.assertTrue(THEME["--font-mono"].startswith('"Azeret Mono"'))


class Shape(unittest.TestCase):
    def test_radius_is_eight_pixels(self) -> None:
        self.assertEqual(LIGHT["--radius"], "0.5rem")


class WidgetKeepsItsLook(unittest.TestCase):
    def test_host_skins_still_link_in_the_verdict_colour(self) -> None:
        # the widget and the platform mocks change in a later issue (meritum-monorepo#39, Out of scope)
        self.assertIn("--host-link: var(--verified)", TOKENS)

    def test_file_says_the_widget_waits(self) -> None:
        self.assertIn("extension/widget.css", TOKENS)


if __name__ == "__main__":
    unittest.main()
