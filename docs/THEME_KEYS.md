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
| `use_settings_bg` | `0` / `1` | RiptOPL | `1` + `settings_bg.png`: Settings over that picture. Leave it out to get the pillars behind RIPPS2's glass page panel (RIPPS2's own look). |

## Element types RIPPS2 adds

### `Ripps2PanelGlass` (build 55; blur in 78)
A glass panel: a navy tint, light at the top and deepening from about a third down, with a thin
frame. Put it after the backdrop and before the text it sits under.

| Key | Values | Build | What it does |
|---|---|---|---|
| `x`,`y`,`width`,`height`,`aligned` | | 55 | The panel's rectangle. |
| `blur` | `0` / `1` | 78 | Frosted glass: what is behind the panel shows through softened. The source is the page's `Background` element -- the selected game's own background art once loaded, else the theme's `default=` -- shrunk to 80x60 and drawn stretched with bilinear filtering, made again only when the game or its art changes. Cheap enough for every page. |
| `tilt`, `tilt_x`, `tilt_y`, `tilt_scale` | | 70 | Right-stick tilt (below). |

**Page transitions.** RIPPS2 morphs one page's glass panel into the next when you move between the
game list and the info page (and into menus). It uses the **first** `Ripps2PanelGlass` of `main` and
of `info`: declare one on each page and the theme gets the full transition treatment. A theme with
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
| `default`, `overlay`, `overlay_*`, `reflection` | | As on `ItemCover` (placeholder, case art, mirror under the selection). |
| `tilt*` | | Right-stick tilt. |

The selection is drawn 12% larger, framed in `sel_text_color`, and last; the others a step dimmer.
Its art is asked for first, so a cold page fills from the cover in focus. The page scrolls by whole
rows to keep the selection in view.

Controls on a Grid theme: **Left / Right** one cover, **Up / Down** one row (held arrows repeat), and
**past the top or bottom row** a new press switches drive. L1/R1 still switch categories.

A Grid page **must also declare an `ItemsList` with `hidden=1`**: the engine adds a visible default
list to any page without one. Pair the grid with an `ItemText` for the selected game's name.

## Keys RIPPS2 adds to existing elements

| Key | On | Build | What it does |
|---|---|---|---|
| `tilt` | any image / panel | 70 | `1`: the element tips with the right stick on the game list and info page. |
| `tilt_x`, `tilt_y` | | 70 | The pivot. Elements sharing a pivot tip together as one plane. |
| `tilt_scale` | | 70 | The angle in percent of the default (1-400, default 100). |
| `alpha` | `GameImage` | 66 | Opacity 0-128 (128 opaque). |
| `slide` | `GameImage` | 59 | Info-page slideshow position 1-4. |
| `hidden` | `ItemsList` | RiptOPL | The list drives selection but is not drawn (Coverflow, Grid). |
| `line_height`, `vcenter` | `AttributeText` | 59 | Wrapped text line step; centre the text block in its height. |
| `item_height` | `ItemsList` | 59 | Row pitch. |
| `<font>_caps` | global font slot | 70 | `1`: that font draws in capitals. |

## RIPPS2 behaviour every theme gets
- Art fades in as it arrives; the info page's art appears as one group (up to 0.8 s wait).
- The category bar, button hints and source name follow Colors and More (fade when idle, hidden...).
- Sounds: a theme's `sound/` folder (`boot.adp`, `cursor.adp`, `confirm.adp`, `cancel.adp`,
  `message.adp`, `transition.adp`) replaces RIPPS2's for that theme.
