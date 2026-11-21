# QuickReportPopover

Poza zakresem konkursu MSZ: komponent został z wcześniejszej wersji produktu (wątek NASK i notatek społeczności) i nie jest używany w demo. Opis poniżej dotyczy tamtej wersji.

Przycisk „Zgłoś” wstrzykiwany w pasek akcji posta i okienko szybkiego zgłoszenia, które z niego wyrasta.

- **Kolejność:** przełącznik Manipulacja / Oszustwo (reklamy sponsorowane otwierają się na Oszustwo), pigułki powodów (wiele naraz), opis własnymi słowami, link do źródła (opcjonalny), informacja o automatycznym dowodzie, przycisk.
- **Wyślij** jest aktywny, gdy wybrano powód albo wpisano co najmniej 3 znaki.
- **Wysyłanie:** pasek w kolorze verified wypełnia przycisk w ~0,9 s („Wysyłanie…”), potem „Wysłane”, okienko się zamyka, a przycisk w pasku akcji zmienia się na „Zgłoszono”.
- **Błąd:** „Nie udało się wysłać. Sprawdź połączenie i spróbuj ponownie; twoje odpowiedzi zostały w formularzu.”
- **Klawiatura:** Esc zamyka i oddaje fokus przyciskowi „Zgłoś”.
- **Kod:** `components/meritum/quick-report-popover.tsx`.
