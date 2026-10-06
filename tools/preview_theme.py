"""Approximate preview of a RIPPS2 theme's game list and info page, without a PS2.

    python3 tools/preview_theme.py "themes/thm_Adapt" preview.png

Draws main and info side by side in RIPPS2's 640x480 space the way the engine places things:
negative x / y count from the right / bottom, POS_MID is the centre, aligned=1 centres the element on
its x / y. Backgrounds and static images, Ripps2PanelGlass (frosted when blur=1, with its tint=,
tint_color= and frame= as build 79 draws them, else build 78's gradient), covers, disc icons, the Grid's
page of covers (one with no art, shown as build 79's glass tile with the name) with the selection's glow,
list rows and text lines in the theme's own fonts. Game art is stood in by generated pictures (a theme's
default= images where it names them). It is a layout check, not a
screenshot: the towers, tilt and fades only show on the console (or in PCSX2).
"""
import os
import sys
from PIL import Image, ImageDraw, ImageFilter, ImageFont

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from check_theme import parse  # noqa: E402

W, H = 640, 480


def num(v, full, default=0):
    if v is None:
        return default
    if v == "POS_MID":
        return full // 2
    if v in ("DIM_INF",):
        return full
    n = int(v)
    return full + n if n < 0 else n


def color(hexs, alpha=255):
    hexs = hexs.lstrip("#")
    return tuple(int(hexs[i:i + 2], 16) for i in (0, 2, 4)) + (alpha,)


def sample_art():
    """A colourful stand-in for a game's background art, so frosted glass has something to soften."""
    im = Image.new("RGBA", (W, H))
    d = ImageDraw.Draw(im)
    for y in range(H):
        d.line([(0, y), (W, y)], fill=(40 + y // 4, 70 + y // 6, 160 - y // 5, 255))
    for i, (cx, cy, r, c) in enumerate(((160, 140, 110, (255, 170, 60)), (470, 300, 150, (60, 220, 160)), (330, 90, 70, (240, 80, 120)))):
        d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=c + (255,))
    return im


def sample_cover(k, w, h):
    """A stand-in for a game's cover: a colour block with a band, different per game."""
    hues = ((200, 60, 60), (60, 120, 210), (230, 170, 40), (80, 170, 90), (150, 70, 190), (40, 170, 190), (220, 110, 50), (110, 110, 130))
    c = hues[k % len(hues)]
    im = Image.new("RGBA", (w, h), c + (255,))
    d = ImageDraw.Draw(im)
    d.rectangle([0, h * 2 // 3, w, h * 2 // 3 + h // 8], fill=(255, 255, 255, 200))
    d.rectangle([0, 0, w - 1, h - 1], outline=(0, 0, 0, 160))
    return im


class Page:
    def __init__(self, folder, glob):
        self.folder, self.glob = folder, glob
        self.im = Image.new("RGBA", (W, H), color(glob.get("bg_color", "#202040")))
        self.d = ImageDraw.Draw(self.im)
        self.backdrop = self.im.copy()

    def font(self, idx, size=None):
        name = self.glob.get("default_font") if idx in (None, "0") else self.glob.get("font%s" % idx)
        size = size or int(self.glob.get("font%s_size" % idx, self.glob.get("default_font_size", 17)))
        try:
            return ImageFont.truetype(os.path.join(self.folder, name), size)
        except Exception:
            return ImageFont.load_default()

    def image(self, name):
        for ext in (".png", ".jpg"):
            p = os.path.join(self.folder, name + ext)
            if os.path.isfile(p):
                return Image.open(p).convert("RGBA")
        return None

    def rect(self, e, w, h):
        x, y = num(e.get("x"), W), num(e.get("y"), H)
        if e.get("aligned", "1") == "1":
            x, y = x - w // 2, y - h // 2
        return x, y

    def paste(self, img, x, y, w, h, dim=1.0):
        img = img.resize((max(1, w), max(1, h)))
        if dim < 1.0:
            img = Image.eval(img, lambda c: int(c * dim))
        self.im.alpha_composite(img, (int(x), int(y)))

    def draw(self, e):
        t = e.get("type")
        if e.get("enabled") == "0" or e.get("hidden") == "1":
            return
        txt = color(self.glob.get("text_color", "#FFFFFF"))
        if t in ("Background", "StaticImage"):
            img = self.image(e.get("default", "")) if e.get("default") else None
            if t == "Background" and e.get("pattern"):
                img = sample_art()  # stands in for a game's own background art
            if img:
                w, h = num(e.get("width"), W, img.width), num(e.get("height"), H, img.height)
                self.paste(img, 0, 0, W if e.get("width") == "DIM_INF" or t == "Background" else w,
                           H if e.get("height") == "DIM_INF" or t == "Background" else h)
            self.backdrop = self.im.copy()
        elif t == "Ripps2PanelGlass":
            w, h = num(e.get("width"), W, 320), num(e.get("height"), H, 240)
            x, y = self.rect(e, w, h)
            if e.get("blur") == "1":
                frost = self.backdrop.resize((80, 60), Image.BOX).filter(ImageFilter.BoxBlur(1)).resize((W, H), Image.BILINEAR)
                self.im.alpha_composite(frost.crop((x, y, x + w, y + h)), (x, y))
            tint = Image.new("RGBA", (w, h))
            td = ImageDraw.Draw(tint)
            if "tint" in e:  # build 79: one constant tint (0-128, the PS2's alpha scale)
                td.rectangle([0, 0, w, h], fill=color(e.get("tint_color", "#040C2E"), min(255, int(e["tint"]) * 2)))
            else:
                for yy in range(h):  # RIPPS2's glass: light at the top, deep from about a third down
                    a = 0x3C if yy < h * 0.22 else int(0x3C + (0xB8 - 0x3C) * min(1, (yy - h * 0.22) / (h * 0.16)))
                    td.line([(0, yy), (w, yy)], fill=(4, 12, 46, a))
            self.im.alpha_composite(tint, (x, y))
            if e.get("frame", "1") != "0":
                self.d.rectangle([x, y, x + w - 1, y + h - 1], outline=(126, 194, 255, 150))
        elif t in ("ItemCover", "ItemIcon"):
            w, h = num(e.get("width"), W, 140), num(e.get("height"), H, 200)
            img = self.image(e["default"]) if e.get("default") else (sample_cover(0, w, h) if t == "ItemCover" else None)
            if img:
                x, y = self.rect(e, w, h)
                if t == "ItemCover" and e.get("reflection") == "1":  # the mirror under the case
                    ref = img.transpose(Image.FLIP_TOP_BOTTOM).crop((0, 0, img.width, img.height // 3))
                    self.paste(Image.eval(ref, lambda c: c // 3), x, y + h + 2, w, h // 3)
                self.paste(img, x, y, w, h)
                if e.get("overlay"):
                    for key in ("overlay", "overlay2"):
                        ov = self.image(e[key]) if e.get(key) else None
                        if ov:
                            self.paste(ov, x, y, w, h)
        elif t == "Grid":
            cols, rows, gap = int(e.get("columns", 4)), int(e.get("rows", 2)), int(e.get("spacing", 14))
            w, h = num(e.get("width"), W, 104), num(e.get("height"), H, 146)
            cx, top = num(e.get("x"), W, W // 2), num(e.get("y"), H, 60)
            img = self.image(e["default"]) if e.get("default") else None
            left = cx - (cols * (w + gap) - gap) // 2
            sel = color(self.glob.get("sel_text_color", "#0064FF"))
            f = self.font(e.get("font"))
            for k in range(cols * rows):
                x, y = left + (k % cols) * (w + gap), top + (k // cols) * (h + gap)
                cw, ch, dim = w, h, 0.85
                if k == 0:  # the selection: 112%, a soft glow and a frame
                    cw, ch, dim = w * 112 // 100, h * 112 // 100, 1.0
                    x, y = x + w // 2 - cw // 2, y + h // 2 - ch // 2
                    glow = Image.new("RGBA", (cw + 40, ch + 40))
                    ImageDraw.Draw(glow).rectangle([14, 14, cw + 25, ch + 25], outline=sel[:3] + (150,), width=6)
                    self.im.alpha_composite(glow.filter(ImageFilter.GaussianBlur(5)), (x - 20, y - 20))
                    self.d.rectangle([x - 2, y - 2, x + cw + 1, y + ch + 1], outline=sel[:3] + (200,), width=2)
                if k == 5 and not img:  # a game with no art: a glass tile with its name
                    tile = Image.new("RGBA", (cw, ch), (4, 12, 46, 64))
                    self.im.alpha_composite(tile, (x, y))
                    self.d.rectangle([x, y, x + cw - 1, y + ch - 1], outline=(126, 194, 255, 150))
                    for n, word in enumerate(("Game", "without art")):
                        tw = self.d.textlength(word, font=f)
                        self.d.text((x + (cw - tw) / 2, y + ch / 2 - 22 + n * 22), word, font=f, fill=txt)
                else:
                    self.paste(img or sample_cover(k, cw, ch), x, y, cw, ch, dim=dim)
        elif t == "ItemsList":
            w, h = num(e.get("width"), W, 373), num(e.get("height"), H, 316)
            x, y = num(e.get("x"), W), num(e.get("y"), H)
            f = self.font(e.get("font"))
            for r in range(max(1, h // 22)):
                fill = color(self.glob.get("sel_text_color", "#0064FF")) if r == 2 else txt
                self.d.text((x + 6, y + r * 22), "Game title %d" % (r + 1), font=f, fill=fill)
        elif t in ("HintText", "InfoHintText"):  # the theme's own button glyphs, as the console draws them
            pairs = [("triangle", "Menu"), ("cross", "Run"), ("square", "Info")] + ([("circle", "Source")] if self.grid else []) if t == "HintText" else [("cross", "Run"), ("circle", "Back")]
            f = self.font(e.get("font"))
            x, y = num(e.get("x"), W), num(e.get("y"), H)
            total = sum(22 + self.d.textlength(w, font=f) + 14 for _, w in pairs) - 14
            if e.get("aligned", "1") == "1":
                x -= total / 2
            for glyph, word in pairs:
                g = self.image(glyph)
                if g:
                    self.paste(g, x, y - 2, 20, 20)
                self.d.text((x + 22, y), word, font=f, fill=color(self.glob.get("ui_text_color", "#C4DAFF")))
                x += 22 + self.d.textlength(word, font=f) + 14
        elif t in ("ItemText", "MenuText", "AttributeText"):
            label = {"ItemText": "Selected game", "MenuText": "ALL GAMES", "HintText": "cross run   triangle options",
                     "InfoHintText": "cross run   circle back"}.get(t, e.get("attribute", "text") + ": sample")
            f = self.font(e.get("font"))
            x, y = num(e.get("x"), W), num(e.get("y"), H)
            if e.get("aligned", "1") == "1":
                tw = self.d.textlength(label, font=f)
                x -= tw / 2
            self.d.text((x, y), label, font=f, fill=color(self.glob.get("ui_text_color", "#C4DAFF")) if t.endswith("HintText") else txt)
        elif t == "GameImage" or t == "AttributeImage":
            w, h = num(e.get("width"), W, 40 if t == "AttributeImage" else 170), num(e.get("height"), H, 30 if t == "AttributeImage" else 110)
            x, y = self.rect(e, w, h) if e.get("aligned", "1") == "1" else (num(e.get("x"), W), num(e.get("y"), H))
            self.d.rectangle([x, y, x + w, y + h], outline=(255, 255, 255, 90))
            self.d.text((x + 4, y + 2), e.get("pattern", e.get("attribute", "")), font=self.font(None, 11), fill=(255, 255, 255, 140))


def render(folder, out):
    glob, elems = parse(os.path.join(folder, "conf_theme.cfg"))
    sheet = Image.new("RGBA", (W * 2 + 16, H), (0, 0, 0, 255))
    for col, fam in enumerate(("main", "info")):
        page = Page(folder, glob)
        page.grid = any(e.get("type") in ("Grid", "Coverflow") for (f, _), e in elems.items() if f == "main")
        i = 0
        while (fam, i) in elems:
            page.draw(elems[(fam, i)])
            i += 1
        sheet.alpha_composite(page.im, (col * (W + 16), 0))
    sheet.convert("RGB").save(out)
    print(out)


if __name__ == "__main__":
    render(sys.argv[1], sys.argv[2] if len(sys.argv) > 2 else "preview.png")
