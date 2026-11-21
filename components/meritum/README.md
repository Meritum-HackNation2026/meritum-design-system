# Meritum components (React + shadcn/ui + Tailwind v4)

Framework-agnostic React (Vite + TanStack Router in the panel, a content script in the extension).

## Setup

1. Tokens: paste `../../tokens/meritum.css` into the app's global CSS after `@import "tailwindcss";`.
2. Fonts (Google Fonts): Archivo (wdth 75..125, wght 400..800) and Azeret Mono (400..600).
3. shadcn primitives (Radix flavour, `asChild` API):
   `npx shadcn@latest add button badge popover tooltip textarea input label chart`
4. Copy this folder to `src/components/meritum/` and wrap the app in `<TooltipProvider>`.

## Components

Meritum now targets only the MSZ "Prawdowid" challenge: a citizen pastes text or a link in the web form (or clicks "Sprawdź" under a post in the extension) and gets a per-claim verdict with verbatim citations. The visual spec is section 6 of `../../DESIGN_SYSTEM.md`.

### Used in the MSZ flow

| Component | Use | State |
|---|---|---|
| `ContextCard` | Becomes the result card: verdict badge per claim (`confirmed`, `false`, `misleading`, `insufficient_evidence`, `not_verifiable`), explanation labelled as model interpretation, sources with publisher, date and fragment, strength with premises, unresolved, limitations, AI disclosure; non-verdict statuses without a badge. | Needs rework: still has the old `note` / `pending` / `scam` variants. |
| `AnalysisSteps` | Processing strip between "Sprawdź" and the result; drive it from the DBOS workflow status (`AnalysisStep` codes in the contracts). | Needs the new step list. |
| `MeritumMark`, `MeritumLabel` | Logo B; the label is mandatory in every injected widget header. | Ready. |

Still to build: the web form ("Sprawdź informację"), the extension "Sprawdź" button and the moderator queue (sections 6.1, 6.2, 6.5 of the spec).

### Legacy (NASK and community notes), not used in the demo

| Component | Was |
|---|---|
| `QuickReportPopover` | "Zgłoś" button and report form. Replaced by the "Sprawdź" flow. |
| `BotDefenseTelemetry` | Live Dashboard of a bot attack on a note. |
| `CampaignRotation` | Campaign view: domain lifetimes, platform sum, shared traces. |

## In the extension

Render inside a Shadow DOM root and inject the compiled CSS there, so host styles cannot leak in or out.
Set `data-host="x|facebook|instagram|reddit|tiktok"` on the root to pick the platform skin, and
`class="dark"` when the host is in dark mode.

## Contracts

Props should mirror the API contracts in `../../contracts/` (Pydantic source of truth, generated `meritum.ts` types and JSON Schema): `CheckResult`, `ClaimResult`, `Citation`, `Source`, `EvidenceStrength`, `AnalysisStatus`, `ModeratorCase`. The components still declare their own older types; switch them to `meritum.ts` during the rework. UI strings come from `../../copy/pl.json`.

## Checked

`tsc --strict --noUncheckedIndexedAccess` and `biome check` (a11y rules on) pass against stubbed shadcn primitives. Tooltips hang off real buttons (an info icon or the domain name), so keyboard users reach every explanation.
