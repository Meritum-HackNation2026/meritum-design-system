# Product

<!-- impeccable:product-schema 1 -->

## Platform

web

## Stack

- **Cloud:** during development the demo runs on the team's own server (meritum.gburek.app). The target is the app in GCP `europe-central2` (Warsaw) with models through Vertex AI in an EU region where the chosen model is available. Cloudflare sits in front of it and is outside the EU, as are Firecrawl, Discord and the optional Google and Microsoft sign-in; the data processors register below says what each one receives. We migrate through CI/CD (CI already runs on GCP runners), possibly during the hackathon. `docker compose up` runs everything locally.
- **Models:** from GCP Vertex AI; any model available there, not necessarily Claude, chosen by configuration. Deterministic settings: temperature 0 and a pinned model version.
- **Code:** all repositories and the system go public at the end of development; the public repository has run instructions with one `docker compose up`. Contracts live in the meritum-core repository as the single source of truth; the design system consumes the generated JSON Schema and TypeScript types.
- **API:** Python, FastAPI, FastMCP, Pydantic, Pydantic AI, DBOS (durable workflows). Ruff and Ty in strict mode.
- **Architecture:** vertical slices by core domain with hexagonal architecture inside each; every domain repeats the same subfolders (`models/`, `dtos/`, `ports/`, `adapters/`, …). Channels (web form, extension, Discord, SMS, MCP) are inbound adapters; the LLM, the web search and the corpus store are outbound adapters behind ports, so a model or provider can be swapped without rebuilding the system. TDD. Architecture tests with pytestarch, behaviour specs with behave.
- **Database:** PostgreSQL with pgvector, Polish full-text search (ispell dictionary in our own container image, since managed Cloud SQL cannot load one) and pg_trgm; hybrid retrieval over the corpus.
- **Web search:** a `WebSearch` port; first adapter Firecrawl (search and content extraction), restricted to catalogue domains. It runs on every check in parallel with corpus retrieval; the search threshold only decides whether we wait for its result. Pages found live wait in quarantine until an injection scan finishes; after the scan they are evidence in the check that fetched them and are recorded in its check record, and they join the shared corpus with the next snapshot. Scheduled RSS and sitemap ingestion runs as DBOS workflows without any third-party search.
- **Rate limiting:** the slowapi middleware (per IP address, region and channel) and Cloudflare in front of the API against DDoS. slowapi counts in memory per process, so with several instances we recommend a shared counter in PostgreSQL or Redis.
- **Frontend:** React, shadcn/ui, TanStack Router, TanStack Query, Tailwind CSS v4, Biome in strict mode. From shadcnblocks only free blocks, or none: paid blocks may not go into public repositories.
- **Extension:** Chrome MV3; a „Sprawdź” button under posts and a paste box in the popup, both calling the same API as the web form. It runs on the demo mocks (design-system/demo/platforms/) and on the real sites; injected UI renders in Shadow DOM. Optional for the jury.
- **Discord:** a bot on the same API that answers in server channels and in direct messages, with an invite link to add it to any server. A Discord mock page in the meritum-mocks repository calls the same API, so the jury can test the channel without joining a server.

## Users

- **Citizens** who meet a rumour, a post or a forwarded message and want to know quickly whether it holds up. Many have low digital skills: they should not need to learn verification methods or install anything. Their job: paste the text or link, read a short answer in plain Polish, open the sources if they want.
- **Social media readers** who already use the extension and want to check a post where they see it, with one click.
- **People who prefer Discord or SMS**, who send the text to a bot (in a server channel or a direct message) or to a number and get a short answer with a link to the full result (SMS if time allows).
- **Moderators and analysts** named by the administrator, who signs them in to the moderator panel with a role (moderator, analyst, admin) and keeps the list of high-risk topics. Their job: take over unanswered claims (a claim whose verdict is „insufficient evidence”) that are high-risk or repeated, see similar claims grouped into one case, and track quality: abstentions, injection attempts, response time, cost.
- **Jury** of the MSZ „Prawdowid” challenge, who run the reference set themselves, without the team's help, through the web form and the Discord mock; the extension is optional.

## Product Purpose

A tool that lets a citizen check a claim as easily as sending a message, grounded in an audited set of credible sources. The system extracts the claims worth checking, searches official documents, public data and fact-checkers' corpora (plus fresh publications from catalogue domains), and gives each claim one of five verdicts: confirmed, false, misleading, insufficient evidence, not verifiable. Every finding cites the source (title, publisher, date, link, verbatim fragment); the strength of the answer follows from explicit premises; when evidence is missing the system says so and explains what it could not establish. Technical failure, a request for clarification and out-of-scope input are never shown as verdicts. Instructions found in checked content never change how the system behaves.

Success: a citizen gets an honest, sourced answer through the channel they already use, and we optimise towards 30 seconds at most per check (the brief asks for a median of 30 s or less; nothing special happens after 30 s); the jury gets the same substantive result through the web form and Discord; nobody is shown a model's guess dressed up as a fact.

The product is entered in one hackathon challenge: **MSZ „Prawdowid”** (fast, easy verification based on credible sources). The full brief is in `../konkursy/`.

## Positioning

Honest by construction: the language model reads, searches and writes, but a verdict needs a verbatim citation, its strength is computed from premises by a fixed rule, and abstaining is a first-class answer. Meets people where they already are (a web page anyone can open, a Discord bot, and a button under the post they are looking at). Auditable: open source catalogue with reasons for inclusion and exclusion, a record of every check, public code at the end of development, and a register of data processors that says what is processed in the EU and what is not.

## Operating Context

- Primary channel: a responsive web form. Conversation history stays in the browser's sessionStorage. Signing in with a Google or Microsoft account is optional; signed-in users keep their history on the server and can delete it. Second channel: the Discord bot on the same API, built from the start; together with the web form it meets the two-channel requirement whatever the mentors decide about the extension. The Chrome extension (button under posts plus the popup paste box) is an extra channel on the same core. If time allows, an SMS demo adapter: an SMS gateway webhook on the same API, operator fees stated plainly. Polish text forces UCS-2 (70 characters), so the SMS answer carries the main claim's verdict and a link to the full result; transliteration to GSM-7 (160 characters) is an option. Consistency: results are cached by normalised input for a fixed time (for example 2 hours) regardless of new corpus snapshots, so the same input gives the same substantive result in every channel while the entry lives. The cache keeps only the substantive part (claims, limitations, corpus version, cited source ids); escalation and the repeat counter are computed on every request, and technical failures are never cached.
- The extension injects UI into third-party feeds in light and dark themes. Per-platform skins (X, Facebook, Instagram, Reddit, TikTok) adapt font, radius, surface, borders and links; the Meritum mark, the verdict word and colour, and the sources block never change. It sends content only after the user clicks.
- Demo for the jury: the same question asked in the web form and on the Discord mock (or the real bot via its invite link), a sourced verdict, an honest abstention with a moderator case, an ignored prompt-injection attempt, and the evaluation results on our own published test set (the brief's „open set”; the jury's reference set from MSZ is hidden). The extension on an X mock is an optional extra; nobody has to enable developer mode. Film under 3 minutes, deck under 12 slides.
- The jury runs it from our instructions, end to end, with no manual help. Nothing in the answer may depend on hard-coded examples.

## Capabilities and Constraints

- Input: text or an http(s) URL (MVP), screenshot with OCR (bonus). Until OCR exists, an image sent through the form or Discord gets the out-of-scope status with a message, and README lists it among unsupported cases. Input validation, length limit, rate limit, automatic masking of obvious personal data.
- Claim extraction: one or more claims per input, facts separated from opinions.
- Retrieval: corpus built from the source catalogue, scraped, chunked and vectorised: at least 100 documents from at least 10 domains and two source types. Primary sources: the organiser's list (official gov.pl and agency sites, including gov.pl/web/dyplomacja) plus ISAP and EUR-Lex for legal acts, dane.gov.pl for public data and the BIP pages of catalogue institutions, which §7 of the brief recommends; each entry states why it qualifies. Secondary sources: fact-checkers through the Google Fact Check Tools API (ClaimReview) only; Fact Check Explorer is a web UI, not an API, so it is not in the catalogue, and API data stays out of snapshots and the result cache beyond what its cache headers allow. Each document has publication and retrieval timestamps and each catalogue entry a publisher id. Live web search runs only on catalogue domains, on every check. The organisers consented to processing the listed sources; we have no written source for that yet, and it does not cover third-party rights, so in production every consent gets confirmed legally with each provider. The EUvsDisinfo database is an optional premium match, shown as context only.
- Verdict per claim with citations, premises and strength. Only settling verdicts (confirmed, false, misleading) have a strength, and it counts only publishers (by catalogue publisher id) whose citations agree with the verdict: strong needs 2 or more agreeing independent publishers, at least one of them primary, and fresh evidence; moderate needs 2 agreeing publishers or 1 primary; one non-primary publisher or archival evidence gives weak. Agreement follows from citation stances. Conflicting credible sources give „insufficient evidence” with both sides cited side by side, a plain note on what differs and no strength. Each claim has a date it refers to and where that date came from (the text, the input's publication date, or today); evidence age is measured against it (365 days by default, hours or days for short-lived sources set per catalogue entry), and the card shows both dates. Legal acts in force, official pages updated in place and evidence about a past event never count as archival; validity is set per citation. Old evidence (archival) is distinct from old content resurfacing as new (scenario B), which is „misleading” with an outdated or out-of-context technique. A neutral source-status warning only for entities on the official EU sanctions list; a match to known incidents as context only, and a domain from the incident database triggers a warning only when the checked link is on that domain and the incident's topic matches the claim. Neither ever changes the verdict.
- Abstention without a fake answer, with what is missing. A moderator case opens automatically for an unanswered claim on a high-risk topic (the model classifies the claim against the admin's topic list, with a keyword list as fallback) or for a similar unanswered claim asked again; repeats are counted per session or user, not per channel. Similarity is measured per claim, a case holds its claims and their checks, and it can have several reasons at once. The UI distinguishes „recommended for hand-off” from „handed off”, and joining an existing case never reveals that someone else asked.
- Prompt-injection resistance: user input, a user-supplied URL and source text are marked as data in every step; a screening layer (an LLM proxy or Google Cloud Model Armor) sits in front of every model call; catalogue pages are scanned at ingestion and live-search pages stay in quarantine until scanned. An instruction in user content is cut out and the rest is analysed as data; a source containing one drops out of the evidence; every attempt is logged. An attempt counts as repelled when the verdict matches the label of the same case without the instruction, the event is logged and no instruction was executed.
- Failures: when a web search we wait for fails, times out or hits a limit, or the model fails after retries, the user gets a technical-failure message, never an answer.
- Speed: several research agents (corpus, live search, fact-checkers) run in parallel and the main agent streams draft answers with research progress; a draft shows no verdict until citations pass verification. Latency comes from the check record (received to answered, through the channel); in the evaluation harness a failed case returns a status instead of raising, so it stays in the median.
- Cost and scale: cost per check from token usage and search calls in the check record, cost of 1 000 queries and of keeping each channel, result-cache hit rate, a DBOS queue with a concurrency limit, HTTP 429 with a clear message under heavy traffic, autoscaling on GCP. DBOS has no „full queue”, so the 429 comes from our own counter of waiting checks. Numbers come from measurement during implementation. Accepted risks: per-citation stance calls multiply model and screening calls, and slowapi counts per process; recommended but not committed: caching scan results by fragment hash, one stance call per claim with isolated pairs, a shared counter in PostgreSQL or Redis.
- Check record: question (masked), time, channel, sources (including live-search pages), verdicts, models used, processing region, cost, latency, cache hit, retrieval errors, injection events; defined retention and a „delete my checks” action for the session; signed-in users also have a user id and can delete their history and account. Masking also covers DBOS step outputs (fetched pages, model outputs), and retention and deletion cover the DBOS system tables. IP address handling and log retention are set in the privacy policy. Channels other than the browser have their own privacy policies: Discord gives a username and user id and SMS a phone number, which we process only to reply and count repeats, store as a salted hash with the same 30-day retention and never show to moderators; „/usun-moje-dane” on Discord and the SMS keyword „USUN” delete the records for that identifier. Usage telemetry is aggregate only, and IP and region are used only against attacks.
- Evaluation script on our own test set, built from the same materials as the knowledge base and covering the brief's scenarios A–J. We publish it, so it is the brief's „open set”; thresholds are tuned only on it, and the jury's reference set from MSZ is hidden. A case's verdict is the verdict of the main claim named in the case file (with several labelled claims, the worst result by a fixed order); non-verdict statuses are their own error class in macro-F1. The script reports macro-F1, citation coverage and correctness, abstention, injection resistance, median latency and cost per 100 checks.
- Exports: JSON and CSV of check records and cases; technique codes mapped to DISARM where an equivalent exists.
- UI language: Polish, plain words. Working name: **Meritum**, subtitle „obywatelski radar dezinformacji”.

## Data Processors

What is processed in the EU and what is not. The same register is in ADR-14 of the product document, in README and in the channel privacy policies.

| Processor | Country or region | Data | Why |
|---|---|---|---|
| Team's own server (on-prem) | country to be filled in | everything the demo processes today: API, worker, PostgreSQL with check records, cases and corpus | current demo (meritum.gburek.app) until the GCP migration |
| Cloudflare | USA | whole requests and responses, including question text and IP addresses, since the tunnel terminates TLS | tunnel to the team's server, TLS, DDoS protection and rate limits |
| GCP `europe-central2` (target) | EU (Warsaw) | API, worker, PostgreSQL with check records, cases and corpus | target demo |
| Vertex AI | GCP, the EU region where the chosen model is available | masked question, source fragments, model outputs | claim extraction, stance, answer |
| Model Armor (if chosen over an LLM proxy) | GCP, region to verify | the content of every model call before it is sent | screening against prompt injection |
| Firecrawl | USA | search queries built from claims, URLs and content of fetched pages | live web search on catalogue domains; its terms grant Firecrawl a licence to user content (§ 8.d per the review, to verify) |
| Google Fact Check Tools API | Google, region to verify | queries with claims | fact-checkers' findings (ClaimReview) |
| Discord | USA | username and user id, message to the bot and the answer | Discord channel |
| SMS gateway | to be chosen | phone number, SMS text and the answer | SMS channel, if time allows |
| Google and Microsoft sign-in | USA | account id | optional sign-in, if time allows |

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
