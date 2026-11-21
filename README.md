# Meritum Design System

**Meritum — obywatelski radar dezinformacji oraz scamu.** Design system, makiety i demo na HackNation 2026 (konkursy MSZ „Prawdowid” i NASK „Kolekcjoner fejków”).

## Od czego zacząć

- [DESIGN_SYSTEM.md](DESIGN_SYSTEM.md): specyfikacja dla całego zespołu i dla agentów AI (kolory, typografia, logo, komponenty, ton). Sekcja 12 to gotowe polecenie do wklejenia.
- [PRODUCT.md](PRODUCT.md): kim są użytkownicy, co robi produkt, zasady.
- [KEY_SELLING_POINTS.md](KEY_SELLING_POINTS.md): jak wygrać oba konkursy jednym produktem.

## Zawartość

Kto czego używa (wtyczka, backend, panel, prezentacje, pokaz): sekcja 13 w [DESIGN_SYSTEM.md](DESIGN_SYSTEM.md).

| Ścieżka | Co |
|---|---|
| `tokens/meritum.css` | tokeny CSS i `@theme` dla Tailwind v4 + shadcn/ui, tryb ciemny, skórki platform |
| `components/meritum/` | komponenty React (shadcn/ui): karta kontekstu, szybkie zgłoszenie, pasek analizy, telemetria ataku botów, widok kampanii |
| `contracts/`, `copy/pl.json` | kontrakty danych (Pydantic, JSON Schema, TypeScript) i teksty interfejsu |
| `extension/` | zestaw wtyczki Chrome: style Shadow DOM, skrypt referencyjny MV3, popup, onboarding, ikony |
| `brand/` | logo (SVG, PNG, logotyp) |
| `presentation/` | szablon PPTX, slajdy HTML, zrzuty demo, grafiki social |
| `demo/live/` | makiety platform z pełnym przepływem Meritum na pokaz |
| `demo/platforms/` | czyste makiety platform + `SELECTORS.md` dla wtyczki |
| `demo/x/`, `demo/widgets/`, `demo/logo/` | demo na X, widżety i ich stany, warianty logo |
| `docs/` | dokument produktowy: user stories, feature'y, ADR |
| `artifact/` | pliki opublikowanego Design System artifactu |

## Podgląd lokalnie

```bash
python3 -m http.server 52990 --bind 127.0.0.1
```

Potem otwórz http://localhost:52990/demo/live/ (makiety na pokaz) albo http://localhost:52990/demo/x/. Skróty: R reset, T motyw, Esc zamyka okno.

Wszystkie liczby, konta i osoby w makietach są fikcyjne i oznaczone jako dane przykładowe.
