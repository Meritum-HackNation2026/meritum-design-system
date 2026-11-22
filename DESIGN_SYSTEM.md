# Meritum: Design System

**Meritum — obywatelski radar dezinformacji.**

Ten dokument opisuje, jak Meritum wygląda i jak mówi. Przekaż go agentowi AI, który robi slajdy, makiety albo materiały marketingowe, razem z poleceniem z sekcji 12. Wszystkie wartości są ostateczne, chyba że ten plik powie inaczej.

---

## 1. Idea w jednym akapicie

Meritum pozwala sprawdzić informację tak łatwo, jak wysłać wiadomość. Obywatel wkleja tekst albo link w formularzu na stronie (kanał podstawowy) albo wysyła go botowi na Discordzie (drugi kanał, także w wiadomości prywatnej). Wtyczka do przeglądarki dodaje „Sprawdź” pod postem i pole do wklejenia tekstu w okienku. Jeśli starczy czasu, dojdzie SMS. Jeden rdzeń weryfikacji wyodrębnia twierdzenia, szuka w opisanym i audytowalnym zbiorze źródeł oraz w świeżych publikacjach z zatwierdzonych serwisów, a potem dla każdego twierdzenia podaje werdykt z dosłownym cytatem, jawnymi przesłankami i siłą podstawy. Gdy dowodów brakuje, wstrzymuje się i mówi, czego nie ustalił; sprawy nierozstrzygnięte i powtarzające się trafiają do kolejki moderatorów. Wygląd łączy precyzję narzędzi dla analityków (Linear, Vercel) z powagą dziennikarstwa śledczego (The Economist, Bellingcat). Metafora przewodnia to **biuletyn synoptyczny**: spokojny komunikat, jasno podane źródła pomiaru i uczciwie zaznaczona niepewność.

### Idea przewodnia: cytat jest dowodem

Meritum nie wygląda jak czat. Wygląda jak sprawdzona wypowiedź: najpierw werdykt, duży, w kolorze werdyktu, potem twierdzenie w cudzysłowie, jedno zdanie wyjaśnienia i dosłowne cytaty ze źródeł. Znakiem rozpoznawczym jest polski cudzysłów „ wysunięty na margines w kolorze `--verified`: stoi przy każdym cytacie ze źródła, przy pytaniu obywatela i przy przykładowych twierdzeniach na pustej stronie. Cudzysłów zastępuje ramkę: cytat nie leży w pudełku. Hierarchię budują skala i tło, nie obrysy. Informacja o AI pada raz na widok.

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
| **Azeret Mono** (400–600) | wyłącznie kod i identyfikatory: ID sprawdzeń i spraw (c_01, #S-1), domeny w tabelach panelu, liczby w metrykach panelu. Daty i godziny w rozmowie i na karcie wyniku są w Archivo z cyframi tabelarycznymi | Google Fonts |

Oba kroje mają polskie znaki. Mono nigdy nie służy do dekoracji, etykiet ani nagłówków.

### Skala

| Styl | Rozmiar / interlinia | Grubość | Gdzie |
|---|---|---|---|
| Display | 40 px / 1,05 | 700, szerokość 108% | tylko slajdy |
| Werdykt | 28 px / 32 px | 700, szerokość 112,5% | słowo werdyktu na karcie wyniku, pierwsze, co karta mówi (6.4) |
| Tytuł | 22 px / 28 px | 700 | nagłówek strony i panelu, przykładowe twierdzenia na pustej stronie |
| Powitanie | 30 px / 36 px (od 1024 px: 40 px) | 700, szerokość 112,5%, światło −0,025 em | tylko hasło na pustej stronie rozmowy (6.8) |
| Twierdzenie | 16 px / 24 px | 600 | treść twierdzenia pod werdyktem, w cudzysłowie |
| Tekst | 16 px / 24 px | 400 | wyjaśnienie, cytat |
| Mały | 14 px / 20 px | 400–600 | wydawca, data, przesłanki |
| Meta | 12 px / 16 px | 600 | nagłówek widżetu „Meritum”, osie wykresu |

Nic poniżej 12 px. Nagłówki zdaniowe (wielka litera tylko na początku), bez rozstrzelonych WERSALIKÓW, bez etykiet nad nagłówkami.

**W widżecie na platformie** treść dziedziczy krój platformy (np. systemowy na X, Reddit Sans na Reddicie). Archivo zostaje tylko w nagłówku „Meritum” i plakietce werdyktu.

---

## 5. Odstępy, siatka, kształty

- **Siatka 4 px.** Typowe odstępy: 4, 6, 8, 12, 14, 16, 24 px.
- **Wnętrze kart:** 14 px w poziomie, 12 px u góry, 14 px na dole.
- **Strona i panel:** marginesy 24 px (16 px na telefonie), odstęp między blokami 12–16 px. Formularz i wynik w jednej kolumnie do 720 px.
- **Promienie:** karty 12 px (w widżecie zgodnie z platformą: X 16, Facebook 8, Instagram 0, Reddit 16, TikTok 8), okienka 14 px, przyciski i plakietki w pełni zaokrąglone (pigułki), pola formularzy 10 px.
- **Głębia:** karty leżą płasko i nie mają cienia. Samodzielna karta (widżet, okienko wtyczki) ma obramowanie 1 px; karta w odpowiedzi w rozmowie (6.8) obramowania nie ma, odróżnia ją tło `--card` od tła strony. W środku karty nie ma ramek: cytat nie leży w pudełku, twierdzenia dzieli odstęp i jedna cienka linia. Cień dostaje tylko to, co się unosi: okienko wtyczki, podpowiedź (tooltip), powiadomienie.
- **Zakazane:** pasek koloru wzdłuż jednego boku karty, siatki identycznych kart z ikoną na górze, szkło i rozmycie tła, ozdobne kształty.

---

## 6. Komponenty

Kod React (shadcn/ui, Tailwind v4) leży w `components/meritum/`, wersja dla Shadow DOM wtyczki w `extension/widget.css`, dane opisują kontrakty (źródłem prawdy jest repozytorium meritum-core, a w `contracts/` leży kopia pobierana skryptem `contracts/sync.sh`, której nie edytuje się ręcznie), teksty `copy/pl.json`. Bot na Discordzie i SMS nie mają własnego wyglądu: korzystają z tych samych tekstów. Bot odpowiada jedną wiadomością z osadzeniem: pole na każde twierdzenie (werdykt, twierdzenie, jeden cytat ze źródłem z datą, siła), kolor osadzenia z najpoważniejszego werdyktu, a pod spodem przycisk-link „Pełna karta” (`discord.card_button`). Za długi wynik skraca cytaty, nie twierdzenia. Odpowiedź jest prywatna (efemeryczna), chyba że użytkownik wybierze opcję „publiczne” (`discord.public_option`). Każdy kanał przy pierwszym kontakcie mówi, że odpowiada system AI (`ai_notice`). Odpowiedź SMS podaje sam werdykt głównego twierdzenia, bez linku, żeby zmieścić się w 70 znakach UCS-2 i uniknąć filtrowania przez operatora; opcją jest GSM-7 bez polskich znaków i 160 znaków (`sms`). Makieta Discorda dla jury leży w repozytorium meritum-mocks i woła to samo API co bot. Wygląd bierze ze skórki `[data-host="discord"]` w `tokens/meritum.css`, a teksty z `discord`: podpis wiadomości użytkownika, szablony twierdzenia bez daty albo bez siły i liczbę twierdzeń w trzech formach. Karta wyniku w skórkach pięciu platform: `demo/widgets/`, cały przepływ „Sprawdź” na makietach: `demo/live/`.

### 6.1 Formularz „Sprawdź informację” (strona WWW, kanał podstawowy)
Jedna kolumna, działa od 320 px szerokości. Na stronie WWW formularz jest polem wiadomości przyklejonym na dole widoku rozmowy (6.8): pole, przycisk nagrania i „Sprawdź” w jednej ramce, tytuł i etykieta zostają dla czytnika ekranu, a informacja o prywatności i lista sprawdzeń przechodzą do wątku. Punkty poniżej opisują treść; układ z tytułem, etykietą nad polem i przyciskiem nagrania pod polem (`CheckForm`) zostaje tylko w okienku wtyczki.
1. Tytuł „Sprawdź informację” i jedno zdanie, co się stanie.
2. Pole „Tekst albo link” (do 4000 znaków), przyjmuje wklejony tekst albo pełny adres zaczynający się od http:// albo https:// (do 2083 znaków, jak `CheckRequest.url`). Pod nim drugorzędny przycisk „Albo nagranie (plik audio)” (`form.audio_label`). Nad polem jedno zdanie, że odpowiada system AI (`ai_notice.first_contact`).
3. Przycisk główny „Sprawdź”, aktywny zawsze poza wysyłką. Za krótki tekst, za długi albo błędny link dają po kliknięciu komunikat pod polem (`errors`). W trakcie: „Sprawdzamy…” i pasek analizy (6.3).
4. Pod przyciskiem informacja o prywatności: konto nie jest potrzebne, maskowanie oczywistych danych osobowych, termin usunięcia zapisu, link „Usuń moje sprawdzenia”.
5. Pod formularzem lista „Twoje sprawdzenia” (`history`): sprawdzenia z tej rozmowy, od najnowszego; kliknięcie otwiera kartę wyniku. Bez logowania lista pochodzi z sessionStorage, a notatka mówi, że historia jest tylko w tej przeglądarce: w tej karcie i w kartach z niej otwartych (przeglądarka kopiuje sessionStorage do takich kart). Pusta lista pokazuje `history.empty`.
6. Przy liście opcjonalne logowanie (`account`): dwa przyciski drugorzędne „Zaloguj się kontem Google” i „Zaloguj się kontem Microsoft” oraz zdanie, że logowanie nie jest potrzebne. Po zalogowaniu historia jest na serwerze, a w miejscu przycisków są „Usuń moją historię”, „Usuń konto i historię” i „Wyloguj się”.

Błędy pod polem, słowami z `copy/pl.json` (`errors`), bez czyszczenia wpisanej treści.

### 6.2 Przycisk „Sprawdź” we wtyczce (kanał dodatkowy)
Znak Meritum 18 px + słowo „Sprawdź” w pasku akcji posta. Stany: spoczynek (kolor ikon platformy), najechanie (tło `#E1EDF2`, tekst `#13506A`), w toku, „Sprawdzono”. Treść posta wysyłamy dopiero po kliknięciu. Wynik pojawia się pod postem jako karta wyniku (6.4). Okienko wtyczki z paska przeglądarki ma to samo pole co formularz WWW, więc ten sam tekst można sprawdzić w obu kanałach i dostać ten sam wynik.

### 6.3 Pasek analizy
Pokazuje kroki workflowu: kółko czeka, kręci się, gotowe, pominięte albo nieudane. Każdy stan czytnik ekranu dostaje słowem z `analysis.step_status`; przy pominiętym i nieudanym kroku to słowo jest też widoczne obok nazwy, więc przekreślenie, znak i kolor nie są jedyną informacją. Kody i teksty kroków: `receive`, `fetch_url`, `transcribe_audio`, `screen_injection`, `extract_claims`, `search_corpus`, `search_web`, `search_fact_checks`, `assess_evidence`, `verify_citations`, `write_answer`, `save_record` (`copy/pl.json`, `analysis.steps`). „Pobieramy stronę z linku” jest pominięte, gdy wklejono sam tekst, a „Zamieniamy nagranie na tekst”, gdy nie ma nagrania. „Szukamy świeżych publikacji w zatwierdzonych serwisach” rusza zawsze, razem z bazą źródeł; gdy baza wystarczy, odpowiedź na ten krok nie czeka. Agenty badawcze działają równolegle, więc kilka kółek może się kręcić naraz. Odpowiedź przychodzi strumieniem: wersja wstępna ma dopisek `analysis.draft` i nie pokazuje werdyktu, dopóki cytaty nie przejdą weryfikacji.

### 6.4 Karta wyniku
Jedna karta na sprawdzenie, a w niej jeden blok na każde twierdzenie. Tło `--card`; obramowanie 1 px tylko poza rozmową (sekcja 5), w widżecie promień platformy. Blok czyta się od werdyktu.
- **Nagłówek:** znak 14 px + „Meritum” (poza rozmową; w odpowiedzi podpis mówi, kto odpowiada).
- **Werdykt:** pierwszy i największy element bloku: słowo („Potwierdzone”, „Fałszywe”, „Wprowadzające w błąd”, „Brak wystarczających dowodów”, „Nie podlega weryfikacji”) w stylu Werdykt, w kolorze tekstu werdyktu (`*-foreground`; dwa nierozstrzygające w kolorze tekstu), bez pigułki. Pigułka (`VerdictBadge` sm/md) zostaje dla list i tabel.
- **Twierdzenie:** pod werdyktem, w cudzysłowie, w stylu Twierdzenie; werdykt i twierdzenie tworzą razem nagłówek bloku. Pod nimi jedno zdanie podpowiedzi z `verdict_hint`.
- **Wyjaśnienie:** 1–3 zdania. Bez podpisu o AI przy każdym twierdzeniu: informacja o AI pada raz (stopka karty albo, w rozmowie, nad polem wiadomości). `result.explanation_hint` nie jest już pokazywany.
- **Na czym się opieramy:** każde źródło jako dowód: najpierw dosłowny fragment w stylu Tekst, z cudzysłowem „ wysuniętym na margines w kolorze `--verified`, bez tła i ramki; pod nim przypis: tytuł (link), wydawca, data publikacji, rodzaj i poziom (urzędowe lub pierwotne, wtórne). Źródło z wyszukiwania w sieci ma dopisek „znalezione w wyszukiwaniu w zatwierdzonych serwisach”.
- **Siła podstawy:** tylko przy werdyktach rozstrzygających. Słowo i trzy kreski poziomu, pod nimi przesłanki słowami: liczba niezależnych wydawców zgodnych z werdyktem, ile z nich urzędowych, data najnowszego źródła i data, której dotyczy twierdzenie (`result.newest`), czy źródła są zgodne. Przy sprzecznych źródłach nie ma siły: werdykt to „Brak wystarczających dowodów”, cytaty obu stron stoją obok siebie, a nad nimi jest jedno zdanie, czym się różnią (`result.conflict`).
- **Czego nie udało się ustalić:** obowiązkowe przy „Brak wystarczających dowodów”.
- **Oś czasu dowodów:** cytaty według wymowy w trzech grupach z nagłówkami `result.stance` (wspierają, przeczą, dają kontekst), z datą twierdzenia i datami publikacji (wiersz `CitationItem` z `showDate={false}`: linia wydawcy podaje wydawcę, rodzaj i poziom źródła bez daty, bo oś pokazuje ją sama); dowód zastąpiony nowszym jest na osi oznaczony (`result.superseded` z datą nowszego dokumentu, `result.superseded_undated`, gdy wynik jej nie podaje). Pod osią „Co zmieniłoby werdykt” (`result.what_would_change`).
- **Kontekst:** ocena fact-checkera z ClaimReview z linkiem (`result.claim_review`), zawsze jako kontekst, nigdy jako cytat. Przy nagraniu transkrypcja z podpisem (`result.transcript_hint`).
- **Ostrzeżenia:** dowód nieaktualny, podobieństwo do znanego incydentu z bazy organizatora albo EUvsDisinfo, z nazwą bazy, albo link do serwisu z takiej bazy (jako kontekst, nie podstawa oceny; przy EUvsDisinfo zastrzeżenie `result.euvsdisinfo_disclaimer`) i neutralna informacja, że treść pochodzi od podmiotu z oficjalnej listy sankcji UE. Każde w osobnym wierszu, bez czerwieni. Żadne nie zmienia werdyktu.
- **Technika:** nazwa techniki manipulacji + podpowiedź „jak rozpoznać?”, gdy dotyczy.
- **Stopka:** „Ograniczenia” (zawsze), stan przekazania moderatorom (`escalation`: zalecane, przekazane, dołączone do sprawy; przy nieudanym zapisie sprawy — `escalation.not_saved`, bez numeru sprawy), informacja o użyciu AI, „Zgłoś błąd” (`result.report_error`) i link „Jak działa Meritum”. W rozmowie stopka nie powtarza informacji o AI, a „Zgłoś błąd” jest dyskretną akcją (link albo menu karty), nie przyciskiem przy każdej karcie.
- **Pojawienie się:** karta rozwija się z wysokości 0 i unosi o 8 px w 0,5 s.

Gdy wynik nie jest werdyktem (doprecyzuj, poza zakresem, problem techniczny), karta ma tylko ikonę, tytuł stanu i komunikat z `status_hint`. Żadnej plakietki, żadnych źródeł.

### 6.5 Kolejka moderatorów (panel)
Do panelu logują się osoby z kontem nadanym przez administratora, w roli moderatora, analityka albo administratora (`moderation.role`). Lista spraw: ID w mono (#S-1), krótki opis, powody słowami (sprawa może mieć kilka: „brak wystarczających dowodów”, „sprawa wysokiego ryzyka” z dopasowanym tematem, „powtarzające się pytanie bez odpowiedzi”, „zgłoszenie błędu przez użytkownika”), twierdzenia sprawy, liczba podobnych pytań i różnych pytających (ta podnosi priorytet), pierwsze i ostatnie wystąpienie, stan. Podobne twierdzenia trafiają do jednej sprawy, nie tworzą nowych. Panel nie pokazuje identyfikatorów z Discorda ani numerów telefonów. Panel pokazuje też jakość: medianę czasu odpowiedzi, odsetek wstrzymań, błędy wyszukiwania, wykryte próby wstrzyknięcia poleceń i szacowany koszt. Wykresy według zasad z sekcji 3: etykiety przy liniach, bez kafelków KPI z ikonami. Analityk i administrator mają też stronę ewaluacji (`evaluation`): lista przebiegów z miernikami, nowy przebieg na golden secie, dodanie zestawu (JSON albo CSV) i porównanie dwóch przebiegów z listą przypadków, które zmieniły wynik.

### 6.6 Powiadomienia
W aplikacji WWW i w panelu powiadomienie pojawia się od razu jako toast (Sonner), w rogu, bez czerwieni. Toast, na który ktoś nie zareagował, zostaje w skrzynce pod ikoną dzwonka jako nieprzeczytany; licznik nieprzeczytanych przy ikonie (`notifications`). Kliknięcie otwiera link z powiadomienia i oznacza je jako przeczytane. Teksty według rodzaju (`notifications.kind`), retencja jak w zapisie sprawdzenia.

### 6.7 Komponenty poza zakresem MSZ
`ContextCard` (notatka i ostrzeżenie o oszustwie), `CampaignRotation`, `BotDefenseTelemetry` i `QuickReportPopover` leżą w `components/legacy/` jako pozostałość wcześniejszej wersji produktu (wątek NASK i notatek społeczności). Nie używamy ich w demo ani w materiałach na konkurs MSZ.

### 6.8 Widok rozmowy (strona WWW)
Strona główna i strona wyniku to jeden widok: rozmowa obywatela z Meritum. Wzór to rubryka „Czytelnicy pytają, redakcja odpowiada”: pytanie jest cytowanym listem, odpowiedź ma podpis redakcji i podstawę. Komponenty: `Question`, `Reply`, `Welcome`, `Attachment`, `Composer` (`components/meritum/conversation.tsx`), teksty `conversation`.
- **Układ:** wątek w jednej kolumnie do 720 px; pusta strona (`Welcome`) od 1024 px zajmuje szerokość do 1120 px w dwóch kolumnach. Na górze cienki nagłówek, potem wątek, na dole przyklejone pole wiadomości (`Composer`). Pole leży na pasku w kolorze tła strony, sama ramka pola unosi się, więc ma cień `--shadow-float` i promień okienka (14 px). Wątek kończy się informacją o AI (jedyną na ekranie), zdaniem o prywatności z „Usuń moje sprawdzenia” i notatką `history.session_note`, tuż nad polem.
- **Pytanie (`Question`):** słowa obywatela bez zmian, wyrównane do prawej, na podniesionym tle, promień 14 px z jednym ostrzejszym rogiem (6 px) po stronie pytającego. Otwierający cudzysłów „ wisi na marginesie po lewej, w kolorze tekstu drugorzędnego. Pod pytaniem godzina w Archivo z cyframi tabelarycznymi. Mówiącego („Ty”) słyszy tylko czytnik ekranu. Nagranie stoi w wątku jako `conversation.audio_question` z nazwą pliku.
- **Odpowiedź (`Reply`):** podpis jak logotyp: znak 20 px, „Meritum” w Archivo 600 o szerokości 112,5%, obok godzina. Pod podpisem pasek analizy (6.3), a potem karta wyniku (6.4), bez dodatkowej ramki wokół. Karta w odpowiedzi nie powtarza nagłówka „Meritum”, bo podpis już mówi, kto odpowiada.
- **Historia to wątek:** sprawdzenia z tej karty (sessionStorage) stoją jako kolejne pary pytanie–odpowiedź, od najstarszego u góry do najnowszego nad polem. Osobnej tabelki „Twoje sprawdzenia” na stronie WWW nie ma; `CheckHistory` zostaje dla historii po zalogowaniu i dla wtyczki.
- **Puste wejście (`Welcome`):** po lewej hasło „Sprawdź, zanim podasz dalej.” w stylu Powitanie (sekcja 4) i zdanie `form.lead`; po prawej (pod spodem na telefonie) 2–3 przykładowe twierdzenia z `conversation.examples` w stylu Tytuł, każde z cudzysłowem „ w kolorze `--verified` wysuniętym na margines, bez ramki. Przykłady to twierdzenia, które system sprawdza i rozstrzyga (np. płaca minimalna 2026), nigdy takie, które kończą się „Nie podlega weryfikacji”. Informacji o AI tu nie ma: stoi raz, nad polem wiadomości. Kliknięcie wysyła twierdzenie jak wpisane pytanie.
- **Pole wiadomości (`Composer`):** pole rośnie z treścią do ok. 8 wierszy, Enter wysyła, Shift+Enter dodaje wiersz. Licznik znaków pojawia się dopiero przy pisaniu. Na telefonie pole ma 16 px, żeby przeglądarka nie powiększała strony, i rośnie najwyżej do ok. 4 wierszy. Placeholder z przykładem (`form.input_placeholder`) jest domyślny; po pierwszym sprawdzeniu aplikacja podaje `conversation.next_placeholder` przez prop `placeholder`. Przycisk nagrania (ikona mikrofonu z etykietą `conversation.attach_audio`) aplikacja wstawia w miejsce `tools` i otwiera nim wybór pliku; wybrany plik zastępuje pole jako `Attachment`: nazwa, „Usuń nagranie” i zdania o dostawcy, koszcie, retencji, limitach i ostrzeżeniu AI z `form`, zanim cokolwiek wyślemy. Obraz (zrzut ekranu albo zdjęcie) używa tego samego `Attachment` z `kind="image"`: miniatura jako `preview`, „Usuń obraz” i zdania `image_note`, limity, `image_cost` i `image_retention`.
- **Ruch:** tylko nowo wysłane pytanie wchodzi z 8 px w 0,24 s (`--animate-enter`, `Question` z `isNew`); pytania odtworzone z historii stoją od razu, przyciski przy wciśnięciu zmniejszają się do 97% w 0,15 s. Po wysłaniu wątek przewija się do nowej wymiany; przy „ogranicz ruch” bez animacji i bez płynnego przewijania.
- **Dostępność:** wątek to lista (`ol`) nazwana `conversation.label`, którą buduje aplikacja z par `Question` i `Reply`; stronę otwiera ukryty nagłówek h1 `form.title`; wynik ogłasza region `aria-live` karty, nie cały wątek. Pole wiadomości ma ukrytą etykietę `form.input_label`, a ramka pokazuje pierścień fokusu 2 px. Pole nigdy nie zasłania elementu z fokusem: strona ma `scroll-padding-bottom` co najmniej o wysokości pola, a nowa odpowiedź dostaje fokus tylko wtedy, gdy nic innego go nie ma.

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
- Wejście nowej wymiany w rozmowie i wciśnięcie przycisku trwają krócej (0,24 s i 0,15 s), bo widać je przy każdym sprawdzeniu (6.8).
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
- Zdjęcia tylko jako tło świata, w którym krąży pogłoska (pasażerowie z telefonami, ulica, katalog, prasa): z Unsplash albo innej licencji pozwalającej na użycie komercyjne, z autorem w podpisie, najwyżej jedno na slajd i nigdy jako produkt, nasi użytkownicy czy zespół. Bez klisz: laptopy, kłódki, tarcze, kaptury hakerów.
- Ikony z Lucide (ta sama biblioteka co frontend), obrys 2 px, w kolorze akcentu, przy punktach listy i w kafelkach architektury. Nigdy jako duży element nad tekstem karty ani w siatce identycznych kafelków.
- Wykresy według zasad z sekcji 3: etykiety przy liniach, czerwień tylko dla błędów.
- Logo w lewym górnym albo dolnym rogu, 24–32 px.
- W przykładach używamy prawdziwych, sprawdzalnych źródeł z korpusu. Nie wymyślamy źródeł, cytatów ani wyników testów.
- Nie piszemy o współpracy z MSZ, NASK ani mediami, dopóki jej nie ma; piszemy „gotowe do integracji z…”.

---

## 12. Polecenie dla agenta AI (kopiuj i wklej)

```
Projektujesz materiał dla Meritum — obywatelskiego radaru dezinformacji
(strona WWW do sprawdzania informacji, bot na Discordzie jako drugi kanał,
wtyczka do przeglądarki, panel moderatora). Trzymaj się DESIGN_SYSTEM.md.

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
- `components/meritum/`: komponenty React (shadcn/ui) typowane kontraktami: `CheckForm` i `CheckHistory` (6.1), `Composer`, `Question`, `Reply`, `Welcome` i `Attachment` (6.8), `CheckButton` (6.2), `AnalysisSteps` (6.3), `ResultCard` z `VerdictBadge`, `CitationItem` i `StrengthMeter` (6.4), `ModerationQueue` (6.5). Instalacja i podgląd: `components/meritum/README.md`.
- `tokens/meritum.css`: te same tokeny dla strony, panelu i wtyczki.

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
