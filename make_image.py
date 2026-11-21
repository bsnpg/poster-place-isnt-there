"""SARANJANA — The Poster for a Place That Isn't There.
Realistic painterly travel poster (NOT flat cartoon): the scene is a
painterly illustration (scene.png, generated once and shipped in the repo);
this script composites the title + tagline + frame with PIL and writes
entry.png. 1024x1024, deterministic (no randomness, no network)."""
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import os

import os as _os
SRC = _os.path.join(_os.path.dirname(_os.path.abspath(__file__)), "scene.png")
OUT = _os.path.join(_os.path.dirname(_os.path.abspath(__file__)), "entry.png")
W = H = 1024

img = Image.open(SRC).convert("RGB")
# center-crop to square then resize to 1024x1024
w, h = img.size
side = min(w, h)
img = img.crop(((w - side) // 2, (h - side) // 2, (w + side) // 2, (h + side) // 2))
img = img.resize((W, H), Image.LANCZOS)

draw = ImageDraw.Draw(img, "RGBA")

# --- top dark gradient band for title readability (subtle) ---
band_h = 190
overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
od = ImageDraw.Draw(overlay)
for y in range(band_h):
    alpha = int(150 * (1 - y / band_h) ** 1.5)
    od.line([(0, y), (W, y)], fill=(10, 8, 30, alpha))
overlay = overlay.filter(ImageFilter.GaussianBlur(2))
img = Image.alpha_composite(img.convert("RGBA"), overlay).convert("RGB")
draw = ImageDraw.Draw(img, "RGBA")

def font(sz, bold=True):
    for p in ("/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf" if bold else "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf",
              "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
              "/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf"):
        if os.path.exists(p):
            return ImageFont.truetype(p, sz)
    return ImageFont.load_default()

def text_center(y, s, fnt, fill, outline=(20, 14, 8), ow=3):
    x = W // 2
    # outline
    for dx in range(-ow, ow + 1):
        for dy in range(-ow, ow + 1):
            if dx or dy:
                draw.text((x + dx, y + dy), s, font=fnt, fill=outline, anchor="ma")
    draw.text((x, y), s, font=fnt, fill=fill, anchor="ma")

# Title SARANJANA — big cream serif with dark outline
f_title = font(106, True)
text_center(18, "SARANJANA", f_title, (255, 244, 214))

# Tagline — gold, letterspaced (smaller so it fits inside the frame)
f_tag = font(26, True)
tag = "W H E R E   T H E   U N S E E N   C I T Y   S H I N E S"
text_center(150, tag, f_tag, (255, 200, 90))

# Thin vintage gold frame
draw.rectangle([14, 14, W - 15, H - 15], outline=(212, 175, 105), width=5)
draw.rectangle([26, 26, W - 27, H - 27], outline=(212, 175, 105, 180), width=2)

# Save as palette PNG (256 colors, adaptive + dithering) to stay under 1 MiB
pal = img.convert("P", palette=Image.ADAPTIVE, colors=256, dither=Image.FLOYDSTEINBERG)
pal.save(OUT, "PNG", optimize=True)
print("saved", OUT, os.path.getsize(OUT), "bytes")


if __name__ == "__main__":
    pass
