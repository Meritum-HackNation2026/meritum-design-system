import { useId, useState } from "react"

import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Popover, PopoverContent, PopoverTrigger } from "@/components/ui/popover"
import { Textarea } from "@/components/ui/textarea"
import { cn } from "@/lib/utils"

import { MeritumMark } from "../meritum/meritum-mark"

export type ReportKind = "manipulation" | "scam"

export interface ReportPayload {
  kind: ReportKind
  reasons: string[]
  note: string
  sourceUrl: string | null
}

const REASONS: Record<ReportKind, readonly string[]> = {
  manipulation: ["Fałszywa informacja", "Teoria spiskowa", "Wyrwane z kontekstu", "Fałszywy autorytet", "Zmanipulowane zdjęcie lub wideo"],
  scam: ["Fałszywy wizerunek znanej osoby", "Podejrzana inwestycja", "Podszywanie się pod bank lub urząd", "Fałszywy sklep lub zbiórka"],
}

type SendState = "idle" | "sending" | "sent"

export interface QuickReportPopoverProps {
  /** Handle shown in the header, e.g. "@prawda_o_ziemi". */
  targetHandle: string
  /** Sponsored posts open on the scam tab. */
  defaultKind?: ReportKind
  /** Resolve when the API accepted the report; reject to show an error. */
  onSubmit: (payload: ReportPayload) => Promise<void>
  /** Called after the success animation, when the popover has closed. */
  onReported?: () => void
  reported?: boolean
}

/** Quick Report Popover: the "Zgłoś" button injected into the host action bar plus its form. */
export function QuickReportPopover({ targetHandle, defaultKind = "manipulation", onSubmit, onReported, reported = false }: QuickReportPopoverProps) {
  const [open, setOpen] = useState(false)
  const [kind, setKind] = useState<ReportKind>(defaultKind)
  const [reasons, setReasons] = useState<string[]>([])
  const [note, setNote] = useState("")
  const [sourceUrl, setSourceUrl] = useState("")
  const [state, setState] = useState<SendState>("idle")
  const [error, setError] = useState<string | null>(null)
  const ids = { note: useId(), url: useId() }

  const canSend = state === "idle" && (reasons.length > 0 || note.trim().length >= 3)
  const toggle = (r: string) => setReasons((cur) => (cur.includes(r) ? cur.filter((x) => x !== r) : [...cur, r]))

  async function send() {
    setState("sending")
    setError(null)
    try {
      await onSubmit({ kind, reasons, note: note.trim(), sourceUrl: sourceUrl.trim() || null })
      setState("sent")
      setTimeout(() => {
        setOpen(false)
        onReported?.()
      }, 650)
    } catch {
      setState("idle")
      setError("Nie udało się wysłać. Sprawdź połączenie i spróbuj ponownie; twoje odpowiedzi zostały w formularzu.")
    }
  }

  return (
    <Popover open={open} onOpenChange={setOpen}>
      <PopoverTrigger asChild>
        <button
          type="button"
          disabled={reported}
          className={cn(
            "inline-flex h-8.5 items-center gap-1.5 rounded-full px-2.5 font-sans text-small font-semibold transition-colors",
            "hover:bg-verified-surface hover:text-verified-foreground aria-expanded:bg-verified-surface aria-expanded:text-verified-foreground",
            reported && "text-verified-foreground",
          )}
        >
          <MeritumMark className="size-4.5" />
          {reported ? "Zgłoszono" : "Zgłoś"}
        </button>
      </PopoverTrigger>
      <PopoverContent align="end" className="w-89 rounded-xl p-0 font-sans shadow-float">
        <div className="flex items-center gap-2 px-4 pt-3.5">
          <MeritumMark className="size-5" />
          <div>
            <p className="text-base font-bold">Zgłoś treść</p>
            <p className="text-meta text-muted-foreground">Post {targetHandle}</p>
          </div>
        </div>
        <form
          className="grid gap-3 px-4 pt-3 pb-4"
          onSubmit={(e) => {
            e.preventDefault()
            if (canSend) void send()
          }}
        >
          <fieldset className="grid grid-cols-2 rounded-[10px] bg-muted p-0.75">
            <legend className="sr-only">Rodzaj zgłoszenia</legend>
            {(["manipulation", "scam"] as const).map((k) => (
              <label
                key={k}
                className="relative cursor-pointer rounded-lg py-1.75 text-center text-small font-semibold text-muted-foreground has-checked:bg-card has-checked:text-foreground has-checked:shadow-xs has-focus-visible:outline-2 has-focus-visible:outline-ring"
              >
                <input
                  type="radio"
                  name="report-kind"
                  value={k}
                  checked={kind === k}
                  onChange={() => {
                    setKind(k)
                    setReasons([])
                  }}
                  className="absolute inset-0 cursor-pointer opacity-0"
                />
                {k === "manipulation" ? "Manipulacja" : "Oszustwo"}
              </label>
            ))}
          </fieldset>

          <fieldset>
            <legend className="mb-1.5 text-small font-semibold">Co jest nie tak? Wybierz jedno lub więcej</legend>
            <div className="flex flex-wrap gap-1.5">
              {REASONS[kind].map((r) => (
                <button
                  key={r}
                  type="button"
                  aria-pressed={reasons.includes(r)}
                  onClick={() => toggle(r)}
                  className="rounded-full border border-border px-2.75 py-1.5 text-small transition-colors hover:border-muted-foreground active:scale-97 aria-pressed:border-primary aria-pressed:bg-primary aria-pressed:text-primary-foreground"
                >
                  {r}
                </button>
              ))}
            </div>
          </fieldset>

          <div className="grid gap-1.5">
            <Label htmlFor={ids.note}>Albo opisz własnymi słowami</Label>
            <Textarea id={ids.note} rows={2} value={note} onChange={(e) => setNote(e.target.value)} placeholder="Np. to nagranie jest z 2019 roku" className="resize-none" />
          </div>
          <div className="grid gap-1.5">
            <Label htmlFor={ids.url}>Link do źródła (opcjonalnie)</Label>
            <Input id={ids.url} type="url" inputMode="url" value={sourceUrl} onChange={(e) => setSourceUrl(e.target.value)} placeholder="https://" />
          </div>
          <p className="text-meta text-muted-foreground">Dowód zapiszemy sami: zrzut ekranu, adres i czas. Zgłoszenie jest anonimowe.</p>
          {error && (
            <p role="alert" className="text-small text-scam-foreground">
              {error}
            </p>
          )}

          <Button type="submit" disabled={!canSend && state === "idle"} className="relative h-10.5 overflow-hidden rounded-[10px] font-bold" aria-live="polite">
            <span
              aria-hidden="true"
              className={cn(
                "absolute inset-0 origin-left bg-verified transition-transform duration-900 ease-(--ease-out-meritum)",
                state === "idle" ? "scale-x-0" : "scale-x-100",
              )}
            />
            <span className="relative">{state === "idle" ? "Wyślij zgłoszenie" : state === "sending" ? "Wysyłanie…" : "Wysłane"}</span>
          </Button>
        </form>
      </PopoverContent>
    </Popover>
  )
}
