"""Write conf_theme.cfg for the Adapt-family themes (Adapt, Adapt Rx, RIPgrid) from one
layout, so the shared pieces -- the frosted screen, the side bar, the info page -- stay in step.

    python3 tools/gen_adapt_family.py

Layers, back to front, on the game list and the info page alike:
  Background (each game's art, widecrop in 16:9) -> a full-screen frosted layer (blur, low tint, no
  frame) -> the side bar (a dark frosted strip and a light rule, frameless) -> the framed glass panel
  under the text -> the art and text.

The whole info page (panel, logo, badges, text, screenshots) tips with the right stick as one plane about
the page's centre; the hint row and the backdrop hold still. Adapt's cover is RIPPS2's case (case +
case_overlay, its reflection below), tipping with the disc; on the game list the case shows the front
cover, then the back (COV2), crossfading as the info page's slideshow does (slide=1, 2). The info page
sits on the other side from the game list's text: Adapt's text right, Adapt Rx's left. On RIPgrid only
the chosen cover tips (front only), and its type is RIPPS2 Sleek from the ELF (builtin: fonts).
"""
import os

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "themes")

HEAD = """# Theme Name: {name}
# Made by: akilluminati47 (Adapt RiptOPL, 8/27/2026), RIPPS2 edition (build 81)
# [case.png] [case_overlay.png] RiptOPL's built-in case (b2); [SCR43.png] Adapt's screenshot frame at 4:3
# RIPPS2: each game's art under frosted glass (a full-screen Ripps2PanelGlass, blur=1), a frosted side
# bar, clear glass panels under the text, page morphs between the list and the info page, the pillars
# behind Settings (no settings_bg), right-stick tilt on the art. Art eases in; no stock disc or case.

bg_color=#050A1C
sel_text_color=#0064FF
text_color=#FFFFFF
ui_text_color=#C4DAFF
towers=0
source_name=pop
{fonts}"""

# Adapt's own type (its TTFs ship in the theme)
ADAPT_FONTS = """default_font=a.ttf
default_font_size=17
font1=b.ttf
font2=c.ttf
font3=d.ttf
font4=b.ttf
font4_size=20
"""
# RIPgrid: RIPPS2 Sleek, the face made for RIPPS2, loaded from the ELF (nothing to ship). The same slots,
# in its weights: Sleek for the source name and hints, Sleek Bold for the grid's names and the release
# line, Sleek Bold Case (a true lowercase) for descriptions and anything typed.
RIPGRID_FONTS = """default_font=builtin:ripps2sleek
default_font_size=17
font1=builtin:ripps2sleekcase
font1_size=16
font2=builtin:ripps2sleek
font2_size=17
font3=builtin:ripps2sleekbold
font3_size=16
font4=builtin:ripps2sleekbold
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


def ripgrid(rx):
    # 4 x 2 covers centred in the room the side bar leaves; the highlight says which game it is, and only
    # it tips with the right stick (about its own centre; tilt_scale lets it turn further than a page)
    main = backdrop("main") + [
        block("main4", type="Grid", pattern="COV", x=340, y=62, width=120, height=168,
              columns=4, rows=2, spacing=16, font=4, tilt=1, tilt_scale=160),
        block("main5", type="ItemsList", x="POS_MID", y=45, width="DIM_INF", height=24, aligned=1,
              font=4, hidden=1),
    ] + common_tail("main", 6)
    return main, []


def write(folder, name, main, mainApps, infoEls, infoApps, extra="", fonts=ADAPT_FONTS):
    text = HEAD.format(name=name, fonts=fonts) + extra + "\n" + "\n".join(main + infoEls + mainApps + infoApps) + "\n"
    with open(os.path.join(ROOT, folder, "conf_theme.cfg"), "w", newline="\n") as f:
        f.write(text)
    print("wrote", folder)


if __name__ == "__main__":
    # RIPgrid has one side: the grid fills the page, so there is nothing to mirror
    for folder, name, make, rx in (("thm_Adapt", "Adapt", adapt, 0), ("thm_Adapt Rx", "Adapt Rx", adapt, 1),
                                   ("thm_RIPgrid", "RIPgrid", ripgrid, 0)):
        m, ma = make(rx)
        # the info page puts its text on the other side from the game list's: Adapt (list right) gets
        # text right and pictures left, Adapt Rx (list left) the reverse; RIPgrid keeps text left
        i, ia = info(1 - rx) if make is adapt else info(rx)
        # Rx: LAUNCH DISC at the bar's right end, over its disc (a default: the user's own order wins)
        extra = "category_order=memory_files_first\n" if rx else ""
        if make is ripgrid:
            extra += ("# RIPgrid's type: RIPPS2 Sleek (Regular, Bold, Bold Case), built into RIPPS2 (builtin: fonts)\n"
                      "# [circle.png] [cross.png] [square.png] [triangle.png] [select.png] from the Grunge theme;\n"
                      "# [start.png] drawn to match\n")
        write(folder, name, m, ma, i, ia, extra, RIPGRID_FONTS if make is ripgrid else ADAPT_FONTS)
