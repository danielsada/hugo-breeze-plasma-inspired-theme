"""Regenerate the README / theme-gallery screenshots from the example site.

    hugo --source exampleSite --cleanDestinationDir
    python scripts/screenshots.py exampleSite/public                    # pip install playwright; playwright install chromium
    python scripts/screenshots.py exampleSite/public --channel msedge   # or use an installed Edge / Chrome

Writes images/screenshot.png (1500×1000) and images/tn.png (900×600), the sizes the Hugo themes site expects,
and docs/images/*.png, which README.md shows.
"""
import argparse, base64, http.server, pathlib, threading
from playwright.sync_api import sync_playwright

ROOT = pathlib.Path(__file__).resolve().parent.parent
PORT = 8898
BASE = f"http://127.0.0.1:{PORT}"
CALM = "*,*::before,*::after{transition:none!important;animation:none!important;caret-color:transparent!important}"


def serve(public):
    class H(http.server.SimpleHTTPRequestHandler):
        def __init__(self, *a, **k):
            super().__init__(*a, directory=str(public), **k)

        def log_message(self, *a):
            pass

    srv = http.server.ThreadingHTTPServer(("127.0.0.1", PORT), H)
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    return srv


def shot(browser, path, w, h, scheme="light", scale=1, before=None, mobile=False):
    ctx = browser.new_context(viewport={"width": w, "height": h}, color_scheme=scheme,
                              device_scale_factor=scale, is_mobile=mobile, has_touch=mobile)
    pg = ctx.new_page()
    pg.goto(BASE + path, wait_until="networkidle")
    pg.add_style_tag(content=CALM)
    if before:
        before(pg)
    pg.wait_for_timeout(400)
    png = pg.screenshot()
    ctx.close()
    return png


def data_uri(png):
    return "data:image/png;base64," + base64.b64encode(png).decode()


def compose(browser, html, w, h, out, scale=1):
    ctx = browser.new_context(viewport={"width": w, "height": h}, device_scale_factor=scale)
    pg = ctx.new_page()
    pg.set_content(html, wait_until="load")
    out.parent.mkdir(parents=True, exist_ok=True)
    pg.screenshot(path=str(out))
    ctx.close()
    print("wrote", out.relative_to(ROOT))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("public", help="the built example site, e.g. exampleSite/public")
    ap.add_argument("--channel", default=None, help="msedge or chrome (default: Playwright's Chromium)")
    a = ap.parse_args()
    srv = serve(pathlib.Path(a.public).resolve())
    docs = ROOT / "docs" / "images"

    def save(name, png):
        docs.mkdir(parents=True, exist_ok=True)
        (docs / name).write_bytes(png)
        print("wrote", (docs / name).relative_to(ROOT))

    with sync_playwright() as p:
        b = p.chromium.launch(channel=a.channel) if a.channel else p.chromium.launch()

        # Hero: the home page in light and dark, split on a diagonal (also the theme-gallery screenshot)
        light = data_uri(shot(b, "/", 1500, 1000, "light"))
        dark = data_uri(shot(b, "/", 1500, 1000, "dark"))
        split = f"""<style>html,body{{margin:0}} img,i{{position:absolute;inset:0;width:1500px;height:1000px;display:block}}
          .d{{clip-path:polygon(64% 0,100% 0,100% 100%,44% 100%)}}
          i{{background:rgba(255,255,255,.75);clip-path:polygon(calc(64% - 1px) 0,calc(64% + 1px) 0,calc(44% + 1px) 100%,calc(44% - 1px) 100%)}}</style>
          <img src="{light}"><img class="d" src="{dark}"><i></i>"""
        compose(b, split, 1500, 1000, ROOT / "images" / "screenshot.png")
        compose(b, split, 1500, 1000, ROOT / "images" / "tn.png", scale=0.6)

        # Gallery
        def filter_series(pg):
            pg.click('.show a[data-f^="series:"]')

        def to_code(pg):
            pg.evaluate("document.getElementById('code').scrollIntoView(); window.scrollBy(0, -24)")

        save("archive.png", shot(b, "/posts/", 1440, 900, "light", before=filter_series))
        save("post-dark.png", shot(b, "/blog/a-theme-that-respects-the-reader/", 1440, 900, "dark", before=to_code))
        save("projects.png", shot(b, "/projects/", 1440, 900, "light"))
        save("notas-dark.png", shot(b, "/notas/", 1440, 900, "dark"))

        # Phones: home, a post with its inline outline open, and the navigation drawer
        def open_toc(pg):
            pg.evaluate("document.querySelector('details.toc').open = true")

        def open_drawer(pg):
            pg.click("[data-open]")

        phones = [
            shot(b, "/", 390, 844, "light", scale=2, mobile=True),
            shot(b, "/blog/home-lab-part-2-one-small-server/", 390, 844, "dark", scale=2, before=open_toc, mobile=True),
            shot(b, "/projects/", 390, 844, "light", scale=2, before=open_drawer, mobile=True),
        ]
        frames = "".join(f'<img src="{data_uri(x)}">' for x in phones)
        mobile = f"""<style>html,body{{margin:0}}
          body{{display:flex;gap:44px;justify-content:center;align-items:center;width:1350px;height:964px;
               background:linear-gradient(135deg,#5fc3f5,#3d8ee9 45%,#5b3fb8)}}
          img{{width:390px;height:844px;border-radius:34px;box-shadow:0 0 0 8px #1b1e24,0 24px 48px -12px rgba(10,12,40,.6)}}</style>{frames}"""
        compose(b, mobile, 1350, 964, docs / "mobile.png")
        b.close()
    srv.shutdown()


if __name__ == "__main__":
    main()
