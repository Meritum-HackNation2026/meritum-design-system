"""Meritum contracts: the data every Meritum surface renders (MSZ "Prawdowid").

Decided target: the single source of truth is the meritum-core repository; the design system consumes the generated
JSON Schema and TypeScript types. Until the move, this file is the working copy (`contracts/generate.sh`).
User-facing strings live in `copy/pl.json`; this file carries codes, not copy.

Rules from the MSZ brief that the models enforce:
- a verdict that settles a claim (confirmed, false, misleading) needs at least one citation and explicit premises;
- the strength of a verdict follows from the premises by a fixed rule, never from the model's say-so;
- agreement follows from the citation stances; conflicting credible sources give "insufficient_evidence" with both sides cited and no strength;
- independence is counted per publisher, not per page or domain;
- evidence age is measured against the date the claim refers to, with a per-catalogue-entry threshold; evidence that does not
  expire (a legal act in force, an official page updated in place, evidence about a past event) is never archival;
- insufficient evidence says what could not be established;
- technical failure, a request for clarification and out-of-scope input are not verdicts and carry no claims;
- recommending a hand-off to a moderator is distinct from creating a case.
"""

from __future__ import annotations

from datetime import datetime
from typing import Annotated, Literal

from pydantic import BaseModel, ConfigDict, Field, HttpUrl, model_validator

Channel = Literal["web", "extension", "discord", "sms", "mcp"]

Verdict = Literal["confirmed", "false", "misleading", "insufficient_evidence", "not_verifiable"]
SETTLING: frozenset[Verdict] = frozenset({"confirmed", "false", "misleading"})

# Outcomes that are not verdicts and must be shown separately (MSZ section 2 and 5).
CheckStatus = Literal["done", "needs_clarification", "out_of_scope", "technical_failure"]

SourceKind = Literal["akt_prawny", "dane_publiczne", "instytucja", "fact_check", "media", "encyklopedia"]
SourceTier = Literal["primary", "secondary"]  # primary: official documents and public data; secondary: fact-checkers, media
SourceVia = Literal["corpus", "rss", "web_search"]  # how the document reached the corpus
Stance = Literal["supports", "refutes", "context"]
Agreement = Literal["consistent", "conflicting"]
# Overrides of the age rule. expires: age counts; in_force: e.g. a legal act in force; updated_in_place: standing official
# guidance edited in place (passenger rights, contact pages); past_event: evidence explicitly about a past event.
Validity = Literal["expires", "in_force", "updated_in_place", "past_event"]
DEFAULT_MAX_AGE_HOURS = 365 * 24
Strength = Literal["strong", "moderate", "weak"]

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
    page_url: Annotated[HttpUrl | None, Field(description="Extension only: the post the text came from.")] = None

    @model_validator(mode="after")
    def _text_or_url(self) -> CheckRequest:
        if self.url is None and (self.text is None or len(self.text.strip()) < 3):
            raise ValueError("send text (3+ characters) or a URL")
        return self


# ---------------------------------------------------------------- sources


class Source(_Model):
    """A document from the audited corpus. Title, publisher, date and link are mandatory to show (MSZ section 2)."""

    id: Annotated[str, Field(min_length=1, max_length=80)]
    title: Annotated[str, Field(min_length=3, max_length=200)]
    publisher: Annotated[str, Field(min_length=2, max_length=120)]
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
    fragment_found_verbatim: Literal[True] = True


class CatalogEntry(_Model):
    """One domain in the open source catalogue: why it qualifies, how it is refreshed, whether it is excluded."""

    domain: Annotated[str, Field(min_length=3, max_length=100)]
    publisher: Annotated[str, Field(min_length=2, max_length=120)]
    kind: SourceKind
    tier: SourceTier
    license: Annotated[str, Field(min_length=2, max_length=120)]
    ingest: Literal["static", "rss", "sitemap", "web_search"]
    refresh_hours: Annotated[int | None, Field(ge=1)] = None
    validity: Annotated[Validity, Field(description="Age override for every document of this entry; past_event is set per evidence.")] = "expires"
    max_age_hours: Annotated[
        int | None, Field(ge=1, description="Shorter threshold for short-lived sources (warnings, roads, weather: hours or days).")
    ] = None
    qualified_because: Annotated[str, Field(min_length=10, max_length=300)]
    excluded: bool = False
    exclusion_reason: Annotated[str | None, Field(max_length=300)] = None

    @model_validator(mode="after")
    def _exclusion_has_reason(self) -> CatalogEntry:
        if self.excluded and not self.exclusion_reason:
            raise ValueError("an excluded source needs a reason")
        if self.validity == "past_event":
            raise ValueError("'past_event' describes one piece of evidence, not a whole catalogue entry")
        if self.validity != "expires" and self.max_age_hours is not None:
            raise ValueError("a source that does not expire has no maximum age")
        return self


# ---------------------------------------------------------------- verdict


class Premises(_Model):
    """Explicit premises behind a verdict (MSZ: strength must follow from quality, recency, agreement, independence)."""

    independent_sources: Annotated[int, Field(ge=0, description="Distinct publishers (institutions) among the citations.")]
    primary_sources: Annotated[int, Field(ge=0, description="Distinct primary-tier publishers among the citations.")]
    newest_source_age_hours: Annotated[
        int | None, Field(ge=0, description="Hours between the newest source and the date the claim refers to, not now.")
    ] = None
    max_age_hours: Annotated[int, Field(ge=1, description="Threshold from the catalogue entry of the newest source.")] = DEFAULT_MAX_AGE_HOURS
    validity: Validity = "expires"
    agreement: Agreement


def is_stale(p: Premises) -> bool:
    return p.validity == "expires" and p.newest_source_age_hours is not None and p.newest_source_age_hours > p.max_age_hours


def strength_for(p: Premises) -> Strength:
    """The one rule that turns premises into strength. Shown to the user next to the premises."""
    if p.agreement == "consistent" and p.independent_sources >= 2 and p.primary_sources >= 1 and not is_stale(p):
        return "strong"
    if p.agreement == "consistent" and p.independent_sources >= 1:
        return "moderate"
    return "weak"


class EvidenceStrength(_Model):
    level: Strength
    premises: Premises

    @model_validator(mode="after")
    def _level_follows_premises(self) -> EvidenceStrength:
        if self.level != strength_for(self.premises):
            raise ValueError(f"strength must be {strength_for(self.premises)!r} for these premises")
        return self


class IncidentMatch(_Model):
    """Similarity to a known incident. Context only: never a basis for the verdict by itself."""

    incident_id: Annotated[str, Field(min_length=1, max_length=80)]
    title: Annotated[str, Field(max_length=200)]
    date: datetime
    url: HttpUrl
    similarity: Annotated[float, Field(ge=0, le=1)]


class SourceStatusWarning(_Model):
    """Neutral note about who published the checked content (e.g. an EU-sanctioned entity). Never a verdict."""

    code: Literal["eu_sanctioned_entity", "state_controlled_media"]
    entity: Annotated[str, Field(max_length=120)]
    basis_url: HttpUrl


class ClaimResult(_Model):
    """One checked claim. Citations (source material) are kept apart from `explanation` (model interpretation)."""

    claim: Annotated[str, Field(min_length=5, max_length=500)]
    verdict: Verdict
    strength: EvidenceStrength | None = None
    citations: list[Citation] = []
    explanation: Annotated[str, Field(min_length=10, max_length=800)]
    unresolved: Annotated[str | None, Field(max_length=500, description="What could not be established.")] = None
    archival: Annotated[bool, Field(description="Newest evidence is older than the claim's context needs.")] = False
    technique: TechniqueCode | None = None
    incident: IncidentMatch | None = None

    @model_validator(mode="after")
    def _verdict_rules(self) -> ClaimResult:
        stances = {c.stance for c in self.citations}
        conflicting = {"supports", "refutes"} <= stances
        if conflicting and (self.verdict != "insufficient_evidence" or self.strength is not None):
            raise ValueError("conflicting sources give 'insufficient_evidence' with both sides cited and no strength")
        if self.verdict == "insufficient_evidence" and self.citations and not conflicting:
            raise ValueError("'insufficient_evidence' carries citations only when credible sources conflict")
        if self.strength:
            p = self.strength.premises
            publishers = {c.source.publisher for c in self.citations}
            primary = {c.source.publisher for c in self.citations if c.source.tier == "primary"}
            if p.agreement != ("conflicting" if conflicting else "consistent"):
                raise ValueError("agreement must follow from the citation stances")
            if (p.independent_sources, p.primary_sources) != (len(publishers), len(primary)):
                raise ValueError("independent and primary sources are counted per publisher among the citations")
        if self.verdict in SETTLING:
            if not self.citations or self.strength is None:
                raise ValueError(f"verdict {self.verdict!r} needs citations and premises")
            if self.verdict == "confirmed" and "supports" not in stances:
                raise ValueError("'confirmed' needs a supporting citation")
            if self.verdict == "false" and "refutes" not in stances:
                raise ValueError("'false' needs a refuting citation")
            if self.verdict == "misleading" and ("context" not in stances or self.technique is None):
                raise ValueError("'misleading' needs a context citation and the technique it uses")
        if self.verdict == "insufficient_evidence" and not self.unresolved:
            raise ValueError("'insufficient_evidence' must say what could not be established")
        if self.strength and is_stale(self.strength.premises) and not self.archival:
            raise ValueError("evidence older than the catalogue threshold must be marked archival")
        if self.archival and self.strength and self.strength.premises.validity != "expires":
            raise ValueError("evidence that does not expire (law in force, page updated in place, past event) is never archival")
        return self


class Escalation(_Model):
    """Hand-off to the moderator queue. 'recommended' means nobody was notified yet."""

    state: Literal["recommended", "created", "updated"]
    case_id: Annotated[str | None, Field(pattern=r"^#S-\d+$")] = None

    @model_validator(mode="after")
    def _case_only_when_handed_off(self) -> Escalation:
        if (self.state == "recommended") != (self.case_id is None):
            raise ValueError("a case id exists only after the case was created or updated")
        return self


class CheckResult(_Model):
    """The answer every channel renders. Same request, same corpus version: same result on every channel."""

    check_id: Annotated[str, Field(min_length=1, max_length=40)]
    status: CheckStatus
    claims: list[ClaimResult] = []
    message: Annotated[str | None, Field(max_length=400, description="For non-verdict statuses: what to do next.")] = None
    limitations: list[Annotated[str, Field(max_length=300)]] = []
    source_warning: SourceStatusWarning | None = None
    escalation: Escalation | None = None
    corpus_version: Annotated[str, Field(min_length=1, max_length=40, description="Id of the scheduled corpus snapshot.")]
    ai_disclosure: Literal[True] = True

    @model_validator(mode="after")
    def _status_rules(self) -> CheckResult:
        if self.status == "done":
            if not self.claims:
                raise ValueError("a finished check has at least one claim")
            if not self.limitations:
                raise ValueError("a finished check states its limitations")
        elif self.claims or not self.message:
            raise ValueError(f"{self.status!r} is not a verdict: no claims, and a message instead")
        return self


# ---------------------------------------------------------------- progress


class AnalysisStep(_Model):
    code: Literal[
        "receive",
        "extract_claims",
        "search_corpus",
        "search_web",
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
    provider: Annotated[str, Field(max_length=60)]
    model: Annotated[str, Field(max_length=80)]
    region: Annotated[str, Field(max_length=40, description="Where the data was processed.")]
    input_tokens: Annotated[int, Field(ge=0)]
    output_tokens: Annotated[int, Field(ge=0)]
    cost_usd: Annotated[float, Field(ge=0)]


class InjectionEvent(_Model):
    """Instructions found in the input or a source. Logged and ignored."""

    location: Literal["input", "source"]
    source_url: HttpUrl | None = None
    excerpt: Annotated[str, Field(max_length=300)]


class CheckRecord(_Model):
    """Audit log of one check (MSZ MVP: question, time, sources, result; plus observability)."""

    check_id: str
    session_id: Annotated[str, Field(min_length=8, max_length=64, description="Random id kept in the browser session.")]
    user_id: Annotated[
        str | None,
        Field(min_length=8, max_length=64, description="Signed-in users only (Google or Microsoft account); None for anonymous checks."),
    ] = None
    channel: Channel
    received_at: datetime
    answered_at: datetime
    question_masked: Annotated[str, Field(max_length=4000, description="Input with obvious personal data masked.")]
    status: CheckStatus
    verdicts: list[Verdict]
    source_ids: list[str]
    corpus_version: str
    models: list[ModelUsage]
    web_search_calls: Annotated[int, Field(ge=0)] = 0
    retrieval_errors: list[Annotated[str, Field(max_length=200)]] = []
    injection_events: list[InjectionEvent] = []
    escalation: Escalation | None = None
    retention_until: datetime

    @property
    def latency_ms(self) -> int:
        return int((self.answered_at - self.received_at).total_seconds() * 1000)

    @property
    def cost_usd(self) -> float:
        return sum(m.cost_usd for m in self.models)

    @property
    def abstained(self) -> bool:
        return self.status == "done" and all(v in ("insufficient_evidence", "not_verifiable") for v in self.verdicts)


class ModeratorCase(_Model):
    """One case per group of similar unresolved checks. Repeated questions update it instead of opening new ones."""

    id: Annotated[str, Field(pattern=r"^#S-\d+$")]
    state: Literal["open", "answered", "closed"]
    reason: Literal["insufficient_evidence", "high_risk", "repeated_unanswered"]
    summary: Annotated[str, Field(min_length=5, max_length=300)]
    check_ids: Annotated[list[str], Field(min_length=1)]
    first_seen: datetime
    last_seen: datetime
    assignee_role: Literal["moderator", "analyst"] = "moderator"

    @property
    def similar_count(self) -> int:
        return len(self.check_ids)
