import type { ReactNode } from "react"

import { Badge } from "@/components/ui/badge"
import { Button } from "@/components/ui/button"
import { Tooltip, TooltipContent, TooltipTrigger } from "@/components/ui/tooltip"
import { cn } from "@/lib/utils"

import { MeritumLabel } from "./meritum-mark"

export type SourceKind = "akt prawny" | "instytucja" | "media" | "encyklopedia" | "oświadczenie"

export interface Source {
  title: string
  url: string
  domain: string
  kind: SourceKind
}

export interface GroupScore {
  label: string
  helpfulPct: number
  ratings: number
}

interface BaseProps {
  /** Mandatory: a note or warning without at least one source must not render. */
  sources: [Source, ...Source[]]
  /** Plain-language technique name shown to teach recognition, e.g. "Fałszywy autorytet i presja czasu". */
  technique?: { name: string; howToSpot: string }
  /** One sentence for "Dlaczego to widzę?". */
  why: string
  className?: string
}

export type ContextCardProps =
  | (BaseProps & {
      variant: "note" | "pending"
      body: ReactNode
      consensus: { a: GroupScore; b: GroupScore; thresholdPct: number }
      vote?: "helpful" | "unhelpful" | null
      onVote?: (vote: "helpful" | "unhelpful") => void
    })
  | (BaseProps & {
      variant: "scam"
      body: ReactNode
      campaign: { id: string; summary: string; onOpen?: () => void }
      evidence: { savedAt: string; summary: string }
      onHide?: () => void
      onReportToPlatform?: () => void
      onDispute?: () => void
    })

const STATE = {
  note: { title: "Kontekst od społeczności", badge: "Zweryfikowany", tone: "bg-verified-surface text-verified-foreground" },
  pending: { title: "Kontekst w przygotowaniu", badge: "W ocenie", tone: "bg-contested-surface text-contested-foreground" },
  scam: { title: "Fałszywa reklama", badge: "Oszustwo", tone: "bg-scam-surface text-scam-foreground" },
} as const

/**
 * Injected Context Card: rendered by the extension under a post (inside Shadow DOM).
 * Frame adapts to the host via `data-host` variables; content, states and sources do not.
 */
export function ContextCard(props: ContextCardProps) {
  const s = STATE[props.variant]
  return (
    <section
      aria-label={`Meritum: ${s.title}`}
      className={cn(
        "animate-rise mt-3 border bg-[var(--host-card,var(--card))] font-[family-name:var(--host-font,var(--font-sans))] text-card-foreground",
        "rounded-[var(--host-radius,var(--radius))]",
        props.variant === "scam" ? "border-scam-border" : "border-border",
        props.className,
      )}
    >
      <header className="flex items-center gap-2 px-3.5 pt-3">
        <MeritumLabel />
        <Hint text={props.why} align="end">
          <span className="ml-auto cursor-help text-meta text-muted-foreground underline underline-offset-2">Dlaczego to widzę?</span>
        </Hint>
      </header>

      <div className="flex items-center gap-2 px-3.5 pt-2">
        <h3 className="font-sans text-body font-bold">{s.title}</h3>
        <Badge className={cn("ml-auto rounded-pill border-0 font-semibold", s.tone)}>{s.badge}</Badge>
      </div>

      <div className="px-3.5 pt-1.5 text-body text-pretty">{props.body}</div>

      <dl className="mx-3.5 mt-2.5 border-t border-border/70 text-small">
        {props.variant === "scam" && (
          <Row label="Kampania" hint="Ta sama twarz, szablon strony i wystawca certyfikatów co inne reklamy z tej kampanii.">
            <span>
              <b className="font-mono">{props.campaign.id}</b>: {props.campaign.summary}
            </span>
            {props.campaign.onOpen && (
              <button type="button" onClick={props.campaign.onOpen} className="ml-auto text-verified underline underline-offset-3">
                zobacz kampanię
              </button>
            )}
          </Row>
        )}
        {props.sources.map((src) => (
          <Row key={src.url} label="Źródło">
            <a href={src.url} target="_blank" rel="noopener noreferrer" className="text-[var(--host-link,var(--verified))] underline decoration-current/35 underline-offset-3 hover:decoration-current">
              {src.title}
            </a>
            <span className="ml-auto whitespace-nowrap text-muted-foreground">
              {src.domain}, {src.kind}
            </span>
          </Row>
        ))}
        {props.variant === "scam" && (
          <Row label="Dowód" hint="Reklama może zniknąć za kilka godzin. Dowód zostaje i da się go wysłać do CERT Polska.">
            <span>
              Zapisany o <span className="font-mono">{props.evidence.savedAt}</span>: {props.evidence.summary}
            </span>
          </Row>
        )}
        {props.technique && (
          <Row label="Technika" hint={props.technique.howToSpot}>
            <span>{props.technique.name}</span>
            <span className="ml-auto text-muted-foreground">jak rozpoznać?</span>
          </Row>
        )}
      </dl>

      {props.variant !== "scam" && <Consensus {...props.consensus} />}

      <footer className="flex flex-wrap items-center gap-2 px-3.5 pt-3 pb-3.5">
        {props.variant === "scam" ? (
          <>
            <Button size="sm" className="rounded-[var(--host-button-radius,var(--radius-pill))]" onClick={props.onHide}>
              Ukryj reklamę
            </Button>
            <Button size="sm" variant="outline" className="rounded-[var(--host-button-radius,var(--radius-pill))]" onClick={props.onReportToPlatform}>
              Zgłoś platformie
            </Button>
            <Hint text="Każde ostrzeżenie można zakwestionować. Trafia wtedy do ponownej oceny przez ludzi." align="end">
              <button type="button" onClick={props.onDispute} className="ml-auto text-meta text-muted-foreground underline underline-offset-3">
                To pomyłka?
              </button>
            </Hint>
          </>
        ) : (
          (["helpful", "unhelpful"] as const).map((v) => (
            <Button
              key={v}
              size="sm"
              variant={props.vote === v ? "default" : "outline"}
              aria-pressed={props.vote === v}
              className="rounded-[var(--host-button-radius,var(--radius-pill))]"
              onClick={() => props.onVote?.(v)}
            >
              {v === "helpful" ? "Pomocne" : "Niepomocne"}
            </Button>
          ))
        )}
      </footer>
    </section>
  )
}

function Row({ label, hint, children }: { label: string; hint?: string; children: ReactNode }) {
  const row = (
    <div tabIndex={hint ? 0 : undefined} className="flex items-baseline gap-2.5 border-b border-border/70 py-1.5">
      <dt className="w-16 shrink-0 text-meta text-muted-foreground">{label}</dt>
      <dd className="flex min-w-0 flex-1 items-baseline gap-2">{children}</dd>
    </div>
  )
  return hint ? <Hint text={hint}>{row}</Hint> : row
}

function Consensus({ a, b, thresholdPct }: { a: GroupScore; b: GroupScore; thresholdPct: number }) {
  const bar = (g: GroupScore, side: "left" | "right") => (
    <div className="relative h-1.5 overflow-hidden rounded-full bg-secondary">
      <div
        className={cn("animate-grow-x absolute inset-y-0 rounded-full bg-verified", side === "left" ? "right-0 origin-right" : "left-0 origin-left")}
        style={{ width: `${g.helpfulPct}%` }}
      />
      <div className="absolute inset-y-0 w-0.5 bg-foreground" style={side === "left" ? { right: `${thresholdPct}%` } : { left: `${thresholdPct}%` }} />
    </div>
  )
  return (
    <Hint text={`Obie grupy muszą przekroczyć próg ${thresholdPct}% ocen „pomocne”. Głosy kont z klastrów botów nie są liczone.`}>
      <div tabIndex={0} className="cursor-help px-3.5 pt-2.5">
        <p className="mb-1.5 font-sans text-small font-semibold">Zatwierdzone przez różne perspektywy</p>
        <div className="grid grid-cols-[1fr_2px_1fr] items-center gap-1.5">
          {bar(a, "left")}
          <span className="h-4 rounded-[1px] bg-foreground" />
          {bar(b, "right")}
        </div>
        <div className="mt-1.5 flex justify-between text-meta text-muted-foreground">
          <span>
            {a.label}: {a.helpfulPct}% pomocne, <span className="font-mono">{a.ratings}</span> ocen
          </span>
          <span>
            {b.label}: {b.helpfulPct}%, <span className="font-mono">{b.ratings}</span> ocen
          </span>
        </div>
      </div>
    </Hint>
  )
}

function Hint({ text, children, align = "center" }: { text: string; children: ReactNode; align?: "start" | "center" | "end" }) {
  return (
    <Tooltip>
      <TooltipTrigger asChild>{children}</TooltipTrigger>
      <TooltipContent align={align} className="max-w-64 text-pretty">
        {text}
      </TooltipContent>
    </Tooltip>
  )
}
