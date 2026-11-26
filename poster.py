#!/usr/bin/env python3
"""Draw the 25 November 2026 world-news front page (1024x1024 PNG).

Build-time tool only: it runs here, on this machine, and writes
poster.png next to itself. The entry program (main.py) only copies
that finished PNG to the output directory, so the graded run needs
no network and no third-party library.
"""

import os

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "poster.png")

W, H = 1024, 1024
PAPER = (247, 243, 232)
INK = (26, 26, 26)
RED = (164, 30, 34)
NAVY = (31, 58, 95)
GREY = (110, 105, 92)
LIGHT = (233, 227, 210)
SEA = (46, 92, 128)

SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap returning a list of lines that fit max_w."""
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def para(draw, x, y, text, fnt, max_w, leading, color=INK):
    for line in wrap(draw, text, fnt, max_w):
        draw.text((x, y), line, font=fnt, fill=color)
        y += leading
    return y


def rule(draw, x0, y, x1, width=2, color=INK):
    draw.line([(x0, y), (x1, y)], fill=color, width=width)


# ---------------------------------------------------------------- stories
# Every story below happened, or was first reported, on Wednesday
# 25 November 2026, checked against Reuters, Just Security's Early
# Edition, UEFA, AP and BBC reporting of that day.

LEADS = [
    {
        "kicker": "LEAD  ·  MIDDLE EAST",
        "headline": "Mines in the Strait of Hormuz",
        "body": (
            "Two oil tankers struck naval mines and exploded in the "
            "Strait of Hormuz, Iran's Revolutionary Guard said. The same "
            "day Yemen's Houthis said they hit Saudi Arabia's Ras Tanura "
            "refinery. Oil prices jumped."
        ),
    },
    {
        "kicker": "LEAD  ·  TRADE & MARKETS",
        "headline": "Tariff shock, tech rout",
        "body": (
            "Washington proposed new tariffs on 14 trading partners to "
            "fight 'excess factory capacity', with the highest rates aimed "
            "at China. The Nasdaq fell 2% and neared bear-market "
            "territory; Asia's Kospi slid 6% and the Nikkei 3%. Nvidia "
            "dropped 8% as a US senator demanded answers on its chief's return."
        ),
    },
]

REGIONS = [
    ("NORTH AMERICA", [
        "US consumer confidence jumps to its highest level in nearly two years.",
        "Salvadoran migrant Kilmar Abrego Garcia leaves the US for Spain after his deportation fight.",
    ]),
    ("SOUTH AMERICA", [
        "Eni and Repsol pledge $2bn of joint investment in Venezuelan oil ventures.",
        "Ecuador and the US review joint military operations; Venezuela reveals a $237bn debt load.",
    ]),
    ("EUROPE", [
        "Zelenskyy turns to the new Democrat-led US Congress as Trump's peace push narrows; the US rules out troops in post-war Ukraine.",
        "France tells Putin to abandon his 'colonial and imperialist delusion'; Poland plans a no-fly zone on its eastern border.",
    ]),
    ("MIDDLE EAST", [
        "Israel's military kills Hamas security chief Mohammad Abuelouf in a Gaza strike.",
        "Houthi forces close to within 60 km of Aden as the Saudi-led coalition urges evacuation of Hodeidah port.",
    ]),
    ("AFRICA", [
        "Sudan's RSF kills 19 civilians in drone strikes on two cities, rights lawyers say.",
        "Senegal's MPs meet to debate the budget decree; at least 30 killed by militants in Nigeria's Niger region.",
    ]),
    ("SOUTH ASIA", [
        "Bangladesh raises garment workers' minimum wage 36% to $139 after protests.",
        "India tells 'cockroach' movement leader Das not to use his passport; Sheikh Hasina sets a 16 December return date.",
    ]),
    ("EAST ASIA", [
        "China's Shenzhou-24 docks at the Tiangong station carrying Pakistan's first astronaut.",
        "China sentences an official to death for leaking over 100 state secrets; Japan aims to be the world's No. 3 AI power.",
    ]),
    ("SOUTHEAST ASIA", [
        "At least 26 miners are thought trapped in an illegal gold mine in Indonesia.",
        "Indonesian students rally at night for teacher welfare and a 20% education budget.",
    ]),
    ("OCEANIA", [
        "Australia and Solomon Islands sign a treaty barring any foreign military base on the islands.",
        "Australia's October inflation hits 4.9%, keeping a rate rise on the table; bushfire evacuations ordered.",
    ]),
    ("TECHNOLOGY", [
        "A US jury convicts Huawei of trade-secret theft and bank fraud in a sprawling criminal trial.",
        "Microsoft declares 'Code Red' after a historic outage, internal memos show; Anthropic shares fall below their IPO price.",
    ]),
]

ALSO = [
    "US spy agencies hit by cyber breach; some unclassified data taken.",
    "Trump pardons turkeys Freedom and Feathers before Thanksgiving.",
    "Melania Trump reunites nine more Ukrainian and Russian children.",
    "Sinner out long after knee surgery; Lakers beat Jazz, Doncic 28.",
    "Bus-truck crash kills 10 in Egypt; Gaza hospital loses power.",
    "BBC journalists strike, disrupting Eurostar; Decathlon data breach.",
    "WHO funds Cuba's health system; Saudi kidnapped in Niger.",
    "Leaked Russian figures: ~490,000 soldiers dead since 2022, BBC reports.",
]

UCL = (
    "CHAMPIONS LEAGUE · MATCHDAY 5 — Sabah 1–4 Barcelona · Club Brugge 0–3 Liverpool · "
    "PSG 2–2 Roma · Sporting 2–2 Man Utd · Lille 2–1 Bayern · Inter 2–0 Stuttgart · "
    "Atlético 2–0 Viking · Shakhtar 0–1 Fenerbahçe · Slavia 0–1 Villarreal"
)

MARKETS = (
    "MARKETS — Nasdaq −2% · Kospi −6% · Nikkei −3% · Brent ~$87.8 · Gold ~$3,524 · "
    "Bitcoin ~$59,000 · VIX up 60% in November"
)

# ---------------------------------------------------------------- drawing

def draw_masthead(d):
    rule(d, 28, 14, 996, 3)
    d.text((512, 26), "THE WORLD IN ONE DAY",
           font=font(SERIF_B, 56), fill=INK, anchor="mt")
    rule(d, 28, 96, 996, 2)
    d.text((512, 104), "WEDNESDAY  25  NOVEMBER  2026",
           font=font(SANS_B, 19), fill=RED, anchor="mt")
    d.text((512, 128), "One day of world news — 31 stories across 10 sections",
           font=font(SANS, 14), fill=GREY, anchor="mt")


def draw_tanker(d, x, y, w, h):
    """A small flat tanker on waves, drawn with plain shapes."""
    d.rectangle([x, y, x + w, y + h], fill=(214, 226, 236))
    # hull
    d.polygon([(x + 12, y + h - 42), (x + w - 12, y + h - 42),
               (x + w - 26, y + h - 22), (x + 26, y + h - 22)], fill=INK)
    # deck tanks
    for i in range(3):
        tx = x + 28 + i * 40
        d.rectangle([tx, y + h - 62, tx + 32, y + h - 42], fill=RED)
    # bridge tower
    d.rectangle([x + w - 58, y + 22, x + w - 22, y + h - 42], fill=NAVY)
    d.rectangle([x + w - 58, y + 16, x + w - 22, y + 22], fill=RED)
    # smoke
    for i, r in enumerate((7, 5, 4)):
        d.ellipse([x + w - 52 + i * 10, y + 2 + i * 3,
                   x + w - 52 + i * 10 + 2 * r, y + 2 + i * 3 + 2 * r],
                  fill=GREY)
    # waves
    for i in range(4):
        wx = x + 8 + i * ((w - 16) // 4)
        d.arc([wx, y + h - 14, wx + 34, y + h + 2], 0, 180, fill=SEA, width=2)


def draw_leads(d):
    y0, hgt = 152, 172
    boxes = [(28, 480), (516, 480)]
    for (x, w), lead in zip(boxes, LEADS):
        d.rectangle([x, y0, x + w, y0 + hgt], outline=INK, width=2)
        d.rectangle([x, y0, x + w, y0 + 26], fill=INK)
        d.text((x + 12, y0 + 5), lead["kicker"],
               font=font(SANS_B, 13), fill=PAPER)
        d.text((x + 12, y0 + 36), lead["headline"],
               font=font(SERIF_B, 24), fill=RED)
        body_w = w - 24
        body_y = y0 + 68
        if lead is LEADS[0]:
            # tanker art on the right of the first lead
            draw_tanker(d, x + w - 168, y0 + 66, 156, 96)
            body_w = w - 192
        para(d, x + 12, body_y, lead["body"], font(SANS, 13),
             body_w, 17)


def draw_regions(d):
    x0, y0 = 28, 334
    cw, chh, gap = 480, 94, 8
    for i, (region, stories) in enumerate(REGIONS):
        col, row = i % 2, i // 2
        x = x0 + col * (cw + gap)
        y = y0 + row * (chh + gap)
        d.rectangle([x, y, x + cw, y + chh], outline=GREY, width=1)
        d.rectangle([x, y, x + cw, y + 22], fill=LIGHT)
        d.text((x + 10, y + 4), region, font=font(SANS_B, 13), fill=RED)
        yy = y + 28
        for s in stories:
            yy = para(d, x + 10, yy, "•  " + s, font(SANS, 12),
                      cw - 20, 15)
            yy += 2


def draw_also(d):
    y0 = 844
    d.rectangle([28, y0, 996, y0 + 22], fill=NAVY)
    d.text((40, y0 + 4), "ALSO TODAY", font=font(SANS_B, 13), fill=PAPER)
    yy = y0 + 28
    col_w = 472
    for i, item in enumerate(ALSO):
        col = i % 2
        row = i // 2
        x = 28 + col * (col_w + 8)
        y = yy + row * 14
        para(d, x, y, "•  " + item, font(SANS, 11), col_w, 13)


def draw_strips(d):
    y = 934  # below ALSO TODAY block
    # UCL strip
    d.rectangle([28, y, 996, y + 28], fill=LIGHT, outline=INK)
    para(d, 40, y + 2, UCL, font(SANS_B, 10), 928, 12)
    y = y + 32
    # markets strip
    d.rectangle([28, y, 996, y + 22], fill=INK)
    d.text((512, y + 4), MARKETS, font=font(SANS_B, 11),
           fill=PAPER, anchor="mt")
    y = y + 26
    # footer
    d.text((512, y + 2),
           "Sources: Reuters · Just Security · UEFA · AP · BBC — every story happened or was "
           "first reported on Wednesday 25 November 2026.",
           font=font(SANS, 10), fill=GREY, anchor="mt")
    d.text((512, y + 15),
           "Drawn by an agent for the make.fun bounty “Sum up 25 November's world news in one image”.",
           font=font(SANS, 10), fill=GREY, anchor="mt")


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    draw_masthead(d)
    draw_leads(d)
    draw_regions(d)
    draw_also(d)
    draw_strips(d)
    img.save(OUT, format="PNG", optimize=True)
    print("wrote", OUT, os.path.getsize(OUT), "bytes")


if __name__ == "__main__":
    main()
