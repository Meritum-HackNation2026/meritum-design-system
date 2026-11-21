"""Writes meritum.schema.json and validates the demo examples. Run via generate.sh."""

import json
from pathlib import Path

from pydantic import TypeAdapter

import meritum_contracts as c

HERE = Path(__file__).parent
ROOTS = {
    "InjectedCard": c.InjectedCard,
    "ReportPayload": c.ReportPayload,
    "AnalysisStatus": c.AnalysisStatus,
    "BotDefenseSnapshot": c.BotDefenseSnapshot,
    "Campaign": c.Campaign,
}

defs: dict[str, object] = {}
for name, tp in ROOTS.items():
    schema = TypeAdapter(tp).json_schema(ref_template="#/$defs/{model}")
    defs.update(schema.pop("$defs", {}))
    defs[name] = schema
out = {"$schema": "https://json-schema.org/draft/2020-12/schema", "title": "Meritum UI contracts", "$defs": defs}
(HERE / "meritum.schema.json").write_text(json.dumps(out, ensure_ascii=False, indent=2) + "\n")

# Self-check: the demo data must validate, and the rules that keep the UI honest must reject bad data.
examples = json.loads((HERE / "examples.json").read_text())
for name, payload in examples.items():
    TypeAdapter(ROOTS[name.split(".")[0]]).validate_python(payload)
bad = examples["Campaign"] | {"ads_total": 48}
try:
    c.Campaign.model_validate(bad)
except ValueError:
    pass
else:
    raise AssertionError("a campaign whose platform sum does not close must be rejected")
try:
    c.ReportPayload.model_validate(examples["ReportPayload"] | {"reasons": [], "note": "  "})
except ValueError:
    pass
else:
    raise AssertionError("a report with no reason and no note must be rejected")
print(f"ok: {len(defs)} schema definitions, {len(examples)} examples valid")
