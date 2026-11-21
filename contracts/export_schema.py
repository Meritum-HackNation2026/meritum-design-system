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


rejections: list[str] = []


def must_reject(label: str, build: Callable[[], object]) -> None:
    rejections.append(label)
    try:
        build()
    except ValueError:
        return
    raise AssertionError(f"must be rejected: {label}")


must_reject("settling verdict without citations", lambda: c.CheckResult.model_validate(with_claim(citations=[])))
must_reject("'confirmed' backed only by a refuting citation", lambda: c.CheckResult.model_validate(with_claim(verdict="confirmed")))
must_reject("strength that does not follow the premises", lambda: c.CheckResult.model_validate(with_claim(strength={"level": "strong", "premises": claim["strength"]["premises"]})))
must_reject("insufficient evidence without saying what is missing", lambda: c.CheckResult.model_validate(with_claim(verdict="insufficient_evidence", unresolved=None)))
premises = claim["strength"]["premises"]
must_reject("'conflicting' flag the citations do not show", lambda: c.CheckResult.model_validate(with_claim(strength={"level": "weak", "premises": premises | {"agreement": "conflicting"}})))
must_reject("'misleading' without context or technique", lambda: c.CheckResult.model_validate(with_claim(verdict="misleading")))
# conflicting credible sources: "insufficient_evidence" with both sides cited, no strength
refuting = claim["citations"][0]
supporting = refuting | {"stance": "supports", "fragment": "Prezydent może sprawować urząd przez trzy kadencje (fragment testowy)."}
must_reject("'confirmed' with a refuting citation next to the supporting one", lambda: c.CheckResult.model_validate(with_claim(verdict="confirmed", citations=[supporting, refuting])))
must_reject("conflicting sources shown with a strength level", lambda: c.CheckResult.model_validate(with_claim(verdict="insufficient_evidence", unresolved="Źródła podają różną liczbę kadencji.", citations=[supporting, refuting])))
c.CheckResult.model_validate(with_claim(verdict="insufficient_evidence", unresolved="Źródła podają różną liczbę kadencji.", citations=[supporting, refuting], strength=None))
must_reject("insufficient evidence with citations but no conflict", lambda: c.CheckResult.model_validate(with_claim(verdict="insufficient_evidence", unresolved="Brak danych.", strength=None)))
# independence per publisher: two pages of one institution count once
same_publisher = refuting | {"fragment": "Prezydent Rzeczypospolitej jest wybierany przez Naród w wyborach powszechnych."}
must_reject("two pages of one publisher counted as two sources", lambda: c.CheckResult.model_validate(with_claim(citations=[refuting, same_publisher], strength={"level": "moderate", "premises": premises | {"independent_sources": 2}})))
c.CheckResult.model_validate(with_claim(citations=[refuting, same_publisher]))
# age is measured against the claim's date; thresholds come from the catalogue; some evidence does not expire
stale = {"level": "moderate", "premises": premises | {"newest_source_age_hours": 900 * 24}}
must_reject("stale evidence not marked archival", lambda: c.CheckResult.model_validate(with_claim(strength=stale)))
c.CheckResult.model_validate(with_claim(strength=stale, archival=True))
short_lived = {"level": "moderate", "premises": premises | {"newest_source_age_hours": 48, "max_age_hours": 24}}
must_reject("weather warning older than its catalogue threshold not marked archival", lambda: c.CheckResult.model_validate(with_claim(strength=short_lived)))
for validity in ("in_force", "updated_in_place", "past_event"):
    lasting = {"level": "moderate", "premises": stale["premises"] | {"validity": validity}}
    c.CheckResult.model_validate(with_claim(strength=lasting))
    must_reject(f"{validity} evidence marked archival", lambda lasting=lasting: c.CheckResult.model_validate(with_claim(strength=lasting, archival=True)))
catalog = examples["CatalogEntry"]
must_reject("catalogue entry that does not expire but has a maximum age", lambda: c.CatalogEntry.model_validate(catalog | {"validity": "in_force", "max_age_hours": 24}))
must_reject("'past_event' set for a whole catalogue entry", lambda: c.CatalogEntry.model_validate(catalog | {"validity": "past_event"}))
c.CatalogEntry.model_validate(catalog | {"domain": "meteo.imgw.pl", "validity": "expires", "max_age_hours": 6})
must_reject("finished check without limitations", lambda: c.CheckResult.model_validate(done | {"limitations": []}))
must_reject("technical failure shown with claims", lambda: c.CheckResult.model_validate(examples["CheckResult.failure"] | {"claims": done["claims"]}))
must_reject("recommendation dressed up as a hand-off", lambda: c.Escalation.model_validate({"state": "recommended", "case_id": "#S-1"}))
must_reject("hand-off without a case", lambda: c.Escalation.model_validate({"state": "created"}))
must_reject("request with neither text nor URL", lambda: c.CheckRequest.model_validate({"channel": "web", "text": "  "}))
must_reject("citation whose fragment was not found", lambda: c.Citation.model_validate(claim["citations"][0] | {"fragment_found_verbatim": False}))
print(f"ok: {len(defs)} schema definitions, {len(examples)} examples valid, {len(rejections)} rules hold")
