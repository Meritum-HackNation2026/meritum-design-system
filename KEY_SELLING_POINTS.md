# Meritum: key selling points

**Meritum — obywatelski radar dezinformacji.** Konkurs MSZ „Prawdowid”.

Dokument roboczy dla całego zespołu: czym się wyróżniamy, jak odpowiadamy na każde wymaganie z treści zadania i co pokazać na demo. Pełna treść zadania jest w `../konkursy/`.

Pokazujemy tylko liczby zmierzone naszym skryptem ewaluacji na opublikowanym zestawie testowym, razem z danymi do odtworzenia. Nie obiecujemy skuteczności, której nie zmierzyliśmy.

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
| Dwa kanały | Formularz WWW (podstawowy) i przycisk „Sprawdź” we wtyczce Chrome pod postem oraz okienko do wklejenia w popupie. Ten sam rdzeń, ten sam wynik. Zapas: bot na Discordzie na tym samym API. |

### Minimalny zakres (MVP)

| Wymaganie | Nasza odpowiedź |
|---|---|
| Rozpoznawanie twierdzeń | LLM ze strukturalnym wyjściem oddziela twierdzenia od opinii. |
| Zbiór źródeł: co najmniej 2 typy | Źródła pierwotne i urzędowe (ISAP, EUR-Lex, dane.gov.pl, gov.pl, BIP) oraz wtórne (fact-checkerzy IFCN/EFCSN, EUvsDisinfo). Co najmniej 100 dokumentów z co najmniej 10 domen, lista do audytu z licencją i powodem kwalifikacji. |
| Bieżące wydarzenia | Cykliczne pobieranie RSS z katalogu i wyszukiwanie na żywo (Firecrawl) ograniczone do domen z katalogu. Każda pobrana strona trafia do korpusu z datą publikacji i pobrania. |
| Wynik, uzasadnienie, siła podstawy, ograniczenia | Jeden z pięciu werdyktów na twierdzenie, wyjaśnienie oznaczone jako interpretacja, siła liczona regułą z przesłanek, zawsze sekcja „Ograniczenia”. |
| Źródło: tytuł, wydawca, data, link, fragment | Wszystkie pięć pól w kontrakcie `Source` i `Citation`. |
| Prosty polski | Teksty w `copy/pl.json`, pisane dla osoby bez wiedzy technicznej. |
| Zapis przebiegu | `CheckRecord`: pytanie z zamaskowanymi danymi, czas, kanał, źródła, werdykty, modele, region, koszt, błędy wyszukiwania, próby wstrzyknięcia poleceń. |

### Wymagania techniczne

| Obszar | Nasza odpowiedź |
|---|---|
| Architektura | Kanały to adaptery wejściowe, LLM i wyszukiwarka to adaptery za portami (architektura heksagonalna). Model zmieniamy konfiguracją. |
| Fakty | Werdykty rozstrzygające wymagają cytatu i przesłanek (walidacja kontraktu). Awaria, niejasne pytanie i pytanie poza zakresem to osobne stany bez twierdzeń. |
| Aktualność | Data publikacji i pobrania przy każdym źródle, preferowanie świeżych, ostrzeżenie o materiale archiwalnym. |
| Bezpieczeństwo | Walidacja wejścia, treść źródeł oddzielona od instrukcji, model bez narzędzi z efektami ubocznymi, sekrety tylko w zmiennych środowiska, limit zapytań, zapis zdarzeń. |
| Prywatność | Maskowanie telefonów, e-maili i PESEL-i przed analizą, retencja 30 dni, przycisk „Usuń moje sprawdzenia”. |
| Obserwowalność | Czas odpowiedzi, modele, błędy wyszukiwania, wstrzymania, koszt każdej odpowiedzi. |
| Zależności zewnętrzne | Opis kluczy, limitów, kosztów i regionu. Brak klucza albo limit kończą się stanem „Problem techniczny”, nigdy werdyktem. |
| Pętla informacji | Sprawa moderatora dla nierozstrzygniętych, ryzykownych i powtarzających się pytań, z deduplikacją. Interfejs odróżnia „zalecamy przekazanie” od „przekazano”. |

### Funkcje premiowane, które bierzemy

1. **Łańcuch dowodowy:** od twierdzenia do cytatów potwierdzających, obalających i uzupełniających kontekst.
2. **Zamknięta pętla informacji:** sprawy moderatora i grupowanie podobnych pytań.
3. **Otwarty katalog źródeł** z zasadami kwalifikowania, aktualizowania i wykluczania (`CatalogEntry`).
4. **Wielojęzyczne wyszukiwanie** z odpowiedzią po polsku.
5. **Dopasowanie do bazy incydentów** od organizatora jako kontekst, nigdy jako werdykt.
6. **Zrzut ekranu z OCR** (scenariusz F), z jawnymi ograniczeniami.
7. **Eksport JSON i CSV**, kody technik zmapowane na DISARM.
8. **Przetwarzanie w EOG** tam, gdzie to możliwe, i opis drogi do samodzielnego hostowania (otwarty model na własnym serwerze z GPU, europejski indeks wyszukiwania).

---

## 3. Wyróżniki

### 3.1 Uczciwość wbudowana w kontrakt
Reguły z treści zadania sprawdza walidacja danych, a nie prompt: werdykt bez cytatu, siła niezgodna z przesłankami, „potwierdzone” przy sprzecznych źródłach i awaria pokazana jako werdykt nie przejdą. Każdą regułę sprawdza test (`contracts/export_schema.py`).

### 3.2 Cytat sprawdzany dosłownie
Model może się pomylić w cytacie. Dlatego zanim cytat trafi do odpowiedzi, sprawdzamy w kodzie, że fragment naprawdę jest w źródle. To podnosi oba mierniki: pokrycie i poprawność cytowań.

### 3.3 Siła odpowiedzi z jawnych przesłanek
Pod werdyktem czytelnik widzi: ile niezależnych źródeł, ile urzędowych, jak świeże i czy są zgodne. Z tego jedną regułą wynika „mocna”, „umiarkowana” albo „słaba”. Nie ma tu liczby wymyślonej przez model.

### 3.4 Sprawdzanie tam, gdzie czytasz
Formularz działa dla każdego, bez instalacji. Wtyczka dodaje „Sprawdź” pod postem na X, Facebooku, Instagramie, Reddicie i TikToku, w stylu danej platformy. Treść posta wysyłamy dopiero po kliknięciu.

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
| 0:00 | Formularz na telefonie | „Wklejasz to, co dostałeś. Bez konta i bez instalacji.” |
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
- **„Prompt injection?”** Treść źródeł to dane, nie instrukcje. Model nie ma narzędzi, które coś zmieniają. Próby zapisujemy.
- **„Gdzie są przetwarzane dane?”** GCP w `europe-central2`. Dostawcę modelu i wyszukiwarki opisujemy z regionem i kosztem, a oba da się wymienić.
- **„Ile to kosztuje?”** Koszt 1 000 zapytań liczymy z zapisu przebiegu (tokeny, wywołania wyszukiwarki). Podajemy zmierzony koszt 100 testów.
- **„Dlaczego wtyczka, a nie WhatsApp?”** Wtyczka działa tam, gdzie człowiek widzi treść, i nie wymaga konta firmowego ani opłat operatora. Ten sam rdzeń obsłuży kolejne kanały bez przebudowy.

---

## 7. Najważniejsze ryzyka (do README i prezentacji)

| Ryzyko | Jak ograniczamy |
|---|---|
| Halucynacje | Dosłowna weryfikacja cytatów, werdykt tylko z cytatem, wstrzymanie się przy braku dowodów. |
| Stronniczość źródeł | Jawny katalog z zasadami, co najmniej dwa typy źródeł, rozbieżności pokazywane wprost. |
| Prywatność | Maskowanie danych osobowych, retencja 30 dni, usuwanie sesji, brak kont. |
| Prompt injection | Separacja instrukcji od danych, brak narzędzi z efektami ubocznymi, zapis zdarzeń, testy ze scenariusza E. |
| Dostępność | WCAG 2.2 AA, prosty język, formularz na telefonie bez instalacji. |
| Nadużycia | Limit zapytań, walidacja wejścia, brak publikacji bez człowieka. |
| Awaria dostawcy | Stan „Problem techniczny”, nigdy pozorny werdykt (scenariusz J). |

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

**Budujemy:** formularz WWW, „Sprawdź” we wtyczce i w popupie, rdzeń weryfikacji (twierdzenia, wyszukiwanie hybrydowe, werdykt, cytaty, przesłanki), korpus z katalogiem, cykliczne RSS i wyszukiwanie Firecrawl w domenach z katalogu, zapis przebiegu, sprawy moderatora z deduplikacją, ochronę przed wstrzykiwaniem poleceń, skrypt ewaluacji, `docker compose`, publiczne demo.

**Jeśli starczy czasu:** OCR zrzutu ekranu, dopasowanie do bazy incydentów, eksport JSON i CSV z kodami DISARM, serwer MCP, bot na Discordzie (obowiązkowo, jeśli mentorzy nie uznają wtyczki za kanał).

**Pomijamy:** konta użytkowników, wyszukiwanie odwrotne obrazu, transkrypcję nagrań, konsensus pomostowy przy publikacji odpowiedzi moderatorów (pomysł na później).

**Otwarte pytanie do mentorów MSZ:** czy wtyczka przeglądarki to „rozwiązanie równoważne” drugiemu kanałowi.
