#!/usr/bin/env python3
"""Generate original vector symbols for the Group 4 infographic board.

v2 — scrapbook redesign. The symbol set moves from institutional/punitive
icons to the themes the group asked for:

  Pan-Africanism · freedom in any form · revolution & resistance · peace & war

Every SVG here is original line/vector artwork drawn for this project (no
external imagery, no tracing). They are line-based so the board can tint them
with CSS (currentColor), overlap them in the collage, and toggle them in
X-ray mode.
"""
from pathlib import Path

OUT = Path(__file__).resolve().parent.parent / "assets" / "symbols"
OUT.mkdir(parents=True, exist_ok=True)

HEAD = ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="{vb}" fill="none" '
        'stroke="currentColor" stroke-linecap="round" stroke-linejoin="round">\n')
END = "</svg>\n"

SYMBOLS = {}

# 01 · Pan-Africanism — globe centred on the African continent
SYMBOLS["globe"] = ("0 0 420 420", """
  <circle cx="210" cy="210" r="176" stroke-width="9"/>
  <ellipse cx="210" cy="210" rx="176" ry="72" stroke-width="7"/>
  <ellipse cx="210" cy="210" rx="72" ry="176" stroke-width="7"/>
  <path d="M210 34 C286 92 306 156 296 210 C286 268 250 322 210 386" stroke-width="7"/>
  <path d="M210 34 C134 92 114 156 124 210 C134 268 170 322 210 386" stroke-width="7"/>
  <path d="M46 168 h46 l24 -30 34 8 20 -26 30 14 24 -18 24 20 28 -8 22 24 28 4 26 22 h34" stroke-width="8"/>
  <path d="M46 252 h40 l26 24 30 -14 26 20 30 -12 26 22 30 -16 30 18 28 -10 26 16 h34" stroke-width="8" opacity=".72"/>
  <path d="M168 132 q28 -20 54 -8" stroke-width="6" opacity=".6"/>
  <path d="M258 96 q22 16 22 42" stroke-width="6" opacity=".6"/>
""")

# 02 · Revolution & resistance — raised fist
SYMBOLS["fist"] = ("0 0 420 420", """
  <path d="M150 214 V150 c0 -12 18 -12 18 0 v50" stroke-width="12"/>
  <path d="M168 172 V128 c0 -13 19 -13 19 0 v44" stroke-width="12"/>
  <path d="M187 138 V120 c0 -13 19 -13 19 0 v30" stroke-width="12"/>
  <path d="M206 130 V122 c0 -12 18 -12 18 0 v30" stroke-width="12"/>
  <path d="M224 168 V138 c0 -12 18 -12 18 0 v92" stroke-width="12"/>
  <path d="M150 214 c-24 -10 -44 -2 -46 20 -3 26 18 40 34 36 l40 -8" stroke-width="12"/>
  <path d="M242 230 c26 -14 62 4 62 40 0 44 -38 78 -86 78 h-26 c-40 0 -66 -18 -78 -46"
        stroke-width="12"/>
  <path d="M118 268 c-18 6 -30 -8 -26 -24" stroke-width="10"/>
  <path d="M148 250 q20 6 34 2" stroke-width="9" opacity=".7"/>
  <path d="M176 206 q16 4 28 0" stroke-width="9" opacity=".7"/>
  <path d="M320 96 l16 -22 M340 120 l24 -12 M300 76 l6 -26" stroke-width="8" opacity=".75"/>
""")

# 03 · Freedom in any form — breaking chain
SYMBOLS["broken-chain"] = ("0 0 460 420", """
  <g stroke-width="15">
    <ellipse cx="104" cy="210" rx="62" ry="34" transform="rotate(-24 104 210)"/>
    <ellipse cx="188" cy="188" rx="62" ry="34" transform="rotate(-24 188 188)"/>
    <ellipse cx="372" cy="210" rx="62" ry="34" transform="rotate(-24 372 210)"/>
    <ellipse cx="288" cy="188" rx="62" ry="34" transform="rotate(-24 288 188)"/>
  </g>
  <path d="M236 196 l-10 -6 M244 176 l-12 8 M252 206 l6 -14" stroke-width="10" stroke-dasharray="0"/>
  <path d="M232 150 l-10 76" stroke-width="7" opacity=".5"/>
  <path d="M258 146 l10 78" stroke-width="7" opacity=".5"/>
  <path d="M228 262 q30 26 62 6" stroke-width="7" opacity=".6"/>
  <circle cx="240" cy="118" r="20" stroke-width="8" opacity=".8"/>
  <path d="M240 98 v-24 M240 138 v24 M220 118 h-24 M260 118 h24" stroke-width="7" opacity=".65"/>
""")

# 04 · Freedom / revolution — torch with flame
SYMBOLS["torch"] = ("0 0 360 460", """
  <path d="M150 420 h60 l-12 -44 h-36 z" stroke-width="10"/>
  <path d="M168 376 V236 h24 v140" stroke-width="10"/>
  <path d="M150 236 q0 -26 30 -26 q30 0 30 26 q0 22 -30 34 q-30 -12 -30 -34 z" stroke-width="11"/>
  <path d="M180 300 q-34 -18 -30 -58 q4 -44 30 -72 q26 28 30 72 q4 40 -30 58 z" stroke-width="12"/>
  <path d="M180 250 q-16 -12 -10 -34 q6 -20 10 -28 q4 8 10 28 q6 22 -10 34 z" stroke-width="8" opacity=".7"/>
  <path d="M64 118 q26 -14 50 4 M246 96 q24 -16 50 -2 M262 150 q22 -4 32 14"
        stroke-width="8" opacity=".7"/>
  <path d="M120 92 q-18 12 -14 34" stroke-width="7" opacity=".55"/>
""")

# 05 · Pan-Africanism — kente / Adinkra-inspired geometry
SYMBOLS["kente"] = ("0 0 460 420", """
  <rect x="46" y="46" width="368" height="328" stroke-width="11"/>
  <path d="M46 130 h368 M46 214 h368 M46 298 h368" stroke-width="9"/>
  <path d="M160 46 v328 M300 46 v328" stroke-width="9"/>
  <path d="M120 92 l20 20 l-20 20 l-20 -20 z" stroke-width="7" opacity=".8"/>
  <path d="M200 92 l20 20 l-20 20 l-20 -20 z" stroke-width="7" opacity=".8"/>
  <path d="M340 92 l20 20 l-20 20 l-20 -20 z" stroke-width="7" opacity=".8"/>
  <path d="M120 176 l20 20 l-20 20 l-20 -20 z" stroke-width="7" opacity=".8"/>
  <path d="M340 176 l20 20 l-20 20 l-20 -20 z" stroke-width="7" opacity=".8"/>
  <path d="M120 260 l20 20 l-20 20 l-20 -20 z" stroke-width="7" opacity=".8"/>
  <path d="M200 260 l20 20 l-20 20 l-20 -20 z" stroke-width="7" opacity=".8"/>
  <path d="M340 260 l20 20 l-20 20 l-20 -20 z" stroke-width="7" opacity=".8"/>
  <path d="M230 214 q0 -26 20 -26 q20 0 20 26 q0 26 -20 26 q-20 0 -20 -26" stroke-width="7" opacity=".75"/>
""" )

# 06 · Peace — dove with olive branch
SYMBOLS["dove"] = ("0 0 520 420", """
  <path d="M118 250 C170 250 210 218 244 178 C274 142 320 122 372 132
           C352 154 344 178 348 204 C352 226 366 244 392 258
           C338 274 286 276 236 262" stroke-width="12"/>
  <path d="M236 262 C214 292 176 306 138 296 C160 286 174 272 180 254"
        stroke-width="12"/>
  <path d="M372 132 C392 108 420 100 446 106 C428 118 418 134 414 154"
        stroke-width="11"/>
  <circle cx="368" cy="152" r="5" stroke-width="6"/>
  <path d="M244 178 C252 158 268 142 288 134" stroke-width="8" opacity=".7"/>
  <path d="M96 300 q40 22 84 14" stroke-width="9"/>
  <path d="M300 306 q28 10 54 2 q-18 18 -44 22 q6 14 -2 28 q-16 -12 -20 -30" stroke-width="9"/>
  <path d="M330 320 q22 -8 36 -26" stroke-width="7" opacity=".7"/>
""")

# 07 · Resistance / voice — megaphone
SYMBOLS["megaphone"] = ("0 0 520 420", """
  <path d="M96 250 L96 176 L300 96 L300 330 L96 250 z" stroke-width="12"/>
  <ellipse cx="300" cy="213" rx="26" ry="117" stroke-width="11"/>
  <path d="M96 176 L60 190 L60 236 L96 250" stroke-width="11"/>
  <path d="M132 254 L152 352 L196 352 L176 262" stroke-width="11"/>
  <path d="M340 138 q22 22 22 75 q0 53 -22 75" stroke-width="9" opacity=".8"/>
  <path d="M376 108 q36 38 36 105 q0 67 -36 105" stroke-width="9" opacity=".65"/>
  <path d="M412 78 q50 54 50 135 q0 81 -50 135" stroke-width="9" opacity=".5"/>
  <path d="M96 214 h-28" stroke-width="9" opacity=".7"/>
""")

# 08 · War / oppression — barbed wire
SYMBOLS["barbed-wire"] = ("0 0 560 300", """
  <path d="M20 150 C90 96 150 96 210 150 C270 204 330 204 390 150 C440 106 490 100 540 138"
        stroke-width="10"/>
  <path d="M20 190 C90 136 150 136 210 190 C270 244 330 244 390 190 C440 146 490 140 540 178"
        stroke-width="10" opacity=".8"/>
  <g stroke-width="9">
    <path d="M118 118 l-22 -18 M118 118 l22 -18 M118 118 l0 -28 M118 118 l0 28 M118 118 l-22 18 M118 118 l22 18"/>
    <path d="M280 210 l-22 -18 M280 210 l22 -18 M280 210 l0 -28 M280 210 l0 28 M280 210 l-22 18 M280 210 l22 18"/>
    <path d="M442 130 l-22 -18 M442 130 l22 -18 M442 130 l0 -28 M442 130 l0 28 M442 130 l-22 18 M442 130 l22 18"/>
  </g>
  <circle cx="118" cy="118" r="6" stroke-width="6"/>
  <circle cx="280" cy="210" r="6" stroke-width="6"/>
  <circle cx="442" cy="130" r="6" stroke-width="6"/>
""")

# 09 · Peace / remembrance — poppy
SYMBOLS["poppy"] = ("0 0 400 460", """
  <path d="M200 448 C200 380 196 330 200 292" stroke-width="10"/>
  <path d="M200 340 C160 330 132 300 128 262" stroke-width="9"/>
  <path d="M200 316 C240 306 268 276 272 238" stroke-width="9"/>
  <path d="M200 396 C176 388 158 368 152 344" stroke-width="8" opacity=".8"/>
  <g stroke-width="10">
    <ellipse cx="200" cy="150" rx="54" ry="74"/>
    <ellipse cx="118" cy="210" rx="54" ry="74" transform="rotate(62 118 210)"/>
    <ellipse cx="282" cy="210" rx="54" ry="74" transform="rotate(-62 282 210)"/>
    <ellipse cx="146" cy="96" rx="54" ry="74" transform="rotate(38 146 96)"/>
    <ellipse cx="254" cy="96" rx="54" ry="74" transform="rotate(-38 254 96)"/>
  </g>
  <circle cx="200" cy="158" r="30" stroke-width="9"/>
  <circle cx="200" cy="158" r="11" stroke-width="7" opacity=".8"/>
""")

# 10 · Freedom in any form — open hands releasing a bird
SYMBOLS["open-hands"] = ("0 0 520 420", """
  <path d="M96 300 C120 344 168 372 230 372 C300 372 348 344 372 300" stroke-width="12"/>
  <path d="M110 296 C140 330 182 350 230 350 C286 350 330 330 358 296"
        stroke-width="10" opacity=".75"/>
  <path d="M92 250 C80 214 92 176 120 156 C126 190 120 220 104 244" stroke-width="11"/>
  <path d="M368 250 C384 216 372 178 344 156 C338 190 344 220 360 244" stroke-width="11"/>
  <path d="M210 190 C214 150 244 122 286 116 C268 138 260 162 262 188
           C266 210 278 228 300 240 C256 252 218 236 202 214"
        stroke-width="11"/>
  <path d="M286 116 C302 96 326 90 348 96 C332 106 324 120 322 136"
        stroke-width="10"/>
  <circle cx="282" cy="146" r="5" stroke-width="6"/>
  <path d="M170 236 q26 -16 50 -10 M350 236 q-26 -16 -50 -10" stroke-width="8" opacity=".7"/>
""")

# through-line · the red thread that runs down the spine
SYMBOLS["thread"] = ("0 0 1400 220", """
  <path d="M10 110 C160 40 300 180 450 110 C600 40 740 180 890 110
           C1040 40 1180 180 1330 110 C1360 96 1382 90 1395 92"
        stroke-width="15"/>
  <path d="M10 110 C160 40 300 180 450 110 C600 40 740 180 890 110
           C1040 40 1180 180 1330 110 C1360 96 1382 90 1395 92"
        stroke-width="6" opacity=".45"/>
""" )

for key, (vb, body) in SYMBOLS.items():
    (OUT / f"{key}.svg").write_text(HEAD.format(vb=vb) + body + END, encoding="utf-8")
    print("wrote", OUT / f"{key}.svg")

print(f"{len(SYMBOLS)} symbols written.")
