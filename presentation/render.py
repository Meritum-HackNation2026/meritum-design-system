"""Renders Meritum PNG assets with system Chrome.

  uv run --with playwright python presentation/render.py brand|shots|social|icons|deck [out_dir]

shots needs design-system/ served over HTTP, by default on http://localhost:52990 (MERITUM_BASE overrides it).
"""
import os
import sys
from pathlib import Path
from playwright.sync_api import sync_playwright

DS = Path(__file__).resolve().parent.parent
EXP = DS / "brand" / "exports"
BASE = os.environ.get("MERITUM_BASE", "http://localhost:52990")  # design-system/ served here
DEMO = f"{BASE}/demo"
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
    for old in out.glob("*.png"):
        old.unlink()  # the set changes with the product; stale shots must not linger
    ctx = b.new_context(viewport={"width": 1440, "height": 900}, device_scale_factor=2, color_scheme="light")
    pg = ctx.new_page()
    pg.goto(f"{DEMO}/live/x/")
    pg.evaluate("localStorage.removeItem('meritum-demo-theme'); sessionStorage.removeItem('meritum-live-fast')")
    pg.reload(); pg.evaluate("document.fonts.ready"); pg.wait_for_timeout(1200)
    pg.add_style_tag(content=".tabs{position:static!important}meritum-root[data-part=demo]{display:none!important}")  # sticky tabs cover element shots; the stage control is not product UI
    flat, ad = pg.locator("article:has(#t3-text)"), pg.locator("article:has(#t2-text)")
    flat.scroll_into_view_if_needed(); pg.mouse.move(0, 0); pg.wait_for_timeout(300)
    flat.locator("button.m-check").click(); pg.wait_for_timeout(6400); pg.mouse.move(0, 0)
    flat.scroll_into_view_if_needed(); pg.wait_for_timeout(600)
    flat.screenshot(path=out / "x-02-false.png")
    flat.locator(".m-card").screenshot(path=out / "x-02-card.png")
    ad.scroll_into_view_if_needed()
    ad.locator("button.m-check").click(); pg.wait_for_timeout(6500); pg.mouse.move(0, 0)
    ad.scroll_into_view_if_needed(); pg.wait_for_timeout(600)
    ad.screenshot(path=out / "x-03-abstain.png")
    ad.locator(".m-card").screenshot(path=out / "x-03-card.png")
    pg.goto(f"{DEMO}/widgets/"); pg.evaluate("document.fonts.ready"); pg.wait_for_timeout(1500)
    pg.add_style_tag(content=".ctl{position:static!important}")
    frame = pg.locator("[data-grid] .frame").first  # X, light
    pg.locator("label:has(input[value=steps])").click(); pg.wait_for_timeout(400)
    frame.screenshot(path=out / "widgets-01-steps.png")
    pg.locator("label:has(input[value=conflict])").click(); pg.wait_for_timeout(400)
    frame.screenshot(path=out / "widgets-02-conflict.png")
    pg.goto(f"{BASE}/presentation/shots/web.html"); pg.wait_for_selector("body[data-ready]")
    pg.evaluate("document.fonts.ready"); pg.wait_for_timeout(600)
    pg.locator("#form").screenshot(path=out / "web-01-form.png")
    pg.locator("#inj-in").screenshot(path=out / "web-02-injection-input.png")
    pg.locator("#inj-log").screenshot(path=out / "web-03-injection-log.png")
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


def icons(b):
    """Lucide SVGs in presentation/icons/ -> an inline <symbol> sprite in slides/index.html (CSS masks and external
    <use> do not load from file://) and accent-coloured PNGs for build_pptx.py."""
    import re
    src = DS / "presentation" / "icons"
    deck = DS / "presentation" / "slides" / "index.html"
    syms = []
    for f in sorted(src.glob("*.svg")):
        inner = re.search(r"<svg[^>]*>(.*)</svg>", f.read_text(), re.S).group(1).strip()
        syms.append(f'<symbol id="i-{f.stem}" viewBox="0 0 24 24">{re.sub(chr(10) + " *", "", inner)}</symbol>')
    # Simple Icons (CC0) brand logos of the stack: filled single-colour paths, ids b-<slug>
    for f in sorted((src / "brands").glob("*.svg")):
        inner = re.sub(r"<title>.*?</title>", "", re.search(r"<svg[^>]*>(.*)</svg>", f.read_text(), re.S).group(1))
        syms.append(f'<symbol id="b-{f.stem}" viewBox="0 0 24 24">{inner.strip()}</symbol>')
    html = deck.read_text()
    a, z = "<!-- icons:start -->", "<!-- icons:end -->"
    assert a in html and z in html, "icon sprite markers missing in slides/index.html"
    deck.write_text(html[:html.index(a) + len(a)] + "\n" + "\n".join(syms) + "\n" + html[html.index(z):])
    out = src / "png"
    out.mkdir(exist_ok=True)
    pg = b.new_page(viewport={"width": 128, "height": 128})
    for f in sorted(src.glob("*.svg")):
        for suffix, colour in (("", "#1D6A86"), ("-white", "#FFFFFF")):
            svg = f.read_text().replace('width="24"', 'width="128"').replace('height="24"', 'height="128"').replace("currentColor", colour)
            pg.set_content(f"<html><body style='margin:0;background:transparent'>{svg}</body></html>")
            pg.screenshot(path=out / f"{f.stem}{suffix}.png", omit_background=True, clip={"x": 0, "y": 0, "width": 128, "height": 128})
    for f in sorted((src / "brands").glob("*.svg")):
        svg = f.read_text().replace("<svg ", '<svg width="128" height="128" fill="#14191E" ', 1)
        pg.set_content(f"<html><body style='margin:0;background:transparent'>{svg}</body></html>")
        pg.screenshot(path=out / f"brand-{f.stem}.png", omit_background=True, clip={"x": 0, "y": 0, "width": 128, "height": 128})


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
        {"brand": lambda: brand(b), "shots": lambda: shots(b, out), "social": lambda: social(b), "icons": lambda: icons(b), "deck": lambda: deck(b, out)}[what]()
        b.close()
