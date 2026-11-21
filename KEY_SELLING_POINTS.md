# Meritum: key selling points

**Meritum — obywatelski radar dezinformacji.** Konkurs MSZ „Prawdowid”.

Dokument roboczy dla całego zespołu: czym się wyróżniamy, jak odpowiadamy na każde wymaganie z treści zadania i co pokazać na demo. Pełna treść zadania jest w `../konkursy/`.

Pokazujemy tylko liczby zmierzone naszym skryptem ewaluacji na naszym zestawie testowym, razem z danymi do odtworzenia. Zestaw referencyjny jury pochodzi od MSZ i jest dla nas ukryty: progi stroimy wyłącznie na własnym zestawie, zbudowanym z tych samych materiałów co baza wiedzy.

Na koniec prac udostępnimy publicznie wszystkie repozytoria i system. Publiczne repozytorium będzie mieć instrukcję uruchomienia jednym poleceniem `docker compose up`. Nie obiecujemy skuteczności, której nie zmierzyliśmy.

---

## 1. Jednym zdaniem

**Wklejasz tekst albo link, a Meritum sprawdza każde twierdzenie w opisanych źródłach, cytuje dosłowny fragment i mówi wprost, gdy dowodów brakuje.**

Na slajd: *Sprawdź, zanim podasz dalej. Każde ustalenie ma źródło.*

---

## 2. Odpowiedź na wymagania MSZ

### Warunek brzegowy (bez niego reszta się nie liczy)

| Wymaganie | Nasza odpowiedź |
|---|---|
| Działanie end-to-end bez ręcznej ingerencji | Jedna ścieżka: przyjęcie, twierdzenia, wyszukiwanie, werdykt, odpowiedź, zapis przebiegu. Workflow DBOS, uruchamiany przez `docker compose` albo na publicznym demo. |
| Brak sfabrykowanych źródeł | Cytat przechodzi tylko wtedy, gdy fragment występuje dosłownie w tekście źródła z korpusu. Inaczej odpada przed pokazaniem. |
| Wstrzymanie się przy braku dowodów | Werdykt „brak wystarczających dowodów” z opisem, czego nie ustaliliśmy. Kontrakt odrzuca taki werdykt bez tego opisu. |
| Dwa kanały | Formularz WWW (podstawowy) i przycisk „Sprawdź” we wtyczce Chrome pod postem oraz okienko do wklejenia w popupie. Ten sam rdzeń, ten sam wynik. Bot na Discordzie na tym samym API budujemy od początku, więc warunek dwóch kanałów nie zależy od decyzji mentorów. Jeśli starczy czasu, dodamy SMS: adapter demonstracyjny przez webhook bramki SMS, z jawnymi opłatami operatora i odpowiedzią skróconą do 70 znaków (UCS-2) z linkiem do pełnego wyniku. |

### Minimalny zakres (MVP)

| Wymaganie | Nasza odpowiedź |
|---|---|
| Rozpoznawanie twierdzeń | LLM ze strukturalnym wyjściem oddziela twierdzenia od opinii. |
| Zbiór źródeł: co najmniej 2 typy | Typ pierwszy: źródła urzędowe i pierwotne z listy organizatora (serwisy gov.pl i agencji, lista niżej). Typ drugi: fact-checkerzy przez Google Fact Check Tools API (ClaimReview) i Fact Check Explorer. Źródła z listy pobieramy, wczytujemy, dzielimy na fragmenty i wektoryzujemy: co najmniej 100 dokumentów z co najmniej 10 domen, lista do audytu z licencją i powodem kwalifikacji. Niezależne źródła liczymy według wydawcy: dwie strony jednego ministerstwa to jedno źródło. Baza EUvsDisinfo to opcjonalna funkcja premiowana: dopasowanie do wrogich operacji informacyjnych, tylko jako kontekst, nigdy werdykt. |
| Bieżące wydarzenia | Cykliczne pobieranie RSS z katalogu i wyszukiwanie na żywo (Firecrawl) ograniczone do domen z katalogu. Strona z wyszukiwania czeka w kwarantannie na skan, a do korpusu dołącza z następną migawką, z datą publikacji i pobrania. Błąd, limit czasu albo limit zapytań wyszukiwania kończą się komunikatem o problemie technicznym, nigdy odpowiedzią. |
| Wynik, uzasadnienie, siła podstawy, ograniczenia | Jeden z pięciu werdyktów na twierdzenie, wyjaśnienie oznaczone jako interpretacja, siła liczona regułą z przesłanek, zawsze sekcja „Ograniczenia”. |
| Źródło: tytuł, wydawca, data, link, fragment | Wszystkie pięć pól w kontrakcie `Source` i `Citation`. |
| Prosty polski | Teksty w `copy/pl.json`, pisane dla osoby bez wiedzy technicznej. |
| Zapis przebiegu | `CheckRecord`: pytanie z zamaskowanymi danymi, czas, kanał, źródła, werdykty, modele, region, koszt, błędy wyszukiwania, próby wstrzyknięcia poleceń. |

### Lista źródeł od organizatora

Katalog źródeł zaczyna się od tej listy. Organizatorzy zgodzili się na przetwarzanie tych źródeł; w rozwiązaniu produkcyjnym wszystkie zgody potwierdzimy prawnie u każdego dostawcy.

- odyseusz.gov.pl
- gov.pl/web/gov/ostrzezenia
- gov.pl/web/mswia/regionalny-system-ostrzegania
- gov.pl/web/rcb/raport-dobowy3
- gov.pl/web/kgpsp/aktualnosci
- policja.pl/pol/aktualnosci
- mazowiecka.policja.gov.pl/ra/aktualnosci/aktualnosci
- gov.pl/web/obrona-narodowa/aktualnosci5
- gov.pl/web/gis/ostrzezenia
- gov.pl/web/paa/panstwowa-agencja-atomistyki
- monitoring.paa.gov.pl
- powietrze.gios.gov.pl/pjp
- moje.cert.pl/komunikaty
- gov.pl/web/infrastruktura (+ /aktualnosci, /prawa-pasazerow, /infolinia-dla-obywatela, /dane-kontaktowe)
- drogi.gddkia.gov.pl/informacje-drogowe (+ /mapy/mapa-informacji-drogowej, /informacje-drogowe/lista-utrudnien)
- gov.pl/web/gddkia/informacja-drogowa---19-111
- ulc.gov.pl (+ /prawa-pasazera, /prawa-pasazera/poradnik-dla-pasazerow)
- portalpasazera.pl
- utk.gov.pl/pl/pasazerowie
- kgsok.pl
- sar.gov.pl
- umgdy.gov.pl
- ums.gov.pl/bezpieczenstwo-morskie/warunki-zeglugi
- gov.pl/web/wody-polskie/komunikaty-nawigacyjne
- meteo.imgw.pl
- hydro.imgw.pl
- baltyk.imgw.pl
- gov.pl/web/rcb/strona-glowna-rzadowego-centrum-bezpieczenstwa
- gov.pl/web/mswia
- gov.pl/web/dyplomacja/informacje-dla-podrozujacych
- gov.pl/web/premier

Fact-checkerzy: Fact Check Explorer (toolbox.google.com/factcheck/explorer) i Google Fact Check Tools API (developers.google.com/fact-check/tools/api). Opcjonalnie: baza euvsdisinfo.eu.

### Wymagania techniczne

| Obszar | Nasza odpowiedź |
|---|---|
| Architektura | Kanały to adaptery wejściowe, LLM i wyszukiwarka to adaptery za portami (architektura heksagonalna). Modele bierzemy z Vertex AI w GCP (dowolny dostępny tam model, niekoniecznie Claude) i zmieniamy konfiguracją. Kontrakty są w repozytorium meritum-core, jedynym źródle prawdy. |
| Fakty | Werdykty rozstrzygające wymagają cytatu i przesłanek (walidacja kontraktu). Awaria, niejasne pytanie i pytanie poza zakresem to osobne stany bez twierdzeń. Sprzeczne wiarygodne źródła dają „brak wystarczających dowodów” z cytatami obu stron obok siebie i bez siły. |
| Aktualność | Data publikacji i pobrania przy każdym źródle, preferowanie świeżych, ostrzeżenie o materiale archiwalnym. Wiek liczymy od daty, której dotyczy twierdzenie: domyślnie 365 dni, dla ostrzeżeń, dróg, pogody i danych hydrologicznych godziny albo dni według katalogu. Obowiązujący akt prawny, strona urzędowa aktualizowana w miejscu i dowód o zdarzeniu z przeszłości nie są archiwalne. |
| Bezpieczeństwo | Warstwa kontroli (proxy LLM albo Google Cloud Model Armor) przed każdym wywołaniem modelu, w każdym kroku. Wejście użytkownika, podany link i treść źródeł są danymi we wszystkich krokach. Strony z katalogu skanujemy przy wczytywaniu, strony z wyszukiwania czekają w kwarantannie. Model bez narzędzi z efektami ubocznymi, sekrety tylko w zmiennych środowiska, limit zapytań (slowapi według adresu IP, regionu i kanału, Cloudflare przed API), zapis zdarzeń. |
| Prywatność | Maskowanie telefonów, e-maili i PESEL-i przed analizą, retencja 30 dni, przycisk „Usuń moje sprawdzenia”. Konto nie jest potrzebne: historia rozmowy zostaje w sessionStorage. Logowanie kontem Google albo Microsoft jest opcjonalne; wtedy historia jest na serwerze i można ją usunąć razem z kontem. Adresy IP i retencję logów opisuje polityka prywatności, a Discord, SMS i wtyczka mają osobne polityki. |
| Obserwowalność | Czas odpowiedzi, modele, błędy wyszukiwania, wstrzymania, koszt każdej odpowiedzi. |
| Zależności zewnętrzne | Opis kluczy, limitów, kosztów i regionu. Brak klucza, limit, awaria wyszukiwania albo modelu kończą się stanem „Problem techniczny” z komunikatem, nigdy werdyktem ani odpowiedzią z samego korpusu. |
| Czas | Treść zadania wymaga mediany do 30 s, my celujemy w najwyżej 30 s. Agenty badawcze działają równolegle, a agent główny strumieniuje odpowiedź z postępem badań. Czas mierzymy biblioteką pydantic-evals. |
| Spójność kanałów | Migawki korpusu według harmonogramu (np. co godzinę), pamięć wyników pod kluczem (znormalizowane wejście, migawka), temperatura 0 i przypięta wersja modelu. |
| Koszt i skalowanie | Koszt każdego sprawdzenia z tokenów i wywołań wyszukiwarki, koszt 1 000 zapytań i utrzymania kanałów, odsetek trafień w pamięci wyników, kolejka DBOS z limitem współbieżności, HTTP 429 z jasnym komunikatem, autoskalowanie w GCP. Liczby podamy po pomiarze. |
| Pętla informacji | Sprawa moderatora dla nierozstrzygniętych, ryzykownych i powtarzających się pytań, z deduplikacją. Interfejs odróżnia „zalecamy przekazanie” od „przekazano”. |

### Funkcje premiowane, które bierzemy

Punkty za funkcje premiowane liczą się tylko wtedy, gdy rozwiązanie spełnia wymagania podstawowe.

1. **Łańcuch dowodowy:** od twierdzenia do cytatów potwierdzających, obalających i uzupełniających kontekst.
2. **Zamknięta pętla informacji:** sprawy moderatora i grupowanie podobnych pytań.
3. **Otwarty katalog źródeł** z zasadami kwalifikowania, aktualizowania i wykluczania (`CatalogEntry`).
4. **Wielojęzyczne wyszukiwanie** z odpowiedzią po polsku.
5. **Dopasowanie do bazy incydentów** od organizatora jako kontekst, nigdy jako werdykt. Scenariusz I jest w zestawie jury, więc budujemy to w MVP. Jeśli starczy czasu, także dopasowanie do bazy EUvsDisinfo.
6. **Zrzut ekranu z OCR** (scenariusz F), z jawnymi ograniczeniami.
7. **Eksport JSON i CSV**, kody technik zmapowane na DISARM.
8. **Przetwarzanie w UE:** GCP z aplikacją w `europe-central2` i modelami przez Vertex AI w regionie UE, publiczny kod i opis drogi do samodzielnego hostowania (otwarty model na własnym serwerze z GPU po hackathonie, europejski indeks wyszukiwania).

---

## 3. Wyróżniki

### 3.1 Uczciwość wbudowana w kontrakt
Reguły z treści zadania sprawdza walidacja danych, a nie prompt: werdykt bez cytatu, siła niezgodna z przesłankami, „potwierdzone” przy sprzecznych źródłach i awaria pokazana jako werdykt nie przejdą. Każdą regułę sprawdza test pytest w meritum-core (`tests/test_checks_contracts.py`).

### 3.2 Cytat sprawdzany dosłownie
Model może się pomylić w cytacie. Dlatego zanim cytat trafi do odpowiedzi, sprawdzamy w kodzie, czy fragment naprawdę jest w źródle. To podnosi oba mierniki: pokrycie i poprawność cytowań.

### 3.3 Siła odpowiedzi z jawnych przesłanek
Pod werdyktem czytelnik widzi: ile niezależnych źródeł, ile urzędowych, jak świeże i czy są zgodne. Z tego jedną regułą wynika „mocna”, „umiarkowana” albo „słaba”. Nie ma tu liczby wymyślonej przez model.

### 3.4 Sprawdzanie tam, gdzie czytasz
Formularz działa dla każdego, bez instalacji i bez zakładania konta. Wtyczka dodaje „Sprawdź” pod postem na X, Facebooku, Instagramie, Reddicie i TikToku, w stylu danej platformy. Treść posta wysyłamy dopiero po kliknięciu.

### 3.5 Świeże źródła bez wychodzenia poza katalog
Bieżące wydarzenia sprawdzamy w publikacjach z zatwierdzonych serwisów. Wyszukiwanie w całym internecie łamałoby zasadę „jasno opisanego zbioru źródeł”, więc go nie robimy.

### 3.6 Człowiek tam, gdzie system nie rozstrzyga
Nierozstrzygnięte sprawy trafiają do moderatora, podobne pytania łączą się w jedną sprawę. Tak wygląda tryb wspierania decyzji z pilotażu opisanego w §9 zadania.

### 3.7 Uczymy rozpoznawania
Odpowiedź nazywa technikę (wyrwanie z kontekstu, nieaktualna informacja, fałszywy autorytet, wybiórcze dane) i w jednym zdaniu mówi, jak ją rozpoznać następnym razem.

---

## 4. Pitch (scena główna: to samo pytanie w dwóch kanałach)

1. **Problem (20 s):** „Od stycznia nie zapłacisz gotówką” krąży w wiadomościach. Sprostowanie istnieje, ale nie tam, gdzie ludzie czytają, a czat AI odpowie płynnie, choć bez źródła.
2. **Formularz (40 s):** wklejamy tekst: dwa twierdzenia, dwa werdykty, cytaty z ISAP i fact-checkera, siła podstawy, ograniczenia.
3. **Wtyczka (30 s):** ten sam tekst pod postem na X, „Sprawdź”, ten sam wynik.
4. **Uczciwość (30 s):** świeża plotka bez publikacji, system się wstrzymuje i zakłada sprawę moderatora. Strona z ukrytym poleceniem „zignoruj reguły”, system je ignoruje i zapisuje zdarzenie.
5. **Wyniki (30 s):** tabela mierników z naszego zestawu testowego i koszt 100 sprawdzeń.
6. **Zamknięcie:** *„Każde ustalenie ma źródło. Gdy źródeł brak, mówimy to wprost.”*

---

## 5. Scenariusz filmu (do 3 minut)

| Czas | Ekran | Co mówi prowadzący |
|---|---|---|
| 0:00 | Formularz na telefonie | „Wklejasz to, co dostałeś. Konto nie jest potrzebne, instalacja też nie.” |
| 0:20 | Wynik z dwoma twierdzeniami | „Każdy werdykt ma cytat, wydawcę i datę. Siła wynika z tego, co widzisz.” |
| 0:50 | Makieta X, przycisk „Sprawdź” | „Ten sam rdzeń we wtyczce. Ten sam wynik.” |
| 1:20 | Brak dowodów, sprawa #S-… | „Nie wiemy, więc nie zgadujemy. Sprawa trafia do moderatora.” |
| 1:50 | Próba wstrzyknięcia poleceń | „Strona próbuje przejąć model. Zignorowane i zapisane.” |
| 2:20 | Tabela mierników, koszt, architektura | „Wyniki odtworzysz jednym poleceniem z repozytorium.” |
| 2:45 | Zamknięcie | Hasło. |

Demo działa na prawdziwym korpusie i prawdziwym API. Żadna odpowiedź nie jest nagrana ani zaszyta w kodzie, bo jury wpisze własne pytania.

---

## 6. Pytania jury i odpowiedzi

- **„Kto decyduje, co jest prawdą?”** Źródła. Model rozumie pytanie, szuka i pisze, ale werdykt wymaga dosłownego cytatu, a siłę liczy reguła. Czego nie da się ustalić, trafia do ludzi.
- **„Co z halucynacjami?”** Cytat, którego nie ma w źródle, odpada w kodzie przed pokazaniem. Wyjaśnienie modelu jest oznaczone jako interpretacja.
- **„Stronniczość źródeł?”** Katalog jest jawny, z powodem kwalifikacji i wykluczenia. Nie oceniamy treści po domenie ani autorze. Status źródła (np. sankcje UE) pokazujemy jako osobną, neutralną informację.
- **„Prompt injection?”** Przed każdym wywołaniem modelu działa warstwa kontroli (proxy LLM albo Model Armor). Wejście użytkownika, link i treść źródeł to dane. Strony skanujemy przy wczytywaniu, a te z wyszukiwania czekają w kwarantannie. Model nie ma narzędzi, które coś zmieniają. Próby zapisujemy.
- **„Gdzie są przetwarzane dane?”** Docelowo w GCP w UE: aplikacja w `europe-central2` (Warszawa), modele przez Vertex AI w regionie UE, w którym jest dostępny wybrany model. W trakcie prac demo działa na serwerze zespołu; do GCP przeniesiemy je przez CI/CD, możliwe, że jeszcze w trakcie hackathonu. Dostawcę modelu i wyszukiwarki opisujemy z regionem i kosztem, a oba da się wymienić.
- **„Ile to kosztuje?”** Koszt każdego sprawdzenia liczymy z zapisu przebiegu (tokeny, wywołania wyszukiwarki), a z niego koszt 100 testów, 1 000 zapytań i utrzymania każdego kanału. Liczby podajemy po pomiarze. Przy większym ruchu sprawdzenia czekają w kolejce, a ponad limit API odpowiada HTTP 429 z jasnym komunikatem.
- **„Na czym stroicie progi?”** Na naszym zestawie testowym z materiałów bazy wiedzy. Zestaw jury od MSZ jest dla nas ukryty.
- **„Czy kod będzie publiczny?”** Tak, wszystkie repozytoria i system na koniec prac, z instrukcją uruchomienia przez `docker compose up`.
- **„Dlaczego wtyczka, a nie WhatsApp?”** Wtyczka działa tam, gdzie człowiek widzi treść, i nie wymaga konta firmowego ani opłat operatora. Ten sam rdzeń obsługuje bota na Discordzie, a jeśli starczy czasu, także SMS przez bramkę z jawnymi opłatami operatora.

---

## 7. Najważniejsze ryzyka (do README i prezentacji)

| Ryzyko | Jak ograniczamy |
|---|---|
| Halucynacje | Dosłowna weryfikacja cytatów, werdykt tylko z cytatem, wstrzymanie się przy braku dowodów. |
| Stronniczość źródeł | Jawny katalog z zasadami, co najmniej dwa typy źródeł, rozbieżności pokazywane wprost. |
| Prywatność | Maskowanie danych osobowych, retencja 30 dni, usuwanie sesji, konta opcjonalne z usuwaniem historii i konta, adresy IP i logi według polityki prywatności, osobne polityki kanałów. |
| Prompt injection | Warstwa kontroli przed każdym wywołaniem modelu, dane oddzielone od instrukcji we wszystkich krokach, skan stron przy wczytywaniu i kwarantanna stron z wyszukiwania, brak narzędzi z efektami ubocznymi, zapis zdarzeń, testy ze scenariusza E. |
| Dostępność | WCAG 2.2 AA, prosty język, formularz na telefonie bez instalacji. |
| Nadużycia | Limit zapytań według adresu IP, regionu i kanału, Cloudflare przed API, walidacja wejścia, brak publikacji bez człowieka. |
| Awaria dostawcy | Błąd, limit czasu albo limit zapytań wyszukiwania i awaria modelu dają stan „Problem techniczny” z komunikatem, nigdy pozorny werdykt (scenariusz J). |
| Koszt i ruch | Koszt mierzony dla każdego sprawdzenia, kolejka z limitem współbieżności, HTTP 429 z komunikatem, autoskalowanie w GCP. |
| Prawa autorskie | Podstawa prawna każdego dokumentu, krótki fragment w ramach prawa cytatu, zgody dostawców treści, lista komponentów zewnętrznych z licencjami (sekcja 6 dokumentu produktowego). |

---

## 8. Czego nie mówimy

- Nie podajemy skuteczności, której nie zmierzyliśmy, ani wyników bez danych do odtworzenia.
- Nie twierdzimy, że współpracujemy z MSZ, NASK ani z fact-checkerami. Mówimy „gotowe do integracji z…”.
- Nie deklarujemy wyszukiwania odwrotnego obrazu, dopóki go nie ma.
- Nie nazywamy systemu „sędzią prawdy”.

---

## 9. Nazwa: Meritum

**Meritum — obywatelski radar dezinformacji.** „Meritum” to „sedno sprawy”: odpowiedź mówi, o co naprawdę chodzi, i pokazuje, skąd to wiemy. „Obywatelski”, bo służy obywatelowi, a nie platformie. Przed pitchem trzeba sprawdzić znak towarowy i wolne domeny. Nazwa bywa używana przez inne firmy, więc w materiałach zawsze idzie z podtytułem.

## 10. Zakres na hackathon

**Budujemy:** formularz WWW, „Sprawdź” we wtyczce i w popupie, rdzeń weryfikacji (twierdzenia, wyszukiwanie hybrydowe, werdykt, cytaty, przesłanki), korpus z katalogiem, cykliczne RSS i wyszukiwanie Firecrawl w domenach z katalogu, zapis przebiegu, sprawy moderatora z deduplikacją, ochronę przed wstrzykiwaniem poleceń, dopasowanie do bazy incydentów, bota na Discordzie, historię rozmowy w sessionStorage, osobne polityki prywatności kanałów, limity zapytań, pomiar kosztu, skrypt ewaluacji (także na pliku jury), `docker compose`, demo (teraz na serwerze zespołu, docelowo w GCP), materiały z §4. Zakres jest szeroki, bo budujemy równolegle z wieloma agentami programistycznymi.

**Jeśli starczy czasu:** kanał SMS, logowanie kontem Google albo Microsoft z historią na serwerze, dopasowanie do bazy EUvsDisinfo, OCR zrzutu ekranu, ostrzeżenie o statusie źródła, wyszukiwanie wielojęzyczne, eksport JSON i CSV z kodami DISARM, serwer MCP.

**Po hackathonie:** wyszukiwanie odwrotne obrazu, transkrypcja nagrań, archiwizacja materiału wskazanego przez użytkownika, zatwierdzanie odpowiedzi moderatorów (z konsensusem pomostowym), otwarty model na własnym serwerze z GPU.

**Otwarte pytanie do mentorów MSZ:** czy wtyczka przeglądarki to „rozwiązanie równoważne” drugiemu kanałowi.
