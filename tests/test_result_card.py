"""Checks that the reference result cards word non-verdict states and limitations from copy, never `message`.

Features: US-SPR-04, F-17, design-system#53
Run: python3 -m unittest discover -s tests
"""

import json
import re
import shutil
import subprocess
import unittest
from pathlib import Path

ROOT = Path(__file__).parent.parent
COPY = json.loads((ROOT / "copy" / "pl.json").read_text(encoding="utf-8"))
EXAMPLES = json.loads((ROOT / "contracts" / "examples.json").read_text(encoding="utf-8"))
CARD_JS = ROOT / "extension" / "reference" / "card.js"
CARD_TSX = ROOT / "components" / "meritum" / "result-card.tsx"
RAW = "RAW API MESSAGE"


def render(result: dict) -> str:
    """Renders one CheckResult with extension/reference/card.js in node."""
    script = (
        f"require({json.dumps(str(CARD_JS))});"
        "const [copy, result] = JSON.parse(require('fs').readFileSync(0, 'utf8'));"
        "MeritumCard.use(copy); process.stdout.write(MeritumCard.card(result));"
    )
    out = subprocess.run(["node", "-e", script], input=json.dumps([COPY, result]), capture_output=True, text=True, check=True)
    return out.stdout


@unittest.skipUnless(shutil.which("node"), "node not installed")
class ReferenceCardTest(unittest.TestCase):
    def test_failure_code_text_never_message(self) -> None:
        html = render({**EXAMPLES["CheckResult.failure"], "message": RAW})
        self.assertIn(COPY["failure_code"]["web_search_unavailable"], html)
        self.assertNotIn(RAW, html)

    def test_status_hint_without_failure_code(self) -> None:
        for status in ("needs_clarification", "out_of_scope", "technical_failure"):
            html = render({**EXAMPLES["CheckResult.failure"], "status": status, "failure_code": None, "message": RAW})
            self.assertIn(COPY["status_hint"][status], html)
            self.assertNotIn(RAW, html)

    def test_limitation_codes_worded_from_copy(self) -> None:
        result = EXAMPLES["CheckResult.claim_review"]
        html = render(result)
        self.assertIn(COPY["limitation_code"]["image_search_not_run"], html)
        self.assertNotIn(result["limitations"][0], html)


class ResultCardSourceTest(unittest.TestCase):
    # shortcut: this repo has no TS test runner, so the TSX twin of card.js is checked by source; render it once one exists
    def test_tsx_never_reads_message(self) -> None:
        source = CARD_TSX.read_text(encoding="utf-8")
        self.assertIsNone(re.search(r"\bresult\.message\b", source))
        self.assertIn("failure_code", source)
        self.assertIn("limitation_codes", source)
