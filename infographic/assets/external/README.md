# EXTERNAL IMAGERY — POLICY AND SOURCES

**Current status: no external image files are used on this board.** All photographs come from the project's `../../../media/` folder and are logged in `../../MEDIA_MANIFEST.md`.

This folder exists so that any future outside image has an unambiguous home and a filename-keyed source record.

## Rules

1. **Save the file here**, using a descriptive lowercase filename (e.g. `tulsa_ruins_1921.jpg`). Do not hotlink.
2. **Add a row to `SOURCES.md`** for every file: filename, title/subject, author/photographer, repository/publisher, URL, licence or permission, access date, and any crop/tint/colour changes.
3. **State the licence.** Public domain, CC0, CC BY, or written permission only. If you cannot state it, do not use the image.
4. **No AI-generated depictions** of enslaved people, Black people, or racial violence. This follows the group's binder policy. Archival/documentary images only; label any reconstruction as an illustration.
5. **Do not add graphic lynching or whipping photographs.** The board deliberately omits them.
6. **Update the build** (`scripts/build_board.py`), the manifest, alt text and caption when an external image is added. Rebuild and re-check the panel geometry.

## Why the folder is separate

The project's historical photographs live in `media/` at the project root. Keeping a separate `assets/external/` folder makes it obvious which files came from outside that set and forces a source record for each one. The grader can inspect the folder and `SOURCES.md` together.

## Related records

- `../../MEDIA_MANIFEST.md` — all media used, including the project `media/` images.
- `../symbols/SOURCES.md` — original SVG symbols.
- `../fonts/SOURCES.md` — font licences.
- `../../VERIFY.md` — open source/rights checks.
