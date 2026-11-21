#!/usr/bin/env bash
# Publishes the demo pages to Cloudflare Pages (project meritum-demo), behind Cloudflare Access.
# Access app "Meritum demo (HackNation2026)" guards meritum-demo.pages.dev and *.meritum-demo.pages.dev.
# Needs: wrangler logged in (wrangler login) on the account that owns the project.
set -euo pipefail
cd "$(dirname "$0")/.."
OUT=$(mktemp -d)
trap 'rm -rf "$OUT"' EXIT
rsync -a --exclude '.git' --exclude '.impeccable' --exclude '.DS_Store' --exclude '__pycache__' \
  --exclude 'node_modules' --exclude 'artifact' --exclude '*.pptx' --exclude 'contracts' --exclude 'copy' \
  --exclude 'components' --exclude 'tokens' --exclude '*.py' --exclude '*.sh' --exclude 'docs' --exclude '*.md' \
  --exclude 'scripts' ./ "$OUT/"
# Landing page lives at demo/index.html; serve it at the site root with root-relative links.
sed 's#\.\./##g; s#href="\([a-z]*\)/"#href="demo/\1/"#g' demo/index.html > "$OUT/index.html"
wrangler pages deploy "$OUT" --project-name meritum-demo --branch main --commit-dirty=true
