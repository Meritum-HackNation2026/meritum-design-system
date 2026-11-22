# Meritum components (React + shadcn/ui + Tailwind v4)

Components for the MSZ "Prawdowid" flow: a citizen pastes text or a link in the web form (or clicks "Sprawdź" under a post) and gets a per-claim verdict with verbatim citations. Visual spec: section 6 of `../../DESIGN_SYSTEM.md`. Props are the contract types, so the components render API responses as they come.

## Setup

1. Tokens: paste `../../tokens/meritum.css` into the app's global CSS after `@import "tailwindcss";`.
2. Fonts: Archivo (wdth 75..125, wght 400..800) and Azeret Mono (400..600); the frontend self-hosts them with Fontsource.
3. shadcn primitives (Radix flavour, `asChild` API): `npx shadcn@latest add button collapsible progress textarea tooltip`; `zod` v4 for `toRequest()`; `lucide-react` for the icons of the conversation view and the „Pokaż kroki” chevron.
4. Copy this folder to `src/components/meritum/`, `../../contracts/meritum.ts` to `src/contracts/meritum.ts` and `../../copy/pl.json` to `src/copy/pl.json` (the components import `@/contracts/meritum` and `@/copy/pl.json`; turn on `resolveJsonModule`). Wrap the app in `<TooltipProvider>`.

## Components

| Component | Spec | Props |
|---|---|---|
| `CheckForm` | 6.1 | `onSubmit(CheckRequest)`, `pending`, `serverError` (an `errors` key), `retentionDays`, `onDeleteChecks`. Validates text (3 to 4000 characters) or a full http(s) link with `toRequest()`, a zod schema whose messages are `errors` keys; keeps the text on an error. |
| `QuotedClaim`, `Composer`, `Attachment` | 6.8 | Page of one check (the conversation view with `Question`, `Reply` and `Welcome` is gone, design-system#150). `QuotedClaim`: the citizen's words as the page's h1 with a hanging „ in ink, or `file` (`kind`, `name`) for a recording or an image. `Composer`: a plain field in the page flow (1 px `--input` outline, no shadow, not docked), controlled `value`/`onValueChange`, `onSubmit(CheckRequest)` (same `toRequest()` rules as `CheckForm`), `pending`, `serverError`, `tools` (left of „Sprawdź”), `attachment` with `onSendAttachment`, `placeholder` (default `form.input_placeholder`; the app passes `conversation.next_placeholder` under a finished result). `Attachment`: `kind` (`audio` default, `image`: icon and remove label), `name`, `onRemove`, optional `preview` (image thumbnail) in place of the icon, the file's notes as children. Icons from `lucide-react`. |
| `CheckHistory` | 6.1, 6.8 | Rail list. `items: HistoryItem[]` (newest first; `pending: true` shows „w toku” instead of a badge), `account` (anonymous with `onSignIn`, signed in with sign-out and delete actions, or `false`/left out for no sign-in block), `onOpen(checkId)`, optional `onNew` for „Nowe sprawdzenie” above the list |
| `CheckButton` | 6.2 | `state: "idle" \| "pending" \| "done"`, `onClick`. Takes the host's icon colour through `--host-icon`. |
| `AnalysisSteps` | 6.3 | `steps: AnalysisStep[]` and `draft: Draft` (the streamed text, `null` when none) from `AnalysisStatus`. Web page only: a bar, „Krok n z m”, the names of the steps in progress and the full list under „Pokaż kroki”, no frame; the draft stands below in a quiet field with no verdict. Skipped steps leave both the count and the total, failed ones count as finished, parallel steps share one number (three done and three searches out of nine read „Krok 4 z 9”, a third of the bar). The extension keeps its list in `extension/reference/card.js`. |
| `ResultCard` | 6.4 | `result: CheckResult`. One block per claim; non-verdict statuses get an icon and a sentence, never a badge. Conflicting sources are shown side by side with what differs. |
| `VerdictBadge` | 3, 6.4 | `verdict`, `size: "sm" \| "md" \| "lg"`. `lg` is the verdict word set large without a pill, the head of a claim block on the result card. Red only for "false". |
| `CitationItem` | 6.4 | `citation: Citation`, `showDate` (default `true`): verbatim fragment with a hanging „, then linked title, publisher and date, kind and tier; `showDate={false}` drops the date for the evidence timeline, which shows it itself; `disclaimer` (the publisher's `CatalogEntry.disclaimer`) adds one quiet line under the attribution |
| `StrengthMeter` | 6.4 | `strength: EvidenceStrength`, `claimDate`, `claimDateSource`: word and three bars in ink, premises in words |
| `ModerationQueue` | 6.5 | `cases: ModeratorCase[]`, `selectedId`, `onOpen(id)`. Question count is the sum of checks over a case's claims, the first question included; the line under it (`moderation.similar`, Polish plural forms) repeats that same number. |
| `MeritumMark`, `MeritumLabel` | 2 | Logo B; the label heads every card. Ink on the page and in the panel (`brand/meritum-mark-mono.svg`); sea stem and dot only under `[data-host]`. |
| `t`, `fill`, `plural`, `formatDate` | | the `copy/pl.json` object, `{placeholder}` filling, Polish plural forms (`one`/`few`/`many`/`other`), Polish dates |

`Hint` and `InfoButton` hang tooltips off real buttons, so keyboard users reach every explanation.

In the extension, render inside a Shadow DOM root and inject the compiled CSS there; set `data-host="x|facebook|instagram|reddit|tiktok"` on the root for the platform skin and `class="dark"` when the host is dark. The framework-free twin of `ResultCard` and `AnalysisSteps` is `../../extension/reference/card.js`.

## Legacy

`../legacy/` keeps the components of the earlier scope (NASK fake ads and community notes): `ContextCard`, `QuickReportPopover`, `BotDefenseTelemetry`, `CampaignRotation`. They are not part of the MSZ product.

## Checked

Type-checked with `tsc` (strict, `noUncheckedIndexedAccess`) and linted with `biome lint` inside a copy of meritum-frontend, and rendered there on the contract examples (`contracts/examples.json`) in light and dark mode at 1280 px and 375 px.
