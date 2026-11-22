"""Checks that deleting the account has its own confirmation, not the one for session checks.

Features: US-BEZ-05, F-31, meritum-frontend#98
Run: python3 -m unittest discover -s tests
"""

import json
import unittest
from pathlib import Path

ACCOUNT = json.loads((Path(__file__).parent.parent / "copy" / "pl.json").read_text(encoding="utf-8"))["account"]


class AccountDelete(unittest.TestCase):
    """The confirmation of „Usuń konto i historię” (`account.delete_account_*`)."""

    def test_confirmation_names_account_history_and_that_it_is_final(self) -> None:
        text = ACCOUNT["delete_account_text"].lower()
        self.assertIn("konto", ACCOUNT["delete_account_title"].lower())
        self.assertIn("konto", text)
        self.assertIn("histori", text)
        self.assertIn("nie da się cofnąć", text)
        self.assertIn("konto", ACCOUNT["delete_account_yes"].lower())


if __name__ == "__main__":
    unittest.main()
