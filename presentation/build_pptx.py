"""Builds presentation/meritum-template.pptx: the same 10 layouts as slides/index.html.

  uv run --with python-pptx python presentation/build_pptx.py

Coordinates are written in the HTML deck's 1920x1080 px grid and converted to EMU.
Fonts: Archivo (text) and Azeret Mono (data). Without them installed PowerPoint
substitutes a default sans; Google Slides has both in its font list.
"""
from pathlib import Path

from pptx import Presentation
from pptx.chart.data import CategoryChartData
from pptx.dml.color import RGBColor
from pptx.enum.chart import XL_CHART_TYPE, XL_MARKER_STYLE
from pptx.enum.shapes import MSO_CONNECTOR, MSO_SHAPE
from pptx.enum.text import MSO_ANCHOR, PP_ALIGN
from pptx.oxml.ns import qn
from pptx.util import Emu, Pt

HERE = Path(__file__).resolve().parent
EXP = HERE.parent / "brand" / "exports"
SHOTS = HERE / "screenshots"

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


def new_slide(n, total, notes, footer=True):
    s = prs.slides.add_slide(BLANK)
    s.background.fill.solid()
    s.background.fill.fore_color.rgb = rgb(BG)
    if footer:
        image(s, EXP / "meritum-mark-light-512.png", 124, 1000, 36, 36)
        text(s, 166, 1004, 300, 32, "meritum", size=24, bold=True)
        text(s, 1592, 1006, 200, 30, f"{n} / {total}", size=20, color=INK2, align=PP_ALIGN.RIGHT)
    s.notes_slide.notes_text_frame.text = notes
    return s


def title(s, t, y=112, w=1500, size=72):
    return text(s, 128, y, w, 180, t, size=size, bold=True, spacing=1.05)


TOTAL = 10

# 1. Tytuł
s = new_slide(1, TOTAL, "Otwieramy jednym zdaniem: Meritum to niezależna warstwa zaufania nad mediami społecznościowymi. "
              "Z jednego zgłoszenia odsłania całą kampanię, a kontekst publikuje dopiero wtedy, gdy zgodzą się ludzie, "
              "którzy zwykle się nie zgadzają.", footer=False)
image(s, EXP / "meritum-lockup-subtitle-light@2x.png", 128, 220, w=420)
text(s, 128, 400, 1000, 460, "Jeden fejk, cała kampania. Jeden kontekst, ponad podziałami.", size=96, bold=True, spacing=1.05)
image(s, SHOTS / "x-04-context-note.png", 1152, 200, w=640)
text(s, 128, 1000, 1200, 32, "HackNation 2026 · MSZ „Prawdowid” · NASK „Kolekcjoner fejków”", size=22, color=INK2)

# 2. Problem
s = new_slide(2, TOTAL, "Problem w 20 sekund. Post o rzekomym zakazie płacenia gotówką ma setki tysięcy wyświetleń, a sprostowanie "
              "leży na stronie, której nikt nie odwiedzi. Reklama z deepfake'iem prezentera po zgłoszeniu znika i jutro wraca "
              "pod nową domeną. Obie sytuacje to ten sam problem.")
title(s, "Fakt-check jest gdzieś w sieci, ale nie tam, gdzie ludzie czytają")
cols = (128, 428, 1040)
rows = [("", "Dezinformacja (MSZ „Prawdowid”)", "Fałszywe reklamy (NASK „Kolekcjoner fejków”)"),
        ("Zagrożenie", "manipulacja, fałszywe narracje", "reklamy z wizerunkiem znanych osób użytym bez zgody"),
        ("Co utrudnia", "nadmiar informacji, brak wiarygodnych źródeł", "szybko znikają, wracają pod nowymi adresami"),
        ("Czego brakuje", "narzędzia do świadomej oceny treści", "szerszego obrazu: jeden materiał to fragment kampanii")]
y = 400
for i, row in enumerate(rows):
    if i:
        hline(s, 128, y - 22, 1664)
    for j, cell in enumerate(row):
        text(s, cols[j], y, 600 if j else 280, 80, cell, size=26 if i == 0 else 28, bold=i == 0,
             color=INK2 if (j == 0 and i) else INK)
    y += 84

# 3. Teza
s = new_slide(3, TOTAL, "To jest argument dla jury: widzą platformę, a nie jednorazowy prototyp. Ten sam produkt odpowiada na oba "
              "wyzwania, zmienia się tylko scena główna demo.")
title(s, "Jeden fejk, cała kampania")
text(s, 128, 220, 1200, 160, "Farma botów forsująca fałszywą narrację i sieć domen rotująca reklamy z deepfake'iem działają tak samo: "
     "wiele kopii, krótkie życie, skoordynowane konta. Dlatego budujemy jeden silnik.", size=32, color=INK2, spacing=1.4)
hline(s, 128, 523, 1664, color=INK, weight=2)
steps = [("Zbiera", "zgłoszenia i ślady: zrzut, adres, przekierowania, czas"),
         ("Łączy", "okazy w kampanie po obrazie, tekście, szablonie strony i domenach"),
         ("Wyjaśnia", "co widzisz, ze źródłami i nazwą techniki manipulacji"),
         ("Chroni", "przed kliknięciem i przed manipulacją głosowaniem")]
for i, (h, d) in enumerate(steps):
    x = 128 + i * 416
    c = s.shapes.add_shape(MSO_SHAPE.OVAL, px(x), px(496), px(56), px(56))
    c.fill.solid()
    c.fill.fore_color.rgb = rgb(SEA if i == 2 else BG)
    c.line.color.rgb = rgb(SEA if i == 2 else INK)
    c.line.width = pt(2)
    c.shadow.inherit = False
    tf = c.text_frame
    tf.margin_left = tf.margin_right = 0
    r = tf.paragraphs[0].add_run()
    r.text = str(i + 1)
    tf.paragraphs[0].alignment = PP_ALIGN.CENTER
    r.font.name, r.font.size, r.font.bold, r.font.color.rgb = SANS, pt(24), True, rgb("FFFFFF" if i == 2 else INK)
    text(s, x, 584, 370, 56, h, size=40, bold=True)
    text(s, x, 644, 360, 120, d, size=26, color=INK2, spacing=1.4)

# 4. Demo
s = new_slide(4, TOTAL, "Pokaz na żywo: demo/x/. Kliknij „Zgłoś” pod postem o płaskiej Ziemi, zaznacz „Teoria spiskowa”, wyślij. "
              "Po około 5 sekundach pod postem pojawia się notatka. Zrzuty to ten sam przepływ, na wypadek braku internetu.")
title(s, "Trzy kliknięcia od zgłoszenia do notatki")
image(s, SHOTS / "x-02-report-popover.png", 128, 260, h=600)
image(s, SHOTS / "x-04-context-note.png", 680, 260, h=600)
image(s, SHOTS / "x-05-scam-warning.png", 1340, 260, h=600)
for x, w, b, t in [(128, 520, "1. Zgłoszenie. ", "Powód do wyboru albo własne słowa."),
                   (680, 620, "2. Notatka. ", "Źródła obowiązkowe, technika nazwana."),
                   (1340, 450, "3. Oszustwo. ", "Najpierw ochrona, potem wyjaśnienie.")]:
    text(s, x, 880, w, 70, [[(b, {"bold": True}), (t, {"color": INK2})]], size=22)

# 5. Konsensus
s = new_slide(5, TOTAL, "Algorytm typu „bridging”, ten sam rodzaj co otwarty algorytm Community Notes, ale niezależny od platformy. "
              "Kto decyduje, co jest prawdą? Nikt sam: AI pisze szkic, ludzie z różnych stron muszą się zgodzić, źródła są publiczne.")
title(s, "Notatka wychodzi, gdy zgodzą się obie strony", w=1000)
for i, t in enumerate(["AI pisze szkic z uwag użytkowników i źródeł.",
                       "Oceniają go dwie grupy, które zwykle oceniają inaczej.",
                       "Publikacja dopiero, gdy obie przekroczą próg 70% ocen „pomocne”.",
                       "Większość nie wystarcza, więc farma botów nie przepchnie notatki."]):
    y = 344 + i * 110
    hline(s, 128, y - 22, 600)
    text(s, 128, y, 40, 40, str(i + 1), size=28, bold=True, color=INK2)
    text(s, 184, y, 540, 90, t, size=28)
hline(s, 128, 344 + 4 * 110 - 22, 600)


def consensus(s, y, head, badge, ok, a, b, la, lb):
    box(s, 824, y, 968, 220)
    text(s, 864, y + 36, 600, 40, head, size=30, bold=True)
    pill(s, 1752 - (160 if ok else 130), y + 32, badge, SEA_T if ok else AMBER_T, SEA_D if ok else AMBER_D, w=160 if ok else 130)
    half, cx, by = 430, 1308, y + 100
    for side, val in ((-1, a), (1, b)):
        x0 = cx + 10 if side > 0 else cx - 10 - half
        box(s, x0, by, half, 16, fill=RAISED, line=None, radius=8)
        fw = half * val / 100
        box(s, (cx + 10) if side > 0 else (cx - 10 - fw), by, fw, 16, fill=SEA if ok else AMBER, line=None, radius=8)
        tx = (cx + 10 + half * 0.7) if side > 0 else (cx - 10 - half * 0.7)
        box(s, tx - 1.5, by - 6, 3, 28, fill=INK, line=None, radius=0)
    box(s, cx - 2, by - 10, 4, 36, fill=INK, line=None, radius=0)
    text(s, 864, y + 150, 440, 40, la, size=24, color=INK2)
    text(s, 1312, y + 150, 440, 40, lb, size=24, color=INK2, align=PP_ALIGN.RIGHT)


consensus(s, 320, "Obie grupy powyżej progu", "Zweryfikowany", True, 88, 84, "Grupa A: 88% pomocne, 231 ocen", "Grupa B: 84%, 198 ocen")
consensus(s, 564, "Jedna grupa poniżej progu", "W ocenie", False, 95, 41, "Grupa A: 95% pomocne, 310 ocen", "Grupa B: 41%, 122 ocen")
text(s, 824, 808, 968, 32, "Dane symulowane. Kreska na każdym pasku to próg 70%.", size=20, color=INK2)

# 6. Kampania
s = new_slide(6, TOTAL, "Scena główna pitchu NASK. Jedno zgłoszenie rozwija kampanię #K-118: 47 wariantów, 23 domeny, 9 dni. "
              "Przerywana linia to domena wyłapana w logach Certificate Transparency, zanim trafiła do reklamy. To sygnał do weryfikacji, a nie wyrok.")
text(s, 128, 112, 1600, 100, [[("Jedno zgłoszenie, cała kampania ", {}), ("#K-118", {"font": MONO})]], size=72, bold=True, spacing=1.05)
image(s, SHOTS / "x-05-scam-warning.png", 128, 248, h=720)
box(s, 744, 248, 1048, 470)
for k, d in enumerate(["dzień 1", "3", "5", "7", "9"]):
    text(s, 1090 + k * 160, 272, 120, 28, d, size=20, color=INK2)
doms = [("inwest-polska24.online", 0, .24, "dead"), ("zysk-dzis-pl.site", .16, .22, "dead"),
        ("prezenter-wywiad.info", .30, .20, "dead"), ("bank-ukrywa.online", .44, .18, "dead"),
        ("sekret-zarobku.site", .58, .42, "live"), ("inwest-polska25.online", .72, .28, "live"),
        ("inwest-polska26.online", .90, .10, "pred")]
for i, (d, start, width, kind) in enumerate(doms):
    y = 312 + i * 52
    hline(s, 780, y, 976)
    text(s, 780, y + 13, 320, 30, d, size=21, font=MONO, color={"dead": INK2, "live": INK, "pred": RED_D}[kind])
    tw = 1756 - 1090
    box(s, 1090 + tw * start, y + 17, tw * width, 18, radius=9,
        fill={"dead": GREY, "live": RED, "pred": None}[kind], line=RED if kind == "pred" else None, weight=2, dash=kind == "pred")
text(s, 780, 680, 976, 30, "6 z 23 domen kampanii + 1 przewidziana · szare: wyłączone · czerwone: aktywne · przerywane: z logów certyfikatów",
     size=18, color=INK2)
hline(s, 744, 748, 1048)
text(s, 744, 770, 1048, 50, [[("Reklamy ", {}), ("47", {"font": MONO, "bold": True, "color": INK, "size": 34}), (" = Facebook ", {}),
                             ("31", {"font": MONO, "bold": True, "color": INK, "size": 34}), (" + Instagram ", {}),
                             ("12", {"font": MONO, "bold": True, "color": INK, "size": 34}), (" + X ", {}),
                             ("4", {"font": MONO, "bold": True, "color": INK, "size": 34})]], size=28, color=INK2)
hline(s, 744, 836, 1048)
text(s, 744, 856, 1048, 30, "Dane symulowane. Prezenter „Tomasz Rewiński” i wszystkie domeny są fikcyjne.", size=20, color=INK2)

# 7. Telemetria
s = new_slide(7, TOTAL, "Zwrot w pitchu MSZ. Farma 312 kont próbuje zakopać notatkę. Czerwona linia to odrzucone głosy, czarna to "
              "realne osoby. Suma się domyka: oddane = liczone + odrzucone. Status notatki się nie zmienia.")
# weather-front glyph: line with three triangles
hline(s, 128, 166, 90, color=RED, weight=3)
for k in range(3):
    tri = s.shapes.add_shape(MSO_SHAPE.ISOSCELES_TRIANGLE, px(131 + k * 30), px(142), px(26), px(24))
    tri.fill.solid()
    tri.fill.fore_color.rgb = rgb(RED)
    tri.line.fill.background()
    tri.shadow.inherit = False
text(s, 244, 112, 1400, 100, "Atak odparty, notatka bez zmian", size=72, bold=True, spacing=1.05)
counted = [37, 41, 40, 39, 42, 40, 41, 38, 40, 43, 39, 41, 40, 42, 39, 41, 40, 38, 42, 40, 41, 39, 40, 42, 40, 41, 39, 40, 38, 41]
rejected = [0] * 12 + [180, 300, 310, 320, 330, 300, 320, 310, 290, 300, 320, 310, 300, 320, 290, 312, 0, 0]
assert sum(counted) == 1204 and sum(rejected) == 4812, "telemetry totals must close: 6 016 = 1 204 + 4 812"
box(s, 128, 232, 1000, 420)
cd = CategoryChartData()
cd.categories = [f"14:{20 + i}" for i in range(30)]
cd.add_series("liczone", counted)
cd.add_series("odrzucone", rejected)
ch = s.shapes.add_chart(XL_CHART_TYPE.LINE, px(148), px(248), px(960), px(390), cd).chart
ch.has_legend = True  # PowerPoint cannot label lines directly without manual labels; legend at the right edge
ch.legend.include_in_layout = False
ch.legend.font.size, ch.legend.font.name = pt(18), SANS
for ser, col in zip(ch.series, (INK, RED)):
    ser.format.line.color.rgb = rgb(col)
    ser.format.line.width = pt(3)
    ser.smooth = False
    ser.marker.style = XL_MARKER_STYLE.NONE
for ax in (ch.category_axis, ch.value_axis):
    ax.tick_labels.font.size, ax.tick_labels.font.name = pt(16), MONO
    ax.tick_labels.font.color.rgb = rgb(INK2)
    ax.format.line.fill.background()
ch.value_axis.major_gridlines.format.line.color.rgb = rgb(LINE)
skip = ch.category_axis._element.makeelement(qn("c:tickLblSkip"), {"val": "6"})  # one label per 6 minutes
nml = ch.category_axis._element.find(qn("c:noMultiLvlLbl"))
nml.addprevious(skip) if nml is not None else ch.category_axis._element.append(skip)
hline(s, 128, 676, 1000)
text(s, 128, 696, 1000, 50, [[("Oddane ", {}), ("6 016", {"font": MONO, "bold": True, "color": INK, "size": 34}), (" = liczone ", {}),
                             ("1 204", {"font": MONO, "bold": True, "color": INK, "size": 34}), (" + odrzucone ", {}),
                             ("4 812", {"font": MONO, "bold": True, "color": RED, "size": 34})]], size=28, color=INK2)
text(s, 900, 708, 228, 30, "dane symulowane", size=20, color=INK2, align=PP_ALIGN.RIGHT)
hline(s, 128, 762, 1000)
text(s, 1192, 232, 600, 130, [[("Klaster ", {}), ("312", {"font": MONO}), (" kont głosuje na notatkę ", {}), ("#N-2291", {"font": MONO}),
                              (" od ", {}), ("14:32", {"font": MONO}), (". Żaden z jego głosów nie trafił do konsensusu.", {})]],
     size=28, color=INK2, spacing=1.4)
text(s, 1192, 392, 120, 28, "Czas", size=20, bold=True, color=INK2)
text(s, 1310, 392, 300, 28, "Odrzucone konto", size=20, bold=True, color=INK2)
text(s, 1592, 392, 200, 28, "Powód", size=20, bold=True, color=INK2, align=PP_ALIGN.RIGHT)
for i, (t, h, why) in enumerate([("14:41", "@pl_patriot_88231", "ten sam klaster"), ("14:41", "@glos_ludu_4410", "rytm 1 głos/s"),
                                 ("14:40", "@marek_k_20931", "konto ma 2 dni"), ("14:39", "@prawda_tv_7781", "ten sam klaster"),
                                 ("14:38", "@ania_m_55102", "konto ma 2 dni")]):
    y = 436 + i * 50
    hline(s, 1192, y, 600)
    text(s, 1192, y + 12, 110, 30, t, size=22, font=MONO, color=INK2)
    text(s, 1310, y + 12, 300, 30, [[(h, {"strike": True})]], size=22, font=MONO, color=RED)
    text(s, 1560, y + 12, 232, 30, why, size=22, color=INK2, align=PP_ALIGN.RIGHT)
text(s, 1192, 700, 600, 30, "Dane symulowane. Wszystkie nazwy kont są wymyślone.", size=20, color=INK2)

# 8. Architektura
s = new_slide(8, TOTAL, "Najważniejsze: ten sam silnik jest dostępny jako API i jako serwer MCP, więc redakcje, uczelnie i CERT mogą "
              "się podpiąć bez instalowania wtyczki.")
title(s, "Działa dziś, skaluje się jutro")
layers = [("Dla ludzi", [("Wtyczka do przeglądarki", "zgłoszenie, notatka, ostrzeżenie, sejf dowodów"),
                         ("Panel analityka", "React, TanStack: kampanie i ataki na żywo"),
                         ("Asystenci AI redakcji", "serwer MCP (FastMCP): „czy ta domena należy do kampanii?”")], False),
          ("Rdzeń", [("FastAPI", "otwarte API: notatki, konsensus, kampanie"),
                     ("Pydantic AI", "szkic notatki ze źródłami; nie decyduje o publikacji"),
                     ("DBOS", "trwałe przepływy; demo odtwarzane bez internetu")], True),
          ("Dane", [("PostgreSQL + pgvector", "graf kampanii: podobieństwo obrazu, tekstu, szablonu strony, domen")], False)]
y = 264
for name, cells, core in layers:
    text(s, 128, y + 24, 240, 30, name, size=24, color=INK2)
    w = (1792 - 412 - 20 * (len(cells) - 1)) / len(cells)
    for k, (h, d) in enumerate(cells):
        x = 412 + k * (w + 20)
        box(s, x, y, w, 140, line=SEA if core else LINE, weight=2 if core else 1)
        text(s, x + 28, y + 22, w - 56, 40, h, size=30, bold=True)
        text(s, x + 28, y + 66, w - 56, 64, d, size=22, color=INK2, spacing=1.3)
    y += 160
hline(s, 128, y + 4, 1664)
text(s, 128, y + 28, 240, 30, "Infrastruktura", size=24, color=INK2)
text(s, 412, y + 26, 1300, 40, "GCP (aplikacja i baza) + Cloudflare (ruch, ochrona API)", size=28)

# 9. Zespół i prośba
s = new_slide(9, TOTAL, "Uzupełnij imiona przed pitchem. Nie mówimy o współpracy z NASK, CERT Polska, MSZ ani mediami, dopóki jej nie ma; "
              "mówimy „gotowe do integracji z…”.")
title(s, "Zespół i czego potrzebujemy")
text(s, 128, 256, 600, 50, "Zespół", size=36, bold=True)
for i, role in enumerate(["backend, API, DBOS", "AI i graf kampanii", "wtyczka i panel", "projekt i pitch"]):
    y = 330 + i * 80
    hline(s, 128, y - 18, 784)
    text(s, 128, y, 400, 40, "[Imię Nazwisko]", size=28, bold=True)
    text(s, 512, y, 400, 40, role, size=28, color=INK2, align=PP_ALIGN.RIGHT)
text(s, 1008, 256, 600, 50, "Prośba", size=36, bold=True)
for i, (b, t) in enumerate([("Pilotaż z redakcją lub uczelnią: ", "pierwsi użytkownicy API i serwera MCP."),
                            ("Dostęp do listy ostrzeżeń: ", "gotowe do integracji z CERT Polska."),
                            ("Konsultacja prawna: ", "RODO, wizerunek i status zaufanego podmiotu sygnalizującego z DSA.")]):
    y = 330 + i * 120
    hline(s, 1008, y - 18, 784)
    text(s, 1008, y, 784, 100, [[(b, {"bold": True}), (t, {})]], size=28, spacing=1.4)

# 10. Zamknięcie
s = new_slide(10, TOTAL, "Hasło pod konkretny konkurs. MSZ: „AI pisze. Ludzie decydują. Źródła są obowiązkowe.” "
              "NASK: „Pojedynczy fejk znika. Kolekcja zostaje.”")
text(s, 128, 150, 1600, 360, "Jeden fejk, cała kampania. Jeden kontekst, ponad podziałami.", size=112, bold=True, spacing=1.05)
text(s, 128, 560, 1600, 200, "AI pisze. Ludzie decydują. Źródła są obowiązkowe.", size=80, bold=True, color=SEA, spacing=1.05)
image(s, EXP / "meritum-lockup-subtitle-light@2x.png", 128, 820, w=360)

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
