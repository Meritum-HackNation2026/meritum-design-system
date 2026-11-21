"""Checks that every code in the contract copy (contracts/meritum.schema.json) has text in copy/pl.json.

Features: US-ZRD-06, US-SPR-06, US-SPR-02, US-POW-01, US-ZRD-11, US-BEZ-03, F-17, F-18, F-26, ADR-29, design-system#10, design-system#66
Run: python3 -m unittest discover -s tests
"""

import json
import unittest
from collections.abc import Iterator
from pathlib import Path

from test_copy import lookup

ROOT = Path(__file__).parent.parent
SCHEMA = json.loads((ROOT / "contracts" / "meritum.schema.json").read_text(encoding="utf-8"))
# copy keys in a code section that are not contract codes: a staff role outside ModeratorCase,
# core/015 not synced yet, and status texts for one input kind
NOT_IN_CONTRACT = {
    "escalation.not_saved",
    "moderation.role.admin",
    "notifications.kind.eval_run_done",
    "status_hint.out_of_scope_image",
    "status_hint.out_of_scope_audio_format",
    "status_hint.technical_failure_url",
}
PROVIDERS = ("google", "gemini", "anthropic", "claude", "openai", "brave", "speech-to-text", "chirp")

# (schema $def, property, copy sections that need a text for each value, values without text)
ENUM_COPY = (
    ("ClaimResult", "verdict", ("verdict", "verdict_hint"), ()),
    ("CheckResult", "status", ("status", "status_hint"), ("done",)),
    ("CheckResult", "failure_code", ("failure_code",), ()),
    ("CheckResult", "limitation_codes", ("limitation_code",), ()),
    ("ClaimResult", "would_change_verdict", ("would_change_verdict",), ()),
    ("ClaimResult", "claim_date_source", ("result.claim_date_source",), ()),
    ("AnalysisStep", "code", ("analysis.steps",), ()),
    ("AnalysisStep", "status", ("analysis.step_status",), ()),
    ("Notification", "kind", ("notifications.kind",), ()),
    ("Notification", "status", ("notifications.status",), ()),
    ("IncidentMatch", "match_basis", ("match_basis",), ()),
    ("IncidentMatch", "database", ("result.incident_database",), ()),
    ("EvidenceStrength", "level", ("strength",), ()),
    ("Premises", "agreement", ("result.agreement",), ()),
    ("Citation", "stance", ("result.stance",), ()),
    ("Escalation", "state", ("escalation",), ()),
    ("Source", "kind", ("source_kind",), ()),
    ("Source", "tier", ("source_tier",), ()),
    ("ModeratorCase", "reasons", ("moderation.reason",), ()),
    ("ModeratorCase", "state", ("moderation.state",), ()),
    ("ModeratorCase", "assignee_role", ("moderation.role",), ()),
    ("ModeratorCase", "high_risk_classified_by", ("moderation.high_risk_by",), ()),
)


def enum_values(node: object) -> Iterator[str]:
    """Yield every enum value under a schema node (plain, array items or nullable anyOf)."""
    if isinstance(node, dict):
        yield from node.get("enum", ())
        for key in ("items", "anyOf"):
            if key in node:
                yield from enum_values(node[key])
    elif isinstance(node, list):
        for item in node:
            yield from enum_values(item)


def codes(definition: str, prop: str) -> list[str]:
    """Return the enum values of one schema property; fail when the property has none."""
    values = list(enum_values(SCHEMA["$defs"][definition]["properties"][prop]))
    assert values, f"{definition}.{prop} has no enum in the schema"
    return values


class EveryContractCodeHasText(unittest.TestCase):
    def test_enum_values_have_text(self) -> None:
        # Gherkin "każdy kod z kontraktu ma tekst" from design-system#10
        for definition, prop, sections, skipped in ENUM_COPY:
            for code in codes(definition, prop):
                if code in skipped:
                    continue
                for section in sections:
                    with self.subTest(code=f"{definition}.{prop}={code}", section=section):
                        value = lookup(f"{section}.{code}")
                        self.assertIsInstance(value, str, f"{section}.{code} is missing")
                        self.assertTrue(value.strip(), f"{section}.{code} is empty")

    def test_every_technique_has_name_and_how_to_spot(self) -> None:
        for code in codes("ClaimResult", "technique"):
            for field in ("name", "how_to_spot"):
                with self.subTest(technique=code, field=field):
                    self.assertTrue(str(lookup(f"techniques.{code}.{field}") or "").strip())

    def test_copy_sections_hold_no_codes_the_contract_dropped(self) -> None:
        for definition, prop, sections, _ in ENUM_COPY:
            known = set(codes(definition, prop))
            for section in sections:
                with self.subTest(section=section):
                    node = lookup(section)
                    self.assertIsInstance(node, dict, section)
                    extra = {key for key in node if key != "$comment" and key not in known} - {
                        key.rsplit(".", 1)[1] for key in NOT_IN_CONTRACT if key.startswith(f"{section}.")
                    }
                    self.assertFalse(extra, f"{section} has keys the contract does not define: {extra}")


class FailureTexts(unittest.TestCase):
    def test_failure_codes_read_as_technical_problem_without_provider(self) -> None:
        for code in codes("CheckResult", "failure_code"):
            text = str(lookup(f"failure_code.{code}"))
            with self.subTest(code=code):
                self.assertIn("To nie jest ocena treści.", text)
                for name in PROVIDERS:
                    self.assertNotIn(name, text.lower())

    def test_fact_check_unavailable_names_access_error_not_missing_article(self) -> None:
        # Gherkin "awaria indeksu fact-checkerów" from design-system#10 (jury scenario J)
        text = str(lookup("limitation_code.fact_check_unavailable"))
        self.assertIn("indeksu Google", text)
        self.assertIn("błędu dostępu", text)
        self.assertIn("nie znaczy, że", text)


class JuryScenarioAnswers(unittest.TestCase):
    def test_no_result_does_not_mean_no_change(self) -> None:
        # jury scenario D
        self.assertIn("nie oznacza, że zmiany nie było", str(lookup("result.no_change_hint")))

    def test_date_on_image_does_not_confirm_publication_date(self) -> None:
        # jury scenario F
        self.assertIn("nie potwierdza", str(lookup("result.image_date_hint")))

    def test_eval_run_done_notification_names_the_evaluation_run(self) -> None:
        # core/015 key, before the EvalRun contract lands
        self.assertIn("ewaluacji", str(lookup("notifications.kind.eval_run_done")))


if __name__ == "__main__":
    unittest.main()
