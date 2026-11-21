# Meritum: zestaw do prezentacji i materiałów marketingowych

Ten folder jest dla osób, które robią slajdy, posty i grafiki o Meritum, a nie piszą kodu. Wszystko tutaj wygląda tak samo jak produkt: te same kolory, kroje pisma i logo. Zasady, z których to wynika, są w `../DESIGN_SYSTEM.md`, a treść pitchu w `../KEY_SELLING_POINTS.md`.

**Uwaga: Meritum startuje teraz tylko w konkursie MSZ „Prawdowid”.** Szablon `meritum-template.pptx`, `slides/index.html`, zrzuty w `screenshots/`, grafiki w `social/` i logotypy z podtytułem w `../brand/exports/` pokazują jeszcze stary produkt na dwa konkursy (zgłoszenia, kampanie, atak botów, podtytuł „oraz scamu”). Trzeba je wygenerować od nowa według sekcji „Deck na konkurs MSZ” poniżej. Do tego czasu nie wysyłaj ich jury.

## Co jest w zestawie

| Plik | Do czego |
|---|---|
| `meritum-template.pptx` | szablon PowerPoint / Google Slides / Keynote (do przerobienia na deck MSZ) |
| `slides/index.html` | ta sama prezentacja w przeglądarce, z notatkami prowadzącego (do przerobienia) |
| `screenshots/` | zrzuty demo (stare: zgłoszenie, notatka, ostrzeżenie o oszustwie; do podmiany na formularz, kartę wyniku, wtyczkę i panel) |
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

## Deck na konkurs MSZ

Wymagania z treści zadania: PDF, najwyżej 12 slajdów, a w nich problem, użytkownicy, architektura, demonstracja, wyniki testów, ryzyka i dalsze kroki. Osobno film demonstracyjny pod linkiem, najwyżej 3 minuty.

Proponowana kolejność (12 slajdów):

1. Tytuł: Meritum, podtytuł „obywatelski radar dezinformacji”, nazwa zespołu.
2. Problem: pogłoska dociera kanałem, którego używa obywatel, a sprawdzenie wymaga wiedzy i czasu.
3. Użytkownicy: obywatel (także o niskich kompetencjach cyfrowych) i moderator lub analityk.
4. Jak to działa: wklejasz tekst albo link, dostajesz werdykt dla każdego twierdzenia z cytatem i źródłem.
5. Demo, kanał WWW: zrzut formularza i karty wyniku.
6. Demo, drugi kanał: „Sprawdź” pod postem we wtyczce, ten sam wynik co na stronie.
7. Uczciwa niepewność: „Brak wystarczających dowodów”, czego nie ustaliliśmy, przekazanie sprawy moderatorom.
8. Architektura: kanały oddzielone od rdzenia weryfikacji, wymienny model, korpus i wyszukiwanie w zatwierdzonych serwisach, zapis przebiegu.
9. Źródła: katalog, typy źródeł, licencje, sposób kwalifikacji i aktualizacji.
10. Wyniki testów: mierniki z sekcji 6 zadania, zmierzone na naszym zestawie, z linkiem do danych.
11. Ryzyka: halucynacje, stronniczość źródeł, prywatność, prompt injection, dostępność, nadużycia.
12. Dalsze kroki i koszt: koszt 1 000 zapytań, droga do pilotażu.

Każda liczba na slajdzie 10 musi pochodzić z uruchomionych testów i dać się odtworzyć. Liczby z makiet podpisujemy „dane symulowane”.

## Szablon PPTX

Obecny szablon ma jeszcze 10 slajdów starej wersji. Po przerobieniu będzie miał układ z sekcji wyżej. Każdy slajd ma notatki prowadzącego.

**Najpierw kroje pisma.** Szablon używa Archivo (cały tekst) i Azeret Mono (tylko liczby, godziny, nazwy kont, domeny). Jeśli ich nie ma, program podstawi inny krój i tekst się rozjedzie.

- **Google Slides:** wgraj plik na Dysk Google, kliknij go dwukrotnie i wybierz „Otwórz w: Prezentacje Google”. Oba kroje są w Google Slides: menu czcionek → „Więcej czcionek” → wpisz „Archivo” i „Azeret Mono” → dodaj.
- **PowerPoint (Windows, Mac):** zainstaluj kroje z [fonts.google.com/specimen/Archivo](https://fonts.google.com/specimen/Archivo) i [fonts.google.com/specimen/Azeret+Mono](https://fonts.google.com/specimen/Azeret+Mono) (przycisk „Get font” → pobierz → otwórz pliki .ttf → „Zainstaluj”). Potem otwórz `meritum-template.pptx`.
- **Keynote:** zainstaluj kroje jak wyżej, potem Plik → Otwórz → `meritum-template.pptx`. Keynote może przesunąć tekst o kilka pikseli: przejrzyj każdy slajd.

**Jak pracować z szablonem**
- Zrób kopię pliku i pracuj na kopii.
- Nowy slajd = duplikat podobnego slajdu (prawy przycisk → „Duplikuj slajd”), potem podmień tekst. Nie zaczynaj od pustego slajdu.
- Wykresy wyników testów wypełniaj tylko liczbami z raportu testów (prawy przycisk → „Edytuj dane”).
- Na slajdzie tytułowym wpisz imiona w miejsce „[Imię Nazwisko]”.
- Zrzuty możesz podmienić na nowe (prawy przycisk na obrazku → „Zmień obraz”), zachowując rozmiar.

## Prezentacja HTML i eksport do PDF

1. Otwórz `slides/index.html` w Chrome (dwuklik na pliku). Potrzebny jest internet, bo kroje ładują się z Google Fonts.
2. Strzałki ← → (albo spacja, klik) zmieniają slajdy. Klawisz **N** pokazuje notatki prowadzącego na dole ekranu. **F11** (Windows) lub **Ctrl+Cmd+F** (Mac) to pełny ekran.
3. **PDF:** Ctrl+P (Mac: Cmd+P) → Miejsce docelowe: „Zapisz jako PDF” → Więcej ustawień → Marginesy: „Brak”, zaznacz „Grafika tła” → Zapisz. Wychodzi jeden slajd na stronę, w formacie 16:9. Do jury idzie najwyżej 12 stron.

## Spójne zrzuty ekranu z demo

Obecne zrzuty w `screenshots/` pokazują starą wersję. Nowe rób na działającym prototypie, nie na makietach z wpisanymi odpowiedziami. Trzymaj się tych ustawień, żeby wyglądały tak samo:

- **Okno przeglądarki 1440 × 900**, powiększenie strony 100%, Chrome. Dla wersji na telefon: 390 × 844.
- **Tryb jasny.** Jedna prezentacja = jeden tryb.
- Kursor odsuń od kart, żeby nie było podświetleń ani dymków.

Które stany uchwycić:

| Co | Po co |
|---|---|
| formularz „Sprawdź informację” przed wysłaniem i pasek analizy w trakcie | slajd 5 |
| karta wyniku z co najmniej dwoma twierdzeniami i cytatami | slajdy 4 i 5 |
| przycisk „Sprawdź” pod postem we wtyczce i karta wyniku pod postem | slajd 6 |
| karta z werdyktem „Brak wystarczających dowodów” i informacją o przekazaniu sprawy | slajd 7 |
| stan „Problem techniczny” | slajd 11 (awaria nie jest werdyktem) |
| kolejka moderatorów i panel jakości | slajdy 7 i 10 |

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
| Jedna myśl na slajd, tytuł do dwóch linii: „Gdy dowodów brakuje, mówimy to wprost” | Trzy akapity i lista punktorów na jednym slajdzie |
| Tło `#F6F7F5`, białe karty z cienką szarą ramką | Gradienty, fiolet, neonowe poświaty, zielony tekst na czarnym tle |
| Czerwień `#C8213A` tylko przy werdykcie „Fałszywe”, zawsze ze słowem | Czerwone nagłówki „dla uwagi”, czerwone tło całego slajdu |
| Prawdziwe zrzuty działającego Meritum | Zdjęcia stockowe, ludzie przy laptopach, kłódki i tarcze |
| Wyniki testów z raportu, z linkiem do danych; liczby z makiet z dopiskiem „dane symulowane” | „Trafność 98%” albo każda liczba, której nie zmierzyliśmy |
| Przykłady z prawdziwymi, sprawdzalnymi źródłami z korpusu | Wymyślone źródła, cytaty albo daty |
| „Gotowe do integracji z OpenCTI” | „Współpracujemy z MSZ”, dopóki to nieprawda |
| „Fałszywe. Konstytucja pozwala na dwie kadencje prezydenta, nie trzy.” | „FAŁSZ! Ten post kłamie!” |
| Nagłówki zdaniowe: „Każde ustalenie ma źródło” | NAPISY WERSALIKAMI nad nagłówkami, emoji, wykrzykniki |
| Wykres z etykietą przy linii i progiem z treści zadania (np. macro-F1 ≥ 0,75) | Kafelki z ikoną i dużą liczbą, legenda daleko od linii |
| Logo w rogu, 24–32 px na slajdzie | Logo rozciągnięte, obrócone, z cieniem, obok logo platform |

## Gotowe polecenie dla AI (do nowych slajdów)

Wklej to do ChatGPT, Claude albo Gemini, a pod spodem napisz, jakiego slajdu potrzebujesz.

```
Robisz slajd (16:9, 1920×1080) dla Meritum — obywatelskiego radaru dezinformacji
(strona WWW do sprawdzania informacji + wtyczka do przeglądarki jako drugi kanał + panel
moderatora), zgłoszonego w konkursie MSZ „Prawdowid”. Język: polski.

Produkt: obywatel wkleja tekst albo link, system dla każdego twierdzenia podaje werdykt
(Potwierdzone, Fałszywe, Wprowadzające w błąd, Brak wystarczających dowodów,
Nie podlega weryfikacji) z dosłownym cytatem, wydawcą, datą, linkiem i siłą podstawy.
Gdy dowodów brakuje, wstrzymuje się i mówi, czego nie ustalił.
Styl „Biuletyn synoptyczny”: spokojnie, precyzyjnie, dużo powietrza. Jedna myśl na slajd,
tytuł zdaniowy do dwóch linii, krój Archivo 700 w rozmiarze 72 px lub większym.
Kolory: tło #F6F7F5, karty #FFFFFF z obramowaniem 1 px #D9DEDD, bez cieni,
tekst #14191E, tekst drugorzędny #4C5862, akcent i „Potwierdzone” #1D6A86,
„Wprowadzające w błąd” #B7791F, „Fałszywe” #C8213A (tylko tam, zawsze ze słowem),
brak dowodów i stany techniczne neutralne.
Kroje: Archivo do wszystkiego, Azeret Mono tylko do liczb, dat, godzin, ID i domen.
Logo Meritum (małe „m” z dwóch łuków) w lewym dolnym rogu, 30 px, obok słowo „meritum”.
Zamiast zdjęć: zrzuty interfejsu Meritum.
Wykresy: etykiety przy liniach, próg z treści zadania zaznaczony linią.
Ton: opisujemy twierdzenia, nie ludzi; każde ustalenie ze źródłem; uczciwa niepewność;
krótkie zdania w stronie czynnej.
Zakazane: gradienty, fiolet, neon, emoji, wykrzykniki, etykiety WERSALIKAMI nad nagłówkami,
siatki kart z ikonami, pasek koloru z boku karty, zdjęcia stockowe, wymyślone źródła i cytaty,
liczby bez dopisku „dane symulowane” albo bez danych do odtworzenia,
twierdzenia o współpracy z MSZ (piszemy „gotowe do integracji z…”).
Hasła, których możesz użyć: „Sprawdź, zanim podasz dalej.”,
„Każde ustalenie ma źródło. Gdy źródeł brak, mówimy to wprost.”

Slajd, którego potrzebuję:
```
