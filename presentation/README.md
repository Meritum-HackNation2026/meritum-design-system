# Meritum: zestaw do prezentacji i materiałów marketingowych

Ten folder jest dla osób, które robią slajdy, posty i grafiki o Meritum, a nie piszą kodu. Wszystko tutaj wygląda tak samo jak produkt: te same kolory, kroje pisma i logo. Zasady, z których to wynika, są w `../DESIGN_SYSTEM.md`, a treść pitchu w `../KEY_SELLING_POINTS.md`.

## Co jest w zestawie

| Plik | Do czego |
|---|---|
| `meritum-template.pptx` | szablon PowerPoint / Google Slides / Keynote, 10 gotowych slajdów |
| `slides/index.html` | ta sama prezentacja w przeglądarce, z notatkami prowadzącego |
| `screenshots/` | zrzuty demo: zgłoszenie, notatka, ostrzeżenie o oszustwie, widżet na 5 platformach |
| `social/` | obraz do linków (1200×630), post kwadratowy (1080×1080), story (1080×1920), baner LinkedIn (1584×396): pliki PNG gotowe do wrzucenia |
| `../brand/exports/` | logo w PNG (znak, ikona aplikacji, logo ze słowem „meritum”) |

### Które logo wziąć

| Plik w `brand/exports/` | Kiedy |
|---|---|
| `meritum-lockup-light@2x.png` | logo ze słowem „meritum” na jasnym tle |
| `meritum-lockup-subtitle-light@2x.png` | to samo z podtytułem, np. na pierwszym slajdzie |
| `meritum-lockup-dark@2x.png`, `meritum-lockup-subtitle-dark@2x.png` | na ciemnym tle |
| `meritum-mark-light-512.png` (lub `-1024`) | sam znak na jasnym tle |
| `meritum-mark-dark-512.png` | sam znak na ciemnym tle (na białym tle w podglądzie wygląda na pusty, to normalne) |
| `meritum-mark-mono-512.png` | druk jednobarwny |
| `meritum-app-icon-*.png` | avatar w mediach społecznościowych, ikona, favicon |

Pliki `.svg` obok to te same logotypy w wersji wektorowej (dla grafików).

## Szablon PPTX

Slajdy w szablonie (w tej kolejności): tytuł, problem, teza „Jeden fejk, cała kampania”, zrzuty demo, konsensus dwóch grup, kampania #K-118, atak botów, architektura, zespół i prośba, zamknięcie z hasłami. Każdy ma notatki prowadzącego.

**Najpierw kroje pisma.** Szablon używa Archivo (cały tekst) i Azeret Mono (tylko liczby, godziny, nazwy kont, domeny). Jeśli ich nie ma, program podstawi inny krój i tekst się rozjedzie.

- **Google Slides:** wgraj plik na Dysk Google, kliknij go dwukrotnie i wybierz „Otwórz w: Prezentacje Google”. Oba kroje są w Google Slides: menu czcionek → „Więcej czcionek” → wpisz „Archivo” i „Azeret Mono” → dodaj.
- **PowerPoint (Windows, Mac):** zainstaluj kroje z [fonts.google.com/specimen/Archivo](https://fonts.google.com/specimen/Archivo) i [fonts.google.com/specimen/Azeret+Mono](https://fonts.google.com/specimen/Azeret+Mono) (przycisk „Get font” → pobierz → otwórz pliki .ttf → „Zainstaluj”). Potem otwórz `meritum-template.pptx`.
- **Keynote:** zainstaluj kroje jak wyżej, potem Plik → Otwórz → `meritum-template.pptx`. Keynote może przesunąć tekst o kilka pikseli: przejrzyj każdy slajd.

**Jak pracować z szablonem**
- Zrób kopię pliku i pracuj na kopii.
- Nowy slajd = duplikat podobnego slajdu (prawy przycisk → „Duplikuj slajd”), potem podmień tekst. Nie zaczynaj od pustego slajdu.
- Wykres na slajdzie „Atak odparty” jest edytowalny: prawy przycisk → „Edytuj dane”. Jeśli zmienisz liczby, popraw też sumę pod wykresem, żeby się domykała (oddane = liczone + odrzucone).
- Na slajdzie „Zespół” wpisz imiona w miejsce „[Imię Nazwisko]”.
- Zrzuty możesz podmienić na nowe (prawy przycisk na obrazku → „Zmień obraz”), zachowując rozmiar.

## Prezentacja HTML i eksport do PDF

1. Otwórz `slides/index.html` w Chrome (dwuklik na pliku). Potrzebny jest internet, bo kroje ładują się z Google Fonts.
2. Strzałki ← → (albo spacja, klik) zmieniają slajdy. Klawisz **N** pokazuje notatki prowadzącego na dole ekranu. **F11** (Windows) lub **Ctrl+Cmd+F** (Mac) to pełny ekran.
3. **PDF:** Ctrl+P (Mac: Cmd+P) → Miejsce docelowe: „Zapisz jako PDF” → Więcej ustawień → Marginesy: „Brak”, zaznacz „Grafika tła” → Zapisz. Wychodzi 10 stron, jeden slajd na stronę, w formacie 16:9.

## Spójne zrzuty ekranu z demo

Zrzuty w `screenshots/` zrobiono automatycznie. Jeśli robisz nowe ręcznie, trzymaj się tych ustawień, żeby wyglądały tak samo:

- **Okno przeglądarki 1440 × 900**, powiększenie strony 100%, Chrome.
- **Tryb jasny** (w demo przycisk „Tryb jasny/ciemny” albo klawisz T). Jedna prezentacja = jeden tryb.
- Kursor odsuń od kart, żeby nie było podświetleń ani dymków.
- Demo na X: `http://localhost:52990/demo/x/` (serwer uruchamia ktoś z zespołu technicznego). Klawisz R zaczyna od nowa.

Które stany uchwycić:

| Plik | Co zrobić |
|---|---|
| `x-01-feed.png` | sam feed po otwarciu strony |
| `x-02-report-popover.png` | kliknij „Zgłoś” pod postem „Prawda o Ziemi”, zaznacz „Teoria spiskowa” |
| `x-03-analysis.png` | kliknij „Wyślij zgłoszenie”, po ok. 2,5 s widać pasek analizy z krokami |
| `x-04-context-note.png`, `x-04-card.png` | po ok. 5 s pod postem jest notatka „Kontekst od społeczności” |
| `x-05-scam-warning.png`, `x-05-card.png` | to samo z reklamą „Finanse Dziś”: „Zgłoś” → „Fałszywy wizerunek znanej osoby” → wyślij, odczekaj ok. 6 s |
| `widgets-*.png` | strona `http://localhost:52990/demo/widgets/`: ta sama karta na 5 platformach i wszystkie stany |

Dla zespołu technicznego: wszystkie PNG da się odtworzyć poleceniami z folderu `design-system/`:

```
uv run --with playwright python presentation/render.py shots    # zrzuty demo (serwer na porcie 52990)
uv run --with playwright python presentation/render.py brand    # logo w PNG
uv run --with playwright python presentation/render.py social   # grafiki do social mediów
uv run --with python-pptx python presentation/build_pptx.py     # szablon PPTX
```

## Rób tak / nie rób tak

| Rób tak | Nie rób tak |
|---|---|
| Jedna myśl na slajd, tytuł do dwóch linii: „Notatka wychodzi, gdy zgodzą się obie strony” | Trzy akapity i lista punktorów na jednym slajdzie |
| Tło `#F6F7F5`, białe karty z cienką szarą ramką | Gradienty, fiolet, neonowe poświaty, zielony tekst na czarnym tle |
| Czerwień `#C8213A` tylko przy oszustwie i ataku, zawsze ze słowem („Oszustwo”) albo znakiem frontu (linia z trzema trójkątami) | Czerwone nagłówki „dla uwagi”, czerwone tło całego slajdu |
| Prawdziwe zrzuty Meritum z `screenshots/` | Zdjęcia stockowe, ludzie przy laptopach, kłódki i tarcze |
| Liczby z demo z dopiskiem „dane symulowane” | „Wykrywamy 98% oszustw” albo każda liczba, której nie zmierzyliśmy |
| „Gotowe do integracji z CERT Polska” | „Współpracujemy z NASK / CERT Polska / MSZ”, dopóki to nieprawda |
| Fikcyjny prezenter „Tomasz Rewiński” i wymyślone domeny | Twarz albo nazwisko prawdziwej osoby jako oszusta |
| „Żaden przepis nie zakazuje płacenia gotówką w sklepach.” | „FAŁSZ! Ten post kłamie!” |
| Nagłówki zdaniowe: „Atak odparty, notatka bez zmian” | NAPISY WERSALIKAMI nad nagłówkami, emoji, wykrzykniki |
| Wykres z etykietą przy linii i sumą, która się domyka | Kafelki z ikoną i dużą liczbą, legenda daleko od linii |
| Logo w rogu, 24–32 px na slajdzie | Logo rozciągnięte, obrócone, z cieniem, obok logo platform |

## Gotowe polecenie dla AI (do nowych slajdów)

Wklej to do ChatGPT, Claude albo Gemini, a pod spodem napisz, jakiego slajdu potrzebujesz.

```
Robisz slajd (16:9, 1920×1080) dla Meritum — obywatelskiego radaru dezinformacji oraz scamu
(wtyczka do przeglądarki + panel analityka). Język: polski.

Styl „Biuletyn synoptyczny”: spokojnie, precyzyjnie, dużo powietrza. Jedna myśl na slajd,
tytuł zdaniowy do dwóch linii, krój Archivo 700 w rozmiarze 72 px lub większym.
Kolory: tło #F6F7F5, karty #FFFFFF z obramowaniem 1 px #D9DEDD, bez cieni,
tekst #14191E, tekst drugorzędny #4C5862, akcent i „zweryfikowane” #1D6A86,
„w ocenie” #B7791F, oszustwo i atak #C8213A (tylko tam, gdzie jest zagrożenie,
zawsze ze słowem albo znakiem frontu: linia z trzema trójkątami).
Kroje: Archivo do wszystkiego, Azeret Mono tylko do liczb, godzin, ID (#K-118), nazw kont i domen.
Logo Meritum (małe „m” z dwóch łuków) w lewym dolnym rogu, 30 px, obok słowo „meritum”.
Zamiast zdjęć: zrzuty interfejsu Meritum.
Wykresy: etykiety przy liniach, suma, która się domyka (np. „Oddane 6 016 = liczone 1 204 + odrzucone 4 812”).
Ton: kontekst, nie wyrok; każde twierdzenie ze źródłem; krótkie zdania w stronie czynnej.
Zakazane: gradienty, fiolet, neon, emoji, wykrzykniki, etykiety WERSALIKAMI nad nagłówkami,
siatki kart z ikonami, pasek koloru z boku karty, zdjęcia stockowe, prawdziwe osoby jako oszuści
(w przykładach fikcyjny prezenter „Tomasz Rewiński”), liczby bez dopisku „dane symulowane”,
twierdzenia o współpracy z NASK, CERT Polska lub MSZ (piszemy „gotowe do integracji z…”).
Hasła, których możesz użyć: „Jeden fejk, cała kampania. Jeden kontekst, ponad podziałami.”,
„AI pisze. Ludzie decydują. Źródła są obowiązkowe.”, „Pojedynczy fejk znika. Kolekcja zostaje.”

Slajd, którego potrzebuję:
```
