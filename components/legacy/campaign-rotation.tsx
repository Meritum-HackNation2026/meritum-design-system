import { Tooltip, TooltipContent, TooltipTrigger } from "@/components/ui/tooltip"
import { cn } from "@/lib/utils"

export interface CampaignDomainRow {
  domain: string
  state: "active" | "dead" | "predicted"
  /** ISO dates; `to` absent = still running (active) or not started (predicted). */
  from: string
  to?: string
  ads: number
  note?: string
}

export interface CampaignRotationProps {
  id: string
  title: string
  adsByPlatform: Record<string, number>
  domains: CampaignDomainRow[]
  sharedTraces: { label: string; ads: number }[]
  /** Window shown on the time axis. */
  window: { from: string; to: string }
  /** Collapse older dead domains into one "+N domen wcześniej" row. */
  maxRows?: number
  simulated?: boolean
  onExport?: () => void
  className?: string
}

const PLATFORM_LABEL: Record<string, string> = { facebook: "Facebook", instagram: "Instagram", x: "X", reddit: "Reddit", tiktok: "TikTok" }
const fmt = (n: number) => n.toLocaleString("pl-PL")
const day = (iso: string) => new Date(iso).toLocaleDateString("pl-PL", { day: "2-digit", month: "2-digit" })

/**
 * Campaign view (NASK "Kolekcjoner fejków"): one sighting, the whole operation.
 * Rows are domains, bars are their lifetimes; dead = grey, active = scam red, predicted (from CT logs) = dashed.
 */
export function CampaignRotation({ id, title, adsByPlatform, domains, sharedTraces, window, maxRows = 12, simulated = true, onExport, className }: CampaignRotationProps) {
  const t0 = Date.parse(window.from)
  const span = Date.parse(window.to) - t0
  const pos = (iso: string) => Math.min(100, Math.max(0, ((Date.parse(iso) - t0) / span) * 100))
  const now = pos(new Date().toISOString())

  const sorted = [...domains].sort((a, b) => Date.parse(a.from) - Date.parse(b.from))
  const hidden = Math.max(0, sorted.length - maxRows)
  const rows = sorted.slice(hidden)
  const total = Object.values(adsByPlatform).reduce((s, n) => s + n, 0) // the sum on screen always closes
  const active = domains.filter((d) => d.state === "active").length
  const predicted = domains.filter((d) => d.state === "predicted").length
  const platforms = Object.entries(adsByPlatform).filter(([, n]) => n > 0)

  return (
    <section aria-labelledby={`camp-${id}`} className={cn("rounded-lg border border-border bg-card font-sans text-card-foreground", className)}>
      <header className="px-4 pt-4">
        <h2 id={`camp-${id}`} className="text-title font-bold tracking-tight">
          Kampania <span className="font-mono">{id}</span>: {title}
        </h2>
        <p className="mt-1 text-small text-muted-foreground">
          {fmt(total)} reklam na {platforms.length} platformach i {domains.length} domen. Teraz działa {active}, {predicted} kolejne czekają w logach certyfikatów.
        </p>
      </header>

      <div className="px-4 pt-3">
        <div className="flex items-baseline justify-between">
          <h3 className="text-small font-bold">Rotacja domen</h3>
          <span className="text-meta text-muted-foreground">
            {day(window.from)}–{day(window.to)}
          </span>
        </div>
        <div className="relative mt-1.5">
          {hidden > 0 && (
            <div className="grid h-5 grid-cols-[11rem_1fr] items-center text-meta text-muted-foreground">
              <span className="font-mono">+{hidden} domen wcześniej</span>
              <span />
            </div>
          )}
          {rows.map((d) => {
            const left = pos(d.from)
            const right = d.to ? pos(d.to) : d.state === "predicted" ? Math.min(100, left + 6) : now
            return (
              <div key={d.domain} className="grid h-5 grid-cols-[11rem_1fr] items-center text-meta">
                <Tooltip>
                  <TooltipTrigger asChild>
                    <button
                      type="button"
                      className={cn(
                        "cursor-help truncate text-left font-mono",
                        d.state === "active" && "font-semibold text-foreground",
                        d.state === "dead" && "text-muted-foreground",
                        d.state === "predicted" && "text-scam-foreground",
                      )}
                    >
                      {d.domain}
                    </button>
                  </TooltipTrigger>
                  <TooltipContent align="start" className="max-w-64">
                    {d.note ?? (d.state === "predicted" ? "Przewidziana z logów certyfikatów, jeszcze bez reklam." : `${fmt(d.ads)} reklam.`)}
                  </TooltipContent>
                </Tooltip>
                    <span className="relative h-full">
                      <i
                        className={cn(
                          "animate-grow-x absolute top-1.5 h-2 origin-left rounded-[2px]",
                          d.state === "active" && "bg-scam",
                          d.state === "dead" && "bg-chart-4",
                          d.state === "predicted" && "top-1 h-3 border-[1.5px] border-dashed border-scam bg-transparent",
                        )}
                        style={{ left: `${left}%`, width: `${Math.max(1.5, right - left)}%` }}
                      />
                    </span>
              </div>
            )
          })}
          <span aria-hidden="true" className="absolute inset-y-0 w-px bg-foreground" style={{ left: `calc(11rem + (100% - 11rem) * ${now / 100})` }} />
        </div>
      </div>

      <p className="mx-4 mt-3 flex flex-wrap items-baseline gap-2 border-t border-border/70 py-2.5 text-small text-muted-foreground">
        Reklamy <b className="font-mono text-base text-foreground">{fmt(total)}</b> ={" "}
        {platforms.map(([p, n], i) => (
          <span key={p}>
            {i > 0 && "+ "}
            {PLATFORM_LABEL[p] ?? p} <b className="font-mono text-base text-foreground">{fmt(n)}</b>
          </span>
        ))}
      </p>

      <table className="mx-4 w-[calc(100%-2rem)] text-small">
        <thead>
          <tr className="text-left text-meta text-muted-foreground">
            <th className="py-1 font-medium">Wspólny ślad</th>
            <th className="py-1 text-right font-medium">Reklamy</th>
          </tr>
        </thead>
        <tbody>
          {sharedTraces.map((t) => (
            <tr key={t.label} className="border-t border-border/70">
              <td className="py-1.5">{t.label}</td>
              <td className="py-1.5 text-right font-mono">{fmt(t.ads)}</td>
            </tr>
          ))}
        </tbody>
      </table>

      <footer className="flex justify-between px-4 pt-2 pb-3 text-meta text-muted-foreground">
        <span>{simulated ? "Dane symulowane na potrzeby demo." : ""}</span>
        {onExport && (
          <button type="button" onClick={onExport} className="text-verified underline underline-offset-3">
            Eksport dowodów dla CERT
          </button>
        )}
      </footer>
    </section>
  )
}
