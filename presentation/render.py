"""Renders Meritum PNG assets with system Chrome.

  uv run --with playwright python presentation/render.py brand|shots|social|deck [out_dir]

shots needs the local demo server: design-system/ served on http://localhost:52990.
"""
import sys
from pathlib import Path
from playwright.sync_api import sync_playwright

DS = Path(__file__).resolve().parent.parent
EXP = DS / "brand" / "exports"
DEMO = "http://localhost:52990/demo"
FONTS = '<link href="https://fonts.googleapis.com/css2?family=Archivo:wdth,wght@75..125,400..800&family=Azeret+Mono:wght@400;500;600&display=swap" rel="stylesheet">'


def svg_page(pg, svg, w, h):
    pg.set_viewport_size({"width": w, "height": h})
    svg = svg.replace("<svg ", f'<svg style="display:block;width:{w}px;height:{h}px" ', 1)
    pg.set_content(f"<html><head>{FONTS}<style>html,body{{margin:0;background:transparent}}</style></head><body>{svg}</body></html>")
    pg.evaluate("document.fonts.ready")
    pg.wait_for_timeout(300)


def brand(b):
    pg = b.new_page()
    marks = {"light": "meritum-mark.svg", "dark": "meritum-mark-on-dark.svg", "mono": "meritum-mark-mono.svg"}
    for name, f in marks.items():
        svg = (DS / "brand" / f).read_text()
        for s in (512, 1024):
            svg_page(pg, svg, s, s)
            pg.screenshot(path=EXP / f"meritum-mark-{name}-{s}.png", omit_background=True)
    icon = (DS / "brand" / "meritum-app-icon.svg").read_text()
    for s in (16, 32, 48, 128, 256, 512):
        svg_page(pg, icon, s, s)
        pg.screenshot(path=EXP / f"meritum-app-icon-{s}.png", omit_background=True)
    pg.close()
    pg = b.new_page(device_scale_factor=2)
    for f in sorted(EXP.glob("meritum-lockup-*.svg")):
        svg = f.read_text()
        vb = [float(v) for v in svg.split('viewBox="')[1].split('"')[0].split()]
        svg_page(pg, svg, int(vb[2] * 3), int(vb[3] * 3))  # 3x the SVG units, at 2x pixel density
        pg.screenshot(path=EXP / f"{f.stem}@2x.png", omit_background=True)


def shots(b, out):
    ctx = b.new_context(viewport={"width": 1440, "height": 900}, device_scale_factor=2, color_scheme="light")
    pg = ctx.new_page()
    pg.goto(f"{DEMO}/x/")
    pg.evaluate("localStorage.removeItem('meritum-demo-theme')")
    pg.reload(); pg.evaluate("document.fonts.ready"); pg.wait_for_timeout(800)
    pg.screenshot(path=out / "x-01-feed.png")
    pg.add_style_tag(content=".tabs{position:static!important}")  # sticky tab bar would cover element shots
    flat = pg.locator('article[data-kind="flat"]')
    flat.locator(".m-report").click(); pg.wait_for_timeout(500)
    flat.locator(".m-chip").filter(has_text="Teoria spiskowa").click(); pg.wait_for_timeout(300)
    box = pg.evaluate("""() => { const a = document.querySelector('article[data-kind=flat]').getBoundingClientRect(),
      b = document.querySelector('.m-pop').getBoundingClientRect();
      return {x: a.left, y: a.top + scrollY, width: a.width, height: Math.max(a.bottom, b.bottom) - a.top + 16}; }""")
    pg.screenshot(path=out / "x-02-report-popover.png", clip=box, full_page=True)
    flat.locator(".m-send").click(); pg.wait_for_timeout(2700)
    flat.screenshot(path=out / "x-03-analysis.png")
    pg.wait_for_timeout(3500)
    flat.scroll_into_view_if_needed(); pg.mouse.move(0, 0); pg.wait_for_timeout(400)
    flat.screenshot(path=out / "x-04-context-note.png")
    pg.screenshot(path=out / "x-04-context-note-full.png")
    flat.locator(".m-card").screenshot(path=out / "x-04-card.png")
    ad = pg.locator('article[data-kind="ad"]')
    ad.scroll_into_view_if_needed()
    ad.locator(".m-report").click(); pg.wait_for_timeout(500)
    ad.locator(".m-chip").filter(has_text="Fałszywy wizerunek").click()
    ad.locator(".m-send").click(); pg.wait_for_timeout(6200)
    ad.scroll_into_view_if_needed(); pg.mouse.move(0, 0); pg.wait_for_timeout(400)
    ad.screenshot(path=out / "x-05-scam-warning.png")
    ad.locator(".m-card").screenshot(path=out / "x-05-card.png")
    pg.goto(f"{DEMO}/widgets/"); pg.evaluate("document.fonts.ready"); pg.wait_for_timeout(1000)
    pg.screenshot(path=out / "widgets-01-top.png")
    pg.locator("#platforms").screenshot(path=out / "widgets-02-platforms.png")
    pg.locator("#states").screenshot(path=out / "widgets-03-states.png")
    ctx.close()


def html_dir(b, src, out, files):
    for f, (w, h) in files.items():
        pg = b.new_page(viewport={"width": w, "height": h})
        pg.goto((src / f).as_uri()); pg.evaluate("document.fonts.ready"); pg.wait_for_timeout(600)
        pg.screenshot(path=out / (Path(f).stem + ".png"))
        pg.close()


def social(b):
    d = DS / "presentation" / "social"
    html_dir(b, d, d, {"og-1200x630.html": (1200, 630), "post-1080x1080.html": (1080, 1080),
                       "story-1080x1920.html": (1080, 1920), "linkedin-banner-1584x396.html": (1584, 396)})


def deck(b, out):
    pg = b.new_page(viewport={"width": 1920, "height": 1080})
    pg.goto((DS / "presentation" / "slides" / "index.html").as_uri()); pg.evaluate("document.fonts.ready"); pg.wait_for_timeout(800)
    n = pg.evaluate("document.querySelectorAll('section.slide').length")
    for i in range(n):
        pg.evaluate(f"go({i})"); pg.wait_for_timeout(150)
        pg.screenshot(path=out / f"slide-{i + 1:02d}.png")
    pg.pdf(path=str(out / "deck.pdf"), width="1920px", height="1080px", print_background=True)


if __name__ == "__main__":
    what = sys.argv[1]
    out = Path(sys.argv[2]) if len(sys.argv) > 2 else DS / "presentation" / "screenshots"
    out.mkdir(parents=True, exist_ok=True); EXP.mkdir(parents=True, exist_ok=True)
    with sync_playwright() as p:
        b = p.chromium.launch(channel="chrome")
        {"brand": lambda: brand(b), "shots": lambda: shots(b, out), "social": lambda: social(b), "deck": lambda: deck(b, out)}[what]()
        b.close()
