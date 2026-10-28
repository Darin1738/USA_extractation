#!/usr/bin/env python3
"""
Bundle the whole board into ONE self-contained HTML file.

Produces:  TheNameChanges_portable.html   (open it anywhere, no folder needed)

It inlines:
  - fonts.css + caslon.css  (each .woff2 -> base64 data URI)
  - board.css + board_v4.css  (as <style>)
  - board.js  (as <script>)
  - every ../media/* image and assets/external/* image -> optimized base64 data URI
  - all four layouts (quilt is the default view), switched in-page.

Images are downscaled to fit a projector (max long edge ~1400px, JPEG q85)
unless they are already small. Run:
  /tmp/opencode/venv/bin/python scripts/bundle.py
  /tmp/opencode/venv/bin/python scripts/bundle.py --max-edge 1600 --quality 88
"""
from __future__ import annotations

import argparse
import base64
import io
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MEDIA = ROOT.parent / "media"
EXT = ROOT / "assets" / "external"
FONTS = ROOT / "assets" / "fonts"

sys.path.insert(0, str(ROOT / "scripts"))
import build_board_v4 as B  # noqa: E402


def read(p: Path) -> str:
    return p.read_text(encoding="utf-8")


def inline_fonts(css: str) -> str:
    def repl(m: re.Match) -> str:
        fn = m.group(1)
        f = FONTS / fn
        if not f.exists():
            return m.group(0)
        b64 = base64.b64encode(f.read_bytes()).decode("ascii")
        return f"url(data:font/woff2;base64,{b64}) format('woff2')"
    return re.sub(r"url\('([^']+\.woff2)'\)\s*format\('woff2'\)", repl, css)


def optimize_image(path: Path, max_edge: int, quality: int) -> tuple[str, str]:
    """Return (mime, base64) for an image, downscaled if needed."""
    from PIL import Image
    try:
        im = Image.open(path)
    except Exception:
        # fall back to raw bytes with a guessed mime
        raw = path.read_bytes()
        mime = "image/png" if path.suffix.lower() == ".png" else "image/jpeg"
        return mime, base64.b64encode(raw).decode("ascii")

    im.load()
    has_alpha = im.mode in ("RGBA", "LA") or (im.mode == "P" and "transparency" in im.info)
    w, h = im.size
    scale = min(1.0, max_edge / max(w, h))
    if scale < 1.0:
        im = im.resize((max(1, int(w * scale)), max(1, int(h * scale))), Image.LANCZOS)

    buf = io.BytesIO()
    if has_alpha:
        im.convert("RGBA").save(buf, format="PNG", optimize=True)
        mime = "image/png"
    else:
        im.convert("RGB").save(buf, format="JPEG", quality=quality, optimize=True, progressive=True)
        mime = "image/jpeg"
    return mime, base64.b64encode(buf.getvalue()).decode("ascii")


def data_uri(path: Path, max_edge: int, quality: int) -> str:
    mime, b64 = optimize_image(path, max_edge, quality)
    return f"data:{mime};base64,{b64}"


def inline_images(html: str, max_edge: int, quality: int) -> tuple[str, str, dict, int]:
    """Return (html, extra_css, emb_map, n_unique).

    Every unique image is embedded EXACTLY ONCE as a data URI inside a
    `.emb-N{background-image:...}` rule. Elements that used a background or an
    <img> are rewritten to reference that class, so the (large) base64 payload
    never appears more than once in the document.
    emb_map maps the original filename (e.g. "Slave Voyages Map.png") to its
    css class, for the modal's dynamic image rendering.
    """
    rel_to_id: dict[str, str] = {}
    emb_map: dict[str, str] = {}
    uri_by_id: dict[str, str] = {}

    def resolve(rel: str) -> Path | None:
        from urllib.parse import unquote
        if rel.startswith("../media/"):
            return MEDIA / unquote(rel[len("../media/"):])
        if rel.startswith("assets/external/"):
            return EXT / unquote(Path(rel).name)
        return None

    def get_id(rel: str) -> str | None:
        if rel in rel_to_id:
            return rel_to_id[rel]
        fs = resolve(rel)
        if fs is None or not fs.exists():
            return None
        eid = f"emb{len(rel_to_id)}"
        rel_to_id[rel] = eid
        emb_map[fs.name] = eid
        uri_by_id[eid] = data_uri(fs, max_edge, quality)
        return eid

    def emit_img(rel: str, cls: str = "", style: str = "", alt: str = "") -> str:
        """A real <img> whose src is filled from window.DATA at runtime.
        Real <img> elements render reliably in every browser (incl. Firefox),
        unlike large CSS background-image data URIs."""
        eid = get_id(rel)
        if not eid:
            return ""
        a = esc_attr(alt or Path(rel).name)
        c = ("emb-img " + cls).strip()
        st = f' style="{style}"' if style else ""
        return f'<img class="{c}" data-emb="{eid}" alt="{a}"{st}>'

    # ---- inline styles that carry a background-image photo -------------------
    # These become a positioned <img> child so the photo shows everywhere.
    def bg_to_img(pre: str, cls: str | None, style: str) -> str:
        rels = re.findall(r"url\(\s*'((?:\.\./media/|assets/external/)[^']+)'\s*\)", style)
        rels = [r for r in rels if get_id(r)]
        if not rels:
            return None  # unchanged
        rel = rels[0]
        # strip the url() declaration; keep layout props in the style attr
        clean = re.sub(
            r"background-image\s*:\s*url\(\s*['\"]?(?:\.\./media/|assets/external/)[^)]*\)\s*;?",
            "", style)
        clean = re.sub(r"(style=\")[;\s]*", r"\1", clean).replace(";;", ";")
        newcls = ((cls or "") + " has-img").strip()
        fpre = pre if pre.endswith(" ") else pre + " "
        return (f'{fpre}class="{newcls}"{clean}>'
                + emit_img(rel, "fill-img"))

    # closed empty div with class= then style=
    def pass1(m: re.Match) -> str:
        r = bg_to_img(m.group(1), m.group(2), m.group(3))
        return r if r is not None else m.group(0)
    html = re.sub(
        r'(<(?:div|span)\b[^>]*?)\sclass="([^"]*)"\s*style="([^"]*)"\s*>\s*</(?:div|span)>',
        pass1, html)
    html = re.sub(
        r'(<(?:div|span)\b[^>]*?)\sclass="([^"]*)"\s*style="([^"]*)"\s*/>',
        pass1, html)

    # closed empty div with style= but no class=
    def pass2(m: re.Match) -> str:
        r = bg_to_img(m.group(1), None, m.group(2))
        return r if r is not None else m.group(0)
    html = re.sub(
        r'(<(?:div|span)\b(?![^>]*\bclass=)[^>]*?)style="([^"]*)"\s*>\s*</(?:div|span)>',
        pass2, html)

    # ---- <img src="rel">  ->  <img data-emb="N"> ----------------------------
    def repl_img(m: re.Match) -> str:
        rel = m.group(2)
        tail = m.group(3) or ""
        alt = re.search(r'alt="([^"]*)"', tail)
        style = re.search(r'style="([^"]*)"', tail)
        cls = re.search(r'class="([^"]*)"', tail)
        return emit_img(rel, cls.group(1) if cls else "",
                        style.group(1) if style else "",
                        alt.group(1) if alt else "")
    html = re.sub(r'(<img\b[^>]*?\bsrc=")((?:\.\./media/|assets/external/)[^"]+)("[^>]*?/?>)',
                  repl_img, html)

    return html, uri_by_id, emb_map, len(rel_to_id)


def esc_attr(s: str) -> str:
    return (s.replace("&", "&amp;").replace('"', "&quot;")
             .replace("<", "&lt;").replace(">", "&gt;"))




def build(max_edge: int, quality: int, default_layout: str) -> Path:
    out = ROOT / "TheNameChanges_portable.html"
    doc = B.build_combined_html(default_layout)

    # 1) inline the stylesheets
    fonts_css = inline_fonts(read(FONTS / "fonts.css") + "\n" + read(FONTS / "caslon.css"))
    board_css = read(ROOT / "assets" / "board.css") + "\n" + read(ROOT / "assets" / "board_v4.css")

    # 2) inline the script
    js = read(ROOT / "assets" / "board.js")
    script_block = f"<script>\n{js}\n</script>"

    # 3) inline images: one data URI per unique image, delivered via real <img>
    doc, uri_by_id, emb_map, n_imgs = inline_images(doc, max_edge, quality)

    # window.DATA maps emb-id -> data URI; a tiny loader fills every <img>,
    # including ones created later by the modal.  <img data-emb="N">
    loader = (
        "<script>window.DATA=" + json.dumps(uri_by_id, ensure_ascii=False) + ";\n"
        "window.EMB=" + json.dumps(emb_map, ensure_ascii=False) + ";\n"
        "(function(){function fill(root){(root||document).querySelectorAll"
        "('img[data-emb]').forEach(function(im){var u=window.DATA[im.dataset.emb];"
        "if(u&&im.src!==u)im.src=u;});}window.fillEmb=fill;"
        "document.addEventListener('DOMContentLoaded',function(){fill();});"
        "if(document.readyState!=='loading')fill();})();</script>"
    )

    # the media elements are real <img> tags; keep the board's img rules working
    # and give the patch photos an absolutely-filled layer.
    img_compat = (
        ".emb-img{display:block;}\n"
        ".has-img{position:relative;overflow:hidden;}\n"
        ".has-img>.fill-img{position:absolute;inset:0;width:100%;height:100%;"
        "object-fit:cover;background:#0b0908;}\n"
        "figure>.emb-img{width:100%;height:100%;flex:1 1 auto;min-height:0;"
        "object-fit:cover;}\n"
        "figure.fit>.emb-img{object-fit:contain;background:#0a0908;}\n"
        ".m-media figure>.emb-img{height:auto;min-height:80px;object-fit:contain;"
        "background:#0a0908;}\n"
    )

    # 4) swap external links for inline styles/script
    doc = re.sub(r'\s*<link rel="stylesheet" href="assets/fonts/fonts\.css">', "", doc)
    doc = re.sub(r'\s*<link rel="stylesheet" href="assets/fonts/caslon\.css">', "", doc)
    doc = re.sub(r'\s*<link rel="stylesheet" href="assets/board\.css">', "", doc)
    doc = re.sub(r'\s*<link rel="stylesheet" href="assets/board_v4\.css">', "", doc)
    style_block = (f"<style>\n/* fonts */\n{fonts_css}\n/* base */\n{board_css}\n"
                   f"/* image compat */\n{img_compat}\n</style>")
    doc = doc.replace("</head>", style_block + "\n</head>")
    doc = doc.replace('<script src="assets/board.js"></script>',
                      loader + "\n" + script_block)

    out.write_text(doc, encoding="utf-8")
    mb = out.stat().st_size / (1024 * 1024)
    print(f"[bundle] inlined {n_imgs} unique images; wrote {out} ({mb:.1f} MB)")
    return out


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--max-edge", type=int, default=1400)
    ap.add_argument("--quality", type=int, default=85)
    ap.add_argument("--default-layout", default="quilt")
    args = ap.parse_args()
    build(args.max_edge, args.quality, args.default_layout)
