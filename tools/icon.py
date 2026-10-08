#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Draws Disco's launcher icon: a faceted mirror ball over the four-colour Glowbar, on Welcome's ink.

One geometry, two outputs: the adaptive icon's vector drawables (res/drawable/ic_launcher_*.xml) and an SVG of the
whole icon for previews. Run it after changing anything here:

    tools/icon.py                  # rewrite the three drawables
    tools/icon.py --svg out.svg    # also write a preview (108 x 108, unmasked)
"""
import math
import random
import sys
from pathlib import Path

RES = Path(__file__).resolve().parent.parent / "app/src/main/res/drawable"

CX, CY, R = 54.0, 45.0, 18.0          # the ball, inside the 66 dp safe circle
LAT, LON = 10, 10                     # facet bands: 18 degrees each, front half only
INSET = 0.87                          # each facet shrinks to this around its centre: the dark gaps between them
KEY = (-0.55, -0.80, 0.25)            # the key light, up and to the left: the facets that mirror it burn white
WOBBLE = 0.09                         # real mirror tiles sit a little crooked: each facet's normal is nudged this much
BLUE, RED, YELLOW, GREEN = "#4285F4", "#EA4335", "#FBBC04", "#34A853"
STRIP_Y, STRIP_H = 70.0, 5.0          # Welcome's Glowbar strip, a step lower under the ball
# Where the strip's segments start and end, seen from the ball: x over y of the direction to it.
SEGMENTS = [(-1.3, -0.55, BLUE), (-0.55, 0.0, RED), (0.0, 0.55, YELLOW), (0.55, 1.3, GREEN)]


def f(v):
    return f"{v:.2f}".rstrip("0").rstrip(".")


def norm(v):
    n = math.sqrt(sum(c * c for c in v))
    return tuple(c / n for c in v)


def mix(a, b, t):
    a, b = [int(a[i:i + 2], 16) for i in (1, 3, 5)], [int(b[i:i + 2], 16) for i in (1, 3, 5)]
    return "#" + "".join(f"{round(x + (y - x) * t):02X}" for x, y in zip(a, b))


def point(theta, phi):
    """A point of the sphere seen from the front: theta is latitude (negative is up), phi longitude."""
    return CX + R * math.cos(theta) * math.sin(phi), CY + R * math.sin(theta)


def environment(r):
    """What a facet facing direction r (x right, y down, z to the viewer) mirrors: a pale room above, a dark floor
    below, the Glowbar below and in front, and the key light."""
    x, y, z = r
    key = norm(KEY)
    if sum(a * b for a, b in zip(r, key)) > 0.97:
        return "#FFFFFF", 1.0
    if 0.6 < y and z > -0.5:
        for lo, hi, col in SEGMENTS:
            if lo <= x / y < hi:
                return mix(col, "#14161C", 0.14), 0.85
    up = -y
    if up >= 0:
        t = up ** 0.75
        return mix("#5C6370", "#E6EAF0", t), 0.35 + 0.6 * t
    t = (-up) ** 0.6
    return mix("#5C6370", "#121419", t), 0.35 - 0.25 * t


def facets():
    """Each visible facet as (corners, colour, brightness 0..1 for the one-colour icon)."""
    rnd = random.Random(63)  # a wobble that keeps the reflected colours in order
    out = []
    for b in range(LAT):
        t0, t1 = math.radians(-90 + 180 * b / LAT), math.radians(-90 + 180 * (b + 1) / LAT)
        for c in range(LON):
            p0, p1 = math.radians(-90 + 180 * c / LON), math.radians(-90 + 180 * (c + 1) / LON)
            pts = [point(t0, p0), point(t0, p1), point(t1, p1), point(t1, p0)]
            mx, my = sum(p[0] for p in pts) / 4, sum(p[1] for p in pts) / 4
            pts = [(mx + (x - mx) * INSET, my + (y - my) * INSET) for x, y in pts]
            tc, pc = (t0 + t1) / 2, (p0 + p1) / 2
            n = norm((math.cos(tc) * math.sin(pc) + rnd.uniform(-WOBBLE, WOBBLE),
                      math.sin(tc) + rnd.uniform(-WOBBLE, WOBBLE), math.cos(tc) * math.cos(pc)))
            # Mirror the view direction (0, 0, 1) in the facet: r = 2 (n . v) n - v.
            r = (2 * n[2] * n[0], 2 * n[2] * n[1], 2 * n[2] * n[2] - 1)
            col, v = environment(r)
            # Facets turned away from us darken towards the rim.
            col = mix(col, "#0E1014", 0.55 * (1 - n[2]) ** 2)
            out.append((pts, col, v))
    return out


def sparkle(cx, cy, s):
    """Welcome's sparkle (the dot of its "i"), centred on cx, cy with arms s long."""
    return (f"M{f(cx)},{f(cy - s)}Q{f(cx)},{f(cy)} {f(cx + s)},{f(cy)}Q{f(cx)},{f(cy)} {f(cx)},{f(cy + s)}"
            f"Q{f(cx)},{f(cy)} {f(cx - s)},{f(cy)}Q{f(cx)},{f(cy)} {f(cx)},{f(cy - s)}Z")


def poly(pts):
    return "M" + "L".join(f"{f(x)},{f(y)}" for x, y in pts) + "Z"


def circle(cx, cy, r):
    return f"M{f(cx - r)},{f(cy)}A{f(r)},{f(r)} 0,1 1,{f(cx + r)},{f(cy)}A{f(r)},{f(r)} 0,1 1,{f(cx - r)},{f(cy)}Z"


def strip(y, h):
    """Welcome's Glowbar strip: four segments, round ends."""
    r = h / 2
    return [(f"M39.5,{f(y)}H45.5V{f(y + h)}H39.5A{f(r)},{f(r)} 0,0 1,39.5 {f(y)}Z", BLUE),
            (f"M45.5,{f(y)}H54V{f(y + h)}H45.5Z", RED),
            (f"M54,{f(y)}H62.5V{f(y + h)}H54Z", YELLOW),
            (f"M62.5,{f(y)}H68.5A{f(r)},{f(r)} 0,0 1,68.5 {f(y + h)}H62.5Z", GREEN)]


SPARK = (CX - 7.1, CY - 8.1, 6.0)  # Welcome's sparkle, on the one facet that mirrors the key light


# Shapes: dicts with d, and fill (a colour), or radial (cx, cy, r, [(offset, colour, alpha)]), or stroke + width.
def foreground():
    top = CY - R
    shapes = [
        # The cord, from above the icon's edge, and the cap it hangs from.
        dict(d=f"M54,0V{f(top - 1.6)}", stroke="#FFFFFF", alpha=0.35, width=0.9),
        dict(d=f"M52.2,{f(top - 2.2)}H55.8V{f(top + 0.6)}H52.2Z", fill="#6E7480"),
        dict(d=f"M52.2,{f(top - 2.2)}H55.8V{f(top - 1.4)}H52.2Z", fill="#B8BDC6"),
        # The Glowbar's light, spilling up from each segment.
        *[dict(d=circle(x, STRIP_Y + 2.5, 13), radial=(x, STRIP_Y + 2.5, 13,
               [(0, col, 0.30), (0.45, col, 0.10), (1, col, 0)])) for x, col in
          ((42.5, BLUE), (49.75, RED), (58.25, YELLOW), (65.5, GREEN))],
        # The ball's body: what shows between the facets.
        dict(d=circle(CX, CY, R + 0.3), fill="#0F1115"),
    ]
    shapes += [dict(d=poly(pts), fill=col) for pts, col, _ in facets()]
    shapes += [
        # A soft bloom and Welcome's sparkle where the light hits.
        dict(d=circle(*SPARK[:2], 8), radial=(*SPARK[:2], 8,
             [(0, "#FFFFFF", 0.8), (0.3, "#FFFFFF", 0.25), (1, "#FFFFFF", 0)])),
        dict(d=sparkle(*SPARK), fill="#FFFFFF"),
    ]
    shapes += [dict(d=d, fill=col) for d, col in strip(STRIP_Y, STRIP_H)]
    return shapes


def monochrome():
    """The themed icon: the same ball, cord, sparkle and strip in one colour; brightness becomes opacity."""
    top = CY - R
    shapes = [dict(d=f"M54,0V{f(top - 1.6)}", stroke="#FFFFFF", alpha=0.6, width=0.9),
              dict(d=f"M52.2,{f(top - 2.2)}H55.8V{f(top + 0.6)}H52.2Z", fill="#FFFFFF")]
    shapes += [dict(d=poly(pts), fill="#FFFFFF", alpha=0.3 + 0.7 * v) for pts, _, v in facets()]
    shapes += [dict(d=sparkle(*SPARK), fill="#FFFFFF"),
               dict(d=f"M39.5,{f(STRIP_Y)}H68.5A2.5,2.5 0,0 1,68.5 {f(STRIP_Y + STRIP_H)}H39.5"
                      f"A2.5,2.5 0,0 1,39.5 {f(STRIP_Y)}Z", fill="#FFFFFF")]
    return shapes


BACKGROUND = [dict(d="M0,0h108v108h-108z", linear=(54, 0, 54, 108, "#22252E", "#0B0C10"))]


def argb(col, alpha=1.0):
    return f"#{round(alpha * 255):02X}{col[1:]}"


def vector(shapes, comment):
    out = ['<?xml version="1.0" encoding="utf-8"?>', f"<!-- {comment} Generated by tools/icon.py: edit that, not this. -->",
           '<vector xmlns:android="http://schemas.android.com/apk/res/android" xmlns:aapt="http://schemas.android.com/aapt"',
           '    android:width="108dp" android:height="108dp" android:viewportWidth="108" android:viewportHeight="108">']
    for s in shapes:
        if "stroke" in s:
            out.append(f'    <path android:strokeColor="{argb(s["stroke"], s.get("alpha", 1))}" android:strokeWidth="{f(s["width"])}"'
                       f' android:strokeLineCap="round" android:pathData="{s["d"]}" />')
        elif "fill" in s:
            out.append(f'    <path android:fillColor="{argb(s["fill"], s.get("alpha", 1))}" android:pathData="{s["d"]}" />')
        else:
            out.append(f'    <path android:pathData="{s["d"]}">')
            out.append('        <aapt:attr name="android:fillColor">')
            if "linear" in s:
                x0, y0, x1, y1, c0, c1 = s["linear"]
                out.append(f'            <gradient android:type="linear" android:startX="{f(x0)}" android:startY="{f(y0)}"'
                           f' android:endX="{f(x1)}" android:endY="{f(y1)}" android:startColor="{argb(c0)}" android:endColor="{argb(c1)}" />')
            else:
                cx, cy, r, stops = s["radial"]
                out.append(f'            <gradient android:type="radial" android:centerX="{f(cx)}" android:centerY="{f(cy)}"'
                           f' android:gradientRadius="{f(r)}">')
                out += [f'                <item android:offset="{f(o)}" android:color="{argb(c, a)}" />' for o, c, a in stops]
                out.append("            </gradient>")
            out.append("        </aapt:attr>")
            out.append("    </path>")
    out.append("</vector>")
    return "\n".join(out) + "\n"


def svg(layers):
    defs, body = [], []
    for s in [s for shapes in layers for s in shapes]:
        if "stroke" in s:
            body.append(f'<path d="{s["d"]}" fill="none" stroke="{s["stroke"]}" stroke-opacity="{f(s.get("alpha", 1))}"'
                        f' stroke-width="{f(s["width"])}" stroke-linecap="round"/>')
        elif "fill" in s:
            body.append(f'<path d="{s["d"]}" fill="{s["fill"]}" fill-opacity="{f(s.get("alpha", 1))}"/>')
        else:
            gid = f"g{len(defs)}"
            if "linear" in s:
                x0, y0, x1, y1, c0, c1 = s["linear"]
                defs.append(f'<linearGradient id="{gid}" gradientUnits="userSpaceOnUse" x1="{x0}" y1="{y0}" x2="{x1}" y2="{y1}">'
                            f'<stop offset="0" stop-color="{c0}"/><stop offset="1" stop-color="{c1}"/></linearGradient>')
            else:
                cx, cy, r, stops = s["radial"]
                defs.append(f'<radialGradient id="{gid}" gradientUnits="userSpaceOnUse" cx="{f(cx)}" cy="{f(cy)}" r="{f(r)}">'
                            + "".join(f'<stop offset="{f(o)}" stop-color="{c}" stop-opacity="{f(a)}"/>' for o, c, a in stops)
                            + "</radialGradient>")
            body.append(f'<path d="{s["d"]}" fill="url(#{gid})"/>')
    return ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 108 108" width="108" height="108">'
            f'<defs>{"".join(defs)}</defs>{"".join(body)}</svg>\n')


def main(argv):
    (RES / "ic_launcher_background.xml").write_text(
        vector(BACKGROUND, "Welcome's ink, a touch lighter at the top, like the Googlebook's lid."))
    (RES / "ic_launcher_foreground.xml").write_text(
        vector(foreground(), "A mirror ball over the four-colour Glowbar, its lower facets catching the bar's colours."))
    (RES / "ic_launcher_monochrome.xml").write_text(
        vector(monochrome(), "Themed icon: the same ball, sparkle and Glowbar in one colour (the launcher tints it)."))
    if "--svg" in argv:
        Path(argv[argv.index("--svg") + 1]).write_text(svg([BACKGROUND, foreground()]))
        if "--mono" in argv:
            Path(argv[argv.index("--mono") + 1]).write_text(svg([[dict(BACKGROUND[0], linear=(54, 0, 54, 108, "#2A3A55", "#2A3A55"))], monochrome()]))


if __name__ == "__main__":
    main(sys.argv[1:])
