import { cn } from "@/lib/utils"

import { MeritumMark } from "./meritum-mark"

export interface AnalysisStep {
  label: string
  status: "pending" | "active" | "done"
}

/** Processing strip shown under a post between "Wysłane" and the published note or warning. Drive `steps` from the DBOS workflow status. */
export function AnalysisSteps({ steps, className }: { steps: AnalysisStep[]; className?: string }) {
  return (
    <div role="status" className={cn("animate-rise mt-3 rounded-[var(--host-radius,var(--radius))] border border-border bg-card px-3.5 py-3 font-sans", className)}>
      <p className="flex items-center gap-1.5 text-meta font-semibold text-muted-foreground">
        <MeritumMark className="size-3.5" />
        Meritum analizuje zgłoszenie
      </p>
      <ol className="mt-2 grid gap-1.5">
        {steps.map((s) => (
          <li key={s.label} className={cn("flex items-center gap-2.5 text-small transition-colors", s.status === "pending" ? "text-muted-foreground" : "text-foreground")}>
            <span
              aria-hidden="true"
              className={cn(
                "grid size-4 shrink-0 place-items-center rounded-full border-[1.5px]",
                s.status === "pending" && "border-border",
                s.status === "active" && "animate-spin border-verified border-t-transparent motion-reduce:animate-none",
                s.status === "done" && "border-verified bg-verified",
              )}
            >
              {s.status === "done" && (
                <svg viewBox="0 0 16 16" className="size-3 text-card">
                  <path d="M3.5 8.5l3 3 6-7" fill="none" stroke="currentColor" strokeWidth={2} strokeLinecap="round" strokeLinejoin="round" />
                </svg>
              )}
            </span>
            {s.label}
            <span className="sr-only">{s.status === "done" ? "gotowe" : s.status === "active" ? "w toku" : "czeka"}</span>
          </li>
        ))}
      </ol>
    </div>
  )
}
