"""Writes meritum.schema.json and validates the examples. Run via generate.sh."""

import json
from collections.abc import Callable
from pathlib import Path
from typing import Any

from pydantic import TypeAdapter

import meritum_contracts as c

HERE = Path(__file__).parent
ROOTS: dict[str, Any] = {
    "CheckRequest": c.CheckRequest,
    "CheckResult": c.CheckResult,
    "AnalysisStatus": c.AnalysisStatus,
    "CheckRecord": c.CheckRecord,
    "ModeratorCase": c.ModeratorCase,
    "CatalogEntry": c.CatalogEntry,
}

defs: dict[str, object] = {}
for name, tp in ROOTS.items():
    schema = TypeAdapter(tp).json_schema(ref_template="#/$defs/{model}")
    defs.update(schema.pop("$defs", {}))
    defs[name] = schema
out = {"$schema": "https://json-schema.org/draft/2020-12/schema", "title": "Meritum contracts", "$defs": defs}
(HERE / "meritum.schema.json").write_text(json.dumps(out, ensure_ascii=False, indent=2) + "\n")

# Self-check: the examples must validate, and the rules from the MSZ brief must reject bad data.
examples = {k: v for k, v in json.loads((HERE / "examples.json").read_text()).items() if not k.startswith("$")}
for name, payload in examples.items():
    TypeAdapter(ROOTS[name.split(".")[0]]).validate_python(payload)

done, claim = examples["CheckResult.done"], examples["CheckResult.done"]["claims"][0]


def with_claim(**changes: object) -> dict[str, object]:
    return done | {"claims": [claim | changes]}


def must_reject(label: str, build: Callable[[], object]) -> None:
    try:
        build()
    except ValueError:
        return
    raise AssertionError(f"must be rejected: {label}")


must_reject("settling verdict without citations", lambda: c.CheckResult.model_validate(with_claim(citations=[])))
must_reject("'confirmed' backed only by a refuting citation", lambda: c.CheckResult.model_validate(with_claim(verdict="confirmed")))
must_reject("strength that does not follow the premises", lambda: c.CheckResult.model_validate(with_claim(strength={"level": "strong", "premises": claim["strength"]["premises"]})))
must_reject("insufficient evidence without saying what is missing", lambda: c.CheckResult.model_validate(with_claim(verdict="insufficient_evidence", unresolved=None)))
must_reject("finished check without limitations", lambda: c.CheckResult.model_validate(done | {"limitations": []}))
must_reject("technical failure shown with claims", lambda: c.CheckResult.model_validate(examples["CheckResult.failure"] | {"claims": done["claims"]}))
must_reject("recommendation dressed up as a hand-off", lambda: c.Escalation.model_validate({"state": "recommended", "case_id": "#S-1"}))
must_reject("hand-off without a case", lambda: c.Escalation.model_validate({"state": "created"}))
must_reject("request with neither text nor URL", lambda: c.CheckRequest.model_validate({"channel": "web", "text": "  "}))
must_reject("citation whose fragment was not found", lambda: c.Citation.model_validate(claim["citations"][0] | {"fragment_found_verbatim": False}))
print(f"ok: {len(defs)} schema definitions, {len(examples)} examples valid, 10 rules hold")
