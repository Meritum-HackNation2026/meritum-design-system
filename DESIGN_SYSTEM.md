# Meritum: Design System

**Meritum — obywatelski radar dezinformacji oraz scamu.**

Ten dokument opisuje, jak Meritum wygląda i jak mówi. Przekaż go agentowi AI, który robi slajdy, makiety albo materiały marketingowe, razem z poleceniem z sekcji 12. Wszystkie wartości są ostateczne, chyba że ten plik powie inaczej.

---

## 1. Idea w jednym akapicie

Meritum to niezależna warstwa zaufania nad mediami społecznościowymi. Z jednego zgłoszenia odsłania całą kampanię oszustów lub manipulatorów, a kontekst publikuje dopiero wtedy, gdy zgodzą się ludzie, którzy zwykle się nie zgadzają. Wygląd łączy precyzję narzędzi dla analityków (Linear, Vercel) z powagą dziennikarstwa śledczego (The Economist, Bellingcat). Metafora przewodnia to **biuletyn synoptyczny**: zwykle jest spokojnie, a atak botów albo kampania oszustów nadciąga jak front na mapie pogody.

**Hasła:** „Jeden fejk, cała kampania. Jeden kontekst, ponad podziałami.” oraz „AI pisze. Ludzie decydują. Źródła są obowiązkowe.”

---

## 2. Logo

Znak **„Dwa łuki”**: małe „m” z dwóch łuków. Łuki to dwie strony sporu, wspólny środkowy trzon (w kolorze akcentu) to zgoda, a kropka nad nim to punkt, w którym się spotykają.

| Plik | Kiedy używać |
|---|---|
| `brand/meritum-mark.svg` | na jasnym tle |
| `brand/meritum-mark-on-dark.svg` | na ciemnym tle |
| `brand/meritum-mark-mono.svg` | druk jednobarwny, grawer, pieczątka |
| `brand/meritum-app-icon.svg` | ikona wtyczki, favicon, avatar w social media |

**Logotyp:** znak + słowo „meritum” małymi literami, krój Archivo, grubość 650, szerokość 112%, światło −0,02 em. Pod spodem opcjonalny podtytuł „obywatelski radar dezinformacji oraz scamu” w Archivo 400, kolor drugorzędny.

**Zasady:**
- Minimalny rozmiar znaku: 14 px na ekranie, 6 mm w druku.
- Pole ochronne: wysokość kropki nad „m” z każdej strony.
- Trzon i kropka zawsze w kolorze akcentu (`#1D6A86` jasno, `#5DB3CF` ciemno). Łuki w kolorze tekstu.
- W widżecie na platformach znak ma 14 px i stoi przed słowem „Meritum” w małym nagłówku.

**Nie wolno:** obracać znaku, dodawać cienia ani gradientu, zmieniać koloru trzonu na inny niż akcent, umieszczać znaku obok logotypów platform tak, jakby był ich częścią, ani rozciągać go.

---

## 3. Kolory

Jedno tło, jeden atrament, jeden akcent. Czerwień pojawia się wyłącznie tam, gdzie jest zagrożenie.

### Baza

| Rola | Jasny | Ciemny | Do czego |
|---|---|---|---|
| Tło aplikacji | `#F6F7F5` | `#0B0F12` | tło panelu i slajdów |
| Karta | `#FFFFFF` | `#0B0F12` | karty, widżety, okienka |
| Atrament | `#14191E` | `#E7ECEE` | cały tekst główny, przycisk główny |
| Tekst drugorzędny | `#4C5862` | `#9AA6AE` | podpisy, etykiety, domeny źródeł |
| Obramowanie | `#D9DEDD` | `#2F3336` | 1 px wokół kart, linie tabel |
| Podniesione tło | `#E8ECEB` | `#22282C` | aktywna zakładka nawigacji, tor paska |

### Stany (semantyka)

| Stan | Kolor | Tło plakietki | Tekst plakietki | Kiedy |
|---|---|---|---|---|
| **Zweryfikowany kontekst** | `#1D6A86` / `#5DB3CF` | `#E1EDF2` / `#123441` | `#13506A` / `#9FD8EC` | opublikowana notatka, linki, paski zgody |
| **W ocenie / sporne** | `#B7791F` / `#F2C46D` | `#F8EEDB` / `#3A2C10` | `#7A4E08` / `#F2C46D` | notatka czeka na zgodę obu grup |
| **Oszustwo / atak botów / anomalia** | `#C8213A` / `#FF6B7D` | `#FBE6E9` / `#43161D` | `#9E1A2E` / `#FFB3BE` | fałszywa reklama, atak na notatkę, odrzucone konta |

Pierwsza wartość dotyczy trybu jasnego, druga ciemnego. Wszystkie pary tekst/tło mają kontrast co najmniej 4,5:1 (sprawdzone: 5,6–17,7:1).

**Zasady koloru:**
- Stan nigdy nie jest oznaczony samym kolorem: zawsze ma też słowo („Zweryfikowany”, „Oszustwo”) albo znak (front z trójkątami przy ataku).
- Na wykresach jest co najwyżej 4 kolory: atrament (realne osoby), czerwień (odrzucone), akcent i szary dla przeszłości.
- Przycisk główny jest prawie czarny (`#14191E`), nigdy w kolorze akcentu.

**Zakazane:** gradienty fioletowo-niebieskie (i w ogóle gradienty), zielony tekst na czarnym tle w stylu „hakerskim”, neonowe poświaty, granat z czerwienią w stylu urzędowym, kremowe tło z terakotą.

---

## 4. Typografia

| Krój | Rola | Źródło |
|---|---|---|
| **Archivo** (wagi 400–800, szerokość 75–125) | cały interfejs, notatki, slajdy, logotyp | Google Fonts |
| **Azeret Mono** (400–600) | wyłącznie dane: ID notatek i kampanii (#K-118), nazwy kont (@pl_patriot_88231), domeny w tabelach, godziny, liczby w metrykach | Google Fonts |

Oba kroje mają polskie znaki. Mono nigdy nie służy do dekoracji, etykiet ani nagłówków.

### Skala

| Styl | Rozmiar / interlinia | Grubość | Gdzie |
|---|---|---|---|
| Display | 40 px / 1,05 | 700, szerokość 108% | tylko slajdy |
| Tytuł | 22 px / 28 px | 700 | nagłówek ekranu panelu |
| Tytuł karty | 15 px | 700 | „Kontekst od społeczności” |
| Tekst | 15 px / 22 px | 400 | treść notatki |
| Mały | 13 px / 20 px | 400–600 | źródła, podpisy |
| Meta | 12 px / 16 px | 600 | nagłówek widżetu „Meritum”, osie wykresu |

Nic poniżej 12 px. Nagłówki zdaniowe (wielka litera tylko na początku), bez rozstrzelonych WERSALIKÓW, bez etykiet nad nagłówkami.

**W widżecie na platformie** treść notatki dziedziczy krój platformy (np. systemowy na X, Reddit Sans na Reddicie). Archivo zostaje tylko w nagłówku „Meritum” i tytule karty.

---

## 5. Odstępy, siatka, kształty

- **Siatka 4 px.** Typowe odstępy: 4, 6, 8, 12, 14, 16, 24 px.
- **Wnętrze kart:** 14 px w poziomie, 12 px u góry, 14 px na dole.
- **Panel analityka:** marginesy 24 px, odstęp między blokami 12–16 px.
- **Promienie:** karty 12 px (w widżecie zgodnie z platformą: X 16, Facebook 8, Instagram 0, Reddit 16, TikTok 8), okienka 14 px, przyciski i plakietki w pełni zaokrąglone (pigułki), pola formularzy 10 px.
- **Głębia:** karty leżą płasko, mają obramowanie 1 px i nie mają cienia. Cień dostaje tylko to, co się unosi: okienko zgłoszenia, podpowiedź (tooltip), powiadomienie.
- **Zakazane:** pasek koloru wzdłuż jednego boku karty, siatki identycznych kart z ikoną na górze, szkło i rozmycie tła, ozdobne kształty.

---

## 6. Komponenty

Kod React (shadcn/ui, Tailwind v4) leży w `components/meritum/`. Interaktywne makiety wszystkich stanów: `demo/widgets/`, pełny przepływ na makiecie X: `demo/x/`.

### 6.1 Przycisk „Zgłoś” (wstrzykiwany)
Znak Meritum 18 px + słowo „Zgłoś” w pasku akcji posta, obok zakładki. Stany: spoczynek (kolor ikon platformy), najechanie (tło `#E1EDF2`, tekst `#13506A`), otwarty, „Zgłoszono” (po wysłaniu, nieaktywny).

### 6.2 Okienko szybkiego zgłoszenia (Quick Report Popover)
Szerokość 356 px, unosi się pod przyciskiem, wyrównane do prawej.
1. Nagłówek: znak, „Zgłoś treść”, „Post @nazwa”, zamknięcie.
2. Przełącznik **Manipulacja / Oszustwo** (reklamy sponsorowane otwierają się na „Oszustwo”).
3. Powody jako pigułki do zaznaczenia, można kilka.
4. „Albo opisz własnymi słowami” (pole tekstowe).
5. „Link do źródła (opcjonalnie)”.
6. Informacja: dowód zapisujemy sami (zrzut, adres, czas), zgłoszenie jest anonimowe.
7. „Wyślij zgłoszenie”: aktywny, gdy wybrano powód lub wpisano co najmniej 3 znaki. Wysyłanie: pasek wypełnia przycisk w ~0,9 s, napis „Wysyłanie…”, potem „Wysłane” i okienko się zamyka.

Błąd: „Nie udało się wysłać. Sprawdź połączenie i spróbuj ponownie; twoje odpowiedzi zostały w formularzu.”

### 6.3 Pasek analizy
Pojawia się pod postem po wysłaniu. Trzy kroki z kółkiem: czeka, kręci się, gotowe. Przykłady: „Łączymy z 56 podobnymi zgłoszeniami”, „Zbieramy źródła: NASA, ESA i 4 media”, „AI pisze szkic, oceniają dwie grupy”.

### 6.4 Karta kontekstu (Injected Context Card)
Wstrzykiwana pod post. Białe tło, obramowanie 1 px, promień platformy.
- **Nagłówek:** znak 14 px + „Meritum” + link „Dlaczego to widzę?” (podpowiedź: jak powstała notatka).
- **Tytuł i plakietka stanu:** „Kontekst od społeczności” + „Zweryfikowany” / „W ocenie”, albo „Fałszywa reklama” + „Oszustwo”.
- **Treść:** 1–3 zdania, bez oceniania autora.
- **Wiersze:** Źródło (obowiązkowe, minimum jedno, każde z domeną i typem: akt prawny, instytucja, media, encyklopedia), Kampania (tylko oszustwo), Dowód (tylko oszustwo), Technika (nazwa techniki + podpowiedź „jak rozpoznać?”).
- **Zgoda perspektyw (tylko notatka):** dwa paski rosnące od środkowej osi, kreska progu 70% na każdym, podpis „Grupa A: 88% pomocne, 231 ocen”.
- **Akcje:** notatka: „Pomocne”, „Niepomocne”; oszustwo: „Ukryj reklamę”, „Zgłoś platformie”, „To pomyłka?”.
- **Pojawienie się:** karta rozwija się z wysokości 0 i unosi o 8 px w 0,5 s; paski zgody rosną po 0,45 s.

### 6.5 Telemetria obrony przed botami (Live Dashboard)
- **Tytuł odpowiada na jedno pytanie:** „Atak odparty, notatka bez zmian”, ze znakiem frontu (linia z trzema trójkątami).
- **Wykres liniowy głosów na minutę:** atrament = liczone (realne osoby), czerwień = odrzucone (klaster). Okno ataku zaznaczone jasnoczerwonym tłem, początek pionową linią „front 14:32”. Etykiety bezpośrednio przy liniach, bez legendy.
- **Suma, która się domyka:** „Oddane 6 016 = liczone 1 204 + odrzucone 4 812”.
- **Tabela odrzuconych kont:** czas, przekreślona nazwa konta w mono, powód słowami („ten sam klaster”, „rytm 1 głos/s”, „konto ma 2 dni”). Nowe wiersze wjeżdżają od góry.
- **Bez kafelków KPI z ikonami** i bez różowych banerów.

### 6.6 Widok kampanii (dla konkursu NASK)
Oś czasu rotacji domen: każda domena to wiersz, pasek pokazuje, kiedy działała. Martwe domeny szare, aktywne czerwone, przewidziane z logów certyfikatów przerywane (jedna zapala się na żywo). Pod spodem suma „Reklamy 47 = Facebook 31 + Instagram 12 + X 4” i tabela „Wspólny ślad”.

---

## 7. Widżet na pięciu platformach

**Zasada: rama od gospodarza, sygnał od Meritum.**

| Od platformy bierzemy | Meritum zostawia zawsze |
|---|---|
| krój pisma i jego rozmiar, promień narożników, tło i obramowanie karty, kształt przycisków, kolor linków | znak i słowo „Meritum” w nagłówku, kolory stanów, pasek zgody dwóch grup, obowiązkowe źródła |

Nigdy nie wstawiamy logotypu platformy do widżetu i nigdy nie udajemy treści platformy. Szczegóły skórek: `demo/widgets/` i zmienne `[data-host]` w `tokens/meritum.css`.

---

## 8. Ton komunikacji

**Mówimy jak dobry redaktor: spokojnie, konkretnie, ze źródłem.**

1. **Kontekst, nie wyrok.** Opisujemy fakty, a nie ludzi. Nigdy „kłamca”, „idiota”, „fake news!”.
2. **Najpierw ochrona, potem wyjaśnienie** (przy oszustwie): najpierw „Nie podawaj tam żadnych danych”, potem dlaczego.
3. **Każde twierdzenie ma źródło.** Bez źródła nie publikujemy.
4. **Nazywamy technikę**, żeby czytelnik nauczył się ją rozpoznawać.
5. **Prosto i krótko:** strona czynna, zdania do ~20 słów, bez żargonu, bez wykrzykników, bez emoji.
6. **Liczby uczciwie:** w demo zawsze z dopiskiem „dane symulowane”.

| Zamiast | Piszemy |
|---|---|
| „FAŁSZ! Ten post kłamie!” | „Żaden przepis nie zakazuje płacenia gotówką w sklepach.” |
| „Uwaga, scam!!!” | „Fałszywa reklama. Wizerunek użyto bez zgody. Nie podawaj tam żadnych danych.” |
| „Submit” / „OK” | „Wyślij zgłoszenie”, „Ukryj reklamę” |
| „Wystąpił błąd” | „Nie udało się wysłać. Sprawdź połączenie i spróbuj ponownie.” |
| „Nasz zaawansowany algorytm AI wykrył…” | „Szkic AI z uwag 57 osób. O publikacji zdecydowali ludzie.” |

---

## 9. Ruch

- Ruch tylko jako odpowiedź na działanie użytkownika albo pokazanie zmiany danych.
- Krzywa `cubic-bezier(0.16, 1, 0.3, 1)` (szybki start, miękkie wyhamowanie), czas 150–550 ms.
- Animujemy przezroczystość, przesunięcie i skalę; wyjątek to rozwijanie karty (wysokość od 0).
- Bez pulsujących kropek, bez animacji w pętli (poza kółkiem „w toku”).
- Przy włączonym „ogranicz ruch” w systemie wszystkie animacje skracają się do zera.

---

## 10. Dostępność

WCAG 2.2 AA w obu trybach, także na tle cudzych feedów. Stany oznaczone słowem lub znakiem, nie tylko kolorem. Widoczny pierścień fokusu (2 px, kolor akcentu). Klawisz Esc zamyka okienko i oddaje fokus przyciskowi. Polskie teksty są dłuższe niż angielskie, więc komponenty muszą wytrzymać długie etykiety.

---

## 11. Slajdy i materiały marketingowe

- Tło slajdu `#F6F7F5` albo `#0B0F12` (jeden tryb na całą prezentację).
- Jedna myśl na slajd, tytuł do 2 linii, Display 40 px lub większy.
- Zamiast zdjęć stockowych: prawdziwe zrzuty interfejsu Meritum (makiety z `demo/`) w dużej skali.
- Wykresy według zasad z sekcji 6.5: etykiety przy liniach, suma, która się domyka, czerwień tylko dla ataku.
- Logo w lewym górnym albo dolnym rogu, 24–32 px.
- Prawdziwe osoby i firmy nigdy nie są pokazywane jako oszuści; w przykładach używamy fikcyjnego prezentera „Tomasz Rewiński” i fikcyjnych domen.
- Nie piszemy o współpracy z NASK, CERT Polska, MSZ ani mediami, dopóki jej nie ma; piszemy „gotowe do integracji z…”.

---

## 12. Polecenie dla agenta AI (kopiuj i wklej)

```
Projektujesz materiał dla Meritum — obywatelskiego radaru dezinformacji oraz scamu
(wtyczka do przeglądarki + panel analityka). Trzymaj się DESIGN_SYSTEM.md.

Styl: „Biuletyn synoptyczny”: precyzja narzędzi dla analityków i powaga dziennikarstwa
śledczego. Spokojnie, czysto, dużo powietrza, płaskie białe karty z obramowaniem 1 px.
Kolory: tło #F6F7F5, karty #FFFFFF, tekst #14191E, tekst drugorzędny #4C5862,
obramowanie #D9DEDD, akcent/zweryfikowany #1D6A86, sporne #B7791F,
oszustwo i atak #C8213A (tylko tam, gdzie jest zagrożenie).
Kroje: Archivo (wszystko), Azeret Mono (tylko ID, nazwy kont, domeny, godziny, liczby).
Logo: brand/meritum-mark.svg (małe „m” z dwóch łuków, trzon i kropka w kolorze #1D6A86).
Przyciski: pigułki, główny prawie czarny. Cień tylko na elementach unoszących się.
Ton: kontekst, nie wyrok; każde twierdzenie ze źródłem; zdania proste, bez wykrzykników i emoji.
Zakazane: gradienty, fiolet, neon, zielony tekst na czarnym, styl urzędowy, kafelki z ikonami,
pasek koloru z boku karty, etykiety WERSALIKAMI nad nagłówkami, prawdziwe osoby jako oszuści,
wymyślone statystyki bez dopisku „dane symulowane”.
```

---

## 13. Pliki

| Ścieżka | Zawartość |
|---|---|
| `tokens/meritum.css` | tokeny CSS i `@theme` dla Tailwind v4 + shadcn/ui, tryb ciemny, skórki platform |
| `components/meritum/` | komponenty React: `ContextCard`, `QuickReportPopover`, `AnalysisSteps`, `BotDefenseTelemetry`, `MeritumMark` |
| `brand/` | logo w SVG |
| `demo/x/` | interaktywne demo na makiecie X |
| `demo/widgets/` | widżet na 5 platformach i wszystkie jego stany |
| `demo/logo/` | warianty znaku (wybrany: B) |
| `demo/platforms/` | makiety pięciu platform do pokazu na żywo (w przygotowaniu) |
| `PRODUCT.md`, `KEY_SELLING_POINTS.md` | produkt i strategia na oba konkursy |
