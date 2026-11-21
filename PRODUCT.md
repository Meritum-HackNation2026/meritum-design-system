# Product

<!-- impeccable:product-schema 1 -->

## Platform

web

## Stack

- **Cloud:** GCP (`europe-central2`) and Cloudflare. A public demo for the jury plus `docker compose` to run everything locally.
- **API:** Python, FastAPI, FastMCP, Pydantic, Pydantic AI, DBOS (durable workflows). Ruff and Ty in strict mode.
- **Architecture:** vertical slices by core domain with hexagonal architecture inside each; every domain repeats the same subfolders (`models/`, `dtos/`, `ports/`, `adapters/`, …). Channels (web form, extension, MCP, optional Discord) are inbound adapters; the LLM, the web search and the corpus store are outbound adapters behind ports, so a model or provider can be swapped without rebuilding the system. TDD. Architecture tests with pytestarch, behaviour specs with behave.
- **Database:** PostgreSQL with pgvector and full-text search (hybrid retrieval over the corpus).
- **Web search:** a `WebSearch` port; first adapter Firecrawl (search and content extraction), restricted to catalogue domains. Scheduled RSS and sitemap ingestion runs as DBOS workflows without any third-party search.
- **Frontend:** React, shadcn/ui with shadcnblocks, TanStack Router, TanStack Query, Tailwind CSS v4, Biome in strict mode.
- **Extension:** Chrome MV3; a „Sprawdź” button under posts and a paste box in the popup, both calling the same API as the web form. It runs on the demo mocks (design-system/demo/platforms/) and on the real sites; injected UI renders in Shadow DOM.

## Users

- **Citizens** who meet a rumour, a post or a forwarded message and want to know quickly whether it holds up. Many have low digital skills: they should not need to learn verification methods or install anything. Their job: paste the text or link, read a short answer in plain Polish, open the sources if they want.
- **Social media readers** who already use the extension and want to check a post where they see it, with one click.
- **Moderators and analysts** named by the administrator. Their job: take over questions the system could not settle (missing evidence, high risk, repeated questions), see similar questions grouped into one case, and track quality: abstentions, injection attempts, response time, cost.
- **Jury** of the MSZ „Prawdowid” challenge, who run the reference set themselves, without the team's help.

## Product Purpose

A tool that lets a citizen check a claim as easily as sending a message, grounded in an audited set of credible sources. The system extracts the claims worth checking, searches official documents, public data and fact-checkers' corpora (plus fresh publications from catalogue domains), and gives each claim one of five verdicts: confirmed, false, misleading, insufficient evidence, not verifiable. Every finding cites the source (title, publisher, date, link, verbatim fragment); the strength of the answer follows from explicit premises; when evidence is missing the system says so and explains what it could not establish. Technical failure, a request for clarification and out-of-scope input are never shown as verdicts. Instructions found in checked content never change how the system behaves.

Success: a citizen gets an honest, sourced answer in under 30 seconds, through the channel they already use; the jury gets the same result through the web and the extension; nobody is shown a model's guess dressed up as a fact.

The product is entered in one hackathon challenge: **MSZ „Prawdowid”** (fast, easy verification based on credible sources). The full brief is in `../konkursy/`.

## Positioning

Honest by construction: the language model reads, searches and writes, but a verdict needs a verbatim citation, its strength is computed from premises by a fixed rule, and abstaining is a first-class answer. Meets people where they read (a web page anyone can open, and a button under the post they are looking at). Auditable: open source catalogue with reasons for inclusion and exclusion, a record of every check, and data processed in the EEA where possible.

## Operating Context

- Primary channel: a responsive web form. Second channel: the Chrome extension (button under posts plus the popup paste box). Both use the same verification core and must give the same result for the same input and corpus version. We confirm with the MSZ mentors that the extension counts as an equivalent channel; a Discord bot on the same API is the fallback.
- The extension injects UI into third-party feeds in light and dark themes. Per-platform skins (X, Facebook, Instagram, Reddit, TikTok) adapt font, radius, surface, borders and links; the Meritum mark, the verdict word and colour, and the sources block never change. It sends content only after the user clicks.
- Demo for the jury: the same question asked in the web form and on an X mock through the extension, a sourced verdict, an honest abstention with a moderator case, an ignored prompt-injection attempt, and the evaluation results on the reference set. Film under 3 minutes, deck under 12 slides.
- The jury runs it from our instructions, end to end, with no manual help. Nothing in the answer may depend on hard-coded examples.

## Capabilities and Constraints

- Input: text or URL (MVP), screenshot with OCR (bonus). Input validation, length limit, rate limit, automatic masking of obvious personal data.
- Claim extraction: one or more claims per input, facts separated from opinions.
- Retrieval: corpus of at least 100 documents from at least 10 domains and at least two source types (primary or official sources and credible secondary sources), each with publication and retrieval timestamps; live web search only on catalogue domains, and every fetched page joins the corpus.
- Verdict per claim with citations, premises and strength; archival-material warning; neutral source-status warning (for example an EU-sanctioned entity) that never decides the verdict; match to known incidents as context only.
- Abstention without a fake answer, with what is missing; moderator case for unresolved, high-risk and repeated questions, with deduplication; the UI distinguishes „recommended for hand-off” from „handed off”.
- Prompt-injection resistance: source text is data, never instructions; detected attempts are logged.
- Check record: question (masked), time, channel, sources, verdicts, models used, processing region, cost, latency, retrieval errors, injection events; defined retention and a „delete my checks” action for the demo session.
- Evaluation script on a public test set covering the brief's scenarios A–J, reporting macro-F1, citation coverage and correctness, abstention, injection resistance, median latency and cost per 100 checks.
- Exports: JSON and CSV of check records and cases; technique codes mapped to DISARM where an equivalent exists.
- UI language: Polish, plain words. Working name: **Meritum**, subtitle „obywatelski radar dezinformacji”.

## Brand Commitments

- Working name: **Meritum** — „obywatelski radar dezinformacji”. Logo: mark B „Dwa łuki” (brand/meritum-mark.svg), chosen 2026-11-21. Brand exports with the old subtitle („…oraz scamu”) must be regenerated.
- Visual direction (chosen 2026-11-21): „Biuletyn synoptyczny” palette on clean white bordered surfaces; spec in DESIGN_SYSTEM.md.
- Binding visual constraints: "Civic-Tech Intelligence / Modern Editorial" (precision of developer tools such as Linear and Vercel with the gravity and legibility of investigative journalism such as The Economist and Bellingcat). Never: hacker green-on-black, purple-blue AI gradients, heavy governmental/official styling, gratuitous animation. Light and dark modes required.

## Evidence on Hand

None yet. No real users, accuracy figures or partner organisations. The only numbers we may show are those our evaluation script measures on the published test set, with the data to reproduce them. Anything else in the demo is labelled as an example.

## Product Principles

1. No source, no finding: every claim the system presents as established leads to a verbatim fragment of a named source.
2. Abstaining is an answer: when evidence is missing or conflicting, say so plainly and say what is missing.
3. Model interpretation is labelled as such and kept apart from source material.
4. Strength comes from premises the reader can see: number of independent sources, official or primary sources, recency, agreement.
5. Never judge by who said it: domain, author, channel, popularity or source status alone never decide a verdict.
6. Failure is not a verdict: outages, missing keys and limits are reported as technical problems.
7. Support, not a judge of truth: the answer invites the reader to open the evidence; people handle what the system cannot settle.

## Accessibility & Inclusion

WCAG 2.2 AA contrast in both themes, including on top of third-party light and dark feeds. Verdicts never rely on colour alone. Respect prefers-reduced-motion. Plain Polish for people without technical knowledge; Polish copy runs longer than English, components must survive long labels. The web form works on a phone without installing anything.
