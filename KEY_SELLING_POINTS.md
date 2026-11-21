# Meritum: key selling points

**Meritum — obywatelski radar dezinformacji oraz scamu.** Jeden produkt, dwa konkursy.

Dokument roboczy dla całego zespołu. Opisuje, czym się wyróżniamy, jak rozegrać oba konkursy jednym produktem i co pokazać na demo. Robocza nazwa: Meritum.

Wszystkie liczby w demo są symulowane i tak je podpisujemy. Nie obiecujemy skuteczności, której nie zmierzyliśmy.

---

## 1. Jednym zdaniem

**Niezależna warstwa zaufania nad mediami społecznościowymi: z jednego zgłoszenia odsłania całą kampanię oszustów lub manipulatorów, a kontekst publikuje dopiero wtedy, gdy zgodzą się ludzie, którzy zwykle się nie zgadzają.**

Krócej, na slajd: *Jeden fejk, cała kampania. Jeden kontekst, ponad podziałami.*

---

## 2. Dlaczego jeden produkt pasuje do obu konkursów

Oba wyzwania opisują ten sam problem z dwóch stron:

| | MSZ „Prawdowid” | NASK „Kolekcjoner fejków” |
|---|---|---|
| Zagrożenie | manipulacja, dezinformacja | fałszywe reklamy z wizerunkiem znanych osób |
| Co je utrudnia | nadmiar informacji, brak wiarygodnych źródeł | szybko znikają, zmieniają formę, wracają pod nowymi adresami |
| Czego brakuje | narzędzia do świadomej oceny treści | szerszego obrazu: pojedynczy materiał to fragment kampanii |
| Czego oczekują | AI, weryfikacja, dotarcie do źródeł | dostrzeżenie skali i ochrona potencjalnych ofiar |

Wspólny rdzeń: **pojedyncza treść jest prawie zawsze fragmentem większej operacji.** Farma botów, która forsuje fałszywą narrację, i sieć domen, która rotuje reklamy z deepfake'iem prezentera, działają tak samo: wiele kopii, krótkie życie, skoordynowane konta. Dlatego budujemy jeden silnik, który:

1. **zbiera** zgłoszenia i ślady (Kolekcjoner),
2. **łączy** je w kampanie (graf kampanii),
3. **wyjaśnia** użytkownikowi, co widzi, ze źródłami (Prawdowid),
4. **chroni** przed kliknięciem i przed manipulacją głosowaniem.

Na każdy konkurs przygotowujemy inny pitch i inną scenę główną demo, ale pokazujemy ten sam działający produkt. To jest argument sam w sobie: jury widzi platformę, a nie jednorazowy prototyp.

---

## 3. Odpowiedź na każde zdanie z wyzwań

**MSZ „Prawdowid”**

| Zdanie z wyzwania | Nasza odpowiedź |
|---|---|
| „Fakt czy manipulacja?” | Notatka kontekstowa pod postem, ze stanem: zweryfikowany kontekst, w trakcie oceny, sporny. |
| „Wykorzystaj sztuczną inteligencję” | AI pisze szkic notatki z uwag użytkowników, analizy treści i źródeł. Nie decyduje o publikacji. |
| „Docierać do wiarygodnych źródeł” | Linki do źródeł są obowiązkowe. Notatka bez źródła nie może zostać opublikowana. Pokazujemy, z której strony sporu pochodzą media. |
| „Świadomie oceniać napotykane treści” | Każda notatka nazywa technikę manipulacji (np. wyrwanie z kontekstu, fałszywy autorytet) i w jednym zdaniu uczy, jak ją rozpoznać następnym razem. |

**NASK „Kolekcjoner fejków”**

| Zdanie z wyzwania | Nasza odpowiedź |
|---|---|
| „Wykorzystują wizerunki znanych osób” | Ostrzeżenie na reklamie: czyj wizerunek użyto bez zgody, z linkiem do dementi lub ostrzeżenia CERT Polska. |
| „Szybko znikają” | Sejf dowodów: wtyczka zapisuje zrzut, adres, łańcuch przekierowań i czas w chwili zobaczenia reklamy. Dowód zostaje, nawet gdy reklama zniknie. |
| „Zmieniają formę i wracają pod nowymi adresami” | Odciski kampanii: podobieństwo obrazu i wideo, twarz, szablon strony docelowej, rejestracje domen. Nowy wariant trafia do znanej kampanii w kilka sekund. |
| „Fragment znacznie większej kampanii” | Widok kampanii: wszystkie warianty, domeny i platformy na jednej osi czasu. |
| „Skuteczniej chronić potencjalne ofiary” | Blokada przed wejściem na stronę z kampanii, tryb opiekuna dla bliskich i eksport zgłoszenia w formacie gotowym dla CERT Polska. |

---

## 4. Siedem wyróżników

### 4.1 Konsensus ponad podziałami, odporny na boty
Notatka publikuje się dopiero, gdy osoby z grup, które zwykle oceniają inaczej, uznają ją za pomocną (algorytm „bridging”, ten sam typ co otwarty algorytm Community Notes, tylko niezależny od platformy). Większość nie wystarcza, więc farma botów nie przepchnie notatki ani jej nie zakopie.

- **Czemu unikalne:** żadne narzędzie fact-checkingowe w Polsce nie działa na wszystkich platformach naraz i nie pokazuje publicznie, że zgoda przyszła z obu stron.
- **Na demo:** atak 312 kont na żywo, wykres pokazuje 4 812 odrzuconych głosów, a status notatki się nie zmienia.

### 4.2 Graf kampanii: z jednego zgłoszenia do całej operacji
Każde zgłoszenie to okaz w kolekcji. System porównuje go z już znanymi okazami po:
- podobieństwie obrazu i klatek wideo (hash percepcyjny, embeddingi w pgvector),
- twarzy znanej osoby (tylko z rejestru osób, które się zgodziły, patrz 5.2),
- tekście reklamy i obietnicy (embeddingi),
- szablonie strony docelowej (odcisk struktury DOM),
- domenach i przekierowaniach (wspólne serwery, rejestratorzy, certyfikaty).

- **Czemu unikalne:** zgłoszenia na platformach są osobne i znikają razem z reklamą. My pokazujemy kampanię jako całość: kiedy ruszyła, ile ma wariantów, które domeny już padły, które działają.
- **Na demo:** użytkownik zgłasza jedną reklamę, a dashboard rozwija kampanię #K-118: 47 wariantów, 23 domeny, 9 dni.

### 4.3 Sejf dowodów
Fałszywe reklamy żyją godzinami. Wtyczka utrwala dowód w chwili zobaczenia: zrzut ekranu, adres, łańcuch przekierowań, nagłówki, znacznik czasu i hash pliku. Dowód można wyeksportować do zgłoszenia w CERT Polska lub do formularza zgłoszeń reklam na platformie.

- **Czemu ważne dla NASK:** CERT Polska działa w strukturach NASK. Dajemy mu materiał, który zwykle przepada.

### 4.4 Ostrzegamy przed domeną, zanim pojawi się reklama
Oszuści rejestrują nowe domeny i wystawiają dla nich certyfikaty TLS. Publiczne logi Certificate Transparency widać od razu. Obserwujemy w nich domeny podobne do znanych kampanii (literówki, te same słowa, ten sam wystawca) i oznaczamy je jako „prawdopodobnie następne”, zanim trafią do reklamy.

- **Efekt „wow”:** na osi czasu kampanii widać przerywaną linię „przewidywane domeny”. Jedna z nich zapala się w trakcie demo.
- **Uczciwie:** to sygnał do weryfikacji, a nie wyrok. Domena trafia do ostrzeżeń dopiero po potwierdzeniu przez ludzi.

### 4.5 Źródła obowiązkowe i spektrum źródeł
AI nie może opublikować twierdzenia bez linku. Pod notatką pokazujemy, skąd pochodzą cytowane media na osi od lewej do prawej. Kiedy notatka cytuje tylko jedną stronę, system prosi o źródło z drugiej, zanim pozwoli głosować.

- **Czemu ważne dla MSZ:** „docieranie do wiarygodnych źródeł” zamienia się w regułę produktu, a nie w obietnicę.

### 4.6 Uczymy rozpoznawania, a nie tylko podajemy werdykt
Każda notatka i każde ostrzeżenie nazywa technikę: wyrwanie z kontekstu, fałszywy autorytet, presja czasu („tylko dziś”), podszywanie się. Techniki dezinformacji mapujemy na otwarty framework DISARM, którego używa się w UE do opisu FIMI (zagranicznej manipulacji informacyjnej). Użytkownik po kilku notatkach sam zaczyna widzieć wzorce.

- **Czemu ważne dla MSZ:** to wprost „świadoma ocena treści”, a język DISARM i FIMI to język, którym MSZ i EEAS opisują zagrożenia.

### 4.7 Otwarte API i serwer MCP
Ten sam silnik weryfikacji wystawiamy jako API i jako serwer MCP (FastMCP). Dziennikarz albo analityk może zapytać swojego asystenta AI: „czy ta domena należy do znanej kampanii?” albo „jakie notatki dotyczą tego zdjęcia?” i dostać odpowiedź ze źródłami.

- **Czemu unikalne:** zamieniamy narzędzie w infrastrukturę. Redakcje, uczelnie i CERT mogą podpiąć się bez instalowania wtyczki.

---

## 5. Pomysły, które mogą zrobić różnicę

Uporządkowane od najtańszych do najdroższych na hackathonie.

1. **„Dlaczego to widzę?”** pod każdą notatką: jednym zdaniem, jak powstała (szkic AI z uwag 41 osób, 4 źródła, decyzja ludzi). Koszt: mały. Zaufanie: duże.
2. **Licznik „Uratowane kliknięcia”** w widoku kampanii: ile osób zobaczyło ostrzeżenie i nie weszło na stronę. W demo podpisany jako symulacja.
3. **Tryb opiekuna (dla bliskich).** Senior instaluje wtyczkę z kodem od wnuczki. Gdy próbuje wejść na stronę z kampanii inwestycyjnej, wtyczka zatrzymuje go i (za jego zgodą) wysyła powiadomienie zaufanej osobie. Ofiary oszustw „na celebrytę” to często osoby starsze, więc to jest najmocniejsza historia emocjonalna w pitchu NASK.
4. **Rejestr wizerunków (opt-in).** Znane osoby albo ich agencje zgłaszają swoją twarz i oficjalne kanały. Każda reklama z tą twarzą poza oficjalnymi kanałami dostaje ostrzeżenie automatycznie, a osoba dostaje raport kampanii, które jej używają. Bez zgody nie przetwarzamy twarzy (RODO).
5. **Predykcja domen z logów certyfikatów** (patrz 4.4).
6. **Ostrzeżenie w rytmie kampanii.** Kiedy kampania wraca pod nową domeną, wszyscy, którzy kiedyś zgłosili jej wariant, dostają jedno powiadomienie: „wróciła, tym razem jako …”. Kolekcjonerzy widzą, że ich zgłoszenie działa dalej.
7. **Raport dla platformy i regulatora.** Jeden przycisk generuje paczkę dowodów kampanii w formacie przydatnym dla zaufanych podmiotów sygnalizujących z art. 22 DSA (Digital Services Act). To pokazuje drogę do realnego wdrożenia.

---

## 6. Dwa pitche na jednym produkcie

### Pitch MSZ „Prawdowid” (scena główna: notatka i atak botów)
1. **Problem (20 s):** post z fałszywą informacją o zakazie gotówki ma 212 tys. wyświetleń. Fact-check jest gdzieś w sieci, ale nie tam, gdzie ludzie czytają.
2. **Pokaz (60 s):** ten sam post z naszą notatką: kontekst, 4 źródła, spektrum mediów, konsensus dwóch grup.
3. **Zwrot (40 s):** farma 312 kont próbuje zakopać notatkę. Dashboard na żywo: głosy odrzucone, status bez zmian.
4. **Edukacja (20 s):** notatka nazywa technikę manipulacji i uczy, jak ją rozpoznać.
5. **Skala (20 s):** pięć platform, otwarte API, serwer MCP dla redakcji.
6. **Zamknięcie:** *„AI pisze. Ludzie decydują. Źródła są obowiązkowe.”*

### Pitch NASK „Kolekcjoner fejków” (scena główna: kampania)
1. **Problem (20 s):** reklama z deepfake'iem znanego prezentera obiecuje 1 200 zł dziennie. Po zgłoszeniu znika i wraca jutro pod nową domeną.
2. **Pokaz (40 s):** na Facebooku wtyczka oznacza reklamę jako oszustwo, zanim ktoś kliknie, i zapisuje dowód.
3. **Szerszy obraz (60 s):** jedno zgłoszenie rozwija kampanię #K-118: 47 wariantów, 23 domeny, 9 dni. Oś czasu pokazuje rotację domen, a przerywana linia pokazuje domeny, które dopiero się pojawią.
4. **Ochrona (30 s):** tryb opiekuna zatrzymuje seniora przed stroną płatności. Eksport dowodów do CERT Polska.
5. **Zamknięcie:** *„Pojedynczy fejk znika. Kolekcja zostaje.”*

---

## 7. Scenariusz demo (4 minuty, oba konkursy)

| Czas | Ekran | Co mówi prowadzący |
|---|---|---|
| 0:00 | Feed X, post o gotówce z notatką | „To jest internet, jaki znamy, z jedną warstwą więcej.” |
| 0:30 | Najechanie na źródła i spektrum | „Każde zdanie ma źródło. Widać, z której strony sporu.” |
| 1:00 | Feed, reklama sponsorowana z celebrytą, ostrzeżenie | „Ta reklama to oszustwo. Wtyczka już zapisała dowód.” |
| 1:30 | Szybkie zgłoszenie (popover) | „Zgłoszenie zajmuje trzy kliknięcia, a link do źródła jest wymagany.” |
| 2:00 | Dashboard, kampania #K-118 | „Jedno zgłoszenie, cała kampania: 47 reklam, 23 domeny.” |
| 2:40 | Dashboard, atak na notatkę | „A teraz ktoś próbuje nas oszukać. 312 kont, zero wpływu.” |
| 3:20 | Slajd architektury | „FastAPI, DBOS, pgvector, MCP. Działa dziś, skaluje się jutro.” |
| 3:40 | Slajd zamykający | Hasło pod konkretny konkurs. |

Zasada: demo musi działać bez internetu. Dane kampanii i ataku odtwarzamy z nagranego scenariusza w DBOS, żeby nic nie zależało od Wi-Fi na sali.

---

## 8. Pytania jury i odpowiedzi

- **„Kto decyduje, co jest prawdą?”** Nikt sam. AI pisze szkic, ludzie z różnych stron muszą się zgodzić, źródła są publiczne. Pokazujemy, skąd przyszła zgoda.
- **„Co z fałszywymi alarmami?”** Ostrzeżenie o oszustwie wymaga co najmniej dwóch niezależnych sygnałów (np. domena z listy CERT i podobieństwo do znanej kampanii). Każde ostrzeżenie ma „Zgłoś pomyłkę” i trafia do ponownej oceny.
- **„A RODO i wizerunek?”** Nie przetwarzamy twarzy osób spoza rejestru opt-in. Dowody przechowujemy minimalnie i z datą usunięcia.
- **„Co jeśli platforma zablokuje wtyczkę?”** Wtyczka działa po stronie użytkownika i niczego nie publikuje na platformie. Rdzeń (graf kampanii, API, MCP) działa niezależnie od wtyczki.
- **„Dlaczego to się utrzyma po hackathonie?”** Otwarte API dla redakcji i CERT, model organizacji pozarządowej, droga do statusu zaufanego podmiotu sygnalizującego z DSA.
- **„Czym różnicie się od Community Notes?”** Działamy na pięciu platformach, łączymy treści w kampanie, obejmujemy oszustwa i reklamy, a źródła są obowiązkowe.

---

## 9. Czego nie mówimy

- Nie podajemy skuteczności („wykrywa 98% oszustw”), której nie zmierzyliśmy.
- Nie nazywamy prawdziwych osób oszustami. W demo używamy fikcyjnego prezentera i fikcyjnych domen.
- Nie twierdzimy, że współpracujemy z NASK, CERT Polska, MSZ ani z mediami, dopóki to nieprawda. Mówimy „gotowe do integracji z…”.
- Nie pokazujemy prawdziwych kont jako botów. Wszystkie nazwy kont w demo są wymyślone.

---

## 10. Nazwa: Meritum

Robocza nazwa i podtytuł: **Meritum — obywatelski radar dezinformacji oraz scamu.**

- **Meritum** to „sedno sprawy”: notatka i ostrzeżenie mówią, o co naprawdę chodzi, bez emocji i bez oceniania ludzi. Słowo zna każdy Polak, a brzmi poważnie bez urzędowości.
- **Obywatelski**: budują go użytkownicy, nie platforma ani rząd. To odpowiedź na pytanie „kto decyduje, co jest prawdą”.
- **Radar**: widzimy kampanię, zanim dotrze do ciebie, i pokazujemy ją na mapie. Słowo spina oba konkursy: dezinformację (MSZ) i scam (NASK).

Przed pitchem trzeba sprawdzić znak towarowy i wolne domeny (np. meritum.org.pl, meritum.app). Nazwa „Meritum” bywa używana przez inne firmy, więc w materiałach zawsze idzie z podtytułem.

## 11. Zakres na hackathon

**Budujemy naprawdę:** wtyczka na X (notatka, ostrzeżenie o oszustwie, zgłoszenie), API z modelem notatek i konsensusu, graf kampanii na pgvector dla przygotowanego zbioru reklam, dashboard z dwoma widokami (kampania, atak), sejf dowodów (zrzut + adres + czas), serwer MCP z dwoma narzędziami.

**Pokazujemy jako makietę:** pozostałe cztery platformy, tryb opiekuna, rejestr wizerunków, predykcję domen z logów certyfikatów, eksport do CERT.

**Pomijamy:** konta użytkowników z hasłami, panel moderacji, aplikację mobilną.
