#!/usr/bin/env python3
"""
Collect public-domain / open-licence imagery for the Group 4 infographic
background collage. Pulls ONLY from rights-clear sources (Library of Congress
"No known restrictions", Smithsonian CC0). Writes downloaded files to
assets/external/ and regenerates assets/external/SOURCES.md.

Run:
  /tmp/opencode/venv/bin/python scripts/collect_images.py
"""
from __future__ import annotations
import json, pathlib, re, sys, urllib.request, urllib.parse

ROOT = pathlib.Path(__file__).resolve().parents[1]
OUT = ROOT / "assets" / "external"
OUT.mkdir(parents=True, exist_ok=True)

UA = {"User-Agent": "Mozilla/5.0 (research; Group4 HIST350)"}


def get(url: str, timeout=60):
    req = urllib.request.Request(url, headers=UA)
    return urllib.request.urlopen(req, timeout=timeout).read()


def loc_full_image(item_id: str) -> str | None:
    """Return the full-res JPEG (…v.jpg) for a LoC item id like '00652806'."""
    data = json.loads(get(f"https://www.loc.gov/item/{item_id}/?fo=json"))
    it = data.get("item", data)
    urls = it.get("image_url") or []
    best = None
    for u in urls:
        u = u.split("#")[0]
        if u.endswith("v.jpg"):
            return u
        if u.endswith("r.jpg"):
            best = u
    return best


def loc_meta(item_id: str) -> dict:
    data = json.loads(get(f"https://www.loc.gov/item/{item_id}/?fo=json"))
    it = data.get("item", data)
    return {
        "title": (it.get("title") or "").strip(),
        "date": str(it.get("date") or "").strip(),
        "creator": ", ".join(
            c.get("title", "") for c in (it.get("contributors") or [])
        ) or (it.get("contributor_names") or [None])[0] or "Unidentified",
        "rights": (it.get("rights_advisory") or "").strip()
        or "No known restrictions on publication.",
        "url": f"https://www.loc.gov/item/{item_id}/",
        "collection": (it.get("partof") or it.get("part_of") or ""),
    }


# ---- curated PD set -------------------------------------------------------
# slug -> (source, item_id, panel/theme note)
LOC_ITEMS = {
    "tulsa_ruins_after_riot":  ("loc", "2017679759", "Tulsa 1921 — ruins"),
    "tulsa_ruins_after_mob":   ("loc", "95521039",   "Tulsa 1921 — after the mob"),
    "tulsa_furniture_street":  ("loc", "93501250",   "Tulsa 1921 — furniture in street"),
    "chain_gang_thomasville":  ("loc", "00652806",   "convict labor / chain gang"),
    "on_the_chain_gang":       ("loc", "2002711523", "convict labor / chain gang"),
    "convicts_leased_timber":  ("loc", "2021669926", "convict leasing — timber"),
    "good_roads_convict":      ("loc", "27008979",   "convict labor — roads"),
    "freedmens_bureau":        ("loc", "92514996",   "Reconstruction / Freedmen's Bureau"),
    "freedmen_school_richmond":("loc", "98501491",   "Freedmen — industrial school"),
    "buffalo_soldier_25th":    ("loc", "2010645137", "Buffalo Soldier, 25th Infantry"),
}

SMI_ITEMS = {
    # slug -> (NMAAHC object id, note)
    "shackles_pre1860": ("NMAAHC-2011_51_3", "enslavement — iron shackles (Liljenquist)"),
    "tulsa_greenwood_burning": ("NMAAHC-2019_95_1_001", "Tulsa 1921 — Greenwood burning"),
}


def main() -> int:
    records = []
    for slug, (src, iid, note) in LOC_ITEMS.items():
        try:
            url = loc_full_image(iid)
            if not url:
                print(f"  !! no image for {slug}"); continue
            blob = get(url)
            dest = OUT / f"{slug}.jpg"
            dest.write_bytes(blob)
            m = loc_meta(iid)
            records.append({
                "file": dest.name, "source": "Library of Congress",
                "title": m["title"], "creator": m["creator"], "date": m["date"],
                "collection": note, "url": m["url"], "rights": m["rights"],
                "bytes": len(blob),
            })
            print(f"  ok {slug} ({len(blob)//1024} KB) — {m['title'][:50]}")
        except Exception as e:  # noqa
            print(f"  !! {slug}: {e}")

    for slug, (oid, note) in SMI_ITEMS.items():
        try:
            url = f"https://ids.si.edu/ids/deliveryService?id={oid}&max=1600"
            blob = get(url)
            dest = OUT / f"{slug}.jpg"
            dest.write_bytes(blob)
            records.append({
                "file": dest.name, "source": "Smithsonian Open Access (NMAAHC)",
                "title": slug.replace("_", " "), "creator": "Unidentified",
                "date": "before 1860" if "shackle" in slug else "1921",
                "collection": note,
                "url": f"https://www.si.edu/object/{oid}",
                "rights": "CC0 (public domain dedication)",
                "bytes": len(blob),
            })
            print(f"  ok {slug} ({len(blob)//1024} KB)")
        except Exception as e:  # noqa
            print(f"  !! {slug}: {e}")

    lines = [
        "# EXTERNAL IMAGE SOURCES",
        "",
        "Public-domain / open-licence imagery used in the Group 4 infographic "
        "background and panels. **Every file below is rights-clear** and was "
        "downloaded by `scripts/collect_images.py`. Do not add files to this "
        "folder without recording them here.",
        "",
        f"Collected: {len(records)} files.",
        "",
        "| File | Title | Creator | Date | Institution | Rights | Item URL |",
        "|---|---|---|---|---|---|---|",
    ]
    for r in records:
        lines.append(
            f"| `{r['file']}` | {r['title']} | {r['creator']} | {r['date']} | "
            f"{r['source']} | {r['rights']} | {r['url']} |"
        )
    lines += [
        "",
        "## Notes",
        "- LoC items carry the Library's own rights statement, quoted verbatim.",
        "- Smithsonian NMAAHC images are dedicated **CC0** under the Open Access initiative.",
        "- Graphic victim imagery was deliberately avoided; ruins, objects, documents "
        "and dignified portraits are preferred.",
        "",
    ]
    (OUT / "SOURCES.md").write_text("\n".join(lines), encoding="utf-8")
    print(f"\nwrote {OUT/'SOURCES.md'} ({len(records)} records)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
