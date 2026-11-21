"""Meritum UI contracts: the data every Meritum surface renders.

Source of truth for the API (FastAPI + Pydantic), the Chrome extension and the panel.
JSON Schema and TypeScript types are generated from this file: `contracts/generate.sh`.
User-facing strings live in `copy/pl.json`; this file carries codes, not copy.
"""

from __future__ import annotations

from datetime import datetime
from typing import Annotated, Literal

from pydantic import BaseModel, ConfigDict, Field, HttpUrl, model_validator

Platform = Literal["x", "facebook", "instagram", "reddit", "tiktok"]

SourceKind = Literal["akt_prawny", "instytucja", "media", "fact_check", "encyklopedia", "oswiadczenie"]

ReportKind = Literal["manipulation", "scam"]

ManipulationReason = Literal[
    "false_information",
    "conspiracy_theory",
    "out_of_context",
    "false_authority",
    "manipulated_media",
]
ScamReason = Literal[
    "fake_celebrity_endorsement",
    "suspicious_investment",
    "impersonating_bank_or_office",
    "fake_shop_or_fundraiser",
]

TechniqueCode = Literal[
    "false_authority",
    "conspiracy_theory",
    "out_of_context",
    "urgency_pressure",
    "fabricated_quote",
    "manipulated_media",
    "impersonation",
    "cherry_picking",
]


class _Model(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)


class Source(_Model):
    """A citation. Every published card has at least one."""

    title: Annotated[str, Field(min_length=3, max_length=140)]
    url: HttpUrl
    domain: Annotated[str, Field(min_length=3, max_length=100)]
    kind: SourceKind
    spectrum: Annotated[
        float | None,
        Field(ge=-1, le=1, description="Media only: position from left (-1) to right (1) as rated by users."),
    ] = None


class Technique(_Model):
    """Named manipulation technique; the card teaches how to spot it."""

    code: TechniqueCode


class GroupScore(_Model):
    label: Annotated[str, Field(max_length=40)]
    helpful_pct: Annotated[int, Field(ge=0, le=100)]
    ratings: Annotated[int, Field(ge=0)]


class Consensus(_Model):
    """Bridging consensus: published only when BOTH groups pass the threshold."""

    group_a: GroupScore
    group_b: GroupScore
    threshold_pct: Annotated[int, Field(ge=50, le=100)] = 70

    @property
    def passed(self) -> bool:
        return min(self.group_a.helpful_pct, self.group_b.helpful_pct) >= self.threshold_pct


class NoteCard(_Model):
    """Community context note under a post (MSZ "Prawdowid")."""

    kind: Literal["note"] = "note"
    status: Literal["verified", "pending"]
    body: Annotated[str, Field(min_length=20, max_length=600)]
    sources: Annotated[list[Source], Field(min_length=1)]
    technique: Technique | None = None
    consensus: Consensus
    drafted_from_reports: Annotated[int, Field(ge=1, description="How many user remarks the AI draft used.")]

    @model_validator(mode="after")
    def _verified_needs_consensus(self) -> NoteCard:
        if self.status == "verified" and not self.consensus.passed:
            raise ValueError("a verified note needs both groups above the threshold")
        return self


class CampaignRef(_Model):
    id: Annotated[str, Field(pattern=r"^#K-\d+$")]
    ads: Annotated[int, Field(ge=1)]
    domains: Annotated[int, Field(ge=1)]
    days: Annotated[int, Field(ge=1)]


class Evidence(_Model):
    """What the extension saved before the ad could vanish."""

    saved_at: datetime
    screenshot: bool
    redirects: Annotated[int, Field(ge=0)]
    final_domain: str


class ScamWarningCard(_Model):
    """Fake ad / scam warning (NASK "Kolekcjoner fejków"). Requires two independent signals."""

    kind: Literal["scam"] = "scam"
    body: Annotated[str, Field(min_length=20, max_length=600)]
    sources: Annotated[list[Source], Field(min_length=1)]
    technique: Technique | None = None
    campaign: CampaignRef | None = None
    evidence: Evidence
    signals: Annotated[list[Literal["cert_warning_list", "known_campaign", "celebrity_registry", "user_reports"]], Field(min_length=2)]


InjectedCard = Annotated[NoteCard | ScamWarningCard, Field(discriminator="kind")]


class ReportPayload(_Model):
    """Sent by the Quick Report Popover."""

    platform: Platform
    post_url: HttpUrl
    post_handle: Annotated[str, Field(max_length=60)]
    kind: ReportKind
    reasons: list[ManipulationReason | ScamReason] = []
    note: Annotated[str, Field(max_length=1000)] = ""
    source_url: HttpUrl | None = None

    @model_validator(mode="after")
    def _reason_or_note(self) -> ReportPayload:
        if not self.reasons and len(self.note.strip()) < 3:
            raise ValueError("pick at least one reason or describe the problem (3+ characters)")
        return self


class AnalysisStep(_Model):
    code: Literal[
        "link_similar_reports",
        "collect_sources",
        "draft_and_rate",
        "save_evidence",
        "match_campaigns",
        "check_cert_list",
        "store_report",
    ]
    status: Literal["pending", "active", "done", "failed"]


class AnalysisStatus(_Model):
    """Polled (or streamed) by the extension after a report; mirrors the DBOS workflow."""

    report_id: str
    steps: Annotated[list[AnalysisStep], Field(min_length=1)]
    outcome: Literal["running", "note_published", "note_pending", "scam_flagged", "collected", "failed"]
    card: InjectedCard | None = None


class VoteMinute(_Model):
    t: Annotated[str, Field(pattern=r"^\d{2}:\d{2}$")]
    counted: Annotated[int, Field(ge=0)]
    rejected: Annotated[int, Field(ge=0)]


class RejectedAccount(_Model):
    at: datetime
    handle: str
    reason: Literal["same_cluster", "timing_pattern", "new_account", "rating_graph"]


class BotDefenseSnapshot(_Model):
    """Live Dashboard telemetry. Totals are derived from `series`, never sent separately."""

    note_id: Annotated[str, Field(pattern=r"^#N-\d+$")]
    cluster_size: Annotated[int, Field(ge=1)]
    attack_from: Annotated[str, Field(pattern=r"^\d{2}:\d{2}(:\d{2})?$")]
    status_changed: bool
    series: Annotated[list[VoteMinute], Field(min_length=1)]
    rejected_accounts: list[RejectedAccount]
    simulated: bool = True

    @property
    def counted_total(self) -> int:
        return sum(m.counted for m in self.series)

    @property
    def rejected_total(self) -> int:
        return sum(m.rejected for m in self.series)


class CampaignDomain(_Model):
    domain: str
    state: Literal["active", "dead", "predicted"]
    first_seen: datetime
    last_seen: datetime | None = None
    ads: Annotated[int, Field(ge=0)]


class SharedTrace(_Model):
    code: Literal["celebrity_face", "landing_template", "cert_issuer_pattern", "payment_gateway", "advertiser_accounts", "ad_copy"]
    ads: Annotated[int, Field(ge=1)]


class Campaign(_Model):
    """Campaign view: one sighting, the whole operation."""

    id: Annotated[str, Field(pattern=r"^#K-\d+$")]
    title: Annotated[str, Field(max_length=80)]
    ads_total: Annotated[int, Field(ge=1)]
    ads_by_platform: dict[Platform, Annotated[int, Field(ge=0)]]
    domains: Annotated[list[CampaignDomain], Field(min_length=1)]
    shared_traces: list[SharedTrace]
    simulated: bool = True

    @model_validator(mode="after")
    def _sum_closes(self) -> Campaign:
        if sum(self.ads_by_platform.values()) != self.ads_total:
            raise ValueError("ads_by_platform must add up to ads_total (the sum on screen has to close)")
        return self
