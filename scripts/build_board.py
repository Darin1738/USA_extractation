#!/usr/bin/env python3
"""
Group 4 · HIST 350 · The Name Changes / The Function Does Not
SCRAPBOOK v2 board builder.

Builds the 24x36 poster HTML, then renders:
  out/board_v2.png       2400 x 3600 (100 ppi)
  out/board_v2@150.png   3600 x 5400 (150 ppi)
  out/board_v2.pdf       24 x 36 in, vector text

Aesthetic: aged-paper scrapbook. Full-bleed collage of clippings, tape,
stamps and original Pan-African / freedom / revolution / peace-war symbols,
with the panel copy sitting on torn clipping cards layered over it.
No large empty whitespace — every gutter carries something.

Run:  /tmp/opencode/venv/bin/python scripts/build_board.py
      /tmp/opencode/venv/bin/python scripts/build_board.py --html-only
"""
from __future__ import annotations

import html
import json
import sys
from pathlib import Path
from urllib.parse import quote as urlquote

ROOT = Path(__file__).resolve().parent.parent
SYM = ROOT / "assets" / "symbols"
OUT = ROOT / "out"
OUT.mkdir(exist_ok=True)

# --------------------------------------------------------------------------
# layout constants
# --------------------------------------------------------------------------
W, H = 2400, 3600
MARGIN = 64
BANNER_Y, BANNER_H = 64, 500
ROW_Y = [632, 1235, 1838, 2441]
PANEL_H = 523
LEFT_X, RIGHT_X, PANEL_W = 64, 1352, 984
P10_Y, P10_H = 3040, 496

# --------------------------------------------------------------------------
# panel content  (v2 — shorter, punchier copy)
# --------------------------------------------------------------------------
P = {}

P["p1"] = dict(
    num="01", tag="THESIS", era="1619 – PRESENT · SIX ERAS OF CONTROL",
    title="THE NAME CHANGES. THE FUNCTION DOES NOT.",
    arg="Slavery was abolished. The logic of controlling and extracting from Black bodies was not.",
    facts=("<b>Black Codes</b> criminalized Black freedom. <b>Convict leasing</b> rented prisoners out. "
           "<b>Mass incarceration</b> built the world's largest prison system. <b>Algorithmic bias</b> hides the same judgment in code."),
    notes=[
        "The thesis: “Slavery was abolished, but the logic of controlling and extracting from Black bodies was rebuilt in new legal form.”",
        "Six areas of control — slavery, Black Codes, convict leasing, Jim Crow, mass incarceration, algorithmic control — run on three pillars: profit from Black bodies; convict leasing → prison labor; plantation → algorithm.",
        "Opening question to hold: if slavery was abolished in 1865, why did prisons become overrun with Black bodies? The board answers it.",
    ],
    questions=[
        "What does it mean for a system to survive its own abolition?",
        "What connects a plantation, a prison cell, and a risk score?",
    ],
    sources=[
        "Thirteenth Amendment, U.S. Constitution (Section 1).",
        "Emancipation Proclamation (1863), U.S. National Archives.",
        "Group 4 blueprint & project binder (panel architecture, thesis).",
    ],
    images=[
        dict(f="emancipation_proclamation.jpg", cap="Emancipation Proclamation, 1863 — freedom with a clause attached.", fit=True),
        dict(f="slave_atlantic_trade_slave_ship.jpg", cap="The Middle Passage: forced migration as the first container of the system."),
    ],
)

P["p2"] = dict(
    num="02", tag="ERA 01", era="1619–1865 · CHATTEL SLAVERY",
    title="SLAVERY & THE RACIAL ORDER",
    arg="Built to extract labor from Black bodies — and deny their humanity.",
    facts=("Enslaved people were deemed property, not persons: a fabricated rationale that kept the economic engine running. "
           "<b>Counterpoint:</b> only a tiny share of Africans in the Atlantic trade landed in North America."),
    stat=dict(v="12.5M", l="forced into the Atlantic trade · <b>~10.7M</b> disembarked alive in the Americas"),
    images=[
        dict(f="slave_atlantic_trade_slave_ship.jpg", cap="A slave ship under sail — the Middle Passage."),
        dict(f="Slave Voyages Pie Chart.png", cap="Where captives were carried. Source: SlaveVoyages.", fit=True),
    ],
    question="If most enslaved Africans went elsewhere, why focus on the U.S.?",
    source="SlaveVoyages · PBS, “How Many Slaves Landed in the U.S.?”",
    notes=[
        "Slavery racialized labor and deemed people property — denying personhood to keep the economic engine running.",
        "~12.5 million Africans were forced into the Atlantic trade; ~10.7 million disembarked alive in the Americas.",
        "Use the counterpoint honestly: only a tiny share landed in North America. What was built here was not only numbers — it was a racial order, the blueprint every later panel runs on.",
    ],
    questions=[
        "If most enslaved Africans went elsewhere, why focus on the U.S.?",
        "How did being called property become a legal identity?",
    ],
    sources=[
        "SlaveVoyages, “Voyages: The Trans-Atlantic Slave Trade Database.”",
        "PBS, “How Many Slaves Landed in the U.S.?”",
    ],
)

P["p3"] = dict(
    num="03", tag="THE HINGE", era="1865 · ABOLITION & EXCEPTION",
    title="THE 13TH AMENDMENT LOOPHOLE",
    arg="Emancipation arrived with an exception written into it.",
    facts=("The clause closes one door and leaves another open. Read it slowly — especially the comma before "
           "<b>“except.”</b> This is the hinge of the whole board."),
    quote=dict(
        q="Neither slavery nor involuntary servitude, except as a punishment for crime … shall exist within the United States.",
        c="U.S. Const. amend. XIII, § 1 (1865)",
    ),
    images=[dict(f="emancipation_proclamation.jpg", cap="Emancipation Proclamation, 1863. Freedom — with a clause attached.", fit=True)],
    question="What does an exception do to a promise?",
    source="U.S. Constitution, amend. XIII · National Archives",
    notes=[
        "The 13th Amendment abolished slavery — with a deliberate exception built in. At first glance reasonable; in practice used to perpetuate the exploitation of labor.",
        "Read the clause aloud and slow down on “except as a punishment for crime.” This panel is the hinge: it closes era one and opens era two.",
    ],
    questions=[
        "What does an exception do to a promise?",
        "Who benefits from leaving that door open?",
    ],
    sources=[
        "U.S. Constitution, amend. XIII, § 1.",
        "National Archives, Emancipation Proclamation (1863).",
    ],
)

P["p4"] = dict(
    num="04", tag="ERA 02", era="1865–66 · RECONSTRUCTION",
    title="BLACK CODES & VAGRANCY",
    arg="Freedom was re-criminalized. Black life became presumptively illegal.",
    facts=("Unemployment, loitering, migration became crimes. Any infraction — even an unpaid fine — rolled into forced labor. "
           "<b>Same machine, new form.</b>"),
    quote=dict(
        q="…convicted of petty crimes, like walking on the grass, vagrancy, and stealing food… Even those declared innocent were often placed in this system when they could not pay their court fees.",
        c="Newspaper account, Library of Congress — date to verify",
    ),
    images=[
        dict(f="imagery.jpg", cap="Newspaper: “free as air” — and “spot every leading Radical negro.”", fit=True),
        dict(f="one_vote_less.jpg", cap="“One Vote Less.” Richmond Whig — freedom met with subtraction.", fit=True),
    ],
    question="Can you be free if your freedom is a crime?",
    source="Studies in American Political Development (Cambridge UP) · LOC, Chronicling America (date under review)",
    notes=[
        "Black Codes criminalized unemployment, loitering and migration — the re-criminalization of freedom.",
        "By leaving “criminals” out of the amendment, the system only had to make Black people the majority of criminals. Any infraction — even an unpaid fine — rolls into forced labor.",
        "Forward connection: fines, fees and cash bail are the same mechanism still running.",
    ],
    questions=[
        "Can you be free if your freedom is a crime?",
        "What happens when an unpaid fine becomes labor?",
    ],
    sources=[
        "Studies in American Political Development, “Spawn of Slavery.”",
        "Library of Congress, Chronicling America (date under review; verify scan).",
    ],
    note="Verification flag: the newspaper's 1961 date should be checked against the LOC scan before the presentation.",
)

P["p5"] = dict(
    num="05", tag="ERA 03", era="1868–1940s · “SLAVERY BY ANOTHER NAME”",
    title="CONVICT LEASING",
    arg="The plantation was rebuilt behind prison walls — and it turned a profit.",
    facts=("States leased Black convicts to plantations, mines and railroads. Brutal mortality produced profit for the state and for industry. "
           "<b>By 1900</b> Black people were a large majority of Southern convicts."),
    stat=dict(v="~73%", l="estimated share of Alabama's state revenue from convict leasing, late 1800s (approx.)"),
    images=[
        dict(f="moneyreward.jpg", cap="Reward poster: five escaped convicts from the Chattahoochee brick works.", fit=True),
        dict(f="african_american_convicts_w_shovels.jpg", cap="Convict laborers with shovels, early 1900s."),
    ],
    question="What is the difference between owning a person and renting their punishment?",
    source="Blackmon, Slavery by Another Name · Alabama Archives · LOC, Inside Adams",
    notes=[
        "States leased convicts to plantations, railroads and mines — so the state and emerging American industry both profited from Black bodies.",
        "Blackmon showed how Southern governments arrested Black Americans on fabricated or minor charges and “leased” their bodies as forced labor.",
        "The figure is an estimate: ~73% of Alabama's state revenue in the late 1800s (no exact figure survives).",
    ],
    questions=[
        "Who got paid?",
        "What is the difference between owning a person and renting their punishment?",
    ],
    sources=[
        "Douglas A. Blackmon, Slavery by Another Name.",
        "Alabama Department of Archives & History, 1846 lease act.",
        "Library of Congress, Inside Adams; NMAAHC Searchable Museum.",
    ],
)

P["p6"] = dict(
    num="06", tag="ERA 04", era="1890s–1960s · JIM CROW",
    title="THE ACCUSATION",
    arg="Criminal accusation became the justification for racial terror.",
    facts=("The “Black rapist” myth — manufactured in media and politics — justified chain gangs, racialized policing and lynching. "
           "No trial. No evidence. Just the charge. <b>Graphic photographs omitted by design.</b>"),
    stat=dict(v="~4,400", l="documented racial-terror lynchings of Black people, <b>1877–1950</b> (EJI)"),
    images=[
        dict(f="fountain_seg.jpg", cap="Segregated fountain: “WHITE” / “COLORED.”"),
        dict(f="letohatchee.jpg", cap="EJI marker: lynching in Letohatchee, Alabama, 1900."),
    ],
    question="Why did the accusation matter more than the evidence?",
    source="EJI, Lynching in America · NAACP, The Burning at Dyersburg, 15 Crisis (1917)",
    notes=[
        "The “Black rapist” myth gave cover to racial terror, chain gangs and racialized policing — lynching on nothing more than an accusation.",
        "Ida B. Wells and NAACP investigations show the accusation doing the work of evidence. From 1877–1950, EJI documents ~4,400 racial-terror lynchings.",
        "Handle with restraint: let the facts carry the weight; do not sensationalize.",
    ],
    questions=[
        "Why did the accusation matter more than the evidence?",
        "How does a lie become law?",
    ],
    sources=[
        "Equal Justice Initiative, Lynching in America.",
        "“The Burning at Dyersburg,” 15 Crisis 178–83 (1917).",
        "Ida B. Wells, Southern Horrors.",
    ],
    note="Content note: the board intentionally uses a memorial marker and a segregation sign rather than photographs of victims.",
)

P["p7"] = dict(
    num="07", tag="ERA 05", era="1971–PRESENT · WAR ON DRUGS", cls="sz-s",
    title="LAW &amp; ORDER → MASS INCARCERATION",
    arg="“Law and order” became the new racial control.",
    facts=("1971 War on Drugs. 1986 Anti-Drug Abuse Act (100:1 crack-to-cocaine). 1994 Crime Bill. Mandatory minimums. Selective enforcement."
           "<span class='pq'>“We could arrest their leaders, raid their homes… Did we know we were lying about the drugs? Of course we did.” "
           "— John Ehrlichman (attributed/reported; disputed)</span>"),
    stat=dict(v="~5% / ~25%", l="U.S. share of world population vs. world prisoners · Black people: <b>~13%</b> of the population, <b>37%</b> of the incarcerated"),
    images=[
        dict(f="mlk_arrested.jpg", cap="Dr. King arrested — the “law and order” era."),
        dict(f="prsion_blck_vs_white.png", cap="Black vs. white incarceration. Source: Prison Policy Initiative.", fit=True),
    ],
    question="Can a law be race-neutral and still racist?",
    source="EJI · Prison Policy Initiative · ACLU-WA · World Prison Brief",
    notes=[
        "Nixon declared war on drugs — fought disproportionately in communities of color through selective enforcement. Then the 1986 100:1 crack-to-cocaine disparity, the 1994 Crime Bill, mandatory minimums.",
        "Quote Ehrlichman but flag it: widely cited, attribution disputed — present as reported, not proven.",
        "~5% of the world's population lives in the U.S.; we hold roughly a quarter of the world's prisoners. Black people are ~13% of the population and 37% of the incarcerated.",
    ],
    questions=[
        "Can a law be race-neutral and still racist?",
        "What did calling drugs ‘public enemy #1’ distract the public from?",
    ],
    sources=[
        "EJI, “Nixon's War on Drugs.”",
        "Prison Policy Initiative; ACLU of Washington; World Prison Brief.",
        "Anti-Drug Abuse Act (1986); Violent Crime Control and Law Enforcement Act (1994).",
    ],
)

P["p8"] = dict(
    num="08", tag="ERA 06", era="2000s–PRESENT · THE ALGORITHM", cls="p8",
    title="PLANTATION → ALGORITHM",
    arg="The overseer's variable judgment became the algorithm's baked-in bias.",
    facts=("COMPAS recidivism scoring, predictive policing, facial recognition. The bias moves from a person to a system that hides behind math — "
           "<b>race-neutral on paper, not in outcome.</b>"),
    stats=[
        dict(v="2×", l="Black defendants flagged high-risk at twice the rate of white defendants <b>(ProPublica, 2016)</b>"),
        dict(v="10–100×", l="higher facial-recognition false positives for Black and Asian faces <b>(NIST, 2019)</b>"),
    ],
    images=[
        dict(f="risk_score_p1_1.png", cap="COMPAS-style risk assessment — page 1.", fit=True),
        dict(f="risk_score_p1_2.png", cap="COMPAS-style risk assessment — page 2.", fit=True),
    ],
    question="If the algorithm cannot see race, how does it reproduce racism?",
    source="ProPublica, “Machine Bias” (2016) · NIST FRVT (2019)",
    notes=[
        "Centuries of manufactured discrimination have been adopted into algorithms that, at scale, only exacerbate the problem.",
        "COMPAS tells a court how likely a defendant is to reoffend. ProPublica (2016) found Black defendants flagged high-risk at 2× the rate of white defendants. NIST (2019) found face-recognition false positives 10–100× more likely for Black and Asian faces.",
        "The plantation becomes the algorithm. The overseer could be questioned; the score looks neutral and is harder to appeal.",
    ],
    questions=[
        "If the algorithm cannot see race, how does it reproduce racism?",
        "Who is accountable when the code is wrong?",
    ],
    sources=[
        "ProPublica, “Machine Bias” (2016).",
        "NIST, Face Recognition Vendor Test (2019).",
        "Flores, Bechtel & Lowenkamp, Federal Probation (2016).",
    ],
)

P["p9"] = dict(
    num="09", tag="DIASPORA", era="BRAZIL & ARGENTINA · 1871–PRESENT", cls="sz-s",
    title="FREE, BUT BOUND",
    arg="The U.S. is one example of a Diaspora pattern: emancipation produces new coercion.",
    facts=("Brazil's <b>Law of the Free Womb</b> (1871) “freed” newborns but bound them to their masters until 21. "
           "Argentina's <b>liberto</b> system conditioned freedom on military service. Afro-Argentine history was written out."),
    stat=dict(v="21", l="years Brazil's “free” children remained bound to their masters"),
    images=[
        dict(f="afroargentines_playing_candombe_porteno_near_bonfire_of_sain_john.jpg", cap="Afro-Argentine candombe, Buenos Aires."),
        dict(f="Slave Voyages Map.png", cap="The Atlantic system, 1514–1866. Source: SlaveVoyages.", fit=True),
    ],
    question="What does “free” mean when freedom is conditioned?",
    source="Phillips, The African Diaspora Experience · Cambridge UP · African Arguments",
    notes=[
        "Step back from the U.S.: Brazil's Law of the Free Womb (1871) “freed” newborns but bound them to their masters until 21 — a “new form of slavery.” The Manumission Fund liberated 20,000+ people.",
        "In Argentina the liberto system conditioned freedom on military service, then kept extending it, while Afro-Argentine contributions were written out of national memory.",
        "The U.S. is one example of the pattern: emancipation doesn't end coercion, it produces new forms of it.",
    ],
    questions=[
        "Is the U.S. an exception or an example?",
        "What does ‘free’ mean when freedom is conditioned?",
    ],
    sources=[
        "Glen O. Phillips, The African Diaspora Experience, pp. 119–174.",
        "Cambridge UP, Freedoms Captives: Time of Gradual Emancipation.",
        "African Arguments, “The Erased Protagonists.”",
    ],
)

P["p10"] = dict(
    num="10", tag="RESISTANCE / MEMORY",
    era="1791–PRESENT · RESISTANCE & ERASURE",
    title="SAME STRUGGLE. NEW TERRAIN.",
    arg="Every system of control met organized resistance — and the fight over memory is the latest front.",
    stat=dict(v="~800", l="people freed in one night · Combahee River raid, July 1863"),
    question="Whose memory is kept, and whose is erased?",
    source="Zinn Education Project · National Archives, Tulsa · UPenn, MOVE · Digital Howard, North Star",
    images=[
        dict(f="escaped_enslaved_people_from_plantation_virgiana.jpg", cap="Escaped enslaved people, Virginia — the first front."),
    ],
    resistance=[
        ("1791", "HAITI", "Toussaint Louverture; the revolution that ended slavery in 1804."),
        ("1847", "NORTH STAR", "Douglass: “Right is of no sex — Truth is of no color.”"),
        ("1863", "COMBAHEE", "Tubman's raid frees ~800 people in one night."),
        ("1878", "FIREBURN", "Queen Mary Thomas, Agnes and Matilda lead the uprising."),
    ],
    memory=[
        ("1921", "TULSA", "~35 blocks burned; 100–300+ killed (official count 36); erased for decades."),
        ("1985", "MOVE", "Philadelphia bombs a home from the air — and the record is contested."),
    ],
    notes=[
        "This story isn't only what was done to Black people — every system on this board was met with organized resistance.",
        "Combahee River raid, July 1863: Tubman freed ~800 people in one night. The 1878 Fireburn: Queens Mary Thomas, Agnes and Matilda led workers burning sugar plantations. Haiti, 1791–1804: the only revolution that ended in a free nation. Douglass's North Star, 1847: “Right is of no sex — Truth is of no color.”",
        "Memory is the front line now. Tulsa, 1921: a white mob destroyed Greenwood, “Black Wall Street,” over a lie; ~35 blocks burned, ~10,000 left homeless, 100–300+ killed though the official count was 36. Then the second erasure — claims denied, records dropped, mass graves still being searched for.",
        "MOVE, 1985: a home bombed from the air by its own city government. Same pattern — the record gets cleaned up after the bodies do.",
        "Closing: the name keeps changing; the function does not. “When the law stopped saying ‘Black,’ did it stop acting on race?” — “What do we owe the record?”",
    ],
    questions=[
        "What does it mean that every system of control met organized resistance?",
        "Whose memory is kept, and whose is erased?",
        "When the law stopped saying ‘Black,’ did it stop acting on race?",
        "What do we owe the record?",
    ],
    sources=[
        "Zinn Education Project, Harriet Tubman's Combahee River raid.",
        "National Archives, Tulsa Race Massacre materials.",
        "UPenn Collaborative History, MOVE / Osage Avenue; Digital Howard, North Star (1847).",
    ],
    note="Tulsa detail: the massacre, the cover-up, and the ongoing search for mass graves.",
)

# --------------------------------------------------------------------------
# symbol metadata  (v2 — Pan-African / freedom / revolution / peace-war)
# --------------------------------------------------------------------------
SYMBOLS = {
    "globe": dict(num="01", name="PAN-AFRICAN GLOBE", era="THE DIASPORA",
        meaning="One people, scattered across the world — and still connected.",
        notes=["The globe is centred on the African continent, with the Diaspora routes crossing it. It frames P9: the U.S. is one node, not the whole story."],
        questions=["Is the U.S. an exception, or an example?"]),
    "fist": dict(num="02", name="THE RAISED FIST", era="REVOLUTION & RESISTANCE",
        meaning="Refusal. The body as a weapon that will not be owned.",
        notes=["The raised fist is the oldest gesture of resistance — from slave revolts to the Black Power salute. It answers the board's punitive symbols: control is met with refusal."],
        questions=["What does it mean that every system of control met resistance?"]),
    "broken-chain": dict(num="03", name="THE BROKEN CHAIN", era="FREEDOM",
        meaning="Freedom in any form: the link snapped, not the person freed by permission.",
        notes=["The chain breaks at the centre. Freedom was not granted from above — it was seized. The remaining links recall what was endured."],
        questions=["Who actually ended slavery — the law, or the people who ran?"]),
    "torch": dict(num="04", name="THE TORCH", era="FREEDOM & REVOLUTION",
        meaning="Light carried forward; the flame passed between generations.",
        notes=["The torch is freedom actively held, not passively given. It links Haiti, the North Star press, Combahee and the modern front."],
        questions=["Who carries the light when the record tries to go dark?"]),
    "kente": dict(num="05", name="KENTE PATTERN", era="PAN-AFRICANISM",
        meaning="African knowledge, craft and identity that survived the crossing.",
        notes=["An original geometric pattern inspired by kente/Adinkra textile structure. It signals that the Diaspora did not begin empty — it carried culture."],
        questions=["What did the Diaspora carry that no auction could sell?"]),
    "dove": dict(num="06", name="THE DOVE", era="PEACE",
        meaning="Peace — and the cost of the wars fought to reach it.",
        notes=["Peace is not the absence of conflict; it is a claim made after violence. The dove sits beside the barbed wire on purpose."],
        questions=["Peace for whom, and paid for by whom?"]),
    "megaphone": dict(num="07", name="THE MEGAPHONE", era="PROTEST & VOICE",
        meaning="Resistance organized out loud — the demand to be heard.",
        notes=["From street protest to the press to the record: the megaphone is voice as power. It is the resistance to every attempt to silence the story."],
        questions=["Whose voice gets amplified, and whose gets erased?"]),
    "barbed-wire": dict(num="08", name="BARBED WIRE", era="WAR & OPPRESSION",
        meaning="War, enclosure and confinement — the architecture of control.",
        notes=["Barbed wire fenced the plantation, the prison camp and the border. It is the counterweight to peace and freedom across the board."],
        questions=["Who decides where the wire goes?"]),
    "poppy": dict(num="09", name="THE POPPY", era="REMEMBRANCE",
        meaning="Peace and remembrance for those the record tried to forget.",
        notes=["The poppy remembers the dead of war and terror — including Tulsa, the lynching victims, and the unnamed buried in mass graves."],
        questions=["What do we owe the record?"]),
    "open-hands": dict(num="10", name="OPEN HANDS", era="LIBERATION",
        meaning="Freedom released, not hoarded — the bird let go.",
        notes=["Open hands release the bird: freedom in any form, freely given. It closes the board by answering the chain."],
        questions=["What does freedom look like when it isn't conditional?"]),
    "thread": dict(num="—", name="THE RED THREAD", era="THE THROUGH-LINE",
        meaning="Profit → punishment → prediction.",
        notes=["The red thread runs down the spine: the same pillars across six eras. The name changes. The function does not."],
        questions=["What connects a plantation, a prison cell, and a risk score?"]),
}

# --------------------------------------------------------------------------
# scrapbook background
#   symbols     (key, x, y, w, h, rotate, class)
#   clippings   (x, y, w, h, rotate, tone, class)
#   tapes       (x, y, w, rotate, tone)
#   stamps      (x, y, rotate, tone, label)
#   bgimgs      (file, x, y, w, h, blend)
# --------------------------------------------------------------------------
COLLAGE = [
    ("thread",      -160, 1090, 2720, 420, -1.2, "blood faint"),
    ("globe",       -170,  120,  720, 720,  -9,  "green"),
    ("fist",        1980,   90,  520, 520,   8,  "blood"),
    ("broken-chain", -150,  760,  700, 640,  -12, ""),
    ("dove",         880,  120,  620, 500,   6,  "faint"),
    ("torch",        2050,  820,  430, 560,  -6, ""),
    ("kente",        240,  680,  620, 560,   3,  "green"),
    ("megaphone",   1420,  980,  760, 600,  -5, ""),
    ("barbed-wire",  -120, 1660,  900, 480,  -3, "faint"),
    ("poppy",         40, 2450,  560, 660,   4,  "blood"),
    ("open-hands",  1900, 2470,  760, 600,  -4, "green faint"),
    ("globe",        640, 3120,  680, 680,   7,  "blood faint"),
    ("thread",       -160, 2900, 2720, 420,   1.4,"blood"),
    ("fist",        1650, 2050,  420, 420,  -8,  "green faint"),
    ("broken-chain",  980, 1520,  380, 340,  -10, "blood faint"),
    ("megaphone",     980, 2400,  420, 330,   6,  "green faint"),
    ("dove",         1000,  820,  380, 300,  -7,  "blood faint"),
    ("poppy",        1560, 1560,  340, 400,   5,  "green faint"),
    ("globe",        1880, 1680,  420, 420,  -4,  "blood faint"),
    ("torch",         960, 3140,  340, 440,   6,  "green faint"),
]

CLIPPINGS = [
    (1320,  300, 360, 220,  -6, "red"),
    (140,  1050, 300, 190,   5, "green"),
    (2050, 1500, 300, 200,  -4, "gold"),
    (140,  2280, 320, 200,   6, "black"),
    (1360, 3080, 300, 190,  -5, "red"),
    (740,  1120, 240, 150,   8, "news"),
    (1740, 1880, 260, 160,  -7, "green"),
    (120,  3160, 300, 180,   4, "gold"),
    (2060, 3160, 280, 180,  -6, "news"),
    (430,   250, 300, 200,  -5, "green"),
    (2000,  980, 280, 190,   7, "red"),
    (560,  2200, 280, 180,  -8, "gold"),
    (1980, 2860, 300, 200,   5, "black"),
    # v2.1 — fill centre column + top-right + gutters (kill dead space)
    (1080,  150, 300, 210,   4, "news"),
    (1120,  480, 260, 180,  -6, "gold"),
    (1080,  820, 280, 190,   5, "black"),
    (1100, 1180, 260, 170,  -5, "green"),
    (1080, 1560, 280, 190,   6, "news"),
    (1090, 1960, 260, 180,  -4, "red"),
    (1080, 2340, 280, 190,   5, "gold"),
    (1100, 2720, 260, 180,  -6, "black"),
    (1080, 3120, 280, 190,   4, "green"),
    (1700, 1450, 240, 160,   7, "news"),
    (1620, 1000, 240, 160,  -6, "gold"),
    (1660, 2480, 240, 160,   6, "green"),
    (700,  1620, 260, 180,  -7, "gold"),
    (620,  2540, 260, 180,   5, "news"),
    (1880,  700, 260, 180,  -5, "black"),
    (2070, 1720, 240, 170,   6, "red"),
    (2010, 3050, 240, 160,  -7, "green"),
]

TAPES = [
    (120,  560, 180, -8, "gold"),
    (2160, 1080, 160,  7, "green"),
    (120,  1780, 180,  5, "red"),
    (2160, 2280, 170, -6, "gold"),
    (120,  2980, 170,  6, "green"),
    (1180,  470, 150, -9, "red"),
    (1180, 2960, 160,  8, "gold"),
    (620,   690, 150,  4, "green"),
    (1660, 2960, 150, -5, "red"),
    (1090,  380, 200, -12, "green"),
    (1100, 1700, 190, 10, "red"),
    (1100, 2660, 190, -9, "gold"),
    (1720, 1230, 170, 8, "black"),
    (1560, 2020, 170, -10, "green"),
    (1980,  860, 150, 12, "red"),
    (1560, 3260, 180, -8, "gold"),
]

STAMPS = [
    (1180,  120, -12, "red", "GROUP 4 · HIST 350"),
    (2140,  560,  9, "green", "RESIST · REMEMBER"),
    (120,  2400,  -7, "gold", "1619 → PRESENT"),
    (1180, 3480,   5, "red", "NAME CHANGES · FUNCTION DOES NOT"),
    (1240, 1180,  10, "green", "FREEDOM"),
    (40,   1700,  -6, "green", "PAN-AFRICAN"),
    (2090, 2660,   8, "red", "REMEMBER TULSA"),
    (600,  3060,  -9, "gold", "NO JUSTICE · NO PEACE"),
    (1090,  980, -14, "black", "ACCUMULATION BY DISPOSSESSION"),
    (1130, 2180,  11, "red", "THE RECORD IS THE FRONT"),
    (1080, 1440,  -8, "green", "FREE · BUT BOUND"),
    (2050,  720, -10, "gold", "STILL REBUILDING"),
]

BG_IMAGES = [
    ("slave_atlantic_trade_slave_ship.jpg", 1500, 60, 860, 470, "screen"),
    ("angola_prison_guard_tower.png", 2140, 1900, 300, 560, ""),
    ("ChatahoocheebricksEnglishWeb-768x576.jpg", -60, 1300, 520, 390, ""),
    ("fountain_seg.jpg", 2160, 2500, 300, 420, ""),
    ("one_vote_less.jpg", -40, 2620, 300, 380, ""),
    ("mlk_arrested.jpg", 100, 480, 300, 380, ""),
    ("prsion_blck_vs_white.png", 1990, 1160, 320, 260, ""),
    ("african_american_convicts_w_shovels.jpg", 1980, 2140, 320, 240, ""),
    ("escaped_enslaved_people_from_plantation_virgiana.jpg", 120, 1980, 340, 240, "screen"),
]

# --------------------------------------------------------------------------
# render helpers
# --------------------------------------------------------------------------
def media_src(fname: str) -> str:
    return "../media/" + urlquote(fname)


def esc(s: str) -> str:
    return html.escape(s, quote=True)


def figure(im: dict) -> str:
    cls = "fit" if im.get("fit") else ""
    return (
        f'<figure class="{cls}"><img src="{media_src(im["f"])}" alt="{esc(im["cap"])}">'
        f'<figcaption>{esc(im["cap"])}</figcaption></figure>'
    )


def statblock(p: dict) -> str:
    if p.get("quote"):
        q = p["quote"]
        return f'<blockquote class="quote"><q>{q["q"]}</q><cite>{esc(q["c"])}</cite></blockquote>'
    if p.get("stats"):
        inner = "".join(
            f'<div class="su"><div class="stat-v">{s["v"]}</div><div class="stat-l">{s["l"]}</div></div>'
            for s in p["stats"]
        )
        return f'<div class="p-stat duo">{inner}</div>'
    s = p["stat"]
    cls = " sm" if len(s["v"]) > 12 else ""
    return f'<div class="p-stat"><div class="stat-v{cls}">{s["v"]}</div><div class="stat-l">{s["l"]}</div></div>'


def panel(p: dict) -> str:
    style = f"left:{p['x']}px;top:{p['y']}px;width:{p['w']}px;height:{p['h']}px;"
    cls = "panel " + p.get("cls", "")
    return f"""
<article class="{cls.strip()}" data-panel="{p['id']}" tabindex="0" role="button" aria-label="Open panel {p['num']}: {esc(p['title'])}" style="{style}">
  <span class="tape tl"></span><span class="tape br"></span>
  <header class="p-head">
    <div class="era">{p['era']}</div>
    <div class="pnum"><b>{p['num']}</b><span>/ 10</span></div>
  </header>
  <div class="p-main">
    <h2 class="p-title">{p['title']}</h2>
    <p class="p-arg">{p['arg']}</p>
    <p class="p-facts">{p['facts']}</p>
  </div>
  {statblock(p)}
  <div class="p-media">{''.join(figure(im) for im in p['images'])}</div>
  <footer class="p-foot">
    <p class="ask"><span class="asktag">ASK</span>{esc(p['question'])}</p>
    <p class="src">SRC · {esc(p['source'])}</p>
  </footer>
  <span class="open-hint">OPEN FILE ↗</span>
</article>"""


def banner(p: dict) -> str:
    return f"""
<section class="banner" data-panel="p1" tabindex="0" role="button" aria-label="Open the thesis banner">
  <div class="b-left">
    <div class="kicker"><span class="dot"></span>HIST 350 · GROUP 4 · MORGAN STATE UNIVERSITY</div>
    <h1 class="b-title"><span>THE NAME CHANGES.</span><span>THE <em class="thin">FUNCTION</em> DOES NOT.</span></h1>
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


def p10(p: dict) -> str:
    res = "".join(
        f'<div class="res-item"><div class="y">{y}</div><div class="t">{t}</div><div class="d">{d}</div></div>'
        for y, t, d in p["resistance"]
    )
    mem = "".join(
        f'<div class="mem-item"><div class="y">{y}</div><div class="t">{t}</div><div class="d">{d}</div></div>'
        for y, t, d in p["memory"]
    )
    media = "".join(figure(im) for im in p["images"])
    return f"""
<article class="panel wide" data-panel="p10" tabindex="0" role="button" aria-label="Open panel 10: resistance and memory">
  <span class="tape tl"></span><span class="tape br"></span>
  <header class="p-head">
    <div class="era">{p['era']}</div>
    <div class="pnum"><b>{p['num']}</b><span>/ 10</span></div>
  </header>
  <div class="w-body">
    <div class="w-left">
      <h2 class="p-title">{p['title']}</h2>
      <p class="p-arg">{p['arg']}</p>
      <div class="p-stat" style="border-top:0;min-height:0;padding-top:4px;margin-top:2px">
        <div class="stat-v">{p['stat']['v']}</div>
        <div class="stat-l">{p['stat']['l']}</div>
      </div>
      <div class="w-close">
        <div class="closing">THE NAME CHANGES. <span>THE FUNCTION DOES NOT.</span></div>
        <p class="ask"><span class="asktag">ASK</span>{esc(p['question'])}</p>
        <p class="src">SRC · {esc(p['source'])}</p>
      </div>
    </div>
    <div class="res">
      <div class="res-block"><h3>Resistance</h3><div class="res-grid">{res}</div></div>
      <div class="midline"><span>MEMORY IS THE LATEST FRONT</span></div>
      <div class="mem-block"><h3>Memory / erasure</h3><div class="mem-grid">{mem}</div></div>
    </div>
    <div class="w-media">{media}</div>
  </div>
</article>"""


def collage() -> str:
    out = []
    for x, y, w, h, rot, tone in CLIPPINGS:
        out.append(
            f'<div class="clip {tone}" style="left:{x}px;top:{y}px;width:{w}px;height:{h}px;transform:rotate({rot}deg)"></div>'
        )
    for f, x, y, w, h, blend in BG_IMAGES:
        out.append(
            f'<div class="bgimg {blend}" style="left:{x}px;top:{y}px;width:{w}px;height:{h}px;'
            f'background-image:url(\'{media_src(f)}\')"></div>'
        )
    for key, x, y, w, h, rot, cls in COLLAGE:
        svg = (SYM / f"{key}.svg").read_text()
        label = esc(SYMBOLS[key]["name"])
        out.append(
            f'<div class="sym {cls}" data-sym="{key}" title="{label}" '
            f'style="left:{x}px;top:{y}px;width:{w}px;height:{h}px;transform:rotate({rot}deg)">{svg}</div>'
        )
    for x, y, w, rot, tone in TAPES:
        out.append(
            f'<div class="scr-tape {tone}" style="left:{x}px;top:{y}px;width:{w}px;transform:rotate({rot}deg)"></div>'
        )
    for x, y, rot, tone, label in STAMPS:
        out.append(
            f'<div class="stamp {tone}" style="left:{x}px;top:{y}px;transform:rotate({rot}deg)">{esc(label)}</div>'
        )
    return '<div class="bg" aria-hidden="true">' + "".join(out) + "</div>"


def spine() -> str:
    years = [(1619, 66), (1865, 576), (1868, 726), (1890, 1026), (1971, 1526), (2000, 1856), (2025, 2226)]
    yrs = "".join(f'<div class="yr" style="top:{top}px">{year}</div>' for year, top in years)
    return f"""
<div class="spine" aria-hidden="true">
  <div class="rail"></div>
  {yrs}
  <div class="pillar p1"><div class="num">I</div><div class="bar"></div><div class="lbl">PROFIT FROM BLACK BODIES</div></div>
  <div class="pillar p2"><div class="num">II</div><div class="bar"></div><div class="lbl">CONVICT LEASING <b>→</b> PRISON LABOR</div></div>
  <div class="pillar p3"><div class="num">III</div><div class="bar"></div><div class="lbl">PLANTATION <b>→</b> ALGORITHM</div></div>
</div>"""


KEYS = [
    ("globe", 86), ("fist", 470), ("broken-chain", 872), ("torch", 1300), ("kente", 1690),
    ("dove", 86), ("megaphone", 420), ("barbed-wire", 800), ("poppy", 1180), ("open-hands", 1560),
]


def symkeys() -> str:
    out = []
    for i, (key, x) in enumerate(KEYS):
        top = 582 if i < 5 else 1185
        s = SYMBOLS[key]
        out.append(
            f'<div class="symkey" data-symkey="{key}" style="left:{x}px;top:{top}px">'
            f'<b>{s["num"]}</b>{s["name"]}<i>↗</i></div>'
        )
    return "".join(out)


GAPNOTES = [
    (1786, 'PROFIT MOVES FROM THE PLANTATION <b>→</b> THE PRISON <b>→</b> THE PLATFORM'),
    (2389, 'THE LAW STOPS SAYING “BLACK.” <b>THE OUTCOMES DO NOT.</b>'),
    (2992, 'EVERY SYSTEM OF CONTROL MET ORGANIZED RESISTANCE'),
]


def gapnotes() -> str:
    return "".join(
        f'<div class="gapnote" style="left:64px;top:{y}px;width:2272px;justify-content:center">'
        f'<span class="ln"></span><span>{txt}</span><span class="ln"></span></div>'
        for y, txt in GAPNOTES
    )


def panel_positions() -> None:
    order = ["p2", "p3", "p4", "p5", "p6", "p7", "p8", "p9"]
    for i, pid in enumerate(order):
        row, col = divmod(i, 2)
        P[pid]["x"] = LEFT_X if col == 0 else RIGHT_X
        P[pid]["y"] = ROW_Y[row]
        P[pid]["w"] = PANEL_W
        P[pid]["h"] = PANEL_H
        P[pid]["id"] = pid


def build_html() -> str:
    panel_positions()
    board_json = {
        "panels": {pid: {k: v for k, v in P[pid].items() if k in
                         ("num", "tag", "era", "title", "arg", "facts", "stat", "stats",
                          "quote", "images", "question", "source", "notes", "questions",
                          "sources", "note")}
                   for pid in P},
        "symbols": SYMBOLS,
    }
    doc = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Group 4 · The Name Changes / The Function Does Not — 1619 to the Algorithm</title>
<link rel="stylesheet" href="assets/fonts/fonts.css">
<link rel="stylesheet" href="assets/fonts/caslon.css">
<link rel="stylesheet" href="assets/board.css">
</head>
<body>
<div class="holder"><div class="stage" id="stage">
  {collage()}
  {banner(P['p1'])}
  {''.join(panel(P[k]) for k in ('p2','p3','p4','p5','p6','p7','p8','p9'))}
  {p10(P['p10'])}
  {spine()}
  {symkeys()}
  {gapnotes()}
  <div class="footer">
    <div><b>GROUP 4</b> · DARIN L. WESLEY (LEADER) · COURTNEY FOWLKES (ASST.) · KIARRA M · ANTWAN POWELL · DEJUAN G · MAKAYLA PARSI · TAJA BRIDGES</div>
    <div class="r">SOURCES ON EACH PANEL · BIBLIOGRAPHY, MEDIA MANIFEST &amp; VERIFICATION LOG: GROUP 4 BINDER · AI USE: LAYOUT, TYPESETTING, SYMBOLS &amp; DRAFT ASSISTANCE; RESEARCH &amp; SOURCE CHECKS: GROUP 4</div>
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
def render(html_only: bool = False) -> None:
    (ROOT / "index.html").write_text(build_html(), encoding="utf-8")
    print("wrote", ROOT / "index.html")
    if html_only:
        return

    from playwright.sync_api import sync_playwright

    url = (ROOT / "index.html").as_uri()
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
                  kr.left < r.left - 1 || kr.top < r.top - 1)) {
                out.push((k.className && String(k.className).slice(0,40)) || k.tagName);
              }
            }
            return {id: el.dataset.panel || el.className, w: Math.round(r.width), h: Math.round(r.height),
                    scrollOverflow: el.scrollHeight - el.clientHeight,
                    out: [...new Set(out)].slice(0, 8)};
          });
          const images = [...document.images].map(i => ({src: i.getAttribute('src'),
            ok: i.complete && i.naturalWidth > 0, nw: i.naturalWidth}));
          return {panels, images, fonts: document.fonts.status,
                  dialog: document.querySelector('dialog') ? 'ok' : 'missing'};
        }""")
        print(json.dumps(qa, indent=2, ensure_ascii=False))

        page.screenshot(path=str(OUT / "board_v2.png"), full_page=True)
        print("wrote", OUT / "board_v2.png")

        hi = browser.new_page(viewport={"width": W, "height": H}, device_scale_factor=1.5)
        hi.goto(url, wait_until="load")
        hi.wait_for_function("document.fonts && document.fonts.status === 'loaded'")
        hi.wait_for_function("Array.from(document.images).every(i => i.complete)")
        hi.evaluate("document.body.classList.add('static'); document.documentElement.style.setProperty('--fit','1')")
        hi.wait_for_timeout(400)
        hi.screenshot(path=str(OUT / "board_v2@150.png"), full_page=True)
        print("wrote", OUT / "board_v2@150.png")

        page.pdf(path=str(OUT / "board_v2.pdf"), width="24in", height="36in",
                 margin={"top": "0", "bottom": "0", "left": "0", "right": "0"},
                 print_background=True, prefer_css_page_size=True)
        print("wrote", OUT / "board_v2.pdf")
        browser.close()


if __name__ == "__main__":
    render(html_only="--html-only" in sys.argv)
