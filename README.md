# Meritum Design System

**Meritum — obywatelski radar dezinformacji.** Design system, kontrakty danych, makiety i demo na HackNation 2026 w konkursie MSZ „Prawdowid”: obywatel wkleja tekst albo link (formularz WWW), wysyła go botowi na Discordzie albo klika „Sprawdź” pod postem (wtyczka) i dostaje werdykt dla każdego twierdzenia z dosłownymi cytatami ze źródeł.

## Od czego zacząć

- [DESIGN_SYSTEM.md](DESIGN_SYSTEM.md): specyfikacja dla całego zespołu i dla agentów AI (kolory, typografia, logo, komponenty, ton). Sekcja 12 to gotowe polecenie do wklejenia.
- [PRODUCT.md](PRODUCT.md): kim są użytkownicy, co robi produkt, zasady.
- [KEY_SELLING_POINTS.md](KEY_SELLING_POINTS.md): jak odpowiadamy na wymagania konkursu MSZ i co pokazujemy na demo.
- [docs/product-doc.html](docs/product-doc.html): dokument produktowy dla zespołu i agentów AI: historie użytkowników, funkcje, decyzje architektoniczne (ADR), prawa autorskie i licencje, ewidencja źródeł, słownik pojęć, wiadomość do mentorów i fakty do potwierdzenia.

## Zawartość

Kto czego używa (wtyczka, backend, panel, prezentacje, pokaz): sekcja 13 w [DESIGN_SYSTEM.md](DESIGN_SYSTEM.md).

| Ścieżka | Co |
|---|---|
| `tokens/meritum.css` | tokeny CSS i `@theme` dla Tailwind v4 + shadcn/ui, tryb ciemny, skórki platform |
| `components/meritum/` | komponenty React (shadcn/ui) typowane kontraktami: formularz, historia, przycisk „Sprawdź”, pasek analizy, karta wyniku, kolejka moderatorów. Komponenty z poprzedniego zakresu (NASK, notatki) są w `components/legacy/` i nie należą do produktu dla MSZ |
| `contracts/` | kopia kontraktów danych z meritum-core, odświeżana skryptem `sync.sh` (JSON Schema, TypeScript, przykłady): zapytanie, werdykty, cytaty z przesłankami, katalog źródeł, sprawa moderatora, zapis przebiegu sprawdzenia, powiadomienie. Źródłem prawdy jest repozytorium meritum-core; design system korzysta z wygenerowanych JSON Schema i typów TS |
| `copy/pl.json` | teksty interfejsu: werdykty, statusy, kroki sprawdzenia, techniki manipulacji, historia sprawdzeń, logowanie obywatela i personelu, administracja kontami i tematami, link jury, przesyłanie nagrania, SMS, Discord, informacja o AI, prywatność kanałów, panel moderatora, powiadomienia, strona ewaluacji, błędy, kody awarii i ograniczeń, „co zmieniłoby werdykt”, podstawa dopasowania. Test `tests/test_copy.py` pilnuje wymaganych kluczy i tonu, a `tests/test_contract_copy.py` sprawdza, czy każdy kod z `contracts/meritum.schema.json` ma tekst |
| `copy/privacy.json` | polityki prywatności strony, Discorda, wtyczki i SMS oraz rejestr podmiotów przetwarzających (ADR-14), wspólne dla frontendu, bota i README. Test `tests/test_privacy.py` pilnuje sekcji polityk, rejestru i tonu |
| `extension/` | zestaw wtyczki Chrome (kanał dodatkowy; drugim kanałem jest bot na Discordzie): style Shadow DOM, skrypt referencyjny MV3, popup, onboarding, ikony |
| `brand/` | logo (SVG, PNG, logotyp) |
| `presentation/` | szablon PPTX, slajdy HTML, zrzuty demo, grafiki social |
| `demo/live/` | makiety platform z przepływem Meritum na pokaz |
| `demo/platforms/` | czyste makiety platform + `SELECTORS.md` dla wtyczki |
| `demo/widgets/`, `demo/logo/` | karta wyniku w skórkach platform, warianty logo |
| `docs/` | dokument produktowy: historie użytkowników, funkcje, ADR |
| `artifact/` | pliki opublikowanego Design System artifactu |

Komponenty, wtyczka i makiety pokazują przepływ „Sprawdź” z kontraktów (`contracts/`) i tekstami z `copy/pl.json`. Wtyczka i makiety wołają jeszcze atrapę API (`extension/reference/api.js`). Slajdy i grafiki w `presentation/` pokazują jeszcze produkt sprzed zmiany zakresu.

## Teksty ekranów logowania, administracji, linku jury i nagrania

Z tych kluczy w `copy/pl.json` korzystają zgłoszenia frontendu:

| Klucze | Zgłoszenie |
|---|---|
| `account.*` (logowanie i wylogowanie obywatela) | [meritum-frontend#28](https://github.com/Meritum-HackNation2026/meritum-frontend/issues/28), frontend/017 |
| `staff.sign_in.*` (logowanie personelu do panelu) | [meritum-frontend#24](https://github.com/Meritum-HackNation2026/meritum-frontend/issues/24), frontend/010 |
| `staff.admin.*` (konta personelu i tematy wysokiego ryzyka) | [meritum-frontend#31](https://github.com/Meritum-HackNation2026/meritum-frontend/issues/31), frontend/021 |
| `jury.*` (wejście z jednorazowego linku jury) | [meritum-frontend#27](https://github.com/Meritum-HackNation2026/meritum-frontend/issues/27), frontend/011 |
| `form.audio_*`, `errors.audio_*` (przesyłanie nagrania; nieobsługiwany format to istniejący `status_hint.out_of_scope_audio_format`) | [meritum-frontend#22](https://github.com/Meritum-HackNation2026/meritum-frontend/issues/22), frontend/007 |
| `method.*` (strona „Jak działa Meritum”: metoda, katalog źródeł, mierniki, poprawki, „Zgłoś błąd”, pilotaż; tytuł to `result.how_it_works`) | [meritum-frontend#20](https://github.com/Meritum-HackNation2026/meritum-frontend/issues/20), frontend/012 |

Testy kluczy, polityk prywatności i tonu (sekcja 8 w DESIGN_SYSTEM.md) uruchamia CI (`.github/workflows/copy.yml`), a lokalnie:

```bash
python3 -m unittest discover -s tests
```

## Podgląd online

https://meritum-demo.pages.dev, za Cloudflare Access: logowanie jednorazowym kodem wysłanym na e-mail z listy zespołu. Nową wersję wdraża `scripts/deploy-demo.sh` (wymaga `wrangler login`).

## Podgląd lokalnie

```bash
python3 -m http.server 52990 --bind 127.0.0.1
```

Potem otwórz http://localhost:52990/demo/live/ (makiety na pokaz) albo http://localhost:52990/demo/widgets/. Skróty na makietach: R reset, T motyw.

Wdrożone makiety platform (te same strony co `demo/platforms/`, z repo [meritum-mocks](https://github.com/Meritum-HackNation2026/meritum-mocks)) są pod https://meritum-x.gburek.app, https://meritum-facebook.gburek.app, https://meritum-instagram.gburek.app, https://meritum-reddit.gburek.app i https://meritum-tiktok.gburek.app. Makiety wdrażają się tylko z `main`, więc nie mają już aktualnej wersji dev.

Kontrakty zmienia się w [meritum-core](https://github.com/Meritum-HackNation2026/meritum-core) (pakiet `src/meritum_core/checks/contracts/`), nie tutaj. Po zmianie kontraktów na gałęzi main workflow `bump-dependents.yml` w meritum-core otwiera tu PR z odświeżoną kopią (ADR-33). Ręcznie kopię w `contracts/` odświeża:

```bash
contracts/sync.sh
```

Skrypt zapisuje commit core w `contracts/SOURCE` i sumy w `contracts/SHA256SUMS`; CI (`.github/workflows/contracts.yml`) odrzuca ręczne zmiany kopii.

Wszystkie liczby, konta i osoby w makietach są fikcyjne i oznaczone jako dane przykładowe.
