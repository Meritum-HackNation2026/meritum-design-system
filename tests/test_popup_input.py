"""Popup input validation matches CheckForm's toRequest() (same error keys).

Features: F-01, ADR-08, design-system#38
Run: python3 -m unittest discover -s tests
"""

import json
import re
import subprocess
import unittest
from pathlib import Path

ROOT = Path(__file__).parent.parent
RUN = """
const fs = require("node:fs");
globalThis.eval(fs.readFileSync("extension/reference/input.js", "utf8"));
const inputs = JSON.parse(process.argv[1]);
process.stdout.write(JSON.stringify(inputs.map(v => MeritumInput.toRequest(v, "extension"))));
"""


def validate(*inputs: str) -> list:
    out = subprocess.run(
        ["node", "-e", RUN, json.dumps(inputs)], cwd=ROOT, check=True, capture_output=True, text=True, timeout=10
    ).stdout
    return json.loads(out)


class PopupInput(unittest.TestCase):
    def test_rejects_what_check_form_rejects(self) -> None:
        got = validate("ab", "ftp://example.com", "https://a.pl/" + "x" * 2071, "x" * 4001, "http://")
        self.assertEqual(got, ["empty", "invalid_url", "url_too_long", "too_long", "invalid_url"])

    def test_accepts_text_and_links(self) -> None:
        got = validate(" abc ", "x" * 4000, "https://a.pl/" + "x" * 2070)
        self.assertEqual(got[0], {"channel": "extension", "text": "abc"})
        self.assertEqual(got[1]["text"], "x" * 4000)
        self.assertEqual(got[2]["url"], "https://a.pl/" + "x" * 2070)

    def test_limits_match_check_form(self) -> None:
        tsx = (ROOT / "components/meritum/check-form.tsx").read_text(encoding="utf-8")
        js = (ROOT / "extension/reference/input.js").read_text(encoding="utf-8")
        for name in ("MAX", "MAX_URL"):
            pattern = rf"const {name} = (\d+)"
            self.assertEqual(re.search(pattern, tsx).group(1), re.search(pattern, js).group(1))


if __name__ == "__main__":
    unittest.main()
