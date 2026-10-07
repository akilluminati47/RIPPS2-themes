# What a RIPPS2 theme can do (build 90)

A RIPPS2 theme is a folder, `THM/thm_<Name>/`, on any drive RIPPS2 reads (USB, HDD, MMCE, a memory
card's `OPL/THM`). Everything on this page is driven from that folder: `conf_theme.cfg`, its images,
fonts and sounds. **Nothing here needs RIPPS2 rebuilt.** Make the folder, copy it, pick it.

RIPPS2 reads OPL / RiptOPL themes, so everything in [THEME_ENGINE_RiptOPL.md](THEME_ENGINE_RiptOPL.md)
works too (element blocks, families, attributes, Coverflow). This page is what RIPPS2 adds on top, and
how RIPPS2's own pages meet a theme. The build each key arrived in is given; an older build ignores a
key it does not know, so a theme stays usable on it.

**Contents:** [the folder](#the-folder) · [coordinates](#coordinates) · [global keys](#global-keys) ·
[Colors and More from the theme](#colors-and-more-from-the-theme-build-81) ·
[hints and glyphs](#hints-and-glyphs-build-90) · [fonts](#fonts) ·
[element types](#element-types-ripps2-adds) · [keys on existing elements](#keys-ripps2-adds-to-existing-elements) ·
[effects and tricks](#effects-and-tricks) · [replacing RIPPS2's own images](#replacing-ripps2s-own-images) ·
[sounds and music](#sounds-and-music) · [what every theme gets](#what-every-theme-gets) ·
[what a theme cannot change](#what-a-theme-cannot-change-yet)

## The folder

| File | What it is |
|---|---|
| `conf_theme.cfg` | The layout and the keys below. Plain `key=value`; element blocks are `main0:` and indented keys. |
| `*.png` | Images. **8-bit palette PNGs**: RIPPS2 keeps those as 8-bit textures with a 32-bit palette (alpha included), a quarter of the VRAM of RGBA and quicker to load. `tools/png8.py` converts. 640x480 for full-screen pieces. |
| `*.ttf` | Fonts, named in the font keys. |
| `sound/*.adp` | The theme's sounds, by event (see [sounds](#sounds-and-music)). |
| `sound/bgm.ogg` | The theme's music. |
| `<name>.png` | Any of RIPPS2's own images, replaced by name (see [replacing](#replacing-ripps2s-own-images)). |

## Coordinates
RIPPS2 lays out in a 640x480 space, scaled to the video mode (720p and 1080i included, build 75).
`x` / `y` count from the left / top; a negative value counts from the right / bottom. `POS_MID` is the
centre. `aligned=1` (the default for most elements) centres the element on `x`,`y`; `aligned=0` makes
`x`,`y` its top-left corner. `scaled=1` narrows width for 16:9 so shapes stay true (covers, cases,
screenshots).

## Global keys

| Key | Values | Build | What it does |
|---|---|---|---|
| `bg_color` | `#RRGGBB` | OPL | The page colour behind everything (shows where there is no art and `towers=0`). |
| `text_color`, `ui_text_color`, `sel_text_color`, `title_color` | `#RRGGBB` | OPL | Text, menu text, the selection (also the Grid's glow), titles. |
| `default_font`, `font1` ... `font15` | a `.ttf` in the folder, or a `builtin:` font | OPL / 59 | The 16 font slots. See [fonts](#fonts). |
| `<font>_size` | pixels | OPL | `font4_size=20`. |
| `<font>_caps` | `0` / `1` | 70 | `1`: that font draws in capitals. |
| `towers` | `0` / `1` (default 1) | 78 | `0`: the game pages never show RIPPS2's pillars. Where a page has no image (a game without art, or art still fading in) `bg_color` shows instead. Settings keep the pillars behind glass unless the theme ships `settings_bg`. |
| `source_name` | `pop`, `shown`, `fade`, `hidden` | 80 / 81 | How the source's name (ALL GAMES, HDD GAMES...) appears. `pop` (build 81): not drawn over the list, it plays as a toast in the middle of the page, the whole name in big capitals, on the first list after boot, on a source change and on coming back to Storage, then fades. `shown` / `fade` (with the category bar's idle fade) / `hidden` (build 81). A theme default: [the user wins](#colors-and-more-from-the-theme-build-81). |
| `use_settings_bg` | `0` / `1` | OPL | `1` + `settings_bg.png`: Settings over that picture. Leave it out for the pillars behind RIPPS2's glass page panel. |
| `use_default` | `0` / `1` (default 1) | OPL | `0`: an image the theme does not ship stays empty instead of falling back to RIPPS2's own. |
| `coverflow_cover_offset` | pixels | RiptOPL | Coverflow's cover offset (see the engine reference). |

## Colors and More from the theme (build 81)

Colors and More (Settings > Interface) is the user's: colour theme, category bar, hints, D-pad glyphs,
category order, source name. A theme can choose its own for each, so it arrives looking the way it was
made:

| Key | Values | The Colors and More row |
|---|---|---|
| `color_theme` | `ripps2`, `ember`, `blood`, `ectoplasm`, `amethyst`, `bone` | Color Theme: one colour matrix over everything RIPPS2 draws itself (towers, orbs, glass, its pages). Greys and art never change, only the blues move. |
| `category_bar` | `shown`, `fade`, `hidden` | LAUNCH DISC, STORAGE, MEMORY FILES along the top. `fade`: fades after 6 s idle, back on a press. |
| `button_hints` | `shown`, `fade`, `hidden` | The button hints along the bottom of the three tabs. |
| `dpad_glyphs` | `hidden`, `shown`, `fade_in`, `fade_out` | The D-pad glyphs beside a drive's name. |
| `category_order` | `launch_disc_first`, `memory_files_first` | Which end of the bar Memory Files sits. RIPFLOW uses `memory_files_first`. |
| `source_name` | `pop`, `shown`, `fade`, `hidden` | Source Name (above). |

**The user always wins.** RIPPS2 remembers which of these rows the user has changed (saved as
`ripps2_userset`). A theme's value shows only on a row the user has never touched that still holds its
own default; anything the user picks, the default included, stays theirs on every theme. Colors and More
shows what is in effect, so the user sees the theme's choice and can change it.

## Hints and glyphs (build 90)

The hint bar and the button glyphs. Each key is the theme's default for a row of Controller Settings >
Hints and Glyphs, where every row starts on **Theme** (this key) and anything else the user picks wins.

| Key | Values | What it does |
|---|---|---|
| `hints_hide` | hint names, comma separated | Leaves those hints off the bar. The buttons still work. |
| `hints_order` | hint names, comma separated | The hints named come first, in that order; the rest follow in the order the page adds them. |
| `hints_labels` | `1` (default), `0`, `badge` | `0`: glyphs only, for glyph art that carries its own words (a hint whose glyph the theme lacks keeps its label). `badge`: each hint is one badge, its glyph and title together on a pill (`hint_badge.png`, or the glyph set's own), the pill's ends kept round and its middle stretched to the title. Never on unless a theme sets it or the user picks Badges. |
| `hints_layout` | `row` (default), `column` | `column`: one hint a line, from the hint element's `x`/`y` down. A column that would run off the bottom ends on the bar's line instead, so the default hint element gives a column in the bottom left corner. |
| `hints_spacing` | 12 to 96 (default 28) | A column's line pitch. |
| `glyph_set` | `theme` (default), `ripps2`, `standard`, `white` | The glyphs on every page. `theme` is the theme's own PNGs (below); `ripps2` is RIPPS2's outlined set; `standard` is the Adapt theme's dark glossy buttons; `white` is the Grunge theme's solid white. The built-in sets cover every glyph, the shoulder buttons, sticks and D-pad included. |

Hint names: `menu` `run` `info` `options` `refresh` `star` `view` `source` (`source` is Coverflow and
Grid's source cycling). Their buttons name them too: `start` `select` `r3` `l3` `cross` `circle` `square`
`triangle`. For example, a sidebar theme:

```
hints_layout=column
hints_spacing=30
hints_order=run,info,options
hints_hide=refresh
```

## The launch disc (build 91)

| Key | Values | What it does |
|---|---|---|
| `launch_disc` | `pop`, `spin` (default: none) | As a game launches, its disc comes in over the middle of the screen: the game's ICO art, else `launch_disc.png` (yours, or RIPPS2's disc). `pop` settles in like the L3 logos and fades; `spin` settles in, then turns faster and faster and never fades. The user can override it in Flow and Grid > Launch Disc. RIPgrid uses `pop`, RIPFLOW `spin`. |

## Fonts

A theme has 16 font slots: `default_font` (slot 0) and `font1` to `font15`, each a `.ttf` in the folder
or one of RIPPS2's built-in faces:

| `builtin:` | Face |
|---|---|
| `builtin:ripps2` | RIPPS2's text face (the built-in theme's default) |
| `builtin:ripps2sleek` | RIPPS2 Sleek: hints, menus, settings |
| `builtin:ripps2sleekbold` | its bold weight: text beside big glyphs, the view word |
| `builtin:ripps2sleekcase` | bold with a true lowercase: typed text, tooltips |
| `builtin:ripflow` | Roboto Condensed (RIPFLOW's text) |
| `builtin:ripflowbold` | Roboto Bold Condensed (RIPFLOW's menus) |

Elements pick a slot with `font=<n>`. RIPPS2's own pages (menus, the category bar, Memory Files, the CD
player...) draw in fixed slots too, so **setting these restyles RIPPS2 itself**. A slot a theme leaves
out falls back to its `default_font`.

| Slot | RIPPS2 draws with it |
|---|---|
| `font2` | the selected category on the bar |
| `font3` | Launch Disc's line about the disc in the drive |
| `font4` | menus, Settings, dialogs, message boxes (RIPPS2's UI font) |
| `font5` | small text: About, the CD player's details |
| `font6` | text beside a button glyph (the START prompts) |
| `font7` | the other categories on the bar |
| `font8` | rows in Memory Files and the CD player's track list |
| `font9` | a title in true case (RetroAchievements) |
| `font10` | About's small print |
| `font11` | the CD player's track title |
| `font14` | the Achievements page's big numbers. A theme without `font14` gets RIPPS2 Sleek Bold at 64 px here (build 81; `font14_size` still sets it), not its default font. (Up to build 80 it also drew L3's view word; from build 81 L3's ALL / PS1 / PS2 and the Pop In toast draw in RIPPS2 Sleek Bold 64 on every theme, so they move the same everywhere.) |
| `font15` | typed text and tooltips, in true lowercase |

## Element types RIPPS2 adds

### `Ripps2PanelGlass` (build 55; blur in 78; tint, tint_color, frame in 79)
A glass panel: by default a navy tint, light at the top and deepening from about a third down, with a
thin frame. Put it after the backdrop and before the text it sits under. With `tint=` it is clear glass
instead: one even tint over the whole panel.

| Key | Values | Build | What it does |
|---|---|---|---|
| `x`,`y`,`width`,`height`,`aligned` | | 55 | The panel's rectangle. |
| `blur` | `0` / `1` | 78 | Frosted glass: what is behind shows through softened. The source is the page's `Background` (the game's own art once loaded, else the theme's `default=`) shrunk to 80x60 and drawn stretched with bilinear filtering, made again only when the game or its art changes. Cheap enough for every page. |
| `tint` | 0-128 | 79 | One constant tint instead of the gradient (128 opaque; 20-50 reads as glass). |
| `tint_color` | `#RRGGBB` (default `#040C2E`) | 79 | The tint's colour. Dark and high makes a strip (Adapt's side bar); light and low a highlight rule. |
| `frame` | `0` / `1` (default 1) | 79 | The thin frame line. `0` for layers that are not panels. |
| `tilt*` | | 70 | Right-stick tilt (below). |

### `Grid` (build 78)
The game list as a page of covers in rows, backed by the cover art (`COV`).

| Key | Default | What it does |
|---|---|---|
| `x` | `POS_MID` | The grid's horizontal centre. |
| `y` | 60 | The top of the first row. |
| `width`,`height` | 104 x 146 | One cover. |
| `columns` | 4 (1-8) | Covers across. |
| `rows` | 2 (1-4) | Rows on a page. Build 82: the grid moves by whole pages, the new page sliding in as the old one slides away (eased like RIPFLOW's carousel; off when Coverflow's animation speed is 0). |
| `spacing` | 14 | Pixels between covers. |
| `default` | none | A placeholder for games without art. Leave it out: those games get a clear glass tile with their name instead (build 79). |
| `overlay`, `overlay_*`, `reflection` | | As on `ItemCover` (case art, a mirror under the selection). |
| `font` | | The name on a no-art tile. |
| `tilt*` | | Build 80: tips only the chosen cover, about its own centre (its glow with it). `tilt_scale` lets one cover turn further than a page. |
| `back_pattern` | `COV2` | Build 82: the art on the back of a turned case. Hold the right stick to one side for 2 seconds and the chosen case turns over to it; it stays turned until held again. Any art suffix works (`SCR` puts a screenshot on the back); `0` leaves the cases unturnable. The back is asked for as soon as the front is in, from a cache of its own. |

Controls on a Grid theme: Left / Right one cover, Up / Down one row, past the top or bottom row a new
press switches drive, the cancel button cycles the sources (the hint row says *Source*), and a 2-second
right-stick hold turns the chosen case over (build 82). A Grid
page **must also declare an `ItemsList` with `hidden=1`**: the engine adds a visible list to any page
without one.

## Keys RIPPS2 adds to existing elements

| Key | On | Build | What it does |
|---|---|---|---|
| `tilt` | any image or panel, text too | 70 | `1`: the element tips with the right stick on the game list and info page. |
| `tilt_x`, `tilt_y` | | 70 | The pivot. Elements sharing a pivot tip together as one plane. |
| `tilt_scale` | | 70 | The angle in percent of the default (1-400, default 100). |
| `overlay2` | `ItemCover`, `GameImage`, `Grid` | RiptOPL | A second overlay drawn over the art (RIPPS2's case: `overlay=case overlay2=case_overlay`). |
| `reflection`, `reflection_offset` | cover elements | RiptOPL | A mirror image under the art, fading out; the offset moves it down. |
| `alpha` | `GameImage` | 66 | Opacity 0-128. |
| `widecrop` | `Background` | 79 | `1`: on a 16:9 picture 4:3 art zooms (its middle three quarters of height) instead of stretching. Frosted panels follow the crop. |
| `slide` | `GameImage` | 59 | Slideshow position 1-4: the page's slides take turns (5 s each, a 1 s crossfade), each in its own place with its own overlay and reflection. Any page: the info page's art (BG, SCR, SCR2), or a game list's case showing the front cover (`COV`) then the back (`COV2`), as Adapt does (build 81). A game without a slide's art skips it. |
| `hidden` | `ItemsList` | RiptOPL | The list drives selection but is not drawn (Coverflow, Grid). |
| `line_height`, `vcenter` | `AttributeText` | 59 | Wrapped text's line step; centre the block in its height. With either set, text longer than its box **rolls** through it. One-line text always scrolls in its room. |
| `item_height` | `ItemsList` | 59 | Row pitch. The highlighted row's bar fills the row, and from build 83 every title is centred on its row by its own font's centreline (measured from the face), so any font sits in the middle of the bar with nothing to adjust. |
| `devices` | any element | RiptOPL | Show the element only on some devices (see the engine reference). |

## Effects and tricks

- **The frosted screen** (build 79). A full-screen panel straight after the `Background`,
  `x=0 y=0 width=640 height=480 aligned=0 blur=1 tint=24 frame=0`, puts every game's art under frosted
  glass: no hard edges, no stretched pixels, and what sits on it stays readable. Panels after it frost
  the same art, so they read as one sheet. Adapt and RIPgrid do this.
- **A side bar** is two frameless panels: a dark strip (`tint=88 tint_color=#01040F`) and a light rule
  beside it (`tint=22 tint_color=#28C5F9`).
- **Page transitions.** RIPPS2 morphs one page's glass into the next between the game list and the info
  page (and into menus), using the **first framed** `Ripps2PanelGlass` of `main` and of `info`. Declare
  one on each page and the theme gets the full transition. A theme with none keeps its backdrop and
  switches the content (RIPFLOW's way).
- **One-sheet tilt.** Give every element of the info page the same `tilt=1 tilt_x=320 tilt_y=260` and
  the page tips as one plane with the right stick, text included. A cover and its disc sharing a pivot
  tip together.
- **RIPPS2's case**: an `ItemCover` at 143 x 201 with `overlay=case overlay2=case_overlay`, overlay
  corners at the four corners and `reflection=1`. `scaled=1` keeps it true on 16:9.
- **4:3 screenshots on any screen**: a `GameImage` (`pattern=SCR`, then `SCR2`) with `scaled=1` in a
  frame overlay (Adapt's `SCR43.png`).
- **Art eases in** as it arrives; the info page's pieces appear as one group (up to 0.8 s).
- **Rolling descriptions**: set `line_height` on a wrapped `AttributeText` and a long description rolls.
- **Settings over the pillars**: leave out `use_settings_bg`.
- **No towers**: `towers=0` and a `bg_color`, for a theme that is all art.
- **The source as a toast**: `source_name=pop`.
- **Arrive in your colours**: `color_theme=` and the other Colors and More keys.
- **Left / right variants**: `tools/mirror_theme.py` drafts the other side; the Adapt family keeps its
  side bar left and swaps the content (`tools/gen_adapt_family.py`).

## Replacing RIPPS2's own images

Any of these, shipped in the theme folder as `<name>.png`, replaces RIPPS2's own (8-bit palette, alpha
kept). Leave one out and RIPPS2 uses its own, unless `use_default=0`.

| Group | Names |
|---|---|
| Launch disc | `launch_disc` (build 91: the disc `launch_disc=pop|spin` brings in when a game has no ICO art; square, round, transparent outside) |
| Button glyphs | `cross` `circle` `square` `triangle` `select` `start` `L1` `R1` `L3` `R3` `L2R2` `left` `right` `ripps2_up` `ripps2_down` `hint_badge` (build 90: the pill for `hints_labels=badge`; make it 40 x 28 or so with a flat middle) |
| Loading | `load0` ... `load7` |
| Devices | `usb` `usb_bd` `ilk_bd` `m4s_bd` `hdd_bd` `hdd` `mmce` `eth` `udp_bd` `udp_fs` `app` `Index_0` ... `Index_4` `no_Device` `Device_1` ... `Device_6` `Device_all` |
| Badges | `ELF` `HDL` `ISO` `VCD` `ZSO` `UL` `APP` `CD` `DVD` `PS1` `PS2` `Aspect_s` `Aspect_w` `Aspect_w1` `Aspect_w2` `Rating_0` ... `Rating_5` `no_Rating` `Scan_240p` `Scan_240p1` `Scan_480i` `Scan_480p` ... `Scan_480p5` `Scan_576i` `Scan_576p` `Scan_720p` `Scan_1080i` `Scan_1080i2` `Scan_1080p` `Vmode_multi` `Vmode_ntsc` `Vmode_pal` |
| Art stand-ins | `cover` `disc` `screen` `screens` `coverapp` `missing` `case` `case_overlay` `apps_case` `logo` `logo0` ... `logo6` `fav` `fav_mark` `settings_bg` |
| RIPPS2's marks | `ripps2_mark` (the PS2 mark that flies along the category bar) `ripps2_mark_glow` `ripps2_glass` `ripps2_ps1logo` `ripps2_ps2logo` (L3's view word) `ripps2_grid_icons` `ra_mark` |

## Sounds and music

A theme's `sound/` folder replaces RIPPS2's sounds while the theme is on: any of the 15 events, as
`.adp` (mono SPU2 ADPCM; RIPPS2 Audio Studio converts any sound). An event the theme leaves out keeps
RIPPS2's own.

| File | Plays |
|---|---|
| `boot.adp` | as the towers rise at power on |
| `cursor.adp` | moving the cursor |
| `confirm.adp` | choosing something |
| `cancel.adp` | going back |
| `message.adp` | a message box opens |
| `transition.adp` | switching tabs |
| `bd_connect.adp`, `bd_disconnect.adp` | a drive arrives, a drive is removed |
| `page_in.adp`, `page_out.adp` | opening a page, closing it |
| `error.adp` | an error message |
| `save.adp` | settings saved |
| `launch.adp` | a game launching |
| `disc.adp` | a disc read in Launch Disc |
| `random.adp` | L2 + R2 picks a random game |

`sound/bgm.ogg` is the theme's music (Ogg Vorbis at a fixed bitrate, no tags). It plays instead of the
user's AUDIO music while the theme is on. Every sound
is loaded into the SPU2's 2 MB at once (music streams), so keep the set small.

## What every theme gets
- Art fades in as it arrives; covers on a Grid ease in once per game.
- Hold **SELECT 4.2 seconds** on the game list to step to the next theme (build 79), once per hold, and
  it is saved; a shorter press refreshes the list.
- L3's view word and the Pop In toast in RIPPS2 Sleek Bold 64 (build 81), the same on every theme, and the category bar's flying mark.
- Colors and More, with the theme's own defaults where it gives them.
- Hints and Glyphs (build 90): the user can hide, reorder or relabel the hints and pick a glyph set on any theme.
- 720p and 1080i in one pass at full detail (build 75).

## What a theme cannot change (yet)
These are RIPPS2's own and need an engine change (`elf/patches` in RIPPS2), not a theme: the towers'
and orbs' shapes and motion (a theme can turn the towers off and recolour them with `color_theme`), the
layout of Launch Disc, Memory Files, STATUS and the Achievements pages (they take the theme's fonts and
colours), where the view word and toasts sit, and the Grid glow's timing. If a look needs one of these,
ask for a key in RIPPS2's issues: new keys land here with the build that brings them.
