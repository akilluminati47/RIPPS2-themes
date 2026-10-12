"""Write conf_theme.cfg for the Adapt themes (Adapt, Adapt Rx) from one layout, so the shared pieces -- the
frosted screen, the side bar, the info page -- stay in step. RIPGRID is built into RIPPS2 (since build 91, as
<RIPGRID>), so it is no longer written here.

Each conf_theme.cfg opens with its creation header, then the key glossary (docs/key_glossary.cfg: every key a
RIPPS2 theme can use), then the theme itself. Change EDITION_DATE and EDITION_BUILD when the themes change.

    python3 tools/gen_adapt_family.py

Layers, back to front, on the game list and the info page alike:
  Background (each game's art, widecrop in 16:9) -> a full-screen frosted layer (blur, low tint, no
  frame) -> the side bar (a dark frosted strip and a light rule, frameless) -> the framed glass panel
  under the text -> the art and text.

The whole info page (panel, logo, badges, text, screenshots) tips with the right stick as one plane about
the page's centre; the hint row and the backdrop hold still. Adapt's cover is RIPPS2's case (case +
case_overlay, its reflection below), tipping with the disc; on the game list the case shows the front
cover, then the back (COV2), crossfading as the info page's slideshow does (slide=1, 2). The info page
sits on the other side from the game list's text: Adapt's text right, Adapt Rx's left.
"""
import os

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "themes")

EDITION_DATE = "10/12/2026"  # the date the RIPPS2 edition last changed: the theme pack's release date
EDITION_BUILD = 100          # the RIPPS2 build it was made and checked on
GLOSSARY = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "docs", "key_glossary.cfg")

RULE = "# " + "=" * 102
HEAD = RULE + """
# Theme Name: {name}
# Made by: akilluminati47
# Created: 8/27/2026 (Adapt, for RiptOPL)
# Updated: {date} (the RIPPS2 edition, made on RIPPS2 build {build}; needs RIPPS2 build 80 or later)
# Credits: [case.png] [case_overlay.png] RiptOPL's built-in case (b2); [SCR43.png] Adapt's screenshot frame
#   cut to 4:3; the fonts (a.ttf, b.ttf, c.ttf, d.ttf) and the other images as shipped in Adapt RiptOPL.
# Look: each game's art under frosted glass (a full-screen Ripps2PanelGlass, blur=1), a frosted side bar on
#   the left, clear glass panels under the text, page morphs between the list and the info page, the pillars
#   behind Settings (no settings_bg), right-stick tilt on the art. Art eases in; no stock disc or case.
#   {side}
# Written by tools/gen_adapt_family.py (github.com/akilluminati47/RIPPS2-themes): change the layout there.
""" + RULE + """
#
{glossary}
#
# ---- THIS THEME: the global keys, then the elements ---------------------------------------------------
bg_color=#050A1C
sel_text_color=#0064FF
text_color=#FFFFFF
ui_text_color=#C4DAFF
towers=0
bg_blur=weak
source_name=pop
{fonts}"""

SIDES = {
    0: "Adapt: the case and disc left, under LAUNCH DISC, the list right; the info page's text right.",
    1: "Adapt Rx: the list left, the case and disc right, under LAUNCH DISC; the info page's text left.",
}

# Adapt's own type (its TTFs ship in the theme)
ADAPT_FONTS = """default_font=a.ttf
default_font_size=17
font1=b.ttf
font2=c.ttf
font3=d.ttf
font4=b.ttf
font4_size=20
"""
FROST_TINT, PANEL_TINT, BAR_TINT, RULE_TINT = 24, 44, 88, 22
INFO_TILT = dict(tilt=1, tilt_x=320, tilt_y=260, tilt_scale=75)  # the info page: one plane


def case(**kv):
    """RIPPS2's case around the cover, true scale, with its reflection (the built-in theme's own keys)."""
    return dict(kv, width=143, height=201, aligned=1, scaled=1, reflection=1, overlay="case", overlay2="case_overlay",
                overlay_ulx=0, overlay_uly=0, overlay_urx=143, overlay_ury=0,
                overlay_llx=0, overlay_lly=201, overlay_lrx=143, overlay_lry=201)


def block(name, **kv):
    out = [name + ":"]
    for k, v in kv.items():
        out.append("\t%s=%s" % (k, v))
    return "\n".join(out)


def backdrop(fam):
    """Background, the frosted screen, the side bar's strip and rule: indices 0-3 of main and info. The
    side bar is on the left in every theme of the family, Adapt Rx included (it mirrors the content)."""
    bar_x, rule_x = 0, 28  # the strip 0-26, the rule 28-40: content starts at x 40
    return [
        block(fam + "0", type="Background", pattern="BG", widecrop=1),
        block(fam + "1", type="Ripps2PanelGlass", aligned=0, x=0, y=0, width=640, height=480,
              blur=1, tint=FROST_TINT, frame=0),
        block(fam + "2", type="Ripps2PanelGlass", aligned=0, x=bar_x, y=0, width=26, height=480,
              blur=1, tint=BAR_TINT, tint_color="#01040F", frame=0),
        block(fam + "3", type="Ripps2PanelGlass", aligned=0, x=rule_x, y=0, width=12, height=480,
              blur=1, tint=RULE_TINT, tint_color="#28C5F9", frame=0),
    ]


def screenshot(name, pattern, x, y):
    # 4:3: a 160 x 120 window in a 170 x 128 frame; scaled=1 keeps it 4:3 on a 16:9 picture, as the case is
    return block(name, type="GameImage", pattern=pattern, scaled=1, x=x, y=y, width=170, height=128, overlay="SCR43",
                 overlay_ulx=6, overlay_uly=4, overlay_urx=166, overlay_ury=4,
                 overlay_llx=6, overlay_lly=124, overlay_lrx=166, overlay_lry=124, **INFO_TILT)


def info(rx):
    # the text panel and the screenshots side by side, clear of the side bar. Rx swaps them, the side bar
    # staying left: screenshots 56-226 (16 px from the bar), glass 242-622 (16 px gap, 18 px to the edge)
    gw = 380 if rx else 395   # glass width
    gx = 242 if rx else 45    # glass left
    tw = gw - 20              # text width
    tx = gx + 10              # text left
    ax = gx + 15              # first attribute icon
    sx = 141 if rx else 532   # screenshots' centre
    els = backdrop("info") + [
        block("info4", type="Ripps2PanelGlass", aligned=0, x=gx, y=160, width=gw, height=255,
              blur=1, tint=PANEL_TINT, frame=1, **INFO_TILT),
        block("info5", type="GameImage", pattern="LGO", x="POS_MID", y=100, aligned=1, width=300,
              height=125, **INFO_TILT),
        block("info6", type="AttributeImage", attribute="Rating", default="rating/0_Rating", aligned=0, x=ax, y=177, **INFO_TILT),
        block("info7", type="AttributeImage", attribute="Scan", aligned=0, x=ax + 172, y=173, **INFO_TILT),
        block("info8", type="AttributeImage", attribute="Players", aligned=0, x=ax + 122, y=173, **INFO_TILT),
        # line_height: a description longer than its box rolls through it instead of running on
        block("info9", type="AttributeText", attribute="Description", aligned=0, display=2, x=tx, y=210,
              width=tw, height=100, wrap=1, line_height=19, font=1, **INFO_TILT),
        block("info10", type="AttributeText", attribute="Developer", aligned=0, display=2, x=tx, y=330,
              width=tw, wrap=0, font=2, **INFO_TILT),
        block("info11", type="AttributeText", attribute="Release", aligned=0, display=2, x=tx, y=358,
              width=tw, font=3, **INFO_TILT),
        block("info12", type="AttributeText", attribute="Genre", display=2, aligned=0, x=tx, y=385,
              width=tw, font=2, **INFO_TILT),
        block("info13", type="InfoHintText", aligned=1, x="POS_MID", y=-41, font=3),
        # a hairline under the logo (its box ends at y 162), the lower frame still clear of the hints
        screenshot("info14", "SCR", sx, 230),
        screenshot("info15", "SCR2", sx, 362),
        # the badge (54 px) 16 px inside the panel's right edge, whichever width the panel is
        block("info16", type="AttributeImage", attribute="Parental", aligned=0, scaled=1, x=gx + gw - 70, y=330, **INFO_TILT),
        block("info17", type="AttributeImage", attribute="Vmode", aligned=0, x=ax + 272, y=173, **INFO_TILT),
        block("info18", type="AttributeImage", attribute="Aspect", aligned=0, x=ax + 222, y=173, **INFO_TILT),
    ]
    # apps: the app's cover where the logo was, no screenshots
    apps = [
        block("appsInfo5", type="ItemCover", **case(x=sx, y=262, **INFO_TILT)),
        block("appsInfo14", type="GameImage", enabled=0),
        block("appsInfo15", type="GameImage", enabled=0),
    ]
    return els, apps


def common_tail(fam, start):
    return [
        block("%s%d" % (fam, start), type="LoadingIcon", x=-60, y=-31),
        block("%s%d" % (fam, start + 1), type="HintText", aligned=1, x="POS_MID", y=-41, font=2),
        block("%s%d" % (fam, start + 2), type="MenuText", x="POS_MID", y=25, aligned=1, width=225, font=2),
    ]


# RIPPS2's category bar: LAUNCH DISC, STORAGE, MEMORY FILES at these x (ripps2ui.c categoryX), labels at y 30
BAR_X = (128, 320, 512)


def adapt(rx):
    # The disc and its case sit right under LAUNCH DISC: Adapt's at the bar's left end (x 128); Rx puts
    # LAUNCH DISC at the right end (category_order=memory_files_first, build 81) and its disc under it
    # (x 512). The list glass takes the rest, 16 px from the bar's rule (x 40), from the case and from the
    # edge: Adapt 216-624, Rx 56-424.
    cx = BAR_X[2] if rx else BAR_X[0]  # cover and disc centre, under LAUNCH DISC
    gx = 56 if rx else 216    # list glass left
    gw = 368 if rx else 408   # list glass width
    lw = gw - 24              # the list inside the glass
    main = backdrop("main") + [
        block("main4", type="Ripps2PanelGlass", aligned=0, x=gx, y=76, width=gw, height=309,
              blur=1, tint=PANEL_TINT, frame=1),
        # the case: the front cover, then the back, crossfading (the slideshow; a game with no back
        # cover keeps its front). The front is the list's cover (COV), so it still loads first.
        block("main5", type="GameImage", pattern="COV", slide=1, **case(x=cx, y=262, tilt=1, tilt_x=cx, tilt_y=200)),
        block("main6", type="GameImage", pattern="COV2", slide=2, **case(x=cx, y=262, tilt=1, tilt_x=cx, tilt_y=200)),
        # the disc: clear of the LAUNCH DISC label above (y 30) and of the case below (its top at 161)
        block("main7", type="ItemIcon", aligned=1, scaled=1, x=cx, y=100, width=112, height=112,
              tilt=1, tilt_x=cx, tilt_y=200),
        block("main8", type="ItemsList", x=gx + 12, y=88, aligned=0, width=lw, height=285, font=4),
    ] + common_tail("main", 9)
    # apps: one wide glass list clear of the side bar (left in both), no cover or disc
    ax = 48
    apps = [
        block("appsMain4", type="Ripps2PanelGlass", aligned=0, x=ax, y=40, width=568, height=368,
              blur=1, tint=PANEL_TINT, frame=1),
        block("appsMain5", type="GameImage", enabled=0),
        block("appsMain6", type="GameImage", enabled=0),
        block("appsMain7", type="ItemIcon", enabled=0),
        block("appsMain8", type="ItemsList", x=ax + 10, y=75, aligned=0, width=548, height=323, font=4),
    ]
    return main, apps


def write(folder, name, rx, main, mainApps, infoEls, infoApps, extra=""):
    glossary = open(GLOSSARY, encoding="utf-8").read().rstrip("\n")
    for n, line in enumerate(glossary.split("\n"), 1):
        if line and not line.startswith("#"):
            raise SystemExit("docs/key_glossary.cfg line %d is not a comment: %r" % (n, line[:60]))
    text = HEAD.format(name=name, date=EDITION_DATE, build=EDITION_BUILD, side=SIDES[rx], glossary=glossary,
                       fonts=ADAPT_FONTS) + extra + "\n" + "\n".join(main + infoEls + mainApps + infoApps) + "\n"
    with open(os.path.join(ROOT, folder, "conf_theme.cfg"), "w", newline="\n") as f:
        f.write(text)
    print("wrote", folder)


if __name__ == "__main__":
    for folder, name, rx in (("thm_Adapt", "Adapt", 0), ("thm_Adapt Rx", "Adapt Rx", 1)):
        m, ma = adapt(rx)
        # the info page puts its text on the other side from the game list's: Adapt (list right) gets
        # text right and pictures left, Adapt Rx (list left) the reverse
        i, ia = info(1 - rx)
        # Rx: LAUNCH DISC at the bar's right end, over its disc (a default: the user's own order wins)
        extra = "category_order=memory_files_first\n" if rx else ""
        write(folder, name, rx, m, ma, i, ia, extra)
