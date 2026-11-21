# Meritum Design System

**Meritum — obywatelski radar dezinformacji.** Design system, kontrakty danych, makiety i demo na HackNation 2026 w konkursie MSZ „Prawdowid”: obywatel wkleja tekst albo link (formularz WWW) lub klika „Sprawdź” pod postem (wtyczka) i dostaje werdykt dla każdego twierdzenia z dosłownymi cytatami ze źródeł.

## Od czego zacząć

- [DESIGN_SYSTEM.md](DESIGN_SYSTEM.md): specyfikacja dla całego zespołu i dla agentów AI (kolory, typografia, logo, komponenty, ton). Sekcja 12 to gotowe polecenie do wklejenia.
- [PRODUCT.md](PRODUCT.md): kim są użytkownicy, co robi produkt, zasady.
- [KEY_SELLING_POINTS.md](KEY_SELLING_POINTS.md): jak odpowiadamy na wymagania konkursu MSZ i co pokazujemy na demo.
- [docs/product-doc.html](docs/product-doc.html): dokument produktowy: historie użytkowników, funkcje, decyzje architektoniczne (ADR).

## Zawartość

Kto czego używa (wtyczka, backend, panel, prezentacje, pokaz): sekcja 13 w [DESIGN_SYSTEM.md](DESIGN_SYSTEM.md).

| Ścieżka | Co |
|---|---|
| `tokens/meritum.css` | tokeny CSS i `@theme` dla Tailwind v4 + shadcn/ui, tryb ciemny, skórki platform |
| `components/meritum/` | komponenty React (shadcn/ui): karta wyniku (`ContextCard`), pasek postępu sprawdzenia (`AnalysisSteps`), znak. Z poprzedniego zakresu (NASK, konsensus) zostały `QuickReportPopover`, `BotDefenseTelemetry` i `CampaignRotation`: nie są częścią produktu dla MSZ |
| `contracts/` | kontrakty danych (Pydantic, JSON Schema, TypeScript): zapytanie, werdykty, cytaty z przesłankami, katalog źródeł, sprawa moderatora, zapis przebiegu sprawdzenia |
| `copy/pl.json` | teksty interfejsu: werdykty, statusy, kroki sprawdzenia, techniki manipulacji, błędy |
| `extension/` | zestaw wtyczki Chrome (drugi kanał): style Shadow DOM, skrypt referencyjny MV3, popup, onboarding, ikony |
| `brand/` | logo (SVG, PNG, logotyp) |
| `presentation/` | szablon PPTX, slajdy HTML, zrzuty demo, grafiki social |
| `demo/live/` | makiety platform z przepływem Meritum na pokaz |
| `demo/platforms/` | czyste makiety platform + `SELECTORS.md` dla wtyczki |
| `demo/x/`, `demo/widgets/`, `demo/logo/` | demo na X, widżety i ich stany, warianty logo |
| `docs/` | dokument produktowy: historie użytkowników, funkcje, ADR |
| `artifact/` | pliki opublikowanego Design System artifactu |

Makiety, wtyczka i część komponentów pokazują jeszcze poprzedni przepływ („Zgłoś”, notatka społeczności, ostrzeżenie o fałszywej reklamie). Docelowy kształt danych opisują `contracts/` i `copy/pl.json`.

## Podgląd online

https://meritum-demo.pages.dev, za Cloudflare Access: logowanie jednorazowym kodem wysłanym na e-mail z listy zespołu. Nową wersję wdraża `scripts/deploy-demo.sh` (wymaga `wrangler login`).

## Podgląd lokalnie

```bash
python3 -m http.server 52990 --bind 127.0.0.1
```

Potem otwórz http://localhost:52990/demo/live/ (makiety na pokaz) albo http://localhost:52990/demo/x/. Skróty: R reset, T motyw, Esc zamyka okno.

Kontrakty i typy po zmianie w `contracts/meritum_contracts.py`:

```bash
contracts/generate.sh
```

Wszystkie liczby, konta i osoby w makietach są fikcyjne i oznaczone jako dane przykładowe.
