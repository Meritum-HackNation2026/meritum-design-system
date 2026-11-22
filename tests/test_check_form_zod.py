"""CheckForm validates the field with a zod schema; its messages are `errors` keys of copy/pl.json.

Features: US-SPR-01, F-01, design-system#55
Run: python3 -m unittest discover -s tests
"""

import json
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).parent.parent
FORM = (ROOT / "components" / "meritum" / "check-form.tsx").read_text(encoding="utf-8")
ERRORS = json.loads((ROOT / "copy" / "pl.json").read_text(encoding="utf-8"))["errors"]
KEYS = ("empty", "too_long", "invalid_url", "url_too_long")


class CheckFormZod(unittest.TestCase):
    def test_form_imports_zod_and_parses_with_a_schema(self) -> None:
        self.assertRegex(FORM, r'import \{ z \} from "zod"')
        self.assertRegex(FORM, r"\.safeParse\(")

    def test_every_schema_message_is_an_errors_key(self) -> None:
        for key in KEYS:
            with self.subTest(key=key):
                self.assertIn(key, ERRORS)
                self.assertIn(f'"{key}" satisfies ErrorKey', FORM)

    def test_limits_come_from_the_contract_constants(self) -> None:
        self.assertRegex(FORM, r"\.min\(MIN, ")
        self.assertRegex(FORM, r"\.max\(MAX, ")
        self.assertRegex(FORM, r"\.max\(MAX_URL, ")
        self.assertEqual(re.search(r"const MIN = (\d+)", FORM).group(1), "3")

    def test_no_hand_rolled_length_checks_left(self) -> None:
        self.assertNotIn('return "too_long"', FORM)
        self.assertNotIn('"empty" :', FORM)
        self.assertNotIn("url.href.length >", FORM)


if __name__ == "__main__":
    unittest.main()
