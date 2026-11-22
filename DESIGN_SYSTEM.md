# Meritum: Design System

**Meritum — obywatelski radar dezinformacji.**

Ten dokument opisuje, jak Meritum wygląda i jak mówi. Przekaż go agentowi AI, który buduje widok strony albo panelu, razem z poleceniem z sekcji 12; przy slajdach, makietach i materiałach marketingowych obowiązują sekcje 7 i 11, które zostają przy dotychczasowym wyglądzie. Wszystkie wartości są ostateczne, chyba że ten plik powie inaczej.

---

## 1. Idea w jednym akapicie

Meritum pozwala sprawdzić informację tak łatwo, jak wysłać wiadomość. Obywatel wkleja tekst albo link w formularzu na stronie (kanał podstawowy) albo wysyła go botowi na Discordzie (drugi kanał, także w wiadomości prywatnej). Wtyczka do przeglądarki dodaje „Sprawdź” pod postem i pole do wklejenia tekstu w okienku. Jeśli starczy czasu, dojdzie SMS. Jeden rdzeń weryfikacji wyodrębnia twierdzenia, szuka w opisanym i audytowalnym zbiorze źródeł oraz w świeżych publikacjach z zatwierdzonych serwisów, a potem dla każdego twierdzenia podaje werdykt z dosłownym cytatem, jawnymi przesłankami i siłą podstawy. Gdy dowodów brakuje, wstrzymuje się i mówi, czego nie ustalił; sprawy nierozstrzygnięte i powtarzające się trafiają do kolejki moderatorów. Wygląd łączy precyzję narzędzi dla analityków (Linear, Vercel) z powagą dziennikarstwa śledczego (The Economist, Bellingcat). Motyw nazywa się **Atrament**: biała strona, czarny atrament, żadnego koloru poza werdyktami. To ma być spokojne, schludne narzędzie, które nie rzuca się w oczy i nie odstrasza osoby bez wprawy w internecie.

### Idea przewodnia: cytat jest dowodem

Meritum nie wygląda jak czat: nie ma dymków ani pola przyklejonego do dołu ekranu. Wygląda jak sprawdzona wypowiedź: twierdzenie w cudzysłowie jako nagłówek, przy każdym twierdzeniu werdykt, jedno zdanie wyjaśnienia i dosłowne cytaty ze źródeł. Znakiem rozpoznawczym jest polski cudzysłów „ wysunięty na margines w kolorze atramentu: stoi przy każdym cytacie ze źródła i przy pytaniu obywatela. Cudzysłów zastępuje ramkę: cytat nie leży w pudełku. Hierarchię budują skala i odstęp, nie obrysy ani tła. Informacja o AI pada raz na widok.

**Hasła:** „Sprawdź, zanim podasz dalej.” oraz „Każde ustalenie ma źródło. Gdy źródeł brak, mówimy to wprost.”

---

## 2. Logo

Znak **„Dwa łuki”**: małe „m” z dwóch łuków. Łuki to twierdzenie i źródło, wspólny środkowy trzon to miejsce, w którym się spotykają, a kropka nad nim to ustalenie.

| Plik | Kiedy używać |
|---|---|
| `brand/meritum-mark.svg` | na jasnym tle |
| `brand/meritum-mark-on-dark.svg` | na ciemnym tle |
| `brand/meritum-mark-mono.svg` | strona WWW i panel (wzór dla komponentu `MeritumMark`), druk jednobarwny, grawer, pieczątka |
| `brand/meritum-app-icon.svg` | ikona wtyczki, favicon, avatar w social media |

**Logotyp:** znak + słowo „meritum” małymi literami, krój Archivo, grubość 650, szerokość 112%, światło −0,02 em. Pod spodem opcjonalny podtytuł „obywatelski radar dezinformacji” w Archivo 400, kolor drugorzędny.

**Zasady:**
- Minimalny rozmiar znaku: 14 px na ekranie, 6 mm w druku.
- Pole ochronne: wysokość kropki nad „m” z każdej strony.
- W plikach marki, we wtyczce, na makietach i slajdach trzon i kropka są morskie (`#1D6A86` jasno, `#5DB3CF` ciemno), a łuki w kolorze tekstu.
- Na stronie WWW i w panelu znak jest jednobarwny: trzon, kropka i łuki w kolorze atramentu, jak w `brand/meritum-mark-mono.svg`. Motyw Atrament nie ma koloru akcentu, a zielony trzon znaczyłby „Potwierdzone” przy każdym wyniku, także fałszywym.
- W widżecie na platformach znak ma 14 px i stoi przed słowem „Meritum” w małym nagłówku.
- Gotowe pliki PNG (512, 1024), ikony 16 do 512 px i poziomy logotyp z podtytułem są w `brand/exports/`. Logotyp z podtytułem ma tekst „obywatelski radar dezinformacji”.

**Nie wolno:** obracać znaku, dodawać cienia ani gradientu, zmieniać koloru trzonu na inny niż morski albo atrament, umieszczać znaku obok logotypów platform tak, jakby był ich częścią, ani rozciągać go.

---

## 3. Kolory

Jedna biała powierzchnia, jeden atrament, żadnego koloru akcentu. Kolor na stronie mają tylko werdykty, a czerwień pojawia się wyłącznie przy „Fałszywe”.

### Baza

| Rola | Token | Jasny | Ciemny | Do czego |
|---|---|---|---|---|
| Strona i karta | `--background`, `--card` | `#FFFFFF` | `#0A0A0A` | tło strony, panelu i wszystkiego, co na nich leży; karta ma kolor strony |
| Okienko | `--popover` | `#FFFFFF` | `#161616` | menu, podpowiedź, objaśnienie etykiety |
| Atrament | `--foreground` | `#0A0A0A` | `#EDEDED` | cały tekst główny, przycisk główny, linki, pierścień fokusu |
| Tekst drugorzędny | `--muted-foreground` | `#5A5D62` | `#A1A1A1` | podpisy, etykiety, wydawcy i daty źródeł |
| Ciche pole | `--muted` | `#F3F4F6` | `#161616` | wiersz pod kursorem, pole z wersją wstępną |
| Podniesione tło | `--secondary` | `#EEF0F2` | `#1F1F1F` | plakietki rodzaju źródła, tor paska postępu |
| Linia pola | `--border` | `#E3E5E8` | `#262626` | obrys okienek i tabel; dekoracyjna, nigdy jako jedyna granica pola do pisania |
| Obrys pola | `--input` | `#858A93` | `#6B6B6B` | obrys pola wiadomości i pól formularzy; kontrast do strony 3,5:1 i 3,7:1 (WCAG 1.4.11 wymaga 3:1) |

Szarości trybu jasnego są lekko chłodne, żeby podświetlenie obok bieli nigdy nie wyglądało na beż. Tryb ciemny jest czarny i neutralny: żaden token tła nie ma przewagi niebieskiego.

### Werdykty i stany

Nazwy tokenów zostają (`--verified`, `--contested`, `--scam`); `--verified` jest zielony i oznacza tylko werdykt „Potwierdzone”. Linki i fokus mają własny token `--link` w kolorze atramentu.

| Werdykt lub stan | Token | Jasny | Ciemny | Do czego |
|---|---|---|---|---|
| **Potwierdzone** | `--verified` | `#0B7A4B` | `#4FCB8B` | kolor werdyktu |
| | `--verified-surface` | `#E4F4EC` | `#12301F` | tło plakietki |
| | `--verified-foreground` | `#0A6240` | `#8FE0B5` | tekst plakietki |
| **Wprowadzające w błąd** | `--contested` | `#B7791F` | `#F2C46D` | kolor werdyktu |
| | `--contested-surface` | `#F8EEDB` | `#3A2C10` | tło plakietki |
| | `--contested-foreground` | `#7A4E08` | `#F2C46D` | tekst plakietki |
| **Fałszywe** | `--scam` | `#C8213A` | `#FF6B7D` | kolor werdyktu |
| | `--scam-surface` | `#FBE6E9` | `#43161D` | tło plakietki |
| | `--scam-foreground` | `#9E1A2E` | `#FFB3BE` | tekst plakietki |

**Brak wystarczających dowodów** i **Nie podlega weryfikacji** są neutralne: tło `--secondary`, tekst drugorzędny.

Zmierzony kontrast (WCAG 2.2 AA wymaga 4,5:1 dla tekstu): tekst główny na stronie 19,8:1 jasno i 16,9:1 ciemno; tekst drugorzędny na stronie 6,6:1 i 7,7:1, na cichym polu 6,0:1 i 7,0:1, na podniesionym tle 5,8:1 i 6,4:1; tekst plakietki na jej tle od 6,2:1 do 6,7:1 jasno i od 8,3:1 do 9,2:1 ciemno. `tests/test_tokens_atrament.py` liczy te pary przy każdej zmianie tokenów.

**Stany, które nie są werdyktem** („Doprecyzuj pytanie”, „Poza zakresem”, „Problem techniczny”) mają neutralny kolor, ikonę i zwykły wiersz tekstu. Nigdy nie wyglądają jak plakietka werdyktu, bo awaria nie jest oceną treści.

**Siła podstawy** („Mocna”, „Umiarkowana”, „Słaba”) jest zawsze w kolorze atramentu, jako słowo z trzema kreskami poziomu. Nie dostaje koloru werdyktu.

**Tryb ciemny o wysokim kontraście** (`data-contrast="more"`): czerń `#000000` i biel `#FFFFFF`, tekst drugorzędny i słowa werdyktów z kontrastem co najmniej 7:1, obrysy co najmniej 3:1. Opis w sekcji 10.

**Zasady koloru:**
- Stan nigdy nie jest oznaczony samym kolorem: zawsze ma też słowo („Potwierdzone”, „Fałszywe”) albo znak.
- Na wykresach jakości są co najwyżej 4 kolory: atrament, zieleń, czerwień tylko dla błędów i szary dla przeszłości.
- Przycisk główny jest w kolorze atramentu. Nie ma koloru akcentu: linki są w kolorze atramentu i podkreślone.
- Kolor morski `#1D6A86` zostaje tylko w plikach marki (sekcja 2) i w skórkach platform (sekcja 7). Na stronie i w panelu znak jest w kolorze atramentu.

**Zakazane:** kremowe, beżowe i każde inne kolorowe tło strony; biała karta na tle w innym kolorze; granatowy tryb ciemny; gradienty; fiolet; zielony tekst na czarnym tle w stylu „hakerskim”; neonowe poświaty; granat z czerwienią w stylu urzędowym.

Wtyczka, makiety platform, makieta Discorda i slajdy zostają przy dotychczasowym wyglądzie do osobnej decyzji. Wtyczka ma własne wartości w `extension/widget.css`, a wszystko pod `[data-host]` dostaje dawne kolory z dwóch reguł w `tokens/meritum.css`.

---

## 4. Typografia

| Krój | Rola | Źródło |
|---|---|---|
| **Schibsted Grotesk** (wagi 400–800) | cały interfejs strony i panelu, odpowiedzi | Google Fonts, hostowany lokalnie przez Fontsource |
| **Archivo** (650, szerokość 112%) | tylko słowo „meritum” w logotypie (sekcja 2) oraz slajdy do osobnej decyzji | Google Fonts |
| **Azeret Mono** (400–600) | wyłącznie kod i identyfikatory: ID sprawdzeń i spraw (c_01, #S-1), domeny w katalogu źródeł i tabelach panelu, liczby w metrykach panelu. Daty i godziny na stronie sprawdzenia są w kroju interfejsu z cyframi tabelarycznymi | Google Fonts |

Wszystkie trzy kroje mają polskie znaki. Schibsted Grotesk nie ma osi szerokości, więc nagłówków nie rozciągamy. Mono nigdy nie służy do dekoracji, etykiet ani nagłówków.

### Skala

| Styl | Rozmiar / interlinia | Grubość | Gdzie |
|---|---|---|---|
| Display | 40 px / 1,05 | 700, szerokość 108% | tylko slajdy |
| Werdykt | 28 px / 32 px | 700 | słowo werdyktu na karcie we wtyczce (6.4) |
| Tytuł | 22 px / 28 px | 700 | nagłówek-cytat strony sprawdzenia, nagłówki sekcji |
| Nagłówek strony | 30 px / 36 px (hasło strony głównej od 1024 px: 40 px) | 700, światło −0,02 em | tytuł strony, hasło strony głównej (6.9) |
| Twierdzenie | 16 px / 24 px | 600 | treść twierdzenia pod werdyktem, w cudzysłowie |
| Tekst | 16 px / 24 px | 400 | wyjaśnienie, cytat |
| Mały | 14 px / 20 px | 400–600 | wydawca, data, przesłanki |
| Meta | 12 px / 16 px | 600 | nagłówek widżetu „Meritum”, osie wykresu |

Nic poniżej 12 px. Nagłówki zdaniowe (wielka litera tylko na początku), bez rozstrzelonych WERSALIKÓW, bez etykiet nad nagłówkami.

**W widżecie na platformie** treść dziedziczy krój platformy (np. systemowy na X, Reddit Sans na Reddicie). Archivo zostaje tylko w nagłówku „Meritum” i plakietce werdyktu.

---

## 5. Odstępy, siatka, kształty

- **Siatka 4 px.** Typowe odstępy: 4, 8, 12, 16, 24, 32, 40, 64 px.
- **Jedna powierzchnia.** Strona jest biała i wszystko leży bezpośrednio na niej. Wynik nie jest kartą: to tekst na stronie. Tło mają tylko małe elementy: plakietki, tor paska postępu, wiersz pod kursorem i ciche pole (`--muted`) z wersją wstępną odpowiedzi.
- **Układ strony.** Treść ma szerokość do 1152 px z marginesem 24 px (16 px na telefonie). Strony robocze mają kolumnę do 720 px od lewej krawędzi belki i przyklejoną szynę 320 px po prawej na to, co należy do strony: historię sprawdzeń albo spis treści. Na telefonie szyna schodzi pod treść.
- **Odstępy zamiast linii.** Sekcje dzieli odstęp (40–64 px), a bloki w sekcji 16–24 px. Nie ma linii pod belką, nad stopką ani linii między sekcjami czy wierszami list.
- **Promienie:** pola i wiersze 8 px, okienka 10 px, przyciski i plakietki w pełni zaokrąglone (pigułki). W widżecie promień zgodny z platformą (sekcja 7).
- **Głębia:** nic na stronie nie ma cienia. Cień dostaje tylko to, co się unosi: menu, objaśnienie etykiety, powiadomienie. Pole wiadomości ma obrys 1 px (`--input`) i nie ma cienia.
- **Zakazane:** ramki w ramce (obrysowany blok w obrysowanym albo wypełnionym polu), biała karta na kolorowym tle, pasek koloru wzdłuż jednego boku karty, siatki identycznych kart z ikoną na górze, szkło i rozmycie tła, ozdobne kształty.

---

## 6. Komponenty

Kod React (shadcn/ui, Tailwind v4) leży w `components/meritum/`, wersja dla Shadow DOM wtyczki w `extension/widget.css`, dane opisują kontrakty (źródłem prawdy jest repozytorium meritum-core, a w `contracts/` leży kopia pobierana skryptem `contracts/sync.sh`, której nie edytuje się ręcznie), teksty `copy/pl.json`. Bot na Discordzie i SMS nie mają własnego wyglądu: korzystają z tych samych tekstów. Bot odpowiada jedną wiadomością z osadzeniem: pole na każde twierdzenie (werdykt, twierdzenie, jeden cytat ze źródłem z datą, siła), kolor osadzenia z najpoważniejszego werdyktu, a pod spodem przycisk-link „Pełna karta” (`discord.card_button`). Za długi wynik skraca cytaty, nie twierdzenia. Odpowiedź jest prywatna (efemeryczna), chyba że użytkownik wybierze opcję „publiczne” (`discord.public_option`). Każdy kanał przy pierwszym kontakcie mówi, że odpowiada system AI (`ai_notice`). Odpowiedź SMS podaje sam werdykt głównego twierdzenia, bez linku, żeby zmieścić się w 70 znakach UCS-2 i uniknąć filtrowania przez operatora; opcją jest GSM-7 bez polskich znaków i 160 znaków (`sms`). Makieta Discorda dla jury leży w repozytorium meritum-mocks i woła to samo API co bot. Wygląd bierze ze skórki `[data-host="discord"]` w `tokens/meritum.css`, a teksty z `discord`: podpis wiadomości użytkownika, szablony twierdzenia bez daty albo bez siły i liczbę twierdzeń w trzech formach. Karta wyniku w skórkach pięciu platform: `demo/widgets/`, cały przepływ „Sprawdź” na makietach: `demo/live/`.

### 6.1 Formularz „Sprawdź informację” (strona WWW, kanał podstawowy)
Jedna kolumna, działa od 320 px szerokości. Na stronie WWW formularz jest polem wiadomości na stronie nowego sprawdzenia i pod gotowym wynikiem (6.8): pole i „Sprawdź” w jednej ramce z obrysem 1 px, tytuł i etykieta zostają dla czytnika ekranu, a historia sprawdzeń stoi w szynie. Punkty poniżej opisują treść; układ z tytułem, etykietą nad polem i przyciskiem nagrania pod polem (`CheckForm`) zostaje tylko w okienku wtyczki.
1. Tytuł „Sprawdź informację” i jedno zdanie, co się stanie.
2. Pole „Tekst albo link” (do 4000 znaków), przyjmuje wklejony tekst albo pełny adres zaczynający się od http:// albo https:// (do 2083 znaków, jak `CheckRequest.url`). Pod nim drugorzędny przycisk „Albo nagranie (plik audio)” (`form.audio_label`). Nad polem jedno zdanie, że odpowiada system AI (`ai_notice.first_contact`).
3. Przycisk główny „Sprawdź”, aktywny zawsze poza wysyłką. Za krótki tekst, za długi albo błędny link dają po kliknięciu komunikat pod polem (`errors`). W trakcie: „Sprawdzamy…” i pasek analizy (6.3).
4. Pod przyciskiem informacja o prywatności: konto nie jest potrzebne, maskowanie oczywistych danych osobowych, termin usunięcia zapisu, link „Usuń moje sprawdzenia”.
5. W okienku wtyczki pod formularzem, a na stronie WWW w szynie (6.8), lista „Twoje sprawdzenia” (`history`): sprawdzenia z tej karty przeglądarki, od najnowszego; kliknięcie otwiera kartę wyniku. Bez logowania lista pochodzi z sessionStorage, a notatka mówi, że historia jest tylko w tej przeglądarce: w tej karcie i w kartach z niej otwartych (przeglądarka kopiuje sessionStorage do takich kart). Pusta lista pokazuje `history.empty`.
6. Przy liście opcjonalne logowanie (`account`): dwa przyciski drugorzędne „Zaloguj się kontem Google” i „Zaloguj się kontem Microsoft” oraz zdanie, że logowanie nie jest potrzebne. Po zalogowaniu historia jest na serwerze, a w miejscu przycisków są „Usuń moją historię”, „Usuń konto i historię” i „Wyloguj się”.

Błędy pod polem, słowami z `copy/pl.json` (`errors`), bez czyszczenia wpisanej treści.

### 6.2 Przycisk „Sprawdź” we wtyczce (kanał dodatkowy)
Znak Meritum 18 px + słowo „Sprawdź” w pasku akcji posta. Stany: spoczynek (kolor ikon platformy), najechanie (tło `#E1EDF2`, tekst `#13506A`), w toku, „Sprawdzono”. Treść posta wysyłamy dopiero po kliknięciu. Wynik pojawia się pod postem jako karta wyniku (6.4). Okienko wtyczki z paska przeglądarki ma to samo pole co formularz WWW, więc ten sam tekst można sprawdzić w obu kanałach i dostać ten sam wynik.

### 6.3 Pasek analizy
Na stronie WWW obywatel widzi pasek postępu (shadcn `Progress`), licznik „Krok n z m” (`analysis.step_of`) i nazwę bieżącego kroku. Gdy wyszukiwania biegną równolegle, pasek podaje nazwy wszystkich kroków w toku. Pełna lista kroków otwiera się na żądanie pod „Pokaż kroki” (`analysis.show_steps`, shadcn `Collapsible`): kółko czeka, kręci się, gotowe, pominięte albo nieudane. Każdy stan czytnik ekranu dostaje słowem z `analysis.step_status`; przy pominiętym i nieudanym kroku to słowo jest też widoczne obok nazwy, więc znak i kolor nie są jedyną informacją. Zmianę kroku ogłasza region `aria-live`. Pasek nie ma obramowania ani tła karty.

Kody i teksty kroków: `receive`, `fetch_url`, `transcribe_audio`, `screen_injection`, `extract_claims`, `search_corpus`, `search_web`, `search_fact_checks`, `assess_evidence`, `verify_citations`, `write_answer`, `save_record` (`copy/pl.json`, `analysis.steps`). „Pobieramy stronę z linku” jest pominięte, gdy wklejono sam tekst, a „Zamieniamy nagranie na tekst”, gdy nie ma nagrania. „Szukamy świeżych publikacji w zatwierdzonych serwisach” rusza zawsze, razem z bazą źródeł; gdy baza wystarczy, odpowiedź na ten krok nie czeka. Odpowiedź przychodzi strumieniem: wersja wstępna stoi pod paskiem w cichym polu z dopiskiem `analysis.draft` i nie pokazuje werdyktu, dopóki cytaty nie przejdą weryfikacji. We wtyczce pasek analizy zostaje listą kroków jak dotąd.

### 6.4 Karta wyniku
Jeden wynik na sprawdzenie, a w nim lista twierdzeń. Na stronie WWW wynik nie ma tła ani obramowania; w widżecie ma tło `--card`, obramowanie 1 px i promień platformy.
- **Podsumowanie:** „Co sprawdziliśmy” z liczbą twierdzeń (`result.claims_count`) i licznikami werdyktów jako plakietkami.
- **Lista twierdzeń:** shadcn `Accordion`, wszystkie wiersze domyślnie rozwinięte. Wiersz to plakietka werdyktu (`VerdictBadge` sm) w stałej kolumnie, twierdzenie w cudzysłowie w stylu Twierdzenie i strzałka. Plakietka stoi obok wyzwalacza, nie w nim, żeby mogła się objaśnić (6.10). Wiersz podświetla się przy najechaniu (`--muted`) i ma kursor wskazujący; między wierszami nie ma linii. Od 576 px szerokości listy treść rozwinięcia wyrównuje się do tekstu twierdzenia, węziej stoi pod plakietką.
- **Werdykt:** słowo („Potwierdzone”, „Fałszywe”, „Wprowadzające w błąd”, „Brak wystarczających dowodów”, „Nie podlega weryfikacji”) w plakietce w kolorach werdyktu; dwa nierozstrzygające są neutralne. Objaśnienie z `verdict_hint` pokazuje się po najechaniu, fokusie albo dotknięciu plakietki. We wtyczce werdykt zostaje słowem w stylu Werdykt, bez pigułki.
- **Wyjaśnienie:** 1–3 zdania. Bez podpisu o AI przy każdym twierdzeniu: informacja o AI pada raz (pod przełącznikiem ograniczeń albo na stronie nowego sprawdzenia). `result.explanation_hint` nie jest już pokazywany.
- **Na czym się opieramy:** każde źródło jako dowód: najpierw dosłowny fragment w stylu Tekst, z cudzysłowem „ wysuniętym na margines w kolorze atramentu, bez tła i ramki; pod nim przypis: tytuł (link w kolorze atramentu, podkreślony), wydawca i data publikacji, a rodzaj i poziom źródła jako plakietki, które się objaśniają (6.10). We wtyczce cudzysłów i link zostają w kolorze morskim. Źródło z wyszukiwania w sieci ma dopisek „znalezione w wyszukiwaniu w zatwierdzonych serwisach”.
- **Siła podstawy:** tylko przy werdyktach rozstrzygających. Słowo i trzy kreski poziomu; objaśnienie poziomu (`strength_hint`) pokazuje się jak przy plakietkach. Przesłanki słowami są dostępne na żądanie: liczba niezależnych wydawców zgodnych z werdyktem, ile z nich urzędowych, data najnowszego źródła i data, której dotyczy twierdzenie (`result.newest`), czy źródła są zgodne. Przy sprzecznych źródłach nie ma siły: werdykt to „Brak wystarczających dowodów”, cytaty obu stron stoją obok siebie, a nad nimi jest jedno zdanie, czym się różnią (`result.conflict`).
- **Czego nie udało się ustalić:** obowiązkowe przy „Brak wystarczających dowodów”.
- **Oś czasu dowodów:** cytaty według wymowy w trzech grupach z nagłówkami `result.stance` (wspierają, przeczą, dają kontekst), z datą twierdzenia i datami publikacji (wiersz `CitationItem` z `showDate={false}`: linia wydawcy podaje wydawcę, rodzaj i poziom źródła bez daty, bo oś pokazuje ją sama); dowód zastąpiony nowszym jest na osi oznaczony (`result.superseded` z datą nowszego dokumentu, `result.superseded_undated`, gdy wynik jej nie podaje). Pod osią „Co zmieniłoby werdykt” (`result.what_would_change`).
- **Kontekst:** ocena fact-checkera z ClaimReview z linkiem (`result.claim_review`), zawsze jako kontekst, nigdy jako cytat. Przy nagraniu transkrypcja z podpisem (`result.transcript_hint`).
- **Ostrzeżenia:** dowód nieaktualny, podobieństwo do znanego incydentu z bazy organizatora albo EUvsDisinfo, z nazwą bazy, albo link do serwisu z takiej bazy (jako kontekst, nie podstawa oceny; przy EUvsDisinfo zastrzeżenie `result.euvsdisinfo_disclaimer`) i neutralna informacja, że treść pochodzi od podmiotu z oficjalnej listy sankcji UE. Każde w osobnym wierszu, bez czerwieni. Żadne nie zmienia werdyktu.
- **Technika:** nazwa techniki manipulacji + podpowiedź „jak rozpoznać?”, gdy dotyczy.
- **Stopka:** „Ograniczenia” z liczbą, zwinięte pod jednym przełącznikiem razem z informacją o użyciu AI; stan przekazania moderatorom (`escalation`: zalecane, przekazane, dołączone do sprawy; przy nieudanym zapisie sprawy — `escalation.not_saved`, bez numeru sprawy); „Zgłoś błąd” (`result.report_error`) i „Jak działa Meritum” jako przyciski z ikonami.
- **Pojawienie się:** wynik wchodzi z 8 px w 0,5 s; wiersz listy rozwija się i zwija w 0,2 s.

Gdy wynik nie jest werdyktem (doprecyzuj, poza zakresem, problem techniczny), karta ma tylko ikonę, tytuł stanu i komunikat z `status_hint`. Żadnej plakietki, żadnych źródeł.

### 6.5 Kolejka moderatorów (panel)
Do panelu logują się osoby z kontem nadanym przez administratora, w roli moderatora, analityka albo administratora (`moderation.role`). Lista spraw: ID w mono (#S-1), krótki opis, powody słowami (sprawa może mieć kilka: „brak wystarczających dowodów”, „sprawa wysokiego ryzyka” z dopasowanym tematem, „powtarzające się pytanie bez odpowiedzi”, „zgłoszenie błędu przez użytkownika”), twierdzenia sprawy, liczba podobnych pytań i różnych pytających (ta podnosi priorytet), pierwsze i ostatnie wystąpienie, stan. Podobne twierdzenia trafiają do jednej sprawy, nie tworzą nowych. Panel nie pokazuje identyfikatorów z Discorda ani numerów telefonów. Panel pokazuje też jakość: medianę czasu odpowiedzi, odsetek wstrzymań, błędy wyszukiwania, wykryte próby wstrzyknięcia poleceń i szacowany koszt. Wykresy według zasad z sekcji 3: etykiety przy liniach, bez kafelków KPI z ikonami. Analityk i administrator mają też stronę ewaluacji (`evaluation`): lista przebiegów z miernikami, nowy przebieg na golden secie, dodanie zestawu (JSON albo CSV) i porównanie dwóch przebiegów z listą przypadków, które zmieniły wynik.

### 6.6 Powiadomienia
W aplikacji WWW i w panelu powiadomienie pojawia się od razu jako toast (Sonner), w rogu, bez czerwieni. Toast, na który ktoś nie zareagował, zostaje w skrzynce pod ikoną dzwonka jako nieprzeczytany; licznik nieprzeczytanych przy ikonie (`notifications`). Kliknięcie otwiera link z powiadomienia i oznacza je jako przeczytane. Teksty według rodzaju (`notifications.kind`), retencja jak w zapisie sprawdzenia.

### 6.7 Komponenty poza zakresem MSZ
`ContextCard` (notatka i ostrzeżenie o oszustwie), `CampaignRotation`, `BotDefenseTelemetry` i `QuickReportPopover` leżą w `components/legacy/` jako pozostałość wcześniejszej wersji produktu (wątek NASK i notatek społeczności). Nie używamy ich w demo ani w materiałach na konkurs MSZ.

### 6.8 Strona sprawdzenia (strona WWW)
Jedno sprawdzenie to jedna strona z własnym adresem, który można wysłać dalej. Strona nie jest rozmową: jest bez dymków, bez podpisów mówiących i bez pola przyklejonego do dołu ekranu. Komponenty: nagłówek-cytat, `Composer`, `CheckHistory` (`components/meritum/`), teksty `check_page`, `conversation` i `form`.
- **Układ:** kolumna do 720 px i szyna 320 px (sekcja 5). W kolumnie od góry: nagłówek-cytat, pasek analizy (6.3) albo wynik (6.4), a pod gotowym wynikiem pole „Sprawdź kolejną informację” (`check_page.next`).
- **Nagłówek-cytat:** słowa obywatela bez zmian jako nagłówek h1 w stylu Tytuł, wyrównany do lewej, z otwierającym cudzysłowem „ wiszącym na marginesie w kolorze atramentu. Nagranie i obraz stoją tu jako `conversation.audio_question` i `conversation.image_question` z nazwą pliku.
- **Nowe sprawdzenie:** osobna strona z tytułem `form.title`, zdaniem `form.lead`, polem i 2–3 przykładowymi twierdzeniami z `conversation.examples` jako przyciskami. Przykłady to twierdzenia, które system sprawdza i rozstrzyga, nigdy takie, które kończą się „Nie podlega weryfikacji”. Pod przykładami stoi informacja o AI (`ai_notice.first_contact`), jedyna na ekranie. Wysłanie twierdzenia przenosi na stronę tego sprawdzenia, pod jego własny adres.
- **Pole wiadomości (`Composer`):** zwykłe pole w treści strony z obrysem 1 px i promieniem pola; nie jest przyklejone do ekranu i przewija się razem z treścią. Rośnie z treścią do ok. 8 wierszy, Enter wysyła, Shift+Enter dodaje wiersz. Licznik znaków pojawia się dopiero przy pisaniu. Na telefonie pole ma 16 px, żeby przeglądarka nie powiększała strony, i rośnie najwyżej do ok. 4 wierszy. Placeholder z przykładem (`form.input_placeholder`) jest domyślny; pod gotowym wynikiem aplikacja podaje `conversation.next_placeholder`. Przycisk nagrania i obrazu aplikacja wstawia w miejsce `tools`; wybrany plik zastępuje pole jako `Attachment` ze zdaniami o dostawcy, koszcie, retencji, limitach i ostrzeżeniu AI z `form`, zanim cokolwiek wyślemy.
- **Historia w szynie (`CheckHistory`):** nad listą przycisk „Nowe sprawdzenie” (`check_page.new`). Każde sprawdzenie z tej karty przeglądarki (sessionStorage) to wiersz: treść pytania w dwóch liniach, pod nią plakietka werdyktu głównego twierdzenia i godzina; sprawdzenie w toku pokazuje stan słowem. Wiersze nie mają linii między sobą i podświetlają się przy najechaniu. Pod listą notatka `history.session_note`. Blok logowania zostaje opcjonalny.
- **Ruch:** wynik wchodzi z 8 px w 0,5 s (`--animate-rise`), przyciski przy wciśnięciu ustępują o 1 px. Przy „ogranicz ruch” bez animacji i bez płynnego przewijania.
- **Dostępność:** stronę otwiera nagłówek h1 z pytaniem; postęp i wynik ogłasza region `aria-live`; pole wiadomości ma ukrytą etykietę `form.input_label`, a ramka pokazuje pierścień fokusu 2 px.

### 6.9 Powłoka strony, strona główna i „Jak działa” (strona WWW)
- **Belka:** przyklejona do góry, w kolorze strony, bez linii pod spodem. Po lewej znak i logotyp, obok „Sprawdź” i „Jak działa” (`nav`) z ikonami; po prawej menu „Wygląd” (sekcja 10), powiadomienia (6.6) i konto: przycisk „Zaloguj się” albo awatar z menu (usuń historię, wyloguj się). Poniżej 768 px linki chowają się w menu.
- **Stopka:** jeden wiersz bez linii nad sobą: znak, „Jak działa Meritum”, „Katalog źródeł”, „Prywatność” i rok.
- **Strona główna:** bez pola. Po lewej hasło „Sprawdź, zanim podasz dalej.” w stylu Nagłówek strony, zdanie `form.lead`, przycisk główny „Sprawdź informację” ze strzałką i drugi „Jak działa Meritum”. Po prawej prawdziwy widok wyniku z podpisem `check_page.sample`, bez ramki i bez tła: pierwsze twierdzenie jest całe i czytelne, a początek następnego wygasza się u dołu maską, na znak, że wynik ma ciąg dalszy. Przykład nie reaguje na kliknięcia. Niżej trzy zasady z ikonami i legenda pięciu werdyktów z objaśnieniami.
- **„Jak działa”:** kolumna ze spisem treści w szynie (`nav.on_page`). Kolejność sekcji to droga pytania: najpierw kroki z paska analizy ponumerowane 01–12 (`method.path`), potem pięć werdyktów z objaśnieniami (`method.verdicts`), katalog źródeł, mierniki jako duże liczby, a na końcu zasady w wierszach, które się rozwijają (`method.details`). Katalog źródeł to lista, nie tabela: domena w mono, wydawca, plakietki rodzaju i poziomu, powód kwalifikacji i licencja.
- **Ikony:** Lucide, obrys 2 px, w kolorze tekstu: przy pozycjach belki, w przyciskach i przed nagłówkami sekcji. Nigdy jako kafelek nad tekstem.

### 6.10 Etykiety, które się objaśniają
Każda mała etykieta tłumaczy się jednym zdaniem: werdykt (`verdict_hint`), rodzaj źródła (`source_kind_hint`), poziom źródła (`source_tier_hint`) i siła podstawy (`strength_hint`). Objaśnienie otwiera się po najechaniu, po fokusie z klawiatury i po dotknięciu, a zamyka po opuszczeniu, klawiszem Esc i po dotknięciu obok. Komponent stoi na shadcn `Popover`, bo `Tooltip` nie otwiera się dotykiem. Objaśnienie nie znika, gdy wskaźnik przejdzie na nie z etykiety (WCAG 1.4.13). Etykieta jest przyciskiem i jako jedyny element klikalny ma kursor pomocy zamiast wskazującego; nie wolno jej wkładać do innego przycisku ani linku.

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
- Animujemy przezroczystość, przesunięcie i skalę; wyjątek to rozwijanie wiersza listy (wysokość od 0).
- Wciśnięcie przycisku i rozwinięcie wiersza trwają krócej (0,15 s i 0,2 s), bo widać je przy każdym sprawdzeniu (6.8).
- Wszystko klikalne ma kursor wskazujący i przejście koloru w 0,15 s. Ikona w przycisku ugina się przy wciśnięciu (skala 0,82), a strzałka w przycisku głównym przesuwa się o 3 px w stronę, w którą prowadzi.
- Bez pulsujących kropek, bez animacji w pętli (poza kółkiem „w toku”).
- Przy włączonym „ogranicz ruch” w systemie wszystkie animacje skracają się do zera, także ruch ikon.

---

## 10. Dostępność

WCAG 2.2 AA w obu trybach, także na tle cudzych feedów. Werdykty oznaczone słowem, nie tylko kolorem. Widoczny pierścień fokusu (2 px, kolor atramentu). Klawisz Esc zamyka okienko i oddaje fokus przyciskowi. Wynik ogłasza region `aria-live`. Formularz działa na telefonie bez przewijania w poziomie. Polskie teksty są dłuższe niż angielskie, więc komponenty muszą wytrzymać długie etykiety, np. „Brak wystarczających dowodów”.

**Menu „Wygląd”** w belce (`display` w `copy/pl.json`) daje dwa ustawienia bez szukania ich w przeglądarce:
- **Motyw:** jasny, ciemny albo ciemny o wysokim kontraście. Bez zapisanego wyboru strona idzie za systemem, a tryb ciemny bierze wartości wysokiego kontrastu, gdy system prosi o większy kontrast. W wysokim kontraście okienka mają obrys 1 px, a fokus obrys 3 px. Tokeny obu ustawień są w `tokens/display.css` (powstaje w design-system#147), importowanym po `tokens/meritum.css`.
- **Rozmiar tekstu:** domyślny, 112,5%, 125% albo 150%, jako procent na elemencie `html` (`data-text`). Procent mnoży rozmiar ustawiony w przeglądarce i skaluje wszystko w `rem`: tekst, odstępy i szerokości, jak Ctrl i plus. W kodzie rozmiary tekstu i odstępy podajemy w `rem`, nie w pikselach; piksele w tym dokumencie to wartości przy domyślnym rozmiarze.

Wybór zapisuje się w przeglądarce. Co musi wytrzymać każda strona:
- **WCAG 1.4.4 (zmiana rozmiaru tekstu):** tekst powiększony do 200% powiększeniem przeglądarki albo rozmiarem czcionki, bez utraty treści i funkcji. 150% z menu to nie jest górna granica.
- **WCAG 1.4.10 (dopasowanie do ekranu):** brak przewijania w poziomie przy szerokości 320 px.
- **Warunek Meritum, ostrzejszy od obu:** punkty łamania układu nie zależą od rozmiaru tekstu z menu, więc strona mieści się bez przewijania w poziomie także przy 150% na szerokości 320 px.
- **WCAG 2.4.11 (fokus niezasłonięty):** belka jest przyklejona, więc strona ma `scroll-padding-top` co najmniej o jej wysokości i element z fokusem nigdy nie chowa się pod belką.
- **WCAG 1.4.13 (treść po najechaniu):** objaśnienie etykiety (6.10) nie znika, gdy wskaźnik przejdzie z etykiety na objaśnienie, i zamyka się klawiszem Esc.

---

## 11. Slajdy i materiały marketingowe

- Tło slajdu `#F6F7F5` albo `#0B0F12` (jeden tryb na całą prezentację).
- Jedna myśl na slajd, tytuł do 2 linii, Display 40 px lub większy.
- Zamiast zdjęć stockowych: prawdziwe zrzuty interfejsu Meritum (strona, wtyczka, panel) w dużej skali.
- Zdjęcia tylko jako tło świata, w którym krąży pogłoska (pasażerowie z telefonami, ulica, katalog, prasa): z Unsplash albo innej licencji pozwalającej na użycie komercyjne, z autorem w podpisie, najwyżej jedno na slajd i nigdy jako produkt, nasi użytkownicy czy zespół. Bez klisz: laptopy, kłódki, tarcze, kaptury hakerów.
- Ikony z Lucide (ta sama biblioteka co frontend), obrys 2 px, w kolorze akcentu, przy punktach listy i w kafelkach architektury. Nigdy jako duży element nad tekstem karty ani w siatce identycznych kafelków.
- Wykresy według zasad z sekcji 3: etykiety przy liniach, czerwień tylko dla błędów.
- Logo w lewym górnym albo dolnym rogu, 24–32 px.
- W przykładach używamy prawdziwych, sprawdzalnych źródeł z korpusu. Nie wymyślamy źródeł, cytatów ani wyników testów.
- Nie piszemy o współpracy z MSZ, NASK ani mediami, dopóki jej nie ma; piszemy „gotowe do integracji z…”.

---

## 12. Polecenie dla agenta AI (kopiuj i wklej)

```
Projektujesz widok strony albo panelu Meritum — obywatelskiego radaru dezinformacji
(strona WWW do sprawdzania informacji, panel moderatora). Trzymaj się DESIGN_SYSTEM.md.
Wtyczka, makiety platform i slajdy mają osobne zasady w sekcjach 7 i 11.

Produkt: obywatel wkleja tekst albo link, system wyodrębnia twierdzenia i dla każdego
podaje werdykt (Potwierdzone, Fałszywe, Wprowadzające w błąd, Brak wystarczających
dowodów, Nie podlega weryfikacji) z dosłownym cytatem, wydawcą, datą i linkiem,
z przesłankami i siłą podstawy. Gdy dowodów brakuje, wstrzymuje się i mówi, czego nie ustalił.
Styl: „Atrament”: spokojne, schludne narzędzie, które nie rzuca się w oczy. Jedna biała
powierzchnia, dużo powietrza, bez kart, bez linii między sekcjami, bez ramek w ramkach.
Strona nie wygląda jak czat: bez dymków i bez pola przyklejonego do dołu.
Kolory: strona i karta #FFFFFF, tekst #0A0A0A, tekst drugorzędny #5A5D62, ciche pole #F3F4F6,
obrys pola #858A93; tryb ciemny: strona #0A0A0A, tekst #EDEDED. Bez koloru akcentu:
przycisk główny, linki i fokus w kolorze tekstu. „Potwierdzone” #0B7A4B,
„Wprowadzające w błąd” #B7791F, „Fałszywe” #C8213A (tylko tam), brak dowodów i stany
techniczne neutralne.
Kroje: Schibsted Grotesk (cały interfejs), Azeret Mono (tylko ID, domeny, liczby w panelu).
Logo: brand/meritum-mark-mono.svg (małe „m” z dwóch łuków, całe w kolorze tekstu) i słowo
„meritum” w Archivo.
Układ: kolumna 720 px i szyna 320 px; przyciski to pigułki; cień tylko na tym, co się unosi.
Komponenty: Meritum, potem shadcn/ui, czasem darmowy blok shadcnblocks. Ikony Lucide.
Ton: opisujemy twierdzenia, nie ludzi; każde ustalenie ze źródłem; uczciwa niepewność;
zdania proste, bez wykrzykników i emoji.
Zakazane: kremowe i kolorowe tła, granatowy tryb ciemny, gradienty, fiolet, neon, styl
urzędowy, kafelki z ikonami, pasek koloru z boku karty, etykiety WERSALIKAMI nad nagłówkami,
wymyślone źródła i cytaty, liczby bez dopisku „dane symulowane” albo bez danych do odtworzenia.
```

---

## 13. Kto czego używa

### Strona WWW i panel (React)
- `components/meritum/`: komponenty React (shadcn/ui) typowane kontraktami: `CheckForm` i `CheckHistory` (6.1), `Composer`, nagłówek-cytat i `Attachment` (6.8; `Question`, `Reply` i `Welcome` znikają razem z widokiem rozmowy w design-system#150), `CheckButton` (6.2), `AnalysisSteps` (6.3), `ResultCard` z `VerdictBadge`, `CitationItem` i `StrengthMeter` (6.4), `ModerationQueue` (6.5). Instalacja i podgląd: `components/meritum/README.md`.
- `tokens/meritum.css`: tokeny strony i panelu; skórki platform pod `[data-host]` trzymają w nim dawne wartości, a wtyczka ma własne w `extension/widget.css`.

### Wtyczka Chrome (programista)
- `extension/widget.css`: style widżetu dla Shadow DOM (`:host`), tokeny jasne i ciemne, skórki platform przez `:host([data-host=…])`. Karta ma tę samą tożsamość co komponenty React: werdykt jako słowo `.m-verdict` w skali 28 px, cytat `.m-frag` z wiszącym „ i bez pola, tekst 16 px, informacja o AI raz w stopce.
- `extension/manifest.json` i `extension/reference/`: referencyjny skrypt (MV3) bez frameworka: wykrywa platformę, znajduje posty selektorami z `demo/platforms/SELECTORS.md`, wstawia przycisk we własnym Shadow DOM i wykrywa motyw gospodarza. Przycisk „Sprawdź” wysyła post dopiero po kliknięciu, pasek analizy i karta wyniku (`reference/card.js`) mają tę samą budowę co komponenty React. Na razie woła atrapę API (`reference/api.js`); połączenie z prawdziwym API opisuje `extension/README.md`.
- `extension/popup/`, `extension/onboarding/`, `extension/icons/`. Opis techniczny po angielsku: `extension/README.md`.

### Backend (FastAPI)
- `contracts/` (`examples.json`, `meritum.schema.json`, `meritum.ts`): kopia wygenerowanych kontraktów z meritum-core (pakiet `src/meritum_core/checks/contracts/`), odświeżana przez `contracts/sync.sh`, nie edytować ręcznie. W meritum-core są to modele Pydantic v2 dla API, strony, wtyczki i panelu (zapytanie, wynik sprawdzenia, twierdzenie, cytat, źródło, przesłanki, status analizy, zapis przebiegu, sprawa moderatora, wpis katalogu źródeł). Reguły z treści zadania MSZ są w modelach:
  - werdykt rozstrzygający (potwierdzone, fałszywe, wprowadzające w błąd) wymaga cytatu i jawnych przesłanek;
  - siła podstawy wynika z przesłanek według jednej stałej reguły, nie z deklaracji modelu, i mają ją tylko werdykty rozstrzygające;
  - zgodność wynika z wymowy cytatów; sprzeczne wiarygodne źródła dają „brak wystarczających dowodów” z cytatami obu stron i bez siły;
  - niezależne źródła liczymy według identyfikatora wydawcy z katalogu, nie według strony, i tylko wśród cytatów zgodnych z werdyktem;
  - wiek dowodu liczymy od daty, której dotyczy twierdzenie (z zapisanym pochodzeniem tej daty), z progiem z katalogu i ważnością każdego cytatu; obowiązujący akt prawny, strona urzędowa aktualizowana w miejscu i dowód o zdarzeniu z przeszłości nie są nieaktualne; dowód zastąpiony nowszym w dacie twierdzenia nie tworzy rozbieżności i nie liczy się do siły;
  - „brak wystarczających dowodów” musi powiedzieć, czego nie ustalono;
  - awaria, prośba o doprecyzowanie i pytanie poza zakresem nie są werdyktami i nie mają twierdzeń; „poza zakresem” to tylko nieobsługiwany typ wejścia albo prośba spoza informacji, a każde twierdzenie o fakcie dostaje werdykt;
  - powiadomienie trafia do jednej sesji albo jednego zalogowanego użytkownika i ma link w aplikacji (`Notification`);
  - zalecenie przekazania sprawy moderatorowi różni się od faktycznego przekazania;
  - cytat przechodzi tylko wtedy, gdy fragment znaleziono w źródle dosłownie;
  - pamięć wyników przechowuje tylko część merytoryczną i nigdy problemu technicznego, a przekazanie moderatorom liczymy przy każdym zapytaniu.
- `contracts/sync.sh` kopiuje z meritum-core `meritum.schema.json` (JSON Schema), `meritum.ts` (typy TypeScript), `examples.json` i kod modeli; generowanie i testy reguł (przykłady, odrzucanie złych danych) są w CI meritum-core, a CI tego repo sprawdza sumy kontrolne kopii.
- `copy/pl.json`: wszystkie teksty interfejsu: formularz, werdykty z podpowiedziami, siła podstawy, stany techniczne, przekazanie moderatorom, ostrzeżenia o statusie źródła, kroki analizy, techniki manipulacji z „jak rozpoznać”, kolejka moderatorów, historia sprawdzeń, logowanie, SMS, Discord, informacja o AI, polityka prywatności kanałów, powiadomienia, strona ewaluacji, oś czasu dowodów, „Zgłoś błąd”, błędy, kody awarii (`failure_code`), spraw poza zakresem (`out_of_scope_code`) i ograniczeń (`limitation_code`), „co zmieniłoby werdykt” (`would_change_verdict`), podstawa dopasowania (`match_basis`). Klucze odpowiadają kodom z kontraktów, a `tests/test_contract_copy.py` sprawdza, czy każdy kod ze schematu ma tekst.

### Prezentacje i film (cały zespół)
- `presentation/`: szablon PPTX, slajdy HTML, zrzuty, grafiki social i instrukcja `presentation/README.md`. Obecne pliki pokazują jeszcze stary produkt na dwa konkursy i trzeba je wygenerować od nowa pod deck MSZ (do 12 slajdów, film do 3 minut).
- `brand/exports/`: logo w PNG (512, 1024), ikona aplikacji 16 do 512 px, poziomy logotyp z podtytułem i bez, jasny i ciemny.

### Pokaz
- `demo/live/<platforma>/`: makiety X, Facebooka, Instagrama, Reddita i TikToka, na których skrypt wtyczki działa bez instalowania. Jury może tam kliknąć „Sprawdź” bez konfiguracji przeglądarki.
- `demo/platforms/`: te same makiety bez Meritum, do testowania prawdziwej wtyczki.
- Makieta Discorda (repozytorium meritum-mocks): jury sprawdza kanał Discord bez dołączania do serwera; strona woła to samo API co prawdziwy bot. Razem z formularzem WWW to główna ścieżka demo, a wtyczka jest opcjonalna.

## 14. Pliki

| Ścieżka | Zawartość |
|---|---|
| `DESIGN_SYSTEM.md` | ta specyfikacja |
| `tokens/meritum.css` | tokeny CSS i `@theme` dla Tailwind v4 + shadcn/ui, tryb ciemny, skórki platform |
| `tokens/display.css` | ustawienia wyświetlania strony i panelu: tryb ciemny o wysokim kontraście i skala rozmiaru tekstu |
| `components/meritum/` | komponenty React: `CheckForm`, `CheckHistory`, `CheckButton`, `AnalysisSteps`, `ResultCard`, `VerdictBadge`, `CitationItem`, `StrengthMeter`, `ModerationQueue`, `MeritumMark` |
| `components/legacy/` | komponenty z wcześniejszego zakresu (NASK, notatki społeczności), poza produktem dla MSZ |
| `contracts/` | kopia kontraktów z meritum-core, odświeżana skryptem `sync.sh`, nie do ręcznej edycji: Pydantic, JSON Schema, typy TS, przykłady |
| `copy/pl.json` | teksty interfejsu |
| `extension/` | zestaw wtyczki Chrome: style Shadow DOM, skrypt referencyjny, popup, onboarding, ikony |
| `brand/` | logo w SVG, `brand/exports/` w PNG i logotyp |
| `presentation/` | szablon PPTX, slajdy HTML, zrzuty, grafiki social, instrukcja |
| `demo/live/` | interaktywne makiety platform na pokaz |
| `demo/platforms/` | czyste makiety platform i `SELECTORS.md` |
| `demo/widgets/`, `demo/logo/` | karta wyniku w skórkach platform (jasna i ciemna), warianty znaku; `demo/x/` przekierowuje do `demo/live/x/` |
| `docs/` | dokument produktowy (historie użytkowników, funkcje, ADR), źródło dla Google Docs |
| `artifact/` | pliki opublikowanego Design System artifactu |
| `PRODUCT.md`, `KEY_SELLING_POINTS.md` | produkt i strategia na konkurs MSZ „Prawdowid” |
