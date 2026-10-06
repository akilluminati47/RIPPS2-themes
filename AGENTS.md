# Building RIPPS2 themes: rules for agents

You are helping make themes for **RIPPS2** (github.com/akilluminati47/RIPPS2), a PS2 front end on
RiptOPL's theme engine. Read these before changing anything.

1. **A theme is a folder** `themes/thm_<Name>/` with `conf_theme.cfg` and its own images, fonts and
   optional `sound/`. Every theme carries its own copies of shared assets: the PS2 reads one folder.
2. **Know the keys.** [docs/THEME_KEYS.md](docs/THEME_KEYS.md) (RIPPS2's additions) and
   [docs/THEME_ENGINE_RiptOPL.md](docs/THEME_ENGINE_RiptOPL.md) (everything else). Never invent a key:
   the engine ignores what it does not know, silently.
3. **Numbering.** `main` and `info` run 0, 1, 2... with no gap; the engine stops at the first missing
   number. Other families (`appsMain`, `appsInfo`, `vcdMain`...) *replace* the element of the same
   number in their base family, so renumbering `main` moves every override with it. Re-check them.
4. **Always run** `python3 tools/check_theme.py themes/<folder>` (no errors) and
   `python3 tools/preview_theme.py themes/<folder> previews/<folder>.png`, and look at the preview,
   before you call a theme done. The preview is layout only; motion, tilt and fades need the console.
5. **Left / right variants**: `tools/mirror_theme.py` drafts the mirrored layout; then fix by hand
   anything that should not simply flip (left-aligned text inside a panel, directional art).
6. **If a look needs something the keys cannot express**, it is an engine change in RIPPS2
   (`elf/patches/` there), not a theme hack. Add the key to THEME_KEYS.md with the build it lands in,
   teach `tools/check_theme.py` about it, and keep the theme working on builds without it where you can.
7. **The Adapt family** (Adapt, Adapt Rx, RIPgrid, RIPgrid Rx) is written by
   `tools/gen_adapt_family.py`: change the layout there and run it, never their `conf_theme.cfg` by hand.
8. **Credit** every asset's maker in the `conf_theme.cfg` header and in `themes/README.md`.
9. Images: PNG, 640x480 for full-screen pieces; 8-bit palette PNGs keep VRAM and load times down
   (the frosted glass reads them fine). Fonts: TTF.
