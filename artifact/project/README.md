# Meritum

**Meritum — obywatelski radar dezinformacji.**

![Znak Meritum: małe „m” z dwóch łuków](/_blob/e651a1909f767e201392a93160ffe775)

Ten brand book opisuje, jak Meritum wygląda i jak mówi. Tokeny są w zakładkach Kolory, Typografia i Odstępy, a komponenty z podglądami w zakładce Komponenty. Ścieżki plików odnoszą się do repozytorium Meritum-HackNation2026/meritum-design-system. Przekaż go agentowi AI, który robi slajdy, makiety albo materiały marketingowe, razem z poleceniem z sekcji 12. Wszystkie wartości są ostateczne, chyba że ten plik powie inaczej.

---

## 1. Idea w jednym akapicie

Meritum pozwala sprawdzić informację tak łatwo, jak wysłać wiadomość. Obywatel wkleja tekst albo link w formularzu na stronie (kanał podstawowy) albo klika „Sprawdź” pod postem we wtyczce do przeglądarki (drugi kanał; w okienku wtyczki jest też pole do wklejenia tekstu). Ten sam rdzeń obsługuje bota na Discordzie, a jeśli starczy czasu, także SMS. Jeden rdzeń weryfikacji wyodrębnia twierdzenia, szuka w opisanym i audytowalnym zbiorze źródeł oraz w świeżych publikacjach z zatwierdzonych serwisów, a potem dla każdego twierdzenia podaje werdykt z dosłownym cytatem, jawnymi przesłankami i siłą podstawy. Gdy dowodów brakuje, wstrzymuje się i mówi, czego nie ustalił; sprawy nierozstrzygnięte i powtarzające się trafiają do kolejki moderatorów. Wygląd łączy precyzję narzędzi dla analityków (Linear, Vercel) z powagą dziennikarstwa śledczego (The Economist, Bellingcat). Metafora przewodnia to **biuletyn synoptyczny**: spokojny komunikat, jasno podane źródła pomiaru i uczciwie zaznaczona niepewność.

**Hasła:** „Sprawdź, zanim podasz dalej.” oraz „Każde ustalenie ma źródło. Gdy źródeł brak, mówimy to wprost.”

---

## 2. Logo

Znak **„Dwa łuki”**: małe „m” z dwóch łuków. Łuki to twierdzenie i źródło, wspólny środkowy trzon (w kolorze akcentu) to miejsce, w którym się spotykają, a kropka nad nim to ustalenie.

| Plik | Kiedy używać |
|---|---|
| `brand/meritum-mark.svg` | na jasnym tle |
| `brand/meritum-mark-on-dark.svg` | na ciemnym tle |
| `brand/meritum-mark-mono.svg` | druk jednobarwny, grawer, pieczątka |
| `brand/meritum-app-icon.svg` | ikona wtyczki, favicon, avatar w social media |

**Logotyp:** znak + słowo „meritum” małymi literami, krój Archivo, grubość 650, szerokość 112%, światło −0,02 em. Pod spodem opcjonalny podtytuł „obywatelski radar dezinformacji” w Archivo 400, kolor drugorzędny.

**Zasady:**
- Minimalny rozmiar znaku: 14 px na ekranie, 6 mm w druku.
- Pole ochronne: wysokość kropki nad „m” z każdej strony.
- Trzon i kropka zawsze w kolorze akcentu (`#1D6A86` jasno, `#5DB3CF` ciemno). Łuki w kolorze tekstu.
- W widżecie na platformach znak ma 14 px i stoi przed słowem „Meritum” w małym nagłówku.
- Gotowe pliki PNG (512, 1024), ikony 16 do 512 px i poziomy logotyp z podtytułem są w `brand/exports/`. Logotyp z podtytułem ma tekst „obywatelski radar dezinformacji”.

**Nie wolno:** obracać znaku, dodawać cienia ani gradientu, zmieniać koloru trzonu na inny niż akcent, umieszczać znaku obok logotypów platform tak, jakby był ich częścią, ani rozciągać go.

---

## 3. Kolory

Jedno tło, jeden atrament, jeden akcent. Czerwień pojawia się wyłącznie przy werdykcie „Fałszywe”.

### Baza

| Rola | Jasny | Ciemny | Do czego |
|---|---|---|---|
| Tło aplikacji | `#F6F7F5` | `#0B0F12` | tło strony, panelu i slajdów |
| Karta | `#FFFFFF` | `#0B0F12` | karty, widżety, okienka |
| Atrament | `#14191E` | `#E7ECEE` | cały tekst główny, przycisk główny |
| Tekst drugorzędny | `#4C5862` | `#9AA6AE` | podpisy, etykiety, wydawcy i daty źródeł |
| Obramowanie | `#D9DEDD` | `#2F3336` | 1 px wokół kart, linie tabel |
| Podniesione tło | `#E8ECEB` | `#22282C` | aktywna zakładka, tor paska, tło cytatu |

### Werdykty i stany

Nazwy tokenów zostają (`--verified`, `--contested`, `--scam`, `--muted`); zmienia się to, co oznaczają.

| Werdykt lub stan | Token | Kolor | Tło plakietki | Tekst plakietki |
|---|---|---|---|---|
| **Potwierdzone** | `--verified` | `#1D6A86` / `#5DB3CF` | `#E1EDF2` / `#123441` | `#13506A` / `#9FD8EC` |
| **Wprowadzające w błąd** | `--contested` | `#B7791F` / `#F2C46D` | `#F8EEDB` / `#3A2C10` | `#7A4E08` / `#F2C46D` |
| **Fałszywe** | `--scam` | `#C8213A` / `#FF6B7D` | `#FBE6E9` / `#43161D` | `#9E1A2E` / `#FFB3BE` |
| **Brak wystarczających dowodów**, **Nie podlega weryfikacji** | `--muted` | atrament | podniesione tło | tekst drugorzędny |

Pierwsza wartość dotyczy trybu jasnego, druga ciemnego. Wszystkie pary tekst/tło mają kontrast co najmniej 4,5:1 (sprawdzone: 5,6–17,7:1).

**Stany, które nie są werdyktem** („Doprecyzuj pytanie”, „Poza zakresem”, „Problem techniczny”) mają neutralny kolor, ikonę i zwykły wiersz tekstu. Nigdy nie wyglądają jak plakietka werdyktu, bo awaria nie jest oceną treści.

**Siła podstawy** („Mocna”, „Umiarkowana”, „Słaba”) jest zawsze w kolorze atramentu, jako słowo z trzema kreskami poziomu. Nie dostaje koloru werdyktu.

**Zasady koloru:**
- Stan nigdy nie jest oznaczony samym kolorem: zawsze ma też słowo („Potwierdzone”, „Fałszywe”) albo znak.
- Na wykresach jakości są co najwyżej 4 kolory: atrament, akcent, czerwień tylko dla błędów i szary dla przeszłości.
- Przycisk główny jest prawie czarny (`#14191E`), nigdy w kolorze akcentu.

**Zakazane:** gradienty fioletowo-niebieskie (i w ogóle gradienty), zielony tekst na czarnym tle w stylu „hakerskim”, neonowe poświaty, granat z czerwienią w stylu urzędowym, kremowe tło z terakotą.

---

## 4. Typografia

| Krój | Rola | Źródło |
|---|---|---|
| **Archivo** (wagi 400–800, szerokość 75–125) | cały interfejs, odpowiedzi, slajdy, logotyp | Google Fonts |
| **Azeret Mono** (400–600) | wyłącznie dane: ID sprawdzeń i spraw (c_01, #S-1), domeny w tabelach, daty, godziny, liczby w metrykach | Google Fonts |

Oba kroje mają polskie znaki. Mono nigdy nie służy do dekoracji, etykiet ani nagłówków.

### Skala

| Styl | Rozmiar / interlinia | Grubość | Gdzie |
|---|---|---|---|
| Display | 40 px / 1,05 | 700, szerokość 108% | tylko slajdy |
| Tytuł | 22 px / 28 px | 700 | nagłówek strony i panelu |
| Tytuł karty | 15 px | 700 | treść twierdzenia na karcie wyniku |
| Tekst | 15 px / 22 px | 400 | wyjaśnienie, cytat |
| Mały | 13 px / 20 px | 400–600 | wydawca, data, przesłanki |
| Meta | 12 px / 16 px | 600 | nagłówek widżetu „Meritum”, osie wykresu |

Nic poniżej 12 px. Nagłówki zdaniowe (wielka litera tylko na początku), bez rozstrzelonych WERSALIKÓW, bez etykiet nad nagłówkami.

**W widżecie na platformie** treść dziedziczy krój platformy (np. systemowy na X, Reddit Sans na Reddicie). Archivo zostaje tylko w nagłówku „Meritum” i plakietce werdyktu.

---

## 5. Odstępy, siatka, kształty

- **Siatka 4 px.** Typowe odstępy: 4, 6, 8, 12, 14, 16, 24 px.
- **Wnętrze kart:** 14 px w poziomie, 12 px u góry, 14 px na dole.
- **Strona i panel:** marginesy 24 px (16 px na telefonie), odstęp między blokami 12–16 px. Formularz i wynik w jednej kolumnie do 720 px.
- **Promienie:** karty 12 px (w widżecie zgodnie z platformą: X 16, Facebook 8, Instagram 0, Reddit 16, TikTok 8), okienka 14 px, przyciski i plakietki w pełni zaokrąglone (pigułki), pola formularzy 10 px.
- **Głębia:** karty leżą płasko, mają obramowanie 1 px i nie mają cienia. Cień dostaje tylko to, co się unosi: okienko wtyczki, podpowiedź (tooltip), powiadomienie.
- **Zakazane:** pasek koloru wzdłuż jednego boku karty, siatki identycznych kart z ikoną na górze, szkło i rozmycie tła, ozdobne kształty.

---

## 6. Komponenty

Kod React (shadcn/ui, Tailwind v4) leży w `components/meritum/`, wersja dla Shadow DOM wtyczki w `extension/widget.css`, dane opisują kontrakty (źródłem prawdy jest repozytorium meritum-core, a w `contracts/` leży kopia pobierana skryptem `contracts/sync.sh`, której nie edytuje się ręcznie), teksty `copy/pl.json`. Bot na Discordzie i SMS nie mają własnego wyglądu: korzystają z tych samych tekstów, a odpowiedź SMS mieści się w 70 znakach (polskie znaki wymuszają kodowanie UCS-2) i kończy się linkiem do pełnej karty wyniku (`sms`). Interaktywne makiety: `demo/widgets/`, przepływ na makiecie X: `demo/x/`. Makiety i komponenty pokazują jeszcze stary przepływ zgłoszenia i trzeba je przerobić według tej sekcji.

### 6.1 Formularz „Sprawdź informację” (strona WWW, kanał podstawowy)
Jedna kolumna, działa od 320 px szerokości.
1. Tytuł „Sprawdź informację” i jedno zdanie, co się stanie.
2. Pole „Tekst albo link” (do 4000 znaków), przyjmuje wklejony tekst albo pełny adres https://.
3. Przycisk główny „Sprawdź”, aktywny od 3 znaków albo poprawnego linku. W trakcie: „Sprawdzamy…” i pasek analizy (6.3).
4. Pod przyciskiem informacja o prywatności: konto nie jest potrzebne, maskowanie oczywistych danych osobowych, termin usunięcia zapisu, link „Usuń moje sprawdzenia”.
5. Pod formularzem lista „Twoje sprawdzenia” (`history`): sprawdzenia z tej rozmowy, od najnowszego; kliknięcie otwiera kartę wyniku. Bez logowania lista pochodzi z sessionStorage, a notatka mówi, że zniknie po zamknięciu karty. Pusta lista pokazuje `history.empty`.
6. Przy liście opcjonalne logowanie (`account`): dwa przyciski drugorzędne „Zaloguj się kontem Google” i „Zaloguj się kontem Microsoft” oraz zdanie, że logowanie nie jest potrzebne. Po zalogowaniu historia jest na serwerze, a w miejscu przycisków są „Usuń moją historię”, „Usuń konto i historię” i „Wyloguj się”.

Błędy pod polem, słowami z `copy/pl.json` (`errors`), bez czyszczenia wpisanej treści.

### 6.2 Przycisk „Sprawdź” we wtyczce (drugi kanał)
Znak Meritum 18 px + słowo „Sprawdź” w pasku akcji posta. Stany: spoczynek (kolor ikon platformy), najechanie (tło `#E1EDF2`, tekst `#13506A`), w toku, „Sprawdzono”. Treść posta wysyłamy dopiero po kliknięciu. Wynik pojawia się pod postem jako karta wyniku (6.4). Okienko wtyczki z paska przeglądarki ma to samo pole co formularz WWW, więc ten sam tekst można sprawdzić w obu kanałach i dostać ten sam wynik.

### 6.3 Pasek analizy
Pokazuje kroki workflowu: kółko czeka, kręci się, gotowe, pominięte albo nieudane. Kody i teksty kroków: `receive`, `extract_claims`, `search_corpus`, `search_web`, `assess_evidence`, `verify_citations`, `write_answer`, `save_record` (`copy/pl.json`, `analysis.steps`). Krok „Szukamy świeżych publikacji w zatwierdzonych serwisach” pojawia się tylko wtedy, gdy baza źródeł nie wystarczyła. Agenty badawcze działają równolegle, więc kilka kółek może się kręcić naraz. Odpowiedź przychodzi strumieniem: wersja wstępna ma dopisek `analysis.draft` i nie pokazuje werdyktu, dopóki cytaty nie przejdą weryfikacji.

### 6.4 Karta wyniku
Jedna karta na sprawdzenie, a w niej jeden blok na każde twierdzenie. Białe tło, obramowanie 1 px, w widżecie promień platformy.
- **Nagłówek:** znak 14 px + „Meritum”.
- **Twierdzenie i plakietka werdyktu:** treść twierdzenia jako tytuł karty, obok plakietka („Potwierdzone”, „Fałszywe”, „Wprowadzające w błąd”, „Brak wystarczających dowodów”, „Nie podlega weryfikacji”) i jedno zdanie podpowiedzi z `verdict_hint`.
- **Wyjaśnienie:** 1–3 zdania z podpisem „To nasze wyjaśnienie, przygotowane z pomocą AI. Podstawą są cytaty ze źródeł poniżej.” Wyjaśnienie jest wizualnie oddzielone od cytatów.
- **Na czym się opieramy:** każde źródło jako wiersz: tytuł (link), wydawca, data publikacji, rodzaj i poziom (urzędowe lub pierwotne, wtórne), a pod spodem dosłowny fragment na podniesionym tle. Źródło z wyszukiwania w sieci ma dopisek „znalezione w wyszukiwaniu w zatwierdzonych serwisach”.
- **Siła podstawy:** słowo i trzy kreski poziomu, pod nimi przesłanki słowami: liczba niezależnych źródeł, ile z nich urzędowych, wiek najnowszego, czy są zgodne. Przy sprzecznych źródłach nie ma siły: werdykt to „Brak wystarczających dowodów”, cytaty obu stron stoją obok siebie, a nad nimi jest jedno zdanie, czym się różnią (`result.conflict`).
- **Czego nie udało się ustalić:** obowiązkowe przy „Brak wystarczających dowodów”.
- **Ostrzeżenia:** materiał archiwalny, podobieństwo do znanego incydentu (jako kontekst, nie podstawa oceny) i neutralna informacja o statusie źródła, np. podmiot objęty sankcjami UE. Każde w osobnym wierszu, bez czerwieni.
- **Technika:** nazwa techniki manipulacji + podpowiedź „jak rozpoznać?”, gdy dotyczy.
- **Stopka:** „Ograniczenia” (zawsze), stan przekazania moderatorom (`escalation`: zalecane, przekazane, dołączone do sprawy) i informacja o użyciu AI.
- **Pojawienie się:** karta rozwija się z wysokości 0 i unosi o 8 px w 0,5 s.

Gdy wynik nie jest werdyktem (doprecyzuj, poza zakresem, problem techniczny), karta ma tylko ikonę, tytuł stanu i komunikat z `status_hint`. Żadnej plakietki, żadnych źródeł.

### 6.5 Kolejka moderatorów (panel)
Lista spraw: ID w mono (#S-1), krótki opis, powód słowami („brak wystarczających dowodów”, „sprawa wysokiego ryzyka”, „powtarzające się pytanie bez odpowiedzi”), liczba podobnych pytań, pierwsze i ostatnie wystąpienie, stan. Podobne pytania trafiają do jednej sprawy, nie tworzą nowych. Panel pokazuje też jakość: medianę czasu odpowiedzi, odsetek wstrzymań, błędy wyszukiwania, wykryte próby wstrzyknięcia poleceń i szacowany koszt. Wykresy według zasad z sekcji 3: etykiety przy liniach, bez kafelków KPI z ikonami.

### 6.6 Komponenty poza zakresem MSZ
`ScamWarningCard`, `CampaignRotation`, `BotDefenseTelemetry` i `QuickReportPopover` zostały w repozytorium z wcześniejszej wersji produktu (wątek NASK i notatek społeczności). Nie używamy ich w demo ani w materiałach na konkurs MSZ.

---

## 7. Widżet na pięciu platformach

**Zasada: rama od gospodarza, sygnał od Meritum.**

| Od platformy bierzemy | Meritum zostawia zawsze |
|---|---|
| krój pisma i jego rozmiar, promień narożników, tło i obramowanie karty, kształt przycisków, kolor linków | znak i słowo „Meritum” w nagłówku, kolory werdyktów, obowiązkowe źródła z cytatem, informację o użyciu AI |

Nigdy nie wstawiamy logotypu platformy do widżetu i nigdy nie udajemy treści platformy. Szczegóły skórek: `demo/widgets/` i zmienne `[data-host]` w `tokens/meritum.css`.

---

## 8. Ton komunikacji

**Mówimy jak dobry redaktor: spokojnie, konkretnie, ze źródłem.**

1. **Opisujemy twierdzenia, nie ludzi.** Nigdy „kłamca”, „idiota”, „fake news!”.
2. **Każde ustalenie ma źródło.** Bez cytatu nie ma werdyktu.
3. **Uczciwa niepewność.** Gdy dowodów brakuje, mówimy, czego nie ustaliliśmy. Nie zgadujemy.
4. **Awaria to nie ocena.** Problem techniczny opisujemy jako problem techniczny.
5. **Nazywamy technikę**, żeby czytelnik nauczył się ją rozpoznawać.
6. **Prosto i krótko:** strona czynna, zdania do ~20 słów, bez żargonu, bez wykrzykników, bez emoji. Piszemy dla osoby bez wiedzy technicznej.
7. **Liczby uczciwie:** w demo zawsze z dopiskiem „dane symulowane”; wyniki testów tylko zmierzone i z danymi do odtworzenia.

| Zamiast | Piszemy |
|---|---|
| „FAŁSZ! Ten post kłamie!” | „Fałszywe. Konstytucja pozwala na dwie kadencje prezydenta, nie trzy.” |
| „Nie wiadomo” | „Nie rozstrzygamy, bo nie mamy wystarczających źródeł. Nie ustaliliśmy, kto ogłosił to zdarzenie.” |
| „Submit” / „OK” | „Sprawdź”, „Usuń moje sprawdzenia” |
| „Wystąpił błąd” | „Nie udało się sprawdzić. To nie jest ocena treści. Spróbuj za kilka minut.” |
| „Nasz zaawansowany algorytm AI ustalił…” | „Odpowiedź przygotował system z użyciem AI. Sprawdź źródła sam.” |

---

## 9. Ruch

- Ruch tylko jako odpowiedź na działanie użytkownika albo pokazanie zmiany danych.
- Krzywa `cubic-bezier(0.16, 1, 0.3, 1)` (szybki start, miękkie wyhamowanie), czas 150–550 ms.
- Animujemy przezroczystość, przesunięcie i skalę; wyjątek to rozwijanie karty (wysokość od 0).
- Bez pulsujących kropek, bez animacji w pętli (poza kółkiem „w toku”).
- Przy włączonym „ogranicz ruch” w systemie wszystkie animacje skracają się do zera.

---

## 10. Dostępność

WCAG 2.2 AA w obu trybach, także na tle cudzych feedów. Werdykty oznaczone słowem, nie tylko kolorem. Widoczny pierścień fokusu (2 px, kolor akcentu). Klawisz Esc zamyka okienko i oddaje fokus przyciskowi. Wynik ogłasza region `aria-live`. Formularz działa na telefonie bez przewijania w poziomie. Polskie teksty są dłuższe niż angielskie, więc komponenty muszą wytrzymać długie etykiety, np. „Brak wystarczających dowodów”.

---

## 11. Slajdy i materiały marketingowe

- Tło slajdu `#F6F7F5` albo `#0B0F12` (jeden tryb na całą prezentację).
- Jedna myśl na slajd, tytuł do 2 linii, Display 40 px lub większy.
- Zamiast zdjęć stockowych: prawdziwe zrzuty interfejsu Meritum (strona, wtyczka, panel) w dużej skali.
- Wykresy według zasad z sekcji 3: etykiety przy liniach, czerwień tylko dla błędów.
- Logo w lewym górnym albo dolnym rogu, 24–32 px.
- W przykładach używamy prawdziwych, sprawdzalnych źródeł z korpusu. Nie wymyślamy źródeł, cytatów ani wyników testów.
- Nie piszemy o współpracy z MSZ, NASK ani mediami, dopóki jej nie ma; piszemy „gotowe do integracji z…”.

---

## 12. Polecenie dla agenta AI (kopiuj i wklej)

```
Projektujesz materiał dla Meritum — obywatelskiego radaru dezinformacji
(strona WWW do sprawdzania informacji, wtyczka do przeglądarki jako drugi kanał,
panel moderatora). Trzymaj się DESIGN_SYSTEM.md.

Produkt: obywatel wkleja tekst albo link, system wyodrębnia twierdzenia i dla każdego
podaje werdykt (Potwierdzone, Fałszywe, Wprowadzające w błąd, Brak wystarczających
dowodów, Nie podlega weryfikacji) z dosłownym cytatem, wydawcą, datą i linkiem,
z przesłankami i siłą podstawy. Gdy dowodów brakuje, wstrzymuje się i mówi, czego nie ustalił.
Styl: „Biuletyn synoptyczny”: precyzja narzędzi dla analityków i powaga dziennikarstwa
śledczego. Spokojnie, czysto, dużo powietrza, płaskie białe karty z obramowaniem 1 px.
Kolory: tło #F6F7F5, karty #FFFFFF, tekst #14191E, tekst drugorzędny #4C5862,
obramowanie #D9DEDD, akcent i „Potwierdzone” #1D6A86, „Wprowadzające w błąd” #B7791F,
„Fałszywe” #C8213A (tylko tam), brak dowodów i stany techniczne neutralne.
Kroje: Archivo (wszystko), Azeret Mono (tylko ID, domeny, daty, godziny, liczby).
Logo: brand/meritum-mark.svg (małe „m” z dwóch łuków, trzon i kropka w kolorze #1D6A86).
Przyciski: pigułki, główny prawie czarny. Cień tylko na elementach unoszących się.
Ton: opisujemy twierdzenia, nie ludzi; każde ustalenie ze źródłem; uczciwa niepewność;
zdania proste, bez wykrzykników i emoji.
Zakazane: gradienty, fiolet, neon, zielony tekst na czarnym, styl urzędowy, kafelki z ikonami,
pasek koloru z boku karty, etykiety WERSALIKAMI nad nagłówkami, wymyślone źródła i cytaty,
liczby bez dopisku „dane symulowane” albo bez danych do odtworzenia.
```

---

## 13. Kto czego używa

### Strona WWW i panel (React)
- `components/meritum/`: komponenty React (shadcn/ui). Do przerobienia na karty wyniku według sekcji 6.4; stan opisuje `components/meritum/README.md`.
- `tokens/meritum.css`: te same tokeny dla strony, panelu i wtyczki.

### Wtyczka Chrome (programista)
- `extension/widget.css`: style widżetu dla Shadow DOM (`:host`), tokeny jasne i ciemne, skórki platform przez `:host([data-host=…])`.
- `extension/manifest.json` i `extension/reference/`: referencyjny skrypt (MV3) bez frameworka: wykrywa platformę, znajduje posty selektorami z `demo/platforms/SELECTORS.md`, wstawia przycisk we własnym Shadow DOM i wykrywa motyw gospodarza. Dziś gra stary przepływ „Zgłoś” na atrapie API; trzeba go zamienić na „Sprawdź” wołające to samo API co formularz WWW.
- `extension/popup/`, `extension/onboarding/`, `extension/icons/`. Opis techniczny po angielsku: `extension/README.md`.

### Backend (FastAPI)
- `contracts/meritum_contracts.py`: kopia kontraktów z meritum-core (`src/meritum_core/checks/contracts.py`), oznaczona jako „nie edytować”; design system korzysta z wygenerowanych w core JSON Schema i typów TS. Modele Pydantic v2 dla API, strony, wtyczki i panelu (zapytanie, wynik sprawdzenia, twierdzenie, cytat, źródło, przesłanki, status analizy, zapis przebiegu, sprawa moderatora, wpis katalogu źródeł). Reguły z treści zadania MSZ są w modelach:
  - werdykt rozstrzygający (potwierdzone, fałszywe, wprowadzające w błąd) wymaga cytatu i jawnych przesłanek;
  - siła podstawy wynika z przesłanek według jednej stałej reguły, nie z deklaracji modelu;
  - zgodność wynika z wymowy cytatów; sprzeczne wiarygodne źródła dają „brak wystarczających dowodów” z cytatami obu stron i bez siły;
  - niezależne źródła liczymy według wydawcy, nie według strony;
  - wiek dowodu liczymy od daty, której dotyczy twierdzenie, z progiem z katalogu; obowiązujący akt prawny, strona urzędowa aktualizowana w miejscu i dowód o zdarzeniu z przeszłości nie są archiwalne;
  - „brak wystarczających dowodów” musi powiedzieć, czego nie ustalono;
  - awaria, prośba o doprecyzowanie i pytanie poza zakresem nie są werdyktami i nie mają twierdzeń;
  - zalecenie przekazania sprawy moderatorowi różni się od faktycznego przekazania;
  - cytat przechodzi tylko wtedy, gdy fragment znaleziono w źródle dosłownie.
- `contracts/sync.sh` kopiuje z meritum-core `meritum.schema.json` (JSON Schema), `meritum.ts` (typy TypeScript), `examples.json` i kod modeli; generowanie i testy reguł (przykłady, odrzucanie złych danych) są w CI meritum-core, a CI tego repo sprawdza sumy kontrolne kopii.
- `copy/pl.json`: wszystkie teksty interfejsu: formularz, werdykty z podpowiedziami, siła podstawy, stany techniczne, przekazanie moderatorom, ostrzeżenia o statusie źródła, kroki analizy, techniki manipulacji z „jak rozpoznać”, kolejka moderatorów, historia sprawdzeń, logowanie, SMS, polityka prywatności kanałów, błędy. Klucze odpowiadają kodom z kontraktów.

### Prezentacje i film (cały zespół)
- `presentation/`: szablon PPTX, slajdy HTML, zrzuty, grafiki social i instrukcja `presentation/README.md`. Obecne pliki pokazują jeszcze stary produkt na dwa konkursy i trzeba je wygenerować od nowa pod deck MSZ (do 12 slajdów, film do 3 minut).
- `brand/exports/`: logo w PNG (512, 1024), ikona aplikacji 16 do 512 px, poziomy logotyp z podtytułem i bez, jasny i ciemny.

### Pokaz
- `demo/live/<platforma>/`: makiety X, Facebooka, Instagrama, Reddita i TikToka, na których skrypt wtyczki działa bez instalowania. Jury może tam kliknąć „Sprawdź” bez konfiguracji przeglądarki.
- `demo/platforms/`: te same makiety bez Meritum, do testowania prawdziwej wtyczki.

## 14. Pliki

| Ścieżka | Zawartość |
|---|---|
| `DESIGN_SYSTEM.md` | ta specyfikacja |
| `tokens/meritum.css` | tokeny CSS i `@theme` dla Tailwind v4 + shadcn/ui, tryb ciemny, skórki platform |
| `components/meritum/` | komponenty React: `ContextCard`, `AnalysisSteps`, `MeritumMark` oraz nieużywane w MSZ `QuickReportPopover`, `BotDefenseTelemetry`, `CampaignRotation` |
| `contracts/` | kopia kontraktów z meritum-core, odświeżana skryptem `sync.sh`, nie do ręcznej edycji: Pydantic, JSON Schema, typy TS, przykłady |
| `copy/pl.json` | teksty interfejsu |
| `extension/` | zestaw wtyczki Chrome: style Shadow DOM, skrypt referencyjny, popup, onboarding, ikony |
| `brand/` | logo w SVG, `brand/exports/` w PNG i logotyp |
| `presentation/` | szablon PPTX, slajdy HTML, zrzuty, grafiki social, instrukcja |
| `demo/live/` | interaktywne makiety platform na pokaz |
| `demo/platforms/` | czyste makiety platform i `SELECTORS.md` |
| `demo/x/`, `demo/widgets/`, `demo/logo/` | demo na X, widżet na platformach ze stanami, warianty znaku |
| `docs/` | dokument produktowy (historie użytkowników, funkcje, ADR), źródło dla Google Docs |
| `artifact/` | pliki opublikowanego Design System artifactu |
| `PRODUCT.md`, `KEY_SELLING_POINTS.md` | produkt i strategia na konkurs MSZ „Prawdowid” |
