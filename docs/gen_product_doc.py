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
    h(1, "Meritum: obywatelski radar dezinformacji oraz scamu"),
    p('<span style="color:#4C5862;">Dokument produktowy · HackNation 2026 · wersja robocza</span>'),
    h(2, "1. Wprowadzenie"),
    p(
        "Meritum to niezależna, obywatelska wtyczka do przeglądarki, która działa na X, Facebooku, Instagramie, Reddicie "
        "i TikToku. Użytkownik w kilku kliknięciach zgłasza manipulację albo fałszywą reklamę, a system dołącza zgłoszenie "
        "do kampanii, do której ono należy. AI pisze szkic notatki kontekstowej z uwag użytkowników, analizy treści i źródeł "
        "z różnych stron sporu. Bez źródeł notatka nie powstanie. O publikacji decydują ludzie i sama większość głosów nie "
        "wystarcza: notatka ukazuje się dopiero wtedy, gdy za pomocną uznają ją osoby z grup, które zwykle oceniają inaczej "
        "(konsensus pomostowy). Na fałszywej reklamie wtyczka pokazuje ostrzeżenie o oszustwie i od razu zapisuje dowód: "
        "zrzut, adres, łańcuch przekierowań i czas."
    ),
    table(
        ["Wyzwanie", "Problem z wyzwania", "Odpowiedź Meritum"],
        [
            row(
                "<strong>MSZ „Prawdowid”</strong>",
                "Odróżnić fakt od manipulacji, dotrzeć do wiarygodnych źródeł, świadomie oceniać treści.",
                "Notatka kontekstowa z obowiązkowymi źródłami, spektrum mediów, nazwana technika manipulacji z podpowiedzią „jak rozpoznać?”, konsensus odporny na boty.",
            ),
            row(
                "<strong>NASK „Kolekcjoner fejków”</strong>",
                "Fałszywe reklamy z wizerunkiem znanych osób szybko znikają, zmieniają formę i wracają pod nowymi adresami; pojedynczy materiał to fragment większej kampanii.",
                "Graf kampanii (warianty, domeny, platformy na jednej osi czasu), sejf dowodów zapisany przed zniknięciem reklamy, ostrzeżenie przed kliknięciem, eksport dla CERT.",
            ),
        ],
        [20, 38, 42],
    ),
    p(
        "Projekt nie ma partnerstw z instytucjami organizującymi wyzwania. Wszystkie liczby, konta i osoby w demo są "
        "fikcyjne i oznaczone jako dane symulowane."
    ),
]

# ---------------------------------------------------------------- 2. stories
MVP, PO = "MVP hackathon", "Po hackathonie"

# domain -> list of (actor, [(id, actor_em, want, so_that, [criteria], priority, contract)])
STORIES: list[tuple[str, str, list[tuple[str, list[tuple]]]]] = [
    ("2.1", "Zgłoszenia i dowody", [
        ("Zgłaszający", [
            ("US-ZGL-01", "Jako zgłaszający", "zgłosić post jako manipulację z popovera pod postem w kilku kliknięciach",
             "nie przerywać przeglądania feedu",
             ["Popover otwiera się przy poście i pokazuje „Post @nazwa”.", "Wybór typu (Manipulacja / Oszustwo) i jednego lub więcej powodów.", "Bez powodu wymagany opis co najmniej 3 znaki."],
             MVP, "ReportPayload, QuickReportPopover"),
            ("US-ZGL-02", "Jako zgłaszający", "zgłosić reklamę jako oszustwo z powodem (fałszywy wizerunek, podejrzana inwestycja, podszywanie się pod bank lub urząd, fałszywy sklep lub zbiórka)",
             "oznaczyć fejka, zanim ktoś straci pieniądze",
             ["Lista powodów zależy od typu zgłoszenia.", "Kody powodów pochodzą z kontraktu, teksty z copy/pl.json."],
             MVP, "ReportPayload.reasons (ScamReason)"),
            ("US-ZGL-03", "Jako zgłaszający", "dołączyć opcjonalny link do źródła",
             "AI i oceniający szybciej zweryfikowali sprawę",
             ["Pole przyjmuje tylko pełny adres https://.", "Błędny adres pokazuje komunikat po polsku, bez utraty formularza."],
             MVP, "ReportPayload.source_url"),
            ("US-ZGL-04", "Jako zgłaszający", "widzieć postęp analizy mojego zgłoszenia krok po kroku",
             "wiedzieć, że zgłoszenie działa i co z nim się dzieje",
             ["Kroki odzwierciedlają workflow DBOS (np. łączenie z podobnymi zgłoszeniami, źródła, dowód, kampanie, lista CERT).", "Wynik: notatka opublikowana, w ocenie, oszustwo oznaczone albo zebrane."],
             MVP, "AnalysisStatus, AnalysisStep, AnalysisSteps"),
            ("US-ZGL-05", "Jako zgłaszający", "nie stracić zgłoszenia przy błędzie sieci i nie wysłać go dwa razy",
             "nie musieć wypełniać formularza od nowa",
             ["Przy błędzie odpowiedzi zostają w formularzu.", "Ponowne zgłoszenie tego samego posta pokazuje „To zgłoszenie już wysłałeś”."],
             MVP, "QuickReportPopover"),
        ]),
        ("Czytelnik", [
            ("US-ZGL-06", "Jako czytelnik", "żeby wtyczka zapisała dowód w chwili, gdy widzę podejrzaną reklamę",
             "ślad został, nawet gdy reklama zniknie",
             ["Zapis: zrzut ekranu, adres, liczba przekierowań, domena docelowa, czas.", "Karta pokazuje „Zapisany o …” z liczbą przekierowań."],
             MVP, "Evidence"),
        ]),
    ]),
    ("2.2", "Kampanie i łączenie treści", [
        ("Zgłaszający", [
            ("US-KAM-01", "Jako zgłaszający", "zobaczyć, do której kampanii trafiło moje zgłoszenie",
             "wiedzieć, że zgłosiłem fragment większej operacji",
             ["Karta pokazuje identyfikator kampanii (#K-…), liczbę reklam, domen i dni.", "Link „zobacz kampanię” prowadzi do widoku kampanii."],
             MVP, "CampaignRef"),
            ("US-KAM-02", "Jako zgłaszający", "dostać jedno powiadomienie, gdy kampania, której wariant zgłosiłem, wraca pod nową domeną",
             "widzieć, że moje zgłoszenie działa dalej",
             ["Jedno powiadomienie na powrót kampanii, nie na każdą reklamę.", "Powiadomienie podaje nową domenę i link do kampanii."],
             PO, "Campaign"),
        ]),
        ("Analityk / fact-checker", [
            ("US-KAM-03", "Jako analityk", "zobaczyć wszystkie warianty kampanii, jej domeny i platformy na jednej osi czasu",
             "ocenić skalę operacji z jednego zgłoszenia",
             ["Każda domena to wiersz ze stanem: aktywna, nieaktywna, przewidziana.", "Suma reklam na platformach równa się liczbie reklam kampanii (walidacja w kontrakcie)."],
             MVP, "Campaign, CampaignDomain, CampaignRotation"),
            ("US-KAM-04", "Jako analityk", "zobaczyć wspólne ślady, które łączą reklamy w kampanię",
             "rozumieć i móc obronić decyzję o połączeniu",
             ["Ślady: twarz z rejestru, szablon strony, wystawca certyfikatów, bramka płatności, konta reklamodawców, tekst reklamy.", "Przy każdym śladzie liczba reklam, które go mają."],
             MVP, "SharedTrace"),
            ("US-KAM-05", "Jako analityk", "widzieć domeny przewidziane z logów Certificate Transparency jako osobny stan",
             "przygotować się na kolejny wariant, zanim trafi do reklamy",
             ["Domena przewidziana jest oznaczona słowem i linią przerywaną, nie samym kolorem.", "Trafia do ostrzeżeń dopiero po potwierdzeniu przez ludzi."],
             PO, "CampaignDomain.state = predicted"),
            ("US-KAM-06", "Jako analityk", "łączyć posty dezinformacyjne skoordynowanej sieci kont w jedną operację tak samo jak reklamy",
             "jeden silnik obsłużył oba zagrożenia",
             ["Podobieństwo tekstu i mediów liczone tym samym mechanizmem co dla reklam.", "Operacja dezinformacyjna ma ten sam widok co kampania reklamowa."],
             PO, "Campaign"),
        ]),
    ]),
    ("2.3", "Notatki kontekstowe i źródła", [
        ("Czytelnik", [
            ("US-NOT-01", "Jako czytelnik", "zobaczyć pod postem krótką notatkę kontekstową ze stanem",
             "w kilka sekund zrozumieć, czy post wprowadza w błąd i dlaczego",
             ["Stan zawsze słowem: „Zweryfikowany” albo „W ocenie”.", "Notatka wyjaśnia i cytuje źródła, bez oceniania autorów."],
             MVP, "NoteCard, ContextCard"),
            ("US-NOT-02", "Jako czytelnik", "otworzyć źródła notatki z ich rodzajem i domeną",
             "samodzielnie sprawdzić, skąd pochodzi kontekst",
             ["Każde źródło ma tytuł, domenę i rodzaj (akt prawny, instytucja, media, fact-checking…).", "Notatka ma co najmniej jedno źródło."],
             MVP, "Source, SourceKind"),
            ("US-NOT-03", "Jako czytelnik", "widzieć, z której strony sporu pochodzą cytowane media",
             "ufać, że notatka nie przyszła od jednej strony",
             ["Media mają pozycję na osi od lewej do prawej, ocenianą przez użytkowników.", "Pozostałe rodzaje źródeł nie mają pozycji."],
             MVP, "Source.spectrum"),
            ("US-NOT-04", "Jako czytelnik", "kliknąć „Dlaczego to widzę?” i dowiedzieć się, jak powstała notatka",
             "rozumieć, jak działa system, który ją pokazuje",
             ["Jedno zdanie: z ilu uwag i źródeł AI zrobiła szkic i że zdecydowały dwie grupy."],
             MVP, "NoteCard.drafted_from_reports"),
            ("US-NOT-05", "Jako czytelnik", "zwinąć albo zamknąć widżet",
             "Meritum nie zabierało mi feedu",
             ["Widżet jest kompaktowy i daje się zamknąć klawiaturą (Esc).", "Nie przesuwa ani nie zasłania treści posta."],
             MVP, "ContextCard"),
        ]),
        ("Analityk / fact-checker", [
            ("US-NOT-06", "Jako fact-checker", "dostać szkic notatki AI z uwag użytkowników, analizy treści i źródeł",
             "nie pisać kontekstu od zera",
             ["Szkic bez źródła nie przechodzi walidacji kontraktu.", "AI nie publikuje: publikacja zależy wyłącznie od konsensusu."],
             MVP, "NoteCard (Pydantic AI)"),
            ("US-NOT-07", "Jako fact-checker", "żeby system poprosił o źródło z drugiej strony, gdy notatka cytuje media tylko z jednej",
             "notatka przeszła ocenę obu grup",
             ["Głosowanie odblokowuje się po dodaniu źródła z drugiej strony osi."],
             PO, "Source.spectrum"),
        ]),
    ]),
    ("2.4", "Konsensus i odporność na boty", [
        ("Oceniający", [
            ("US-KON-01", "Jako oceniający", "ocenić notatkę jako pomocną albo niepomocną",
             "mój głos wpłynął na publikację",
             ["Jeden głos na notatkę z jednego konta urządzenia.", "Po głosie widzę aktualny stan zgody obu grup."],
             MVP, "Consensus"),
            ("US-KON-02", "Jako oceniający", "widzieć pasek zgody dwóch grup z progiem",
             "rozumieć, że sama większość nie wystarczy",
             ["Pasek pokazuje procent „pomocne” i liczbę ocen każdej grupy.", "Notatka jest „Zweryfikowana” tylko, gdy obie grupy przekroczą próg (domyślnie 70%)."],
             MVP, "Consensus, GroupScore"),
        ]),
        ("Analityk / fact-checker", [
            ("US-KON-03", "Jako analityk", "obserwować na żywo atak klastra kont na notatkę: głosy liczone kontra odrzucone w każdej minucie",
             "widzieć, że atak nie zmienił wyniku",
             ["Sumy liczone są z serii minutowej, nigdy wysyłane osobno.", "Na ekranie zawsze „oddane = liczone + odrzucone”."],
             MVP, "BotDefenseSnapshot, VoteMinute, BotDefenseTelemetry"),
            ("US-KON-04", "Jako analityk", "przejrzeć odrzucone konta z powodem odrzucenia",
             "móc pokazać, dlaczego filtr odrzucił konto",
             ["Powody słowami: ten sam klaster, rytm głosów, nowe konto, ten sam graf ocen.", "Nazwy kont w demo są fikcyjne."],
             MVP, "RejectedAccount"),
            ("US-KON-05", "Jako analityk", "dostać wyraźny sygnał, gdy atak jednak zmienił status notatki",
             "ręcznie sprawdzić oceny",
             ["Tytuł „Atak zmienił status notatki” i prośba o ręczną ocenę.", "Kolor czerwony tylko razem ze słowem."],
             MVP, "BotDefenseSnapshot.status_changed"),
        ]),
        ("Administrator", [
            ("US-KON-06", "Jako administrator", "odtworzyć nagrany scenariusz ataku i kampanii bez dostępu do internetu",
             "demo na sali nie zależało od Wi-Fi",
             ["Scenariusz odtwarzany jako workflow DBOS.", "Dane mają flagę „simulated” i podpis „Dane symulowane”."],
             MVP, "BotDefenseSnapshot.simulated, Campaign.simulated"),
        ]),
    ]),
    ("2.5", "Ostrzeżenia o oszustwach i ochrona", [
        ("Czytelnik", [
            ("US-OSZ-01", "Jako czytelnik", "zobaczyć ostrzeżenie na fałszywej reklamie, zanim w nią kliknę",
             "nie stracić pieniędzy",
             ["Ostrzeżenie pokazuje kampanię, zapisany dowód i źródło (np. dementi).", "Stan „Oszustwo” zawsze słowem."],
             MVP, "ScamWarningCard, ContextCard"),
            ("US-OSZ-02", "Jako czytelnik", "dostawać ostrzeżenie tylko wtedy, gdy są co najmniej dwa niezależne sygnały",
             "nie dostawać fałszywych alarmów",
             ["Sygnały: lista ostrzeżeń CERT Polska, znana kampania, rejestr wizerunków, zgłoszenia użytkowników.", "Mniej niż dwa sygnały: walidacja kontraktu odrzuca kartę."],
             MVP, "ScamWarningCard.signals"),
            ("US-OSZ-03", "Jako czytelnik", "zakwestionować ostrzeżenie przyciskiem „To pomyłka?”",
             "błędne ostrzeżenie trafiło do ponownej oceny przez ludzi",
             ["Każde ostrzeżenie ma tę akcję.", "Po zgłoszeniu pomyłki widzę, że sprawa wróciła do oceny."],
             MVP, "ScamWarningCard"),
            ("US-OSZ-04", "Jako czytelnik", "ukryć fałszywą reklamę albo zgłosić ją platformie",
             "nie widzieć jej więcej i pomóc ją usunąć",
             ["„Ukryj reklamę” i „Pokaż” działają bez przeładowania.", "„Zgłoś platformie” otwiera formularz platformy."],
             MVP, "ContextCard"),
        ]),
        ("Osoba starsza i opiekun", [
            ("US-OSZ-05", "Jako osoba starsza", "zostać zatrzymana przed wejściem na stronę z kampanii inwestycyjnej",
             "nie podać danych karty oszustom",
             ["Pełnoekranowa blokada z prostym wyjaśnieniem i przyciskiem powrotu.", "Blokada pojawia się przed wyjaśnieniem."],
             PO, "brak"),
            ("US-OSZ-06", "Jako opiekun", "dostać powiadomienie, gdy bliska osoba zostanie zatrzymana na stronie z kampanii",
             "zadzwonić do niej, zanim zrobi przelew",
             ["Powiadomienie tylko za zgodą osoby chronionej.", "Bez treści przeglądanych stron: tylko kampania i czas."],
             PO, "brak"),
        ]),
    ]),
    ("2.6", "Edukacja i techniki manipulacji", [
        ("Czytelnik", [
            ("US-EDU-01", "Jako czytelnik", "zobaczyć nazwę techniki manipulacji i jedno zdanie „jak rozpoznać?”",
             "następnym razem rozpoznać ją sam",
             ["Techniki: m.in. fałszywy autorytet, wyrwanie z kontekstu, presja czasu, zmyślony cytat, wybiórcze dane.", "Treść podpowiedzi pochodzi z copy/pl.json."],
             MVP, "Technique, TechniqueCode"),
            ("US-EDU-02", "Jako czytelnik", "żeby ostrzeżenie o oszustwie też nazywało technikę (np. presja czasu, podszywanie się)",
             "uczyć się rozpoznawać manipulację także na reklamach",
             ["Ta sama lista technik dla notatek i ostrzeżeń."],
             MVP, "ScamWarningCard.technique"),
        ]),
        ("Osoba starsza i opiekun", [
            ("US-EDU-03", "Jako osoba starsza", "po zatrzymaniu dostać krótkie wyjaśnienie, po czym poznać takie oszustwo",
             "lepiej się bronić bez pomocy",
             ["Jedno lub dwa zdania prostym językiem, bez żargonu."],
             PO, "Technique"),
        ]),
        ("Analityk / fact-checker", [
            ("US-EDU-04", "Jako analityk", "mieć techniki dezinformacji zmapowane na otwarty framework DISARM",
             "raportować w języku, którym opisuje się FIMI w UE",
             ["Każdy kod techniki ma przypisany identyfikator DISARM tam, gdzie istnieje odpowiednik."],
             PO, "TechniqueCode"),
        ]),
    ]),
    ("2.7", "Panel analityka i eksport (CERT, platformy, DSA)", [
        ("Analityk / fact-checker", [
            ("US-ANA-01", "Jako analityk", "mieć panel z dwoma widokami: kampania i atak na notatkę",
             "śledzić kampanie i ataki w jednym miejscu",
             ["Nawigacja między widokami bez przeładowania strony.", "Działa w trybie jasnym i ciemnym."],
             MVP, "CampaignRotation, BotDefenseTelemetry"),
            ("US-ANA-02", "Jako analityk", "filtrować kampanie po platformie, stanie domen i czasie",
             "szybko znaleźć aktywne operacje",
             ["Filtry zapisują się w adresie URL panelu."],
             PO, "Campaign"),
        ]),
        ("Operator CERT", [
            ("US-ANA-03", "Jako operator CERT", "wyeksportować dowody kampanii w formacie gotowym do zgłoszenia",
             "nie zbierać ręcznie śladów, które już zniknęły",
             ["Paczka zawiera zrzuty, adresy, łańcuchy przekierowań, czasy i hashe plików.", "Na hackathonie jako makieta przycisku i podglądu."],
             PO, "Campaign, Evidence"),
            ("US-ANA-04", "Jako operator CERT", "żeby analiza sprawdzała domenę na liście ostrzeżeń CERT Polska",
             "trafienie było jednym z dwóch sygnałów ostrzeżenia",
             ["Krok „Sprawdzamy domenę na liście CERT Polska” w pasku analizy.", "Trafienie zapisane jako sygnał cert_warning_list."],
             MVP, "AnalysisStep check_cert_list"),
        ]),
        ("Analityk / fact-checker (platformy i DSA)", [
            ("US-ANA-05", "Jako analityk", "jednym przyciskiem przygotować paczkę dowodów kampanii dla platformy lub zaufanego podmiotu sygnalizującego (art. 22 DSA)",
             "pokazać, jak wyglądałoby przekazanie dowodów platformie",
             ["Paczka opisuje kampanię, wszystkie warianty i dowody.", "Format opisany jako „gotowy do integracji”, bez deklarowania współpracy."],
             PO, "Campaign"),
        ]),
    ]),
    ("2.8", "Platforma, API i MCP", [
        ("Redakcja / dziennikarz (API, MCP)", [
            ("US-API-01", "Jako dziennikarz", "zapytać mojego asystenta AI przez MCP, czy domena należy do znanej kampanii",
             "zweryfikować trop bez instalowania wtyczki",
             ["Narzędzie MCP zwraca kampanię, stan domeny i źródła albo informację, że domena jest nieznana."],
             MVP, "FastMCP, CampaignRef"),
            ("US-API-02", "Jako dziennikarz", "zapytać przez MCP, jakie notatki dotyczą danego posta lub adresu",
             "cytować kontekst z jego źródłami",
             ["Odpowiedź zawiera treść notatki, stan i źródła z kontraktu."],
             MVP, "FastMCP, NoteCard"),
            ("US-API-03", "Jako redakcja", "korzystać z publicznego API z kluczem i limitem zapytań",
             "zbudować własne narzędzia na tym samym silniku",
             ["Dokumentacja OpenAPI generowana z kontraktów Pydantic.", "Klucz i limit na redakcję."],
             PO, "contracts (OpenAPI)"),
        ]),
        ("Czytelnik", [
            ("US-API-04", "Jako czytelnik", "widzieć widżet Meritum na każdej z pięciu platform w stylu tej platformy, ale z tym samym znakiem i stanami",
             "widżet pasował do platformy, a jednocześnie było widać, że pochodzi od Meritum",
             ["Skórka: krój, promień, tło, przyciski, linki platformy.", "Stałe: znak i słowo „Meritum”, kolory stanów, pasek zgody, źródła; nigdy logo platformy."],
             MVP, "ContextCard (skórki)"),
            ("US-API-05", "Jako czytelnik", "dostać jasny komunikat, gdy jestem offline albo na nieobsługiwanej stronie",
             "wiedzieć, czemu nie widzę notatek",
             ["Komunikaty z copy/pl.json (offline, unsupported_site)."],
             MVP, "brak"),
        ]),
        ("Administrator", [
            ("US-API-06", "Jako administrator", "wdrażać backend, workery DBOS i bazę przez GitHub Actions na własnych runnerach",
             "mieć powtarzalne wdrożenia bez ręcznego logowania na serwery",
             ["Buildy na runnerach GCP (x64), wdrożenie backendu na runnerze ARM64 on-prem.", "Obrazy Dockera budowane dla linux/arm64."],
             MVP, "infra"),
            ("US-API-07", "Jako administrator", "generować JSON Schema i typy TypeScript z kontraktów Pydantic w CI",
             "API, wtyczka i panel nie rozjechały się",
             ["Skrypt generate.sh w CI; różnica w wygenerowanych plikach zatrzymuje build."],
             MVP, "meritum_contracts.py"),
        ]),
    ]),
    ("2.9", "Prywatność i zgody (rejestr wizerunków opt-in, tryb opiekuna)", [
        ("Osoba publiczna (rejestr wizerunków)", [
            ("US-PRY-01", "Jako osoba publiczna", "zgłosić swoją twarz i oficjalne kanały do rejestru opt-in",
             "reklamy z moim wizerunkiem poza tymi kanałami dostawały ostrzeżenie",
             ["Bez wpisu w rejestrze system nie przetwarza twarzy.", "Trafienie w rejestrze to sygnał celebrity_registry."],
             PO, "ScamWarningCard.signals"),
            ("US-PRY-02", "Jako osoba publiczna", "dostawać raport kampanii, które używają mojego wizerunku",
             "reagować publicznie i prawnie",
             ["Raport z listą kampanii, wariantów i domen."],
             PO, "Campaign, SharedTrace"),
            ("US-PRY-03", "Jako osoba publiczna", "wycofać zgodę i usunąć swoje dane z rejestru",
             "zachować kontrolę nad wizerunkiem (RODO)",
             ["Usunięcie obejmuje wzorce twarzy i kanały.", "Potwierdzenie usunięcia z datą."],
             PO, "brak"),
        ]),
        ("Zgłaszający", [
            ("US-PRY-04", "Jako zgłaszający", "zgłaszać anonimowo, bez zakładania konta z hasłem",
             "nie bać się zgłoszenia",
             ["Formularz informuje, że zgłoszenie jest anonimowe.", "Kontrakt zgłoszenia nie zawiera danych osobowych zgłaszającego."],
             MVP, "ReportPayload"),
        ]),
        ("Osoba starsza i opiekun", [
            ("US-PRY-05", "Jako osoba starsza", "włączyć tryb opiekuna kodem od bliskiej osoby i w każdej chwili go wyłączyć",
             "decydować, co bliscy wiedzą",
             ["Parowanie kodem, bez konta z hasłem.", "Wyłączenie trybu kończy powiadomienia."],
             PO, "brak"),
        ]),
        ("Administrator", [
            ("US-PRY-06", "Jako administrator", "przechowywać dowody minimalnie, z datą usunięcia",
             "spełnić zasadę minimalizacji danych",
             ["Każdy dowód ma termin retencji.", "Automatyczne usuwanie po terminie (workflow DBOS)."],
             PO, "Evidence"),
        ]),
    ]),
]

story_count = 0
parts += [
    h(2, "2. Historie użytkowników"),
    p(
        "Historie są pogrupowane według domen, a w każdej domenie według aktorów. Priorytet <strong>MVP hackathon</strong> "
        "oznacza zakres z sekcji 11 dokumentu KEY_SELLING_POINTS.md (budujemy albo pokazujemy w demo); "
        "<strong>Po hackathonie</strong> to rozwój lub makieta. Kolumna „Kontrakt / komponent” wskazuje model z "
        "contracts/meritum_contracts.py albo komponent z components/meritum/."
    ),
]
for num, domain, actors in STORIES:
    rows: list[str] = []
    for actor, stories in actors:
        rows.append(sub_row(actor, 5))
        for sid, who, want, so, crit, prio, contract in stories:
            story_count += 1
            text = f"<em>{e(who)}</em> chcę {e(want)}, aby {e(so)}."
            ac = "<br>".join(f"• {e(c)}" for c in crit)
            rows.append(row(f"<strong>{sid}</strong>", text, ac, e(prio), code(contract) if contract != "brak" else "brak"))
    parts += [h(3, f"{num}. {domain}"), table(["ID", "Historia", "Kryteria akceptacji", "Priorytet", "Kontrakt / komponent"], rows, [15, 24, 26, 13, 22])]

# ---------------------------------------------------------------- 3. features
FEATURES = [
    ("F-01", "Szybkie zgłoszenie", "Popover pod postem: typ, powody, opis, opcjonalne źródło; anonimowo, bez konta.", "ZGL-01, ZGL-02, ZGL-03, ZGL-05, PRY-04", "oba", "Budujemy", "S"),
    ("F-02", "Pasek analizy", "Kroki workflow DBOS widoczne w wtyczce po zgłoszeniu, z wynikiem analizy.", "ZGL-04, ANA-04", "oba", "Budujemy", "M"),
    ("F-03", "Sejf dowodów", "Zapis w chwili zobaczenia: zrzut, adres, przekierowania, czas; hash pliku.", "ZGL-06, OSZ-01", "NASK", "Budujemy", "M"),
    ("F-04", "Karta kontekstu", "Notatka pod postem ze stanem, źródłami, spektrum mediów i „Dlaczego to widzę?”.", "NOT-01, NOT-02, NOT-03, NOT-04, NOT-05", "MSZ", "Budujemy", "M"),
    ("F-05", "Szkic notatki AI ze źródłami", "Pydantic AI pisze szkic z uwag, analizy treści i źródeł; kontrakt odrzuca szkic bez źródła.", "NOT-06, NOT-07", "MSZ", "Budujemy", "L"),
    ("F-06", "Konsensus pomostowy i oceny", "Głosowanie „pomocne / niepomocne”, dwie grupy, próg dla obu; pasek zgody.", "KON-01, KON-02", "MSZ", "Budujemy", "L"),
    ("F-07", "Telemetria ataku botów", "Widok na żywo: liczone kontra odrzucone na minutę, odrzucone konta z powodem, alarm zmiany statusu.", "KON-03, KON-04, KON-05, KON-06", "oba", "Budujemy", "M"),
    ("F-08", "Ostrzeżenie o fałszywej reklamie", "Karta „Oszustwo” z kampanią, dowodem, techniką, „To pomyłka?”, ukryciem reklamy; min. dwa sygnały.", "OSZ-01, OSZ-02, OSZ-03, OSZ-04, EDU-02", "NASK", "Budujemy", "M"),
    ("F-09", "Graf kampanii na pgvector", "Łączenie zgłoszeń po podobieństwie obrazu, tekstu, szablonu strony i domen dla przygotowanego zbioru reklam.", "KAM-01, KAM-06", "oba", "Budujemy", "L"),
    ("F-10", "Widok kampanii w panelu", "Oś rotacji domen, suma reklam na platformach, tabela wspólnych śladów.", "KAM-03, KAM-04, ANA-01", "NASK", "Budujemy", "M"),
    ("F-11", "Techniki manipulacji", "Nazwa techniki i podpowiedź „jak rozpoznać?” w notatkach i ostrzeżeniach.", "EDU-01, EDU-02, EDU-03", "MSZ", "Budujemy", "S"),
    ("F-12", "Serwer MCP", "FastMCP z dwoma narzędziami: domena a kampania, notatki dla posta lub adresu.", "API-01, API-02", "oba", "Budujemy", "S"),
    ("F-13", "Skórki pozostałych platform", "Widżet na Facebooku, Instagramie, Reddicie i TikToku na makietach platform.", "API-04", "oba", "Makieta", "M"),
    ("F-14", "Tryb opiekuna", "Blokada strony z kampanii, parowanie kodem, powiadomienie bliskiej osoby za zgodą.", "OSZ-05, OSZ-06, PRY-05, EDU-03", "NASK", "Makieta", "M"),
    ("F-15", "Rejestr wizerunków opt-in", "Twarze i oficjalne kanały osób, które się zgodziły; raporty kampanii; wycofanie zgody.", "PRY-01, PRY-02, PRY-03", "NASK", "Makieta", "L"),
    ("F-16", "Predykcja domen z logów certyfikatów", "Obserwacja logów Certificate Transparency i stan „przewidziana” na osi kampanii.", "KAM-05", "NASK", "Makieta", "M"),
    ("F-17", "Eksport dowodów dla CERT", "Paczka dowodów kampanii w formacie gotowym do zgłoszenia.", "ANA-03", "NASK", "Makieta", "S"),
    ("F-18", "Raport dla platform i DSA", "Paczka dowodów dla platformy lub zaufanego podmiotu sygnalizującego.", "ANA-05", "oba", "Pomijamy", "M"),
    ("F-19", "Powiadomienie o powrocie kampanii", "Jedno powiadomienie dla zgłaszających, gdy kampania wraca pod nową domeną.", "KAM-02", "NASK", "Pomijamy", "S"),
    ("F-20", "Mapowanie na DISARM", "Identyfikatory DISARM dla kodów technik w panelu i eksporcie.", "EDU-04", "MSZ", "Pomijamy", "S"),
    ("F-21", "Publiczne API z kluczami", "API dla redakcji z kluczem, limitem i dokumentacją OpenAPI.", "API-03", "oba", "Pomijamy", "M"),
    ("F-22", "Filtry panelu i retencja dowodów", "Filtry kampanii w panelu; automatyczne usuwanie dowodów po terminie.", "ANA-02, PRY-06", "oba", "Pomijamy", "M"),
    ("F-23", "Kontrakty i dostarczanie", "Generowanie JSON Schema i TS z kontraktów w CI; wdrożenia na self-hosted runnerach; tryb offline i komunikaty.", "API-05, API-06, API-07", "oba", "Budujemy", "S"),
]
parts += [
    h(2, "3. Proponowane funkcje"),
    p(
        "Funkcje wynikają z historii z sekcji 2. Zakres jak w sekcji 11 KEY_SELLING_POINTS.md: <strong>Budujemy</strong> "
        "naprawdę, pokazujemy jako <strong>Makieta</strong>, <strong>Pomijamy</strong> na hackathonie. Nakład: "
        "<strong>S</strong> do kilku godzin, <strong>M</strong> około dnia, <strong>L</strong> więcej niż dzień pracy zespołu."
    ),
    table(
        ["ID", "Funkcja", "Opis", "Historie", "Wyzwanie", "Zakres", "Nakład"],
        [
            row(f"<strong>{fid}</strong>", f"<strong>{e(name)}</strong>", e(desc), e(", ".join("US-" + s for s in stories.split(", "))), e(ch), e(scope), e(eff))
            for fid, name, desc, stories, ch, scope, eff in FEATURES
        ],
        [8, 15, 27, 17, 12, 12, 9],
    ),
]

# ---------------------------------------------------------------- 4. ADRs
A, PR = "Przyjęta", "Proponowana"
ADRS = [
    ("ADR-01", "Pionowe wycinki domenowe z architekturą heksagonalną", A,
     "Zespół buduje w krótkim czasie kilka domen naraz (zgłoszenia, kampanie, notatki, konsensus, ostrzeżenia) i musi pracować równolegle bez konfliktów.",
     "Backend dzielimy na pionowe wycinki według domen. Każdy powtarza te same podfoldery: models/, dtos/, ports/, adapters/. Domena zależy tylko od portów; FastAPI, DBOS, PostgreSQL i LLM to adaptery. Granice pilnuje pytestarch.",
     "Nowa funkcja trafia do nowego wycinka i nie wymaga zmian w warstwach całej aplikacji. Domenę testujemy bez bazy i sieci. " + risk("więcej plików na start i pokusa skrótów pod presją czasu; testy architektury łapią je w CI."),
     "Klasyczne warstwy (routers/services/repositories); jeden moduł na całą aplikację."),
    ("ADR-02", "Kontrakty Pydantic jako jedno źródło prawdy", A,
     "API, wtyczka i panel renderują te same dane (karty, zgłoszenia, kampanie, telemetrię). Rozjazd typów psuje demo.",
     "contracts/meritum_contracts.py definiuje modele (m.in. ReportPayload, NoteCard, ScamWarningCard, Campaign, BotDefenseSnapshot). Z nich generujemy JSON Schema i typy TypeScript (generate.sh). Kontrakt niesie kody, a teksty są w copy/pl.json.",
     "Reguły produktu (źródło obowiązkowe, dwa sygnały, suma reklam) sprawdza walidacja modeli. Modele są zamrożone i odrzucają nadmiarowe pola. " + risk("zmiana kontraktu wymaga regeneracji typów; CI musi to wymuszać."),
     "Ręcznie pisane typy TS; OpenAPI jako źródło i generowanie Pydantic z niego."),
    ("ADR-03", "DBOS dla trwałych workflowów analizy zgłoszeń", A,
     "Analiza zgłoszenia ma kilka kroków (podobne zgłoszenia, źródła, szkic AI, dowód, kampanie, lista CERT) z wywołaniami zewnętrznymi, które mogą się nie udać.",
     "Każda analiza to workflow DBOS z krokami odpowiadającymi AnalysisStep. Status kroków odczytuje wtyczka (AnalysisStatus). Ten sam mechanizm odtwarza nagrany scenariusz demo offline.",
     "Restart workera nie gubi zgłoszeń; kroki są ponawiane, a stan jest w PostgreSQL. " + risk("nowa dla zespołu biblioteka; trzeba trzymać kroki idempotentne."),
     "Celery z Redisem; kolejka w chmurze (Pub/Sub, Cloud Tasks); zwykłe zadania w tle FastAPI."),
    ("ADR-04", "PostgreSQL z pgvector dla podobieństwa i grafu kampanii", A,
     "Łączenie wariantów w kampanie wymaga wyszukiwania podobnych obrazów, tekstów i szablonów stron obok zwykłych danych relacyjnych.",
     "Jedna baza PostgreSQL: dane relacyjne, embeddingi w pgvector, hashe percepcyjne i odciski szablonów. Graf kampanii jako tabele relacji, bez osobnej bazy grafowej.",
     "Jeden system do kopii, migracji i wdrożenia; zapytania łączą podobieństwo z filtrami. DBOS korzysta z tej samej bazy. " + risk("przy dużej skali indeksy wektorowe wymagają strojenia."),
     "Osobna baza wektorowa (Qdrant, Pinecone); baza grafowa (Neo4j)."),
    ("ADR-05", "Konsensus pomostowy zamiast większości głosów", A,
     "Większość głosów łatwo przejąć farmą botów lub brigadingiem, a czytelnik nie ufa notatce, która wygląda na głos jednej strony.",
     "Notatka jest „Zweryfikowana” tylko, gdy obie grupy, które zwykle oceniają inaczej, przekroczą próg (domyślnie 70%). Walidator NoteCard odrzuca status verified bez zgody obu grup. Głosy z klastrów botów nie są liczone.",
     "Atak klastra kont nie przepycha ani nie zakopuje notatki, a filtr jest wyjaśnialny (RejectedAccount). " + risk("mniej notatek osiąga publikację; przy małej liczbie oceniających podział na grupy jest niestabilny."),
     "Zwykła większość; moderacja redakcyjna; ocena wyłącznie przez AI."),
    ("ADR-06", "Źródła i sygnały wymuszone w kontrakcie", A,
     "Zasad „źródła są obowiązkowe” i „ostrzeżenie wymaga dwóch niezależnych sygnałów” nie może obejść ani AI, ani interfejs.",
     "NoteCard i ScamWarningCard wymagają co najmniej jednego źródła; ScamWarningCard wymaga co najmniej dwóch sygnałów. Szkic AI, który tego nie spełnia, nie przechodzi walidacji i wraca do poprawy.",
     "Zasada produktu jest sprawdzalna testem. " + risk("AI może dawać słabe źródła; jakość źródeł oceniają ludzie."),
     "Zasada w promptach i przeglądzie ręcznym."),
    ("ADR-07", "Sejf dowodów w chwili zobaczenia", A,
     "Fałszywe reklamy żyją krótko; po zgłoszeniu platformie znikają razem ze śladami.",
     "Wtyczka zapisuje dowód lokalnie w chwili wyświetlenia reklamy (zrzut, adres, przekierowania, czas) i wysyła go z analizą. Na hackathonie: zrzut, adres i czas. Proponujemy pliki w magazynie obiektów GCP, a metadane i hash w PostgreSQL.",
     "Dowód zostaje także po zniknięciu reklamy i nadaje się do eksportu. " + risk("dane osobowe na zrzutach; potrzebna minimalizacja i termin usunięcia (US-PRY-06)."),
     "Zapis dopiero po stronie serwera po zgłoszeniu (za późno); zewnętrzne archiwa stron."),
    ("ADR-08", "Wtyczka Chrome MV3: widżety w Shadow DOM ze skórkami platform", A,
     "Widżet wstrzykujemy do cudzych feedów w trybie jasnym i ciemnym; CSS platformy nie może przeciekać do widżetu ani odwrotnie, a widżet ma wyglądać natywnie.",
     "Wtyczka Manifest V3. Każdy widżet renderuje się w Shadow DOM. Skórka platformy zmienia krój, promień, tło, obramowanie, przyciski i linki; znak „Meritum”, kolory stanów, pasek zgody i źródła są stałe. Framework UI wtyczki wciąż otwarty.",
     "Izolacja stylów w obie strony i jeden komponent na pięć platform. " + risk("zmiany DOM platform; łagodzi to kontrakt selektorów (ADR-09)."),
     "Iframe na widżet; style globalne z prefiksem klas."),
    ("ADR-09", "Kontrakt selektorów: ta sama wtyczka na makietach i prawdziwych stronach", A,
     "Demo musi działać bez internetu, a wtyczka ma też działać na prawdziwych serwisach.",
     "Makiety platform (demo/platforms/) odtwarzają prawdziwe punkty zaczepienia DOM opisane w SELECTORS.md. Wtyczka zna tylko kontrakt selektorów i nie zależy od konkretnej strony.",
     "Jeden kod na demo i produkcję; testy wtyczki na makietach. " + risk("selektory platform się zmieniają; kontrakt trzeba aktualizować i testować."),
     "Osobny tryb demo we wtyczce; nagrane strony bez wtyczki."),
    ("ADR-10", "Serwer MCP (FastMCP) nad tym samym silnikiem", A,
     "Redakcje, uczelnie i analitycy chcą korzystać z weryfikacji bez instalowania wtyczki, często z poziomu asystentów AI.",
     "FastMCP wystawia narzędzia jako kolejny adapter wejściowy obok FastAPI, nad tymi samymi portami domen. Na hackathonie dwa narzędzia: domena a kampania, notatki dla posta lub adresu.",
     "Logika nie jest powielana; odpowiedzi MCP używają tych samych kontraktów i źródeł. " + risk("nadużycia publicznego dostępu; potrzebne klucze i limity (US-API-03)."),
     "Tylko REST API; osobny serwis MCP z własną logiką."),
    ("ADR-11", "Pydantic AI ze strukturalnym wyjściem; AI tylko szkicuje", PR,
     "AI ma pisać szkic notatki i ostrzeżenia, ale nie może decydować o publikacji ani zmyślać źródeł.",
     "Agent Pydantic AI zwraca wynik w typie kontraktu (szkic NoteCard lub ScamWarningCard), walidowany jak każde inne wejście. Krok szkicu jest krokiem workflow DBOS; publikacja zależy wyłącznie od konsensusu.",
     "Model LLM można wymienić bez zmiany domeny; odrzucone szkice są ponawiane. " + risk("halucynowane źródła; każdy link sprawdzamy (czy istnieje) przed głosowaniem."),
     "Wolny tekst z LLM parsowany ręcznie; wybór modelu wpisany na sztywno w domenie."),
    ("ADR-12", "GCP i Cloudflare", "Przyjęta (dostawcy), podział ról proponowany",
     "Potrzebujemy obliczeń i magazynu dla backendu oraz szybkiej, chronionej warstwy brzegowej dla panelu i API.",
     "GCP: maszyny runnerów CI i magazyn obiektów na dowody. Cloudflare: DNS, TLS i ochrona przed nadużyciami przed API oraz hosting statycznego panelu. Backend, workery DBOS i PostgreSQL działają na własnym serwerze ARM64 (ADR-13).",
     "Brzeg sieci obsługuje Cloudflare, a obliczenia GCP i serwer on-prem. " + risk("dwóch dostawców to dwa zestawy uprawnień i kosztów; sekrety tylko w ustawieniach repozytorium."),
     "Wszystko w jednej chmurze; hosting zarządzany (np. Cloud Run) dla backendu."),
    ("ADR-13", "Self-hosted runnery GitHub Actions: 3 × GCP x64 i 1 × ARM64 on-prem", A,
     "CI potrzebuje mocy do buildów i testów, a backend ma działać na serwerze ARM64 z GPU.",
     "Trzy runnery organizacji na GCP (etykieta meritum) do buildów i testów; runner dellpromaxgb10 (ARM64, etykiety backend, gpu) wdraża backend, workery DBOS i PostgreSQL z pgvector. Obrazy budujemy dla linux/arm64.",
     "Szybkie buildy bez limitów minut i wdrożenie tam, gdzie działa backend. " + risk("host on-prem dzielimy z runnerem innego projektu; nie czyścimy globalnie obrazów Dockera ani nie zajmujemy jego portów."),
     "Runnery hostowane przez GitHub; ręczne wdrożenia przez SSH."),
    ("ADR-14", "Panel: React, TanStack Router + Query, shadcn/ui, Tailwind v4; jakość wymuszana narzędziami", A,
     "Panel analityka i komponenty wtyczki muszą powstać szybko, wyglądać spójnie z design systemem i nie gubić jakości pod presją czasu.",
     "Panel w React z TanStack Router (typowane trasy, filtry w URL) i TanStack Query (cache, odpytywanie statusu), komponenty shadcn/ui i shadcnblocks, tokeny Meritum w Tailwind v4. Jakość: Biome strict (frontend), Ruff i Ty strict (Python), TDD, pytestarch dla architektury, behave dla zachowań.",
     "Te same tokeny i komponenty w panelu, wtyczce i makietach; błędy typów łapane przed demo. " + risk("ścisłe reguły spowalniają pierwsze godziny; wyłączenia tylko z komentarzem."),
     "Next.js; React Router; ESLint i Prettier; mypy."),
]
parts += [
    h(2, "4. Decyzje architektoniczne (ADR)"),
    p(
        "Status <strong>Przyjęta</strong> oznacza decyzję już podjętą przez zespół (stos technologiczny, zasady produktu). "
        "<strong>Proponowana</strong> to propozycja do przeglądu."
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
