"""Checks that every text naming masked data lists the same types and says what stays visible.

Features: US-BEZ-04, US-BEZ-06, F-20, ADR-13, ADR-35 (design-system#61)
Source of the list: copy/privacy.json "masking", after meritum-core#102 (INFO_TYPE_MARKERS).
Run: python3 -m unittest discover -s tests
"""

import json
import re
import unittest
from html import unescape
from pathlib import Path

ROOT = Path(__file__).parent.parent
PRIVACY = json.loads((ROOT / "copy" / "privacy.json").read_text(encoding="utf-8"))
PL = json.loads((ROOT / "copy" / "pl.json").read_text(encoding="utf-8"))
DOC = unescape((ROOT / "docs" / "product-doc.html").read_text(encoding="utf-8"))
MASKING = PRIVACY["masking"]
MASKED = MASKING["masked"]
KEPT = MASKING["kept"]


def section(pattern: str) -> str:
    """Text of the first product document block matched by a regex that ends before the next block."""
    match = re.search(pattern, DOC, re.S)
    assert match, pattern
    return match.group(1)


STORY = section(r"<strong>US-BEZ-04</strong>(.*?)</tr>")
ADR = section(r"<h3[^>]*>ADR-13\.(.*?)(?=<h[1-3])")
GLOSSARY = section(r"Maskowanie danych osobowych</strong></td>(.*?)</tr>")
CORE_TYPES = {"telefon", "e-mail", "PESEL", "dowód osobisty", "paszport", "numer konta", "karta płatnicza"}


class MaskingListIsOneEverywhere(unittest.TestCase):
    def test_list_matches_core_info_types(self):
        self.assertEqual(CORE_TYPES, set(MASKED))

    def test_site_policy_and_ui_text_list_every_type(self):
        for name, text in (("policies.web.data", PRIVACY["policies"]["web"]["data"]), ("pl.json form.privacy", PL["form"]["privacy"])):
            for label in MASKED:
                self.assertIn(label, text, f"{name}: {label}")

    def test_product_doc_lists_every_type_in_story_adr_and_glossary(self):
        for name, text in (("US-BEZ-04", STORY), ("ADR-13", ADR), ("słownik", GLOSSARY)):
            for label in MASKED:
                self.assertIn(label, text, f"{name}: {label}")

    def test_site_policy_and_adr_say_what_stays_visible(self):
        self.assertIn(KEPT, PRIVACY["policies"]["web"]["data"])
        self.assertIn(KEPT, ADR)
        self.assertIn("osób publicznych", PL["form"]["privacy"])

    def test_address_is_not_listed_as_masked(self):
        self.assertNotIn("adres,", PRIVACY["policies"]["web"]["data"])


if __name__ == "__main__":
    unittest.main()
