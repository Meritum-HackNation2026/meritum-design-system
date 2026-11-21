"""Checks visible AnalysisSteps state words through the framework-free renderer.

Features: US-SPR-02, F-09, design-system#44
Run: python3 -m unittest discover -s tests
"""

import subprocess
import unittest
from pathlib import Path

ROOT = Path(__file__).parent.parent
RENDER_STEPS = """
const fs = require("node:fs");
globalThis.eval(fs.readFileSync("extension/reference/card.js", "utf8"));
const copy = JSON.parse(fs.readFileSync("copy/pl.json", "utf8"));
MeritumCard.use(copy);
process.stdout.write(MeritumCard.steps({
  draft: false,
  steps: [
    { code: "fetch_url", status: "skipped" },
    { code: "receive", status: "done" },
    { code: "search_web", status: "failed" },
  ],
}));
"""


class AnalysisSteps(unittest.TestCase):
    """Checks state-word visibility in the public extension renderer."""

    def test_skipped_and_failed_are_visible_while_done_stays_screen_reader_only(self) -> None:
        rendered = subprocess.run(
            ["node", "-e", RENDER_STEPS],
            cwd=ROOT,
            check=True,
            capture_output=True,
            text=True,
            timeout=10,
        ).stdout

        self.assertIn(
            '<span class="m-step-status"><span class="m-sr">, </span>pominięte</span>',
            rendered,
        )
        self.assertIn(
            '<span class="m-step-status"><span class="m-sr">, </span>nieudane</span>',
            rendered,
        )
        self.assertIn('<span class="m-sr">, gotowe</span>', rendered)


if __name__ == "__main__":
    unittest.main()
