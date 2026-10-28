#!/usr/bin/env python3
"""
Group 4 · HIST 350 · The Name Changes / The Function Does Not
v3 builder — DARK, DENSE, FLYER-SIZED (18 x 24 in portrait).

Content comes from build_board.py (P, SYMBOLS) so the copy lives in one place.
This script owns the v3 LAYOUT, the continuous dark montage collage, and the
three visual variants.

Variants:
  a = colour collage   (saturated pan-African red/green/gold over black)
  b = duotone evidence (archival photos, ink/maroon duotone, gold+green accents)
  c = bold graphic     (flat colour fields, huge type, symbols as heroes)

Run:
  /tmp/opencode/venv/bin/python scripts/build_board_v3.py                # all 3
  /tmp/opencode/venv/bin/python scripts/build_board_v3.py --variant a
  /tmp/opencode/venv/bin/python scripts/build_board_v3.py --variant a --html-only
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

# --------------------------------------------------------------------------
# v3 canvas: 18 x 24 in portrait  ->  1800 x 2400 @100ppi
# --------------------------------------------------------------------------
W, H = 1800, 2400
M = 44  # margin

BANNER = dict(x=M, y=M, w=W - 2 * M, h=336)
ROW_Y = [416, 806, 1196, 1586]
PANEL_H = 378
LEFT_X, RIGHT_X = M, 936
PANEL_W = 820
P10 = dict(x=M, y=1976, h=356)          # wide resistance/memory panel under the grid
FOOTER_Y = 2346
# rows occupy 416..1964 ; P10 1976..2332 ; footer 2346..2400

# --------------------------------------------------------------------------
# sourced public-domain imagery (see assets/external/SOURCES.md)
# --------------------------------------------------------------------------
PD = {
    "tulsa_riot": EXT / "tulsa_ruins_after_riot.jpg",
    "tulsa_mob": EXT / "tulsa_ruins_after_mob.jpg",
    "tulsa_furn": EXT / "tulsa_furniture_street.jpg",
    "tulsa_burn": EXT / "tulsa_greenwood_burning.jpg",
    "chain_thomas": EXT / "chain_gang_thomasville.jpg",
    "chain_on": EXT / "on_the_chain_gang.jpg",
    "shackles": EXT / "shackles_pre1860.jpg",
    "freedmen_bureau": EXT / "freedmens_bureau.jpg",
    "freedmen_school": EXT / "freedmen_school_richmond.jpg",
    "buffalo": EXT / "buffalo_soldier_25th.jpg",
}


def ext_src(p: Path) -> str:
    # index.html lives in infographic/, so assets/ is a direct sibling
    return "assets/external/" + urlquote(p.name)


# --------------------------------------------------------------------------
# montage: a deterministic (seeded) dense layer of overlapping cut-outs.
# each piece = (kind, payload, x, y, w, h, rot, tone)
# kind: 'photo' | 'sym' | 'type' | 'block' | 'tape' | 'stamp'
# --------------------------------------------------------------------------
def build_montage(variant: str) -> list[dict]:
    rng = random.Random(3500)  # deterministic across runs
    pieces: list[dict] = []

    photos = list(PD.items())
    symkeys = ["globe", "fist", "broken-chain", "torch", "kente",
               "dove", "megaphone", "barbed-wire", "poppy", "open-hands", "thread"]
    tones = ["red", "green", "gold", "black"]
    frag = [
        "PROPERTY", "1865", "EXCEPT", "BLACK CODES", "CONVICT LEASING",
        "JIM CROW", "MASS INCARCERATION", "RISK SCORE", "TULSA 1921",
        "NEVER AGAIN", "FREE BUT BOUND", "THE RECORD", "1619", "13TH",
        "SEIZED", "ENDURED", "REMEMBER", "NO JUSTICE",
    ]

    # --- photos: large, overlapping, cover most of the canvas ---------------
    # hand-placed "spine" photos guarantee full coverage; then jitter cluster.
    anchors = [
        (EXT / "slave_atlantic_trade_slave_ship.jpg", -60, -40, 520, 380),
        (PD["tulsa_burn"], 1180, -30, 620, 440),
        (PD["shackles"], -70, 380, 460, 320),
        (PD["chain_thomas"], 1240, 430, 600, 430),
        (PD["freedmen_bureau"], 300, 760, 560, 420),
        (PD["freedmen_school"], 1250, 900, 540, 420),
        (PD["chain_on"], -80, 1140, 520, 400),
        (PD["buffalo"], 1230, 1380, 580, 420),
        (PD["tulsa_riot"], 120, 1520, 620, 460),
        (PD["tulsa_furn"], 900, 1760, 620, 440),
        (EXT / "african_american_convicts_w_shovels.jpg", 80, 1900, 520, 380),
        (PD["tulsa_mob"], 700, 1150, 480, 360),
    ]
    for i, (f, x, y, w, h) in enumerate(anchors):
        if not f.exists():
            continue
        pieces.append(dict(kind="photo", src=ext_src(f), x=x, y=y, w=w, h=h,
                           rot=round(rng.uniform(-9, 9), 2),
                           tone=rng.choice(tones + ["ink"]), depth=i))

    # secondary jittered photos to fill gaps between anchors
    for i in range(10):
        _, f = photos[i % len(photos)]
        if not f.exists():
            continue
        x = rng.randint(-80, W - 240)
        y = rng.randint(-60, H - 220)
        w = rng.randint(280, 520)
        h = int(w * rng.uniform(0.62, 0.9))
        pieces.append(dict(kind="photo", src=ext_src(f), x=x, y=y, w=w, h=h,
                           rot=round(rng.uniform(-12, 12), 2),
                           tone=rng.choice(tones + ["ink", "ink"]), depth=20 + i))

    # --- torn paper colour blocks (the pan-African colour field) -----------
    for i in range(26):
        w = rng.randint(150, 340)
        h = rng.randint(120, 300)
        pieces.append(dict(kind="block", x=rng.randint(-40, W - 120),
                           y=rng.randint(-40, H - 120), w=w, h=h,
                           rot=round(rng.uniform(-14, 14), 2),
                           tone=rng.choice(tones), depth=50 + i))

    # --- symbol cut-outs, large, edge-bleeding ----------------------------
    for i, key in enumerate(symkeys):
        w = rng.randint(240, 460)
        pieces.append(dict(kind="sym", key=key, x=rng.randint(-120, W - 180),
                           y=rng.randint(-80, H - 220), w=w, h=w,
                           rot=round(rng.uniform(-16, 16), 2),
                           tone=rng.choice(["red", "green", "gold", "cream"]),
                           depth=90 + i))

    # --- type fragments (newspaper / letterpress energy) ------------------
    for i in range(22):
        pieces.append(dict(kind="type", text=rng.choice(frag),
                           x=rng.randint(-20, W - 200), y=rng.randint(-10, H - 40),
                           w=rng.randint(140, 380), rot=round(rng.uniform(-16, 16), 2),
                           tone=rng.choice(tones + ["cream", "cream"]), depth=140 + i))

    # --- tape + stamps, crossing everything -------------------------------
    for i in range(22):
        pieces.append(dict(kind="tape", x=rng.randint(-40, W - 120),
                           y=rng.randint(-20, H - 60), w=rng.randint(120, 260),
                           rot=round(rng.uniform(-70, 70), 2),
                           tone=rng.choice(tones), depth=200 + i))
    stamps = [
        "PAN-AFRICAN", "REMEMBER TULSA", "NO JUSTICE · NO PEACE",
        "GROUP 4 · HIST 350", "1619 → PRESENT", "FREE · BUT BOUND",
        "THE RECORD IS THE FRONT", "STILL REBUILDING", "RESIST",
        "ACCUMULATION BY DISPOSSESSION",
    ]
    for i, s in enumerate(stamps):
        pieces.append(dict(kind="stamp", text=s,
                           x=rng.randint(0, W - 200), y=rng.randint(40, H - 60),
                           rot=round(rng.uniform(-14, 14), 2),
                           tone=rng.choice(tones), depth=240 + i))

    pieces.sort(key=lambda d: d["depth"])
    return pieces


def montage_html(pieces: list[dict]) -> str:
    out = []
    for p in pieces:
        st = (f"left:{p['x']}px;top:{p['y']}px;"
              f"width:{p.get('w',0)}px;height:{p.get('h',0)}px;"
              f"transform:rotate({p['rot']}deg)")
        k = p["kind"]
        if k == "photo":
            out.append(f'<div class="cut photo t-{p["tone"]}" style="{st};'
                       f'background-image:url(\'{p["src"]}\')"></div>')
        elif k == "block":
            out.append(f'<div class="cut block t-{p["tone"]}" style="{st}"></div>')
        elif k == "sym":
            svg = (SYM / f"{p['key']}.svg").read_text()
            out.append(f'<div class="cut sym t-{p["tone"]}" data-sym="{p["key"]}" '
                       f'style="{st}">{svg}</div>')
        elif k == "type":
            out.append(f'<div class="cut type t-{p["tone"]}" style="{st}">{html.escape(p["text"])}</div>')
        elif k == "tape":
            out.append(f'<div class="cut tape t-{p["tone"]}" style="{st}"></div>')
        elif k == "stamp":
            out.append(f'<div class="cut stamp t-{p["tone"]}" style="{st}">{html.escape(p["text"])}</div>')
    return '<div class="montage" aria-hidden="true">' + "".join(out) + "</div>"


# --------------------------------------------------------------------------
# layout markup (v3 coordinates)
# --------------------------------------------------------------------------
def banner_html() -> str:
    b = BANNER
    return f"""
<section class="banner" data-panel="p1" tabindex="0" role="button"
  aria-label="Open the thesis banner"
  style="left:{b['x']}px;top:{b['y']}px;width:{b['w']}px;height:{b['h']}px">
  <div class="b-left">
    <div class="kicker"><span class="dot"></span>HIST 350 · GROUP 4 · MORGAN STATE UNIVERSITY</div>
    <h1 class="b-title"><span>THE NAME CHANGES.</span><span>THE <em>FUNCTION</em> DOES NOT.</span></h1>
    <p class="thesis">“Slavery was abolished, but the logic of <b>controlling and extracting</b> from Black bodies was rebuilt in new legal form.”</p>
    <div class="b-meta">SIX AREAS OF CONTROL <span>·</span> THREE PILLARS <span>·</span> ONE CONTINUOUS LINE</div>
  </div>
  <div class="b-right">
    <div class="case">
      <div class="label">Opening question / case file 01</div>
      <p class="q">If slavery was abolished in 1865, <em>why did prisons become overrun with Black bodies?</em></p>
      <p class="sub">The answer is assembled across ten panels →</p>
    </div>
    <div class="hookside"><span>Follow the red thread</span><span class="rule"></span><span>1619 → present</span></div>
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
</section>"""


def panel_html(p: dict) -> str:
    style = f"left:{p['x']}px;top:{p['y']}px;width:{p['w']}px;height:{p['h']}px;"
    return f"""
<article class="panel {p.get('cls','').strip()}" data-panel="{p['id']}" tabindex="0"
  role="button" aria-label="Open panel {p['num']}: {html.escape(p['title'])}" style="{style}">
  <span class="tape tl"></span><span class="tape br"></span>
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
    <p class="ask"><span class="asktag">ASK</span>{html.escape(p['question'])}</p>
    <p class="src">SRC · {html.escape(p['source'])}</p>
  </div>
</article>"""


def p10_html() -> str:
    p = P["p10"]
    b = P10
    res = "".join(
        f'<div class="res-item"><div class="y">{y}</div><div class="t">{t}</div><div class="d">{d}</div></div>'
        for y, t, d in p["resistance"])
    mem = "".join(
        f'<div class="mem-item"><div class="y">{y}</div><div class="t">{t}</div><div class="d">{d}</div></div>'
        for y, t, d in p["memory"])
    return f"""
<article class="panel wide" data-panel="p10" tabindex="0" role="button"
  aria-label="Open panel 10: resistance and memory"
  style="left:{b['x']}px;top:{b['y']}px;width:{W-2*M}px;height:{b['h']}px">
  <span class="tape tl"></span><span class="tape br"></span>
  <header class="p-head">
    <div class="era">{p['era']}</div>
    <div class="pnum"><b>{p['num']}</b><span>/ 10</span></div>
  </header>
  <div class="w-body">
    <div class="w-left">
      <h2 class="p-title">{p['title']}</h2>
      <p class="p-arg">{p['arg']}</p>
      <div class="w-close">
        <div class="closing">THE NAME CHANGES. <span>THE FUNCTION DOES NOT.</span></div>
        <p class="ask"><span class="asktag">ASK</span>{html.escape(p['question'])}</p>
        <p class="src">SRC · {html.escape(p['source'])}</p>
      </div>
    </div>
    <div class="res">
      <div class="res-block"><h3>Resistance</h3><div class="res-grid">{res}</div></div>
      <div class="mem-block"><h3>Memory / erasure</h3><div class="mem-grid">{mem}</div></div>
    </div>
  </div>
</article>"""


def spine_html() -> str:
    top, h = ROW_Y[0], (ROW_Y[-1] + PANEL_H) - ROW_Y[0]
    years = [(1619, 40), (1865, 360), (1868, 470), (1890, 660), (1971, 960), (2000, 1140), (2025, 1320)]
    yrs = "".join(f'<div class="yr" style="top:{t}px">{y}</div>' for y, t in years)
    return f"""
<div class="spine" aria-hidden="true" style="left:876px;top:{top}px;height:{h}px">
  <div class="rail"></div>
  {yrs}
  <div class="pillar p1"><div class="num">I</div><div class="bar"></div><div class="lbl">PROFIT FROM BLACK BODIES</div></div>
  <div class="pillar p2"><div class="num">II</div><div class="bar"></div><div class="lbl">CONVICT LEASING <b>→</b> PRISON LABOR</div></div>
  <div class="pillar p3"><div class="num">III</div><div class="bar"></div><div class="lbl">PLANTATION <b>→</b> ALGORITHM</div></div>
</div>"""


KEYS = ["globe", "fist", "broken-chain", "torch", "kente",
        "dove", "megaphone", "barbed-wire", "poppy", "open-hands"]


def symkeys_html() -> str:
    out = []
    for i, key in enumerate(KEYS):
        s = SYMBOLS[key]
        col = i % 5
        row = i // 5
        x = 60 + col * 176
        top = ROW_Y[0] + 6 + row * 30
        out.append(f'<div class="symkey" data-symkey="{key}" style="left:{x}px;top:{top}px">'
                   f'<b>{s["num"]}</b>{s["name"]}<i>↗</i></div>')
    return "".join(out)


GAPNOTES = [
    (ROW_Y[0] + PANEL_H + 8, 'PROFIT MOVES FROM THE PLANTATION <b>→</b> THE PRISON <b>→</b> THE PLATFORM'),
    (ROW_Y[1] + PANEL_H + 8, 'THE LAW STOPS SAYING “BLACK.” <b>THE OUTCOMES DO NOT.</b>'),
    (ROW_Y[2] + PANEL_H + 8, 'EVERY SYSTEM OF CONTROL MET ORGANIZED RESISTANCE'),
]


def gapnotes_html() -> str:
    return "".join(
        f'<div class="gapnote" style="left:{M}px;top:{y}px;width:{W-2*M}px;justify-content:center">'
        f'<span class="ln"></span><span>{txt}</span><span class="ln"></span></div>'
        for y, txt in GAPNOTES)


def panel_positions() -> None:
    order = ["p2", "p3", "p4", "p5", "p6", "p7", "p8", "p9"]
    for i, pid in enumerate(order):
        row, col = divmod(i, 2)
        P[pid]["x"] = LEFT_X if col == 0 else RIGHT_X
        P[pid]["y"] = ROW_Y[row]
        P[pid]["w"] = PANEL_W
        P[pid]["h"] = PANEL_H
        P[pid]["id"] = pid


FOOT = ("GROUP 4 · DARIN L. WESLEY (LEADER) · COURTNEY FOWLKES (ASST.) · KIARRA M · "
        "ANTWAN POWELL · DEJUAN G · MAKAYLA PARSI · TAJA BRIDGES")


def build_html(variant: str) -> str:
    panel_positions()
    board_json = {
        "variant": variant,
        "panels": {pid: {k: v for k, v in P[pid].items() if k in
                         ("num", "tag", "era", "title", "arg", "facts", "stat", "stats",
                          "quote", "images", "question", "source", "notes", "questions",
                          "sources", "note")} for pid in P},
        "symbols": SYMBOLS,
    }
    doc = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Group 4 · The Name Changes — variant {variant.upper()}</title>
<link rel="stylesheet" href="assets/fonts/fonts.css">
<link rel="stylesheet" href="assets/fonts/caslon.css">
<link rel="stylesheet" href="assets/board.css">
<link rel="stylesheet" href="assets/board_v3.css">
<link rel="stylesheet" href="assets/board_v3_{variant}.css">
</head>
<body data-variant="{variant}">
<div class="holder"><div class="stage" id="stage">
  {montage_html(build_montage(variant))}
  {banner_html()}
  {''.join(panel_html(P[k]) for k in ('p2','p3','p4','p5','p6','p7','p8','p9'))}
  {p10_html()}
  {spine_html()}
  {symkeys_html()}
  {gapnotes_html()}
  <div class="footer" style="left:{M}px;top:{FOOTER_Y}px;width:{W-2*M}px">
    <div><b>GROUP 4</b> · {FOOT.split('·',1)[1].strip()}</div>
    <div class="r">SOURCES ON EACH PANEL · SEE BIBLIOGRAPHY, MEDIA MANIFEST &amp; VERIFICATION LOG · AI USE: LAYOUT, TYPESETTING, SYMBOLS &amp; DRAFT ASSISTANCE; RESEARCH &amp; SOURCE CHECKS: GROUP 4</div>
  </div>
</div></div>

<dialog id="modal" aria-label="Panel detail">
  <div id="modal-head" class="m-head"></div>
  <div id="modal-body" class="m-body"></div>
</dialog>

<div class="toolbar" role="toolbar" aria-label="Board controls">
  <div class="brand"><b>GROUP 4</b> · THE NAME CHANGES</div>
  <button id="xray" type="button">X-RAY THE COLLAGE</button>
  <button id="qtoggle" type="button">HIDE QUESTIONS</button>
</div>

<script>window.BOARD = {json.dumps(board_json, ensure_ascii=False)};</script>
<script src="assets/board.js"></script>
</body>
</html>
"""
    return doc


# --------------------------------------------------------------------------
# render + QA
# --------------------------------------------------------------------------
def render(variant: str, html_only: bool = False) -> None:
    idx = ROOT / "index.html"
    idx.write_text(build_html(variant), encoding="utf-8")
    print(f"[{variant}] wrote {idx}")
    if html_only:
        return

    from playwright.sync_api import sync_playwright

    url = idx.as_uri()
    stem = f"board_v3{variant}"
    with sync_playwright() as pw:
        browser = pw.chromium.launch()
        page = browser.new_page(viewport={"width": W, "height": H}, device_scale_factor=1)
        page.goto(url, wait_until="load")
        page.wait_for_function("document.fonts && document.fonts.status === 'loaded'")
        page.wait_for_function("Array.from(document.images).every(i => i.complete)")
        page.evaluate("document.body.classList.add('static'); document.documentElement.style.setProperty('--fit','1')")
        page.wait_for_timeout(400)

        qa = page.evaluate("""() => {
          const panels = [...document.querySelectorAll('.panel, .banner')].map(el => {
            const r = el.getBoundingClientRect();
            const out = [];
            for (const k of el.querySelectorAll('*')) {
              if (k.classList && (k.classList.contains('tape') || k.classList.contains('scr-tape') ||
                  k.classList.contains('stamp') || k.classList.contains('open-hint'))) continue;
              const kr = k.getBoundingClientRect();
              if (kr.width > 0 && (kr.right > r.right + 1 || kr.bottom > r.bottom + 1 ||
                  kr.left < r.left - 1 || kr.top < r.top - 1)) out.push((k.className&&String(k.className).slice(0,40))||k.tagName);
            }
            return {id: el.dataset.panel || el.className,
                    scrollOverflow: el.scrollHeight - el.clientHeight,
                    out: [...new Set(out)].slice(0,6)};
          });
          const images = [...document.images].map(i => ({src: i.getAttribute('src'),
            ok: i.complete && i.naturalWidth > 0}));
          return {panels, badImages: images.filter(i=>!i.ok), fonts: document.fonts.status,
                  dialog: document.querySelector('dialog') ? 'ok' : 'missing'};
        }""")
        print(f"[{variant}] QA", json.dumps(qa, ensure_ascii=False)[:1200])

        page.locator("#stage").screenshot(path=str(OUT / f"{stem}.png"))
        print(f"[{variant}] wrote {stem}.png")

        hi = browser.new_page(viewport={"width": W, "height": H}, device_scale_factor=1.5)
        hi.goto(url, wait_until="load")
        hi.wait_for_function("document.fonts && document.fonts.status === 'loaded'")
        hi.wait_for_function("Array.from(document.images).every(i => i.complete)")
        hi.evaluate("document.body.classList.add('static'); document.documentElement.style.setProperty('--fit','1')")
        hi.wait_for_timeout(300)
        hi.locator("#stage").screenshot(path=str(OUT / f"{stem}@150.png"))
        print(f"[{variant}] wrote {stem}@150.png")

        page.pdf(path=str(OUT / f"{stem}.pdf"), width="18in", height="24in",
                 margin={"top": "0", "bottom": "0", "left": "0", "right": "0"},
                 print_background=True, prefer_css_page_size=True)
        print(f"[{variant}] wrote {stem}.pdf")
        browser.close()


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--variant", choices=["a", "b", "c"], default=None)
    ap.add_argument("--html-only", action="store_true")
    args = ap.parse_args()
    variants = [args.variant] if args.variant else ["a", "b", "c"]
    for v in variants:
        render(v, html_only=args.html_only)
