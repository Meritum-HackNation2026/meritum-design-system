# Meritum components (React + shadcn/ui + Tailwind v4)

Framework-agnostic React (Vite + TanStack Router in the panel, a content script in the extension).

## Setup

1. Tokens: paste `../../tokens/meritum.css` into the app's global CSS after `@import "tailwindcss";`.
2. Fonts (Google Fonts): Archivo (wdth 75..125, wght 400..800) and Azeret Mono (400..600).
3. shadcn primitives (Radix flavour, `asChild` API):
   `npx shadcn@latest add button badge popover tooltip textarea input label chart`
4. Copy this folder to `src/components/meritum/` and wrap the app in `<TooltipProvider>`.

## Components

| Component | Use |
|---|---|
| `QuickReportPopover` | "Zgłoś" button injected into a post's action bar + the report form. `onSubmit` returns a promise. |
| `AnalysisSteps` | Processing strip between "Wysłane" and the result; drive it from the DBOS workflow status. |
| `ContextCard` | `variant="note" | "pending" | "scam"`. `sources` is a non-empty tuple: a card without a source does not type-check. |
| `BotDefenseTelemetry` | Live Dashboard widget; totals are summed from `series`, so the sum line always closes. |
| `MeritumMark`, `MeritumLabel` | Logo B; the label is mandatory in every injected widget header. |

## In the extension

Render inside a Shadow DOM root and inject the compiled CSS there, so host styles cannot leak in or out.
Set `data-host="x|facebook|instagram|reddit|tiktok"` on the root to pick the platform skin, and
`class="dark"` when the host is in dark mode.

Not compiled in this repo yet: there is no app scaffold. Run `tsc --noEmit` and `biome check` after copying.
