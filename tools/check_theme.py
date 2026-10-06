"""Check a RIPPS2 theme folder before it goes near a PS2.

    python3 tools/check_theme.py "themes/thm_Adapt"

Checks conf_theme.cfg the way RIPPS2's theme engine reads it (src/themes.c, RIPPS2 build 81):
- main and info are numbered 0, 1, 2... with no gap (the engine stops reading at the first missing
  number); every other family (appsMain, vcdInfo...) replaces its base family's element of the same
  number, so a number past the base family's last is never read;
- every element type is one the engine knows;
- every image the theme names (default=, overlay=, bg/attribute folders) and every font exists;
- RIPPS2 keys are where they work (blur/tint/tint_color/frame on Ripps2PanelGlass, columns/rows/spacing/back_pattern
  on Grid, widecrop on Background) and in range (tint 0-128, tint_color #RRGGBB);
- a Grid or Coverflow page also declares an ItemsList (hidden=1), else the engine adds a visible one;
- source_name, color_theme, category_bar, button_hints, dpad_glyphs and category_order hold values RIPPS2 knows;
- every PNG is an 8-bit palette PNG (a warning: RGBA ones cost four times the VRAM; tools/png8.py).
Exit code 1 on an error; warnings do not fail.
"""
import os
import re
import struct
import sys

# fonts compiled into RIPPS2 (src/fntsys.c): a theme names them as builtin:<name> and ships nothing
BUILTIN_FONTS = {"builtin:ripps2", "builtin:ripps2sleek", "builtin:ripps2sleekbold", "builtin:ripps2sleekcase",
                 "builtin:ripflow", "builtin:ripflowbold"}

TYPES = {"AttributeText", "StaticText", "AttributeImage", "GameImage", "StaticImage", "Background", "MenuIcon",
         "MenuText", "ItemsList", "ItemIcon", "ItemCover", "ItemText", "HintText", "InfoHintText", "LoadingIcon",
         "BdmIndex", "GameCountText", "Coverflow", "Ripps2PanelGlass", "Grid"}
FAMILIES = ["main", "info", "appsMain", "appsInfo", "favsMain", "favsInfo", "vcdMain", "vcdInfo", "favsVcdMain",
            "favsVcdInfo", "favsAppsMain", "favsAppsInfo"]
# main and info are read 0, 1, 2... until a number is missing; every other family replaces the element of
# the same number in its base family, and only numbers the base family has are read
BASE = {f: ("info" if f.endswith("Info") else "main") for f in FAMILIES if f not in ("main", "info")}
GRID_KEYS = {"columns", "rows", "spacing", "back_pattern"}
GLASS_KEYS = {"blur", "tint", "tint_color", "frame"}  # build 78-79


def parse(path):
    glob, elems, cur = {}, {}, None
    for n, raw in enumerate(open(path, encoding="utf-8", errors="replace"), 1):
        line = raw.rstrip("\r\n")
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        m = re.match(r"^([A-Za-z]+)(\d+):\s*$", line.strip())
        if m and not line.startswith(("\t", " ")):
            cur = (m.group(1), int(m.group(2)))
            elems.setdefault(cur, {"_line": n})
            continue
        if "=" in line:
            k, v = line.strip().split("=", 1)
            if line.startswith(("\t", " ")) and cur:
                elems[cur][k.strip()] = v.strip()
            else:
                glob[k.strip()] = v.strip()
                cur = None
    return glob, elems


def main(folder):
    cfg = os.path.join(folder, "conf_theme.cfg")
    errors, warnings = [], []
    if not os.path.isfile(cfg):
        print("ERROR no conf_theme.cfg in %s" % folder)
        return 1
    glob, elems = parse(cfg)

    def img(name):
        return any(os.path.isfile(os.path.join(folder, name + ext)) for ext in (".png", ".jpg", ""))

    for k, v in glob.items():
        if (k == "default_font" or re.match(r"font\d+$", k)) and v.startswith("builtin:"):
            if v not in BUILTIN_FONTS:
                errors.append("font %s=%s: RIPPS2 has no such built-in font (%s)" % (k, v, ", ".join(sorted(BUILTIN_FONTS))))
            continue
        if (k == "default_font" or re.match(r"font\d+$", k)) and not os.path.isfile(os.path.join(folder, v)):
            errors.append("font %s=%s is missing" % (k, v))
    # Colors and More from the theme (build 81; source_name=pop since 80): each must be a value RIPPS2 knows
    CHOICES = {"source_name": ("pop", "shown", "fade", "hidden"), "category_bar": ("shown", "fade", "hidden"),
               "button_hints": ("shown", "fade", "hidden"), "dpad_glyphs": ("hidden", "shown", "fade_in", "fade_out"),
               "category_order": ("launch_disc_first", "memory_files_first"),
               "color_theme": ("ripps2", "ember", "blood", "ectoplasm", "amethyst", "bone")}
    for key, values in CHOICES.items():
        if key in glob and glob[key].lower() not in values:
            errors.append("%s=%s: one of %s" % (key, glob[key], ", ".join(values)))
    if glob.get("use_settings_bg") == "1" and not img("settings_bg"):
        errors.append("use_settings_bg=1 but settings_bg.png is missing")

    for fam in FAMILIES:
        nums = sorted(i for f, i in elems if f == fam)
        if fam in BASE:
            base = len([1 for f, i in elems if f == BASE[fam]])
            for i in nums:
                if i >= base:
                    warnings.append("%s%d is never read: %s has only %d elements (0-%d)" % (fam, i, BASE[fam], base, base - 1))
        elif nums and nums != list(range(len(nums))):
            gap = next(i for i, n in enumerate(nums) if n != i)
            errors.append("%s: numbering breaks at %s%d (the engine stops reading there)" % (fam, fam, gap))
        types = []
        for i in nums:
            e = elems[(fam, i)]
            t = e.get("type")
            where = "%s%d (line %d)" % (fam, i, e["_line"])
            if t is None:
                if e.get("enabled") != "0":
                    warnings.append("%s has no type (it inherits main's element of that number)" % where)
                continue
            types.append(t)
            if t not in TYPES:
                errors.append("%s: unknown type %s" % (where, t))
            for key in ("default", "overlay", "overlay2"):
                if key in e and not img(e[key]):
                    errors.append("%s: %s=%s is missing" % (where, key, e[key]))
            if GLASS_KEYS & set(e) and t != "Ripps2PanelGlass":
                warnings.append("%s: blur/tint/tint_color/frame work only on Ripps2PanelGlass" % where)
            if "widecrop" in e and t != "Background":
                warnings.append("%s: widecrop works only on Background" % where)
            if "tint" in e and not (e["tint"].isdigit() and 0 <= int(e["tint"]) <= 128):
                errors.append("%s: tint is 0-128 (got %s)" % (where, e["tint"]))
            if "tint_color" in e and not re.match(r"^#[0-9A-Fa-f]{6}$", e["tint_color"]):
                errors.append("%s: tint_color is #RRGGBB (got %s)" % (where, e["tint_color"]))
            if t == "Grid" and "default" in e:
                warnings.append("%s: a Grid default= puts that picture on every game without art (build 79 shows a glass tile with the name)" % where)
            if GRID_KEYS & set(e) and t != "Grid":
                warnings.append("%s: columns/rows/spacing/back_pattern work only on Grid" % where)
            if t == "Grid":
                c, r = int(e.get("columns", 4)), int(e.get("rows", 2))
                if not (1 <= c <= 8 and 1 <= r <= 4):
                    errors.append("%s: columns 1-8 and rows 1-4 (got %d x %d)" % (where, c, r))
                if "back_pattern" in e and not re.match(r"^(0|[A-Za-z0-9]+)$", e["back_pattern"]):
                    errors.append("%s: back_pattern is an art suffix such as COV2 or SCR, or 0 (got %s)" % (where, e["back_pattern"]))
        if fam in ("main", "appsMain") and ({"Grid", "Coverflow"} & set(types)) and "ItemsList" not in types:
            errors.append("%s: a Grid/Coverflow page needs an ItemsList (hidden=1), else a visible default list is added" % fam)

    for root, _, files in os.walk(folder):  # RIPPS2 keeps 8-bit palette PNGs as 8-bit textures
        for name in sorted(files):
            if name.lower().endswith(".png"):
                with open(os.path.join(root, name), "rb") as fh:
                    head = fh.read(26)
                if len(head) == 26 and (head[25], head[24]) != (3, 8):  # colour type 3 (palette), 8-bit
                    warnings.append("%s is not an 8-bit palette PNG (4x the VRAM; tools/png8.py converts it)"
                                    % os.path.relpath(os.path.join(root, name), folder))

    for w in warnings:
        print("WARN  " + w)
    for e in errors:
        print("ERROR " + e)
    print("%s: %d error(s), %d warning(s)" % (folder, len(errors), len(warnings)))
    return 1 if errors else 0


if __name__ == "__main__":
    folders = [f for f in sys.argv[1:] if os.path.isdir(f)]
    sys.exit(max(main(f) for f in folders) if folders else 2)
