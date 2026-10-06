# RIPPS2 theme keys

RIPPS2 reads OPL / RiptOPL themes (a `thm_<Name>` folder with `conf_theme.cfg`): everything in
[THEME_ENGINE_RiptOPL.md](THEME_ENGINE_RiptOPL.md) works. This page lists what RIPPS2 adds and how its
own behaviour meets a theme. The build each key arrived in is given; a theme using a key needs that
RIPPS2 build or later (older builds ignore keys they do not know).

## Coordinates in one paragraph
RIPPS2 lays out in a 640x480 space, scaled to the video mode (720p and 1080i included, build 75).
`x` / `y` count from the left / top; a negative value counts from the right / bottom. `POS_MID` is
the centre. `aligned=1` (the default for most elements) centres the element on `x`,`y`; `aligned=0`
makes `x`,`y` its top-left corner. `scaled=1` narrows width for 16:9 (widescreen keeps shapes round).

## Global keys

| Key | Values | Build | What it does |
|---|---|---|---|
| `towers` | `0` / `1` (default 1) | 78 | `0`: the game pages never show RIPPS2's pillars. Where a page has no image (a game without background art, or while its art fades in) the theme's `bg_color` shows instead. Settings still show the pillars behind glass unless the theme ships `settings_bg`. |
| `source_name` | `pop` | 80 | The theme's Source Name (ALL GAMES, HDD GAMES...) is Pop In: it rises in letter by letter, as L3's view word does, when the page opens or the source changes, then stays. It stands in for the setting's Shown; a user who picks Fade When Idle, Hidden or Pop In in Colors and More gets that. |
| `use_settings_bg` | `0` / `1` | RiptOPL | `1` + `settings_bg.png`: Settings over that picture. Leave it out to get the pillars behind RIPPS2's glass page panel (RIPPS2's own look). |

## Element types RIPPS2 adds

### `Ripps2PanelGlass` (build 55; blur in 78; tint, tint_color, frame in 79)
A glass panel: by default a navy tint, light at the top and deepening from about a third down, with a
thin frame. Put it after the backdrop and before the text it sits under. With `tint=` it is clear glass
instead: one even tint over the whole panel.

| Key | Values | Build | What it does |
|---|---|---|---|
| `x`,`y`,`width`,`height`,`aligned` | | 55 | The panel's rectangle. |
| `blur` | `0` / `1` | 78 | Frosted glass: what is behind the panel shows through softened. The source is the page's `Background` element -- the selected game's own background art once loaded, else the theme's `default=` -- shrunk to 80x60 and drawn stretched with bilinear filtering, made again only when the game or its art changes. Cheap enough for every page. |
| `tint` | 0-128 | 79 | One constant tint instead of the gradient (128 opaque; 20-50 reads as glass). With `blur=1` the art stays a soft, even presence behind the text. |
| `tint_color` | `#RRGGBB` (default `#040C2E`) | 79 | The tint's colour. A dark `tint_color` with a high `tint` makes a contrasting strip (Adapt's side bar); a light one at a low `tint` a highlight rule. |
| `frame` | `0` / `1` (default 1) | 79 | The thin frame line. `0` for layers that are not panels: a full-screen frosted layer, a side bar. |
| `tilt`, `tilt_x`, `tilt_y`, `tilt_scale` | | 70 | Right-stick tilt (below). |

The frost eases in with the art under it, and where a game has no background art the panel is just its
tint over `bg_color` / the pillars.

**The frosted screen (build 79).** A full-screen panel straight after the `Background` --
`x=0 y=0 width=640 height=480 aligned=0 blur=1 tint=24 frame=0` -- puts every game's art under frosted
glass: no hard edges, no stretched pixels, and the panels and covers over it stay readable. Panels after it
frost the same art, so they read as one sheet of glass. Adapt and RIPgrid do this on both pages.

**Page transitions.** RIPPS2 morphs one page's glass panel into the next when you move between the
game list and the info page (and into menus). It uses the **first framed** `Ripps2PanelGlass` of `main` and
of `info` (build 79: frameless layers such as the frosted screen or a side bar are skipped; a page with
only frameless ones uses its first): declare one on each page and the theme gets the full transition
treatment. A theme with
none keeps its backdrop in place and switches the content (RIPFLOW's way).

### `Grid` (build 78)
The game list as a page of covers in rows. Backed by the cover art (`COV`) like `ItemCover`.

| Key | Default | What it does |
|---|---|---|
| `x` | `POS_MID` | The grid's horizontal centre. |
| `y` | 60 | The top of the first row. |
| `width`,`height` | 104 x 146 | One cover. |
| `columns` | 4 (1-8) | Covers across. |
| `rows` | 2 (1-4) | Rows on screen. |
| `spacing` | 14 | Pixels between covers. |
| `default` | none | A placeholder for games without art. Leave it out (build 79): those games get a clear glass tile with their name instead, so no stock disc or case fills the grid. |
| `overlay`, `overlay_*`, `reflection` | | As on `ItemCover` (case art, mirror under the selection). |
| `font` | | The font of the name on a no-art tile. |
| `tilt*` | | Right-stick tilt. |

Each cover eases in as its art arrives (build 79), remembered per game, so scrolling back does not fade
again. The selection is drawn 12% larger and last with a **breathing glow** in `sel_text_color` (soft
rings swelling and easing over 2.4 s, under a crisp frame); the others a step dimmer. Its art is asked
for first, so a cold page fills from the cover in focus. The page scrolls by whole rows to keep the
selection in view. The glow says which game is selected, so a grid needs no name panel.

Controls on a Grid theme: **Left / Right** one cover, **Up / Down** one row (held arrows repeat), and
**past the top or bottom row** a new press switches drive. L1/R1 still switch categories. Build 80:
the **cancel button** (Circle, or Cross with Circle to select) cycles the sources on the game list, on Grid
and Coverflow themes alike, and the hint row says *Source*; inside a folder it climbs out first, and on the
info page it is still Back.

**Tilt on a Grid (build 80):** `tilt=1` tips only the chosen cover, about its own centre (its glow with
it); the rest of the page holds still. `tilt_scale` (100 = a page's angle) lets one cover turn further.

A Grid page **must also declare an `ItemsList` with `hidden=1`**: the engine adds a visible default
list to any page without one.

## Keys RIPPS2 adds to existing elements

| Key | On | Build | What it does |
|---|---|---|---|
| `tilt` | any image / panel | 70 | `1`: the element tips with the right stick on the game list and info page. |
| `tilt_x`, `tilt_y` | | 70 | The pivot. Elements sharing a pivot tip together as one plane: give every piece of an info page (text included, it tilts too) the same pivot and the page moves as one sheet. |
| `tilt_scale` | | 70 | The angle in percent of the default (1-400, default 100). |
| `alpha` | `GameImage` | 66 | Opacity 0-128 (128 opaque). |
| `widecrop` | `Background` | 79 | `1`: on a 16:9 picture the art shows its middle three quarters of height (a zoom, the faux crop) instead of stretching 4:3 art wide. Frosted panels over it follow the same crop. |
| `slide` | `GameImage` | 59 | Info-page slideshow position 1-4. |
| `hidden` | `ItemsList` | RiptOPL | The list drives selection but is not drawn (Coverflow, Grid). |
| `line_height`, `vcenter` | `AttributeText` | 59 | Wrapped text line step; centre the text block in its height. With either set, wrapped text longer than its box **rolls** through it (set one on every description). One-line text always scrolls inside its room. |
| `item_height` | `ItemsList` | 59 | Row pitch. |
| `<font>_caps` | global font slot | 70 | `1`: that font draws in capitals. |

## RIPPS2 behaviour every theme gets
- Art fades in as it arrives; the info page's art appears as one group (up to 0.8 s wait).
- Switching themes from the game list (build 79): **hold SELECT 4.2 seconds** and RIPPS2 steps to the
  next theme in Settings > Interface > Theme, once per hold, and saves it; a press under 4.2 s refreshes
  the list as before. Handy for trying a theme you are working on against the others.
- The category bar, button hints and source name follow Colors and More (fade when idle, hidden...).
- Sounds: a theme's `sound/` folder (`boot.adp`, `cursor.adp`, `confirm.adp`, `cancel.adp`,
  `message.adp`, `transition.adp`) replaces RIPPS2's for that theme.
