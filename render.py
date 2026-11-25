#!/usr/bin/env python3
"""Draw the 25 November 2026 front page (1024x1024) from stories_20261125.json.

Local-only renderer (Pillow). Deterministic: no randomness, no clock, no
network. Run: python3 render.py  ->  writes entry.png next to this file.
"""
import json
import math
import os
import sys

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
W = H = 1024
PAPER = (248, 244, 234)
INK = (18, 18, 18)
SOFT = (90, 86, 76)
RED = (185, 28, 28)
NAVY = (30, 58, 95)
RULE = (180, 172, 156)
BADGE = {
    "CONFIRMED": (22, 101, 52),
    "REPORTED": (29, 78, 216),
    "CLAIM": (180, 83, 9),
    "ONGOING": (126, 34, 206),
}
BADGE_SHORT = {"CONFIRMED": "CONF.", "REPORTED": "REP.", "CLAIM": "CLM.", "ONGOING": "ONG."}

SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def font(size, bold=False, serif=False):
    path = (SERIF_B if serif else SANS_B) if bold else (SERIF if serif else SANS)
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, width):
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def text_block(draw, x, y, text, fnt, fill, width, leading=None):
    if leading is None:
        leading = int(fnt.size * 1.22)
    for line in wrap(draw, text, fnt, width):
        draw.text((x, y), line, font=fnt, fill=fill)
        y += leading
    return y


def circle_number(draw, cx, cy, r, n, fill=RED):
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=fill, outline=(255, 255, 255), width=1)
    f = font(max(8, r - 1), bold=True)
    t = str(n)
    tw = draw.textlength(t, font=f)
    th = f.size
    draw.text((cx - tw / 2, cy - th / 2 - 1), t, font=f, fill=(255, 255, 255))


def badge_chip(draw, x, y, label):
    f = font(8, bold=True)
    w = draw.textlength(label, font=f) + 10
    h = 14
    draw.rounded_rectangle([x, y, x + w, y + h], radius=3, fill=BADGE[label])
    draw.text((x + 5, y + 2), label, font=f, fill=(255, 255, 255))
    return w


# ---- dotted world map: rough continent outlines in (lon, lat) ----
CONTINENTS = [
    [(-168, 66), (-140, 70), (-125, 72), (-110, 73), (-95, 80), (-85, 70), (-76, 62), (-70, 58), (-65, 45), (-75, 35), (-80, 26), (-85, 30), (-90, 21), (-97, 16), (-105, 20), (-110, 24), (-117, 33), (-125, 40), (-125, 49), (-135, 58), (-155, 58), (-165, 60)],
    [(-55, 60), (-40, 64), (-30, 68), (-22, 70), (-25, 76), (-45, 76), (-58, 74), (-60, 66)],
    [(-80, 10), (-72, 12), (-62, 10), (-52, 5), (-50, -2), (-42, -5), (-35, -8), (-40, -20), (-48, -28), (-55, -35), (-65, -41), (-70, -50), (-73, -53), (-70, -20), (-78, -5), (-81, 0), (-80, 8)],
    [(-10, 36), (-9, 43), (-2, 48), (-4, 50), (0, 51), (3, 53), (8, 57), (10, 59), (5, 60), (12, 61), (18, 56), (21, 55), (24, 58), (28, 60), (30, 62), (30, 70), (25, 71), (18, 69), (12, 66), (5, 62), (5, 58), (-2, 57), (-5, 50), (-10, 44), (-9, 38)],
    [(-6, 35), (0, 36), (10, 37), (11, 34), (20, 32), (32, 31), (35, 28), (37, 22), (40, 15), (43, 11), (48, 10), (51, 12), (46, 5), (41, -2), (40, -10), (35, -18), (32, -26), (28, -33), (20, -35), (16, -28), (13, -18), (12, -6), (9, 4), (4, 6), (-8, 5), (-15, 11), (-17, 15), (-16, 20), (-13, 27), (-10, 31)],
    [(30, 70), (40, 68), (55, 69), (68, 73), (80, 73), (95, 76), (110, 74), (130, 72), (145, 72), (160, 70), (170, 66), (178, 65), (170, 60), (162, 56), (156, 52), (142, 50), (140, 40), (130, 38), (127, 35), (122, 32), (120, 25), (110, 20), (105, 10), (100, 8), (98, 12), (95, 16), (90, 22), (85, 20), (80, 15), (77, 8), (73, 20), (66, 25), (60, 25), (57, 26), (52, 28), (50, 30), (48, 30), (44, 29), (40, 32), (36, 36), (33, 36), (30, 36), (28, 38), (27, 41), (30, 46), (30, 52), (28, 60), (30, 66)],
    [(113, -22), (114, -30), (115, -35), (120, -34), (129, -32), (132, -32), (135, -35), (140, -38), (145, -38), (150, -37), (153, -32), (153, -27), (150, -23), (146, -19), (142, -15), (142, -11), (137, -12), (135, -15), (132, -12), (130, -13), (126, -14), (122, -17), (118, -20)],
    [(95, 5), (100, 0), (105, -5), (110, -7), (115, -8), (120, -10), (125, -9), (130, -4), (135, -3), (140, -4), (140, -8), (130, -8), (120, -8), (110, -8), (100, -5), (95, 0)],
    [(130, 31), (132, 33), (135, 34), (138, 35), (140, 38), (141, 41), (143, 44), (145, 44), (142, 42), (140, 37), (137, 35), (133, 34)],
    [(-5, 50), (-3, 53), (-5, 56), (-3, 58), (-1, 57), (0, 53), (1, 51), (-3, 50)],
]


def _inside(lon, lat, poly):
    inside = False
    n = len(poly)
    j = n - 1
    for i in range(n):
        xi, yi = poly[i]
        xj, yj = poly[j]
        if (yi > lat) != (yj > lat):
            xint = (xj - xi) * (lat - yi) / (yj - yi) + xi
            if lon < xint:
                inside = not inside
        j = i
    return inside


def on_land(lon, lat):
    return any(_inside(lon, lat, p) for p in CONTINENTS)


def draw_map(draw, x0, y0, w, h, pins):
    draw.rectangle([x0, y0, x0 + w, y0 + h], fill=(232, 238, 244), outline=RULE)
    step = 6
    lat_top, lat_bot = 78.0, -56.0
    lon_l, lon_r = -170.0, 190.0
    yy = y0 + 4
    while yy < y0 + h - 2:
        lat = lat_top - (yy - y0) / h * (lat_top - lat_bot)
        xx = x0 + 4
        while xx < x0 + w - 2:
            lon = lon_l + (xx - x0) / w * (lon_r - lon_l)
            if on_land(lon, lat):
                draw.ellipse([xx - 1, yy - 1, xx + 1, yy + 1], fill=(70, 78, 92))
            xx += step
        yy += step

    def to_xy(lon, lat):
        return (x0 + (lon - lon_l) / (lon_r - lon_l) * w,
                y0 + (lat_top - lat) / (lat_top - lat_bot) * h)

    for pin in pins:
        px, py = to_xy(pin["lon"], pin["lat"])
        px += pin.get("dx", 0)
        py += pin.get("dy", 0)
        circle_number(draw, px, py, 9, pin["n"])


# ---- illustrated scenes (one per numbered story 1-13) ----
def scene(draw, n, x, y, w, h):
    d = draw
    if n == 1:  # Kospi crash: falling chart on dark red
        d.rectangle([x, y, x + w, y + h], fill=(64, 10, 10))
        for i in range(5):
            gx = x + 12 + i * (w - 24) // 4
            d.line([gx, y + 6, gx, y + h - 6], fill=(120, 40, 40), width=1)
        pts = [(x + 8, y + 18), (x + w * 0.3, y + 30), (x + w * 0.5, y + 26),
               (x + w * 0.68, y + 55), (x + w * 0.85, y + 82), (x + w - 8, y + h - 14)]
        d.line(pts, fill=(255, 120, 90), width=4)
        for px, py in pts[1:-1]:
            d.ellipse([px - 3, py - 3, px + 3, py + 3], fill=(255, 200, 180))
        f = font(26 if w > 200 else 16, bold=True)
        t = "-6.2%"
        d.text((x + w - d.textlength(t, font=f) - 8, y + h - 34), t, font=f, fill=(255, 255, 255))
        for i, cw in enumerate((26, 18, 30)):
            cx = x + 14 + i * 34
            d.rectangle([cx, y + h - 26 - cw, cx + 20, y + h - 26], fill=(20, 120, 90))
    elif n == 2:  # Shenzhou: rocket + station over Earth
        d.rectangle([x, y, x + w, y + h], fill=(8, 16, 44))
        for sx, sy in ((14, 12), (40, 26), (w - 30, 14), (w - 60, 30), (w // 2, 10), (30, h - 30)):
            d.ellipse([x + sx, y + sy, x + sx + 2, y + sy + 2], fill=(255, 255, 255))
        d.ellipse([x, y + h * 0.74, x + w, y + h * 1.35], fill=(38, 90, 160))
        d.ellipse([x, y + h * 0.74, x + w, y + h * 1.02], fill=(70, 140, 210))
        rx, ry = x + w * 0.16, y + h * 0.12
        d.polygon([(rx + 14, ry), (rx + 22, ry + 16), (rx + 22, ry + 58), (rx + 6, ry + 58), (rx + 6, ry + 16)], fill=(240, 240, 240))
        d.polygon([(rx + 14, ry - 12), (rx + 22, ry + 16), (rx + 6, ry + 16)], fill=(200, 40, 40))
        d.polygon([(rx + 14, ry + 58), (rx + 24, ry + 76), (rx + 4, ry + 76)], fill=(255, 150, 40))
        sx = x + w * 0.55
        d.rectangle([sx, y + h * 0.3, sx + 66, y + h * 0.3 + 14], fill=(220, 180, 80))
        d.rectangle([sx + 8, y + h * 0.3 - 12, sx + 58, y + h * 0.3 + 26], fill=(200, 200, 200))
        d.rectangle([sx - 26, y + h * 0.3 + 2, sx, y + h * 0.3 + 12], fill=(40, 80, 180))
        d.rectangle([sx + 66, y + h * 0.3 + 2, sx + 92, y + h * 0.3 + 12], fill=(40, 80, 180))
        f = font(11, bold=True)
        d.text((x + 8, y + h - 20), "SHENZHOU-24  ·  00:18 UTC", font=f, fill=(180, 210, 255))
    elif n == 3:  # Tariffs: port containers + 20% stamp
        d.rectangle([x, y, x + w, y + h], fill=(150, 190, 220))
        d.rectangle([x, y + h - 26, x + w, y + h], fill=(70, 80, 95))
        cols = [(200, 60, 50), (40, 110, 170), (220, 150, 40), (60, 140, 80)]
        for r in range(2):
            for c in range(4):
                cx = x + 10 + c * 52
                cy = y + h - 26 - (r + 1) * 24
                d.rectangle([cx, cy, cx + 48, cy + 22], fill=cols[(r + c) % 4], outline=(255, 255, 255))
        d.rectangle([x + w - 46, y + 8, x + w - 40, y + h - 26], fill=(40, 40, 40))
        d.rectangle([x + w - 70, y + 8, x + w - 12, y + 16], fill=(40, 40, 40))
        cx, cy = x + w * 0.30, y + h * 0.32
        d.ellipse([cx - 34, cy - 34, cx + 34, cy + 34], outline=(185, 28, 28), width=5)
        f = font(24 if w > 200 else 15, bold=True)
        t = "20%"
        d.text((cx - d.textlength(t, font=f) / 2, cy - 13), t, font=f, fill=(185, 28, 28))
    elif n == 4:  # Hormuz: tanker on fire
        d.rectangle([x, y, x + w, y + h], fill=(250, 170, 60))
        d.rectangle([x, y + h * 0.62, x + w, y + h], fill=(30, 60, 110))
        d.rectangle([x + w * 0.12, y + h * 0.48, x + w * 0.88, y + h * 0.62], fill=(30, 30, 30))
        d.rectangle([x + w * 0.62, y + h * 0.28, x + w * 0.70, y + h * 0.48], fill=(200, 200, 200))
        for fx, fh in ((0.25, 46), (0.42, 60), (0.60, 50), (0.78, 38)):
            px = x + w * fx
            d.polygon([(px - 14, y + h * 0.5), (px, y + h * 0.5 - fh), (px + 14, y + h * 0.5)],
                      fill=(255, 220, 60))
        for sx in (0.3, 0.55, 0.8):
            d.ellipse([x + w * sx - 12, y + 6, x + w * sx + 12, y + 26], fill=(90, 90, 90))
        d.line([x + 6, y + h - 8, x + w - 6, y + h - 8], fill=(255, 255, 255), width=2)
    elif n == 5:  # Solomon: island + flags
        d.rectangle([x, y, x + w, y + h], fill=(120, 200, 240))
        d.ellipse([x + w - 34, y + 8, x + w - 10, y + 32], fill=(255, 230, 120))
        d.rectangle([x, y + h * 0.66, x + w, y + h], fill=(20, 90, 160))
        d.polygon([(x + w * 0.1, y + h * 0.66), (x + w * 0.45, y + h * 0.3),
                   (x + w * 0.8, y + h * 0.66)], fill=(40, 130, 60))
        d.rectangle([x + w * 0.44, y + h * 0.3, x + w * 0.46, y + h * 0.62], fill=(110, 70, 30))
        d.polygon([(x + w * 0.46, y + h * 0.3), (x + w * 0.62, y + h * 0.38),
                   (x + w * 0.46, y + h * 0.46)], fill=(30, 90, 200))
        d.rectangle([x + w * 0.14, y + h * 0.55, x + w * 0.30, y + h * 0.66], fill=(240, 240, 240))
        d.rectangle([x + w * 0.14, y + h * 0.55, x + w * 0.22, y + h * 0.66], fill=(200, 40, 40))
    elif n == 6:  # UK energy: meter gauge + bolt
        d.rectangle([x, y, x + w, y + h], fill=(245, 220, 140))
        cx, cy, r = x + w * 0.5, y + h * 0.62, min(w, h) * 0.36
        d.pieslice([cx - r, cy - r, cx + r, cy + r], 180, 360, fill=(255, 255, 255), outline=INK, width=2)
        d.pieslice([cx - r, cy - r, cx + r, cy + r], 300, 360, fill=(185, 28, 28))
        d.line([cx, cy, cx + r * 0.75, cy - r * 0.55], fill=RED, width=3)
        d.ellipse([cx - 5, cy - 5, cx + 5, cy + 5], fill=INK)
        d.polygon([(x + w * 0.12, y + 12), (x + w * 0.22, y + 12), (x + w * 0.15, y + 30),
                   (x + w * 0.24, y + 30), (x + w * 0.10, y + 52), (x + w * 0.17, y + 30)],
                  fill=(255, 180, 0))
        f = font(15 if w > 200 else 11, bold=True)
        d.text((x + w - 52, y + 8), "+36%", font=f, fill=RED)
    elif n == 7:  # Java mine: earth cross-section + shaft
        d.rectangle([x, y, x + w, y + h], fill=(150, 105, 60))
        d.rectangle([x, y, x + w, y + h * 0.3], fill=(135, 200, 110))
        d.rectangle([x + w * 0.42, y + h * 0.3, x + w * 0.58, y + h], fill=(40, 25, 12))
        for hx, hy in ((0.2, 0.45), (0.75, 0.55), (0.3, 0.75), (0.72, 0.8)):
            d.ellipse([x + w * hx - 7, y + h * hy - 5, x + w * hx + 7, y + h * hy + 5], fill=(255, 220, 0))
            d.ellipse([x + w * hx - 2, y + h * hy + 5, x + w * hx + 2, y + h * hy + 12], fill=(60, 40, 20))
        d.polygon([(x + w * 0.5, y + h * 0.3), (x + w * 0.62, y + h * 0.55),
                   (x + w * 0.38, y + h * 0.55)], fill=(255, 240, 160))
        f = font(12 if w > 200 else 10, bold=True)
        d.text((x + 8, y + 6), "26 TRAPPED", font=f, fill=(255, 255, 255))
    elif n == 8:  # Ebola: clinic + ambulance
        d.rectangle([x, y, x + w, y + h], fill=(220, 235, 245))
        d.rectangle([x + w * 0.12, y + h * 0.3, x + w * 0.62, y + h * 0.78], fill=(255, 255, 255), outline=INK)
        d.rectangle([x + w * 0.24, y + h * 0.3, x + w * 0.5, y + h * 0.3 + 6], fill=RED)
        d.rectangle([x + w * 0.34, y + h * 0.3 - 6, x + w * 0.4, y + h * 0.3 + 14], fill=RED)
        d.rectangle([x + w * 0.62, y + h * 0.58, x + w * 0.92, y + h * 0.8], fill=(255, 255, 255), outline=RED, width=2)
        d.rectangle([x + w * 0.72, y + h * 0.62, x + w * 0.78, y + h * 0.68], fill=RED)
        d.rectangle([x + w * 0.70, y + h * 0.58, x + w * 0.84, y + h * 0.62], fill=RED)
        d.ellipse([x + w * 0.66, y + h * 0.78, x + w * 0.66 + 10, y + h * 0.78 + 10], fill=INK)
        d.ellipse([x + w * 0.84, y + h * 0.78, x + w * 0.84 + 10, y + h * 0.78 + 10], fill=INK)
        d.rectangle([x, y + h - 12, x + w, y + h], fill=(120, 120, 120))
    elif n == 9:  # Kyiv ships: night sea, drone, blast
        d.rectangle([x, y, x + w, y + h], fill=(12, 24, 60))
        d.ellipse([x + w - 30, y + 8, x + w - 8, y + 30], fill=(240, 240, 220))
        d.rectangle([x, y + h * 0.62, x + w, y + h], fill=(20, 50, 100))
        d.rectangle([x + w * 0.1, y + h * 0.5, x + w * 0.5, y + h * 0.62], fill=(10, 10, 10))
        d.rectangle([x + w * 0.28, y + h * 0.36, x + w * 0.34, y + h * 0.5], fill=(10, 10, 10))
        d.rectangle([x + w * 0.58, y + h * 0.44, x + w * 0.88, y + h * 0.62], fill=(10, 10, 10))
        for k in range(8):
            ang = k * math.pi / 4
            d.line([x + w * 0.72 + 16 * math.cos(ang), y + h * 0.3 + 16 * math.sin(ang),
                    x + w * 0.72 + 30 * math.cos(ang), y + h * 0.3 + 30 * math.sin(ang)],
                   fill=(255, 200, 40), width=3)
        d.ellipse([x + w * 0.72 - 8, y + h * 0.3 - 8, x + w * 0.72 + 8, y + h * 0.3 + 8], fill=(255, 120, 0))
        d.rectangle([x + w * 0.45, y + h * 0.18, x + w * 0.45 + 12, y + h * 0.18 + 6], fill=(180, 180, 180))
    elif n == 10:  # Cyber: dark building + padlock
        d.rectangle([x, y, x + w, y + h], fill=(16, 20, 32))
        d.rectangle([x + w * 0.2, y + h * 0.25, x + w * 0.62, y + h], fill=(50, 60, 90))
        for r in range(4):
            for c in range(3):
                wx = x + w * (0.26 + c * 0.12)
                wy = y + h * (0.32 + r * 0.17)
                d.rectangle([wx, wy, wx + 12, wy + 9], fill=(90, 220, 120) if (r + c) % 3 else (255, 220, 80))
        cx, cy = x + w * 0.78, y + h * 0.55
        d.rectangle([cx - 18, cy - 6, cx + 18, cy + 22], fill=(220, 180, 40))
        d.arc([cx - 12, cy - 22, cx + 12, cy + 2], 180, 360, fill=(220, 180, 40), width=5)
        d.ellipse([cx - 3, cy + 2, cx + 3, cy + 8], fill=INK)
        f = font(10, bold=True)
        d.text((x + 8, y + 6), "01001101 01100001", font=f, fill=(90, 220, 120))
    elif n == 11:  # Cricket: pitch + batsman
        d.rectangle([x, y, x + w, y + h], fill=(60, 140, 70))
        d.rectangle([x + w * 0.3, y, x + w * 0.7, y + h], fill=(210, 180, 120))
        d.rectangle([x + w * 0.44, y + h * 0.15, x + w * 0.5, y + h * 0.85], fill=(240, 240, 240))
        d.ellipse([x + w * 0.52, y + h * 0.2, x + w * 0.52 + 14, y + h * 0.2 + 14], fill=(200, 120, 80))
        d.polygon([(x + w * 0.53, y + h * 0.32), (x + w * 0.62, y + h * 0.55),
                   (x + w * 0.56, y + h * 0.58), (x + w * 0.47, y + h * 0.36)], fill=(200, 120, 80))
        d.rectangle([x + w * 0.6, y + h * 0.5, x + w * 0.62, y + h * 0.72], fill=(220, 180, 120))
        d.ellipse([x + w * 0.68, y + h * 0.66, x + w * 0.68 + 8, y + h * 0.66 + 8], fill=(200, 40, 40))
        for sx in (0.47, 0.49, 0.51):
            d.rectangle([x + w * sx, y + h * 0.82, x + w * sx + 3, y + h * 0.95], fill=(255, 220, 100))
        f = font(13 if w > 200 else 10, bold=True)
        d.text((x + 8, y + h - 22), "204 off 53", font=f, fill=(255, 255, 255))
    elif n == 12:  # Medal: gold disc + ribbon
        d.rectangle([x, y, x + w, y + h], fill=(30, 40, 90))
        cx, cy = x + w * 0.5, y + h * 0.58
        d.polygon([(cx - 26, y + 6), (cx - 8, y + 6), (cx - 2, cy - 22), (cx + 8, y + 6),
                   (cx + 26, y + 6), (cx + 14, cy - 22), (cx, y + 6)], fill=(180, 40, 40))
        d.ellipse([cx - 34, cy - 34, cx + 34, cy + 34], fill=(230, 190, 60), outline=(160, 120, 20), width=3)
        d.ellipse([cx - 24, cy - 24, cx + 24, cy + 24], outline=(160, 120, 20), width=2)
        for k in range(5):
            ang = -math.pi / 2 + k * 2 * math.pi / 5
            d.ellipse([cx + 13 * math.cos(ang) - 3, cy + 13 * math.sin(ang) - 3,
                       cx + 13 * math.cos(ang) + 3, cy + 13 * math.sin(ang) + 3], fill=(255, 255, 255))
    elif n == 13:  # Aden: desert convoy
        d.rectangle([x, y, x + w, y + h], fill=(250, 200, 110))
        d.ellipse([x + w - 36, y + 8, x + w - 12, y + 32], fill=(255, 240, 160))
        d.polygon([(x, y + h * 0.45), (x + w * 0.3, y + h * 0.2), (x + w * 0.6, y + h * 0.45)],
                  fill=(180, 120, 60))
        d.rectangle([x, y + h * 0.62, x + w, y + h], fill=(220, 170, 90))
        for tx in (0.12, 0.42, 0.68):
            d.rectangle([x + w * tx, y + h * 0.66, x + w * (tx + 0.2), y + h * 0.82], fill=(90, 70, 40))
            d.ellipse([x + w * (tx + 0.03), y + h * 0.82, x + w * (tx + 0.03) + 9, y + h * 0.82 + 9], fill=INK)
            d.ellipse([x + w * (tx + 0.13), y + h * 0.82, x + w * (tx + 0.13) + 9, y + h * 0.82 + 9], fill=INK)
        d.line([x + w * 0.1, y + h * 0.9, x + w * 0.95, y + h * 0.9], fill=(255, 255, 255), width=2)


# ---- page layout ----
def truncate(draw, text, fnt, width):
    if draw.textlength(text, font=fnt) <= width:
        return text
    while text and draw.textlength(text + "…", font=fnt) > width:
        text = text[:-1]
    return text + "…"


def main():
    with open(os.path.join(HERE, "stories_20261125.json"), encoding="utf-8") as f:
        data = json.load(f)
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # Masthead: paper name + giant date
    name = "T H E   W O R L D   O N   W E D N E S D A Y"
    nf = font(13, bold=True)
    d.text(((W - d.textlength(name, font=nf)) / 2, 8), name, font=nf, fill=RED)
    df = font(40, bold=True, serif=True)
    date = data["date"]
    d.text(((W - d.textlength(date, font=df)) / 2, 26), date, font=df, fill=INK)
    d.line([16, 72, 1008, 72], fill=INK, width=2)
    d.line([16, 75, 1008, 75], fill=INK, width=1)

    # UTC strip
    d.rectangle([16, 79, 1008, 103], fill=NAVY)
    uf = font(10, bold=True)
    label = "THE DAY IN UTC"
    d.text((26, 85), label, font=uf, fill=(255, 220, 90))
    items = [f"{t}  {what}" for t, what in data["utc_strip"]]
    strip = "   ·   ".join(items)
    sf = font(10)
    d.text((26 + d.textlength(label, font=uf) + 18, 85), strip, font=sf, fill=(255, 255, 255))

    # Big red numbers
    cell = 992 / 6
    vf = font(28, bold=True)
    lf = font(8)
    for i, num in enumerate(data["numbers"]):
        cx = 16 + cell * i + cell / 2
        v = num["value"]
        d.text((cx - d.textlength(v, font=vf) / 2, 108), v, font=vf, fill=RED)
        lab = truncate(d, num["label"], lf, cell - 8)
        d.text((cx - d.textlength(lab, font=lf) / 2, 140), lab, font=lf, fill=SOFT)
    d.line([16, 154, 1008, 154], fill=RULE, width=1)

    # Three illustrated leads
    leads = data["leads"]
    xs = [16, 351, 686]
    for col, lead in enumerate(leads):
        x = xs[col]
        scene(d, lead["n"], x, 158, 322, 118)
        d.rectangle([x, 276, x + 322, 278], fill=RULE)
        cy = 288
        circle_number(d, x + 9, cy, 9, lead["n"])
        bw = badge_chip(d, x + 24, cy - 7, lead["badge"])
        kf = font(9, bold=True)
        d.text((x + 24 + bw + 7, cy - 6), lead["kicker"], font=kf, fill=INK)
        hf = font(17, bold=True, serif=True)
        y = text_block(d, x, 300, lead["headline"], hf, INK, 322, leading=20)
        y = text_block(d, x, y + 3, lead["deck"], font(10), SOFT, 322, leading=13)
        sf2 = font(8)
        d.text((x, 380), lead["place"] + "  ·  " + lead["source"], font=sf2, fill=SOFT)
    d.line([16, 392, 1008, 392], fill=INK, width=1)

    # Grid: 10 illustrated stories, 5 x 2
    grid = data["grid"]
    gx = [16, 216, 416, 616, 816]
    gy = [398, 536]
    for idx, story in enumerate(grid):
        col, row = idx % 5, idx // 5
        x, y0 = gx[col], gy[row]
        scene(d, story["n"], x, y0, 190, 62)
        cy = y0 + 74
        circle_number(d, x + 7, cy, 8, story["n"])
        bw = badge_chip(d, x + 19, cy - 7, story["badge"])
        kf = font(8, bold=True)
        d.text((x + 19 + bw + 5, cy - 6), truncate(d, story["kicker"], kf, 190 - 24 - bw), font=kf, fill=INK)
        hf = font(11, bold=True, serif=True)
        text_block(d, x, y0 + 88, story["headline"], hf, INK, 190, leading=13)
        d.text((x, y0 + 120), truncate(d, story["place"] + " · " + story["source"], font(8), 190),
               font=font(8), fill=SOFT)
    d.line([16, 668, 1008, 668], fill=RULE, width=1)

    # World map with numbered pins 1-13
    draw_map(d, 16, 674, 320, 196, data["pins"])
    mf = font(8, bold=True)
    cap = "WORLD MAP — PINS 1–13 MARK THE ILLUSTRATED STORIES"
    d.text((16, 874), truncate(d, cap, mf, 320), font=mf, fill=SOFT)

    # ALSO: 23 more stories, numbered 14-36, two columns
    ax = [348, 686]
    tf = font(12, bold=True)
    d.text((348, 674), "ALSO — 23 MORE STORIES", font=tf, fill=INK)
    d.line([348, 692, 1008, 692], fill=INK, width=1)
    also = data["also"]
    hf2 = font(9)
    bf = font(7, bold=True)
    sf3 = font(8)
    for idx, story in enumerate(also):
        col = 0 if idx < 12 else 1
        row = idx if idx < 12 else idx - 12
        x = ax[col]
        y = 700 + row * 17
        circle_number(d, x + 7, y + 6, 7, story["n"])
        badge = BADGE_SHORT[story["badge"]]
        src = story["source"]
        tail = f"  {badge} {src}"
        avail = 322 - 18 - d.textlength(tail, font=bf) - 4
        head = truncate(d, story["headline"], hf2, avail)
        d.text((x + 18, y), head, font=hf2, fill=INK)
        tx = x + 18 + d.textlength(head, font=hf2) + 4
        d.text((tx, y + 1), badge, font=bf, fill=BADGE[story["badge"]])
        d.text((tx + d.textlength(badge, font=bf) + 3, y), src, font=sf3, fill=SOFT)

    # LEFT OUT box
    d.rectangle([16, 904, 1008, 950], outline=RED, width=2, fill=(252, 240, 238))
    lf2 = font(10, bold=True)
    d.text((26, 910), "LEFT OUT — NOT 25 NOVEMBER", font=lf2, fill=RED)
    items = [f"{what} ({when})" for what, when in data["left_out"]]
    line1 = "  ·  ".join(items[:3])
    line2 = "  ·  ".join(items[3:])
    d.text((26, 926), line1, font=font(10), fill=INK)
    d.text((26, 938), line2, font=font(10), fill=INK)

    # Footer: badge legend, region bars, sources
    lx = 16
    leg = font(9)
    d.text((lx, 958), "HOW WE KNOW IT:", font=font(9, bold=True), fill=INK)
    lx += d.textlength("HOW WE KNOW IT:  ", font=font(9, bold=True))
    for label, meaning in (("CONFIRMED", "2+ outlets or official source"),
                           ("REPORTED", "a single wire"),
                           ("CLAIM", "one side's statement"),
                           ("ONGOING", "still developing")):
        r = 4
        d.ellipse([lx, 961, lx + 8, 969], fill=BADGE[label])
        lx += 11
        seg = f"{label} — {meaning}      "
        d.text((lx, 958), seg, font=leg, fill=INK)
        lx += d.textlength(seg, font=leg)
    rx = 16
    order = ["ASIA-PACIFIC", "AMERICAS", "EUROPE", "MIDDLE EAST", "AFRICA"]
    for region in order:
        count = data["regions"][region]
        rf = font(8, bold=True)
        d.text((rx, 978), region, font=rf, fill=INK)
        bx = rx + d.textlength(region, font=rf) + 6
        d.rectangle([bx, 980, bx + 110, 986], fill=(225, 220, 210))
        d.rectangle([bx, 980, bx + 110 * count / 10, 986], fill=NAVY)
        d.text((bx + 116, 978), str(count), font=rf, fill=INK)
        rx = bx + 116 + 22
    srcs = ("Sources: Reuters · AFP · Xinhua · WHO · CNN · BBC · RFE/RL · WH News · "
            "BusinessWorld · Jagran Josh · The Hindu · Dell — all 36 stories verified to "
            + data["verified_to"] + ".")
    d.text((16, 996), truncate(d, srcs, font(8), 992), font=font(8), fill=SOFT)

    out = os.path.join(HERE, "entry.png")
    img.save(out, format="PNG", optimize=True)
    size = os.path.getsize(out)
    import hashlib
    sha = hashlib.sha256(open(out, "rb").read()).hexdigest()
    print(f"entry.png {size} bytes sha256 {sha}")
    assert size <= 1048576, "entry.png over 1 MiB"
    assert img.size == (1024, 1024)


if __name__ == "__main__":
    main()
