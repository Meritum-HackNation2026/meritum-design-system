"""Checks that docs/product-doc.html states the controller and retention periods of copy/privacy.json.

Features: US-ZRD-12, US-BEZ-02, US-BEZ-05, ADR-13 (design-system#21)
Run: python3 -m unittest discover -s tests
"""

import json
import re
import unittest
from html import unescape
from pathlib import Path

ROOT = Path(__file__).parent.parent
PRIVACY = json.loads((ROOT / "copy" / "privacy.json").read_text(encoding="utf-8"))
DOC = unescape((ROOT / "docs" / "product-doc.html").read_text(encoding="utf-8"))
WEB = PRIVACY["policies"]["web"]
CONTROLLER = PRIVACY["controller"]


def story(story_id: str) -> str:
    """Text of one user story row in the product document."""
    match = re.search(rf"<strong>{story_id}</strong>(.*?)</tr>", DOC, re.S)
    assert match, story_id
    return match.group(1)


def adr(adr_id: str) -> str:
    """Text of one ADR section, from its heading to the next one."""
    match = re.search(rf"<h3[^>]*>{adr_id}\.(.*?)(?=<h[1-3])", DOC, re.S)
    assert match, adr_id
    return match.group(1)


def days(text: str) -> set[str]:
    """Retention periods (exact sets, so a stray extra period also fails) in days named in a text ("14 dni", "po 30 dniach")."""
    return set(re.findall(r"(\d+) dni", text))


class ProductDocMatchesPrivacy(unittest.TestCase):
    def test_adr13_names_ip_log_and_rate_limit_retention(self):
        text = adr("ADR-13")
        self.assertEqual(days(WEB["ip_addresses"]) | days(WEB["retention"]), days(text))
        self.assertIn("okna limitu", WEB["ip_addresses"])
        self.assertIn("okna limitu", text)

    def test_rate_limit_story_names_ip_log_retention(self):
        text = story("US-BEZ-02")
        self.assertEqual(days(WEB["ip_addresses"]), days(text))
        self.assertIn("okna limitu", text)

    def test_deletion_story_names_history_retention(self):
        text = story("US-BEZ-05")
        self.assertEqual(days(WEB["retention"]), days(text))
        self.assertIn("„Usuń konto”", text)

    def test_controller_and_contact_match_policies(self):
        for text in (story("US-ZRD-12"), story("US-BEZ-05"), adr("ADR-13")):
            self.assertIn(CONTROLLER["name"], text)
            self.assertIn(CONTROLLER["contact"], text)
        self.assertIn(CONTROLLER["no_partnership"], story("US-ZRD-12"))

    def test_sign_in_account_data_is_the_same_everywhere(self) -> None:
        """Product doc, KEY_SELLING_POINTS.md, PRODUCT.md and the register name the same sign-in data (design-system#30)."""
        register = next(i for i in PRIVACY["processors"]["items"] if i["id"] == "sign_in")
        self.assertIn("Imię i nazwisko, adres e-mail i identyfikator konta", register["data"])
        self.assertNotIn("starczy czasu", register["purpose"])
        for name in ("KEY_SELLING_POINTS.md", "PRODUCT.md"):
            text = (ROOT / name).read_text(encoding="utf-8")
            row = next(line for line in text.splitlines() if line.startswith("| Google") and ("sign-in" in line or "(logowanie)" in line))
            self.assertNotIn("starczy czasu", row)
            self.assertNotIn("if time allows", row)
            self.assertTrue(
                "imię i nazwisko, adres e-mail i identyfikator konta" in row or "name, e-mail address and account id" in row,
                name,
            )
        self.assertIn("imię i nazwisko, adres e-mail i identyfikator konta", story("US-SPR-10"))
        self.assertIn("imię i nazwisko, adres e-mail i identyfikator konta", DOC)


if __name__ == "__main__":
    unittest.main()
