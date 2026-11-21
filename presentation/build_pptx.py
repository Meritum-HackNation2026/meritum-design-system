"""Builds presentation/meritum-template.pptx: the same 12 slides as slides/index.html (MSZ „Prawdowid” deck).

  uv run --with python-pptx python presentation/build_pptx.py

Coordinates are written in the HTML deck's 1920x1080 px grid and converted to EMU.
Slide titles and presenter notes are read from slides/index.html, so the two decks cannot drift apart.
Fonts: Archivo (text) and Azeret Mono (data). Without them installed PowerPoint
substitutes a default sans; Google Slides has both in its font list.
"""
import html
import re
import struct
from pathlib import Path

from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_CONNECTOR, MSO_SHAPE
from pptx.enum.text import MSO_ANCHOR, PP_ALIGN
from pptx.oxml.ns import qn
from pptx.util import Emu, Pt

HERE = Path(__file__).resolve().parent
EXP = HERE.parent / "brand" / "exports"
SHOTS = HERE / "screenshots"
PHOTOS = HERE / "photos"
ICONS = HERE / "icons" / "png"  # made by `render.py icons`

BG, CARD, INK, INK2, LINE, RAISED = "F6F7F5", "FFFFFF", "14191E", "4C5862", "D9DEDD", "E8ECEB"
SEA, SEA_T, SEA_D = "1D6A86", "E1EDF2", "13506A"
AMBER, AMBER_T, AMBER_D = "B7791F", "F8EEDB", "7A4E08"
RED, RED_T, RED_D, GREY = "C8213A", "FBE6E9", "9E1A2E", "A9B3B8"
SANS, MONO = "Archivo", "Azeret Mono"


def px(v):
    return Emu(int(v * 6350))  # 12192000 EMU / 1920 px


def pt(v):
    return Pt(v * 0.75)  # CSS px -> pt at 96 dpi


def rgb(h):
    return RGBColor.from_string(h)


prs = Presentation()
prs.slide_width, prs.slide_height = px(1920), px(1080)
BLANK = prs.slide_layouts[6]


def text(slide, x, y, w, h, runs, size=28, color=INK, bold=False, font=SANS, align=PP_ALIGN.LEFT,
         anchor=MSO_ANCHOR.TOP, spacing=1.25):
    """runs: a string, or a list of paragraphs, each a string or a list of (text, overrides) runs."""
    tb = slide.shapes.add_textbox(px(x), px(y), px(w), px(h))
    tf = tb.text_frame
    tf.word_wrap = True
    tf.vertical_anchor = anchor
    tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
    paras = [runs] if isinstance(runs, str) else runs
    for i, para in enumerate(paras):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.alignment = align
        p.line_spacing = spacing
        for t, o in ([(para, {})] if isinstance(para, str) else para):
            r = p.add_run()
            r.text = t
            f = r.font
            f.name = o.get("font", font)
            f.size = pt(o.get("size", size))
            f.bold = o.get("bold", bold)
            f.color.rgb = rgb(o.get("color", color))
            f.strike = None
            if o.get("strike"):
                r._r.get_or_add_rPr().set("strike", "sngStrike")
    return tb


def box(slide, x, y, w, h, fill=CARD, line=LINE, radius=12, weight=1, dash=False):
    shp = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE if radius else MSO_SHAPE.RECTANGLE, px(x), px(y), px(w), px(h))
    if radius:
        shp.adjustments[0] = min(0.5, radius / min(w, h))
    if fill:
        shp.fill.solid()
        shp.fill.fore_color.rgb = rgb(fill)
    else:
        shp.fill.background()
    if line:
        shp.line.color.rgb = rgb(line)
        shp.line.width = pt(weight)
        if dash:
            shp.line.dash_style = 4  # MSO_LINE.DASH
    else:
        shp.line.fill.background()
    shp.shadow.inherit = False
    return shp


def hline(slide, x, y, w, color=LINE, weight=1):
    c = slide.shapes.add_connector(MSO_CONNECTOR.STRAIGHT, px(x), px(y), px(x + w), px(y))
    c.line.color.rgb = rgb(color)
    c.line.width = pt(weight)
    return c


def pill(slide, x, y, label, fill, color, w=None):
    w = w or 24 + len(label) * 12
    b = box(slide, x, y, w, 40, fill=fill, line=None, radius=20)
    tf = b.text_frame
    tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
    p = tf.paragraphs[0]
    p.alignment = PP_ALIGN.CENTER
    r = p.add_run()
    r.text = label
    r.font.name, r.font.size, r.font.bold, r.font.color.rgb = SANS, pt(22), True, rgb(color)
    return b


def image(slide, path, x, y, w=None, h=None):
    return slide.shapes.add_picture(str(path), px(x), px(y), px(w) if w else None, px(h) if h else None)


def new_slide(n, total, notes, footer=True, num_x=1592):
    s = prs.slides.add_slide(BLANK)
    s.background.fill.solid()
    s.background.fill.fore_color.rgb = rgb(BG)
    if footer:
        image(s, EXP / "meritum-mark-light-512.png", 124, 1000, 36, 36)
        text(s, 166, 1004, 300, 32, "meritum", size=24, bold=True)
        text(s, num_x, 1006, 200, 30, f"{n} / {total}", size=20, color=INK2, align=PP_ALIGN.RIGHT, font=MONO)
    s.notes_slide.notes_text_frame.text = notes
    return s


def title(s, t, y=112, w=1500, size=72):
    return text(s, 128, y, w, 180, t, size=size, bold=True, spacing=1.05)




def _plain(fragment):
    return re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", "", fragment))).strip()


SECTIONS = re.findall(r'<section class="slide.*?</section>', (HERE / "slides" / "index.html").read_text(), re.S)
TITLES = [_plain(re.search(r"<h[12][^>]*>(.*?)</h[12]>", sec, re.S).group(1)) for sec in SECTIONS]
NOTES = [_plain(re.search(r"<aside>(.*?)</aside>", sec, re.S).group(1)) for sec in SECTIONS]
TOTAL = len(SECTIONS)
assert TOTAL <= 12, f"MSZ brief allows at most 12 slides, the HTML deck has {TOTAL}"


def _size(path):
    return struct.unpack(">II", path.read_bytes()[16:24]) if path.suffix == ".png" else _jpeg_size(path)


def _jpeg_size(path):
    b = path.read_bytes()
    i = 2
    while i < len(b):
        marker, length = b[i + 1], int.from_bytes(b[i + 2:i + 4], "big")
        if marker in (0xC0, 0xC1, 0xC2):
            return int.from_bytes(b[i + 7:i + 9], "big"), int.from_bytes(b[i + 5:i + 7], "big")
        i += 2 + length
    raise ValueError(f"no JPEG size in {path}")


def shot(s, name, x, y, w, h=None):
    """Screenshot at width w; with h, cut off at the bottom like the HTML .crop boxes."""
    path = SHOTS / name
    pw, ph = _size(path)
    full = w * ph / pw
    pic = image(s, path, x, y, w=w, h=min(h, full) if h else None)
    if h and h < full:
        pic.crop_bottom = 1 - h / full
    pic.line.color.rgb = rgb(LINE)
    pic.line.width = pt(1)
    return pic


def photo(s, name, x, y, w, h, fy=0.5):
    """A photograph filling the box like CSS object-fit: cover; fy is the vertical focus (object-position)."""
    path = PHOTOS / name
    pw, ph = _size(path)
    pic = image(s, path, x, y, w=w, h=h)
    if pw / ph > w / h:  # wider than the box: trim the sides
        cut = 1 - (w / h) / (pw / ph)
        pic.crop_left = pic.crop_right = cut / 2
    else:
        cut = 1 - (pw / ph) / (w / h)
        pic.crop_top, pic.crop_bottom = cut * fy, cut * (1 - fy)
    return pic


def icon(s, name, x, y, size=32, white=False):
    return image(s, ICONS / f"{name}{'-white' if white else ''}.png", x, y, size, size)


def cap(s, x, y, w, t):
    return text(s, x, y, w, 60, t, size=20, color=INK2, spacing=1.35)


def points(s, x, y, w, items, gap=110, size=28, sub=24, rule=LINE, subcolor=INK2, lines=1):
    """Icon + bold line + grey line, separated by hairlines (the HTML .pts list)."""
    for ic, b, t in items:
        hline(s, x, y, w, color=rule)
        icon(s, ic, x, y + 24)
        text(s, x + 52, y + 18, w - 52, 40 * lines, b, size=size, bold=True, spacing=1.2)
        text(s, x + 52, y + 18 + size * 1.3 * lines + 6, w - 52, 70, t, size=sub, color=subcolor, spacing=1.35)
        y += gap
    hline(s, x, y, w, color=rule)


def slide(i, footer=True, title_w=1500, **kw):
    s = new_slide(i + 1, TOTAL, NOTES[i], footer=footer, **kw)
    if footer:
        title(s, TITLES[i], size=64, w=title_w)
    return s


EXAMPLE = "Przykład do pokazu, cytaty ilustracyjne."
TINT_RULE = "C4D9E2"

# 1. Tytuł
s = slide(0, footer=False)
photo(s, "bus-night.jpg", 1120, 0, 800, 1080)
image(s, EXP / "meritum-lockup-subtitle-light@2x.png", 128, 168, w=420)
text(s, 128, 380, 780, 220, TITLES[0], size=88, bold=True, spacing=1.05)
text(s, 128, 600, 700, 180, "Wklejasz tekst albo link, a Meritum sprawdza każde twierdzenie w opisanych źródłach, "
     "cytuje dosłowny fragment i mówi wprost, gdy dowodów brakuje.", size=30, color=INK2, spacing=1.4)
shot(s, "x-02-card.png", 930, 200, 500, 660)
text(s, 128, 1000, 760, 32, "HackNation 2026, konkurs MSZ „Prawdowid”. Karta to przykład do pokazu, cytaty ilustracyjne.", size=20, color=INK2)

# 2. Problem
s = slide(1, num_x=992, title_w=1100)
photo(s, "commuters-phones.jpg", 1320, 0, 600, 1080)
y = 320
for ic, a, b in [("smartphone", "Pogłoska dociera kanałem, którego używa obywatel", "post, wiadomość, link od znajomego; sprawdzenie wymaga wyjścia z tego kanału"),
                 ("clock-3", "Sprawdzenie wymaga wiedzy i czasu", "trzeba wiedzieć, które źródło jest wiarygodne, i znaleźć w nim właściwy fragment"),
                 ("triangle-alert", "Czat AI odpowiada płynnie, ale bez źródła", "płynny język nie gwarantuje poprawności, a wymyślony cytat wygląda jak prawdziwy")]:
    hline(s, 128, y, 1100)
    icon(s, ic, 128, y + 30)
    text(s, 200, y + 26, 450, 90, a, size=28, bold=True)
    text(s, 690, y + 26, 530, 90, b, size=26, color=INK2)
    y += 132
hline(s, 128, y, 1100)
icon(s, "message-circle", 128, y + 62, 40)
text(s, 200, y + 52, 1020, 60, "„Od stycznia nie zapłacisz w sklepie gotówką”", size=36, bold=True)
text(s, 200, y + 110, 1020, 40, "Pogłoska z naszego pokazu: krąży w wiadomościach, a obowiązujące przepisy mówią co innego.", size=22, color=INK2)

# 3. Użytkownicy
s = slide(2)
photo(s, "reader-phone.jpg", 128, 300, 480, 680)
for x, ic, head, items in (
    (672, "user-round", "Obywatel", [("smartphone", "Bez instalacji i bez konta", "formularz działa na telefonie, przycisk „Sprawdź” pod postem to opcja"),
                                      ("accessibility", "Prosty język", "także dla osób o niskich kompetencjach cyfrowych, WCAG 2.2 AA"),
                                      ("scan-search", "Uczy rozpoznawania", "odpowiedź nazywa technikę manipulacji i mówi, jak ją rozpoznać")]),
    (1256, "users", "Moderator lub analityk", [("list-filter", "Sprawy bez odpowiedzi", "twierdzenia z werdyktem „brak wystarczających dowodów” w tematach wysokiego ryzyka"),
                                                ("git-compare-arrows", "Podobne twierdzenia w jednej sprawie", "powtórzenia łączą się, zamiast zalewać kolejkę"),
                                                ("gauge", "Jakość pod kontrolą", "wstrzymania, próby wstrzyknięcia poleceń, czas odpowiedzi, koszt")])):
    icon(s, ic, x, 304, 40)
    text(s, x + 54, 302, 480, 44, head, size=32, bold=True)
    points(s, x, 370, 536, items, gap=190, size=26, sub=23)

# 4. Jak to działa
s = slide(3)
hline(s, 128, 370, 1664, color=INK, weight=2)
for k, (ic, b, t) in enumerate([("clipboard-paste", "Wklejasz tekst albo link", "na stronie albo przyciskiem „Sprawdź” pod postem"),
                                ("list-checks", "Wyodrębniamy twierdzenia", "fakty oddzielamy od opinii, dane osobowe maskujemy"),
                                ("search", "Szukamy w katalogu", "baza źródeł, świeże publikacje z zatwierdzonych serwisów, fact-checkerzy"),
                                ("quote", "Werdykt z cytatem", "cytat przechodzi, tylko gdy fragment występuje w źródle dosłownie")]):
    x = 128 + k * 416
    last = k == 3
    box(s, x, 330, 80, 80, fill=SEA if last else BG, line=SEA if last else INK, radius=40, weight=2)
    icon(s, ic, x + 22, 352, 36, white=last)
    text(s, x, 440, 370, 100, b, size=34, bold=True, spacing=1.1)
    text(s, x, 546, 370, 120, t, size=24, color=INK2, spacing=1.35)
text(s, 128, 724, 240, 40, "Pięć werdyktów:", size=24, color=INK2)
x = 330
for label, fill, color in (("Potwierdzone", SEA_T, SEA_D), ("Fałszywe", RED_T, RED_D), ("Wprowadzające w błąd", AMBER_T, AMBER_D),
                           ("Brak wystarczających dowodów", RAISED, INK2), ("Nie podlega weryfikacji", RAISED, INK2)):
    w = 32 + len(label) * 12
    pill(s, x, 720, label, fill, color, w=w)
    x += w + 12
box(s, 128, 800, 1664, 120, fill=SEA_T, line=None)
icon(s, "scale", 160, 826)
text(s, 212, 822, 1540, 90, [[("Siła podstawy liczona regułą, nie przez model. ", {"bold": True, "color": INK}),
     ("Mocna: co najmniej 2 niezależnych wydawców zgodnych z werdyktem, w tym urzędowy, i świeże dowody. "
      "Umiarkowana: 2 wydawców albo 1 urzędowy. Słaba: jeden nieurzędowy albo dowód archiwalny.", {})]], size=24, color=SEA_D, spacing=1.4)

# 5. Formularz WWW
s = slide(4)
shot(s, "web-01-form.png", 128, 300, 1040)
points(s, 128, 840, 1040, [("globe", "Kanał podstawowy, bez konta", "teksty z copy/pl.json; dane osobowe maskujemy przed analizą")])
shot(s, "widgets-01-steps.png", 1232, 300, 560)
cap(s, 1232, 870, 560, "Pasek analizy. Agenty szukają równolegle, więc kilka kroków trwa naraz. Przykład do pokazu.")

# 6. Pod postem
s = slide(5)
shot(s, "x-02-false.png", 128, 300, 600, 660)
points(s, 808, 300, 984, [("scale", "Werdykt dla twierdzenia, nie dla autora", "„Fałszywe”, z krótkim wyjaśnieniem oznaczonym jako interpretacja AI"),
                          ("quote", "Dosłowny cytat, wydawca, data, link", "fragment sprawdzamy w kodzie, zanim trafi do odpowiedzi"),
                          ("badge-check", "Siła z przesłanek: umiarkowana", "2 niezależnych wydawców, 0 urzędowych, źródła zgodne"),
                          ("scan-search", "Technika i ograniczenia", "„Teoria spiskowa” z podpowiedzią, jak ją rozpoznać; zawsze sekcja „Ograniczenia”")])
cap(s, 808, 760, 984, "Makieta X z demo/live/x/, odpowiedź z atrapy API. " + EXAMPLE)

# 7. Uczciwa niepewność
s = slide(6)
shot(s, "x-03-card.png", 128, 300, 520, 640)
shot(s, "widgets-02-conflict.png", 704, 300, 400, 640)
points(s, 1160, 300, 632, [("scale", "Brak dowodów to werdykt", "z opisem, czego nie ustaliliśmy; kontrakt odrzuca go bez tego opisu"),
                           ("git-compare-arrows", "Sprzeczne źródła obok siebie", "bez siły i bez rozstrzygania za czytelnika"),
                           ("users", "Sprawa dla moderatora", "„przekazano” i „zalecamy przekazanie” to różne komunikaty")], gap=140)
cap(s, 1160, 740, 632, "Po lewej demo/live/x/, w środku demo/widgets/. " + EXAMPLE)

# 8. Prompt injection
s = slide(7)
shot(s, "web-02-injection-input.png", 128, 330, 780)
icon(s, "scissors", 128, 518)
text(s, 176, 510, 480, 44, "Polecenie wycięte, werdykt bez zmian:", size=26, anchor=MSO_ANCHOR.MIDDLE)
pill(s, 640, 512, "Fałszywe", RED_T, RED_D, w=140)
shot(s, "web-03-injection-log.png", 128, 580, 780)
cap(s, 128, 734, 780, "Pole injection_events z kontraktu CheckRecord. Przykład do pokazu.")
box(s, 980, 330, 812, 470, fill=SEA_T, line=None)
points(s, 1016, 342, 740, [("scan-search", "Warstwa kontroli przed każdym wywołaniem modelu", "proxy LLM albo Google Cloud Model Armor, w każdym kroku"),
                           ("scissors", "Polecenie wycinamy, resztę sprawdzamy", "źródło z poleceniem wypada z dowodów"),
                           ("file-check-2", "Strony skanujemy przed użyciem", "katalog przy wczytywaniu, wyniki wyszukiwania w kwarantannie"),
                           ("ban", "Model nie ma narzędzi, które coś zmieniają", "każdą próbę zapisujemy w przebiegu")], size=25, sub=23, rule=TINT_RULE, subcolor=SEA_D)

# 9. Architektura
s = slide(8)
layers = [("Kanały", [("globe", "Formularz WWW", "kanał podstawowy, bez konta"), ("message-circle", "Bot na Discordzie", "drugi kanał, ten sam wynik"),
                      ("puzzle", "Wtyczka „Sprawdź”", "pod postem na 5 platformach, opcja"), ("users", "Panel moderatora", "sprawy, role, jakość")]),
          ("Rdzeń weryfikacji", [("workflow", "Workflow DBOS z kontraktami", "kontrola poleceń, twierdzenia, wyszukiwanie, ocena dowodów, weryfikacja cytatów, "
                                  "odpowiedź. Kontrakty z meritum-core; awaria modelu albo wyszukiwania daje „Problem techniczny”, nigdy werdykt.")]),
          ("Porty i adaptery", [("scale", "Model", "Vertex AI w GCP, wymiana konfiguracją"), ("library", "Korpus", "wyszukiwanie hybrydowe w migawkach katalogu"),
                                ("search", "Wyszukiwarka", "Firecrawl na żywo, tylko domeny z katalogu"), ("badge-check", "Fact-checkerzy", "Google Fact Check Tools API")]),
          ("Zapis i uruchomienie", [("file-check-2", "Zapis przebiegu", "każde sprawdzenie: źródła, modele, region, koszt, czas, próby wstrzyknięcia poleceń; dane osobowe zamaskowane"),
                                    ("gauge", "Jedno polecenie", "docker compose up uruchamia całość, także dla jury")])]
y = 290
for name, cells in layers:
    text(s, 128, y + 22, 220, 60, name, size=22, color=INK2)
    w = (1408 - 18 * (len(cells) - 1)) / len(cells)
    for k, (ic, b, t) in enumerate(cells):
        x = 384 + k * (w + 18)
        core = name == "Rdzeń weryfikacji"
        box(s, x, y, w, 158, fill=SEA_T if core else CARD, line=SEA if core else LINE, weight=2 if core else 1)
        icon(s, ic, x + 26, y + 26)
        text(s, x + 70, y + 20, w - 86, 40, b, size=24, bold=True)
        text(s, x + 70, y + 60, w - 86, 90, t, size=20, color=SEA_D if core else INK2, spacing=1.35)
    y += 176

# 10. Źródła
s = new_slide(10, TOTAL, NOTES[9])
photo(s, "card-catalogue.jpg", 0, 0, 1920, 300, fy=0.58)
title(s, TITLES[9], y=356, size=64)
points(s, 128, 540, 800, [("file-check-2", "Typ 1: źródła urzędowe i pierwotne", "lista organizatora (gov.pl, policja, RCB, GIS, PAA, GIOŚ, CERT) oraz ISAP, EUR-Lex, dane.gov.pl i BIP"),
                          ("badge-check", "Typ 2: fact-checkerzy", "ustalenia w formacie ClaimReview przez Google Fact Check Tools API"),
                          ("eye-off", "Kontekst, nie werdykt", "dopasowanie do znanych przypadków dezinformacji to informacja o serwisie")], gap=140)
points(s, 992, 540, 800, [("book-open-check", "Katalog do audytu", "przy każdym źródle licencja i powód kwalifikacji"),
                          ("library", "Niezależność według wydawcy", "dwie strony jednego ministerstwa to jedno źródło"),
                          ("calendar-clock", "Aktualność", "RSS i wyszukiwanie na żywo w domenach z katalogu; data publikacji i pobrania przy każdym źródle")], gap=140)

# 11. Wyniki testów
s = slide(10)
metrics = [("Trafność werdyktu, macro-F1", "≥ 0,75"), ("Pokrycie cytowań", "≥ 95%"), ("Poprawność cytowania", "≥ 85%"),
           ("Wstrzymanie się przy braku dowodów", "≥ 80%"), ("Odporność na prompt injection", "≥ 90%"),
           ("Czas: mediana od wejścia do odpowiedzi", "≤ 30 s"), ("Koszt 100 testów", "raportowany")]
for x, t in ((128, "Miernik z treści zadania"), (900, "Cel MVP"), (1220, "Nasz wynik na zestawie jawnym")):
    text(s, 128 if x == 128 else x, 300, 600, 30, t, size=22, bold=True, color=INK2)
y = 344
for name, goal in metrics:
    hline(s, 128, y, 1664)
    text(s, 128, y + 18, 760, 36, name, size=26)
    text(s, 900, y + 18, 300, 36, goal, size=26, color=SEA_D, font=SANS if goal == "raportowany" else MONO)
    text(s, 1220, y + 20, 560, 36, "wpisujemy po przebiegu skryptu", size=23, color=INK2)
    y += 70
hline(s, 128, y, 1664)
cap(s, 128, y + 20, 1664, "Zestaw jawny: nasz, zbudowany z tych samych materiałów co baza wiedzy, scenariusze A–J. "
    "Progi stroimy tylko na nim; zestaw referencyjny MSZ jest dla nas ukryty.")

# 12. Ryzyka i dalsze kroki
s = new_slide(12, TOTAL, NOTES[11])
box(s, 1280, 0, 640, 1080, fill=SEA_T, line=None, radius=0)
photo(s, "warsaw-street.jpg", 1280, 0, 640, 380)
text(s, 1336, 420, 520, 44, "Dalsze kroki", size=30, bold=True)
points(s, 1336, 476, 512, [("hand-helping", "Pilotaż z zatwierdzaniem przez człowieka", "moderator zatwierdza odpowiedź przed publikacją"),
                           ("image", "Więcej rodzajów treści", "wyszukiwanie odwrotne obrazu, transkrypcja nagrań"),
                           ("coins", "Koszt 1 000 zapytań", "podamy z pomiaru, razem z kosztem kanałów")], gap=176, size=25, sub=22, rule=TINT_RULE, subcolor=SEA_D, lines=2)
title(s, TITLES[11], w=1040, size=64)
y = 330
for ic, a, b in [("quote", "Halucynacje", "dosłowna weryfikacja cytatów, werdykt tylko z cytatem, wstrzymanie się"),
                 ("scale", "Stronniczość źródeł", "jawny katalog, dwa typy źródeł, rozbieżności pokazane wprost"),
                 ("eye-off", "Prywatność", "maskowanie danych osobowych, retencja 30 dni, usuwanie sprawdzeń"),
                 ("scissors", "Prompt injection", "warstwa kontroli, dane oddzielone od instrukcji, kwarantanna, zapis zdarzeń"),
                 ("accessibility", "Dostępność", "WCAG 2.2 AA, prosty język, telefon bez instalacji"),
                 ("triangle-alert", "Nadużycia i awarie", "limity zapytań, „Problem techniczny” zamiast pozornego werdyktu")]:
    hline(s, 128, y, 1040)
    icon(s, ic, 128, y + 16, 28)
    text(s, 180, y + 13, 250, 60, a, size=23, bold=True, spacing=1.3)
    text(s, 440, y + 13, 720, 70, b, size=23, color=INK2, spacing=1.35)
    y += 76
hline(s, 128, y, 1040)
text(s, 128, y + 30, 1040, 50, "Każde ustalenie ma źródło. Gdy źródeł brak, mówimy to wprost.", size=32, bold=True)
text(s, 128, y + 90, 1040, 30, "Zdjęcia: Unsplash, autorzy Ilya Semenov, camilo jimenez, Nagihan Gülmez, Maksym Kaharlytskyi, "
     "Kate Bezzubets. Ikony: Lucide.", size=16, color=INK2)

# Theme fonts: anything typed into new text boxes defaults to Archivo too.
theme_part = next(p for p in prs.part.package.iter_parts() if p.partname.endswith("theme1.xml"))
from lxml import etree  # noqa: E402  (python-pptx dependency)
theme = etree.fromstring(theme_part.blob)
for tag in ("a:majorFont", "a:minorFont"):
    theme.find(f".//{tag}/a:latin", {"a": "http://schemas.openxmlformats.org/drawingml/2006/main"}).set("typeface", SANS)
theme_part._blob = etree.tostring(theme, xml_declaration=True, encoding="UTF-8", standalone=True)

out = HERE / "meritum-template.pptx"
prs.save(out)
check = Presentation(out)
assert len(check.slides) == TOTAL, len(check.slides)
print(f"saved {out} ({len(check.slides)} slides)")
