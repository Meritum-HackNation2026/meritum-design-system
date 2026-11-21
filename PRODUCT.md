# Product

<!-- impeccable:product-schema 1 -->

## Platform

web

## Stack

- **Cloud:** GCP and Cloudflare.
- **API:** Python, FastAPI, FastMCP, Pydantic, Pydantic AI, DBOS (durable workflows). Ruff and Ty in strict mode.
- **Architecture:** vertical slices by core domain with hexagonal architecture inside each; every domain repeats the same subfolders (`models/`, `dtos/`, `ports/`, `adapters/`, …). TDD. Architecture tests with pytestarch, behaviour specs with behave.
- **Database:** PostgreSQL with pgvector.
- **Frontend:** React, shadcn/ui with shadcnblocks, TanStack Router, TanStack Query, Tailwind CSS v4, Biome in strict mode.
- **Extension:** a Chrome extension that runs both on the demo mocks (design-system/demo/platforms/) and on the real sites; mocks reproduce the real DOM hooks (see demo/platforms/SELECTORS.md). Framework still open (injected UI should render inside Shadow DOM so host-page CSS cannot leak in either direction).

## Users

- **Social media readers** on X, Instagram, Reddit, Facebook and TikTok who meet a manipulative post or a scam ad in their feed. They spend seconds on it, scrolling, often on a laptop browser. Their job: understand quickly whether the post misleads or the ad is a trap, and why, then move on safely. Older and less digitally confident users are the main victims of investment scams that abuse celebrity likeness.
- **Contributors**: the same readers when they report a manipulation or a fake ad, or rate a note. Their job: flag content in a few clicks and judge whether a draft note is fair.
- **Analysts and operators** (fact-checkers, CERT-style incident handlers, the team during the demo) using the admin panel. Their job: see the bigger picture: which scattered ads and posts belong to one campaign, which attacks on consensus were repelled.
- **Jury** of two challenges: MSZ "Prawdowid" and NASK "Kolekcjoner fejków".

## Product Purpose

An independent, civic trust layer that runs as a browser extension across social platforms and covers two threats: disinformation and manipulation, and scams such as fake ads that abuse celebrity likeness. Users report content; the system links each report to the campaign it belongs to; an AI drafts a context note or a scam warning from user remarks, an analysis of the content, verifiable facts and media coverage from across the political spectrum; a note is published only after people who usually disagree rate it helpful. Success: a reader trusts the note because it visibly did not come from one side, a scam is recognised before money is lost, and a coordinated attack cannot push a note through or bury one.

The product is entered in two hackathon challenges:
- **MSZ "Prawdowid"**: an AI prototype that helps users tell fact from manipulation, reach credible sources and assess content consciously.
- **NASK "Kolekcjoner fejków"**: fake ads abusing celebrity likeness vanish fast, change form and return under new addresses; a single item may be a fragment of a much larger campaign; the task is to see the bigger picture and protect potential victims.

## Positioning

Platform-independent (works the same on five networks, owned by none of them), campaign-aware (every report is a specimen linked to the operation behind it, so one sighting reveals the whole campaign) and bridging-based (publication requires agreement across viewpoints, not a majority, which makes bot farms and brigading ineffective). The AI drafts; people decide; evidence is preserved before a scam disappears.

## Operating Context

- The extension injects its UI into third-party feeds it does not control, in both light and dark platform themes. Injected UI must read as native yet clearly separate and trustworthy.
- Per-platform skins (decided 2026-11-21): the injected widget adapts to each host (X, Facebook, Instagram, Reddit, TikTok): host font and size, corner radius, card surface and border, button style and link colour. Constant everywhere: a small Meritum mark and the name „Meritum” in the widget header, state colours, the two-group consensus bar and mandatory sources. Never a platform logo inside the widget.
- Main demo for the jury: on X, a context card under a manipulative post and a scam warning on a sponsored fake ad; the dashboard shows the scam campaign behind that ad (variants, rotating domains) and a bot farm attack on a note being rejected in real time.
- Materials: the extension, an admin panel with the Live Dashboard, and a pitch deck. Non-technical team members generate slides, mocks and marketing with AI agents from DESIGN_SYSTEM.md.

## Capabilities and Constraints

- Report a manipulation or a scam / fake ad (quick popover in the extension).
- AI-generated context note with mandatory source links and a cross-perspective consensus indicator; voting on notes.
- Scam warning on fake ads, with the campaign it belongs to and preserved evidence (snapshot, URL, redirect chain, time).
- Campaign view: variants of one operation linked across platforms and rotating domains.
- Bot and brigading resistance; telemetry of rejected bot votes versus real user votes.
- UI language: Polish.
- Working name: **Meritum**, subtitle „obywatelski radar dezinformacji oraz scamu”.

## Brand Commitments

- Working name: **Meritum** — „obywatelski radar dezinformacji oraz scamu”. Logo: mark B „Dwa łuki” (brand/meritum-mark.svg), chosen 2026-11-21.
- Visual direction (chosen 2026-11-21): „Biuletyn synoptyczny” palette on clean white bordered surfaces; spec in DESIGN_SYSTEM.md.
- Binding visual constraints from the brief: "Civic-Tech Intelligence / Modern Editorial" (precision of developer tools such as Linear and Vercel with the gravity and legibility of investigative journalism such as The Economist and Bellingcat). Never: hacker green-on-black, purple-blue AI gradients, heavy governmental/official styling, gratuitous animation. Light and dark modes required.

## Evidence on Hand

None yet. No real users, testimonials, partner media, accuracy figures or attack statistics exist. Demo numbers must be labelled as simulated; never present them as real results.

## Product Principles

1. Context, not verdicts: notes explain and cite; they never call people liars.
2. Consensus is the product: show that agreement came from different perspectives, every time.
3. Transparent machinery: AI drafting and bot filtering are visible and explainable, never magic.
4. Guest in someone else's feed: be compact, calm and dismissible; never hijack the page.
5. Resilience on display: an attack is shown as handled, not as panic.
6. One sighting, whole campaign: never treat a fake as an isolated item; show what it belongs to.
7. Protect first, then explain: a scam warning stops the risky step before it teaches.

## Accessibility & Inclusion

WCAG 2.2 AA contrast in both themes, including on top of third-party light and dark feeds. States must not rely on colour alone. Respect prefers-reduced-motion. Polish copy runs longer than English; components must survive long labels.
