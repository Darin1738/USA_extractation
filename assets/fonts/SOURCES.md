# FONT SOURCES

All fonts are self-hosted in this folder and loaded locally by `fonts.css` / `caslon.css`. The board makes **no network font requests** at runtime.

**Licence:** all families are distributed under the **SIL Open Font License, Version 1.1**. The full licence text is in `OFL.txt` in this folder. The OFL allows free use, modification and embedding; if you redistribute the font files, keep the licence and copyright notices with them.

| File | Family / weight | Board use | Upstream |
|---|---|---|---|
| `Anton-400-normal.woff2` | Anton 400 | Panel titles, banner title, years, big numbers | Google Fonts — Anton, The Anton Project Authors |
| `LibreCaslonText-400-normal.woff2` | Libre Caslon Text 400 | Body/argument text | Google Fonts — Libre Caslon Text, The Libre Caslon Text Project Authors |
| `LibreCaslonText-400-italic.woff2` | Libre Caslon Text 400 italic | Pull quotes, emphasis | Google Fonts — same |
| `LibreCaslonText-700-normal.woff2` | Libre Caslon Text 700 | Panel titles/strong text | Google Fonts — same |
| `IBMPlexMono-400-normal.woff2` | IBM Plex Mono 400 | Metadata, labels, source lines | Google Fonts — IBM Plex Mono, IBM |
| `IBMPlexMono-600-normal.woff2` | IBM Plex Mono 600 | Labels, symbol keys | Google Fonts — same |
| `SpecialElite-400-normal.woff2` | Special Elite 400 | Archival captions, stamp/typewriter texture | Google Fonts — Special Elite, Astigmatic |
| `LibreBaskerville-400-normal.woff2` | Libre Baskerville 400 | **Bundled but unused** (legacy; body uses Libre Caslon) | Google Fonts — Libre Baskerville, Impallari Type |
| `LibreBaskerville-400-italic.woff2` | Libre Baskerville 400 italic | **Bundled but unused** | Google Fonts — same |
| `LibreBaskerville-700-normal.woff2` | Libre Baskerville 700 | **Bundled but unused** | Google Fonts — same |

## Notes on the font-loading fix (v1)

Earlier builds failed to load the display/mono faces because `fonts.css` pointed at `assets/assets/fonts/...` (a duplicated path), and the `@font-face` family names did not match the CSS variables (`IBM Plex Mono` vs `IBM Plex Mono`, `Special Elite` vs `Special Elite` after correction). The current files use relative filenames and the corrected family names. If you move the `assets/` folder, keep `fonts.css` and the `.woff2` files together, or update the `url(...)` paths.

## If you replace a font

1. Keep the OFL licence text or the new font's licence in this folder.
2. Update `fonts.css` / `caslon.css` and the `--font-*` variables in `board.css`.
3. Rebuild and check the banner title, P8 stat values, and footer — these are the tightest type fits.
