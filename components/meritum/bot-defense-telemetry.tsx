import { CartesianGrid, Line, LineChart, ReferenceArea, ReferenceLine, XAxis, YAxis } from "recharts"

import { type ChartConfig, ChartContainer, ChartTooltip, ChartTooltipContent } from "@/components/ui/chart"
import { cn } from "@/lib/utils"

export interface VoteMinute {
  /** "HH:MM" */
  t: string
  counted: number
  rejected: number
}

export interface RejectedAccount {
  at: string
  handle: string
  /** Plain words, e.g. "ten sam klaster", "rytm 1 głos/s", "konto ma 2 dni". */
  reason: string
}

export interface BotDefenseTelemetryProps {
  noteId: string
  clusterSize: number
  series: VoteMinute[]
  attack: { from: string; to?: string }
  /** Did the note's status change during the attack? The title answers this question. */
  statusChanged: boolean
  rejectedAccounts: RejectedAccount[]
  simulated?: boolean
  className?: string
}

const chartConfig = {
  counted: { label: "Liczone: realne osoby", color: "var(--chart-1)" },
  rejected: { label: "Odrzucone: klaster kont", color: "var(--chart-2)" },
} satisfies ChartConfig

const fmt = (n: number) => n.toLocaleString("pl-PL")

/** Bot Defense Telemetry: one question ("did the attack change the result?"), one chart, a sum that closes, and the rejected accounts as a table. */
export function BotDefenseTelemetry({ noteId, clusterSize, series, attack, statusChanged, rejectedAccounts, simulated = true, className }: BotDefenseTelemetryProps) {
  // Totals come from the rows, so the sum line always closes.
  const counted = series.reduce((s, r) => s + r.counted, 0)
  const rejected = series.reduce((s, r) => s + r.rejected, 0)
  const end = attack.to ?? series.at(-1)?.t

  return (
    <section className={cn("rounded-lg border border-border bg-card font-sans text-card-foreground", className)} aria-labelledby="bdt-title">
      <header className="px-4 pt-4">
        <h2 id="bdt-title" className="flex items-center gap-2.5 text-title font-bold tracking-tight">
          {!statusChanged && <FrontMark />}
          {statusChanged ? "Atak zmienił status notatki" : "Atak odparty, notatka bez zmian"}
        </h2>
        <p className="mt-1 text-small text-muted-foreground">
          Klaster {fmt(clusterSize)} kont głosuje na notatkę <span className="font-mono">{noteId}</span> od <span className="font-mono">{attack.from}</span>.{" "}
          {statusChanged ? "Sprawdź oceny ręcznie." : "Żaden z jego głosów nie trafił do konsensusu."}
        </p>
      </header>

      <div className="px-2 pt-3">
        <ChartContainer config={chartConfig} className="aspect-auto h-64 w-full">
          <LineChart accessibilityLayer data={series} margin={{ left: 0, right: 96, top: 8 }}>
            <CartesianGrid vertical={false} strokeDasharray="0" />
            <XAxis dataKey="t" tickLine={false} axisLine={false} tickMargin={8} minTickGap={48} className="font-mono" />
            <YAxis tickLine={false} axisLine={false} width={36} className="font-mono" />
            <ReferenceArea x1={attack.from} x2={end} fill="var(--scam-surface)" fillOpacity={0.6} />
            <ReferenceLine x={attack.from} stroke="var(--scam)" strokeWidth={1.5} label={{ value: `front ${attack.from}`, position: "insideBottomRight", fill: "var(--scam-foreground)", fontSize: 12, fontWeight: 700 }} />
            <ChartTooltip content={<ChartTooltipContent indicator="line" />} />
            <Line dataKey="counted" type="linear" stroke="var(--color-counted)" strokeWidth={2} dot={false} isAnimationActive />
            <Line dataKey="rejected" type="linear" stroke="var(--color-rejected)" strokeWidth={2} dot={false} isAnimationActive />
          </LineChart>
        </ChartContainer>
      </div>

      <p className="mx-4 flex flex-wrap items-baseline gap-2 border-y border-border/70 py-2.5 text-small text-muted-foreground">
        Oddane <b className="font-mono text-base text-foreground">{fmt(counted + rejected)}</b> = liczone{" "}
        <b className="font-mono text-base text-foreground">{fmt(counted)}</b> + odrzucone <b className="font-mono text-base text-scam">{fmt(rejected)}</b>
      </p>

      <table className="mx-4 my-2 w-[calc(100%-2rem)] text-small">
        <thead>
          <tr className="text-left text-meta text-muted-foreground">
            <th className="py-1 font-medium">Czas</th>
            <th className="py-1 font-medium">Odrzucone konto</th>
            <th className="py-1 text-right font-medium">Powód</th>
          </tr>
        </thead>
        <tbody>
          {rejectedAccounts.map((a) => (
            <tr key={`${a.at}-${a.handle}`} className="animate-rise border-t border-border/70">
              <td className="py-1.5 font-mono text-muted-foreground">{a.at}</td>
              <td className="py-1.5 font-mono text-scam line-through decoration-[1.5px]">{a.handle}</td>
              <td className="py-1.5 text-right text-muted-foreground">{a.reason}</td>
            </tr>
          ))}
        </tbody>
      </table>
      <footer className="flex justify-between px-4 pb-3 text-meta text-muted-foreground">
        <span>{simulated ? "Dane symulowane na potrzeby demo." : "Odrzucone głosy zostają w rejestrze z powodem."}</span>
        <span>
          Wszystkie konta: <span className="font-mono">{fmt(clusterSize)}</span>
        </span>
      </footer>
    </section>
  )
}

/** Weather-front glyph: the signature of the attack onset. */
function FrontMark() {
  return (
    <svg viewBox="0 0 30 12" className="h-3 w-7.5 shrink-0" aria-hidden="true">
      <path d="M0 11H30" stroke="var(--scam)" strokeWidth={1.6} />
      <path d="M1 11l4.5-7 4.5 7zM11 11l4.5-7 4.5 7zM21 11l4.5-7 4.5 7z" fill="var(--scam)" />
    </svg>
  )
}
