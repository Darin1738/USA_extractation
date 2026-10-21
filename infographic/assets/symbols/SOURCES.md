# SYMBOL SOURCES

All symbols in this folder are **original vector line drawings created for this project** by `scripts/make_symbols.py`. They are not traced from stock illustrations, photographs or another artist's work, and no external SVG was imported.

**v2 (scrapbook redesign)** rebuilds the set around the themes the group asked for: **Pan-Africanism, freedom in any form, revolution & resistance, and peace & war.** The earlier punitive/institutional icons (chains, ledger, bars, panopticon, etc.) were replaced.

| # | File | Symbol | Theme | Board meaning |
|---|---|---|---|---|
| 01 | `globe.svg` | Pan-African globe | Pan-Africanism | One people, scattered across the world — and still connected. Africa-centred, Diaspora routes crossing it. |
| 02 | `fist.svg` | Raised fist | Revolution & resistance | Refusal. The body that will not be owned. |
| 03 | `broken-chain.svg` | Broken chain | Freedom in any form | The link snapped: freedom seized, not granted. |
| 04 | `torch.svg` | Torch | Freedom & revolution | Light carried forward between generations. |
| 05 | `kente.svg` | Kente pattern | Pan-Africanism | African craft and identity that survived the crossing. |
| 06 | `dove.svg` | Dove | Peace | Peace — and the cost of the wars fought to reach it. |
| 07 | `megaphone.svg` | Megaphone | Protest & voice | Resistance organized out loud. |
| 08 | `barbed-wire.svg` | Barbed wire | War & oppression | Enclosure and confinement — the architecture of control. |
| 09 | `poppy.svg` | Poppy | Remembrance | Peace and remembrance for those the record tried to forget. |
| 10 | `open-hands.svg` | Open hands | Liberation | Freedom released, not hoarded. |
| —  | `thread.svg` | Red thread | Through-line | Profit → punishment → prediction; runs down the spine. |

**Licence:** original work, free to use in this project and its presentation. If the board is published or reused, credit **Group 4, HIST 350, Morgan State University**. Do not represent the symbols as stock or public-domain artwork from elsewhere.

**Technique:** each SVG uses `viewBox`, `fill="none"`, `stroke="currentColor"` and simple paths/ellipses so the board can tint it with CSS (red/green/gold), overlap it in the scrapbook collage, and expose it in X-ray mode. Line-based and resolution-independent.

**Regenerate:**

```bash
cd /home/abyss/Projects/School/History/new/infographic
/tmp/opencode/venv/bin/python scripts/make_symbols.py
```

`README.txt` in this folder is the quick list; this file is the source record.
