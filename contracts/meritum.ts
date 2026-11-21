/* Generated from contracts/meritum_contracts.py by contracts/generate.sh. Do not edit. */

export type Id = string;
export type Ads = number;
export type Domains = number;
export type Days = number;
export type Label = string;
export type HelpfulPct = number;
export type Ratings = number;
export type ThresholdPct = number;
export type SavedAt = string;
export type Screenshot = boolean;
export type Redirects = number;
export type FinalDomain = string;
export type Kind = "note";
export type Status = "verified" | "pending";
export type Body = string;
/**
 * @minItems 1
 */
export type Sources = [Source, ...Source[]];
export type Title = string;
export type Url = string;
export type Domain = string;
export type Kind1 = "akt_prawny" | "instytucja" | "media" | "fact_check" | "encyklopedia" | "oswiadczenie";
/**
 * Media only: position from left (-1) to right (1) as rated by users.
 */
export type Spectrum = number | null;
export type Code =
  | "false_authority"
  | "conspiracy_theory"
  | "out_of_context"
  | "urgency_pressure"
  | "fabricated_quote"
  | "manipulated_media"
  | "impersonation"
  | "cherry_picking";
/**
 * How many user remarks the AI draft used.
 */
export type DraftedFromReports = number;
export type Kind2 = "scam";
export type Body1 = string;
/**
 * @minItems 1
 */
export type Sources1 = [Source, ...Source[]];
/**
 * @minItems 2
 */
export type Signals = [
  "cert_warning_list" | "known_campaign" | "celebrity_registry" | "user_reports",
  "cert_warning_list" | "known_campaign" | "celebrity_registry" | "user_reports",
  ...("cert_warning_list" | "known_campaign" | "celebrity_registry" | "user_reports")[]
];
/**
 * This interface was referenced by `MeritumUIContracts`'s JSON-Schema
 * via the `definition` "InjectedCard".
 */
export type InjectedCard = NoteCard | ScamWarningCard;
export type Platform = "x" | "facebook" | "instagram" | "reddit" | "tiktok";
export type PostUrl = string;
export type PostHandle = string;
export type Kind3 = "manipulation" | "scam";
export type Reasons = (
  | ("false_information" | "conspiracy_theory" | "out_of_context" | "false_authority" | "manipulated_media")
  | (
      | "fake_celebrity_endorsement"
      | "suspicious_investment"
      | "impersonating_bank_or_office"
      | "fake_shop_or_fundraiser"
    )
)[];
export type Note = string;
export type SourceUrl = string | null;
export type Code1 =
  | "link_similar_reports"
  | "collect_sources"
  | "draft_and_rate"
  | "save_evidence"
  | "match_campaigns"
  | "check_cert_list"
  | "store_report";
export type Status1 = "pending" | "active" | "done" | "failed";
export type ReportId = string;
/**
 * @minItems 1
 */
export type Steps = [AnalysisStep, ...AnalysisStep[]];
export type Outcome = "running" | "note_published" | "note_pending" | "scam_flagged" | "collected" | "failed";
export type Card = (NoteCard | ScamWarningCard) | null;
export type At = string;
export type Handle = string;
export type Reason = "same_cluster" | "timing_pattern" | "new_account" | "rating_graph";
export type T = string;
export type Counted = number;
export type Rejected = number;
export type NoteId = string;
export type ClusterSize = number;
export type AttackFrom = string;
export type StatusChanged = boolean;
/**
 * @minItems 1
 */
export type Series = [VoteMinute, ...VoteMinute[]];
export type RejectedAccounts = RejectedAccount[];
export type Simulated = boolean;
export type Domain1 = string;
export type State = "active" | "dead" | "predicted";
export type FirstSeen = string;
export type LastSeen = string | null;
export type Ads1 = number;
export type Code2 =
  "celebrity_face" | "landing_template" | "cert_issuer_pattern" | "payment_gateway" | "advertiser_accounts" | "ad_copy";
export type Ads2 = number;
export type Id1 = string;
export type Title1 = string;
export type AdsTotal = number;
/**
 * @minItems 1
 */
export type Domains1 = [CampaignDomain, ...CampaignDomain[]];
export type SharedTraces = SharedTrace[];
export type Simulated1 = boolean;

export interface MeritumUIContracts {
  [k: string]: unknown;
}
/**
 * This interface was referenced by `MeritumUIContracts`'s JSON-Schema
 * via the `definition` "CampaignRef".
 */
export interface CampaignRef {
  id: Id;
  ads: Ads;
  domains: Domains;
  days: Days;
}
/**
 * Bridging consensus: published only when BOTH groups pass the threshold.
 *
 * This interface was referenced by `MeritumUIContracts`'s JSON-Schema
 * via the `definition` "Consensus".
 */
export interface Consensus {
  group_a: GroupScore;
  group_b: GroupScore;
  threshold_pct?: ThresholdPct;
}
/**
 * This interface was referenced by `MeritumUIContracts`'s JSON-Schema
 * via the `definition` "GroupScore".
 */
export interface GroupScore {
  label: Label;
  helpful_pct: HelpfulPct;
  ratings: Ratings;
}
/**
 * What the extension saved before the ad could vanish.
 *
 * This interface was referenced by `MeritumUIContracts`'s JSON-Schema
 * via the `definition` "Evidence".
 */
export interface Evidence {
  saved_at: SavedAt;
  screenshot: Screenshot;
  redirects: Redirects;
  final_domain: FinalDomain;
}
/**
 * Community context note under a post (MSZ "Prawdowid").
 *
 * This interface was referenced by `MeritumUIContracts`'s JSON-Schema
 * via the `definition` "NoteCard".
 */
export interface NoteCard {
  kind?: Kind;
  status: Status;
  body: Body;
  sources: Sources;
  technique?: Technique | null;
  consensus: Consensus;
  drafted_from_reports: DraftedFromReports;
}
/**
 * A citation. Every published card has at least one.
 *
 * This interface was referenced by `MeritumUIContracts`'s JSON-Schema
 * via the `definition` "Source".
 */
export interface Source {
  title: Title;
  url: Url;
  domain: Domain;
  kind: Kind1;
  spectrum?: Spectrum;
}
/**
 * Named manipulation technique; the card teaches how to spot it.
 *
 * This interface was referenced by `MeritumUIContracts`'s JSON-Schema
 * via the `definition` "Technique".
 */
export interface Technique {
  code: Code;
}
/**
 * Fake ad / scam warning (NASK "Kolekcjoner fejków"). Requires two independent signals.
 *
 * This interface was referenced by `MeritumUIContracts`'s JSON-Schema
 * via the `definition` "ScamWarningCard".
 */
export interface ScamWarningCard {
  kind?: Kind2;
  body: Body1;
  sources: Sources1;
  technique?: Technique | null;
  campaign?: CampaignRef | null;
  evidence: Evidence;
  signals: Signals;
}
/**
 * Sent by the Quick Report Popover.
 *
 * This interface was referenced by `MeritumUIContracts`'s JSON-Schema
 * via the `definition` "ReportPayload".
 */
export interface ReportPayload {
  platform: Platform;
  post_url: PostUrl;
  post_handle: PostHandle;
  kind: Kind3;
  reasons?: Reasons;
  note?: Note;
  source_url?: SourceUrl;
}
/**
 * This interface was referenced by `MeritumUIContracts`'s JSON-Schema
 * via the `definition` "AnalysisStep".
 */
export interface AnalysisStep {
  code: Code1;
  status: Status1;
}
/**
 * Polled (or streamed) by the extension after a report; mirrors the DBOS workflow.
 *
 * This interface was referenced by `MeritumUIContracts`'s JSON-Schema
 * via the `definition` "AnalysisStatus".
 */
export interface AnalysisStatus {
  report_id: ReportId;
  steps: Steps;
  outcome: Outcome;
  card?: Card;
}
/**
 * This interface was referenced by `MeritumUIContracts`'s JSON-Schema
 * via the `definition` "RejectedAccount".
 */
export interface RejectedAccount {
  at: At;
  handle: Handle;
  reason: Reason;
}
/**
 * This interface was referenced by `MeritumUIContracts`'s JSON-Schema
 * via the `definition` "VoteMinute".
 */
export interface VoteMinute {
  t: T;
  counted: Counted;
  rejected: Rejected;
}
/**
 * Live Dashboard telemetry. Totals are derived from `series`, never sent separately.
 *
 * This interface was referenced by `MeritumUIContracts`'s JSON-Schema
 * via the `definition` "BotDefenseSnapshot".
 */
export interface BotDefenseSnapshot {
  note_id: NoteId;
  cluster_size: ClusterSize;
  attack_from: AttackFrom;
  status_changed: StatusChanged;
  series: Series;
  rejected_accounts: RejectedAccounts;
  simulated?: Simulated;
}
/**
 * This interface was referenced by `MeritumUIContracts`'s JSON-Schema
 * via the `definition` "CampaignDomain".
 */
export interface CampaignDomain {
  domain: Domain1;
  state: State;
  first_seen: FirstSeen;
  last_seen?: LastSeen;
  ads: Ads1;
}
/**
 * This interface was referenced by `MeritumUIContracts`'s JSON-Schema
 * via the `definition` "SharedTrace".
 */
export interface SharedTrace {
  code: Code2;
  ads: Ads2;
}
/**
 * Campaign view: one sighting, the whole operation.
 *
 * This interface was referenced by `MeritumUIContracts`'s JSON-Schema
 * via the `definition` "Campaign".
 */
export interface Campaign {
  id: Id1;
  title: Title1;
  ads_total: AdsTotal;
  ads_by_platform: AdsByPlatform;
  domains: Domains1;
  shared_traces: SharedTraces;
  simulated?: Simulated1;
}
export interface AdsByPlatform {
  [k: string]: number;
}
