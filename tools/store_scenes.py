#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Draws the store kit's scenes (store-submission/graphics/scenes/*.png): stand-ins for a Googlebook desktop, its app
list and the Glowbar, with the real launcher icon. No real screen content: the other apps are blank placeholders.
Google Chrome renders them. graphics.js then puts each on a captioned 1920 x 1080 screenshot (spec.json).

    tools/store_scenes.py
"""
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))
import icon  # noqa: E402

OUT = ROOT / "store-submission/graphics/scenes"
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
W, H = 1600, 1000

ICON = icon.svg([icon.BACKGROUND, icon.foreground()])
# The launcher shows the middle 72 of the icon's 108 dp, masked round.
LAUNCHER_ICON = '<div class="ic" style="width:{s}px;height:{s}px">' + ICON.replace(
    'width="108" height="108"', 'width="{big}" height="{big}" style="margin:-{off}px"') + "</div>"


def launcher_icon(size):
    return LAUNCHER_ICON.format(s=size, big=round(size * 1.5), off=round(size * 0.25))


BASE = """*{{margin:0;box-sizing:border-box}}html,body{{width:{w}px;height:{h}px;overflow:hidden}}
body{{font-family:'DM Sans',system-ui,sans-serif;position:relative;
  background:radial-gradient(60% 70% at 18% 20%, #3b2a6b 0%, transparent 60%),
             radial-gradient(55% 60% at 85% 75%, #12405e 0%, transparent 60%),
             linear-gradient(160deg, #1b1830, #0c0e1a)}}
.ic{{border-radius:50%;overflow:hidden;flex:none}}.ic svg{{display:block}}
.ph{{border-radius:50%;flex:none}}"""
FONTS = ('<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=DM+Sans:opsz,wght@9..40,500;'
         '9..40,700&display=block">')
POINTER = ('<svg width="34" height="46" viewBox="0 0 17 23"><path d="M1,1 L1,18 L5.2,14.2 L8.2,21 L11,19.8 L8.1,13.2 '
           'L13.8,13.2 Z" fill="#fff" stroke="#111" stroke-width="1.2" stroke-linejoin="round"/></svg>')
GREYS = ["#4a4f63", "#5a5f73", "#3f4558", "#56506a", "#4b5a66", "#615a70", "#475066", "#585e6e"]


def taskbar():
    dots = []
    for i in range(9):
        if i == 5:
            dots.append(f'<div style="position:relative">{launcher_icon(104)}'
                        '<div style="position:absolute;left:50%;bottom:-18px;width:12px;height:12px;margin-left:-6px;'
                        'border-radius:6px;background:#fff"></div>'
                        f'<div style="position:absolute;left:52px;top:50px;transform:scale(1.6);transform-origin:0 0">{POINTER}</div>'
                        '<div class="tip">Glowbar Disco</div></div>')
        else:
            dots.append(f'<div class="ph" style="width:104px;height:104px;background:{GREYS[i % len(GREYS)]}"></div>')
    return f"""<style>
.bar{{position:absolute;left:0;right:0;bottom:0;height:180px;background:rgba(18,18,26,.72);
  display:flex;align-items:center;justify-content:center;gap:44px;border-top:1px solid rgba(255,255,255,.08)}}
.tip{{position:absolute;bottom:150px;left:50%;transform:translateX(-50%);white-space:nowrap;background:#2b2a33;
  color:#fff;font-size:44px;font-weight:500;padding:16px 30px;border-radius:18px;box-shadow:0 8px 24px rgba(0,0,0,.4)}}
</style><div class="bar">{''.join(dots)}</div>"""


def applist():
    cells = []
    for i in range(24):
        if i == 9:
            cells.append(f'<div class="cell hit">{launcher_icon(84)}<div class="lab">Glowbar Disco</div></div>')
        else:
            w = 60 + (i * 37) % 50
            cells.append(f'<div class="cell"><div class="ph" style="width:84px;height:84px;background:#cfc8da"></div>'
                         f'<div class="bar" style="width:{w}px"></div></div>')
    return f"""<style>
.panel{{position:absolute;left:50%;top:50%;transform:translate(-50%,-50%);width:1020px;padding:36px 40px 44px;
  background:#efe9f4;border-radius:36px;box-shadow:0 40px 90px rgba(0,0,0,.45)}}
.search{{height:72px;border-radius:36px;background:#fff;display:flex;align-items:center;padding:0 30px;
  color:#8a8494;font-size:28px;margin-bottom:34px}}
.grid{{display:grid;grid-template-columns:repeat(6,1fr);row-gap:30px}}
.cell{{display:flex;flex-direction:column;align-items:center;gap:14px;padding:12px 0}}
.bar{{height:14px;border-radius:7px;background:#d9d2e3}}
.hit{{background:#ddd3ea;border-radius:24px}}
.lab{{font-size:24px;font-weight:700;color:#1d1b22;white-space:nowrap}}
</style><div class="panel"><div class="search">Search</div><div class="grid">{''.join(cells)}</div></div>"""


def glow():
    big = icon.svg([icon.foreground()]).replace('width="108" height="108"', 'width="1400" height="1400"')
    return f"""<style>body{{background:#000}}
.big{{position:absolute;left:50%;top:50%;width:1400px;height:1400px;transform:translate(-50%,-50%)}}
</style><div class="big">{big}</div>"""


def nothing():
    chips = "".join(f'<div class="chip">{t}</div>' for t in ("No window", "No permissions", "About 30 KB"))
    return f"""<style>
.col{{position:absolute;inset:0;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:64px}}
.chips{{display:flex;gap:24px}}
.chip{{font-size:40px;font-weight:700;color:#fff;padding:22px 38px;border-radius:999px;
  background:rgba(255,255,255,.1);border:1px solid rgba(255,255,255,.16)}}
</style><div class="col">{launcher_icon(360)}<div class="chips">{chips}</div></div>"""


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory() as tmp:
        for name, body, w, h in (("taskbar", taskbar(), W, 560), ("applist", applist(), W, H), ("glow", glow(), W, H),
                                 ("nothing", nothing(), W, H)):
            html = Path(tmp) / f"{name}.html"
            html.write_text(f"<!doctype html><html><head>{FONTS}<style>{BASE.format(w=w, h=h)}</style></head><body>{body}</body></html>")
            out = OUT / f"{name}.png"
            subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--hide-scrollbars", f"--window-size={w},{h}",
                            "--virtual-time-budget=3000", f"--screenshot={out}", f"file://{html}"],
                           check=True, stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL)
            print(out.relative_to(ROOT))


if __name__ == "__main__":
    main()
