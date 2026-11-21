#!/usr/bin/env python3
"""SOLUNARA — The Poster for a Place That Isn't There.
Flat-vector art-deco travel poster, drawn procedurally with PIL.
A floating isle with a temple; the sea climbs UP to it in a waterfall.
1024x1024, deterministic (no randomness, no network)."""
import math
from PIL import Image, ImageDraw, ImageFont

W = H = 1024
SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"

CREAM = (250, 240, 214)
GOLD = (212, 164, 84)
GOLD_LT = (233, 196, 120)
INK = (38, 32, 48)
SEA_DK = (16, 92, 110)
SEA_MD = (23, 128, 148)
SEA_LT = (64, 178, 186)
ROCK = (58, 52, 74)
ROCK_LT = (84, 76, 104)
WHITE = (250, 246, 236)
PINK = (214, 74, 130)
PINK_LT = (232, 120, 164)


def lerp(a, b, t):
    return tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(3))


def vgrad(draw, x0, y0, x1, y1, c_top, c_bot):
    h = max(1, y1 - y0)
    for y in range(y0, y1):
        c = lerp(c_top, c_bot, (y - y0) / h)
        draw.line([(x0, y), (x1, y)], fill=c)


def text_center(draw, cx, y, s, font, fill, tracking=0):
    """Draw text centered at cx, with letter tracking (px between chars)."""
    if tracking == 0:
        w = draw.textlength(s, font=font)
        draw.text((cx - w / 2, y), s, font=font, fill=fill)
        return
    widths = [draw.textlength(ch, font=font) for ch in s]
    total = sum(widths) + tracking * (len(s) - 1)
    x = cx - total / 2
    for ch, w in zip(s, widths):
        draw.text((x, y), ch, font=font, fill=fill)
        x += w + tracking


def main():
    img = Image.new("RGB", (W, H), CREAM)
    d = ImageDraw.Draw(img, "RGBA")

    # ---- frame ----
    d.rectangle([0, 0, W - 1, H - 1], outline=GOLD, width=10)
    d.rectangle([18, 18, W - 19, H - 19], outline=GOLD, width=2)
    # inner picture area
    X0, Y0, X1, Y1 = 26, 26, W - 27, H - 27
    HOR = 640  # horizon / sea line

    # ---- sky: deep indigo -> rose -> peach -> gold ----
    sky_stops = [
        (Y0, (44, 44, 96)),
        (220, (94, 78, 138)),
        (380, (188, 110, 130)),
        (520, (238, 164, 118)),
        (HOR, (246, 204, 130)),
    ]
    for i in range(len(sky_stops) - 1):
        y0, c0 = sky_stops[i]
        y1, c1 = sky_stops[i + 1]
        vgrad(d, X0, y0, X1, y1, c0, c1)

    # ---- stars (upper sky) ----
    stars = [(90, 90), (170, 60), (260, 110), (760, 70), (850, 120), (930, 80),
             (330, 70), (640, 100), (920, 200), (60, 200), (430, 55), (560, 80)]
    for sx, sy in stars:
        r = 2 if (sx + sy) % 3 else 3
        d.ellipse([sx - r, sy - r, sx + r, sy + r], fill=(250, 240, 200))

    # ---- sun: pale gold disc + glow, low right ----
    sx, sy, sr = 720, 470, 66
    for rr, alpha in [(110, 40), (92, 60), (78, 90)]:
        d.ellipse([sx - rr, sy - rr, sx + rr, sy + rr], fill=(244, 214, 140, alpha))
    d.ellipse([sx - sr, sy - sr, sx + sr, sy + sr], fill=(252, 226, 150))
    d.ellipse([sx - sr + 10, sy - sr + 10, sx + sr - 10, sy + sr - 10], fill=(253, 234, 176))

    # ---- sea ----
    vgrad(d, X0, HOR, X1, 948, SEA_LT, SEA_DK)
    # wave dashes
    for row, yy in enumerate(range(HOR + 26, 940, 34)):
        step = 46 + (row % 3) * 12
        off = (row * 29) % step
        for xx in range(X0 + 20 + off, X1 - 20, step):
            ln = 22 + (xx % 17)
            d.line([(xx, yy), (xx + ln, yy)], fill=(255, 255, 255, 110), width=3)
    # golden reflection column under the waterfall
    for yy in range(HOR + 14, 940, 22):
        wdt = 10 + (yy % 26)
        d.line([(512 - wdt // 2, yy), (512 + wdt // 2, yy)], fill=(244, 206, 120, 150), width=4)

    # ---- upward waterfall: sea -> floating isle ----
    # tapered column, wider at the sea, narrowing to the isle; foam + sparkles
    fall_top, fall_bot = 428, HOR
    for i, yy in enumerate(range(fall_bot, fall_top, -14)):
        t = (fall_bot - yy) / (fall_bot - fall_top)  # 0 bottom -> 1 top
        half = int(46 - 26 * t)
        sway = int(8 * math.sin(yy / 46.0))
        cx = 512 + sway
        col = lerp((214, 236, 240), (150, 205, 220), t)
        d.rounded_rectangle([cx - half, yy - 7, cx + half, yy + 7], radius=7, fill=col)
    # foam ring where it leaves the sea
    for k in range(9):
        fx = 512 + (k - 4) * 16
        fr = 7 + (k % 3) * 2
        d.ellipse([fx - fr, HOR - 6 - fr, fx + fr, HOR - 6 + fr],
                  fill=(240, 248, 250))
    # sparkles rising along the fall
    for k, (px, py) in enumerate([(470, 600), (552, 560), (488, 520), (540, 480), (500, 450)]):
        r = 4 + (k % 2) * 2
        d.line([(px - r, py), (px + r, py)], fill=(255, 255, 255), width=2)
        d.line([(px, py - r), (px, py + r)], fill=(255, 255, 255), width=2)

    # ---- floating isle (rock) ----
    isle = [(330, 400), (370, 388), (430, 392), (470, 384), (540, 388),
            (600, 380), (660, 392), (690, 408), (640, 470), (560, 500),
            (512, 512), (460, 496), (390, 470), (350, 430)]
    d.polygon(isle, fill=ROCK)
    d.polygon([(370, 388), (430, 392), (470, 384), (540, 388), (600, 380),
               (660, 392), (690, 408), (640, 430), (380, 428)], fill=ROCK_LT)
    # rock shading strokes
    for (ax, ay, bx, by) in [(400, 430, 470, 490), (560, 430, 520, 495), (620, 420, 580, 470)]:
        d.line([(ax, ay), (bx, by)], fill=(40, 36, 54), width=4)
    # temple on the isle: white pediment + columns + dome
    d.rectangle([452, 352, 572, 388], fill=WHITE)  # platform
    for cx in (472, 512, 552):
        d.rectangle([cx - 6, 322, cx + 6, 352], fill=WHITE)
    d.polygon([(452, 322), (572, 322), (512, 296)], fill=WHITE)  # pediment
    d.ellipse([496, 272, 528, 300], fill=GOLD_LT)  # dome
    d.rectangle([510, 264, 514, 274], fill=GOLD_LT)
    # temple windows (gold)
    for cx in (492, 532):
        d.rectangle([cx - 4, 330, cx + 4, 346], fill=GOLD)
    # cypress trees on the isle
    for tx in (400, 624):
        d.polygon([(tx, 330), (tx - 12, 388), (tx + 12, 388)], fill=(28, 62, 44))
        d.ellipse([tx - 7, 322, tx + 7, 340], fill=(28, 62, 44))

    # ---- sailboats ----
    def sailboat(bx, by, s):
        d.polygon([(bx, by - 34 * s), (bx, by), (bx + 22 * s, by)], fill=WHITE)
        d.polygon([(bx - 4 * s, by - 24 * s), (bx - 4 * s, by), (bx - 18 * s, by)], fill=(240, 230, 210))
        d.polygon([(bx - 26 * s, by), (bx + 26 * s, by), (bx + 16 * s, by + 10 * s),
                   (bx - 16 * s, by + 10 * s)], fill=(44, 38, 52))
        d.line([(bx, by - 34 * s), (bx, by - 40 * s)], fill=(44, 38, 52), width=2)
    sailboat(210, 800, 1.0)
    sailboat(830, 760, 0.8)

    # ---- terrace (bottom) ----
    d.rectangle([X0, 948, X1, Y1], fill=(232, 222, 198))
    d.rectangle([X0, 948, X1, 956], fill=(200, 186, 158))
    for bx in range(X0 + 26, X1 - 10, 34):
        d.rectangle([bx, 956, bx + 12, 996], fill=(214, 202, 176))
        d.rectangle([bx, 956, bx + 12, 962], fill=(190, 176, 148))
    d.rectangle([X0, 996, X1, Y1], fill=(222, 210, 184))
    # couple (back view silhouettes) at the balustrade, left of centre
    # woman with straw hat (left)
    d.ellipse([392, 886, 420, 914], fill=(52, 44, 58))  # hair
    d.ellipse([378, 900, 434, 912], fill=(214, 180, 112))  # hat brim
    d.ellipse([392, 884, 420, 902], fill=(228, 196, 128))  # hat crown
    d.polygon([(388, 914), (424, 914), (434, 996), (378, 996)], fill=(196, 84, 96))  # dress
    # man (right)
    d.ellipse([452, 888, 480, 916], fill=(52, 44, 58))  # head
    d.polygon([(446, 916), (486, 916), (494, 996), (438, 996)], fill=(240, 236, 224))  # shirt
    # small table with two wine glasses, right
    d.ellipse([640, 930, 700, 940], fill=(190, 176, 148))
    d.rectangle([666, 940, 672, 982], fill=(120, 108, 88))
    d.rectangle([648, 982, 690, 988], fill=(120, 108, 88))
    for gx in (656, 682):
        d.polygon([(gx - 5, 912), (gx + 5, 912), (gx + 3, 928), (gx - 3, 928)], fill=(250, 246, 236))
        d.line([(gx, 928), (gx, 934)], fill=(120, 108, 88), width=2)

    # ---- bougainvillea clusters (bottom corners) ----
    def bougainvillea(cx, cy, spread):
        import random
        rnd = random.Random(7)
        for _ in range(46):
            ox = rnd.randint(-spread, spread)
            oy = rnd.randint(-spread // 2, spread // 2)
            r = rnd.randint(4, 9)
            col = PINK if rnd.random() < 0.6 else PINK_LT
            d.ellipse([cx + ox - r, cy + oy - r, cx + ox + r, cy + oy + r], fill=col)
        for _ in range(10):
            ox = rnd.randint(-spread, spread)
            oy = rnd.randint(-spread // 2, spread // 2)
            d.ellipse([cx + ox - 3, cy + oy - 3, cx + ox + 3, cy + oy + 3], fill=(46, 96, 52))
    bougainvillea(70, 980, 60)
    bougainvillea(950, 985, 55)
    bougainvillea(60, 880, 34)
    bougainvillea(960, 900, 30)

    # ---- title ----
    f_big = ImageFont.truetype(SERIF_B, 118)
    f_sub = ImageFont.truetype(SANS_B, 30)
    f_tag = ImageFont.truetype(SANS, 22)
    # soft shadow then cream face
    text_center(d, 514, 62, "SOLUNARA", f_big, (120, 84, 40), tracking=10)
    text_center(d, 512, 60, "SOLUNARA", f_big, CREAM, tracking=10)
    text_center(d, 512, 184, "WHERE THE SEA CLIMBS TO THE SKY", f_sub, GOLD_LT, tracking=4)

    img.save("entry.png", optimize=True)
    print("saved entry.png")


if __name__ == "__main__":
    main()
