#!/usr/bin/env python3
"""World News, 23 November 2026 -- newspaper front page infographic.

Draws a 1024x1024 PNG with Pillow: masthead, a hero panel with a stylised
map of the Strait of Hormuz, six story cards in a 2x3 grid, and a bottom
news ticker. No network, no clock, no randomness: two runs are byte-identical.
"""

import os

from PIL import Image, ImageDraw, ImageFont

CANVAS_W = 1024
CANVAS_H = 1024

PAPER = (247, 243, 232)
INK = (24, 24, 22)
RED = (178, 34, 28)
NAVY = (18, 42, 66)
TEAL = (23, 78, 102)
SEA = (31, 94, 122)
LAND = (214, 196, 158)
LAND2 = (198, 178, 138)
GOLD = (196, 148, 44)
GREY = (110, 108, 100)
LIGHT_LINE = (190, 184, 168)
CARD_BG = (255, 253, 246)
SMOKE = (150, 148, 142)

FONT_DIR = "/usr/share/fonts/truetype/dejavu"


def load_font(name, size):
    return ImageFont.truetype(os.path.join(FONT_DIR, name), size)


F_TITLE = load_font("DejaVuSerif-Bold.ttf", 66)
F_DATE = load_font("DejaVuSans-Bold.ttf", 19)
F_KICK = load_font("DejaVuSans-Bold.ttf", 16)
F_HERO = load_font("DejaVuSerif-Bold.ttf", 38)
F_DECK = load_font("DejaVuSans.ttf", 20)
F_CARD_H = load_font("DejaVuSerif-Bold.ttf", 21)
F_CARD_D = load_font("DejaVuSans.ttf", 15)
F_TICK = load_font("DejaVuSans-Bold.ttf", 15)
F_MAP = load_font("DejaVuSans-Bold.ttf", 15)
F_MAP_S = load_font("DejaVuSans.ttf", 13)


def fit_lines(draw, text, font, max_w, max_lines=3):
    """Greedy word wrap; returns at most max_lines lines, last one ellipsised."""
    words = text.split()
    lines = []
    cur = ""
    for word in words:
        trial = word if not cur else cur + " " + word
        if draw.textlength(trial, font=font) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
            if len(lines) == max_lines:
                break
    if cur and len(lines) < max_lines:
        lines.append(cur)
    if len(lines) == max_lines and words:
        joined = " ".join(lines)
        if len(joined) < len(text):
            last = lines[-1]
            while last and draw.textlength(last + "...", font=font) > max_w:
                last = last.rsplit(" ", 1)[0] if " " in last else ""
            lines[-1] = last + "..."
    return lines


def put_lines(draw, lines, font, x, y, fill, spacing=4):
    for line in lines:
        draw.text((x, y), line, font=font, fill=fill)
        y += font.size + spacing
    return y


def rule(draw, x0, y, x1, fill=INK, width=2):
    draw.line([(x0, y), (x1, y)], fill=fill, width=width)


def draw_tanker(draw, cx, cy, scale, hull=(40, 40, 38), deck=(210, 205, 190)):
    """Small tanker silhouette centred at (cx, cy); scale ~1.0."""
    w = int(74 * scale)
    h = int(16 * scale)
    draw.polygon(
        [(cx - w // 2, cy - h // 2), (cx + w // 2, cy - h // 2),
         (cx + w // 2 - 8, cy + h // 2), (cx - w // 2 + 10, cy + h // 2)],
        fill=hull,
    )
    draw.rectangle([cx - w // 4, cy - h // 2 - 10, cx - w // 4 + 12, cy - h // 2],
                   fill=deck)
    draw.rectangle([cx + w // 6, cy - h // 2 - 7, cx + w // 6 + 8, cy - h // 2],
                   fill=deck)
    draw.line([(cx - w // 2 - 6, cy + h // 2 + 4), (cx + w // 2 + 6, cy + h // 2 + 4)],
              fill=(255, 255, 255), width=2)


def draw_burst(draw, cx, cy, r, core=(255, 122, 26), mid=(230, 60, 20)):
    """Starburst flame."""
    pts = []
    for i in range(12):
        ang = i * 30
        rad = r if i % 2 == 0 else r * 0.55
        import math
        pts.append((cx + rad * math.cos(math.radians(ang)),
                    cy + rad * math.sin(math.radians(ang))))
    draw.polygon(pts, fill=mid)
    draw.ellipse([cx - r * 0.45, cy - r * 0.45, cx + r * 0.45, cy + r * 0.45],
                 fill=core)


def draw_smoke(draw, cx, cy, r):
    for dx, dy, rr in [(-14, 6, 11), (0, -6, 13), (14, 4, 10), (4, -16, 9)]:
        draw.ellipse([cx + dx - rr, cy + dy - rr, cx + dx + rr, cy + dy + rr],
                     fill=SMOKE)


# ---------------------------------------------------------------- masthead

def paint_masthead(draw):
    draw.text((24, 8), "No. 327", font=F_MAP_S, fill=GREY)
    draw.text((1024 - 24 - draw.textlength("PRICE: ONE IMAGE", font=F_MAP_S), 8),
              "PRICE: ONE IMAGE", font=F_MAP_S, fill=GREY)
    title = "WORLD NEWS"
    tw = draw.textlength(title, font=F_TITLE)
    draw.text(((1024 - tw) / 2, 26), title, font=F_TITLE, fill=INK)
    rule(draw, 24, 104, 1000, width=3)
    date = "MONDAY, 23 NOVEMBER 2026"
    dw = draw.textlength(date, font=F_DATE)
    draw.text(((1024 - dw) / 2, 112), date, font=F_DATE, fill=RED)
    rule(draw, 24, 140, 1000, width=1)


# ---------------------------------------------------------------- hero

def paint_hero(draw):
    x0, y0, x1, y1 = 24, 150, 1000, 486
    draw.rectangle([x0, y0, x1, y1], outline=INK, width=2)
    draw.text((x0 + 16, y0 + 10), "LEAD STORY  •  GULF CRISIS",
              font=F_KICK, fill=RED)
    headline = "TANKER WAR IN THE STRAIT OF HORMUZ"
    lines = fit_lines(draw, headline, F_HERO, x1 - x0 - 32, 2)
    put_lines(draw, lines, F_HERO, x0 + 16, y0 + 34, INK, spacing=2)
    deck = ("At least 25 tankers struck in and around the strait in seven days "
            "as Iran's navy reports ships hitting mines and UK maritime "
            "authorities report projectile strikes. Gulf oil flow drops sharply.")
    dlines = fit_lines(draw, deck, F_DECK, x1 - x0 - 32, 2)
    put_lines(draw, dlines, F_DECK, x0 + 16, y0 + 118, (52, 52, 48), spacing=3)

    # --- stylised map of the strait
    mx0, my0, mx1, my1 = x0 + 14, y0 + 178, x1 - 14, y1 - 14
    draw.rectangle([mx0, my0, mx1, my1], fill=SEA)
    # strait channel (lighter water band, drawn before the landmasses)
    draw.polygon([(mx0, my0 + 58), (mx1, my0 + 46), (mx1, my0 + 90),
                  (mx0, my0 + 100)], fill=(52, 128, 158))
    # Iran landmass (top, full width)
    draw.polygon([(mx0, my0), (mx1, my0), (mx1, my0 + 28),
                  (640, my0 + 42), (300, my0 + 34), (mx0, my0 + 48)],
                 fill=LAND)
    # Oman landmass (bottom right only; bottom left stays open sea)
    draw.polygon([(560, my1), (mx1, my1), (mx1, my1 - 30),
                  (760, my1 - 52), (560, my1 - 56)], fill=LAND2)
    draw.text((mx0 + 16, my0 + 8), "IRAN", font=F_MAP, fill=(90, 74, 52))
    draw.text((mx1 - 70, my1 - 24), "OMAN", font=F_MAP, fill=(90, 74, 52))
    draw.text((mx0 + 16, my1 - 24), "PERSIAN GULF", font=F_MAP_S,
              fill=(220, 235, 240))
    draw.text((mx1 - 150, my0 + 30), "GULF OF OMAN", font=F_MAP_S,
              fill=(220, 235, 240))
    draw.text((mx0 + 16, my0 + 50), "STRAIT OF HORMUZ", font=F_MAP,
              fill=(255, 255, 255))
    # tankers sailing in the channel
    draw_tanker(draw, 330, my0 + 78, 1.0)
    draw_tanker(draw, 520, my0 + 74, 0.9)
    draw_tanker(draw, 690, my0 + 70, 0.85)
    draw_burst(draw, 430, my0 + 80, 20)
    draw_smoke(draw, 430, my0 + 48, 10)
    draw_burst(draw, 600, my0 + 88, 14)
    # strike markers along the channel
    for sx, sy in [(280, my0 + 92), (380, my0 + 66), (480, my0 + 92),
                   (570, my0 + 62), (640, my0 + 92), (730, my0 + 84)]:
        draw.ellipse([sx - 4, sy - 4, sx + 4, sy + 4], fill=RED,
                     outline=(255, 255, 255), width=1)
    # callout, top right over open sea
    cx0, cy0 = mx1 - 218, my0 + 52
    draw.rectangle([cx0, cy0, cx0 + 204, cy0 + 40], fill=(255, 253, 246),
                   outline=RED, width=2)
    draw.text((cx0 + 10, cy0 + 6), "25 TANKERS STRUCK", font=F_KICK, fill=RED)
    draw.text((cx0 + 10, cy0 + 24), "in seven days", font=F_MAP_S, fill=INK)


# ---------------------------------------------------------------- cards

def icon_globe(draw, bx, by, s):
    cx, cy, r = bx + 52, by + 46, 34
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(52, 128, 158),
                 outline=NAVY, width=2)
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], outline=(255, 255, 255), width=1)
    draw.line([(cx - r, cy), (cx + r, cy)], fill=(255, 255, 255), width=1)
    draw.ellipse([cx - 12, cy - r, cx + 12, cy + r], outline=(255, 255, 255), width=1)
    draw.line([(cx + 8, cy - 20), (cx - 6, cy + 2), (cx + 12, cy + 18)],
              fill=RED, width=3)


def icon_drone(draw, bx, by, s):
    draw.polygon([(bx + 18, by + 66), (bx + 86, by + 66), (bx + 78, by + 84),
                  (bx + 28, by + 84)], fill=NAVY)
    draw.rectangle([bx + 46, by + 44, bx + 58, by + 66], fill=NAVY)
    draw.line([(bx + 52, by + 44), (bx + 52, by + 30)], fill=INK, width=2)
    draw.ellipse([bx + 38, by + 24, bx + 66, by + 38], fill=GREY)
    draw.line([(bx + 30, by + 30), (bx + 74, by + 30)], fill=INK, width=2)
    draw_burst(draw, bx + 84, by + 30, 13)


def icon_missile(draw, bx, by, s):
    draw.polygon([(bx + 24, by + 78), (bx + 44, by + 78), (bx + 66, by + 40),
                  (bx + 74, by + 24), (bx + 58, by + 30), (bx + 40, by + 62)],
                 fill=(90, 90, 88))
    draw.polygon([(bx + 74, by + 24), (bx + 86, by + 12), (bx + 80, by + 30)],
                 fill=RED)
    draw_burst(draw, bx + 30, by + 84, 10)
    draw.ellipse([bx + 60, by + 52, bx + 92, by + 88], outline=GOLD, width=3)
    draw.line([(bx + 76, by + 52), (bx + 76, by + 88)], fill=GOLD, width=2)


def icon_space(draw, bx, by, s):
    cx, cy, r = bx + 46, by + 52, 24
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(196, 148, 44),
                 outline=(120, 90, 20), width=2)
    for ox, oy, orr in [(-8, -6, 4), (6, 8, 5), (10, -8, 3)]:
        draw.ellipse([cx + ox - orr, cy + oy - orr, cx + ox + orr, cy + oy + orr],
                     fill=(150, 110, 30))
    draw.ellipse([bx + 6, by + 14, bx + 96, by + 92], outline=NAVY, width=2)
    draw.rectangle([bx + 78, by + 18, bx + 92, by + 30], fill=NAVY)
    draw.line([(bx + 85, by + 30), (bx + 74, by + 40)], fill=NAVY, width=2)


def icon_chart(draw, bx, by, s):
    draw.line([(bx + 14, by + 84), (bx + 14, by + 16)], fill=INK, width=2)
    draw.line([(bx + 14, by + 84), (bx + 92, by + 84)], fill=INK, width=2)
    draw.line([(bx + 18, by + 28), (bx + 38, by + 44), (bx + 54, by + 38),
               (bx + 74, by + 62), (bx + 88, by + 74)], fill=RED, width=4)
    draw.polygon([(bx + 88, by + 74), (bx + 76, by + 68), (bx + 82, by + 82)],
                 fill=RED)


def icon_block(draw, bx, by, s):
    draw.rectangle([bx + 26, by + 18, bx + 78, by + 88], fill=(150, 142, 128),
                   outline=INK, width=2)
    for wy in (28, 46, 64):
        for wx in (34, 50, 66):
            draw.rectangle([bx + wx, by + wy, bx + wx + 8, by + wy + 8],
                           fill=(60, 60, 58))
    draw.polygon([(bx + 26, by + 18), (bx + 52, by + 6), (bx + 78, by + 18)],
                 fill=RED)
    draw_smoke(draw, bx + 52, by - 2, 8)


STORIES = [
    ("CLIMATE", "COP31 talks collapse with no deal",
     "Fossil-fuel phase-out deadlock ends the summit empty-handed.",
     icon_globe),
    ("UKRAINE WAR", "Sea drones hit Russian warship in Libya",
     "Merkury severely damaged at Benghazi naval base; later capsized.",
     icon_drone),
    ("NATO", "Poland: fallen objects were Russian missiles",
     "Warsaw confirms cruise missiles; NATO allies to meet.",
     icon_missile),
    ("SPACE", "BepiColombo enters orbit around Mercury",
     "Eight-year journey ends; only the second mission ever to do so.",
     icon_space),
    ("MARKETS", "Markets plunge on AI-bubble fears",
     "Taiwan shares down 17.5% in a week; Kospi falls over 3%.",
     icon_chart),
    ("UKRAINE", "Russian drone hits Kyiv apartment block",
     "2 killed, 11 missing in Dymer, north of Kyiv, incl. two children.",
     icon_block),
]


def paint_cards(draw):
    gx, gy = 24, 500
    cw, ch, gap = 480, 132, 16
    for i, (kick, head, deck, icon) in enumerate(STORIES):
        row, col = divmod(i, 2)
        x0 = gx + col * (cw + gap)
        y0 = gy + row * (ch + gap)
        draw.rectangle([x0, y0, x0 + cw, y0 + ch], fill=CARD_BG,
                       outline=LIGHT_LINE, width=1)
        draw.line([(x0, y0), (x0, y0 + ch)], fill=RED, width=4)
        icon(draw, x0 + 12, y0 + 14, 1.0)
        tx = x0 + 128
        draw.text((tx, y0 + 10), kick, font=F_KICK, fill=RED)
        hlines = fit_lines(draw, head, F_CARD_H, cw - 128 - 14, 2)
        y = put_lines(draw, hlines, F_CARD_H, tx, y0 + 30, INK, spacing=1)
        dlines = fit_lines(draw, deck, F_CARD_D, cw - 128 - 14, 2)
        put_lines(draw, dlines, F_CARD_D, tx, y + 2, (70, 68, 62), spacing=2)


# ---------------------------------------------------------------- ticker

TICKER = [
    "Democrats win biggest House majority since 1992",
    "Liverpool 4-0 Man Utd",
    "Marquez ties MotoGP title record",
    "Cikande candy factory fire kills 24",
    "Lahore most polluted city - AQI 538",
    "Shuri Castle main hall restored",
]


def paint_ticker(draw):
    y0, y1 = 928, 1000
    draw.rectangle([0, y0, 1024, y1], fill=NAVY)
    draw.text((24, y0 + 8), "LATEST", font=F_TICK, fill=GOLD)
    line1 = "  •  ".join(TICKER[:3])
    line2 = "  •  ".join(TICKER[3:])
    draw.text((24, y0 + 30), line1, font=F_TICK, fill=(255, 255, 255))
    draw.text((24, y0 + 52), line2, font=F_TICK, fill=(220, 228, 236))


# ---------------------------------------------------------------- main

def build():
    img = Image.new("RGB", (CANVAS_W, CANVAS_H), PAPER)
    draw = ImageDraw.Draw(img)
    paint_masthead(draw)
    paint_hero(draw)
    paint_cards(draw)
    paint_ticker(draw)
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    img.save(os.path.join(out_dir, "entry.png"))


if __name__ == "__main__":
    build()
