# Meritum: key selling points

**Meritum — obywatelski radar dezinformacji.** Konkurs MSZ „Prawdowid”.

Dokument roboczy dla całego zespołu: czym się wyróżniamy, jak odpowiadamy na każde wymaganie z treści zadania i co pokazać na demo. Pełna treść zadania jest w `../konkursy/`.

Pokazujemy tylko liczby zmierzone naszą ewaluacją (pydantic-evals) na golden secie, czyli zestawie deweloperskim, razem z danymi do odtworzenia. Zestaw referencyjny jury pochodzi od MSZ i jest dla nas ukryty: progi stroimy wyłącznie na golden secie, zbudowanym z tych samych materiałów co baza wiedzy. Pytamy mentorów, czy MSZ opublikuje jawną część zestawu; jeśli tak, podamy wyniki na obu.

Na koniec prac udostępnimy publicznie wszystkie repozytoria i system. Publiczne repozytorium będzie mieć instrukcję uruchomienia jednym poleceniem `docker compose up`. Nie obiecujemy skuteczności, której nie zmierzyliśmy. Kod to dziś szkielet (endpoint health, workflow DBOS ping, kontrakty); budujemy go od ścieżki end-to-end, a kolejność jest w sekcji 3 dokumentu produktowego.

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
| Dwa kanały | Formularz WWW (podstawowy) i bot na Discordzie na tym samym rdzeniu: ten sam wynik. Bot odpowiada na kanałach serwera i w wiadomościach prywatnych, przyjmuje też wiadomości głosowe, a przy pierwszym kontakcie mówi, że jest systemem AI. Odpowiedź dzieli: najpierw podsumowanie z linkiem do pełnej karty, potem po jednej wiadomości na twierdzenie, każda do 2000 znaków i bez przecinania cytatu. Jury dodaje go linkiem zaproszenia do własnego serwera albo testuje na makiecie Discorda, która woła to samo API, bez dołączania do serwera. Warunek dwóch kanałów nie zależy więc od decyzji mentorów w sprawie wtyczki. Przycisk „Sprawdź” we wtyczce Chrome i okienko do wklejenia w popupie to kanał dodatkowy, dla jury opcjonalny. Jeśli starczy czasu, dodamy SMS: adapter demonstracyjny przez webhook bramki SMS Gateway for Android (sms-gate.app, tryb Cloud), z jawnymi opłatami operatora; w 70 znakach (UCS-2) wysyłamy sam werdykt głównego twierdzenia, bez linku, bo operatorzy często je filtrują. |

### Minimalny zakres (MVP)

| Wymaganie | Nasza odpowiedź |
|---|---|
| Rozpoznawanie twierdzeń | LLM ze strukturalnym wyjściem oddziela twierdzenia od opinii. |
| Zbiór źródeł: co najmniej 2 typy | Typ pierwszy: źródła urzędowe i pierwotne z listy organizatora (serwisy gov.pl i agencji, lista niżej) oraz ISAP, EUR-Lex, dane.gov.pl i BIP, które rekomenduje §7 treści zadania. Typ drugi: artykuły z fakenews.pl i pravda.org.pl (sygnatariusze IFCN, bez blokad, z RSS i mapami strony) oraz teksty „fact” z EUvsDisinfo. Demagog i AFP Sprawdzam blokują automaty, więc z nich bierzemy tylko ocenę ClaimReview i link z Google Fact Check Tools API. Ocena fact-checkera z IFCN albo EFCSN może być przesłanką werdyktu: cytujemy nazwę, ocenę, tytuł, datę i link, bez fragmentu strony („Według Demagoga …”); Konkret24 wykluczamy (brak w IFCN i EFCSN, TVN wymaga umowy licencyjnej). Źródła z listy pobieramy, wczytujemy, dzielimy na fragmenty i wektoryzujemy: co najmniej 100 dokumentów z co najmniej 10 domen, lista do audytu z licencją i powodem kwalifikacji. Niezależne źródła liczymy według identyfikatora wydawcy z katalogu: dwie strony jednego ministerstwa to jedno źródło. Baza incydentów organizatora i lokalna kopia EUvsDisinfo to jedna funkcja MVP: dopasowanie jest kontekstem, a nie werdyktem, tekst „fact” cytatem. |
| Bieżące wydarzenia | Cykliczne pobieranie RSS i map stron z katalogu jako podstawa, a do tego wyszukiwanie na żywo przez Vertex AI Search ograniczone do domen z katalogu, uruchamiane przy każdym sprawdzeniu równolegle z korpusem. Wynik daje adres, a stronę pobieramy sami z poszanowaniem robots.txt i Content-Signal. Strona z wyszukiwania czeka w kwarantannie na skan, potem jest dowodem w tym samym sprawdzeniu, a do korpusu dołącza z następną migawką, z datą publikacji i pobrania. Gdy czekamy na wyszukiwanie, jego błąd, limit czasu albo limit zapytań kończą się komunikatem o problemie technicznym, nigdy odpowiedzią. |
| Wynik, uzasadnienie, siła podstawy, ograniczenia | Jeden z pięciu werdyktów na twierdzenie, wyjaśnienie oznaczone jako interpretacja, siła liczona regułą z przesłanek, zawsze sekcja „Ograniczenia”. |
| Źródło: tytuł, wydawca, data, link, fragment | Wszystkie pięć pól w kontrakcie `Source` i `Citation`. |
| Prosty polski | Teksty w `copy/pl.json`, pisane dla osoby bez wiedzy technicznej. |
| Zapis przebiegu | `CheckRecord`: pytanie z zamaskowanymi danymi, czas, kanał, źródła, werdykty, modele, region, koszt, błędy wyszukiwania, próby wstrzyknięcia poleceń. |

### Lista źródeł od organizatora

Katalog źródeł zaczyna się od tej listy. Organizatorzy zgodzili się na przetwarzanie tych źródeł. Nie mamy tej zgody na piśmie i nie obejmuje ona praw osób trzecich, więc w rozwiązaniu produkcyjnym potwierdzimy prawnie zgodę każdego dostawcy.

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

Źródła pierwotne spoza listy, które rekomenduje §7 treści zadania, a §5 pozwala nam uzasadnić: ISAP (isap.sejm.gov.pl) i EUR-Lex (eur-lex.europa.eu) jako oficjalne publikatory aktów prawnych, dane.gov.pl jako portal danych publicznych i BIP instytucji z katalogu. Każda pozycja katalogu podaje powód kwalifikacji. gov.pl/web/dyplomacja kwalifikujemy jako źródło urzędowe MSZ.

Fact-checkerzy: fakenews.pl i pravda.org.pl pobieramy przez RSS i mapy strony. Demagog i AFP Sprawdzam to tylko ocena i link z Google Fact Check Tools API (developers.google.com/fact-check/tools/api), bo blokują automaty; ocena może być przesłanką werdyktu, a Konkret24 jest wykluczony. Dla każdej domeny sprawdzamy robots.txt, Content-Signal i zastrzeżenia eksploracji tekstów i danych. Fact Check Explorer to interfejs WWW, a nie API, więc nie ma go w katalogu. Baza euvsdisinfo.eu: lokalna kopia przez serwer MCP, pobierana według instrukcji https://euvsdisinfo.eu/public-docs/How_to_grab_all_Articles_and_Cases_from_disinfo.pdf.

### Wymagania techniczne

| Obszar | Nasza odpowiedź |
|---|---|
| Architektura | Kanały to adaptery wejściowe, LLM i wyszukiwarka to adaptery za portami (architektura heksagonalna). Modele bierzemy z Vertex AI w GCP (dowolny dostępny tam model, niekoniecznie Claude) i zmieniamy konfiguracją. Kontrakty są w repozytorium meritum-core, jedynym źródle prawdy. |
| Fakty | Werdykty rozstrzygające wymagają cytatu i przesłanek (walidacja kontraktu). Awaria, niejasne pytanie i pytanie poza zakresem to osobne stany bez twierdzeń. „Poza zakresem” dostaje tylko nieobsługiwany typ wejścia albo prośba, która nie dotyczy informacji, a każde twierdzenie o fakcie dostaje werdykt. Sprzeczne wiarygodne źródła dają „brak wystarczających dowodów” z cytatami obu stron obok siebie i bez siły. Siłę mają tylko werdykty rozstrzygające, liczoną z wydawców, których cytaty zgadzają się z werdyktem. |
| Aktualność | Data publikacji i pobrania przy każdym źródle, preferowanie świeżych, ostrzeżenie o dowodzie nieaktualnym (w treści zadania: materiał archiwalny). Każde twierdzenie ma datę, której dotyczy, z zapisanym pochodzeniem (tekst, data publikacji treści albo dziś); od niej liczymy wiek: domyślnie 365 dni, dla ostrzeżeń, dróg, pogody i danych hydrologicznych godziny albo dni według katalogu. Dowód nieaktualny daje siłę „słaba”. Obowiązujący akt prawny, strona urzędowa aktualizowana w miejscu i dowód o zdarzeniu z przeszłości nie są nieaktualne. Dowód zastąpiony nowszym w dacie twierdzenia nie tworzy rozbieżności i nie liczy się do siły. Stara treść puszczona znowu w obieg to osobna sprawa: werdykt „wprowadzające w błąd”. |
| Bezpieczeństwo | Nasz detektor (wzorce po polsku i angielsku, izolowany klasyfikator LLM) przed każdym wywołaniem modelu, w każdym kroku; Google Cloud Model Armor to opcjonalna druga warstwa, bo polskiego nie ma wśród jego testowanych języków. Odporność mierzymy na polskim zestawie ataków. Wejście użytkownika, podany link i treść źródeł są danymi we wszystkich krokach. Polecenie w treści użytkownika wycinamy, a resztę analizujemy; źródło z poleceniem wypada z dowodów. Strony z katalogu skanujemy przy wczytywaniu, strony z wyszukiwania czekają w kwarantannie. Model bez narzędzi z efektami ubocznymi, sekrety tylko w zmiennych środowiska, limit zapytań (slowapi według adresu IP, regionu i kanału, Cloudflare przed API), zapis zdarzeń. |
| Prywatność | Maskowanie telefonów, e-maili i PESEL-i przed analizą, retencja 30 dni, przycisk „Usuń moje sprawdzenia”. Konto nie jest potrzebne: historia rozmowy zostaje w sessionStorage. Logowanie kontem Google albo Microsoft jest opcjonalne; wtedy historia jest na serwerze i można ją usunąć razem z kontem. Adresy IP i retencję logów opisuje polityka prywatności, a Discord, SMS i wtyczka mają osobne polityki. Identyfikator z Discorda i numer telefonu służą tylko do odpowiedzi i liczenia powtórzeń, są przechowywane jako skrót z solą przez 30 dni i nie trafiają do moderatorów; usuwa je polecenie /usun-moje-dane albo SMS ze słowem USUN. Na Discordzie, w SMS-ach i w MCP identyfikatorem sesji jest ten skrót. Każdy kanał przy pierwszym kontakcie mówi, że odpowiada system AI (AI Act, art. 50, od 2 sierpnia 2026 r.). |
| Obserwowalność | Czas odpowiedzi, modele, błędy wyszukiwania, wstrzymania, koszt każdej odpowiedzi. |
| Zależności zewnętrzne | Opis kluczy, limitów, kosztów i rejestr podmiotów przetwarzających z krajem (niżej). Brak klucza, limit, awaria wyszukiwania albo modelu kończą się stanem „Problem techniczny” z komunikatem, nigdy werdyktem ani odpowiedzią z samego korpusu. |
| Czas | Treść zadania wymaga mediany do 30 s, my optymalizujemy pod najwyżej 30 s; po 30 s system niczego nie przerywa. Agenty badawcze działają równolegle, a agent główny strumieniuje odpowiedź z postępem badań. Czas bierzemy z zapisu przebiegu, mierzony przez kanał; nieudane przypadki zostają w medianie. |
| Spójność kanałów | Pamięć wyników pod kluczem ze znormalizowanego wejścia przez stały czas (np. 2 h), tylko z częścią merytoryczną; eskalację liczymy przy każdym zapytaniu. Migawki korpusu według harmonogramu (np. co godzinę), temperatura 0 i przypięta wersja modelu. Test spójności porównuje JSON z CheckResult, a nie wyrenderowany tekst. |
| Koszt i skalowanie | Koszt każdego sprawdzenia z tokenów i wywołań wyszukiwarki, koszt 1 000 zapytań i utrzymania kanałów, odsetek trafień w pamięci wyników, kolejka DBOS z limitem współbieżności, HTTP 429 z jasnym komunikatem według własnego licznika oczekujących sprawdzeń, autoskalowanie w GCP. Liczby podamy po pomiarze. |
| Pętla informacji | Sprawa moderatora dla pytań bez odpowiedzi w tematach wysokiego ryzyka, dla drugiego podobnego pytania od kogokolwiek i w dowolnym kanale oraz po kliknięciu „Zgłoś błąd”, z grupowaniem podobnych twierdzeń; liczba różnych pytających podnosi tylko priorytet. Moderator i pytający dostają powiadomienia (toasty i skrzynka). Panel z rolami moderatora, analityka i administratora. Interfejs odróżnia „zalecamy przekazanie” od „przekazano”. |

### Rejestr podmiotów przetwarzających

Co jest przetwarzane w UE, a co poza nią. Ten sam rejestr jest w ADR-14 dokumentu produktowego, w README i w politykach prywatności kanałów.

| Podmiot | Kraj lub region | Jakie dane | Po co |
|---|---|---|---|
| Serwer zespołu (on-prem) | do uzupełnienia przez zespół | wszystko, co dziś przetwarza demo | obecne demo (meritum.gburek.app) do migracji do GCP |
| Cloudflare | USA | całe żądania i odpowiedzi, w tym treść pytań i adresy IP (tunel kończy TLS) | tunel, TLS, ochrona przed DDoS i limity |
| GCP europe-central2 (docelowo) | UE (Warszawa) | API, worker, PostgreSQL z zapisami, sprawami i korpusem | docelowe demo |
| Cloud Storage (bucket prywatny) | GCP europe-central2 (Warszawa) | pliki audio i obrazy ze sprawdzeń | przechowywanie plików przez czas życia zapisu sprawdzenia |
| Vertex AI | GCP, region UE z wybranym modelem | zamaskowane pytanie, fragmenty źródeł, odpowiedzi modelu | modele |
| Model Armor (kandydat na klasyfikator wstrzyknięć) | GCP, multi-region eu | treść każdego wywołania modelu | wykrywanie wstrzyknięć przed modelem |
| Cloudflare Workers AI (kandydat) | Cloudflare, poza UE; region do sprawdzenia | wejście użytkownika, pobrane strony, fragmenty źródeł | klasyfikator wstrzyknięć i reranker, jeśli wygrają w ewaluacji |
| Vertex AI ranking API (kandydat) | GCP, region do sprawdzenia | zamaskowane twierdzenia, fragmenty źródeł | reranking fragmentów przed modelem |
| Google Sensitive Data Protection (DLP) | GCP, region UE | wejście użytkownika przed maskowaniem, wyniki kroków | maskowanie danych osobowych |
| Mistral w Vertex AI (opcja) | GCP europe-west4 | zamaskowane pytanie, fragmenty źródeł, odpowiedzi modelu | opcjonalny model od dostawcy z UE |
| Speech-to-Text v2 (Chirp 3) | GCP, multi-region eu | pliki audio i transkrypcje | weryfikacja nagrań |
| Vertex AI (embeddingi) | GCP, region UE; dostępność modelu w europe-central2 do sprawdzenia | zamaskowane twierdzenia, fragmenty, opisy incydentów | wyszukiwanie i podobieństwo |
| Vertex AI Search | GCP, lokalizacja global (poza gwarancją UE) | zapytania z zamaskowanych twierdzeń | wyszukiwanie na żywo w domenach katalogu |
| SearXNG (własna instancja) | nasz serwer; zapytania trafiają dalej do wyszukiwarek, z których korzysta, także spoza UE | zapytania z zamaskowanych twierdzeń | zapasowe wyszukiwanie na żywo |
| Linkup (opcja) | Francja; bez umowy Enterprise zapytania mogą trafić do US, EU, CA albo APAC | zapytania z zamaskowanych twierdzeń | opcjonalne wyszukiwanie na żywo |
| Firecrawl (opcja) | USA | adresy i treść pobieranych stron | opcjonalne hostowane pobieranie stron; §8.d regulaminu daje Firecrawl nieodwołalną licencję do przesłanych treści |
| Google Fact Check Tools API | Google, region do sprawdzenia | zapytania z twierdzeniami | adresy i oceny ClaimReview, które mogą być przesłanką werdyktu |
| Serwer MCP EUvsDisinfo (Vercel) | USA | token i nasze zapytania o strony bazy, bez danych użytkowników | lokalna kopia EUvsDisinfo |
| Powiadomienia moderatora: Cloudflare Email Workers, Gmail API albo webhook (np. Google Chat) | Cloudflare albo Google, region do sprawdzenia | e-mail moderatora, numer i streszczenie sprawy | powiadomienia moderatora |
| GitHub | USA | kod, zgłoszenia, logi CI, bez danych użytkowników | repozytoria i CI |
| Jasnopis (jeśli przez API) | do sprawdzenia | próbka odpowiedzi z ewaluacji | ocena zrozumiałości |
| Discord | USA | nazwa i identyfikator użytkownika, treść wiadomości, wiadomości głosowe i odpowiedź | kanał Discord |
| SMS Gateway for Android, sms-gate.app (tryb Cloud) | api.sms-gate.app; dostawca nie podaje regionu, poza gwarancją EOG | numer telefonu, treść SMS-a i odpowiedź | kanał SMS (US-WTY-07) |
| Google i Microsoft (logowanie) | USA | identyfikator konta | opcjonalne logowanie, jeśli starczy czasu |

### Funkcje premiowane

Punkty za funkcje premiowane liczą się tylko wtedy, gdy rozwiązanie spełnia wymagania podstawowe.

Bierzemy:

1. Łańcuch dowodowy: od twierdzenia do cytatów potwierdzających, obalających i uzupełniających kontekst, na osi czasu z datami i z informacją, co zmieniłoby werdykt.
2. Zamknięta pętla informacji: sprawy moderatora, grupowanie podobnych twierdzeń, przycisk „Zgłoś błąd” i powiadomienia.
3. Otwarty katalog źródeł z zasadami kwalifikowania, aktualizowania i wykluczania (`CatalogEntry`) i ewidencją źródeł.
4. Dopasowanie do bazy incydentów od organizatora i do lokalnej kopii EUvsDisinfo jako kontekst, nigdy jako werdykt; teksty „fact” z EUvsDisinfo jako cytaty. Scenariusz I jest w zestawie jury, więc budujemy to w MVP.
5. Weryfikacja nagrań: plik audio albo wiadomość głosowa z Discorda, transkrypcja Chirp 3 w regionie UE, potem zwykłe sprawdzenie.
6. Jawne miejsce przetwarzania: rejestr podmiotów przetwarzających (co w UE, a co poza nią), docelowo aplikacja w GCP `europe-central2` i modele przez Vertex AI w regionie UE, opcjonalnie Mistral Small 3.1 w `europe-west4`, publiczny kod i opis drogi do samodzielnego hostowania (otwarty model na własnym serwerze z GPU po hackathonie, europejski indeks wyszukiwania).

Jeśli starczy czasu:

7. Obraz: OCR, metadane i wyszukiwanie wcześniejszych wystąpień (scenariusz F), z jawnymi ograniczeniami. Do tego czasu obraz dostaje stan „poza zakresem”.
8. Wielojęzyczne wyszukiwanie z odpowiedzią po polsku.
9. Eksport FIMI: JSON, CSV i paczka STIX 2.1 dla OpenCTI, kody technik zmapowane na DISARM do potwierdzenia przez analityka.
10. Kontrolowana archiwizacja materiału wskazanego przez użytkownika, z podstawą prawną, retencją, kontrolą dostępu i procedurą usunięcia.

---

## 3. Wyróżniki

### 3.1 Uczciwość wbudowana w kontrakt
Reguły z treści zadania sprawdza walidacja danych, a nie prompt: werdykt bez cytatu, siła niezgodna z przesłankami, „potwierdzone” przy sprzecznych źródłach i awaria pokazana jako werdykt nie przejdą. Każdą regułę sprawdza test pytest w meritum-core (`tests/test_checks_contracts.py`).

### 3.2 Cytat sprawdzany dosłownie
Model może się pomylić w cytacie. Dlatego zanim cytat trafi do odpowiedzi, sprawdzamy w kodzie, czy fragment naprawdę jest w źródle. To podnosi oba mierniki: pokrycie i poprawność cytowań.

### 3.3 Siła odpowiedzi z jawnych przesłanek
Pod werdyktem czytelnik widzi: ile niezależnych źródeł, ile urzędowych, jak świeże i czy są zgodne. Z tego jedną regułą wynika „mocna”, „umiarkowana” albo „słaba”. Nie ma tu liczby wymyślonej przez model.

### 3.4 Sprawdzanie tam, gdzie jesteś
Formularz działa dla każdego, bez instalacji i bez zakładania konta. Bot na Discordzie odpowiada na kanale serwera i w wiadomości prywatnej. Wtyczka dodaje „Sprawdź” pod postem na X, Facebooku, Instagramie, Reddicie i TikToku, w stylu danej platformy. Treść posta wysyłamy dopiero po kliknięciu.

### 3.5 Świeże źródła bez wychodzenia poza katalog
Bieżące wydarzenia sprawdzamy w publikacjach z zatwierdzonych serwisów. Wyszukiwanie w całym internecie łamałoby zasadę „jasno opisanego zbioru źródeł”, więc go nie robimy.

### 3.6 Człowiek tam, gdzie system nie rozstrzyga
Na hackathonie pytania bez odpowiedzi trafiają do kolejki moderatora, a podobne twierdzenia łączą się w jedną sprawę. Zatwierdzanie odpowiedzi przez człowieka przed publikacją, jak w trybie wspierania decyzji z §9 zadania, planujemy na pilotaż.

### 3.7 Uczymy rozpoznawania
Odpowiedź nazywa technikę (wyrwanie z kontekstu, nieaktualna informacja, fałszywy autorytet, wybiórcze dane) i w jednym zdaniu mówi, jak ją rozpoznać następnym razem.

### 3.8 Ta sama dezinformacja w innym języku
Lokalna kopia EUvsDisinfo i embeddingi wielojęzyczne pozwalają dopasować polskie twierdzenie do przypadku opisanego po angielsku albo rosyjsku i zacytować gotowe sprostowanie z bazy.

### 3.9 Metoda na widoku
Strona „Jak działa Meritum” opisuje metodę według zasad IFCN i EFCSN: katalog źródeł, mierniki z ostatniej ewaluacji, politykę poprawek i drogę do pilotażu z §9. Każda karta ma przycisk „Zgłoś błąd”.

---

## 4. Pitch (scena główna: to samo pytanie w dwóch kanałach)

1. **Problem (20 s):** „Od stycznia nie zapłacisz gotówką” krąży w wiadomościach. Sprostowanie istnieje, ale nie tam, gdzie ludzie czytają, a czat AI odpowie płynnie, choć bez źródła.
2. **Formularz (40 s):** wklejamy tekst: dwa twierdzenia, dwa werdykty, cytaty wyłącznie ze źródeł z katalogu (np. ustawa z ISAP), siła podstawy, ograniczenia.
3. **Discord (30 s):** ten sam tekst wysłany botowi na makiecie Discorda, ten sam wynik. Wtyczkę pod postem na X pokazujemy tylko wtedy, gdy starczy czasu.
4. **Uczciwość (30 s):** świeża plotka bez publikacji, system się wstrzymuje i zakłada sprawę moderatora. Strona z ukrytym poleceniem „zignoruj reguły”, system je ignoruje i zapisuje zdarzenie.
5. **Wyniki (30 s):** tabela mierników z naszego zestawu testowego i koszt 100 sprawdzeń.
6. **Zamknięcie:** *„Każde ustalenie ma źródło. Gdy źródeł brak, mówimy to wprost.”*

---

## 5. Scenariusz filmu (do 3 minut)

| Czas | Ekran | Co mówi prowadzący |
|---|---|---|
| 0:00 | Formularz na telefonie | „Wklejasz to, co dostałeś. Konto nie jest potrzebne, instalacja też nie.” |
| 0:20 | Wynik z dwoma twierdzeniami | „Każdy werdykt ma cytat, wydawcę i datę. Siła wynika z tego, co widzisz.” |
| 0:50 | Makieta Discorda, wiadomość do bota | „Ten sam rdzeń na Discordzie. Ten sam wynik.” |
| 1:20 | Brak dowodów, sprawa #S-… | „Nie wiemy, więc nie zgadujemy. Sprawa trafia do moderatora.” |
| 1:50 | Próba wstrzyknięcia poleceń | „Strona próbuje przejąć model. Zignorowane i zapisane.” |
| 2:20 | Tabela mierników, koszt, architektura | „Wyniki odtworzysz jednym poleceniem z repozytorium.” |
| 2:45 | Zamknięcie | Hasło. |

Demo działa na prawdziwym korpusie i prawdziwym API. Żadna odpowiedź nie jest nagrana ani zaszyta w kodzie, bo jury wpisze własne pytania.

---

## 6. Pytania jury i odpowiedzi

- **„Kto decyduje, co jest prawdą?”** Źródła. Model rozumie pytanie, szuka i pisze, ale werdykt wymaga dosłownego cytatu, a siłę liczy reguła. Czego nie da się ustalić, trafia do ludzi.
- **„Co z halucynacjami?”** Cytat, którego nie ma w źródle, odpada w kodzie przed pokazaniem. Wyjaśnienie modelu jest oznaczone jako interpretacja.
- **„Stronniczość źródeł?”** Katalog jest jawny, z powodem kwalifikacji i wykluczenia. Nie oceniamy treści po domenie ani autorze. Status źródła pokazujemy jako osobną, neutralną informację tylko dla podmiotów z oficjalnej listy sankcji UE.
- **„Prompt injection?”** Przed każdym wywołaniem modelu działa nasz detektor, a Model Armor może być drugą warstwą. Odporność mierzymy na polskich atakach. Wejście użytkownika, link i treść źródeł to dane. Polecenie w pytaniu wycinamy, a resztę sprawdzamy. Strony skanujemy przy wczytywaniu, a te z wyszukiwania czekają w kwarantannie. Model nie ma narzędzi, które coś zmieniają. Próby zapisujemy.
- **„Gdzie są przetwarzane dane?”** Rejestr podmiotów przetwarzających mówi to dla każdej części danych. W UE docelowo działa aplikacja z bazą (GCP `europe-central2`, Warszawa) i modele przez Vertex AI w regionie UE, w którym jest dostępny wybrany model. Poza UE są Cloudflare (tunel i TLS, widzi całe żądania), wyszukiwanie Vertex AI Search w lokalizacji global, Discord, GitHub, serwer MCP EUvsDisinfo i opcjonalne logowanie Google albo Microsoft. Transkrypcja nagrań działa w regionie UE. W trakcie prac demo działa na serwerze zespołu; do GCP przeniesiemy je przez CI/CD, możliwe, że jeszcze w trakcie hackathonu. Dostawcę modelu i wyszukiwarki da się wymienić.
- **„Ile to kosztuje?”** Koszt każdego sprawdzenia liczymy z zapisu przebiegu (tokeny, wywołania wyszukiwarki), a z niego koszt 100 testów, 1 000 zapytań i utrzymania każdego kanału. Liczby podajemy po pomiarze. Przy większym ruchu sprawdzenia czekają w kolejce, a ponad limit API odpowiada HTTP 429 z jasnym komunikatem.
- **„Na czym stroicie progi?”** Na golden secie (zestawie deweloperskim) z materiałów bazy wiedzy. Zestaw jury od MSZ jest dla nas ukryty.
- **„Nie mam kluczy API.”** README ma dwie ścieżki: publiczne demo bez kluczy i uruchomienie lokalne z własnymi kluczami. Brakujące klucze zgłasza test gotowości przy starcie, nigdy odpowiedź.
- **„Czy kod będzie publiczny?”** Tak, wszystkie repozytoria i system na koniec prac, z instrukcją uruchomienia przez `docker compose up`.
- **„Dlaczego Discord, a nie WhatsApp?”** Discord nie wymaga konta firmowego ani opłat operatora, a jury przetestuje go na makiecie bez dołączania do serwera. Ten sam rdzeń obsługuje wtyczkę, która działa tam, gdzie człowiek widzi treść, a jeśli starczy czasu, także SMS przez bramkę z jawnymi opłatami operatora.

---

## 7. Najważniejsze ryzyka (do README i prezentacji)

| Ryzyko | Jak ograniczamy |
|---|---|
| Halucynacje | Dosłowna weryfikacja cytatów, werdykt tylko z cytatem, wstrzymanie się przy braku dowodów. |
| Stronniczość źródeł | Jawny katalog z zasadami, co najmniej dwa typy źródeł, rozbieżności pokazywane wprost. |
| Prywatność | Maskowanie danych osobowych, retencja 30 dni, usuwanie sesji, konta opcjonalne z usuwaniem historii i konta, identyfikatory z Discorda i SMS jako skrót z solą, adresy IP i logi według polityki prywatności, osobne polityki kanałów, rejestr podmiotów przetwarzających. |
| Prompt injection | Nasz detektor przed każdym wywołaniem modelu, opcjonalnie Model Armor jako druga warstwa, pomiar na polskim zestawie ataków, dane oddzielone od instrukcji we wszystkich krokach, skan stron przy wczytywaniu i kwarantanna stron z wyszukiwania, brak narzędzi z efektami ubocznymi, zapis zdarzeń, testy ze scenariusza E. |
| Dostępność | WCAG 2.2 AA, prosty język, formularz na telefonie bez instalacji. |
| Nadużycia | Limit zapytań według adresu IP, regionu i kanału, Cloudflare przed API, walidacja wejścia. Na hackathonie system nie publikuje odpowiedzi, a pytania bez odpowiedzi trafiają do kolejki moderatora; zatwierdzanie odpowiedzi przed publikacją planujemy na pilotaż. |
| Awaria dostawcy | Błąd, limit czasu albo limit zapytań wyszukiwania i awaria modelu dają stan „Problem techniczny” z komunikatem, nigdy pozorny werdykt (scenariusz J). |
| Koszt i ruch | Koszt mierzony dla każdego sprawdzenia, kolejka z limitem współbieżności, HTTP 429 z komunikatem według własnego licznika, autoskalowanie w GCP. |
| Czas i obciążenie (ryzyko przyjęte) | 30 s to cel, pod który optymalizujemy; po 30 s nic się nie dzieje. Ocena wymowy każdego cytatu mnoży wywołania modelu i warstwy kontroli, a slowapi liczy w pamięci każdego procesu. Zalecamy, bez zobowiązania: pamięć wyników skanu według skrótu fragmentu, jedno wywołanie oceny wymowy na twierdzenie, wspólny licznik w PostgreSQL albo Redisie. |
| Prawa autorskie i licencje | Na hackathonie nie podejmujemy działań prawnych. Ryzyka z zalecanymi środkami (prawo cytatu, zgoda organizatora na piśmie, ponowne wykorzystanie informacji sektora publicznego, wyjątek eksploracji tekstów i danych, warunki Google API, retencja korpusu, lista komponentów zewnętrznych z licencjami) są w sekcji 6 dokumentu produktowego. |

---

## 8. Czego nie mówimy

- Nie podajemy skuteczności, której nie zmierzyliśmy, ani wyników bez danych do odtworzenia.
- Nie twierdzimy, że współpracujemy z MSZ, NASK ani z fact-checkerami. Mówimy „gotowe do integracji z…”.
- Nie deklarujemy wyszukiwania odwrotnego obrazu, dopóki go nie ma.
- Nie mówimy, że wszystkie dane są przetwarzane w UE: część usług działa w USA (rejestr podmiotów przetwarzających).
- Nie nazywamy systemu „sędzią prawdy”.

---

## 9. Nazwa: Meritum

**Meritum — obywatelski radar dezinformacji.** „Meritum” to „sedno sprawy”: odpowiedź mówi, o co naprawdę chodzi, i pokazuje, skąd to wiemy. „Obywatelski”, bo służy obywatelowi, a nie platformie. Przed pitchem trzeba sprawdzić znak towarowy i wolne domeny. Nazwa bywa używana przez inne firmy, więc w materiałach zawsze idzie z podtytułem.

## 10. Zakres na hackathon

**Budujemy:** najpierw szkielet end-to-end (formularz, API, workflow DBOS, model zastępczy, zapis przebiegu, karta wyniku), potem prawdziwe części: formularz WWW z nagraniami audio, bota na Discordzie (kanały serwera, wiadomości prywatne, wiadomości głosowe, link zaproszenia) z makietą Discorda dla jury, „Sprawdź” we wtyczce i w popupie, rdzeń weryfikacji (twierdzenia, wyszukiwanie hybrydowe, werdykt, cytaty, przesłanki, dowody zastąpione), korpus z katalogiem i ewidencją źródeł, cykliczne RSS i mapy stron, wyszukiwanie na żywo przez Vertex AI Search, lokalną kopię EUvsDisinfo i bazę incydentów, zapis przebiegu, sprawy moderatora z deduplikacją, „Zgłoś błąd” i panel z rolami, powiadomienia (toasty i skrzynka), ochronę przed wstrzykiwaniem poleceń, informację o AI w każdym kanale, historię rozmowy w sessionStorage, osobne polityki prywatności kanałów, limity zapytań, pomiar kosztu, ewaluację w pydantic-evals ze stroną ewaluacji i paczką do odtworzenia, stronę „Jak działa Meritum”, `docker compose`, demo (teraz na serwerze zespołu, docelowo w GCP), materiały z §4. Zakres jest szeroki, bo budujemy równolegle z wieloma agentami programistycznymi.

**Jeśli starczy czasu:** kanał SMS, logowanie kontem Google albo Microsoft z rozmowami na serwerze (opcjonalne, nigdy wymagane), obraz (OCR, metadane, wyszukiwanie wcześniejszych wystąpień), ostrzeżenie o statusie źródła, wyszukiwanie wielojęzyczne, eksport FIMI (JSON, CSV, STIX 2.1, DISARM), serwer MCP z konektorem dla aplikacji czatu AI (ChatGPT, claude.ai), kontrolowana archiwizacja, odpowiedzi moderatora i powiadomienia o nowych dowodach.

**Po hackathonie:** zatwierdzanie odpowiedzi moderatorów przed publikacją (z konsensusem pomostowym), otwarty model na własnym serwerze z GPU.

**Pytania do mentorów MSZ** (gotowa wiadomość w załączniku A dokumentu produktowego): czy wtyczka przeglądarki to „rozwiązanie równoważne” drugiemu kanałowi (warunek dwóch kanałów od tego nie zależy, bo spełniają go formularz i Discord), licencja EUvsDisinfo (token już mamy) i bazy incydentów, jawna część zestawu referencyjnego, fact-checkerzy na liście źródeł i pisemna zgoda na pobieranie i cytowanie źródeł z listy.
