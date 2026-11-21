# Copy of meritum-core src/meritum_core/checks/contracts.py at d790abc66171d3774b2cef5fcdbae659a57a3035.
# Do not edit: change it in meritum-core and run contracts/sync.sh.
"""Meritum contracts: the data every Meritum surface renders (MSZ "Prawdowid").

This module is the single source of truth. `scripts/export_contracts.py` writes `contracts/meritum.schema.json`
and `contracts/meritum.ts`; the design system and the TypeScript apps consume those generated files.
User-facing strings live in `copy/pl.json`; this file carries codes, not copy.

Rules from the MSZ brief that the models enforce:
- a verdict that settles a claim (confirmed, false, misleading) needs at least one citation and explicit premises;
  only such a verdict has a strength;
- the strength of a verdict follows from the premises by a fixed rule, never from the model's say-so;
- agreement follows from the citation stances; conflicting credible sources give "insufficient_evidence" with both sides cited and no strength;
- independence is counted per catalogue publisher (publisher_id), not per page or domain, and only among citations whose
  stance agrees with the verdict;
- evidence age is measured against the date the claim refers to (claim_date), with a per-catalogue-entry threshold; evidence
  that does not expire (a legal act in force, an official page updated in place, evidence about a past event) is never archival;
- insufficient evidence says what could not be established;
- technical failure, a request for clarification and out-of-scope input are not verdicts and carry no claims;
- recommending a hand-off to a moderator is distinct from creating a case;
- the result cache keeps only the substantive part of a result and never a technical failure; escalation is computed per request.
"""

from __future__ import annotations

from datetime import date, datetime
from typing import Annotated, Literal

from pydantic import BaseModel, ConfigDict, Field, HttpUrl, model_validator

Channel = Literal["web", "extension", "discord", "sms", "mcp"]

# Version of these contracts (CheckRequest, CheckResult, ...); independent of the
# job contract version in meritum_core.jobs.contracts. Raise it on any change that
# breaks a consumer, and regenerate (scripts/generate-contracts.sh).
CONTRACT_VERSION = 2

MIN_TEXT_CHARS = 3
STRONG_MIN_SOURCES = 2

Verdict = Literal[
    "confirmed", "false", "misleading", "insufficient_evidence", "not_verifiable"
]
SETTLING: frozenset[Verdict] = frozenset({"confirmed", "false", "misleading"})

# Outcomes that are not verdicts and must be shown separately (MSZ section 2 and 5).
CheckStatus = Literal[
    "done", "needs_clarification", "out_of_scope", "technical_failure"
]

SourceKind = Literal[
    "akt_prawny", "dane_publiczne", "instytucja", "fact_check", "media"
]
SourceTier = Literal[
    "primary", "secondary"
]  # primary: official documents and public data; secondary: fact-checkers (media only if the catalogue admits them)
SourceVia = Literal[
    "corpus", "rss", "web_search"
]  # how the document reached the corpus
Stance = Literal["supports", "refutes", "context"]
# The stance that agrees with each settling verdict; only those citations count towards strength.
AGREEING_STANCE: dict[Verdict, Stance] = {
    "confirmed": "supports",
    "false": "refutes",
    "misleading": "context",
}
Agreement = Literal["consistent", "conflicting"]
# Overrides of the age rule. expires: age counts; in_force: e.g. a legal act in force; updated_in_place: standing official
# guidance edited in place (passenger rights, contact pages); past_event: evidence explicitly about a past event.
Validity = Literal["expires", "in_force", "updated_in_place", "past_event"]
DEFAULT_MAX_AGE_HOURS = 365 * 24
Strength = Literal["strong", "moderate", "weak"]
# Where the claim date comes from: a date in the checked text, the publication date of the input (e.g. the post), or today.
ClaimDateSource = Literal["text", "input_published_at", "today"]
PublisherId = Annotated[str, Field(pattern=r"^[a-z0-9][a-z0-9-]{1,79}$")]

TechniqueCode = Literal[
    "false_authority",
    "conspiracy_theory",
    "out_of_context",
    "outdated",
    "fabricated_quote",
    "manipulated_media",
    "impersonation",
    "cherry_picking",
]


class _Model(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)


# ---------------------------------------------------------------- input


class CheckRequest(_Model):
    """What a channel adapter sends to the verification core. The core is channel-agnostic."""

    channel: Channel
    text: Annotated[str | None, Field(max_length=4000)] = None
    url: HttpUrl | None = None
    page_url: Annotated[
        HttpUrl | None,
        Field(description="Extension only: the post the text came from."),
    ] = None

    @model_validator(mode="after")
    def _text_or_url(self) -> CheckRequest:
        if self.url is None and (
            self.text is None or len(self.text.strip()) < MIN_TEXT_CHARS
        ):
            raise ValueError("send text (3+ characters) or a URL")
        return self


# ---------------------------------------------------------------- sources


class Source(_Model):
    """A document from the audited corpus. Title, publisher, date and link are mandatory to show (MSZ section 2)."""

    id: Annotated[str, Field(min_length=1, max_length=80)]
    title: Annotated[str, Field(min_length=3, max_length=200)]
    publisher: Annotated[str, Field(min_length=2, max_length=120)]
    publisher_id: Annotated[
        PublisherId,
        Field(
            description="Publisher id from the catalogue; independence is counted on it."
        ),
    ]
    url: HttpUrl
    domain: Annotated[str, Field(min_length=3, max_length=100)]
    kind: SourceKind
    tier: SourceTier
    published_at: datetime | None = None
    fetched_at: datetime
    language: Annotated[str, Field(pattern=r"^[a-z]{2}$")] = "pl"
    via: SourceVia = "corpus"


class Citation(_Model):
    """A fragment of a source and how it bears on the claim. The pipeline drops fragments it cannot find verbatim."""

    source: Source
    fragment: Annotated[str, Field(min_length=10, max_length=600)]
    stance: Stance
    validity: Annotated[
        Validity,
        Field(
            description="Age rule for this piece of evidence: the catalogue entry's validity, or past_event set per evidence."
        ),
    ] = "expires"
    fragment_found_verbatim: Literal[True] = True


class CatalogEntry(_Model):
    """One domain in the open source catalogue: why it qualifies, how it is refreshed, whether it is excluded."""

    domain: Annotated[str, Field(min_length=3, max_length=100)]
    publisher: Annotated[str, Field(min_length=2, max_length=120)]
    publisher_id: PublisherId
    kind: SourceKind
    tier: SourceTier
    license: Annotated[str, Field(min_length=2, max_length=120)]
    ingest: Literal["static", "rss", "sitemap", "web_search"]
    refresh_hours: Annotated[int | None, Field(ge=1)] = None
    validity: Annotated[
        Validity,
        Field(
            description="Age override for every document of this entry; past_event is set per evidence."
        ),
    ] = "expires"
    max_age_hours: Annotated[
        int | None,
        Field(
            ge=1,
            description="Shorter threshold for short-lived sources (warnings, roads, weather: hours or days).",
        ),
    ] = None
    qualified_because: Annotated[str, Field(min_length=10, max_length=300)]
    excluded: bool = False
    exclusion_reason: Annotated[str | None, Field(max_length=300)] = None

    @model_validator(mode="after")
    def _exclusion_has_reason(self) -> CatalogEntry:
        if self.excluded and (
            self.exclusion_reason is None or not self.exclusion_reason
        ):
            raise ValueError("an excluded source needs a reason")
        if self.validity == "past_event":
            raise ValueError(
                "'past_event' describes one piece of evidence, not a whole catalogue entry"
            )
        if self.validity != "expires" and self.max_age_hours is not None:
            raise ValueError("a source that does not expire has no maximum age")
        return self


# ---------------------------------------------------------------- verdict


class Premises(_Model):
    """Explicit premises behind a verdict (MSZ: strength must follow from quality, recency, agreement, independence)."""

    independent_sources: Annotated[
        int,
        Field(
            ge=0,
            description="Distinct publishers (publisher_id) among the citations whose stance agrees with the verdict.",
        ),
    ]
    primary_sources: Annotated[
        int,
        Field(
            ge=0,
            description="Distinct primary-tier publishers among the agreeing citations.",
        ),
    ]
    newest_source_published_at: Annotated[
        datetime | None,
        Field(
            description="Publication date of the newest agreeing source, shown as a date."
        ),
    ] = None
    newest_source_age_hours: Annotated[
        int | None,
        Field(
            ge=0,
            description="Hours from the newest agreeing source to the claim date (ClaimResult.claim_date), not to now; 0 when the source is newer.",
        ),
    ] = None
    max_age_hours: Annotated[
        int,
        Field(
            ge=1, description="Threshold from the catalogue entry of the newest source."
        ),
    ] = DEFAULT_MAX_AGE_HOURS
    validity: Validity = "expires"
    agreement: Agreement


def is_stale(p: Premises) -> bool:
    """Whether expiring evidence is older than its catalogue threshold.

    Returns:
        True when the newest source is past `max_age_hours`.
    """
    return (
        p.validity == "expires"
        and p.newest_source_age_hours is not None
        and p.newest_source_age_hours > p.max_age_hours
    )


def strength_for(p: Premises) -> Strength:
    """The one rule that turns premises into strength. Shown to the user next to the premises.

    Counts cover only publishers whose citations agree with the verdict. Strong: 2+ agreeing
    independent publishers, 1+ of them primary, fresh evidence. Moderate: 2+ agreeing publishers
    or 1 primary, fresh evidence. Weak: one non-primary publisher, or archival evidence.

    Returns:
        "strong", "moderate" or "weak".
    """
    if p.agreement != "consistent" or is_stale(p):
        return "weak"
    if p.independent_sources >= STRONG_MIN_SOURCES and p.primary_sources >= 1:
        return "strong"
    if p.independent_sources >= STRONG_MIN_SOURCES or p.primary_sources >= 1:
        return "moderate"
    return "weak"


class EvidenceStrength(_Model):
    """Strength level together with the premises it follows from."""

    level: Strength
    premises: Premises

    @model_validator(mode="after")
    def _level_follows_premises(self) -> EvidenceStrength:
        if self.level != strength_for(self.premises):
            raise ValueError(
                f"strength must be {strength_for(self.premises)!r} for these premises"
            )
        return self


class IncidentMatch(_Model):
    """Similarity to a known incident. Context only: never a basis for the verdict by itself, and never changes it.

    `domain` is the one explicitly defined warning case: the checked URL is on a domain the incident database lists,
    and the incident's topic matches the claim.
    """

    incident_id: Annotated[str, Field(min_length=1, max_length=80)]
    matched_on: Literal["content", "domain"] = "content"
    title: Annotated[str, Field(max_length=200)]
    date: datetime
    url: HttpUrl
    similarity: Annotated[float, Field(ge=0, le=1)]


class SourceStatusWarning(_Model):
    """Neutral note that the checked content comes from an entity on the official EU sanctions list. Never a verdict."""

    code: Literal["eu_sanctioned_entity"]
    entity: Annotated[str, Field(max_length=120)]
    basis_url: HttpUrl


class ClaimResult(_Model):
    """One checked claim. Citations (source material) are kept apart from `explanation` (model interpretation)."""

    claim: Annotated[str, Field(min_length=5, max_length=500)]
    claim_date: Annotated[
        date | None,
        Field(
            description="The date the claim refers to; evidence age is measured against it."
        ),
    ] = None
    claim_date_source: ClaimDateSource | None = None
    verdict: Verdict
    strength: EvidenceStrength | None = None
    citations: list[Citation] = []
    explanation: Annotated[str, Field(min_length=10, max_length=800)]
    unresolved: Annotated[
        str | None, Field(max_length=500, description="What could not be established.")
    ] = None
    archival: Annotated[
        bool,
        Field(description="Newest evidence is older than the claim's context needs."),
    ] = False
    technique: TechniqueCode | None = None
    incident: IncidentMatch | None = None

    @model_validator(mode="after")
    def _verdict_rules(self) -> ClaimResult:
        stances = {c.stance for c in self.citations}
        conflicting = {"supports", "refutes"} <= stances
        if conflicting and (
            self.verdict != "insufficient_evidence" or self.strength is not None
        ):
            raise ValueError(
                "conflicting sources give 'insufficient_evidence' with both sides cited and no strength"
            )
        if (
            self.verdict == "insufficient_evidence"
            and self.citations
            and not conflicting
        ):
            raise ValueError(
                "'insufficient_evidence' carries citations only when credible sources conflict"
            )
        if (self.claim_date is None) != (self.claim_date_source is None):
            raise ValueError("a claim date comes with where it was taken from")
        if self.strength is not None and self.verdict not in SETTLING:
            raise ValueError(
                "only a settling verdict (confirmed, false, misleading) has a strength"
            )
        if self.verdict in SETTLING:
            if not self.citations or self.strength is None:
                raise ValueError(
                    f"verdict {self.verdict!r} needs citations and premises"
                )
            if self.verdict == "confirmed" and "supports" not in stances:
                raise ValueError("'confirmed' needs a supporting citation")
            if self.verdict == "false" and "refutes" not in stances:
                raise ValueError("'false' needs a refuting citation")
            if self.verdict == "misleading" and (
                "context" not in stances or self.technique is None
            ):
                raise ValueError(
                    "'misleading' needs a context citation and the technique it uses"
                )
        if self.strength is not None and self.verdict in SETTLING:
            p = self.strength.premises
            agreeing = [
                c for c in self.citations if c.stance == AGREEING_STANCE[self.verdict]
            ]
            publishers = {c.source.publisher_id for c in agreeing}
            primary = {
                c.source.publisher_id for c in agreeing if c.source.tier == "primary"
            }
            if p.agreement != ("conflicting" if conflicting else "consistent"):
                raise ValueError("agreement must follow from the citation stances")
            if (p.independent_sources, p.primary_sources) != (
                len(publishers),
                len(primary),
            ):
                raise ValueError(
                    "independent and primary sources are counted per publisher among the citations that agree with the verdict"
                )
            if p.validity != "expires" and p.validity not in {
                c.validity for c in agreeing
            }:
                raise ValueError(
                    "the premises' validity must come from an agreeing citation"
                )
        if self.verdict == "insufficient_evidence" and (
            self.unresolved is None or not self.unresolved
        ):
            raise ValueError(
                "'insufficient_evidence' must say what could not be established"
            )
        if self.strength and is_stale(self.strength.premises) and not self.archival:
            raise ValueError(
                "evidence older than the catalogue threshold must be marked archival"
            )
        if (
            self.archival
            and self.strength
            and self.strength.premises.validity != "expires"
        ):
            raise ValueError(
                "evidence that does not expire (law in force, page updated in place, past event) is never archival"
            )
        return self


class Escalation(_Model):
    """Hand-off to the moderator queue. 'recommended' means nobody was notified yet.

    Computed on every request, cache hits included: the result cache never stores it.
    """

    state: Literal["recommended", "created", "updated"]
    case_id: Annotated[str | None, Field(pattern=r"^#S-\d+$")] = None

    @model_validator(mode="after")
    def _case_only_when_handed_off(self) -> Escalation:
        if (self.state == "recommended") != (self.case_id is None):
            raise ValueError(
                "a case id exists only after the case was created or updated"
            )
        return self


class CheckResult(_Model):
    """The answer every channel renders. The same normalised input within the result cache's lifetime gets the same substantive result on every channel."""

    check_id: Annotated[str, Field(min_length=1, max_length=40)]
    status: CheckStatus
    claims: list[ClaimResult] = []
    message: Annotated[
        str | None,
        Field(max_length=400, description="For non-verdict statuses: what to do next."),
    ] = None
    limitations: list[Annotated[str, Field(max_length=300)]] = []
    source_warning: SourceStatusWarning | None = None
    escalation: Escalation | None = None
    corpus_version: Annotated[
        str,
        Field(
            min_length=1,
            max_length=40,
            description="Id of the scheduled corpus snapshot.",
        ),
    ]
    ai_disclosure: Literal[True] = True

    @model_validator(mode="after")
    def _status_rules(self) -> CheckResult:
        if self.status == "done":
            if not self.claims:
                raise ValueError("a finished check has at least one claim")
            if not self.limitations:
                raise ValueError("a finished check states its limitations")
        elif self.claims or self.message is None or not self.message:
            raise ValueError(
                f"{self.status!r} is not a verdict: no claims, and a message instead"
            )
        return self


CacheableStatus = Literal["done", "needs_clarification", "out_of_scope"]


class CachedResult(_Model):
    """What the result cache keeps: only the substantive part of a CheckResult.

    The key is the normalised input. The entry lives a fixed time, whatever snapshots appear meanwhile.
    Escalation and the repeat counter are not here: they are computed on every request.
    A technical failure is never cached.
    """

    status: CacheableStatus
    claims: list[ClaimResult] = []
    message: Annotated[str | None, Field(max_length=400)] = None
    limitations: list[Annotated[str, Field(max_length=300)]] = []
    source_warning: SourceStatusWarning | None = None
    corpus_version: Annotated[str, Field(min_length=1, max_length=40)]
    source_ids: Annotated[
        list[str], Field(description="Ids of the sources cited in the claims.")
    ] = []
    cached_at: datetime
    expires_at: datetime

    @model_validator(mode="after")
    def _cache_rules(self) -> CachedResult:
        if self.expires_at <= self.cached_at:
            raise ValueError("a cache entry expires after it was stored")
        cited = {c.source.id for claim in self.claims for c in claim.citations}
        if cited != set(self.source_ids):
            raise ValueError("source_ids are the ids of the cited sources")
        return self


# ---------------------------------------------------------------- progress


class AnalysisStep(_Model):
    """One step of the processing strip shown between „Sprawdź” and the result."""

    code: Literal[
        "receive",
        "fetch_url",
        "screen_injection",
        "extract_claims",
        "search_corpus",
        "search_web",
        "search_fact_checks",
        "assess_evidence",
        "verify_citations",
        "write_answer",
        "save_record",
    ]
    status: Literal["pending", "active", "done", "skipped", "failed"]


class AnalysisStatus(_Model):
    """Polled (or streamed) by every channel while a check runs; mirrors the DBOS workflow."""

    check_id: str
    steps: Annotated[list[AnalysisStep], Field(min_length=1)]
    result: CheckResult | None = None


# ---------------------------------------------------------------- audit and moderation


class ModelUsage(_Model):
    """One model call: provider, model, region of processing, tokens and cost."""

    provider: Annotated[str, Field(max_length=60)]
    model: Annotated[str, Field(max_length=80)]
    region: Annotated[
        str, Field(max_length=40, description="Where the data was processed.")
    ]
    input_tokens: Annotated[int, Field(ge=0)]
    output_tokens: Annotated[int, Field(ge=0)]
    cost_usd: Annotated[float, Field(ge=0)]


class InjectionEvent(_Model):
    """Instructions found in the input or a source. Logged and never executed.

    In user content the instruction is cut out and the rest is analysed as data; a catalogue source
    with an instruction drops out of the evidence.
    """

    location: Literal["input", "source"]
    action: Literal["instruction_removed", "source_dropped"]
    source_url: HttpUrl | None = None
    excerpt: Annotated[str, Field(max_length=300)]

    @model_validator(mode="after")
    def _action_follows_location(self) -> InjectionEvent:
        expected = (
            "instruction_removed" if self.location == "input" else "source_dropped"
        )
        if self.action != expected:
            raise ValueError(
                "an instruction in user input is cut out; a source with one is dropped"
            )
        if (self.location == "source") != (self.source_url is not None):
            raise ValueError(
                "a source event names the source URL, an input event does not"
            )
        return self


class CheckRecord(_Model):
    """Audit log of one check (MSZ MVP: question, time, sources, result; plus observability)."""

    check_id: str
    session_id: Annotated[
        str,
        Field(
            min_length=8,
            max_length=64,
            description="Random id kept in the browser session.",
        ),
    ]
    user_id: Annotated[
        str | None,
        Field(
            min_length=8,
            max_length=64,
            description="Signed-in users only (Google or Microsoft account); None for anonymous checks.",
        ),
    ] = None
    channel: Channel
    channel_user_hash: Annotated[
        str | None,
        Field(
            pattern=r"^[0-9a-f]{64}$",
            description="Discord and SMS only: salted SHA-256 of the user id or phone number, used to reply and count repeats; never shown to moderators.",
        ),
    ] = None
    received_at: datetime
    answered_at: datetime
    question_masked: Annotated[
        str,
        Field(max_length=4000, description="Input with obvious personal data masked."),
    ]
    status: CheckStatus
    verdicts: list[Verdict]
    source_ids: list[str]
    corpus_version: str
    models: list[ModelUsage]
    web_search_calls: Annotated[int, Field(ge=0)] = 0
    retrieval_errors: list[Annotated[str, Field(max_length=200)]] = []
    injection_events: list[InjectionEvent] = []
    escalation: Escalation | None = None
    cache_hit: Annotated[
        bool,
        Field(
            description="Substantive part served from the result cache; escalation was still computed."
        ),
    ] = False
    retention_until: datetime

    @model_validator(mode="after")
    def _channel_identity(self) -> CheckRecord:
        if (self.channel in {"discord", "sms"}) != (self.channel_user_hash is not None):
            raise ValueError(
                "only Discord and SMS checks carry a hashed channel user id, and they always do"
            )
        return self

    @property
    def latency_ms(self) -> int:
        """Time from receiving the question to answering it, in milliseconds."""
        return int((self.answered_at - self.received_at).total_seconds() * 1000)

    @property
    def cost_usd(self) -> float:
        """Total model cost of the check."""
        return sum(m.cost_usd for m in self.models)

    @property
    def abstained(self) -> bool:
        """Whether a finished check settled no claim."""
        return self.status == "done" and all(
            v in {"insufficient_evidence", "not_verifiable"} for v in self.verdicts
        )


CaseReason = Literal["insufficient_evidence", "high_risk", "repeated_unanswered"]
StaffRole = Literal[
    "moderator", "analyst", "admin"
]  # admin manages staff accounts and the high-risk topic list


class CaseClaim(_Model):
    """One unanswered claim in a case (its verdict was "insufficient_evidence") and the checks that asked it."""

    claim: Annotated[str, Field(min_length=5, max_length=500)]
    check_ids: Annotated[list[str], Field(min_length=1)]


class ModeratorCase(_Model):
    """One case per group of similar unanswered claims. Similarity is measured per claim; a repeated claim joins the case."""

    id: Annotated[str, Field(pattern=r"^#S-\d+$")]
    state: Literal["open", "answered", "closed"]
    reasons: Annotated[list[CaseReason], Field(min_length=1)]
    high_risk_topic: Annotated[
        str | None,
        Field(
            max_length=80,
            description="Topic from the admin's high-risk list that matched.",
        ),
    ] = None
    high_risk_classified_by: Annotated[
        Literal["model", "keywords"] | None,
        Field(
            description="Model classification against the admin list, or the keyword list as a fallback."
        ),
    ] = None
    summary: Annotated[str, Field(min_length=5, max_length=300)]
    claims: Annotated[list[CaseClaim], Field(min_length=1)]
    first_seen: datetime
    last_seen: datetime
    assignee_role: Literal["moderator", "analyst"] = "moderator"

    @model_validator(mode="after")
    def _case_rules(self) -> ModeratorCase:
        if len(set(self.reasons)) != len(self.reasons):
            raise ValueError("each reason is listed once")
        high_risk = "high_risk" in self.reasons
        if high_risk != (self.high_risk_topic is not None) or high_risk != (
            self.high_risk_classified_by is not None
        ):
            raise ValueError(
                "a high-risk case names the matched topic and how it was classified"
            )
        return self

    @property
    def check_ids(self) -> list[str]:
        """Distinct checks grouped by the case, in order of appearance."""
        return list(dict.fromkeys(i for c in self.claims for i in c.check_ids))

    @property
    def similar_count(self) -> int:
        """How many checks the case groups."""
        return len(self.check_ids)
