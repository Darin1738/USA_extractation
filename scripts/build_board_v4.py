#!/usr/bin/env python3
"""
Group 4 · HIST 350 · The Name Changes / The Function Does Not
v4 builder — FLYER LAYOUTS over a STITCHED PATCHWORK of media.

Why v4 exists
-------------
v3 shipped one geometry (`panel_positions()` was identical for a/b/c) and only
swapped colour filters. v4 decouples the two axes:

    LAYOUT  = broadside | quilt | zine        (this file)
    COLOUR  = variant A — colour collage       (board_v4.css)

The background is no longer a random confetti montage. It is a sewn quilt:
irregular media patches laid edge to edge, dark seams, running stitches,
blanket-stitch ticks, cross-stitches at the joins, and a literal red thread
that laces the whole board together. The red thread is also the board's
argument: one continuous line from 1619 to the algorithm.

Variants:
  broadside = asymmetric protest flyer, one hero panel, big masthead
  quilt     = panels as stitched-in blocks on an explicit patchwork
  zine      = newsprint leaflet: left rail, three columns, wide close

Run:
  /tmp/opencode/venv/bin/python scripts/build_board_v4.py
  /tmp/opencode/venv/bin/python scripts/build_board_v4.py --layout broadside
  /tmp/opencode/venv/bin/python scripts/build_board_v4.py --layout quilt --no-pdf
"""
from __future__ import annotations

import argparse
import html
import json
import random
import sys
from pathlib import Path
from urllib.parse import quote as urlquote

ROOT = Path(__file__).resolve().parent.parent
SYM = ROOT / "assets" / "symbols"
EXT = ROOT / "assets" / "external"
OUT = ROOT / "out"
OUT.mkdir(exist_ok=True)
sys.path.insert(0, str(ROOT / "scripts"))

import build_board as C  # noqa: E402  (content source of truth)

P = C.P
SYMBOLS = C.SYMBOLS

W, H = 1800, 2400
M = 44


# ==========================================================================
# media pool for the patchwork (all archival / documentary, no AI imagery)
# ==========================================================================
MEDIA_FILES = [
    "slave_atlantic_trade_slave_ship.jpg",
    "emancipation_proclamation.jpg",
    "african_american_convicts_w_shovels.jpg",
    "ChatahoocheebricksEnglishWeb-768x576.jpg",
    "moneyreward.jpg",
    "one_vote_less.jpg",
    "imagery.jpg",
    "fountain_seg.jpg",
    "letohatchee.jpg",
    "mlk_arrested.jpg",
    "prsion_blck_vs_white.png",
    "risk_score_p1_1.png",
    "risk_score_p1_2.png",
    "escaped_enslaved_people_from_plantation_virgiana.jpg",
    "angola_prison_guard_tower.png",
    "afroargentines_playing_candombe_porteno_near_bonfire_of_sain_john.jpg",
    "Slave Voyages Map.png",
    "Slave Voyages Pie Chart.png",
    "inarcerated_laborers_from-louisiana-state-penitentiary-angola.png",
    "south_carolina_first_slave_law.jpg",
]

EXT_FILES = [
    "chain_gang_thomasville.jpg",
    "freedmen_bureau.jpg",
    "freedmen_school_richmond.jpg",
    "shackles_pre1860.jpg",
    "buffalo_soldier_25th.jpg",
    "tulsa_ruins_after_riot.jpg",
    "tulsa_furniture_street.jpg",
    "tulsa_greenwood_burning.jpg",
    "on_the_chain_gang.jpg",
    "tulsa_ruins_after_mob.jpg",
]


def med_src(fname: str) -> str:
    return "../media/" + urlquote(fname)


def ext_src(fname: str) -> str:
    return "assets/external/" + urlquote(fname)


def media_pool() -> list[str]:
    pool = [med_src(f) for f in MEDIA_FILES if (ROOT.parent / "media" / f).exists()]
    pool += [ext_src(f) for f in EXT_FILES if (EXT / f).exists()]
    return pool


# ==========================================================================
# LAYOUTS  (x, y, w, h)
# ==========================================================================
LAYOUTS = {
    "broadside": dict(
        banner=(44, 44, 1712, 392),
        panels={
            "p2": (44, 452, 980, 620),      # hero
            "p3": (1052, 452, 704, 300),
            "p4": (1052, 768, 704, 304),
            "p5": (44, 1088, 556, 420),
            "p6": (624, 1088, 556, 420),
            "p7": (1204, 1088, 552, 420),
            "p8": (44, 1522, 884, 416),
            "p9": (952, 1522, 804, 416),
            "p10": (44, 1952, 1712, 376),
        },
        legend=(44, 2338, 1712, 30),
        footer=2372,
        rot={},
    ),
    "quilt": dict(
        banner=(44, 44, 1712, 392),
        panels={
            "p2": (44, 452, 846, 560),
            "p3": (910, 452, 413, 272),
            "p4": (1343, 452, 413, 272),
            "p5": (910, 738, 413, 274),
            "p6": (1343, 738, 413, 274),
            "p7": (44, 1026, 846, 440),
            "p8": (910, 1026, 413, 440),
            "p9": (1343, 1026, 413, 440),
            "p10": (44, 1480, 1712, 852),
        },
        legend=(44, 2338, 1712, 30),
        footer=2372,
        rot={"p2": -0.5, "p3": 0.8, "p4": -0.8, "p5": 0.6, "p6": -0.6,
             "p7": 0.35, "p8": -0.5, "p9": 0.7, "p10": -0.25},
    ),
    "zine": dict(
        banner=(44, 36, 1712, 392),
        rail=(44, 448, 340, 1872),
        panels={
            "p2": (424, 448, 432, 520),
            "p3": (872, 448, 432, 430),
            "p4": (1320, 448, 436, 640),
            "p5": (872, 894, 432, 470),
            "p6": (424, 984, 432, 390),
            "p7": (1320, 1104, 436, 904),
            "p8": (424, 1390, 432, 618),
            "p9": (872, 1380, 432, 628),
            "p10": (424, 1936, 1332, 404),
        },
        legend=(44, 2350, 1712, 24),
        footer=2378,
        rot={},
    ),
    # v1 — the original: near-black bed, four rows of cream cards, sparse colour.
    # Geometry adapted from board_v1.png (2400x3600) scaled to 1800x2400.
    "v1": dict(
        banner=(44, 44, 1712, 372),
        panels={
            "p2": (44, 436, 842, 386),
            "p3": (914, 436, 842, 386),
            "p4": (44, 832, 842, 386),
            "p5": (914, 832, 842, 386),
            "p6": (44, 1228, 842, 386),
            "p7": (914, 1228, 842, 386),
            "p8": (44, 1624, 842, 386),
            "p9": (914, 1624, 842, 386),
            "p10": (44, 2020, 1712, 250),
        },
        legend=(44, 2276, 1712, 24),
        footer=2298,
        rot={},
    ),
}


# ==========================================================================
# PATCHWORK + STITCHING
# ==========================================================================
def _seam_columns(rng: random.Random) -> list[tuple[int, int, list[int]]]:
    """Column boundaries plus the horizontal cuts inside each column."""
    base = [0, 300, 610, 900, 1190, 1500, 1800]
    xs = [base[0]] + [b + rng.randint(-34, 34) for b in base[1:-1]] + [base[-1]]
    cols = []
    for i in range(len(xs) - 1):
        y = -24
        cuts = []
        while y < H + 24:
            y = min(H + 24, y + rng.randint(205, 385))
            cuts.append(y)
        cols.append((xs[i], xs[i + 1], cuts))
    return cols


def _line(x1: float, y1: float, x2: float, y2: float) -> str:
    return f"M{x1:.0f} {y1:.0f}L{x2:.0f} {y2:.0f}"


def _thread(x0: int, rng: random.Random) -> tuple[str, list[tuple[int, int]]]:
    pts = [(x0, -60)]
    y = -60
    while y < H + 60:
        y += rng.randint(280, 520)
        pts.append((rng.randint(80, W - 80), y))
    d = f"M{pts[0][0]} {pts[0][1]}"
    for (xa, ya), (xb, yb) in zip(pts, pts[1:]):
        c1x = xa + rng.randint(-190, 190)
        c1y = ya + (yb - ya) * 0.38
        c2x = xb + rng.randint(-190, 190)
        c2y = ya + (yb - ya) * 0.72
        d += f"C{c1x:.0f} {c1y:.0f} {c2x:.0f} {c2y:.0f} {xb} {yb}"
    return d, pts


APPLIQUES = [
    ("globe", 105, 258, 250, -7, "gold"),
    ("fist", 1470, 586, 230, 6, "red"),
    ("broken-chain", 90, 1660, 270, -5, "green"),
    ("kente", 1480, 1430, 250, 4, "gold"),
    ("megaphone", 690, 2190, 230, -6, "red"),
]


def build_quilt(seed: int) -> dict:
    rng = random.Random(seed)
    cols = _seam_columns(rng)
    photos = media_pool()
    if not photos:
        photos = ["assets/external/freedmen_bureau.jpg"]
    rng.shuffle(photos)
    tones = ["red", "green", "gold", "ink", "ink", "ink"]

    patches: list[dict] = []
    n = 0
    for x0, x1, cuts in cols:
        y0 = -24
        for y1 in cuts:
            # every ninth patch is a cloth swatch instead of a photograph
            if n % 9 == 4:
                patches.append(dict(kind="swatch", x=x0, y=y0, w=x1 - x0, h=y1 - y0,
                                    tone=rng.choice(["red", "green", "gold"])))
            else:
                patches.append(dict(kind="photo", x=x0, y=y0, w=x1 - x0, h=y1 - y0,
                                    src=photos[n % len(photos)],
                                    tone=rng.choice(tones)))
            n += 1
            y0 = y1

    # seams: vertical runs + horizontal runs per column
    v_runs, h_runs, ticks, crosses = [], [], [], []
    for x, _, _ in cols[1:-1]:
        v_runs.append(_line(x, 0, x, H))
        y = 8
        while y < H:
            ticks.append(_line(x - 9, y, x + 9, y))
            y += 30
    for x0, x1, cuts in cols:
        for y in cuts:
            if y < 0 or y > H:
                continue
            h_runs.append(_line(x0, y, x1, y))
            x = x0 + 10
            while x < x1 - 10:
                ticks.append(_line(x, y - 9, x, y + 9))
                x += 32
            # cross-stitch where the horizontal seam meets a vertical seam
            for vb in [c[0] for c in cols[1:-1]]:
                if x0 < vb < x1:
                    crosses.append(f"M{vb-7} {y-7}L{vb+7} {y+7}")
                    crosses.append(f"M{vb-7} {y+7}L{vb+7} {y-7}")

    thread_a, pts_a = _thread(420, rng)
    thread_b, pts_b = _thread(1320, rng)
    knots = [f'<circle class="knot" cx="{x}" cy="{y}" r="5"/>' for x, y in pts_a[1:-1]]
    knots += [f'<circle class="knot gold" cx="{x}" cy="{y}" r="4"/>' for x, y in pts_b[1:-1]]

    swatches = []
    for key, x, y, s, rot, tone in APPLIQUES:
        svg = (SYM / f"{key}.svg").read_text()
        swatches.append(
            f'<div class="applique t-{tone}" data-sym="{key}" '
            f'style="left:{x}px;top:{y}px;width:{s}px;height:{s}px;'
            f'transform:rotate({rot}deg)">{svg}</div>'
        )

    # a few tapes bridging seams, deterministic
    tapes = []
    for x, y, rot in [(300, 640, 12), (610, 1280, -14), (900, 1820, 9),
                      (1190, 560, -11), (1500, 1540, 13), (610, 2140, -8)]:
        tapes.append(f'<div class="quilt-tape" style="left:{x-70}px;top:{y-15}px;'
                     f'transform:rotate({rot}deg)"></div>')

    return dict(patches=patches, v_runs="".join(v_runs), h_runs="".join(h_runs),
                ticks="".join(ticks), crosses="".join(crosses),
                thread_a=thread_a, thread_b=thread_b, knots="".join(knots),
                swatches="".join(swatches), tapes="".join(tapes))


def quilt_html(seed: int, layout: str = "quilt") -> str:
    q = build_quilt(seed)
    out = ['<div class="quilt" aria-hidden="true">']
    if layout == "v1":
        # v1 keeps the media patches but drops the busy stitches/threads:
        # a quiet dark bed so the cream cards carry the board.
        for p in q["patches"]:
            x, y, w, h = p["x"], p["y"], p["w"], p["h"]
            kind = "photo" if p["kind"] == "photo" else "swatch"
            extra = f'background-image:url(\'{p["src"]}\')' if kind == "photo" else ""
            out.append(
                f'<div class="patch {"" if kind == "photo" else "swatch "}t-{p["tone"]}" '
                f'style="left:{x + 3}px;top:{y + 3}px;width:{max(1, w - 6)}px;'
                f'height:{max(1, h - 6)}px;{extra}"></div>'
            )
        out.append("</div>")
        return "".join(out)
    for p in q["patches"]:
        x, y, w, h = p["x"], p["y"], p["w"], p["h"]
        if p["kind"] == "photo":
            out.append(
                f'<div class="patch t-{p["tone"]}" style="left:{x + 3}px;top:{y + 3}px;'
                f'width:{max(1, w - 6)}px;height:{max(1, h - 6)}px;'
                f'background-image:url(\'{p["src"]}\')"></div>'
            )
        else:
            out.append(
                f'<div class="patch swatch t-{p["tone"]}" style="left:{x + 3}px;'
                f'top:{y + 3}px;width:{max(1, w - 6)}px;height:{max(1, h - 6)}px"></div>'
            )
    out.append(
        '<svg class="stitching" viewBox="0 0 1800 2400" preserveAspectRatio="none">'
        f'<path class="run" d="{q["v_runs"]}{q["h_runs"]}"/>'
        f'<path class="tick" d="{q["ticks"]}"/>'
        f'<path class="cross" d="{q["crosses"]}"/>'
        f'<path class="thread" d="{q["thread_a"]}"/>'
        f'<path class="thread gold" d="{q["thread_b"]}"/>'
        f'{q["knots"]}'
        "</svg>"
    )
    out.append(q["swatches"])
    out.append(q["tapes"])
    out.append("</div>")
    return "".join(out)


# ==========================================================================
# MARKUP
# ==========================================================================
def esc(s: str) -> str:
    return html.escape(s, quote=True)


def size_class(w: int, h: int) -> str:
    if w >= 840:
        return "lg"
    if w >= 660:
        return "md"
    return "sm"


def banner_html(layout: str) -> str:
    x, y, w, h = LAYOUTS[layout]["banner"]
    return f"""
<section class="banner lay-{layout}" data-panel="p1" tabindex="0" role="button"
  aria-label="Open the thesis banner"
  style="left:{x}px;top:{y}px;width:{w}px;height:{h}px">
  <div class="mast-top">
    <div class="kicker"><span class="dot"></span>HIST 350 · GROUP 4 · MORGAN STATE UNIVERSITY</div>
    <div class="filetag">CASE FILE <b>01</b>/10 · 1619 → PRESENT</div>
  </div>
  <div class="mast-grid">
    <h1 class="b-title"><span>THE NAME CHANGES.</span><span>THE <em>FUNCTION</em> DOES NOT.</span></h1>
    <div class="mast-side">
      <p class="thesis">“Slavery was abolished, but the logic of <b>controlling and extracting</b> from Black bodies was rebuilt in new legal form.”</p>
      <div class="case">
        <div class="label">Opening question / why this board</div>
        <p class="q">If slavery was abolished in 1865, <em>why did prisons become overrun with Black bodies?</em></p>
      </div>
    </div>
  </div>
  <div class="era-strip">
    <span class="e"><b>1619</b> SLAVERY</span><span class="dash"></span>
    <span class="e"><b>1865</b> 13TH</span><span class="dash"></span>
    <span class="e"><b>1865–66</b> BLACK CODES</span><span class="dash"></span>
    <span class="e"><b>1868</b> CONVICT LEASING</span><span class="dash"></span>
    <span class="e"><b>1890s</b> JIM CROW</span><span class="dash"></span>
    <span class="e"><b>1971</b> MASS INCARCERATION</span><span class="dash"></span>
    <span class="e"><b>2000s</b> ALGORITHM</span>
  </div>
  <div class="mast-badge"><span>SIX AREAS</span><b>ONE FUNCTION</b></div>
</section>"""


def panel_html(p: dict, layout: str) -> str:
    x, y, w, h = LAYOUTS[layout]["panels"][p["id"]]
    rot = LAYOUTS[layout]["rot"].get(p["id"], 0)
    size = size_class(w, h)
    style = (f"left:{x}px;top:{y}px;width:{w}px;height:{h}px;"
             f"--rot:{rot}deg;")
    z = 5 + (1 if p["id"] in ("p2", "p7", "p10") else 0)
    style += f"z-index:{z};"
    return f"""
<article class="panel p-{size} lay-{layout}" data-panel="{p['id']}" data-size="{size}"
  tabindex="0" role="button" aria-label="Open panel {p['num']}: {esc(p['title'])}"
  style="{style}">
  <span class="tape tl"></span><span class="tape br"></span>
  <span class="pin a"></span><span class="pin b"></span>
  <header class="p-head">
    <div class="era">{p['era']}</div>
    <div class="pnum"><b>{p['num']}</b><span>/ 10</span></div>
  </header>
  <div class="p-main">
    <h2 class="p-title">{p['title']}</h2>
    <p class="p-arg">{p['arg']}</p>
    <p class="p-facts">{p['facts']}</p>
    {C.statblock(p)}
  </div>
  <div class="p-media">{''.join(C.figure(im) for im in p['images'])}</div>
  <div class="p-foot">
    <p class="ask"><span class="asktag">ASK</span>{esc(p['question'])}</p>
    <p class="src">SRC · {esc(p['source'])}</p>
  </div>
</article>"""


def p10_html(layout: str) -> str:
    p = P["p10"]
    x, y, w, h = LAYOUTS[layout]["panels"]["p10"]
    rot = LAYOUTS[layout]["rot"].get("p10", 0)
    size = "xl" if layout != "zine" else "wide"
    res = "".join(
        f'<div class="res-item"><div class="y">{yy}</div><div class="t">{t}</div><div class="d">{d}</div></div>'
        for yy, t, d in p["resistance"])
    mem = "".join(
        f'<div class="mem-item"><div class="y">{yy}</div><div class="t">{t}</div><div class="d">{d}</div></div>'
        for yy, t, d in p["memory"])
    media = "".join(C.figure(im) for im in p["images"])
    return f"""
<article class="panel p10 p-{size} lay-{layout}" data-panel="p10" data-size="{size}"
  tabindex="0" role="button" aria-label="Open panel 10: resistance and memory"
  style="left:{x}px;top:{y}px;width:{w}px;height:{h}px;--rot:{rot}deg;z-index:6;">
  <span class="tape tl"></span><span class="tape br"></span>
  <span class="pin a"></span><span class="pin b"></span>
  <header class="p-head">
    <div class="era">{p['era']}</div>
    <div class="pnum"><b>{p['num']}</b><span>/ 10</span></div>
  </header>
  <div class="w-body">
    <div class="w-left">
      <h2 class="p-title">{p['title']}</h2>
      <p class="p-arg">{p['arg']}</p>
      <div class="p10-media">{media}</div>
      <div class="w-close">
        <div class="closing">THE NAME CHANGES. <span>THE FUNCTION DOES NOT.</span></div>
        <p class="ask"><span class="asktag">ASK</span>{esc(p['question'])}</p>
        <p class="src">SRC · {esc(p['source'])}</p>
      </div>
    </div>
    <div class="res">
      <div class="res-block"><h3>Resistance</h3><div class="res-grid">{res}</div></div>
      <div class="mem-block"><h3>Memory / erasure</h3><div class="mem-grid">{mem}</div></div>
    </div>
  </div>
</article>"""


def rail_html(layout: str) -> str:
    """Zine-only left rail: thesis, timeline, symbol key."""
    if layout != "zine":
        return ""
    x, y, w, h = LAYOUTS[layout]["rail"]
    years = [("1619", "CHATTEL SLAVERY"), ("1865", "13TH AMENDMENT"),
             ("1865–66", "BLACK CODES"), ("1868", "CONVICT LEASING"),
             ("1890s", "JIM CROW"), ("1971", "WAR ON DRUGS"),
             ("2000s", "ALGORITHM")]
    tl = "".join(f'<li><b>{a}</b><span>{b}</span></li>' for a, b in years)
    return f"""
<aside class="zrail" style="left:{x}px;top:{y}px;width:{w}px;height:{h}px">
  <div class="zr-kicker">THE THROUGH-LINE</div>
  <p class="zr-thesis">Profit from Black bodies moved from the plantation, to the prison, to the platform.</p>
  <div class="zr-rule"></div>
  <div class="zr-kicker">TIMELINE</div>
  <ol class="zr-tl">{tl}</ol>
  <div class="zr-rule"></div>
  <div class="zr-kicker">THREE PILLARS</div>
  <ol class="zr-pillars">
    <li><b>I</b> PROFIT FROM BLACK BODIES</li>
    <li><b>II</b> CONVICT LEASING → PRISON LABOR</li>
    <li><b>III</b> PLANTATION → ALGORITHM</li>
  </ol>
  <div class="zr-rule"></div>
  <p class="zr-foot">SOURCES ON EVERY PANEL.<br>SEE BIBLIOGRAPHY &amp; VERIFICATION LOG.</p>
</aside>"""


def legend_html(layout: str) -> str:
    x, y, w, h = LAYOUTS[layout]["legend"]
    short = {
        "globe": "GLOBE", "fist": "FIST", "broken-chain": "CHAIN", "torch": "TORCH",
        "kente": "KENTE", "dove": "DOVE", "megaphone": "VOICE", "barbed-wire": "WIRE",
        "poppy": "POPPY", "open-hands": "HANDS",
    }
    items = "".join(
        f'<button class="symkey" type="button" data-symkey="{k}" title="{esc(SYMBOLS[k]["name"])}">'
        f'<b>{SYMBOLS[k]["num"]}</b>{short[k]}</button>'
        for k in short
    )
    return (f'<div class="legend" style="left:{x}px;top:{y}px;width:{w}px;height:{h}px">'
            f'<span class="legend-lbl">SYMBOL KEY</span>{items}'
            f'<span class="legend-note">CLICK ANY SYMBOL OR PANEL TO OPEN THE FILE</span></div>')


def footer_html(layout: str) -> str:
    y = LAYOUTS[layout]["footer"]
    return f"""
<div class="footer" style="left:{M}px;top:{y}px;width:{W - 2 * M}px">
  <div><b>GROUP 4</b> · DARIN L. WESLEY (LEADER) · COURTNEY FOWLKES (ASST.) · KIARRA M · ANTWAN POWELL · DEJUAN G · MAKAYLA PARSI · TAJA BRIDGES</div>
  <div class="r">SOURCES ON EACH PANEL · BIBLIOGRAPHY, MEDIA MANIFEST &amp; VERIFICATION LOG: GROUP 4 BINDER · AI USE: LAYOUT, TYPESETTING, SYMBOLS &amp; DRAFT ASSISTANCE; RESEARCH &amp; SOURCE CHECKS: GROUP 4</div>
</div>"""


def page_name(layout: str) -> str:
    return f"board_{layout}.html"


def board_sections(layout: str) -> str:
    """The positioned children of the stage for one layout (no wrapper)."""
    panel_ids = ("p2", "p3", "p4", "p5", "p6", "p7", "p8", "p9")
    for pid in panel_ids + ("p10",):
        P[pid]["id"] = pid
    seed = {"broadside": 4410, "quilt": 7721, "zine": 9913, "v1": 5504}[layout]
    return (quilt_html(seed, layout) + banner_html(layout) +
            "".join(panel_html(P[k], layout) for k in panel_ids) +
            p10_html(layout) + rail_html(layout) +
            legend_html(layout) + footer_html(layout))


def board_json(layout: str) -> dict:
    return {
        "variant": "a",
        "layout": layout,
        "panels": {pid: {k: v for k, v in P[pid].items() if k in
                         ("num", "tag", "era", "title", "arg", "facts", "stat", "stats",
                          "quote", "images", "question", "source", "notes", "questions",
                          "sources", "note")} for pid in P},
        "symbols": SYMBOLS,
    }


def build_html(layout: str) -> str:
    panel_ids = ("p2", "p3", "p4", "p5", "p6", "p7", "p8", "p9")
    for pid in panel_ids + ("p10",):
        P[pid]["id"] = pid

    board_json = {
        "variant": "a",
        "layout": layout,
        "panels": {pid: {k: v for k, v in P[pid].items() if k in
                         ("num", "tag", "era", "title", "arg", "facts", "stat", "stats",
                          "quote", "images", "question", "source", "notes", "questions",
                          "sources", "note")} for pid in P},
        "symbols": SYMBOLS,
    }
    seed = {"broadside": 4410, "quilt": 7721, "zine": 9913, "v1": 5504}[layout]
    doc = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Group 4 · The Name Changes — {layout}</title>
<link rel="stylesheet" href="assets/fonts/fonts.css">
<link rel="stylesheet" href="assets/fonts/caslon.css">
<link rel="stylesheet" href="assets/board.css">
<link rel="stylesheet" href="assets/board_v4.css">
</head>
<body data-variant="a" data-layout="{layout}">
<div class="holder"><div class="stage" id="stage">
  {quilt_html(seed, layout)}
  {banner_html(layout)}
  {''.join(panel_html(P[k], layout) for k in panel_ids)}
  {p10_html(layout)}
  {rail_html(layout)}
  {legend_html(layout)}
  {footer_html(layout)}
</div></div>

<dialog id="modal" aria-label="Panel detail">
  <div id="modal-head" class="m-head"></div>
  <div id="modal-body" class="m-body"></div>
</dialog>

<div class="toolbar" role="toolbar" aria-label="Board controls">
  <div class="brand"><b>GROUP 4</b> · THE NAME CHANGES · {layout.upper()}</div>
  <div class="lay-switch" role="group" aria-label="Switch layout">
    <a class="lay-btn{' on' if layout == 'v1' else ''}" href="board_v1.html">V1</a>
    <a class="lay-btn{' on' if layout == 'quilt' else ''}" href="board_quilt.html">QUILT</a>
    <a class="lay-btn{' on' if layout == 'zine' else ''}" href="board_zine.html">ZINE</a>
    <a class="lay-btn{' on' if layout == 'broadside' else ''}" href="board_broadside.html">BROADSIDE</a>
  </div>
  <button id="xray" type="button">X-RAY THE COLLAGE</button>
  <button id="qtoggle" type="button">HIDE QUESTIONS</button>
  <a class="lay-btn home" href="index.html">ALL LAYOUTS</a>
</div>

<script>window.BOARD = {json.dumps(board_json, ensure_ascii=False)};</script>
<script src="assets/board.js"></script>
</body>
</html>
"""
    return doc


def build_combined_html(default_layout: str = "quilt") -> str:
    """One document containing all four layouts; switch in-page, no reloads."""
    order = ["v1", "quilt", "zine", "broadside"]
    sets = "".join(
        f'<div class="layout-set" data-set="{lay}">{board_sections(lay)}</div>'
        for lay in order
    )
    boards = {lay: board_json(lay) for lay in order}
    switch = "".join(
        f'<button class="lay-btn" type="button" data-goto="{lay}">{lay.upper()}</button>'
        for lay in order
    )
    doc = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Group 4 · The Name Changes / The Function Does Not</title>
<link rel="stylesheet" href="assets/fonts/fonts.css">
<link rel="stylesheet" href="assets/fonts/caslon.css">
<link rel="stylesheet" href="assets/board.css">
<link rel="stylesheet" href="assets/board_v4.css">
</head>
<body data-variant="a" data-layout="{default_layout}">
<div class="holder"><div class="stage" id="stage">
  {sets}
</div></div>

<dialog id="modal" aria-label="Panel detail">
  <div id="modal-head" class="m-head"></div>
  <div id="modal-body" class="m-body"></div>
</dialog>

<div class="toolbar" role="toolbar" aria-label="Board controls">
  <div class="brand"><b>GROUP 4</b> · THE NAME CHANGES</div>
  <div class="lay-switch" role="group" aria-label="Switch layout">{switch}</div>
  <button id="xray" type="button">X-RAY THE COLLAGE</button>
  <button id="qtoggle" type="button">HIDE QUESTIONS</button>
</div>

<script>window.BOARDS = {json.dumps(boards, ensure_ascii=False)};
window.BOARD = window.BOARDS[{json.dumps(default_layout)}];</script>
<script src="assets/board.js"></script>
<script>
(function(){{
  var btns = document.querySelectorAll('.lay-btn[data-goto]');
  function apply(lay){{
    document.body.setAttribute('data-layout', lay);
    window.BOARD = window.BOARDS[lay];
    btns.forEach(function(b){{ b.classList.toggle('on', b.getAttribute('data-goto') === lay); }});
  }}
  btns.forEach(function(b){{ b.addEventListener('click', function(){{ apply(b.getAttribute('data-goto')); }}); }});
  apply({json.dumps(default_layout)});
}})();
</script>
</body>
</html>
"""
    return doc


# ==========================================================================
# RENDER + QA
# ==========================================================================
def render(layout: str, html_only: bool = False, pdf: bool = True) -> None:
    idx = ROOT / page_name(layout)
    idx.write_text(build_html(layout), encoding="utf-8")
    print(f"[{layout}] wrote {idx}")
    if html_only:
        return

    from playwright.sync_api import sync_playwright

    url = idx.as_uri()
    stem = f"board_v4_{layout}"
    with sync_playwright() as pw:
        browser = pw.chromium.launch()
        page = browser.new_page(viewport={"width": W, "height": H}, device_scale_factor=1)
        page.goto(url, wait_until="load")
        page.wait_for_function("document.fonts && document.fonts.status === 'loaded'")
        page.wait_for_function("Array.from(document.images).every(i => i.complete)")
        page.evaluate("document.body.classList.add('static'); document.documentElement.style.setProperty('--fit','1')")
        page.wait_for_timeout(500)

        qa = page.evaluate("""() => {
          const panels = [...document.querySelectorAll('.panel, .banner')].map(el => {
            const r = el.getBoundingClientRect();
            const out = [];
            for (const k of el.querySelectorAll('*')) {
              if (k.classList && (k.classList.contains('tape') || k.classList.contains('pin') ||
                  k.classList.contains('quilt-tape') || k.classList.contains('stamp'))) continue;
              const kr = k.getBoundingClientRect();
              // 26px tolerance covers the small panel rotation in the quilt layout
              if (kr.width > 0 && kr.height > 0 && (kr.right > r.right + 26 ||
                  kr.bottom > r.bottom + 26 || kr.left < r.left - 26 || kr.top < r.top - 26)) {
                out.push((k.className && String(k.className).slice(0,40)) || k.tagName);
              }
            }
            return {id: el.dataset.panel || el.className,
                    w: Math.round(r.width), h: Math.round(r.height),
                    scrollOverflow: el.scrollHeight - el.clientHeight,
                    out: [...new Set(out)].slice(0, 6)};
          });
          const images = [...document.images].map(i => ({src: i.getAttribute('src'),
            ok: i.complete && i.naturalWidth > 0}));
          const stage = document.getElementById('stage');
          return {panels, badImages: images.filter(i=>!i.ok).slice(0,8),
                  fonts: document.fonts.status, stage: [stage.scrollWidth, stage.scrollHeight],
                  dialog: document.querySelector('dialog') ? 'ok' : 'missing'};
        }""")
        print(f"[{layout}] QA", json.dumps(qa, ensure_ascii=False)[:2600])

        page.locator("#stage").screenshot(path=str(OUT / f"{stem}.png"))
        print(f"[{layout}] wrote {stem}.png")

        hi = browser.new_page(viewport={"width": W, "height": H}, device_scale_factor=1.5)
        hi.goto(url, wait_until="load")
        hi.wait_for_function("document.fonts && document.fonts.status === 'loaded'")
        hi.wait_for_function("Array.from(document.images).every(i => i.complete)")
        hi.evaluate("document.body.classList.add('static'); document.documentElement.style.setProperty('--fit','1')")
        hi.wait_for_timeout(400)
        hi.locator("#stage").screenshot(path=str(OUT / f"{stem}@150.png"))
        print(f"[{layout}] wrote {stem}@150.png")

        if pdf:
            page.pdf(path=str(OUT / f"{stem}.pdf"), width="18in", height="24in",
                     margin={"top": "0", "bottom": "0", "left": "0", "right": "0"},
                     print_background=True, prefer_css_page_size=True)
            print(f"[{layout}] wrote {stem}.pdf")
        browser.close()


CHOOSER = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Group 4 · The Name Changes — choose a layout</title>
<link rel="stylesheet" href="assets/fonts/fonts.css">
<link rel="stylesheet" href="assets/fonts/caslon.css">
<link rel="stylesheet" href="assets/board.css">
<link rel="stylesheet" href="assets/board_v4.css">
<style>
  .chooser{{max-width:1100px;margin:48px auto;padding:0 28px;color:#f2e8ce;
    font-family:'IBM Plex Mono',monospace;}}
  .chooser h1{{font-family:'Anton',Impact,sans-serif;font-size:56px;line-height:.95;
    text-transform:uppercase;margin:0 0 6px;}}
  .chooser h1 em{{color:#e6bb3a;font-style:normal;}}
  .chooser p{{color:#c9bda1;max-width:70ch;line-height:1.5;}}
  .cards{{display:grid;grid-template-columns:repeat(auto-fit,minmax(230px,1fr));gap:18px;margin:30px 0;}}
  .card{{display:block;text-decoration:none;color:#f2e8ce;border:1.5px solid rgba(230,187,58,.5);
    background:linear-gradient(160deg,#17120f,#0b0807);padding:16px 16px 18px;
    box-shadow:0 16px 34px rgba(0,0,0,.6);transition:transform .15s,border-color .15s;}}
  .card:hover{{transform:translateY(-3px);border-color:#e6bb3a;}}
  .card b{{display:block;font-family:'Anton',Impact,sans-serif;font-size:30px;
    text-transform:uppercase;margin-bottom:4px;}}
  .card span{{display:block;font-size:12.5px;color:#c9bda1;line-height:1.45;}}
  .card .go{{margin-top:12px;font-size:11px;letter-spacing:.18em;color:#e01f3d;text-transform:uppercase;}}
</style>
</head>
<body data-variant="a" data-layout="v1">
<div class="chooser">
  <div class="kicker">HIST 350 · GROUP 4 · MORGAN STATE UNIVERSITY</div>
  <h1>The Name Changes. <em>The Function Does Not.</em></h1>
  <p>Four boards, one argument: the logic of controlling and extracting from Black bodies
  was never abolished — only rebuilt in new legal form. Pick a layout; every board carries the
  same ten panels, sources and symbol key.</p>
  <div class="cards">
    <a class="card" href="board_v1.html"><b>V1 · Original</b>
      <span>Near-black bed, four rows of cream cards. Sparse, archival, quiet.</span>
      <div class="go">Open V1 →</div></a>
    <a class="card" href="board_quilt.html"><b>Quilt</b>
      <span>Irregular panels stitched onto a sewn patchwork of media, red thread lacing the board.</span>
      <div class="go">Open Quilt →</div></a>
    <a class="card" href="board_zine.html"><b>Zine</b>
      <span>Newsprint leaflet: masthead, left rail, three columns. Bright paper, black ink.</span>
      <div class="go">Open Zine →</div></a>
    <a class="card" href="board_broadside.html"><b>Broadside</b>
      <span>Asymmetric protest flyer with a hero panel and stacked columns.</span>
      <div class="go">Open Broadside →</div></a>
  </div>
</div>
</body>
</html>
"""


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--layout", choices=["broadside", "quilt", "zine", "v1"], default=None)
    ap.add_argument("--html-only", action="store_true")
    ap.add_argument("--no-pdf", action="store_true")
    args = ap.parse_args()
    layouts = [args.layout] if args.layout else ["broadside", "quilt", "zine", "v1"]
    for v in layouts:
        render(v, html_only=args.html_only, pdf=not args.no_pdf)
    if not args.html_only:
        (ROOT / "index.html").write_text(CHOOSER, encoding="utf-8")
        print("[chooser] wrote", ROOT / "index.html")
