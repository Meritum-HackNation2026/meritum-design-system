#!/usr/bin/env bash
# Regenerates meritum.schema.json and meritum.ts from meritum_contracts.py and checks the examples.
set -euo pipefail
cd "$(dirname "$0")"
uv run --quiet --with 'pydantic>=2.12' python export_schema.py
npx --yes json-schema-to-typescript@15.0.4 -i meritum.schema.json -o meritum.ts --unreachableDefinitions --additionalProperties false \
  --bannerComment '/* Generated from contracts/meritum_contracts.py by contracts/generate.sh. Do not edit. */'
