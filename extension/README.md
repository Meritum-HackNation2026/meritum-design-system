# Meritum Chrome extension kit

Everything a developer needs to build the real Manifest V3 extension: the Shadow DOM widget styles, a working framework-free content script, the toolbar popup, onboarding and options pages, and icons. The same content script runs on the real sites and on the local mocks in `demo/platforms/`. The visual spec is `../DESIGN_SYSTEM.md`.

## Load it

1. `chrome://extensions`, turn on Developer mode, **Load unpacked**, pick this `extension/` folder.
2. Serve `design-system/` on port 52990 (`python3 -m http.server 52990` from `design-system/`) and open `http://localhost:52990/demo/platforms/x/` (or `facebook`, `instagram`, `reddit`, `tiktok`; add `?theme=dark`).

`manifest.json` lives at the extension root, not in `reference/`: Chrome only loads files under the manifest's folder, and the popup, icons and `widget.css` sit next to `reference/`.

Without installing anything: `demo/live/<platform>/` loads the same `reference/api.js` + `reference/content.js` as plain scripts (see "Stage demo").

## File map

| Path | What it is |
|---|---|
| `manifest.json` | MV3 manifest: content scripts for x.com, twitter.com, facebook.com, instagram.com, reddit.com, tiktok.com and `http://localhost:52990/*`; `widget.css` is web-accessible; permissions `storage`, `activeTab` |
| `widget.css` | Widget styles for Shadow DOM. Built from `demo/meritum.css` (same class names) + `tokens/meritum.css` |
| `reference/content.js` | Content script: platform detection, post discovery, injection, report popover, send / analysis / reveal flow, theme detection |
| `reference/api.js` | Mocked API, `MeritumAPI.submitReport()` |
| `reference/background.js` | Service-worker stub: first-run tab, default settings; where real API calls belong |
| `ui.css` | Tokens and small components for the extension's own pages |
| `popup/popup.html`, `.css`, `.js` | Toolbar popup, 360 px wide, ~560 px tall. Preview states with `?state=active\|paused\|unsupported\|offline&theme=light\|dark` |
| `popup/states.html` | All popup states, light and dark, on one page |
| `onboarding/welcome.html` | First-run page (opened by `background.js` on install) |
| `onboarding/options.html` | Options page (`options_ui`) |
| `onboarding/settings.js`, `pages.css` | Shared settings binding and layout for both pages |
| `icons/icon-16/32/48/128.png` | Toolbar and store icons. 48 and 128 are `brand/meritum-app-icon.svg`; 16 and 32 use `icons/meritum-icon-small.svg`, a variant with a 40% thicker stroke and less padding so the arches stay readable at 16 px |

## How the kit maps to the design system

| Design system | Extension |
|---|---|
| `tokens/meritum.css` `:root` / `.dark` roles | `widget.css` `:host` / `:host(.dark)` as short `--m-*` names (`--m-ink` = `--foreground`, `--m-ink2` = `--muted-foreground`, `--m-sea` = `--verified`, `--m-red` = `--scam`, `--m-amber` = `--contested-foreground`, ...) and `ui.css` `:root` for the pages |
| `[data-host]` skins in `tokens/meritum.css` | `:host([data-host="x\|facebook\|instagram\|reddit\|tiktok"])`: host font, card radius, button radius, link colour, card background and border (light and dark) |
| `components/meritum/quick-report-popover.tsx` | `.m-pop` markup in `openReport()` |
| `components/meritum/analysis-steps.tsx` | `.m-proc` in `analyse()` |
| `components/meritum/context-card.tsx` | `.m-card` in `noteCard()` / `scamCard()`, data shape from `api.js` |
| `components/meritum/meritum-mark.tsx` | `mark()` in `content.js` (inline SVG, accent from `--m-sea`) |

If you build the widget in React instead, render the same components into the shadow roots and adopt `widget.css` there; class names match `demo/meritum.css`, so markup copied from `demo/x/` works unchanged.

Link colours in the skins are the hosts' blues darkened where needed to pass 4.5:1 (X light `#1D6FB0` instead of `#1D9BF0`). Meritum's state colours, mark and sources never change per platform.

## Shadow DOM recipe

Every injected node is `<meritum-root data-part="..." data-host="x">` with an open shadow root:

- `data-part="button"`: the "Zgłoś" button in the action bar.
- `data-part="slot"`: block under the post (analysis strip, card, thank-you line).
- `data-part="overlay"`: one per page, appended to `<body>`: popover, toasts, the `aria-live` region.
- `data-part="placeholder"`: the "Reklama ukryta" row that replaces a hidden ad.

Why this shape:

- `meritum-root` is a valid custom element name, so `attachShadow()` works without `customElements.define()` (content scripts have no custom element registry), and host rules like `div[role=group] > div` never match it.
- `widget.css` is fetched once and turned into one constructed `CSSStyleSheet`, adopted by every shadow root (`root.adoptedStyleSheets = [SHEET]`). No per-post `<style>` copies.
- Chrome ignores `@font-face` inside shadow roots, so `content.js` copies the four `@font-face` rules into `document.adoptedStyleSheets`. The families are named `Meritum Archivo` / `Meritum Azeret Mono` so they never clash with the page.
- Host-page CSS outranks `:host` rules (`*{margin:0}` would win), so all spacing lives on elements inside the shadow root. The one exception, TikTok's floating slot, is positioned with an inline style.
- Each shadow root stops `click`, `keydown`, `keyup`, `keypress` from leaving it: X opens the post on click and has single-key shortcuts (`l` likes, `j`/`k` move).
- Popover is `position: fixed` in the overlay, placed from the button's rect, re-placed on `scroll` (capture phase, so TikTok's inner scroll container counts) and `resize`. It opens under the button; if there is no room, the page scrolls to make room, and only a page that cannot scroll (TikTok) gets it above.
- Mode is `open` for debugging. Switch to `closed` for production (`mkHost()` in `content.js`).

## Theme detection

`pageIsDark()` reads the computed `background-color` of `<body>`, then `<html>` (skipping transparent ones), and treats relative luminance under 0.4 as dark; with no opaque background it falls back to `prefers-color-scheme`. The result toggles `.dark` on every `meritum-root`. A small `MutationObserver` watches only `class`, `style` and `data-theme` on `<html>` and `<body>`, which covers every host's own theme hook:

- X: `body style="background-color: ..."` only
- Facebook, Instagram: `__fb-dark-mode` / `__fb-light-mode` on `<html>`
- Reddit: `theme-dark` / `theme-light` on `<html>` (unverified, see `SELECTORS.md`)
- TikTok: `data-theme="dark"` on `<html>` or `<body>`

The popup and pages follow the "Wygląd" setting (`light`, `dark`, `auto`) from `chrome.storage.local`. On the platforms the widget always follows the host.

## Injection points (summary of `demo/platforms/SELECTORS.md`)

Never select by class; all five sites hash them.

| Platform | Post | "Zgłoś" goes | Slot goes | Sponsored | Watch out for |
|---|---|---|---|---|---|
| X | `article[data-testid="tweet"]` | into `[role="group"]`, before the bookmark slot | after `[role="group"]` | ancestor `[data-testid="placementTracking"]` | virtualised `cellInnerDiv`s are recycled for other posts; id = status link |
| Facebook | closest `[data-virtualized]` around `[data-ad-rendering-role="profile_name"]` | appended to the row holding `share_button`'s `div[role="button"]` | after that row | `a[aria-label="Sponsorowane"]` (not `textContent`, FB splits it into letters) | `data-virtualized="true"` units are emptied and re-rendered; skip them |
| Instagram | `main article` | into the left group of the action `section`, next to Udostępnij | after the `section` | a `span` reading „Sponsorowane” | only ~4 articles in DOM at once; find icons by `svg[aria-label]` |
| Reddit | `shreddit-post`, `shreddit-ad-post` | own light-DOM row right after the post element, inside its `article` | after that row | `shreddit-ad-post` / `promoted` | the action row is in the post's shadow root and may re-render; new pages arrive via `faceplate-partial` |
| TikTok | `article[data-e2e="recommend-list-item-container"]` | after `[data-e2e="share-icon"]` in the actions column, as a 48 px round action with caption | floating over the bottom of the video (no room under a full-height video) | a `span` reading „Sponsorowane” | scrolling happens in `#column-list-container`, not `window` |

Reddit selectors and TikTok ad labels were not observed live (see `SELECTORS.md`): check them before a live demo.

## Post lifecycle

- `mounted: WeakMap<post, {id, btn, slot}>`. A post is skipped only when its id is unchanged and its button is still connected. A recycled node (new id) or a re-render that dropped our nodes gets fresh hosts.
- `reports: Map<postId, {result}>`. When a known post is re-rendered (virtualised lists), the card is restored instantly, without the animation.
- Cloned posts (the mocks' infinite scroll uses `cloneNode`) carry our element without its shadow root; those dead hosts are removed before injecting.

## Accessibility

- The button is a real `<button>` with `aria-haspopup="dialog"` and `aria-expanded`; after sending it reads „Zgłoszono” and gets `aria-disabled="true"`.
- The popover is `role="dialog"` `aria-modal="true"`, labelled by its title. Focus moves to the selected type radio, `Tab` / `Shift+Tab` cycle inside it, `Esc` closes it from anywhere (capture-phase listener) and returns focus to the button. Outside click closes it.
- One polite `aria-live` region in the overlay announces: sending, sent, each analysis step, note published / ad flagged, ad hidden. Send errors use `role="alert"`.
- Focus ring 2 px in the accent colour; states always carry a word („Zweryfikowany”, „W ocenie”, „Oszustwo”), never colour alone.
- `prefers-reduced-motion`: animations drop to ~0, timed steps shorten to 120 ms.

## Performance

- One `MutationObserver` on `document.body` (`childList`, `subtree`), throttled to one scan per 150 ms; mutation batches that only touch our own nodes are ignored. Mutations inside our shadow roots are never observed.
- A second observer watches only three attributes on `<html>` and `<body>` for theme changes.
- Scans read selectors and attributes only, never layout (the one style read is TikTok's `position` check, once per post). Layout is read for popover placement, inside `requestAnimationFrame`, and only while the popover is open.
- Scroll and resize listeners exist only while the popover is open.
- One shared stylesheet object for all shadow roots.

## What is mocked

- `reference/api.js`: `submitReport(report)` waits 300 ms and returns a note for the flat-earth post, a scam warning for the Finanse Dziś ad (matched on handle and text), and a „thanks, first report” result for anything else. It throws when `navigator.onLine` is false, which shows the error line in the popover. Replace it with a message to `background.js`, which does the real `fetch` (content scripts are bound by the host page's CORS and CSP). Keep the response shape `{ id, steps, result }`; `result` shapes are documented at the top of `api.js`.
- Analysis steps are timed (1 s each), not driven by the server. A real backend should stream or poll step status.
- „Zobacz kampanię”, „Zgłoś platformie”, „Pomocne / Niepomocne” only show a toast.
- The panel URL `https://meritum.example/panel` is a placeholder.
- „Tryb opiekuna” exists in the popup and options (stored as `guardian`), but the content script does not change anything yet.
- The popup's per-item „Na tej stronie” list is sample markup; the content script answers `meritum:summary` with counts only.
- Pausing a site writes `paused` and reloads the tab; the content script reads it on load.

## Stage demo (no extension)

`demo/live/` holds copies of the five mocks with `reference/api.js`, `reference/content.js` and a demo control (`demo/live/demo.js`: reset `R`, theme `T`, „Przyspiesz” runs the flow 3x faster). Rebuild them after a mock changes with `sh demo/live/build.sh`. If the extension is also installed, only one copy runs (`html[data-meritum-active]`).

## Known limits

- Fonts load from `fonts.gstatic.com`. A host CSP with a strict `font-src` (X has one) can block them; the widget then falls back to `system-ui`. For production, ship the woff2 files in the extension and point the `@font-face` URLs at `chrome.runtime.getURL()`; check that the host CSP allows them.
- X's action bar is four flexible slots. With „Zgłoszono” in the bar, a long count such as „184 tys.” can wrap to two lines on a 600 px column. If that matters, use the fallback from `SELECTORS.md`: a separate row right after `[role="group"]`.
- Clones of the same X post share a status link, so a reported post's card also appears on later clones in the mock feed.
