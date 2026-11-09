#!/usr/bin/env python3
"""Standalone figures for the Corporate Accounting 54321 answer sheet.

Numbers are the worked answers. The PNGs are written next to the PDF.
"""
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

OUT = Path(__file__).resolve().parent / "output"
NAVY = (31, 78, 121)
INK = (26, 26, 26)
MUTED = (70, 90, 110)
ALT = (234, 241, 250)
WHITE = (255, 255, 255)
LINE = (195, 204, 214)
W = 1600
PAD = 48
FONT = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
FONTB = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def face(size, bold=False):
    return ImageFont.truetype(FONTB if bold else FONT, size)


def canvas(height):
    im = Image.new("RGB", (W, height), WHITE)
    return im, ImageDraw.Draw(im)


def header(d, title, sub=""):
    d.rectangle((0, 0, W, 128), fill=NAVY)
    d.text((PAD, 28), title, font=face(52, True), fill=WHITE)
    if sub:
        d.text((PAD, 86), sub, font=face(28), fill=(214, 226, 238))


def pair_row(d, y, left, right, fill=None, height=84):
    if fill:
        d.rectangle((PAD, y, W - PAD, y + height), fill=fill)
    d.text((PAD + 20, y + 18), left, font=face(40, True), fill=INK)
    f = face(40, True)
    tw = d.textlength(right, font=f)
    d.text((W - PAD - 20 - tw, y + 18), right, font=f, fill=NAVY)
    return y + height + 10


def save(im, name):
    OUT.mkdir(parents=True, exist_ok=True)
    path = OUT / name
    im.save(path, "PNG")
    print(path)


def section_a():
    items = [
        ("1(a) Valuation of shares", "Real worth of a share when the price is unreliable."),
        ("1(b) Goodwill", "Extra earning power above a normal return."),
        ("1(c) Liquidator", "Realises assets, pays creditors, returns any surplus."),
        ("1(d) Preferential creditors", "Govt dues, 4 months' wages, holiday pay, PF and ESI."),
        ("1(e) Profit prior to incorporation", "Capital profit. Capital reserve. Not a dividend."),
        ("1(f) Features of goodwill", "Intangible, sold only with the business, fluctuating, earns super profit."),
        ("1(g) Schedule III notes", "Bad debts: Other expenses. Employer PF: Employee benefits."),
        ("1(h) Underwriting", "Contract to take the shares the public does not buy."),
        ("1(i) Firm underwriting", "A fixed number of shares, whether the public subscribes or not."),
        ("1(j) Super profit", "Average profit minus normal profit."),
    ]
    row_h = 118
    h = 150 + len(items) * row_h + 30
    im, d = canvas(h)
    header(d, "Section A  ·  2 marks", "Q.P. 54321  ·  first ten answers")
    y = 150
    for i, (title, body) in enumerate(items):
        fill = ALT if i % 2 == 0 else WHITE
        d.rectangle((PAD, y, W - PAD, y + row_h - 12), fill=fill)
        d.text((PAD + 20, y + 12), title, font=face(36, True), fill=NAVY)
        d.text((PAD + 20, y + 60), body, font=face(30), fill=INK)
        y += row_h
    save(im, "section-a.png")


def q2():
    im, d = canvas(760)
    header(d, "Q2  ·  Value of each class of share", "Net assets method, with a notional call")
    y = 156
    y = pair_row(d, y, "Tangible assets minus creditors", "Rs. 20,00,000", ALT)
    y = pair_row(d, y, "Add notional call on B shares", "Rs. 2,50,000")
    y = pair_row(d, y, "Assets if all shares are fully paid", "Rs. 22,50,000", ALT)
    y = pair_row(d, y, "Value of one fully paid share", "Rs. 112.50")
    y += 16
    box_w = (W - 2 * PAD - 24) // 2
    for i, (label, value, note) in enumerate((
            ("A share", "Rs. 112.50", "Rs. 100 paid"),
            ("B share", "Rs. 87.50", "Rs. 75 paid  ·  112.50 minus 25"))):
        x = PAD + i * (box_w + 24)
        d.rounded_rectangle((x, y, x + box_w, y + 200), radius=16, fill=NAVY)
        d.text((x + 28, y + 24), label, font=face(36), fill=(214, 226, 238))
        d.text((x + 28, y + 78), value, font=face(64, True), fill=WHITE)
        d.text((x + 28, y + 156), note, font=face(28), fill=(214, 226, 238))
    save(im, "q2-share-values.png")


def q3():
    im, d = canvas(700)
    header(d, "Q3  ·  Goodwill", "3 years' purchase of super profit")
    y = 156
    steps = [
        ("Total profit of five years", "Rs. 24,00,000"),
        ("Average profit", "Rs. 4,80,000"),
        ("Normal profit, 10% of 40,00,000", "Rs. 4,00,000"),
        ("Super profit", "Rs. 80,000"),
        ("Goodwill  =  80,000  x  3", "Rs. 2,40,000"),
    ]
    for i, (left, right) in enumerate(steps):
        fill = NAVY if i == len(steps) - 1 else (ALT if i % 2 == 0 else WHITE)
        ink = WHITE if i == len(steps) - 1 else INK
        val = WHITE if i == len(steps) - 1 else NAVY
        d.rectangle((PAD, y, W - PAD, y + 88), fill=fill)
        d.text((PAD + 20, y + 22), left, font=face(38, True), fill=ink)
        f = face(38, True)
        tw = d.textlength(right, font=f)
        d.text((W - PAD - 20 - tw, y + 22), right, font=f, fill=val)
        y += 98
    save(im, "q3-goodwill.png")


def q4():
    im, d = canvas(560)
    header(d, "Q4  ·  Time ratio", "Takeover 1 Apr 2021  ·  accounts close 31 Mar 2022")
    y = 180
    pre_w, gap = 371, 20
    d.text((PAD, y), "Pre-incorporation", font=face(32, True), fill=NAVY)
    d.text((PAD + pre_w + gap, y), "Post-incorporation", font=face(32, True), fill=NAVY)
    y = 240
    d.rounded_rectangle((PAD, y, PAD + pre_w, y + 90), radius=12, fill=NAVY)
    d.rounded_rectangle((PAD + pre_w + gap, y, W - PAD, y + 90), radius=12, fill=(70, 110, 150))
    d.text((PAD + 90, y + 24), "3 months", font=face(40, True), fill=WHITE)
    d.text((PAD + pre_w + gap + 420, y + 24), "9 months", font=face(40, True), fill=WHITE)
    d.text((PAD, 360), "1 April to 30 June", font=face(28), fill=MUTED)
    d.text((PAD + pre_w + gap, 360), "1 July 2021 to 31 March 2022", font=face(28), fill=MUTED)
    d.text((PAD, 430), "Time ratio  =  3 : 9  =  1 : 3", font=face(48, True), fill=NAVY)
    d.text((PAD, 500), "Sales of Rs. 10,00,000 cannot come out of total sales of Rs. 3,00,000.", font=face(28), fill=INK)
    save(im, "q4-time-ratio.png")


def q5():
    rows = [
        ("Revenue from operations", "9,78,800", False),
        ("Other income", "11,400", False),
        ("Total income", "9,90,200", True),
        ("Cost of goods sold", "6,57,500", False),
        ("Employee benefits", "10,000", False),
        ("Finance cost", "6,000", False),
        ("Depreciation", "70,000", False),
        ("Other expenses", "61,600", False),
        ("Total expenses", "8,05,100", True),
        ("Profit for the year", "1,85,100", True),
    ]
    h = 160 + len(rows) * 78 + 40
    im, d = canvas(h)
    header(d, "Q5  ·  ABC Ltd.", "Statement of profit and loss for the year ended 31.03.2025")
    y = 152
    for i, (left, right, strong) in enumerate(rows):
        last = i == len(rows) - 1
        fill = NAVY if last else (ALT if i % 2 == 0 else WHITE)
        ink = WHITE if last else INK
        d.rectangle((PAD, y, W - PAD, y + 70), fill=fill)
        d.text((PAD + 20, y + 14), left, font=face(36, strong or last), fill=ink)
        f = face(36, True)
        tw = d.textlength(right, font=f)
        d.text((W - PAD - 20 - tw, y + 14), right, font=f, fill=WHITE if last else NAVY)
        y += 78
    save(im, "q5-profit-and-loss.png")


def q6():
    im, d = canvas(720)
    header(d, "Q6  ·  Liquidator's remuneration", "5% on assets realised, 4% on the amount distributed")
    y = 156
    rows = [
        ("Assets realised", "5,00,000", False),
        ("Less secured creditors", "1,00,000", False),
        ("Less 5% on assets realised", "25,000", False),
        ("Cash left for the creditors", "3,75,000", False),
        ("4% commission, 4/104 of that cash", "14,423.08", False),
        ("Total remuneration", "39,423.08", True),
    ]
    for i, (left, right, last) in enumerate(rows):
        fill = NAVY if last else (ALT if i % 2 == 0 else WHITE)
        ink = WHITE if last else INK
        d.rectangle((PAD, y, W - PAD, y + 78), fill=fill)
        d.text((PAD + 20, y + 18), left, font=face(36, True), fill=ink)
        f = face(36, True)
        tw = d.textlength(right, font=f)
        d.text((W - PAD - 20 - tw, y + 18), right, font=f, fill=WHITE if last else NAVY)
        y += 86
    save(im, "q6-liquidator-remuneration.png")


def table(title, sub, headers, rows, name, emphasize_last=True):
    cols = len(headers)
    row_h = 78
    h = 160 + (len(rows) + 1) * row_h + 30
    im, d = canvas(h)
    header(d, title, sub)
    y = 152
    col_w = (W - 2 * PAD) / cols
    def cell(text, x, yy, fill, color, bold=False):
        d.rectangle((x, yy, x + col_w, yy + row_h - 8), fill=fill)
        f = face(32, bold)
        tw = d.textlength(text, font=f)
        d.text((x + col_w - 16 - tw, yy + 18), text, font=f, fill=color)
    # header row, left aligned for first col
    for c, text in enumerate(headers):
        x = PAD + c * col_w
        d.rectangle((x, y, x + col_w - 4, y + row_h - 8), fill=NAVY)
        f = face(30, True)
        if c == 0:
            d.text((x + 16, y + 18), text, font=f, fill=WHITE)
        else:
            tw = d.textlength(text, font=f)
            d.text((x + col_w - 20 - tw, y + 18), text, font=f, fill=WHITE)
    y += row_h
    for r, row in enumerate(rows):
        last = emphasize_last and r == len(rows) - 1
        for c, text in enumerate(row):
            x = PAD + c * col_w
            fill = NAVY if last else (ALT if r % 2 == 0 else WHITE)
            color = WHITE if last else INK
            d.rectangle((x, y, x + col_w - 4, y + row_h - 8), fill=fill)
            f = face(30, c == 0 or last)
            if c == 0:
                d.text((x + 16, y + 18), text, font=f, fill=color)
            else:
                tw = d.textlength(text, font=f)
                d.text((x + col_w - 20 - tw, y + 18), text, font=f, fill=WHITE if last else NAVY)
        y += row_h
    save(im, name)


def q7():
    table(
        "Q7  ·  Arun Ltd. underwriters",
        "Unmarked applications shared 5 : 3 : 2",
        ["Particulars", "X", "Y", "Z"],
        [
            ["Gross liability", "10,000", "6,000", "4,000"],
            ["Less marked", "4,500", "3,000", "2,500"],
            ["Less unmarked", "3,000", "1,800", "1,200"],
            ["Net liability", "2,500", "1,200", "300"],
        ],
        "q7-underwriting-liability.png",
    )


def q10():
    blocks = [
        ("Shares", [
            "Intrinsic  =  net assets for equity / number of shares",
            "Yield  =  (expected rate / normal rate) x paid-up value",
            "Fair value  =  (intrinsic + yield) / 2",
        ]),
        ("Goodwill", [
            "Average profit  x  years' purchase",
            "Super profit  x  years' purchase",
            "Annuity: super profit  x  present value of Re. 1",
        ]),
    ]
    im, d = canvas(760)
    header(d, "Q10  ·  Methods in B.Com. 3.1", "Davangere University SEP syllabus")
    y = 160
    for title, lines in blocks:
        d.text((PAD, y), title, font=face(40, True), fill=NAVY)
        y += 64
        for line in lines:
            d.rectangle((PAD, y, W - PAD, y + 72), fill=ALT)
            d.text((PAD + 20, y + 16), line, font=face(32), fill=INK)
            y += 84
        y += 16
    save(im, "q10-valuation-methods.png")


def q11():
    im, d = canvas(520)
    header(d, "Q11  ·  Spandu Ltd.", "Value of one equity share")
    y = 180
    box_w = (W - 2 * PAD - 48) // 3
    cards = [
        ("Net assets", "Rs. 15", "6,00,000 / 40,000"),
        ("Yield", "Rs. 20", "Expected rate 20%"),
        ("Fair value", "Rs. 17.50", "(15 + 20) / 2"),
    ]
    for i, (label, value, note) in enumerate(cards):
        x = PAD + i * (box_w + 24)
        d.rounded_rectangle((x, y, x + box_w, y + 250), radius=16, fill=NAVY)
        d.text((x + 24, y + 28), label, font=face(32), fill=(214, 226, 238))
        d.text((x + 24, y + 90), value, font=face(56, True), fill=WHITE)
        d.text((x + 24, y + 180), note, font=face(26), fill=(214, 226, 238))
    save(im, "q11-equity-share-value.png")


def q12():
    table(
        "Q12  ·  Surya Ltd. underwriters",
        "Firm shares credited to that underwriter, then added back",
        ["Particulars", "A", "B", "C"],
        [
            ["Gross liability", "1,00,000", "60,000", "40,000"],
            ["Less marked", "70,000", "28,000", "32,000"],
            ["Less firm", "20,000", "10,000", "10,000"],
            ["Less unmarked", "5,000", "3,000", "2,000"],
            ["Net liability", "2,500", "17,500", "Nil"],
            ["Add firm", "20,000", "10,000", "10,000"],
            ["Total liability", "22,500", "27,500", "10,000"],
        ],
        "q12-surya-underwriting.png",
    )


if __name__ == "__main__":
    section_a()
    q2()
    q3()
    q4()
    q5()
    q6()
    q7()
    q10()
    q11()
    q12()
