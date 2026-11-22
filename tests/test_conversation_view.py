"""Checks that the conversation view of the web page is described, tokenised and exported.

Features: US-SPR-01, US-SPR-09, F-01, design-system#79, design-system#103
Run: python3 -m unittest discover -s tests
"""

import re
import unittest
from pathlib import Path

ROOT = Path(__file__).parent.parent
INDEX = (ROOT / "components" / "meritum" / "index.ts").read_text(encoding="utf-8")
TOKENS = (ROOT / "tokens" / "meritum.css").read_text(encoding="utf-8")
SPEC = (ROOT / "DESIGN_SYSTEM.md").read_text(encoding="utf-8")


class ConversationView(unittest.TestCase):
    def test_components_are_exported_from_the_index(self) -> None:
        exported = re.search(r'export \{([^}]*)\} from "\./conversation"', INDEX)
        self.assertIsNotNone(exported)
        names = {name.strip() for name in exported.group(1).split(",")} if exported else set()
        self.assertEqual(names, {"Attachment", "Composer", "Question", "Reply", "Welcome"})

    def test_composer_takes_a_placeholder_and_is_shorter_on_a_phone(self) -> None:
        # design-system#103
        composer = (ROOT / "components" / "meritum" / "conversation.tsx").read_text(encoding="utf-8")
        self.assertIn("placeholder = t.form.input_placeholder", composer)
        self.assertIn("placeholder={placeholder}", composer)
        self.assertRegex(composer, r"max-h-\d+ min-h-11 sm:max-h-48")

    def test_tokens_have_the_welcome_size_and_the_entry_motion(self) -> None:
        self.assertRegex(TOKENS, r"--text-headline:\s*1\.875rem;\s*--text-headline--line-height:\s*2\.25rem;")
        self.assertRegex(TOKENS, r"--animate-enter:\s*rise 0\.24s var\(--ease-out-meritum\) both;")

    def test_design_system_describes_the_check_page(self) -> None:
        # design-system#146: the check page replaced the conversation view; the components follow in #150
        section = SPEC.split("### 6.8 Strona sprawdzenia", 1)[-1].split("\n### ", 1)[0]
        self.assertIn("### 6.8 Strona sprawdzenia", SPEC)
        for part in ("nagłówek-cytat", "bez dymków", "nie jest przyklejone", "`Composer`", "`CheckHistory`"):
            with self.subTest(part=part):
                self.assertIn(part, section)


if __name__ == "__main__":
    unittest.main()
