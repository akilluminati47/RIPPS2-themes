# RIPPS2 themes

Themes for [RIPPS2](https://github.com/akilluminati47/RIPPS2), the PS2 front end, and the kit for
making more: key reference, a checker, a layout previewer and a left/right mirror tool. Built so that
people and coding agents alike can add a theme and know it will load before it reaches a console.

## The themes

| Theme | Look | Needs RIPPS2 |
|---|---|---|
| **Adapt** / **Adapt Rx** | akilluminati47's Adapt (RiptOPL): each game's background art under a dark vignette, cover and disc on one side, the list on frosted glass on the other (Rx: mirrored). Info page on frosted glass, page morphs between them, Settings over the pillars, the art tips with the right stick, no towers on the game pages. | build 78 |
| **RIPgrid** / **RIPgrid Rx** | Adapt's look with the games as a 3x2 cover grid beside a frosted panel holding the disc and the selected title (Rx: panel on the right). | build 78 |

Install: copy a `thm_...` folder into a `THM` folder on your drive (USB, HDD, MMCE, memory card), as
for any OPL theme, then pick it in RIPPS2's Settings > Interface > Theme.

## The kit

| | |
|---|---|
| [AGENTS.md](AGENTS.md) | The rules: read first. |
| [docs/THEME_KEYS.md](docs/THEME_KEYS.md) | Every key RIPPS2 adds (Grid, frosted glass, towers, tilt, transitions...). |
| [docs/THEME_ENGINE_RiptOPL.md](docs/THEME_ENGINE_RiptOPL.md) | The engine underneath (RiptOPL's reference). |
| `tools/check_theme.py` | Will it load? Numbering, types, missing files, misplaced keys. |
| `tools/preview_theme.py` | A PNG of the game list and info page, laid out as the engine does. |
| `tools/mirror_theme.py` | Draft the other-side layout of a theme. |
| `previews/` | The current previews. |

```
python3 tools/check_theme.py themes/*
python3 tools/preview_theme.py "themes/thm_Adapt" previews/thm_Adapt.png
python3 tools/mirror_theme.py "themes/thm_Adapt" "themes/thm_Adapt Rx" "Adapt Rx"
```
Python 3 and Pillow (`pip install pillow`) for the previewer.
