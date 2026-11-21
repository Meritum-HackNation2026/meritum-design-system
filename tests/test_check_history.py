"""Checks that CheckHistory can render without its sign-in block.

Features: US-BEZ-05, F-20, design-system#74
Run: python3 -m unittest discover -s tests
"""

import re
import unittest
from pathlib import Path

SOURCE = (Path(__file__).parent.parent / "components" / "meritum" / "check-history.tsx").read_text(encoding="utf-8")
SIGN_IN_TEXTS = ("t.account.optional", "t.account.sign_in_google", "t.account.stored", "t.account.sign_out")


class CheckHistoryAccountTest(unittest.TestCase):
    # shortcut: this repo has no TS test runner, so the component is checked by source; render it once one exists
    def test_account_false_hides_the_sign_in_block(self) -> None:
        # Gherkin "historia bez bloku logowania" from design-system#74
        self.assertRegex(SOURCE, r"account\??: Account \| false")
        block = re.search(r"\{account && \((.*)\)\}\s*</section>", SOURCE, re.DOTALL)
        assert block, "the sign-in block is not guarded by `account &&`"
        for text in SIGN_IN_TEXTS:
            self.assertEqual(SOURCE.count(text), block.group(1).count(text), text)


if __name__ == "__main__":
    unittest.main()
