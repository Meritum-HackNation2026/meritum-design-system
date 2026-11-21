# Product

<!-- impeccable:product-schema 1 -->

## Platform

web

## Stack

- **Cloud:** during development the demo runs on the team's own server. The target is GCP in the EU: the app in `europe-central2` (Warsaw), Cloudflare in front of it, models through Vertex AI in an EU region where the chosen model is available. We migrate through CI/CD (CI already runs on GCP runners), possibly during the hackathon. `docker compose up` runs everything locally.
- **Models:** from GCP Vertex AI; any model available there, not necessarily Claude, chosen by configuration. Deterministic settings: temperature 0 and a pinned model version.
- **Code:** all repositories and the system go public at the end of development; the public repository has run instructions with one `docker compose up`. Contracts live in the meritum-core repository as the single source of truth; the design system consumes the generated JSON Schema and TypeScript types.
- **API:** Python, FastAPI, FastMCP, Pydantic, Pydantic AI, DBOS (durable workflows). Ruff and Ty in strict mode.
- **Architecture:** vertical slices by core domain with hexagonal architecture inside each; every domain repeats the same subfolders (`models/`, `dtos/`, `ports/`, `adapters/`, …). Channels (web form, extension, Discord, SMS, MCP) are inbound adapters; the LLM, the web search and the corpus store are outbound adapters behind ports, so a model or provider can be swapped without rebuilding the system. TDD. Architecture tests with pytestarch, behaviour specs with behave.
- **Database:** PostgreSQL with pgvector, Polish full-text search (ispell dictionary in our own container image, since managed Cloud SQL cannot load one) and pg_trgm; hybrid retrieval over the corpus.
- **Web search:** a `WebSearch` port; first adapter Firecrawl (search and content extraction), restricted to catalogue domains. Pages found live wait in quarantine until an injection scan finishes, then join the next corpus snapshot. Scheduled RSS and sitemap ingestion runs as DBOS workflows without any third-party search.
- **Rate limiting:** the slowapi middleware (per IP address, region and channel) and Cloudflare in front of the API against DDoS.
- **Frontend:** React, shadcn/ui with shadcnblocks, TanStack Router, TanStack Query, Tailwind CSS v4, Biome in strict mode.
- **Extension:** Chrome MV3; a „Sprawdź” button under posts and a paste box in the popup, both calling the same API as the web form. It runs on the demo mocks (design-system/demo/platforms/) and on the real sites; injected UI renders in Shadow DOM.

## Users

- **Citizens** who meet a rumour, a post or a forwarded message and want to know quickly whether it holds up. Many have low digital skills: they should not need to learn verification methods or install anything. Their job: paste the text or link, read a short answer in plain Polish, open the sources if they want.
- **Social media readers** who already use the extension and want to check a post where they see it, with one click.
- **People who prefer SMS or Discord**, who send the text to a number or a bot and get a short answer with a link to the full result (SMS if time allows).
- **Moderators and analysts** named by the administrator. Their job: take over questions the system could not settle (missing evidence, high risk, repeated questions), see similar questions grouped into one case, and track quality: abstentions, injection attempts, response time, cost.
- **Jury** of the MSZ „Prawdowid” challenge, who run the reference set themselves, without the team's help.

## Product Purpose

A tool that lets a citizen check a claim as easily as sending a message, grounded in an audited set of credible sources. The system extracts the claims worth checking, searches official documents, public data and fact-checkers' corpora (plus fresh publications from catalogue domains), and gives each claim one of five verdicts: confirmed, false, misleading, insufficient evidence, not verifiable. Every finding cites the source (title, publisher, date, link, verbatim fragment); the strength of the answer follows from explicit premises; when evidence is missing the system says so and explains what it could not establish. Technical failure, a request for clarification and out-of-scope input are never shown as verdicts. Instructions found in checked content never change how the system behaves.

Success: a citizen gets an honest, sourced answer within 30 seconds at most (our target; the brief asks for a median of 30 s or less), through the channel they already use; the jury gets the same result through the web and the extension; nobody is shown a model's guess dressed up as a fact.

The product is entered in one hackathon challenge: **MSZ „Prawdowid”** (fast, easy verification based on credible sources). The full brief is in `../konkursy/`.

## Positioning

Honest by construction: the language model reads, searches and writes, but a verdict needs a verbatim citation, its strength is computed from premises by a fixed rule, and abstaining is a first-class answer. Meets people where they read (a web page anyone can open, and a button under the post they are looking at). Auditable: open source catalogue with reasons for inclusion and exclusion, a record of every check, public code at the end of development, and data processed in GCP in the EU.

## Operating Context

- Primary channel: a responsive web form. Conversation history stays in the browser's sessionStorage. Signing in with a Google or Microsoft account is optional; signed-in users keep their history on the server and can delete it. Second channel: the Chrome extension (button under posts plus the popup paste box). Both use the same verification core and must give the same result for the same input and corpus version. We confirm with the MSZ mentors that the extension counts as an equivalent channel. A Discord bot on the same API is built from the start, so the two-channel requirement holds either way. If time allows, an SMS demo adapter: an SMS gateway webhook on the same API, operator fees stated plainly, answers cut to 70 characters (Polish text forces UCS-2) with a link to the full result. Consistency: the corpus is versioned as scheduled snapshots (for example hourly) and results are cached by (normalised input, snapshot id), so the same input within one snapshot gives the same result in every channel.
- The extension injects UI into third-party feeds in light and dark themes. Per-platform skins (X, Facebook, Instagram, Reddit, TikTok) adapt font, radius, surface, borders and links; the Meritum mark, the verdict word and colour, and the sources block never change. It sends content only after the user clicks.
- Demo for the jury: the same question asked in the web form and on an X mock through the extension, a sourced verdict, an honest abstention with a moderator case, an ignored prompt-injection attempt, and the evaluation results on our own test set (the jury's reference set from MSZ is hidden). Film under 3 minutes, deck under 12 slides.
- The jury runs it from our instructions, end to end, with no manual help. Nothing in the answer may depend on hard-coded examples.

## Capabilities and Constraints

- Input: text or URL (MVP), screenshot with OCR (bonus). Input validation, length limit, rate limit, automatic masking of obvious personal data.
- Claim extraction: one or more claims per input, facts separated from opinions.
- Retrieval: corpus built from the organiser's source list (official gov.pl and agency sites), scraped, chunked and vectorised: at least 100 documents from at least 10 domains and two source types: official or primary sources, and fact-checkers through the Google Fact Check Tools API (ClaimReview) and Fact Check Explorer. Each document has publication and retrieval timestamps. Live web search runs only on catalogue domains; fetched pages join the next snapshot after an injection scan. The organisers consented to processing the listed sources; in production every consent gets confirmed legally with each provider. The EUvsDisinfo database is an optional premium match, shown as context only.
- Verdict per claim with citations, premises and strength. Independent sources are counted per publisher from the catalogue, and agreement follows from citation stances. Conflicting credible sources give „insufficient evidence” with both sides cited side by side, a plain note on what differs and no strength. Archival warning: evidence age is measured against the date the claim refers to (365 days by default, hours or days for short-lived sources set per catalogue entry); legal acts in force, official pages updated in place and evidence about a past event never count as archival; neutral source-status warning (for example an EU-sanctioned entity) that never decides the verdict; match to known incidents as context only.
- Abstention without a fake answer, with what is missing; moderator case for unresolved, high-risk and repeated questions, with deduplication; the UI distinguishes „recommended for hand-off” from „handed off”.
- Prompt-injection resistance: user input, a user-supplied URL and source text are marked as data in every step; a screening layer (an LLM proxy or Google Cloud Model Armor) sits in front of every model call; catalogue pages are scanned at ingestion and live-search pages stay in quarantine until scanned; detected attempts are logged.
- Failures: when web search fails, times out or hits a limit, or the model fails after retries, the user gets a technical-failure message, never an answer.
- Speed: several research agents run in parallel and the main agent streams draft answers with research progress; a draft shows no verdict until citations pass verification. Timing is benchmarked with pydantic-evals.
- Cost and scale: cost per check from token usage and search calls in the check record, cost of 1 000 queries and of keeping each channel, result-cache hit rate, a DBOS queue with a concurrency limit, HTTP 429 with a clear message under heavy traffic, autoscaling on GCP. Numbers come from measurement during implementation.
- Check record: question (masked), time, channel, sources, verdicts, models used, processing region, cost, latency, retrieval errors, injection events; defined retention and a „delete my checks” action for the session; signed-in users also have a user id and can delete their history and account. IP address handling and log retention are set in the privacy policy; channels other than the browser have their own privacy policies (aggregate usage telemetry only, no names or e-mails, IP and region only against attacks).
- Evaluation script on our own test set, built from the same materials as the knowledge base and covering the brief's scenarios A–J (thresholds are tuned only on this set; the jury's reference set from MSZ is hidden), reporting macro-F1, citation coverage and correctness, abstention, injection resistance, median latency and cost per 100 checks.
- Exports: JSON and CSV of check records and cases; technique codes mapped to DISARM where an equivalent exists.
- UI language: Polish, plain words. Working name: **Meritum**, subtitle „obywatelski radar dezinformacji”.

## Brand Commitments

- Working name: **Meritum** — „obywatelski radar dezinformacji”. Logo: mark B „Dwa łuki” (brand/meritum-mark.svg), chosen 2026-11-21. Lockups with the subtitle in brand/exports/ already carry „obywatelski radar dezinformacji”.
- Visual direction (chosen 2026-11-21): „Biuletyn synoptyczny” palette on clean white bordered surfaces; spec in DESIGN_SYSTEM.md.
- Binding visual constraints: "Civic-Tech Intelligence / Modern Editorial" (precision of developer tools such as Linear and Vercel with the gravity and legibility of investigative journalism such as The Economist and Bellingcat). Never: hacker green-on-black, purple-blue AI gradients, heavy governmental/official styling, gratuitous animation. Light and dark modes required.

## Evidence on Hand

None yet. No real users, accuracy figures or partner organisations. The only numbers we may show are those our evaluation script measures on our own test set, with the data to reproduce them. Anything else in the demo is labelled as an example.

## Product Principles

1. No source, no finding: every claim the system presents as established leads to a verbatim fragment of a named source.
2. Abstaining is an answer: when evidence is missing or conflicting, say so plainly and say what is missing.
3. Model interpretation is labelled as such and kept apart from source material.
4. Strength comes from premises the reader can see: number of independent sources, official or primary sources, recency, agreement.
5. Never judge by who said it: domain, author, channel, popularity or source status alone never decide a verdict.
6. Failure is not a verdict: outages, missing keys, limits and failed web searches or model calls are reported as technical problems.
7. Support, not a judge of truth: the answer invites the reader to open the evidence; people handle what the system cannot settle.

## Accessibility & Inclusion

WCAG 2.2 AA contrast in both themes, including on top of third-party light and dark feeds. Verdicts never rely on colour alone. Respect prefers-reduced-motion. Plain Polish for people without technical knowledge; Polish copy runs longer than English, components must survive long labels. The web form works on a phone without installing anything.
