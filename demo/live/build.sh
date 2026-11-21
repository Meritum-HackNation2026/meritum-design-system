#!/bin/sh
# Regenerates demo/live/<platform>/index.html from the clean mocks in demo/platforms/ (which stay untouched):
# fixes the asset paths and loads the extension's api.js + content.js (+ widget.css via content.js) and the demo control.
set -eu
cd "$(dirname "$0")"
for p in x facebook instagram reddit tiktok; do
  mkdir -p "$p"
  sed -e 's#"\.\./assets/#"../../platforms/assets/#g' \
      -e 's#<title>\(.*\)</title>#<title>\1, demo Meritum</title>#' \
      -e 's#</body>#<script src="../../../extension/reference/api.js"></script>\
<script src="../../../extension/reference/content.js"></script>\
<script src="../demo.js"></script>\
</body>#' \
      "../platforms/$p/index.html" > "$p/index.html"
done
echo "demo/live: 5 pages rebuilt"
