"""Sensitive Data Protection register and web masked-data copy (design-system#47).

Features: US-BEZ-04, F-20, ADR-13, ADR-14, ADR-35
Run: python3 -m unittest discover -s tests
"""

import json
import unittest
from pathlib import Path

PRIVACY = json.loads((Path(__file__).parent.parent / "copy" / "privacy.json").read_text(encoding="utf-8"))
ACTIVE = {item["id"]: item for item in PRIVACY["processors"]["items"]}
WEB_DATA = PRIVACY["policies"]["web"]["data"]


class SensitiveDataProtection(unittest.TestCase):
    def test_region_is_regional_europe_central2_endpoint(self) -> None:
        # Criterion: region says „GCP europe-central2 (Warszawa), endpoint regionalny”
        self.assertEqual(
            "GCP europe-central2 (Warszawa), endpoint regionalny",
            ACTIVE["sensitive_data_protection"]["region"],
        )

    def test_data_says_user_input_and_step_results_reach_dlp_before_masking(self) -> None:
        # Criterion: data says user input and step results reach DLP before masking.
        # Exact string so the old „…przed maskowaniem i wyniki kroków” fails.
        self.assertEqual(
            "Wejście użytkownika i wyniki kroków przed maskowaniem",
            ACTIVE["sensitive_data_protection"]["data"],
        )


class WebMaskedDataTypes(unittest.TestCase):
    def test_web_policy_lists_all_masked_data_types(self) -> None:
        # Criterion: policies.web.data lists phone, e-mail, PESEL, address,
        # document numbers, accounts and cards (DESIGN_SYSTEM.md §8 tone).
        # Full parenthetical so „adres e-mail” / „karcie przeglądarki” alone cannot pass.
        self.assertIn(
            "(telefon, e-mail, PESEL, adres, numery dokumentów, konta i karty)",
            WEB_DATA,
        )


if __name__ == "__main__":
    unittest.main()
