#!/usr/bin/env bash
# Refresh this copy of the Meritum contracts from meritum-core, the single source
# of truth. Copies only the files core generates for consumers; the contracts
# themselves live in core's package src/meritum_core/checks/contracts/.
#   contracts/sync.sh            copy from core's main
#   contracts/sync.sh <ref>      copy from another branch, tag or commit
# Never edit the copied files by hand: CI (contracts.yml) checks them against
# SHA256SUMS. Change the contracts in meritum-core, then run this script.
# Needs `gh` signed in with read access to Meritum-HackNation2026/meritum-core.
set -euo pipefail
cd "$(dirname "$0")"
repo=Meritum-HackNation2026/meritum-core
ref=$(gh api "repos/$repo/commits/${1:-main}" --jq .sha)
fetch() { gh api -H 'Accept: application/vnd.github.raw' "repos/$repo/contents/$1?ref=$ref"; }

rm -f meritum_contracts.py # stale copy of the former checks/contracts.py
fetch contracts/examples.json >examples.json
fetch contracts/meritum.schema.json >meritum.schema.json
fetch contracts/meritum.ts >meritum.ts

printf 'meritum-core %s\n' "$ref" >SOURCE
sha256sum examples.json meritum.schema.json meritum.ts >SHA256SUMS
echo "contracts synced from $repo@${ref:0:12}"
