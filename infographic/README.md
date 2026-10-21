# Group 4 — *The Name Changes. The Function Does Not.*
**HIST 350 · Morgan State University · 24 × 36 in infographic + interactive board**

A ten-panel public infographic on the legacy of slavery in the American criminal justice system, with a Diaspora sidebar and a closing panel on resistance and memory.

> **Thesis:** Slavery was abolished, but the logic of controlling and extracting from Black bodies was rebuilt in new legal form.

**Historical question:** How and why did the American criminal justice system inherit and reproduce slavery's controlling and extractive functions after emancipation — and does the African Diaspora comparison show this as a U.S. pattern or a hemispheric one?

---

## What is in this folder

| Path | What it is |
|---|---|
| `index.html` | Interactive board (panel dossiers, symbol key, X-ray collage, hide-questions). Needs the sibling `../media/` folder. |
| `out/board_v2.png` | Static board, **2400 × 3600 px** (24 × 36 in at 100 ppi). Use this for review. |
| `out/board_v2@150.png` | High-res board, **3600 × 5400 px**. |
| `out/board_v2.pdf` | Vector PDF, **24 × 36 in**, full-resolution images (~38 MB). |
| `out/board_v2_print.pdf` | Print-optimised PDF, 300 ppi images (~21 MB). |
| `out/board_v2_thumb.png` | 600 × 900 preview. |
| `assets/board.css` | Design system: scrapbook collage, torn clipping cards, pan-African palette, print rules. |
| `assets/board.js` | Interactive layer (modals, symbol key, X-ray, hide-questions). |
| `assets/fonts/` | Local WOFF2 fonts + licences. |
| `assets/symbols/` | Eleven original SVG symbols (Pan-African / freedom / revolution / peace-war). |
| `assets/external/` | Reserved for any future **external** imagery, with its own source file. |
| `scripts/build_board.py` | Single source of truth for panel copy, positions, media, and render/QA. |
| `scripts/make_symbols.py` | Generates the ten SVG symbols. |
| `MEDIA_MANIFEST.md` | Every photograph used, with panel, caption, credit and verification status. |
| `BIBLIOGRAPHY.md` | Working bibliography keyed to the ten panels. |
| `VERIFY.md` | Claims that still need a source check before public presentation. |

---

## View and present

### Static (recommended for the projector)
1. Open `out/board_v2.png` or `out/board_v2_print.pdf`.
2. Present at **Actual size / 100%**; do **not** use “fit to page” or add margins.
3. The PDF is exactly **24 × 36 in**. The PNG is the same aspect at 100 ppi.

### Interactive
Open `index.html` in a modern browser. Keep this folder **inside the project root** so `../media/` resolves. The static PNG/PDF are self-contained and do not need the media folder.

- Click any panel or the banner → panel dossier (speaker notes, questions, sources, media).
- Click a numbered symbol tag (01–10) or an exposed background symbol → symbol dossier.
- **X-RAY THE COLLAGE** dims the panels and exposes the background collage — this is where the symbolism reads best.
- **HIDE QUESTIONS** removes the ASK lines for a Q&A-free display.
- `Esc` closes a dossier. Panels are keyboard-focusable (`Tab`, then `Enter`).
- On a laptop/projector the board fits the viewport width; the poster is tall, so scroll or use the PDF for a single-screen reveal.

---

## Design system (scrapbook v2)

- **Format:** portrait 24 × 36 in, two-column clipping grid, centre timeline spine.
- **Aesthetic:** aged-paper scrapbook. Full-bleed collage of torn paper, screen-printed photographs, washi tape, rubber stamps and hand-drawn symbols, with the panel copy on torn clipping cards layered on top at slight angles. Intentionally dense — almost no dead whitespace; the heavy subject reads as evidence piling up.
- **Palette:** pan-African — red `#c8102e`, black `#111010`, green `#0b6b3a`, gold `#c9a227` on aged paper creams `#e8dcc2`/`#d6c39a`. Red and green carry the resistance story; black is the substrate; gold is the through-line.
- **Typography:** Anton (display), Libre Caslon Text (body), IBM Plex Mono (metadata), Special Elite (archival captions). All fonts are local.
- **Structure:** banner/thesis → six eras (P2–P7) → algorithm (P8) → Diaspora sidebar (P9) → resistance/memory (P10) → footer.
- **Imagery:** archival/documentary only; graphic lynching photographs deliberately omitted.
- **Symbolism:** an original set built around Pan-Africanism, freedom, revolution/resistance and peace/war — see `assets/symbols/SOURCES.md`.
- **Images:** archival/ documentary only. Graphic lynching photographs are deliberately omitted; P6 uses a segregation sign and an EJI memorial marker instead.
- **Symbols:** ten original vector drawings (chains, cotton, ship, bars, ledger, eye, fingerprint, circuit, redaction, red thread). They are not stock or traced artwork.
- **Accessibility:** alt text on every image, captions on the board, high-contrast text, keyboard panel access, reduced-motion support, print files.

---

## Source and asset policy

- **Photographs** come from the group's `../media/` folder. Every used file is logged in **`MEDIA_MANIFEST.md`** with the exact filename, panel, caption, credit and status.
- **External imagery** (anything not already in `../media/`) must go in **`assets/external/`** and be added to **`assets/external/SOURCES.md`** as `filename → URL / author / licence / access date / modifications`. Do not hotlink.
- **Fonts** are from Google Fonts under the SIL Open Font License 1.1. See `assets/fonts/SOURCES.md`; the licence text is `assets/fonts/OFL.txt`.
- **Symbols** are original to this project. See `assets/symbols/SOURCES.md`.
- **No AI-generated imagery** is used. This follows the binder's rule against AI depictions of enslaved people or racial violence.

---

## Accuracy and disclosure — read before presenting

`VERIFY.md` lists the open checks. The most important:

1. **P4 “Black Codes” newspaper date.** The binder's LOC link points at a **1961** newspaper page, which cannot be the date of an 1865–66 Black Code. The board therefore says **“date under review”** and the citation says **“date to verify.”** Do not say 1961 as fact until the scan is checked.
2. **P7 Ehrlichman quote.** Widely cited, but its attribution is disputed. The board labels it *attributed/reported; attribution disputed*. Keep that hedge when speaking.
3. **P5 “~73% of Alabama revenue.”** An approximation; no exact figure survives. Cite the Alabama source you verified.
4. **Media rights.** `mlk_arrested.jpg` is credited **Charles Moore / Blackstar**; confirm classroom/public-use permission. The unused `protestors.jpg` is marked **© Corbis** and was removed from the board. Several other files have no credit in their metadata — see the manifest.
5. **AI use.** The footer discloses AI assistance for layout, typesetting, symbols and drafting. The group's binder says AI is not used for final historical prose; **rewrite/verify the final spoken and printed prose in your own voice** before submission, and adjust the footer if your policy requires different wording.

---

## Rebuild

The render pipeline needs Playwright + Chromium, Pillow and the local fonts. On this machine the working environment is `/tmp/opencode/venv`.

```bash
cd /home/abyss/Projects/School/History/new/infographic
/tmp/opencode/venv/bin/python scripts/build_board.py
```

That writes a fresh `index.html` plus the PNG, @150 PNG and PDF in `out/`. To regenerate only the HTML:

```bash
/tmp/opencode/venv/bin/python scripts/build_board.py --html-only
```

To regenerate the symbols:

```bash
/tmp/opencode/venv/bin/python scripts/make_symbols.py
```

To rebuild the print-optimised PDF:

```bash
gs -q -dNOPAUSE -dBATCH -sDEVICE=pdfwrite -dPDFSETTINGS=/prepress \
  -dCompatibilityLevel=1.4 -dDetectDuplicateImages=true \
  -dCompressFonts=true -dSubsetFonts=true \
  -sOutputFile=out/board_v2_print.pdf out/board_v2.pdf
```

---

## Version

**v2 — 21 Oct 2026.** Scrapbook redesign: full-bleed aged-paper collage, torn clipping cards, pan-African palette, new Pan-African/freedom/revolution/peace-war symbol set, and shorter punchier copy. Static PNG/PDF and interactive HTML rebuilt and QA-passed. Media credits and the open source checks in `VERIFY.md` still need the group's final pass.

*Superseded:* v1 (archive-noir grid) — kept only as prior art; the `out/board_v2.*` files are current.
