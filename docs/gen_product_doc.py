"""Generates design-system/docs/product-doc.html (source for the Google Doc)."""

import re
from html import escape as e
from pathlib import Path

OUT = Path("/Users/cyprian/Documents/GitHub/HackNation2026/design-system/docs/product-doc.html")

FONT = "font-family:Archivo,Arial,sans-serif;"
INK, ACC, PALE, PALE_TXT, RED, BORDER = "#14191E", "#1D6A86", "#E1EDF2", "#13506A", "#C8213A", "#D9DEDD"
CELL = f"border:1px solid {BORDER};padding:3px 5px;vertical-align:top;{FONT}font-size:9pt;color:#000000;"
TH = f"border:1px solid {BORDER};padding:3px 5px;background-color:{ACC};color:#FFFFFF;font-weight:bold;{FONT}font-size:9pt;text-align:left;"
SUB = f"border:1px solid {BORDER};padding:3px 5px;background-color:{PALE};color:{PALE_TXT};font-weight:bold;{FONT}font-size:9pt;"
TABLE = "border-collapse:collapse;width:100%;"
P = f"{FONT}font-size:11pt;color:#000000;"


def h(level: int, text: str) -> str:
    size = {1: "24pt", 2: "16pt", 3: "12.5pt"}[level]
    return f'<h{level} style="{FONT}color:{INK};font-size:{size};font-weight:bold;">{e(text)}</h{level}>'


def p(html: str) -> str:
    return f'<p style="{P}">{html}</p>'


def risk(text: str) -> str:
    return f'<span style="color:{RED};font-weight:bold;">Ryzyko:</span> {e(text)}'


def table(head: list[str], rows: list[str], widths: list[int] | None = None) -> str:
    widths = widths or [0] * len(head)
    th = "".join(f'<th style="{TH}{f"width:{w}%;" if w else ""}">{e(c)}</th>' for c, w in zip(head, widths))
    return f'<table style="{TABLE}"><thead><tr>{th}</tr></thead><tbody>{"".join(rows)}</tbody></table>'


def row(*cells: str) -> str:
    return "<tr>" + "".join(f'<td style="{CELL}">{c}</td>' for c in cells) + "</tr>"


def sub_row(text: str, span: int) -> str:
    return f'<tr><td colspan="{span}" style="{SUB}">{e(text)}</td></tr>'


def code(text: str) -> str:
    # zero-width space before inner capitals (Google Docs drops <wbr>): long names break only at word joins
    return f'<span style="font-family:\'Azeret Mono\',\'Courier New\',monospace;font-size:9pt;">{re.sub(r"(?<=[a-z])(?=[A-Z])", "\u200b", e(text))}</span>'

# ---------------------------------------------------------------- 1. header
parts: list[str] = [
    h(1, "Meritum: obywatelski radar dezinformacji"),
    p('<span style="color:#4C5862;">Dokument produktowy · HackNation 2026 · konkurs MSZ „Prawdowid” · wersja robocza</span>'),
    h(2, "1. Wprowadzenie"),
    p(
        "Meritum pozwala obywatelowi sprawdzić doniesienie tak łatwo, jak wysłać wiadomość. Wkleja tekst albo link w "
        "formularzu na stronie albo klika „Sprawdź” pod postem we wtyczce do przeglądarki. System wyodrębnia twierdzenia, "
        "szuka ich w opisanym zbiorze źródeł (dokumenty urzędowe, dane publiczne, fact-checkerzy, świeże publikacje z "
        "zatwierdzonych serwisów) i dla każdego twierdzenia podaje jeden z pięciu werdyktów: potwierdzone, fałszywe, "
        "wprowadzające w błąd, brak wystarczających dowodów, nie podlega weryfikacji. Każde ustalenie prowadzi do "
        "dosłownego fragmentu źródła z tytułem, wydawcą, datą i linkiem. Siła odpowiedzi wynika z jawnych przesłanek. "
        "Gdy dowodów brakuje, system mówi to wprost, a sprawa może trafić do moderatora."
    ),
    table(
        ["Wymaganie z treści zadania", "Odpowiedź Meritum"],
        [
            row("Dwa kanały, ta sama logika", "Formularz WWW (podstawowy) i „Sprawdź” we wtyczce Chrome na jednym rdzeniu weryfikacji. Bot na Discordzie budujemy od początku jako zapasowy drugi kanał."),
            row("Każda teza prowadzi do dowodu", "Werdykt rozstrzygający wymaga cytatu, a cytat musi dosłownie występować w źródle."),
            row("Wstrzymanie się bez pozornej odpowiedzi", "Werdykt „brak wystarczających dowodów” z opisem, czego nie ustalono; sprawa moderatora."),
            row("Awaria to nie werdykt", "Osobne stany: problem techniczny, doprecyzuj pytanie, poza zakresem."),
            row("Odporność na prompt injection", "Treść źródeł trafia do modelu wyłącznie jako dane. Źródło z wykrytym poleceniem wypada z dowodów, a próba jest zapisywana."),
            row("Mierniki i odtwarzalność", "Skrypt ewaluacji na publicznym zestawie testowym, wyniki z danymi w repozytorium."),
        ],
        [35, 65],
    ),
    p(
        "Projekt nie ma partnerstw z MSZ ani z organizacjami fact-checkingowymi. Liczby pokazujemy tylko zmierzone "
        "naszym skryptem ewaluacji. Otwarte pytanie do mentorów MSZ: czy wtyczka przeglądarki jest „rozwiązaniem "
        "równoważnym” drugiemu kanałowi."
    ),
]

# ---------------------------------------------------------------- 2. stories
MVP, IF, PO = "MVP hackathon", "Jeśli starczy czasu", "Po hackathonie"

# domain -> list of (actor, [(id, actor_em, want, so_that, [criteria], priority, contract)])
STORIES: list[tuple[str, str, list[tuple[str, list[tuple]]]]] = [
    ("2.1", "Sprawdzanie przez formularz WWW", [
        ("Obywatel", [
            ("US-SPR-01", "Jako obywatel", "wkleić tekst albo link w formularzu na telefonie, bez konta i bez instalacji",
             "sprawdzić doniesienie tak łatwo, jak wysłać wiadomość",
             ["Pole przyjmuje tekst do 4000 znaków albo pełny adres https://.", "Puste albo zbyt krótkie wejście pokazuje komunikat po polsku i nie znika."],
             MVP, "CheckRequest"),
            ("US-SPR-02", "Jako obywatel", "widzieć postęp sprawdzania krok po kroku",
             "wiedzieć, że coś się dzieje i co dokładnie",
             ["Osiem kroków: przyjęcie pytania, wyodrębnienie twierdzeń, baza źródeł, świeże publikacje, porównanie źródeł, sprawdzenie cytatów, odpowiedź, zapis przebiegu.", "Krok pominięty jest oznaczony słowem."],
             MVP, "AnalysisStatus, AnalysisStep"),
            ("US-SPR-03", "Jako obywatel", "żeby system sam znalazł w moim tekście twierdzenia do sprawdzenia i oddzielił je od opinii",
             "nie musieć formułować pytania jak specjalista",
             ["Najwyżej 5 twierdzeń na zapytanie; pozostałe wymienione w ograniczeniach.", "Opinie i przewidywania dostają werdykt „nie podlega weryfikacji”."],
             MVP, "ClaimResult.claim"),
            ("US-SPR-04", "Jako obywatel", "dostać osobny werdykt dla każdego twierdzenia, prostym językiem",
             "wiedzieć, które części tekstu są prawdziwe",
             ["Jeden z pięciu werdyktów, zawsze słowem i kolorem.", "Mediana czasu odpowiedzi do 30 s dla tekstu i linku.", "Limit czasu na każdy krok, wyszukiwanie w sieci najwyżej 10 s, najwyżej 3 twierdzenia sprawdzane równolegle.", "Przekroczony limit wyszukiwania daje wynik z samego korpusu z adnotacją w ograniczeniach, a nie problem techniczny."],
             MVP, "ClaimResult.verdict"),
            ("US-SPR-05", "Jako obywatel", "przeczytać, czego nie udało się ustalić, gdy brakuje dowodów",
             "nie dostać pozornej odpowiedzi",
             ["„Brak wystarczających dowodów” zawsze ma opis braków (walidacja kontraktu).", "Nie pokazujemy wtedy siły ani cytatów udających rozstrzygnięcie."],
             MVP, "ClaimResult.unresolved"),
            ("US-SPR-06", "Jako obywatel", "dostać komunikat wyraźnie inny niż werdykt, gdy coś się nie udało, pytanie jest niejasne albo poza zakresem",
             "nie pomylić awarii z oceną treści",
             ["Stany needs_clarification, out_of_scope, technical_failure nie mają twierdzeń, mają komunikat.", "Wygląd nie przypomina plakietki werdyktu."],
             MVP, "CheckResult.status"),
            ("US-SPR-07", "Jako obywatel", "wkleić link do artykułu albo posta",
             "nie przepisywać treści ręcznie",
             ["Serwer pobiera tylko publiczne strony http(s); adresy wewnętrzne i lokalne są blokowane (ochrona przed SSRF).", "Nie omijamy logowania ani paywalli: strona za logowaniem (np. post na Facebooku) daje stan „doprecyzuj” z prośbą o wklejenie tekstu."],
             MVP, "CheckRequest.url"),
            ("US-SPR-08", "Jako obywatel", "wysłać zrzut ekranu z tekstem i datą",
             "sprawdzić to, co dostałem jako obrazek",
             ["OCR odczytuje tekst i datę.", "Odpowiedź ujawnia ograniczenia analizy obrazu, w tym brak wyszukiwania odwrotnego obrazu.", "README podaje koszt, zakres i retencję usługi OCR."],
             IF, "brak (pole obrazu dojdzie z funkcją)"),
        ]),
        ("Osoba o niskich kompetencjach cyfrowych", [
            ("US-DST-01", "Jako osoba bez wiedzy technicznej", "korzystać z formularza na telefonie i rozumieć odpowiedź bez słownika",
             "sprawdzić informację bez pomocy innych",
             ["WCAG 2.2 AA: kontrast, obsługa klawiaturą, czytnik ekranu, działanie od 320 px szerokości.", "Odpowiedzi sprawdzane narzędziem do oceny zrozumiałości tekstu (np. Jasnopis) na próbce z ewaluacji.", "Werdykt nigdy nie jest oznaczony samym kolorem."],
             MVP, "ResultCard"),
        ]),
    ]),
    ("2.2", "Drugi kanał: wtyczka do przeglądarki", [
        ("Czytelnik mediów społecznościowych", [
            ("US-WTY-01", "Jako czytelnik", "kliknąć „Sprawdź” pod postem na X, Facebooku, Instagramie, Reddicie albo TikToku",
             "sprawdzić treść tam, gdzie ją widzę",
             ["Wtyczka wysyła tekst posta i jego adres do tego samego API co formularz.", "Wynik pokazuje się pod postem, w stylu platformy."],
             MVP, "CheckRequest(channel=extension)"),
            ("US-WTY-02", "Jako czytelnik", "wkleić tekst albo link w okienku wtyczki",
             "sprawdzić treść z dowolnej strony",
             ["Okienko ma to samo pole i te same komunikaty co formularz WWW."],
             MVP, "CheckRequest"),
            ("US-WTY-03", "Jako czytelnik", "dostać we wtyczce ten sam wynik co na stronie",
             "ufać, że kanał nie zmienia odpowiedzi",
             ["Wejście jest normalizowane przed sprawdzeniem (spacje, cudzysłowy, adres posta odcięty od tekstu).", "Wynik zapisany pod kluczem (znormalizowane wejście, wersja korpusu) i zwracany każdemu kanałowi.", "Strony dopisane z wyszukiwania podnoszą wersję korpusu dopiero po zakończeniu sprawdzenia.", "Test międzykanałowy w skrypcie ewaluacji: 100% zgodności."],
             MVP, "CheckResult.corpus_version"),
            ("US-WTY-04", "Jako czytelnik", "żeby wtyczka nie wysyłała niczego bez mojego kliknięcia",
             "zachować prywatność podczas przeglądania",
             ["Brak automatycznego skanowania feedu.", "Informacja o tym w okienku wtyczki."],
             MVP, "brak"),
            ("US-WTY-05", "Jako czytelnik", "widzieć widżet w stylu platformy, ale z tym samym znakiem, werdyktem i źródłami",
             "widżet pasował do strony i był rozpoznawalny",
             ["Skórka: krój, promień, tło, przyciski, linki.", "Stałe: znak Meritum, słowo i kolor werdyktu, blok źródeł."],
             MVP, "ResultCard (skórki)"),
        ]),
        ("Użytkownik komunikatora", [
            ("US-WTY-06", "Jako użytkownik Discorda", "wysłać botowi tekst albo link",
             "sprawdzić treść bez wychodzenia z komunikatora",
             ["Bot odpowiada automatycznie, bez udziału zespołu, tym samym rdzeniem co formularz.", "Budujemy go od początku: jeśli mentorzy nie uznają wtyczki za kanał, warunek dwóch kanałów i tak jest spełniony."],
             MVP, "CheckRequest(channel=discord)"),
        ]),
    ]),
    ("2.3", "Źródła, dowody i werdykt", [
        ("Obywatel", [
            ("US-ZRD-01", "Jako obywatel", "zobaczyć przy każdym ustaleniu tytuł, wydawcę, datę, link i wykorzystany fragment",
             "samodzielnie sprawdzić, skąd to wiadomo",
             ["Fragment jest dosłowny: kod sprawdza, że występuje w tekście źródła. Cytat, którego nie znaleziono, nie trafia do odpowiedzi.", "Tytuł, wydawca i data pochodzą z bazy po identyfikatorze źródła, nigdy z odpowiedzi modelu.", "Stanowisko cytatu (wspiera, obala, kontekst) ocenia osobne wywołanie, które widzi tylko parę: twierdzenie i fragment.", "Ewaluacja obejmuje ręczną ocenę losowej próby cytatów (czy fragment naprawdę wspiera tezę)."],
             MVP, "Source, Citation"),
            ("US-ZRD-02", "Jako obywatel", "odróżnić cytaty ze źródeł od wyjaśnienia przygotowanego przez AI",
             "wiedzieć, co jest dowodem, a co interpretacją",
             ["Wyjaśnienie ma osobny podpis i informację o użyciu AI.", "Cytaty są w osobnym bloku."],
             MVP, "ClaimResult.explanation"),
            ("US-ZRD-03", "Jako obywatel", "zobaczyć, jak mocna jest podstawa odpowiedzi i z czego to wynika",
             "ocenić, ile mogę zaufać werdyktowi",
             ["Przesłanki: niezależne źródła, źródła urzędowe, wiek najnowszego źródła, zgodność.", "Siła wynika z jednej reguły w kodzie i nie może się od niej różnić.", "Najnowsze źródło starsze niż 365 dni obniża siłę najwyżej do „umiarkowana”."],
             MVP, "EvidenceStrength, Premises"),
            ("US-ZRD-04", "Jako obywatel", "zobaczyć rozbieżność, gdy wiarygodne źródła podają różne dane",
             "nie dostać arbitralnej pewności",
             ["Sprzeczne źródła dają tylko „brak wystarczających dowodów” albo „wprowadzające w błąd”, nigdy „potwierdzone” ani „fałszywe”, i nigdy siłę „mocna”.", "Oba stanowiska z cytatami."],
             MVP, "Premises.agreement"),
            ("US-ZRD-05", "Jako obywatel", "dostać ostrzeżenie, gdy najnowsze źródło jest stare",
             "wiedzieć, że informacja mogła się zmienić",
             ["Źródło starsze niż 365 dni oznacza twierdzenie jako materiał archiwalny (walidacja kontraktu).", "Dla twierdzeń o bieżących wydarzeniach próg jest krótszy i ustawia go kurator."],
             MVP, "ClaimResult.archival"),
            ("US-ZRD-06", "Jako obywatel", "zobaczyć nazwę techniki manipulacji i jedno zdanie „jak rozpoznać?”",
             "następnym razem rozpoznać ją sam",
             ["Techniki: m.in. wyrwanie z kontekstu, nieaktualna informacja, fałszywy autorytet, wybiórcze dane.", "Treść podpowiedzi z copy/pl.json."],
             MVP, "TechniqueCode"),
            ("US-ZRD-07", "Jako obywatel", "dostać neutralną informację, gdy treść pochodzi od podmiotu objętego sankcjami UE",
             "znać kontekst źródła bez przesądzania o treści",
             ["Ostrzeżenie jest osobne od werdyktu i nie wpływa na niego.", "Tylko gdy informacja jest aktualna i sprawdzalna."],
             IF, "SourceStatusWarning"),
            ("US-ZRD-08", "Jako obywatel", "zobaczyć, że treść jest podobna do znanego incydentu dezinformacji",
             "poznać kontekst sprawy",
             ["Dopasowanie do bazy incydentów od organizatora, pokazane jako kontekst (scenariusz I).", "Sama domena z bazy incydentów nie daje werdyktu: test sprawdza, że werdykt jest identyczny z dopasowaniem i bez niego."],
             MVP, "IncidentMatch"),
        ]),
    ]),
    ("2.4", "Korpus i wyszukiwanie", [
        ("Kurator źródeł", [
            ("US-KOR-01", "Jako kurator źródeł", "prowadzić jawny katalog domen z powodem kwalifikacji, licencją, trybem odświeżania i powodem wykluczenia",
             "lista źródeł była dostępna do audytu",
             ["Wykluczenie bez powodu nie przechodzi walidacji.", "Katalog eksportowany razem z repozytorium."],
             MVP, "CatalogEntry"),
            ("US-KOR-02", "Jako kurator źródeł", "mieć korpus z co najmniej 100 dokumentów z co najmniej 10 domen i dwóch typów źródeł",
             "odpowiedzi opierały się na źródłach urzędowych i wtórnych",
             ["Źródła pierwotne lub urzędowe oraz wtórne.", "Każdy dokument ma datę publikacji (jeśli znana) i datę pobrania."],
             MVP, "Source"),
            ("US-KOR-03", "Jako kurator źródeł", "żeby nowe publikacje z katalogu same trafiały do korpusu",
             "system znał bieżące wydarzenia",
             ["Workflow DBOS co 15–30 min pobiera RSS i mapy stron zatwierdzonych serwisów.", "Błąd pobrania jest zapisany, nie blokuje sprawdzeń."],
             MVP, "Source.via = rss"),
            ("US-KOR-04", "Jako kurator źródeł", "żeby wyszukiwanie na żywo szukało tylko w domenach z katalogu",
             "nie wyjść poza jasno opisany zbiór źródeł",
             ["Wyszukiwanie uruchamia się tylko przy zbyt małej liczbie dowodów w korpusie.", "Pobrana strona zostaje w korpusie, więc kolejne pytania z każdego kanału korzystają z niej bez ponownego wyszukiwania."],
             MVP, "Source.via = web_search"),
            ("US-KOR-05", "Jako kurator źródeł", "żeby każdy zapisany dokument miał podstawę prawną, okres przechowywania i procedurę usunięcia",
             "korpus był zgodny z prawem autorskim i zasadami retencji",
             ["Podstawa: licencja z katalogu, dokument urzędowy (art. 4 prawa autorskiego) albo wyjątek eksploracji tekstów i danych.", "Pełny tekst tylko do wyszukiwania, dostęp wyłącznie dla systemu; użytkownik widzi krótki fragment i link.", "Usunięcie dokumentu na wniosek wydawcy w ciągu 7 dni."],
             MVP, "CatalogEntry.license"),
        ]),
        ("Obywatel", [
            ("US-KOR-06", "Jako obywatel", "dostać odpowiedź po polsku, nawet gdy źródła są w innym języku",
             "korzystać z zagranicznych źródeł",
             ["Wyszukiwanie po polsku i angielsku, cytat w oryginale, wyjaśnienie po polsku."],
             IF, "Source.language"),
        ]),
    ]),
    ("2.5", "Bezpieczeństwo i prywatność", [
        ("Administrator", [
            ("US-BEZ-01", "Jako administrator", "żeby instrukcje znalezione w sprawdzanej treści i źródłach były ignorowane i zapisywane",
             "nikt nie mógł zmienić zasad działania systemu",
             ["Źródło z wykrytym poleceniem wypada z dowodów, a fakt ten trafia do ograniczeń odpowiedzi.", "Ocena stanowiska cytatu nie widzi instrukcji użytkownika ani innych źródeł.", "Próba odparta = werdykt i cytaty identyczne jak dla tego samego materiału bez wstrzykniętego polecenia; odporność ≥ 90% w ewaluacji.", "Każda próba zapisana jako zdarzenie."],
             MVP, "InjectionEvent"),
            ("US-BEZ-02", "Jako administrator", "walidować wejście i limitować liczbę zapytań",
             "ograniczyć nadużycia i koszty",
             ["Limit na adres IP i kanał.", "Przekroczenie limitu daje komunikat, nie werdykt."],
             MVP, "CheckRequest"),
            ("US-BEZ-03", "Jako administrator", "żeby brak klucza, limit albo awaria dostawcy kończyły się stanem „Problem techniczny”",
             "nigdy nie pokazać pozornego wyniku",
             ["Scenariusz J w skrypcie ewaluacji."],
             MVP, "CheckResult.status"),
        ]),
        ("Obywatel", [
            ("US-BEZ-04", "Jako obywatel", "żeby oczywiste dane osobowe w moim tekście zostały ukryte przed analizą",
             "nie zostawić ich w systemie",
             ["Maskowanie telefonów, e-maili i numerów PESEL w API, zanim wystartuje workflow DBOS (DBOS zapisuje wejścia workflowów w bazie).", "Zapis przebiegu i dostawcy modelu dostają tylko wersję zamaskowaną."],
             MVP, "CheckRecord.question_masked"),
            ("US-BEZ-05", "Jako obywatel", "usunąć swoje sprawdzenia i wiedzieć, jak długo są przechowywane",
             "mieć kontrolę nad swoimi danymi",
             ["Retencja 30 dni, potem automatyczne usunięcie (workflow DBOS).", "Przycisk „Usuń moje sprawdzenia” usuwa wszystkie zapisy z losowym identyfikatorem sesji z przeglądarki, łącznie z danymi workflowów DBOS i powiązaniami ze sprawami moderatora."],
             MVP, "CheckRecord.session_id"),
        ]),
    ]),
    ("2.6", "Pętla informacji i moderacja", [
        ("Moderator i analityk", [
            ("US-MOD-01", "Jako moderator", "dostać sprawę, gdy brakuje dowodów, sprawa jest wysokiego ryzyka albo pytanie powtarza się bez odpowiedzi",
             "zająć się tym, czego system nie rozstrzyga",
             ["Sprawa powstaje automatycznie, gdy brak dowodów dotyczy tematu wysokiego ryzyka (lista administratora, np. zdrowie, bezpieczeństwo publiczne, wybory) albo gdy podobne pytanie bez odpowiedzi pojawia się drugi raz.", "Moderatora wskazuje administrator; powiadomienie trafia do panelu i na skonfigurowany e-mail albo webhook.", "Sprawa ma powód, streszczenie i listę sprawdzeń."],
             MVP, "ModeratorCase"),
            ("US-MOD-02", "Jako moderator", "widzieć podobne pytania w jednej sprawie",
             "nie dostawać tej samej sprawy wiele razy",
             ["Podobieństwo liczone na embeddingach twierdzeń; próg (start 0,85) strojony na zestawie testowym.", "Podobne pytanie aktualizuje istniejącą sprawę zamiast tworzyć nową (scenariusz H: 100% poprawnych spraw).", "Liczba podobnych pytań przy sprawie."],
             MVP, "ModeratorCase.check_ids"),
        ]),
        ("Obywatel", [
            ("US-MOD-03", "Jako obywatel", "wiedzieć, czy moja sprawa została przekazana, czy tylko zalecono przekazanie",
             "nie dostać fałszywej obietnicy",
             ["Pojedynczy brak dowodów w zwykłym temacie daje „Zalecamy przekazanie” bez numeru sprawy i przycisk „Przekaż moderatorom”.", "Kliknięcie albo automatyczna reguła z US-MOD-01 tworzy sprawę; dopiero wtedy pojawia się numer.", "Walidacja kontraktu pilnuje tej różnicy."],
             MVP, "Escalation"),
        ]),
        ("Moderator", [
            ("US-MOD-04", "Jako moderator", "zatwierdzić odpowiedź przed publikacją",
             "odpowiedzi publiczne sprawdzał człowiek, jak w pilotażu z §9 zadania",
             ["Konsensus osób o różnych poglądach jako opcja przy publikacji."],
             PO, "brak"),
        ]),
    ]),
    ("2.7", "Obserwowalność, ewaluacja i eksport", [
        ("Analityk i administrator", [
            ("US-OBS-01", "Jako analityk", "mieć zapis przebiegu każdego sprawdzenia",
             "móc odtworzyć i obronić każdą odpowiedź",
             ["Pytanie, czas, kanał, źródła, werdykty, wersja korpusu, eskalacja."],
             MVP, "CheckRecord"),
            ("US-OBS-02", "Jako administrator", "widzieć czas odpowiedzi, użyte modele, region, koszt, błędy wyszukiwania i wstrzymania",
             "pilnować jakości i kosztów",
             ["Koszt liczony z tokenów i wywołań wyszukiwarki.", "Szacunek kosztu 1 000 zapytań w README."],
             MVP, "CheckRecord, ModelUsage"),
            ("US-OBS-03", "Jako analityk", "wyeksportować sprawdzenia i sprawy do JSON i CSV, z kodami technik w DISARM",
             "korzystać z danych w narzędziach analitycznych",
             ["Identyfikator DISARM tam, gdzie istnieje odpowiednik."],
             IF, "CheckRecord, ModeratorCase"),
        ]),
        ("Zespół i jury", [
            ("US-OBS-04", "Jako członek zespołu", "uruchomić jednym poleceniem ewaluację na publicznym zestawie testowym",
             "podać wyniki z danymi do odtworzenia",
             ["Scenariusze A–J.", "Mierniki: macro-F1, pokrycie i poprawność cytowań, wstrzymanie, odporność, mediana czasu, koszt 100 testów, spójność kanałów, pętla informacji."],
             MVP, "CheckResult, CheckRecord"),
            ("US-OBS-05", "Jako członek jury", "uruchomić tę samą ewaluację na własnym pliku z przypadkami",
             "sprawdzić wyniki na zestawie referencyjnym",
             ["Skrypt przyjmuje plik JSON albo CSV z co najmniej 30 przypadkami.", "README zawiera jawną listę przypadków, których system nie obsługuje."],
             MVP, "CheckRequest, CheckResult"),
        ]),
    ]),
    ("2.8", "Wdrożenie i integracje", [
        ("Jury i administrator", [
            ("US-WDR-01", "Jako członek jury", "uruchomić system z instrukcji w README albo otworzyć publiczne demo",
             "przetestować go bez pomocy zespołu",
             ["`docker compose up` z przykładowym plikiem .env bez sekretów w repozytorium.", "Publiczne demo w GCP europe-central2.", "README opisuje instalację wtyczki (spakowany .zip i „Załaduj rozpakowane”) w mniej niż 2 minuty; demo na makietach działa też bez instalacji."],
             MVP, "infra"),
            ("US-WDR-02", "Jako administrator", "wymienić model albo dostawcę wyszukiwania konfiguracją",
             "nie przebudowywać systemu",
             ["LLM i wyszukiwarka za portami; adaptery wybierane zmienną środowiskową.", "pytestarch pilnuje, że domena nie importuje adapterów."],
             MVP, "porty"),
            ("US-WDR-03", "Jako administrator", "mieć opis kluczy, limitów, kosztów, regionu przetwarzania i zachowania przy awarii",
             "spełnić wymagania formalne i ocenić ryzyko dostawców",
             ["Sekcja w README i na slajdzie architektury.", "Koszt 1 000 zapytań, koszt utrzymania kanałów i zachowanie przy zwiększonym ruchu (kolejka DBOS, limity)."],
             MVP, "brak"),
            ("US-WDR-04", "Jako członek jury", "dostać komplet materiałów wymaganych w §4 zadania",
             "ocenić projekt bez dopytywania zespołu",
             ["Nazwa zespołu, tytuł i opis do 4 000 znaków; PDF do 12 slajdów; film do 3 minut; link do repozytorium z instrukcją.", "Opis architektury, przepływu danych, modeli, dostawców i ograniczeń; opis źródeł z licencjami.", "Wyniki testów z danymi do odtworzenia i lista ryzyk z sekcji 5 tego dokumentu."],
             MVP, "brak"),
            ("US-WDR-05", "Jako administrator", "generować JSON Schema i typy TypeScript z kontraktów w CI",
             "API, formularz, wtyczka i panel się nie rozjechały",
             ["Różnica w wygenerowanych plikach zatrzymuje build."],
             MVP, "meritum_contracts.py"),
        ]),
        ("Redakcja i analityk (MCP)", [
            ("US-WDR-06", "Jako dziennikarz", "sprawdzić twierdzenie z poziomu asystenta AI przez MCP",
             "korzystać z tego samego rdzenia bez strony i wtyczki",
             ["Narzędzie MCP zwraca CheckResult."],
             IF, "FastMCP, CheckResult"),
        ]),
        ("Administrator", [
            ("US-WDR-07", "Jako administrator", "uruchomić otwarty model na własnym serwerze z GPU",
             "ograniczyć zależność od dostawców spoza EOG",
             ["Ten sam port LLM, inny adapter.", "Porównanie jakości i kosztu z modelem komercyjnym w skrypcie ewaluacji."],
             PO, "porty"),
        ]),
    ]),
]

story_count = 0
parts += [
    h(2, "2. Historie użytkowników"),
    p(
        "Historie są pogrupowane według domen, a w każdej domenie według aktorów. Priorytet <strong>MVP hackathon</strong> "
        "to to, co budujemy na hackathon: wymagania podstawowe i techniczne z treści zadania MSZ, scenariusze testowe "
        "jury oraz wybrane funkcje premiowane (pętla informacji, katalog źródeł). <strong>Jeśli starczy czasu</strong> "
        "to pozostałe funkcje premiowane. <strong>Po hackathonie</strong> to rozwój. Kolumna „Kontrakt / komponent” "
        "wskazuje model z contracts/meritum_contracts.py albo komponent."
    ),
]
for num, domain, actors in STORIES:
    rows: list[str] = []
    for actor, stories in actors:
        rows.append(sub_row(actor, 5))
        for sid, who, want, so, crit, prio, contract in stories:
            story_count += 1
            text = f"<em>{e(who)}</em> chcę{',' if want.startswith('żeby') else ''} {e(want)}, aby {e(so)}."
            ac = "<br>".join(f"• {e(c)}" for c in crit)
            rows.append(row(f"<strong>{sid}</strong>", text, ac, e(prio), code(contract) if contract != "brak" else "brak"))
    parts += [h(3, f"{num}. {domain}"), table(["ID", "Historia", "Kryteria akceptacji", "Priorytet", "Kontrakt / komponent"], rows, [15, 24, 26, 13, 22])]

# ---------------------------------------------------------------- 3. features
_FEATURES = [
    ("Formularz WWW", "Responsywna strona: pole na tekst lub link, postęp, karta wyniku, usuwanie sprawdzeń; WCAG 2.2 AA.", "SPR-01, SPR-02, DST-01, BEZ-05", "MVP: kanał WWW", "Budujemy", "M"),
    ("„Sprawdź” we wtyczce", "Przycisk pod postem na pięciu platformach i pole w popupie; wysyłka tylko po kliknięciu, przez background.js do tego samego API.", "WTY-01, WTY-02, WTY-04, WTY-05", "MVP: drugi kanał", "Budujemy", "M"),
    ("Bot na Discordzie", "Zapasowy drugi kanał na tym samym API, budowany od początku.", "WTY-06", "Warunek brzegowy: dwa kanały", "Budujemy", "S"),
    ("Spójność kanałów", "Normalizacja wejścia i pamięć wyników pod kluczem (wejście, wersja korpusu).", "WTY-03", "§5 Kanały i dostęp", "Budujemy", "S"),
    ("Pobieranie linku", "Pobranie publicznej strony z ochroną przed SSRF; strony za logowaniem prowadzą do prośby o wklejenie tekstu.", "SPR-07", "MVP: wejście URL", "Budujemy", "S"),
    ("Wyodrębnianie twierdzeń", "Pydantic AI ze strukturalnym wyjściem: do 5 twierdzeń, fakty oddzielone od opinii.", "SPR-03, SPR-04", "MVP", "Budujemy", "S"),
    ("Korpus i katalog źródeł", "Co najmniej 100 dokumentów, 10 domen, 2 typy; katalog z licencją, powodem kwalifikacji i wykluczenia; retencja i usuwanie na wniosek wydawcy.", "KOR-01, KOR-02, KOR-05", "§5 Źródła, §5 Zakazy", "Budujemy", "M"),
    ("Wyszukiwanie hybrydowe", "pgvector i wyszukiwanie pełnotekstowe ze słownikiem polskim w PostgreSQL, preferowanie świeżych dokumentów.", "KOR-02, ZRD-05", "MVP", "Budujemy", "M"),
    ("Świeże publikacje", "Cykliczne RSS (DBOS) i wyszukiwanie Firecrawl ograniczone do domen z katalogu, z limitem 10 s; wyniki trafiają do korpusu.", "KOR-03, KOR-04", "§5 Aktualność", "Budujemy", "M"),
    ("Werdykt z przesłankami", "Ocena stanowiska cytatów, mapowanie na pięć werdyktów, siła liczona regułą, rozbieżności, materiał archiwalny.", "SPR-04, SPR-05, ZRD-03, ZRD-04, ZRD-05", "MVP, §5 Fakty", "Budujemy", "L"),
    ("Weryfikacja cytatów", "Fragment musi występować dosłownie w tekście źródła; metadane z bazy; stanowisko oceniane osobno.", "ZRD-01", "Mierniki: pokrycie i poprawność cytowań", "Budujemy", "S"),
    ("Karta wyniku", "Werdykt słowem, twierdzenie, wyjaśnienie oznaczone jako AI, źródła z fragmentem, siła, braki, ograniczenia, technika.", "ZRD-01, ZRD-02, ZRD-06, SPR-06", "MVP, §5 Dostępność", "Budujemy", "M"),
    ("Dopasowanie do incydentów", "Podobieństwo do bazy incydentów od organizatora, pokazane jako kontekst; test, że nie zmienia werdyktu.", "ZRD-08", "Scenariusz I", "Budujemy", "S"),
    ("Stany niebędące werdyktem", "Problem techniczny, doprecyzuj pytanie, poza zakresem; brak klucza i limity jako problem techniczny.", "SPR-06, BEZ-03", "§5 Zależności", "Budujemy", "S"),
    ("Ochrona przed prompt injection", "Separacja instrukcji od danych, wykluczanie źródeł z poleceniami, ocena stanowiska bez instrukcji użytkownika, zapis prób.", "BEZ-01", "§5 Bezpieczeństwo", "Budujemy", "M"),
    ("Prywatność i limity", "Maskowanie danych osobowych przed workflowem, retencja 30 dni, usuwanie sesji, limit zapytań, walidacja wejścia.", "BEZ-02, BEZ-04, BEZ-05", "§5 Prywatność", "Budujemy", "S"),
    ("Zapis przebiegu i obserwowalność", "CheckRecord z czasem, modelami, regionem, kosztem, błędami wyszukiwania i zdarzeniami.", "OBS-01, OBS-02", "§5 Obserwowalność", "Budujemy", "S"),
    ("Sprawy moderatora", "Automatyczne sprawy dla tematów wysokiego ryzyka i powtórzeń, deduplikacja, przycisk „Przekaż moderatorom”, powiadomienia.", "MOD-01, MOD-02, MOD-03", "Premiowane: pętla, scenariusz H", "Budujemy", "M"),
    ("Skrypt ewaluacji", "Publiczny zestaw testowy A–J, uruchomienie na pliku jury, raport wszystkich mierników obowiązkowych.", "OBS-04, OBS-05, WTY-03", "§6 Mierniki", "Budujemy", "M"),
    ("Wdrożenie i materiały dla jury", "docker compose, publiczne demo w GCP europe-central2, instrukcja wtyczki, README z kosztami i dostawcami, materiały z §4.", "WDR-01, WDR-02, WDR-03, WDR-05, WDR-04", "§4 Formalne", "Budujemy", "M"),
    ("OCR zrzutu ekranu", "Odczyt tekstu i daty z obrazu; README podaje koszt, zakres i retencję usługi; bez wyszukiwania odwrotnego obrazu.", "SPR-08", "Premiowane: multimodalność", "Jeśli czas", "M"),
    ("Ostrzeżenie o statusie źródła", "Neutralna informacja o sankcjach UE lub mediach państwowych, osobna od werdyktu.", "ZRD-07", "§5 Zakazy", "Jeśli czas", "S"),
    ("Wielojęzyczne wyszukiwanie", "Zapytania po polsku i angielsku, odpowiedź po polsku.", "KOR-06", "Premiowane", "Jeśli czas", "S"),
    ("Eksport i DISARM", "JSON i CSV sprawdzeń i spraw, kody technik zmapowane na DISARM.", "OBS-03", "Premiowane: integracje", "Jeśli czas", "S"),
    ("Serwer MCP", "FastMCP jako kolejny adapter wejściowy zwracający CheckResult.", "WDR-06", "Premiowane: architektura", "Jeśli czas", "S"),
    ("Zatwierdzanie odpowiedzi przez ludzi", "Publikacja odpowiedzi moderatora po akceptacji, opcjonalnie z konsensusem osób o różnych poglądach.", "MOD-04", "§9 Pilotaż", "Po hackathonie", "L"),
    ("Model na własnym serwerze", "Otwarty model na serwerze z GPU za tym samym portem.", "WDR-07", "Premiowane: EOG", "Po hackathonie", "M"),
]
FEATURES = [(f"F-{i:02d}", *f) for i, f in enumerate(_FEATURES, 1)]
parts += [
    h(2, "3. Proponowane funkcje"),
    p(
        "Funkcje wynikają z historii z sekcji 2. <strong>Budujemy</strong> na hackathon, <strong>Jeśli czas</strong> to "
        "funkcje premiowane po spełnieniu wymagań podstawowych, <strong>Po hackathonie</strong> to rozwój. Nakład: "
        "<strong>S</strong> do kilku godzin, <strong>M</strong> około pół dnia, <strong>L</strong> więcej."
    ),
    table(
        ["ID", "Funkcja", "Opis", "Historie", "Wymaganie MSZ", "Zakres", "Nakład"],
        [
            row(f"<strong>{fid}</strong>", f"<strong>{e(name)}</strong>", e(desc), e(", ".join("US-" + s for s in stories.split(", "))), e(req), e(scope), e(eff))
            for fid, name, desc, stories, req, scope, eff in FEATURES
        ],
        [8, 15, 27, 17, 12, 12, 9],
    ),
]

# ---------------------------------------------------------------- 4. ADRs
A, PR = "Przyjęta", "Proponowana"
ADRS = [
    ("ADR-01", "Pionowe wycinki domenowe z architekturą heksagonalną", A,
     "MSZ wymaga oddzielenia obsługi kanałów od logiki weryfikacji i wymiany modelu lub dostawcy bez przebudowy. Zespół pracuje równolegle nad kilkoma domenami.",
     "Wycinki: sprawdzanie, korpus, moderacja, zapis przebiegu. Każdy powtarza podfoldery models/, dtos/, ports/, adapters/. Kanały (WWW, wtyczka, MCP, Discord) to adaptery wejściowe; LLM, wyszukiwarka i baza to adaptery wyjściowe. Granice pilnuje pytestarch.",
     "Nowy kanał albo model to nowy adapter. Domenę testujemy bez sieci. " + risk("więcej plików na start; testy architektury łapią skróty w CI."),
     "Klasyczne warstwy; logika w handlerach kanałów."),
    ("ADR-02", "Kontrakty Pydantic jako jedno źródło prawdy i miejsce reguł z treści zadania", A,
     "API, formularz, wtyczka i panel renderują te same dane. Reguły MSZ (cytat przy werdykcie, wstrzymanie się, awaria to nie werdykt) nie mogą zależeć od promptu.",
     "contracts/meritum_contracts.py definiuje CheckRequest, CheckResult, ClaimResult, Citation, EvidenceStrength, Escalation, CheckRecord, ModeratorCase i CatalogEntry. Walidatory wymuszają reguły; generate.sh tworzy JSON Schema i typy TS i sprawdza, że złe dane są odrzucane.",
     "Reguły są sprawdzalne testem. " + risk("zmiana kontraktu wymaga regeneracji typów; CI musi to wymuszać."),
     "Reguły tylko w promptach; ręcznie pisane typy TS."),
    ("ADR-03", "DBOS dla workflowu sprawdzania i cyklicznego pobierania źródeł", A,
     "Sprawdzenie ma kilka kroków z wywołaniami zewnętrznymi, które mogą zawieść. Korpus musi się odświeżać sam.",
     "Każde sprawdzenie to workflow DBOS z krokami AnalysisStep; kanały odczytują AnalysisStatus. Pobieranie RSS i usuwanie danych po retencji to zaplanowane workflowy DBOS.",
     "Restart nie gubi sprawdzeń; kroki są ponawiane, stan w PostgreSQL. " + risk("kroki muszą być idempotentne."),
     "Celery z Redisem; Cloud Tasks; cron poza aplikacją."),
    ("ADR-04", "PostgreSQL z pgvector i wyszukiwaniem pełnotekstowym", A,
     "Wyszukiwanie dowodów wymaga podobieństwa znaczeniowego i dokładnych słów (nazwy, liczby, daty).",
     "Jedna baza: dokumenty, fragmenty, embeddingi w pgvector, indeks pełnotekstowy, zapisy przebiegu, sprawy. PostgreSQL we własnym obrazie kontenera ze słownikiem polskim (ispell z SJP.PL), bo bez niego „Tusk” i „Tuska” to różne słowa; do tego pg_trgm na literówki. Embeddingi z modelu wielojęzycznego, którego dostawcę i region podajemy w README. Wyniki obu wyszukiwań łączone i ważone świeżością.",
     "Jeden system do kopii i wdrożenia; DBOS korzysta z tej samej bazy. " + risk("zarządzana baza (Cloud SQL) nie pozwala dodać własnego słownika, więc PostgreSQL działa w kontenerze i sami robimy kopie."),
     "Osobna baza wektorowa; Elasticsearch."),
    ("ADR-05", "Werdykt i jego siła liczone regułą z przesłanek", A,
     "MSZ: siła werdyktu ma wynikać z jawnych przesłanek, a wynik modelu nie może być przedstawiony jako fakt bez podstawy.",
     "Model ocenia stanowisko każdego cytatu (wspiera, obala, kontekst). Kod wybiera werdykt: same cytaty wspierające dają „potwierdzone”, same obalające „fałszywe”; „wprowadzające w błąd” wymaga cytatu dającego kontekst i nazwanej techniki; źródła sprzeczne dają tylko „brak wystarczających dowodów” albo „wprowadzające w błąd”; brak cytatów to „brak wystarczających dowodów”, a opinie i przewidywania „nie podlega weryfikacji”. Siłę liczy funkcja strength_for z przesłanek (niezależne źródła, urzędowe, wiek, zgodność); źródło starsze niż 365 dni obniża ją najwyżej do „umiarkowana”. Kontrakt odrzuca werdykt niezgodny z tymi regułami.",
     "Przesłanki są widoczne dla czytelnika i powtarzalne. " + risk("reguła może być zbyt ostrożna; progi stroimy na zestawie testowym."),
     "Pewność podawana przez model; jeden prompt od pytania do werdyktu."),
    ("ADR-06", "Dosłowna weryfikacja cytatów", A,
     "Mierniki: pokrycie cytowań ≥ 95% i poprawność ≥ 85%. Model potrafi przekręcić cytat.",
     "Po wygenerowaniu odpowiedzi kod sprawdza, że każdy fragment występuje w tekście źródła (po normalizacji spacji i cudzysłowów). Tytuł, wydawcę i datę bierzemy z bazy po identyfikatorze źródła. Czy fragment wspiera tezę, ocenia osobne wywołanie, które widzi tylko twierdzenie i fragment; losową próbę sprawdzamy ręcznie w ewaluacji. Cytat niespełniający warunku odpada, a twierdzenie bez cytatu traci werdykt rozstrzygający.",
     "Brak zmyślonych cytatów i metadanych w odpowiedzi. " + risk("dosłowność nie gwarantuje, że fragment wspiera tezę; stąd osobna ocena stanowiska i ręczna próba. Parafrazy odpadają, więc prompt wymaga dosłownych fragmentów."),
     "Zaufanie modelowi; sprawdzanie podobieństwa embeddingów."),
    ("ADR-07", "Wyszukiwanie w sieci za portem, tylko w domenach z katalogu", A,
     "Bez świeżych publikacji system wstrzymuje się przy każdym bieżącym wydarzeniu. Wyszukiwanie w całym internecie łamie zasadę jasno opisanego zbioru źródeł.",
     "Port WebSearch z adapterem Firecrawl (wyszukiwanie i treść). Uruchamiany tylko przy zbyt małej liczbie dowodów w korpusie, z filtrem domen z katalogu. Limit 10 s na wyszukiwanie. Każda pobrana strona trafia do korpusu z datą pobrania, podstawą prawną i retencją (US-KOR-05); wersja korpusu rośnie dopiero po zakończeniu sprawdzenia. Tryby omijania blokad wyłączone; respektowanie robots.txt i paywalli sprawdzamy testem adaptera.",
     "Świeże dowody, ten sam wynik w obu kanałach, audytowalna lista. " + risk("dostawca spoza EOG, koszt i opóźnienie; europejski indeks (Staan) jako droga migracji."),
     "Wyszukiwanie w całym internecie; tylko statyczny korpus."),
    ("ADR-08", "Formularz WWW jako kanał podstawowy, wtyczka jako drugi", PR,
     "MSZ wymaga interfejsu WWW i drugiego kanału. Osoby o niskich kompetencjach cyfrowych nie powinny niczego instalować. Mamy gotową wtyczkę i makiety platform.",
     "Formularz WWW obsługuje każdego. Wtyczka dodaje „Sprawdź” pod postem i pole w popupie, oba wołają to samo API. Wersja bez instalacji działa na makietach demo. Bot na Discordzie budujemy od początku na tym samym API, żeby warunek dwóch kanałów nie zależał od decyzji mentorów. Status zmienimy po ich odpowiedzi.",
     "Sprawdzanie tam, gdzie człowiek widzi treść. " + risk("jury musi zainstalować wtyczkę samo; README prowadzi przez instalację w mniej niż 2 minuty."),
     "WhatsApp lub Messenger (weryfikacja konta firmowego); SMS (opłaty)."),
    ("ADR-09", "Wtyczka Chrome MV3: widżety w Shadow DOM ze skórkami platform", A,
     "Widżet trafia do cudzych feedów w trybie jasnym i ciemnym; style nie mogą przeciekać w żadną stronę.",
     "Każdy widżet renderuje się w Shadow DOM. Skórka platformy zmienia krój, promień, tło, obramowanie, przyciski i linki; znak, werdykt i blok źródeł są stałe. Zapytania do API idą przez background.js.",
     "Izolacja stylów i jeden komponent na pięć platform. " + risk("zmiany DOM platform; łagodzi to kontrakt selektorów (ADR-10)."),
     "Iframe na widżet; style globalne z prefiksem."),
    ("ADR-10", "Kontrakt selektorów: ta sama wtyczka na makietach i prawdziwych stronach", A,
     "Demo musi działać przewidywalnie, a wtyczka ma działać na prawdziwych serwisach.",
     "Makiety (demo/platforms/) odtwarzają punkty zaczepienia DOM z SELECTORS.md. Wtyczka zna tylko kontrakt selektorów.",
     "Jeden kod na demo i produkcję. " + risk("selektory platform się zmieniają."),
     "Osobny tryb demo we wtyczce."),
    ("ADR-11", "Pydantic AI ze strukturalnym wyjściem; model nie decyduje sam", A,
     "Model rozumie pytanie, wyodrębnia twierdzenia, ocenia stanowisko cytatów i pisze odpowiedź, ale nie może zmyślać źródeł ani rozstrzygać bez podstawy.",
     "Agenci Pydantic AI zwracają typy z kontraktu. Model wybierany konfiguracją; dostawca, region i koszt trafiają do CheckRecord.",
     "Model wymienny bez zmiany domeny. " + risk("różne modele różnie trzymają format; ewaluacja przy każdej zmianie."),
     "Wolny tekst parsowany ręcznie; model wpisany na sztywno."),
    ("ADR-12", "Ochrona przed prompt injection warstwami", A,
     "Scenariusz E: strona źródłowa instruuje model, by zignorował reguły. Wymagana odporność ≥ 90%.",
     "Wykrywanie poleceń w treści (wzorce i osobny klasyfikator) przed użyciem źródła; źródło z wykrytym poleceniem wypada z dowodów i trafia do ograniczeń, a zdarzenie do InjectionEvent. Ocena stanowiska widzi tylko parę: twierdzenie i fragment, bez instrukcji użytkownika i innych źródeł. Model bez narzędzi z efektami ubocznymi; werdykt liczony w kodzie (ADR-05); limit długości wejścia. Test: werdykt i cytaty mają być takie same jak dla materiału bez wstrzykniętego polecenia.",
     "Wstrzyknięte polecenie musi przejść wykrywanie i zmienić ocenę pojedynczego fragmentu, żeby wpłynąć na werdykt; reguły werdyktu i walidacja cytatów zostają bez zmian. " + risk("klasyfikator przepuści część ataków, a ocena stanowiska wciąż zależy od modelu; zestaw testowy rozszerzamy o nowe techniki."),
     "Tylko instrukcja w prompcie „nie słuchaj poleceń z treści”."),
    ("ADR-13", "Prywatność: maskowanie, retencja, usuwanie sesji", A,
     "MSZ wymaga minimalizacji danych, maskowania oczywistych danych osobowych, retencji i usuwania sesji demonstracyjnej.",
     "Maskowanie telefonów, e-maili i PESEL-i w API, zanim wystartuje workflow DBOS (DBOS zapisuje wejścia w bazie), więc ani zapis, ani dostawca modelu nie dostają danych w jawnej postaci. Retencja 30 dni, usuwanie workflowem DBOS. Bez kont; sesja identyfikowana losowym identyfikatorem w przeglądarce (CheckRecord.session_id), a „Usuń moje sprawdzenia” czyści też dane workflowów i powiązania ze sprawami.",
     "Mniej danych osobowych w systemie i u dostawców. " + risk("maskowanie regułami nie złapie wszystkiego; opisujemy to w ograniczeniach."),
     "Pełne logi bez maskowania; konta użytkowników."),
    ("ADR-14", "GCP europe-central2 i Cloudflare; demo dla jury w chmurze", A,
     "Jury musi uruchomić system albo otworzyć demo bez naszej pomocy. MSZ premiuje przejrzystość miejsca przetwarzania i mniejszą zależność od dostawców spoza EOG.",
     "Publiczne demo (API, worker, PostgreSQL w kontenerze, patrz ADR-04) w GCP europe-central2, Cloudflare przed nim (TLS, ochrona przed nadużyciami). docker compose do uruchomienia lokalnego. Serwer on-prem z GPU tylko jako opcja dla otwartego modelu.",
     "Demo niezależne od domowej sieci. " + risk("koszt GCP w trakcie oceny; budżet i limity ustawione z góry."),
     "Backend tylko na serwerze on-prem; Cloud Run bez workerów DBOS."),
    ("ADR-15", "Self-hosted runnery GitHub Actions", A,
     "CI potrzebuje mocy do buildów, testów i ewaluacji.",
     "Trzy runnery organizacji na GCP (etykieta meritum) i runner ARM64 on-prem. Ewaluacja na zestawie testowym jako zadanie CI.",
     "Szybkie buildy bez limitów minut. " + risk("host on-prem jest współdzielony z innym projektem."),
     "Runnery hostowane przez GitHub."),
    ("ADR-16", "Frontend: React, TanStack Router + Query, shadcn/ui, Tailwind v4; jakość wymuszana narzędziami", A,
     "Formularz, panel moderatora i komponenty wtyczki muszą powstać szybko i spójnie z design systemem.",
     "React z TanStack Router i TanStack Query, shadcn/ui, tokeny Meritum w Tailwind v4. Biome strict, Ruff i Ty strict, TDD, pytestarch, behave.",
     "Te same tokeny w formularzu, panelu i wtyczce. " + risk("licencja shadcnblocks do sprawdzenia przed przeniesieniem praw autorskich na MSZ."),
     "Next.js; ESLint i Prettier."),
    ("ADR-17", "Serwer MCP (FastMCP) jako kolejny adapter", PR,
     "MSZ premiuje architekturę, do której łatwo podłączyć kolejne kanały.",
     "FastMCP wystawia narzędzie „sprawdź twierdzenie” nad tym samym portem co formularz i wtyczka.",
     "Kolejny kanał to kolejny adapter na tym samym porcie. " + risk("nadużycia publicznego dostępu; klucze i limity."),
     "Tylko REST API."),
]
parts += [
    h(2, "4. Decyzje architektoniczne (ADR)"),
    p(
        "Status <strong>Przyjęta</strong> oznacza decyzję podjętą przez zespół. <strong>Proponowana</strong> czeka na "
        "przegląd albo na odpowiedź mentorów."
    ),
]
for aid, title, status, ctx, dec, cons, alt in ADRS:
    label = lambda t: f'<td style="{SUB}width:22%;">{e(t)}</td>'
    val = lambda html: f'<td style="{CELL}">{html}</td>'
    rows = "".join(
        f"<tr>{label(k)}{val(v)}</tr>"
        for k, v in [("Status", f"<strong>{e(status)}</strong>"), ("Kontekst", e(ctx)), ("Decyzja", e(dec)), ("Konsekwencje", cons), ("Alternatywy", e(alt))]
    )
    parts += [h(3, f"{aid}. {title}"), f'<table style="{TABLE}"><tbody>{rows}</tbody></table>']

# ---------------------------------------------------------------- 5. risks
RISKS = [
    ("Halucynacje", "Werdykt tylko z cytatem; cytat sprawdzany dosłownie, metadane z bazy, stanowisko oceniane osobno; wstrzymanie się przy braku dowodów."),
    ("Stronniczość źródeł", "Jawny katalog z zasadami kwalifikacji i wykluczenia, co najmniej dwa typy źródeł, rozbieżności pokazywane wprost; status źródła nigdy nie decyduje o werdykcie."),
    ("Prywatność", "Maskowanie danych osobowych przed workflowem, retencja 30 dni, usuwanie sesji, brak kont, region przetwarzania w README."),
    ("Prompt injection", "Wykrywanie poleceń, wykluczanie takich źródeł, ocena stanowiska bez instrukcji użytkownika, werdykt w kodzie, zapis zdarzeń, testy ze scenariusza E."),
    ("Dostępność", "WCAG 2.2 AA, prosty język sprawdzany narzędziem do oceny zrozumiałości, formularz na telefonie bez instalacji."),
    ("Nadużycia", "Limit zapytań, walidacja wejścia, ochrona przed SSRF przy pobieraniu linków, publikacja odpowiedzi tylko przez człowieka."),
    ("Prawa autorskie", "Podstawa prawna i retencja każdego dokumentu w korpusie, użytkownik widzi tylko krótki fragment z linkiem, usuwanie na wniosek wydawcy."),
    ("Awaria dostawcy", "Stan „Problem techniczny” albo wynik z samego korpusu z adnotacją; nigdy pozorny werdykt (scenariusz J)."),
]
parts += [h(2, "5. Najważniejsze ryzyka"), table(["Ryzyko", "Jak ograniczamy"], [row(f"<strong>{e(k)}</strong>", e(v)) for k, v in RISKS], [22, 78])]

html = f"""<!doctype html>
<html lang="pl"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>Meritum dokument produktowy</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Archivo:wght@400;700&family=Azeret+Mono:wght@400&display=swap" rel="stylesheet">
</head><body style="background:#FFFFFF;margin:24px auto;max-width:1000px;padding:0 16px;{FONT}">
{"".join(parts)}
</body></html>
"""
OUT.write_text(html, encoding="utf-8")
print(f"stories={story_count} features={len(FEATURES)} adrs={len(ADRS)} bytes={len(html)}")
assert story_count == sum(len(s) for _, _, a in STORIES for _, s in a)
