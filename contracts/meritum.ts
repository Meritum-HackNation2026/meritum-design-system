/* Generated from contracts/meritum_contracts.py by contracts/generate.sh. Do not edit. */

export type Channel = "web" | "extension" | "discord" | "mcp";
export type Text = string | null;
export type Url = string | null;
/**
 * Extension only: the post the text came from.
 */
export type PageUrl = string | null;
export type Id = string;
export type Title = string;
export type Publisher = string;
export type Url1 = string;
export type Domain = string;
export type Kind = "akt_prawny" | "dane_publiczne" | "instytucja" | "fact_check" | "media" | "encyklopedia";
export type Tier = "primary" | "secondary";
export type PublishedAt = string | null;
export type FetchedAt = string;
export type Language = string;
export type Via = "corpus" | "rss" | "web_search";
export type Fragment = string;
export type Stance = "supports" | "refutes" | "context";
export type FragmentFoundVerbatim = true;
export type Claim = string;
export type Verdict = "confirmed" | "false" | "misleading" | "insufficient_evidence" | "not_verifiable";
export type Level = "strong" | "moderate" | "weak";
export type IndependentSources = number;
export type PrimarySources = number;
export type NewestSourceAgeDays = number | null;
export type Agreement = "consistent" | "conflicting";
export type Citations = Citation[];
export type Explanation = string;
/**
 * What could not be established.
 */
export type Unresolved = string | null;
/**
 * Newest evidence is older than the claim's context needs.
 */
export type Archival = boolean;
export type Technique =
  | (
      | "false_authority"
      | "conspiracy_theory"
      | "out_of_context"
      | "outdated"
      | "fabricated_quote"
      | "manipulated_media"
      | "impersonation"
      | "cherry_picking"
    )
  | null;
export type IncidentId = string;
export type Title1 = string;
export type Date = string;
export type Url2 = string;
export type Similarity = number;
export type State = "recommended" | "created" | "updated";
export type CaseId = string | null;
export type Code = "eu_sanctioned_entity" | "state_controlled_media";
export type Entity = string;
export type BasisUrl = string;
export type CheckId = string;
export type Status = "done" | "needs_clarification" | "out_of_scope" | "technical_failure";
export type Claims = ClaimResult[];
/**
 * For non-verdict statuses: what to do next.
 */
export type Message = string | null;
export type Limitations = string[];
export type CorpusVersion = string;
export type AiDisclosure = true;
export type Code1 =
  | "receive"
  | "extract_claims"
  | "search_corpus"
  | "search_web"
  | "assess_evidence"
  | "verify_citations"
  | "write_answer"
  | "save_record";
export type Status1 = "pending" | "active" | "done" | "skipped" | "failed";
export type CheckId1 = string;
/**
 * @minItems 1
 */
export type Steps = [AnalysisStep, ...AnalysisStep[]];
export type Location = "input" | "source";
export type SourceUrl = string | null;
export type Excerpt = string;
export type Provider = string;
export type Model = string;
/**
 * Where the data was processed.
 */
export type Region = string;
export type InputTokens = number;
export type OutputTokens = number;
export type CostUsd = number;
export type CheckId2 = string;
export type Channel1 = "web" | "extension" | "discord" | "mcp";
export type ReceivedAt = string;
export type AnsweredAt = string;
/**
 * Input with obvious personal data masked.
 */
export type QuestionMasked = string;
export type Status2 = "done" | "needs_clarification" | "out_of_scope" | "technical_failure";
export type Verdicts = ("confirmed" | "false" | "misleading" | "insufficient_evidence" | "not_verifiable")[];
export type SourceIds = string[];
export type CorpusVersion1 = string;
export type Models = ModelUsage[];
export type WebSearchCalls = number;
export type RetrievalErrors = string[];
export type InjectionEvents = InjectionEvent[];
export type RetentionUntil = string;
export type Id1 = string;
export type State1 = "open" | "answered" | "closed";
export type Reason = "insufficient_evidence" | "high_risk" | "repeated_unanswered";
export type Summary = string;
/**
 * @minItems 1
 */
export type CheckIds = [string, ...string[]];
export type FirstSeen = string;
export type LastSeen = string;
export type AssigneeRole = "moderator" | "analyst";
export type Domain1 = string;
export type Publisher1 = string;
export type Kind1 = "akt_prawny" | "dane_publiczne" | "instytucja" | "fact_check" | "media" | "encyklopedia";
export type Tier1 = "primary" | "secondary";
export type License = string;
export type Ingest = "static" | "rss" | "sitemap" | "web_search";
export type RefreshHours = number | null;
export type QualifiedBecause = string;
export type Excluded = boolean;
export type ExclusionReason = string | null;

export interface MeritumContracts {
  [k: string]: unknown;
}
/**
 * What a channel adapter sends to the verification core. The core is channel-agnostic.
 *
 * This interface was referenced by `MeritumContracts`'s JSON-Schema
 * via the `definition` "CheckRequest".
 */
export interface CheckRequest {
  channel: Channel;
  text?: Text;
  url?: Url;
  page_url?: PageUrl;
}
/**
 * A fragment of a source and how it bears on the claim. The pipeline drops fragments it cannot find verbatim.
 *
 * This interface was referenced by `MeritumContracts`'s JSON-Schema
 * via the `definition` "Citation".
 */
export interface Citation {
  source: Source;
  fragment: Fragment;
  stance: Stance;
  fragment_found_verbatim?: FragmentFoundVerbatim;
}
/**
 * A document from the audited corpus. Title, publisher, date and link are mandatory to show (MSZ section 2).
 *
 * This interface was referenced by `MeritumContracts`'s JSON-Schema
 * via the `definition` "Source".
 */
export interface Source {
  id: Id;
  title: Title;
  publisher: Publisher;
  url: Url1;
  domain: Domain;
  kind: Kind;
  tier: Tier;
  published_at?: PublishedAt;
  fetched_at: FetchedAt;
  language?: Language;
  via?: Via;
}
/**
 * One checked claim. Citations (source material) are kept apart from `explanation` (model interpretation).
 *
 * This interface was referenced by `MeritumContracts`'s JSON-Schema
 * via the `definition` "ClaimResult".
 */
export interface ClaimResult {
  claim: Claim;
  verdict: Verdict;
  strength?: EvidenceStrength | null;
  citations?: Citations;
  explanation: Explanation;
  unresolved?: Unresolved;
  archival?: Archival;
  technique?: Technique;
  incident?: IncidentMatch | null;
}
/**
 * This interface was referenced by `MeritumContracts`'s JSON-Schema
 * via the `definition` "EvidenceStrength".
 */
export interface EvidenceStrength {
  level: Level;
  premises: Premises;
}
/**
 * Explicit premises behind a verdict (MSZ: strength must follow from quality, recency, agreement, independence).
 *
 * This interface was referenced by `MeritumContracts`'s JSON-Schema
 * via the `definition` "Premises".
 */
export interface Premises {
  independent_sources: IndependentSources;
  primary_sources: PrimarySources;
  newest_source_age_days?: NewestSourceAgeDays;
  agreement: Agreement;
}
/**
 * Similarity to a known incident. Context only: never a basis for the verdict by itself.
 *
 * This interface was referenced by `MeritumContracts`'s JSON-Schema
 * via the `definition` "IncidentMatch".
 */
export interface IncidentMatch {
  incident_id: IncidentId;
  title: Title1;
  date: Date;
  url: Url2;
  similarity: Similarity;
}
/**
 * Hand-off to the moderator queue. 'recommended' means nobody was notified yet.
 *
 * This interface was referenced by `MeritumContracts`'s JSON-Schema
 * via the `definition` "Escalation".
 */
export interface Escalation {
  state: State;
  case_id?: CaseId;
}
/**
 * Neutral note about who published the checked content (e.g. an EU-sanctioned entity). Never a verdict.
 *
 * This interface was referenced by `MeritumContracts`'s JSON-Schema
 * via the `definition` "SourceStatusWarning".
 */
export interface SourceStatusWarning {
  code: Code;
  entity: Entity;
  basis_url: BasisUrl;
}
/**
 * The answer every channel renders. Same request, same corpus version: same result on every channel.
 *
 * This interface was referenced by `MeritumContracts`'s JSON-Schema
 * via the `definition` "CheckResult".
 */
export interface CheckResult {
  check_id: CheckId;
  status: Status;
  claims?: Claims;
  message?: Message;
  limitations?: Limitations;
  source_warning?: SourceStatusWarning | null;
  escalation?: Escalation | null;
  corpus_version: CorpusVersion;
  ai_disclosure?: AiDisclosure;
}
/**
 * This interface was referenced by `MeritumContracts`'s JSON-Schema
 * via the `definition` "AnalysisStep".
 */
export interface AnalysisStep {
  code: Code1;
  status: Status1;
}
/**
 * Polled (or streamed) by every channel while a check runs; mirrors the DBOS workflow.
 *
 * This interface was referenced by `MeritumContracts`'s JSON-Schema
 * via the `definition` "AnalysisStatus".
 */
export interface AnalysisStatus {
  check_id: CheckId1;
  steps: Steps;
  result?: CheckResult | null;
}
/**
 * Instructions found in the input or a source. Logged and ignored.
 *
 * This interface was referenced by `MeritumContracts`'s JSON-Schema
 * via the `definition` "InjectionEvent".
 */
export interface InjectionEvent {
  location: Location;
  source_url?: SourceUrl;
  excerpt: Excerpt;
}
/**
 * This interface was referenced by `MeritumContracts`'s JSON-Schema
 * via the `definition` "ModelUsage".
 */
export interface ModelUsage {
  provider: Provider;
  model: Model;
  region: Region;
  input_tokens: InputTokens;
  output_tokens: OutputTokens;
  cost_usd: CostUsd;
}
/**
 * Audit log of one check (MSZ MVP: question, time, sources, result; plus observability).
 *
 * This interface was referenced by `MeritumContracts`'s JSON-Schema
 * via the `definition` "CheckRecord".
 */
export interface CheckRecord {
  check_id: CheckId2;
  channel: Channel1;
  received_at: ReceivedAt;
  answered_at: AnsweredAt;
  question_masked: QuestionMasked;
  status: Status2;
  verdicts: Verdicts;
  source_ids: SourceIds;
  corpus_version: CorpusVersion1;
  models: Models;
  web_search_calls?: WebSearchCalls;
  retrieval_errors?: RetrievalErrors;
  injection_events?: InjectionEvents;
  escalation?: Escalation | null;
  retention_until: RetentionUntil;
}
/**
 * One case per group of similar unresolved checks. Repeated questions update it instead of opening new ones.
 *
 * This interface was referenced by `MeritumContracts`'s JSON-Schema
 * via the `definition` "ModeratorCase".
 */
export interface ModeratorCase {
  id: Id1;
  state: State1;
  reason: Reason;
  summary: Summary;
  check_ids: CheckIds;
  first_seen: FirstSeen;
  last_seen: LastSeen;
  assignee_role?: AssigneeRole;
}
/**
 * One domain in the open source catalogue: why it qualifies, how it is refreshed, whether it is excluded.
 *
 * This interface was referenced by `MeritumContracts`'s JSON-Schema
 * via the `definition` "CatalogEntry".
 */
export interface CatalogEntry {
  domain: Domain1;
  publisher: Publisher1;
  kind: Kind1;
  tier: Tier1;
  license: License;
  ingest: Ingest;
  refresh_hours?: RefreshHours;
  qualified_because: QualifiedBecause;
  excluded?: Excluded;
  exclusion_reason?: ExclusionReason;
}
