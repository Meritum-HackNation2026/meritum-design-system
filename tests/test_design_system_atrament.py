"""Checks that DESIGN_SYSTEM.md describes the Atrament theme, one surface without rules and the check page.

Features: US-SPR-01, US-SPR-04, US-DST-01, F-01, F-17, design-system#146
Run: python3 -m unittest discover -s tests
"""

import re
import unittest
from pathlib import Path

from test_tokens_atrament import DARK, LIGHT

SPEC = (Path(__file__).parent.parent / "DESIGN_SYSTEM.md").read_text(encoding="utf-8")
# a colour row: | role | `--token`, `--token` | `#light` | `#dark` | use |
ROW = re.compile(r"^\|[^|]+\|((?:\s*`--[a-z-]+`,?)+)\s*\|\s*`(#[0-9A-F]{6})`\s*\|\s*`(#[0-9A-F]{6})`\s*\|", re.M)
TABLE_TOKENS = (
    "--background",
    "--card",
    "--popover",
    "--foreground",
    "--muted-foreground",
    "--border",
    "--input",
    "--secondary",
    "--muted",
    "--verified",
    "--verified-surface",
    "--verified-foreground",
    "--contested",
    "--contested-surface",
    "--contested-foreground",
    "--scam",
    "--scam-surface",
    "--scam-foreground",
)


def section(number: str) -> str:
    """Text of a top-level section or a 6.x subsection, up to the next heading of the same level."""
    marker = f"### {number} " if "." in number else f"## {number}. "
    stop = "\n### " if "." in number else "\n## "
    start = SPEC.index(marker)
    end = SPEC.find(stop, start + len(marker))
    return SPEC[start : end if end != -1 else None]


class ColoursMatchTokens(unittest.TestCase):
    def test_colour_tables_give_the_token_values(self) -> None:
        # Gherkin "dokument i tokeny podają te same kolory"
        seen = set()
        for tokens, light, dark in ROW.findall(section("3")):
            for token in re.findall(r"--[a-z-]+", tokens):
                seen.add(token)
                self.assertEqual(light, LIGHT[token], f"{token} light")
                self.assertEqual(dark, DARK[token], f"{token} dark")
        self.assertFalse(set(TABLE_TOKENS) - seen, "tokens missing from the colour tables")

    def test_measured_contrast_is_written_down(self) -> None:
        self.assertRegex(section("3"), r"\d,\d:1")


class Bans(unittest.TestCase):
    def test_spec_bans_what_the_team_rejected(self) -> None:
        # Gherkin "dokument zakazuje tego, co odrzucono"
        colours, shapes = section("3"), section("5")
        for part in ("kremowe", "kolorowe tło", "granatowy tryb ciemny"):
            with self.subTest(part=part):
                self.assertIn(part, colours)
        for part in ("linii między sekcjami", "ramki w ramce"):
            with self.subTest(part=part):
                self.assertIn(part, shapes)

    def test_old_palette_is_gone_from_the_rules_for_the_page(self) -> None:
        for number in ("3", "5", "12"):
            for old in ("#F6F7F5", "#0B0F12", "#14191E"):
                with self.subTest(section=number, colour=old):
                    self.assertNotIn(old, section(number))


class Typeface(unittest.TestCase):
    def test_schibsted_grotesk_is_the_interface_face(self) -> None:
        text = section("4")
        self.assertIn("Schibsted Grotesk", text)
        self.assertRegex(text, r"Archivo[^|]*\|[^|]*logotyp")
        self.assertIn("Azeret Mono", text)


class Layout(unittest.TestCase):
    def test_one_surface_with_a_column_and_a_rail(self) -> None:
        text = section("5")
        for part in ("jedna powierzchnia", "720 px", "320 px", "szyn"):
            with self.subTest(part=part):
                self.assertIn(part, text.lower() if part == "jedna powierzchnia" else text)


class Components(unittest.TestCase):
    def test_result_is_an_open_list_of_claims(self) -> None:
        text = section("6.4")
        for part in ("lista twierdzeń", "domyślnie rozwinięt", "`Accordion`", "trzy kreski"):
            with self.subTest(part=part):
                self.assertIn(part, text)

    def test_progress_is_a_bar_with_steps_on_request(self) -> None:
        text = section("6.3")
        for part in ("pasek postępu", "Krok", "na żądanie"):
            with self.subTest(part=part):
                self.assertIn(part, text)

    def test_check_page_replaces_the_conversation(self) -> None:
        text = section("6.8")
        self.assertIn("### 6.8 Strona sprawdzenia", SPEC)
        self.assertNotIn("### 6.8 Widok rozmowy", SPEC)
        for part in ("nagłówek-cytat", "bez dymków", "nie jest przyklejone", "szynie", "`Composer`"):
            with self.subTest(part=part):
                self.assertIn(part, text)

    def test_shell_home_and_method_pages_are_described(self) -> None:
        text = section("6.9")
        for part in ("belka", "stopka", "strona główna", "bez pola", "Jak działa", "droga pytania"):
            with self.subTest(part=part):
                self.assertIn(part, text.lower() if part != "Jak działa" else text)

    def test_labels_explain_themselves(self) -> None:
        text = section("6.10")
        for part in ("najechaniu", "fokusie", "dotknięciu", "`Popover`"):
            with self.subTest(part=part):
                self.assertIn(part, text)


class MotionAndAccess(unittest.TestCase):
    def test_icons_answer_a_press(self) -> None:
        text = section("9")
        self.assertIn("ugina", text)
        self.assertIn("ogranicz ruch", text)

    def test_display_menu_is_part_of_accessibility(self) -> None:
        text = section("10")
        for part in ("„Wygląd”", "150%", "320 px", "wysokim kontraście"):
            with self.subTest(part=part):
                self.assertIn(part, text)


class AgentPrompt(unittest.TestCase):
    def test_prompt_gives_the_new_values(self) -> None:
        text = section("12")
        for part in ("#FFFFFF", "#0A0A0A", "Schibsted Grotesk", "bez linii"):
            with self.subTest(part=part):
                self.assertIn(part, text)
        self.assertNotIn("#1D6A86", text)


class OtherSurfacesWait(unittest.TestCase):
    def test_spec_says_widget_mocks_and_slides_keep_their_look(self) -> None:
        self.assertRegex(SPEC, r"(?s)Wtyczka, makiety platform[^.]*slajdy[^.]*dotychczasow")

    def test_the_one_idea_stays(self) -> None:
        self.assertRegex(SPEC, r"(?m)^### Idea przewodnia: cytat jest dowodem")


if __name__ == "__main__":
    unittest.main()
