# Meritum Design System

**Meritum — obywatelski radar dezinformacji oraz scamu.** Design system, makiety i demo na HackNation 2026 (konkursy MSZ „Prawdowid” i NASK „Kolekcjoner fejków”).

## Od czego zacząć

- [DESIGN_SYSTEM.md](DESIGN_SYSTEM.md): specyfikacja dla całego zespołu i dla agentów AI (kolory, typografia, logo, komponenty, ton). Sekcja 12 to gotowe polecenie do wklejenia.
- [PRODUCT.md](PRODUCT.md): kim są użytkownicy, co robi produkt, zasady.
- [KEY_SELLING_POINTS.md](KEY_SELLING_POINTS.md): jak wygrać oba konkursy jednym produktem.

## Zawartość

| Ścieżka | Co |
|---|---|
| `tokens/meritum.css` | tokeny CSS i `@theme` dla Tailwind v4 + shadcn/ui, tryb ciemny, skórki platform |
| `components/meritum/` | komponenty React (shadcn/ui): karta kontekstu, szybkie zgłoszenie, pasek analizy, telemetria ataku botów |
| `brand/` | logo (SVG) |
| `demo/x/` | interaktywne demo: zgłoszenie, analiza, notatka i ostrzeżenie na makiecie X |
| `demo/widgets/` | widżet na 5 platformach i wszystkie jego stany |
| `demo/logo/` | warianty znaku (wybrany: B „Dwa łuki”) |
| `demo/platforms/` | makiety X, Facebooka, Instagrama, Reddita i TikToka do pokazu na żywo + `SELECTORS.md` dla wtyczki |
| `artifact/` | pliki opublikowanego Design System artifactu |

## Podgląd lokalnie

```bash
python3 -m http.server 52990 --bind 127.0.0.1
```

Potem otwórz http://localhost:52990/demo/x/ (skróty w demo: R reset, T motyw, Esc zamyka okno).

Wszystkie liczby, konta i osoby w makietach są fikcyjne i oznaczone jako dane przykładowe.
