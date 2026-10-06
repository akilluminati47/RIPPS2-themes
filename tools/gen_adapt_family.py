"""Write conf_theme.cfg for the four Adapt-family themes (Adapt, Adapt Rx, RIPgrid, RIPgrid Rx) from one
layout, so the shared pieces -- the frosted screen, the side bar, the info page -- stay in step.

    python3 tools/gen_adapt_family.py

Layers, back to front, on the game list and the info page alike:
  Background (each game's art, widecrop in 16:9) -> a full-screen frosted layer (blur, low tint, no
  frame) -> the side bar (a dark frosted strip and a light rule, frameless) -> the framed glass panel
  under the text -> the art and text.
"""
import os

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "themes")

HEAD = """# Theme Name: {name}
# Made by: akilluminati47 (Adapt RiptOPL, 8/27/2026), RIPPS2 edition (build 79)
# RIPPS2: each game's art under frosted glass (a full-screen Ripps2PanelGlass, blur=1), a frosted side
# bar, clear glass panels under the text, page morphs between the list and the info page, the pillars
# behind Settings (no settings_bg), right-stick tilt on the art. Art eases in; no stock disc or case.

bg_color=#050A1C
sel_text_color=#0064FF
text_color=#FFFFFF
ui_text_color=#C4DAFF
towers=0
default_font=a.ttf
default_font_size=17
font1=b.ttf
font2=c.ttf
font3=d.ttf
font4=b.ttf
font4_size=20
"""

FROST_TINT, PANEL_TINT, BAR_TINT, RULE_TINT = 24, 44, 88, 22


def block(name, **kv):
    out = [name + ":"]
    for k, v in kv.items():
        out.append("\t%s=%s" % (k, v))
    return "\n".join(out)


def backdrop(fam, rx):
    """Background, the frosted screen, the side bar's strip and rule: indices 0-3 of main and info."""
    bar_x, rule_x = (614, 600) if rx else (0, 28)
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
    return block(name, type="GameImage", pattern=pattern, scaled=1, x=x, y=y, overlay="SCR_overlay",
                 overlay_ulx=6, overlay_uly=4, overlay_urx=171, overlay_ury=4,
                 overlay_llx=6, overlay_lly=115, overlay_lrx=171, overlay_lry=115,
                 tilt=1, tilt_x=x, tilt_y=290)


def info(rx):
    # the text panel sits clear of the side bar; the screenshots take the other side
    gx = 195 if rx else 45    # glass left (395 wide: clear of the side bar and the screenshots)
    tx = gx + 10              # text left
    ax = gx + 15              # first attribute icon
    sx = 106 if rx else 532   # screenshots' centre
    els = backdrop("info", rx) + [
        block("info4", type="Ripps2PanelGlass", aligned=0, x=gx, y=160, width=395, height=255,
              blur=1, tint=PANEL_TINT, frame=1, tilt=1, tilt_x=gx + 197, tilt_y=287),
        block("info5", type="GameImage", pattern="LGO", x="POS_MID", y=100, aligned=1, width=300,
              height=125, tilt=1, tilt_x=330 if rx else 320, tilt_y=100),
        block("info6", type="AttributeImage", attribute="Rating", default="rating/0_Rating", aligned=0, x=ax, y=177),
        block("info7", type="AttributeImage", attribute="Scan", aligned=0, x=ax + 172, y=173),
        block("info8", type="AttributeImage", attribute="Players", aligned=0, x=ax + 122, y=173),
        block("info9", type="AttributeText", attribute="Description", aligned=0, display=2, x=tx, y=210,
              width=375, height=100, wrap=1, font=1),
        block("info10", type="AttributeText", attribute="Developer", aligned=0, display=2, x=tx, y=330,
              width=375, wrap=0, font=2),
        block("info11", type="AttributeText", attribute="Release", aligned=0, display=2, x=tx, y=358,
              width=375, font=3),
        block("info12", type="AttributeText", attribute="Genre", display=2, aligned=0, x=tx, y=385,
              width=375, font=2),
        block("info13", type="InfoHintText", aligned=1, x="POS_MID", y=-41, font=3),
        screenshot("info14", "SCR", sx, 225),
        screenshot("info15", "SCR2", sx, 356),
        block("info16", type="AttributeImage", attribute="Parental", aligned=0, scaled=1, x=ax + 303, y=330),
        block("info17", type="AttributeImage", attribute="Vmode", aligned=0, x=ax + 272, y=173),
        block("info18", type="AttributeImage", attribute="Aspect", aligned=0, x=ax + 222, y=173),
    ]
    # apps: the app's cover where the logo was, no screenshots
    apps = [
        block("appsInfo5", type="ItemCover", width=135, height=190, x=sx, y=270, aligned=1, scaled=1,
              reflection=1, tilt=1, tilt_x=sx, tilt_y=270),
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


def adapt(rx):
    gx = 25 if rx else 188    # list glass
    cx = 530 if rx else 110   # cover and disc centre
    main = backdrop("main", rx) + [
        block("main4", type="Ripps2PanelGlass", aligned=0, x=gx, y=76, width=432, height=309,
              blur=1, tint=PANEL_TINT, frame=1),
        block("main5", type="ItemCover", width=135, height=190, x=cx, y=277, aligned=1, scaled=1,
              reflection=1, tilt=1, tilt_x=cx, tilt_y=200),
        block("main6", type="ItemIcon", aligned=1, scaled=1, x=cx, y=96, width=120, height=120,
              tilt=1, tilt_x=cx, tilt_y=200),
        block("main7", type="ItemsList", x=gx + 12, y=88, aligned=0, width=420, height=285, font=4),
    ] + common_tail("main", 8)
    # apps: one wide glass list clear of the side bar, no cover or disc
    ax = 24 if rx else 48
    apps = [
        block("appsMain4", type="Ripps2PanelGlass", aligned=0, x=ax, y=40, width=568, height=368,
              blur=1, tint=PANEL_TINT, frame=1),
        block("appsMain5", type="ItemCover", enabled=0),
        block("appsMain6", type="ItemIcon", enabled=0),
        block("appsMain7", type="ItemsList", x=ax + 10, y=75, aligned=0, width=548, height=323, font=4),
    ]
    return main, apps


def ripgrid(rx):
    # 4 x 2 covers centred in the room the side bar leaves; the highlight says which game it is
    main = backdrop("main", rx) + [
        block("main4", type="Grid", pattern="COV", x=300 if rx else 340, y=62, width=120, height=168,
              columns=4, rows=2, spacing=16, font=4, tilt=1, tilt_x=300 if rx else 340, tilt_y=238),
        block("main5", type="ItemsList", x="POS_MID", y=45, width="DIM_INF", height=24, aligned=1,
              font=4, hidden=1),
    ] + common_tail("main", 6)
    return main, []


def write(folder, name, main, mainApps, infoEls, infoApps):
    text = HEAD.format(name=name) + "\n" + "\n".join(main + infoEls + mainApps + infoApps) + "\n"
    with open(os.path.join(ROOT, folder, "conf_theme.cfg"), "w", newline="\n") as f:
        f.write(text)
    print("wrote", folder)


if __name__ == "__main__":
    for folder, name, make, rx in (("thm_Adapt", "Adapt", adapt, 0), ("thm_Adapt Rx", "Adapt Rx", adapt, 1),
                                   ("thm_RIPgrid", "RIPgrid", ripgrid, 0), ("thm_RIPgrid Rx", "RIPgrid Rx", ripgrid, 1)):
        m, ma = make(rx)
        i, ia = info(rx)
        write(folder, name, m, ma, i, ia)
