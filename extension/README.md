# Meritum Chrome extension kit

The extension is Meritum's second channel for the MSZ "Prawdowid" challenge. The primary channel is the web form, where a citizen pastes text or a link. The extension adds the same check where people meet the content: a „Sprawdź” (Check) button under posts on X, Facebook, Instagram, Reddit and TikTok, and the same paste box in the toolbar popup.

Both channels call the same verification API with the same `CheckRequest` (`../contracts/meritum.ts` and `meritum.schema.json`, a synced copy that is never edited by hand; the single source of truth is the meritum-core repository) and render the same `CheckResult`. The extension holds no verification logic of its own, so the same request with the same corpus version gives the same verdicts and citations on both channels (MSZ scenario G).

Rules for this channel:

- Nothing leaves the page until the user clicks „Sprawdź”. Then the content script sends the post text and its URL (`text`, `page_url`) to `background.js`, which calls the API. No feed scanning, no automatic cards.
- No automatic warnings on ads. The scam card and the „hide ad” flow from the earlier NASK scope are out.
- The result card shows one of five verdicts per claim (confirmed, false, misleading, insufficient evidence, not verifiable) with citations (title, publisher, date, link, fragment), the premises behind the strength and the limitations. Technical failure, „needs clarification” and „out of scope” are shown as statuses, never as verdicts. All strings come from `../copy/pl.json`.

The real Manifest V3 extension is built in the [meritum-extension](https://github.com/Meritum-HackNation2026/meritum-extension) repository (WXT, React, TypeScript). This folder is its reference kit: the Shadow DOM widget styles, a working framework-free content script, the toolbar popup, onboarding and options pages, and icons. The same content script runs on the real sites and on the local mocks in `demo/platforms/`. The visual spec is `../DESIGN_SYSTEM.md`. The code in `reference/` runs the „Sprawdź” flow on a mocked API; what is still missing for the real API is under „What must change” below.

## Load it

1. `chrome://extensions`, turn on Developer mode, **Load unpacked**, pick this `extension/` folder.
2. Open a deployed mock: https://meritum-x.gburek.app (or `meritum-facebook`, `meritum-instagram`, `meritum-reddit`, `meritum-tiktok`; the dev versions end in `-dev`, e.g. https://meritum-x-dev.gburek.app; add `?theme=dark`). They are served by [meritum-mocks](https://github.com/Meritum-HackNation2026/meritum-mocks) from a copy of `demo/platforms/`. To test changes to the mocks before they are deployed, serve `design-system/` locally on port 52990 (`python3 -m http.server 52990` from `design-system/`) and open `http://localhost:52990/demo/platforms/x/`.

`manifest.json` lives at the extension root, not in `reference/`: Chrome only loads files under the manifest's folder, and the popup, icons and `widget.css` sit next to `reference/`.

Without installing anything: `demo/live/<platform>/` loads the same `reference/api.js`, `reference/card.js` and `reference/content.js` as plain scripts (see "Stage demo").

## File map

| Path | What it is |
|---|---|
| `manifest.json` | MV3 manifest: content scripts for x.com, twitter.com, facebook.com, instagram.com, reddit.com, tiktok.com, the deployed mocks (`https://*.gburek.app/*`) and `http://localhost:52990/*`; `widget.css` and `pl.json` are web-accessible; permissions `storage`, `activeTab` |
| `widget.css` | Widget styles for Shadow DOM, tokens from `tokens/meritum.css`: „Sprawdź” button, analysis strip, result card, platform skins |
| `pl.json` | Symlink to `../copy/pl.json`: every string the widget shows, keyed by contract codes |
| `reference/content.js` | Content script: platform detection, post discovery, injection, theme detection, the check on click |
| `reference/card.js` | `MeritumCard`: the result card and the analysis strip as HTML strings (same structure as `components/meritum/result-card.tsx`), shared by the content script and the popup |
| `reference/input.js` | `MeritumInput.toRequest(raw, channel)`: the popup's input check, same rules and `errors` keys as `toRequest()` in `components/meritum/check-form.tsx` (`tests/test_popup_input.py` keeps the limits equal) |
| `reference/api.js` | Mocked API, `MeritumAPI.check(request, onStatus)`: contract-shaped `CheckResult` and `AnalysisStatus` for the stage demo only (see below) |
| `reference/background.js` | Service-worker stub: first-run tab, default settings; this is where the real `fetch` to the check API goes |
| `ui.css` | Tokens and small components for the extension's own pages |
| `popup/popup.html`, `.css`, `.js` | Toolbar popup, 360 px wide: the web form's paste box (text or link) with the result card, the per-site switch and „Twoje sprawdzenia”. Preview states with `?state=active\|paused\|unsupported\|offline&theme=light\|dark` |
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
| `components/meritum/check-button.tsx` | `.m-check` in `inject()` |
| `components/meritum/analysis-steps.tsx` | `.m-proc` from `MeritumCard.steps()` |
| `components/meritum/result-card.tsx` (with `verdict-badge`, `citation-item`, `strength-meter`) | `.m-card` from `MeritumCard.card()` |
| `components/meritum/meritum-mark.tsx` | `mark()` in `content.js` and `card.js` (inline SVG, accent from `--m-sea`) |

If you build the widget in React instead (meritum-extension does), render `components/meritum/` into the shadow roots with the compiled Tailwind CSS, or keep `card.js` markup and adopt `widget.css`. `demo/widgets/` shows the card in every skin.

Link colours in the skins are the hosts' blues darkened where needed to pass 4.5:1 (X light `#1D6FB0` instead of `#1D9BF0`). Meritum's state colours, mark and sources never change per platform.

## Shadow DOM recipe

Every injected node is `<meritum-root data-part="..." data-host="x">` with an open shadow root:

- `data-part="button"`: the „Sprawdź” button in the action bar.
- `data-part="slot"`: block under the post (check progress, result card).
- `data-part="overlay"`: one per page, appended to `<body>`: the `aria-live` region.

Why this shape:

- `meritum-root` is a valid custom element name, so `attachShadow()` works without `customElements.define()` (content scripts have no custom element registry), and host rules like `div[role=group] > div` never match it.
- `widget.css` is fetched once and turned into one constructed `CSSStyleSheet`, adopted by every shadow root (`root.adoptedStyleSheets = [SHEET]`). No per-post `<style>` copies.
- Chrome ignores `@font-face` inside shadow roots, so `content.js` copies the four `@font-face` rules into `document.adoptedStyleSheets`. The families are named `Meritum Archivo` / `Meritum Azeret Mono` so they never clash with the page.
- Host-page CSS outranks `:host` rules (`*{margin:0}` would win), so all spacing lives on elements inside the shadow root. The one exception, TikTok's floating slot, is positioned with an inline style.
- Each shadow root stops `click`, `keydown`, `keyup`, `keypress` from leaving it: X opens the post on click and has single-key shortcuts (`l` likes, `j`/`k` move).
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

| Platform | Post | „Sprawdź” goes | Slot goes | Sponsored | Watch out for |
|---|---|---|---|---|---|
| X | `article[data-testid="tweet"]` | into `[role="group"]`, before the bookmark slot | after `[role="group"]` | ancestor `[data-testid="placementTracking"]` | virtualised `cellInnerDiv`s are recycled for other posts; id = status link |
| Facebook | closest `[data-virtualized]` around `[data-ad-rendering-role="profile_name"]` | appended to the row holding `share_button`'s `div[role="button"]` | after that row | `a[aria-label="Sponsorowane"]` (not `textContent`, FB splits it into letters) | `data-virtualized="true"` units are emptied and re-rendered; skip them |
| Instagram | `main article` | into the left group of the action `section`, next to Udostępnij | after the `section` | a `span` reading „Sponsorowane” | only ~4 articles in DOM at once; find icons by `svg[aria-label]` |
| Reddit | `shreddit-post`, `shreddit-ad-post` | own light-DOM row right after the post element, inside its `article` | after that row | `shreddit-ad-post` / `promoted` | the action row is in the post's shadow root and may re-render; new pages arrive via `faceplate-partial` |
| TikTok | `article[data-e2e="recommend-list-item-container"]` | after `[data-e2e="share-icon"]` in the actions column, as a 48 px round action with caption | floating over the bottom of the video (no room under a full-height video) | a `span` reading „Sponsorowane” | scrolling happens in `#column-list-container`, not `window` |

Reddit selectors and TikTok ad labels were not observed live (see `SELECTORS.md`): check them before a live demo.

## Post lifecycle

- `mounted: WeakMap<post, {id, btn, slot}>`. A post is skipped only when its id is unchanged and its button is still connected. A recycled node (new id) or a re-render that dropped our nodes gets fresh hosts.
- `checks: Map<postId, CheckResult>`. When a known post is re-rendered (virtualised lists), the card is restored instantly, without the animation. A technical failure is not kept, so the next click retries.
- Cloned posts (the mocks' infinite scroll uses `cloneNode`) carry our element without its shadow root; those dead hosts are removed before injecting.

## Accessibility

- The button is a real `<button>` with `aria-busy` while the check runs; afterwards it reads „Sprawdzono” and a second click scrolls to the card.
- The analysis strip is an `<output>`, so step changes are announced; one polite `aria-live` region in the overlay announces the main verdict when the card opens.
- Focus ring 2 px in the accent colour; verdicts always carry a word („Potwierdzone”, „Fałszywe”, „Brak wystarczających dowodów”…), never colour alone.
- `prefers-reduced-motion`: animations drop to ~0, timed steps shorten to 120 ms.

## Performance

- One `MutationObserver` on `document.body` (`childList`, `subtree`), throttled to one scan per 150 ms; mutation batches that only touch our own nodes are ignored. Mutations inside our shadow roots are never observed.
- A second observer watches only three attributes on `<html>` and `<body>` for theme changes.
- Scans read selectors and attributes only, never layout (the one style read is TikTok's `position` check, once per post). - One shared stylesheet object for all shadow roots.

## What must change (TODO)

The reference runs the „Sprawdź” flow end to end on `reference/api.js`, a mock with two fixed answers (`/płask|krzywizn/`, `/Rewiński|inwest-polska24|1 200 zł/`); anything else gets „Poza zakresem”. The MSZ brief forbids answers that depend on hardcoded examples, so the mock is for the stage demo and visual checks only. Before the jury tries the extension:

- **`reference/background.js`:** add a message handler (`meritum:check`) that POSTs the `CheckRequest` (`channel: "extension"`, `text`, `page_url`) to the check API, polls or streams `AnalysisStatus`, and returns the `CheckResult`. Content scripts are bound by the host page's CORS and CSP, so the `fetch` must live here. Map no network, rate limit and HTTP errors to the `errors.*` and `status.technical_failure` copy, never to a verdict.
- **`reference/api.js`:** replace the body of `check()` with that message, keeping its signature; then delete the fixed answers.

## Stage demo (no extension)

`demo/live/` holds copies of the five mocks with `reference/api.js`, `reference/card.js`, `reference/content.js` and a demo control. Today they run on the mock answers; once `api.js` calls the real API, this is also how the jury can try the second channel without installing anything (`demo/live/demo.js`: reset `R`, theme `T`, „Przyspiesz” runs the flow 3x faster). Rebuild them after a mock changes with `sh demo/live/build.sh`. If the extension is also installed, only one copy runs (`html[data-meritum-active]`).

## Known limits

- Fonts load from `fonts.gstatic.com`. A host CSP with a strict `font-src` (X has one) can block them; the widget then falls back to `system-ui`. For production, ship the woff2 files in the extension and point the `@font-face` URLs at `chrome.runtime.getURL()`; check that the host CSP allows them.
- X's action bar is four flexible slots. With „Sprawdzono” in the bar, a long count such as „184 tys.” can wrap to two lines on a 600 px column. If that matters, use the fallback from `SELECTORS.md`: a separate row right after `[role="group"]`.
- Clones of the same X post share a status link, so a checked post's card also appears on later clones in the mock feed.
