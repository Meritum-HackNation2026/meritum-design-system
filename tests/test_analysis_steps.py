"""Checks AnalysisSteps: the web progress bar (design-system#149) and the extension's state words.

The bar's counting runs in node from components/meritum/_analysis-progress.ts (type stripping);
the React markup is checked in the source, since this repo has no React to render it.

Features: US-SPR-02, F-09, design-system#44, design-system#149
Run: python3 -m unittest discover -s tests
"""

import json
import re
import shutil
import subprocess
import unittest
from pathlib import Path

ROOT = Path(__file__).parent.parent
COMPONENT = ROOT / "components" / "meritum" / "analysis-steps.tsx"
PROGRESS = ROOT / "components" / "meritum" / "_analysis-progress.ts"
# Gherkin 1 of #149: three steps done, the three searches in progress, three still to come.
PARALLEL_SEARCHES = [
    {"code": "receive", "status": "done"},
    {"code": "fetch_url", "status": "skipped"},
    {"code": "screen_injection", "status": "done"},
    {"code": "extract_claims", "status": "done"},
    {"code": "search_corpus", "status": "active"},
    {"code": "search_web", "status": "active"},
    {"code": "search_fact_checks", "status": "active"},
    {"code": "assess_evidence", "status": "pending"},
    {"code": "verify_citations", "status": "pending"},
    {"code": "write_answer", "status": "pending"},
]


def progress(steps: list[dict[str, str]]) -> dict[str, object]:
    """Runs analysisProgress() from _analysis-progress.ts in node and returns its result."""
    script = (
        f"const {{ analysisProgress }} = await import({json.dumps(PROGRESS.as_uri())});"
        "const { readFileSync } = await import('node:fs');"
        "const steps = JSON.parse(readFileSync(0, 'utf8'));"
        "process.stdout.write(JSON.stringify(analysisProgress(steps)));"
    )
    out = subprocess.run(
        ["node", "--input-type=module", "-e", script],
        input=json.dumps(steps),
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
        encoding="utf-8",
        timeout=10,
    ).stdout
    return json.loads(out)


@unittest.skipUnless(shutil.which("node"), "node not installed")
class ProgressCount(unittest.TestCase):
    """Scenario: trzy wyszukiwania biegną równolegle."""

    def test_three_parallel_searches_read_step_4_of_9_and_a_third_of_the_bar(self) -> None:
        result = progress(PARALLEL_SEARCHES)
        self.assertEqual((result["step"], result["of"]), (4, 9))
        self.assertAlmostEqual(result["percent"], 100 / 3)
        self.assertEqual([s["code"] for s in result["active"]], ["search_corpus", "search_web", "search_fact_checks"])

    def test_failed_step_is_passed_and_the_last_step_never_exceeds_the_total(self) -> None:
        result = progress([{"code": "receive", "status": "done"}, {"code": "search_web", "status": "failed"}])
        self.assertEqual((result["step"], result["of"], result["percent"]), (2, 2, 100))


class ProgressMarkup(unittest.TestCase):
    """The bar, the counter, the names in progress and the list on request, from copy/pl.json."""

    source = COMPONENT.read_text(encoding="utf-8")

    def test_bar_counter_and_names_of_steps_in_progress(self) -> None:
        self.assertIn('from "@/components/ui/progress"', self.source)
        self.assertIn("<Progress value={progress.percent}", self.source)
        self.assertIn("fill(t.analysis.step_of, { n: progress.step, of: progress.of })", self.source)
        self.assertIn("progress.active.map", self.source)

    def test_full_list_opens_under_show_steps_with_every_state_in_words(self) -> None:
        self.assertIn('from "@/components/ui/collapsible"', self.source)
        trigger = re.search(r"<CollapsibleTrigger[^>]*>\s*\{t\.analysis\.show_steps\}", self.source)
        self.assertIsNotNone(trigger, "the trigger reads analysis.show_steps")
        self.assertIn("{t.analysis.step_status[s.status]}", self.source)
        self.assertIn('const stateIsVisible = s.status === "skipped" || s.status === "failed"', self.source)
        self.assertIn('!stateIsVisible && "sr-only"', self.source)

    def test_live_region_and_the_spinner_as_the_only_loop(self) -> None:
        self.assertEqual(self.source.count('aria-live="polite"'), 1)
        self.assertEqual(re.findall(r"animate-(?:spin|pulse|ping|bounce)\S*", self.source), ["animate-spin"])
        self.assertIn("animate-spin border-verified border-t-transparent motion-reduce:animate-none", self.source)

    def test_no_card_frame_on_the_web_page(self) -> None:
        self.assertNotIn("border border-border", self.source)
        self.assertNotIn("--host-card", self.source)
        self.assertNotIn("<output", self.source)

    def test_draft_stands_below_in_a_quiet_field_without_a_verdict(self) -> None:
        self.assertIn("draft?: Draft", self.source)
        self.assertIn("rounded-lg bg-muted", self.source)
        self.assertIn("{t.analysis.draft}", self.source)
        self.assertNotIn("VerdictBadge", self.source)

    def test_files_stay_under_250_lines(self) -> None:
        for path in (COMPONENT, PROGRESS):
            self.assertLessEqual(len(path.read_text(encoding="utf-8").splitlines()), 250, path.name)
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


@unittest.skipUnless(shutil.which("node"), "node not installed")
class ExtensionSteps(unittest.TestCase):
    """Checks state-word visibility in the public extension renderer (out of scope for #149, kept)."""

    def test_skipped_and_failed_are_visible_while_done_stays_screen_reader_only(self) -> None:
        rendered = subprocess.run(
            ["node", "-e", RENDER_STEPS],
            cwd=ROOT,
            check=True,
            capture_output=True,
            text=True,
            encoding="utf-8",
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
