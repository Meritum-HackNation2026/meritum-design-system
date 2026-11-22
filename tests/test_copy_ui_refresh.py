"""Checks the texts of the refreshed web page: navigation, the check page, label hints, the display menu.

Features: US-SPR-01, US-SPR-04, US-ZRD-12, US-DST-01, F-01, F-17, F-29, design-system#145
Run: python3 -m unittest discover -s tests
"""

import unittest

from test_contract_copy import codes
from test_copy import lookup

# (schema $def, property, copy section with one sentence of explanation per code)
HINTS = (
    ("Source", "kind", "source_kind_hint"),
    ("Source", "tier", "source_tier_hint"),
    ("EvidenceStrength", "level", "strength_hint"),
)
SCREEN_KEYS = (
    "nav.check",
    "nav.how",
    "nav.privacy",
    "nav.sign_in",
    "nav.menu",
    "nav.account",
    "nav.on_page",
    "check_page.new",
    "check_page.next",
    "check_page.sample",
    "analysis.step_of",
    "analysis.show_steps",
    "result.strength_facts.independent",
    "result.strength_facts.primary",
    "result.strength_facts.newest",
    "display.title",
    "display.label",
    "display.theme_title",
    "display.theme.light",
    "display.theme.dark",
    "display.theme.contrast",
    "display.text_title",
    "display.text.m",
    "display.text.l",
    "display.text.xl",
    "display.text.xxl",
    "method.path.title",
    "method.path.lead",
    "method.verdicts.title",
    "method.details.title",
)


class LabelHints(unittest.TestCase):
    def test_every_small_label_has_one_sentence_of_explanation(self) -> None:
        # Gherkin "każda mała etykieta ma objaśnienie"
        for definition, prop, section in HINTS:
            for code in codes(definition, prop):
                with self.subTest(code=f"{section}.{code}"):
                    hint = lookup(f"{section}.{code}")
                    self.assertIsInstance(hint, str, f"{section}.{code} is missing")
                    self.assertNotIn(". ", hint)  # one sentence; a dot inside a name such as dane.gov.pl is fine
                    self.assertTrue(hint.endswith("."), hint)

    def test_strength_hints_follow_the_contract_rule(self) -> None:
        # strong: two or more agreeing independent publishers, one of them primary, fresh evidence;
        # moderate: two agreeing publishers or one primary; weak: one non-primary publisher or outdated evidence
        strong, moderate, weak = (str(lookup(f"strength_hint.{level}")) for level in ("strong", "moderate", "weak"))
        for word in ("dwóch", "pierwotny", "aktualne"):
            self.assertIn(word, strong)
        for word in ("Dwóch", "albo", "pierwotne"):
            self.assertIn(word, moderate)
        for word in ("Jeden", "albo", "nieaktualny"):
            self.assertIn(word, weak)


class ClaimCount(unittest.TestCase):
    def test_claim_count_declines_in_polish(self) -> None:
        # Gherkin "liczba twierdzeń odmienia się po polsku": Intl.PluralRules('pl') gives one, few, many
        forms = {form: str(lookup(f"result.claims_count.{form}")) for form in ("one", "few", "many", "other")}
        self.assertEqual(forms["one"].format(count=1), "1 twierdzenie")
        self.assertEqual(forms["few"].format(count=2), "2 twierdzenia")
        self.assertEqual(forms["many"].format(count=5), "5 twierdzeń")
        self.assertIn("{count}", forms["other"])


class ScreenTexts(unittest.TestCase):
    def test_new_screens_have_their_texts(self) -> None:
        for key in SCREEN_KEYS:
            with self.subTest(key=key):
                value = lookup(key)
                self.assertIsInstance(value, str, f"{key} is missing")
                self.assertTrue(value.strip(), f"{key} is empty")

    def test_step_counter_names_both_numbers(self) -> None:
        self.assertEqual(str(lookup("analysis.step_of")).format(n=4, of=9), "Krok 4 z 9")

    def test_new_sections_say_who_uses_them(self) -> None:
        for section in ("nav", "check_page", "display", "source_kind_hint", "source_tier_hint", "strength_hint"):
            with self.subTest(section=section):
                self.assertIn("#", str(lookup(f"{section}.$comment")))


if __name__ == "__main__":
    unittest.main()
