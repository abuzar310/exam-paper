#!/usr/bin/env python3
"""One PNG per English Q.P. 54302 answer, saved next to the single-column PDF.

The wording is the answers.md text. These files are for viewing one answer at a time.
"""
import re
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

HERE = Path(__file__).resolve().parent
OUT = HERE / "output"
MD = HERE / "answers.md"
NAVY = (31, 78, 121)
INK = (26, 26, 26)
MUTED = (70, 90, 110)
ALT = (234, 241, 250)
WHITE = (255, 255, 255)
LINE = (195, 204, 214)
W = 1600
PAD = 56
FONT = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
FONTB = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"

# Question number -> (short title, file name, section label)
META = {
    "Q1. (a)": ("Akaki's office", "q1a-akaki-office.png", "Part I  ·  Short note"),
    "Q1. (b)": ("Petrovitch, the tailor", "q1b-petrovitch.png", "Part I  ·  Short note"),
    "Q1. (c)": ("Eeri after Mudli's death", "q1c-eeri.png", "Part I  ·  Short note"),
    "Q1. (d)": ("Indian tradition of telling tales", "q1d-telling-tales.png", "Part I  ·  Short note"),
    "Q2. (a)": ("Poverty in The Overcoat", "q2a-poverty.png", "Part I  ·  Long answer"),
    "Q2. (b)": ("Class struggle in The Overcoat", "q2b-class-struggle.png", "Part I  ·  Long answer"),
    "Q2. (c)": ("Two traditions in Kirubunkal", "q2c-two-traditions.png", "Part I  ·  Long answer"),
    "Q3. (1)": ("Letter of enquiry", "q3-1-enquiry.png", "Part II  ·  Writing skills"),
    "Q3. (2)": ("Quotation letter", "q3-2-quotation.png", "Part II  ·  Writing skills"),
    "Q3. (3)": ("Order letter", "q3-3-order.png", "Part II  ·  Writing skills"),
    "Q3. (4)": ("Complaint letter", "q3-4-complaint.png", "Part II  ·  Writing skills"),
    "Q3. (5)": ("Circular letter", "q3-5-circular.png", "Part II  ·  Writing skills"),
    "Q3. (6)": ("Commercial terms", "q3-6-commercial-terms.png", "Part II  ·  Writing skills"),
}


def face(size, bold=False):
    return ImageFont.truetype(FONTB if bold else FONT, size)


def wrap(draw, text, font, width):
    words = text.split()
    if not words:
        return [""]
    lines, cur = [], words[0]
    for word in words[1:]:
        trial = cur + " " + word
        if draw.textlength(trial, font=font) <= width:
            cur = trial
        else:
            lines.append(cur)
            cur = word
    lines.append(cur)
    return lines


def is_firm(line):
    letters = [c for c in line if c.isalpha()]
    return bool(letters) and all(c.isupper() for c in letters) and len(line) < 48


def parse_sections(text):
    text = re.sub(r"<!--.*?-->", "", text, flags=re.S)
    sections, q, blocks, table = [], None, [], None
    for raw in text.splitlines():
        s = raw.strip()
        if s.startswith("## "):
            if table:
                blocks.append(("table", table))
                table = None
            if q:
                sections.append((q, blocks))
            q, blocks = s[3:].strip(), []
            continue
        if s.startswith("# "):
            continue
        if s.startswith("|"):
            cells = [c.strip() for c in s.strip("|").split("|")]
            if all(re.fullmatch(r":?-+:?", c) for c in cells):
                continue
            table = (table or []) + [cells]
            continue
        if table:
            blocks.append(("table", table))
            table = None
        if not s:
            blocks.append(("blank", ""))
        else:
            blocks.append(("line", s))
    if table:
        blocks.append(("table", table))
    if q:
        sections.append((q, blocks))
    return sections


def draw_table(d, rows, y, width):
    n = max(len(r) for r in rows)
    rows = [r + [""] * (n - len(r)) for r in rows]
    col_w = width / n
    head, body = face(28, True), face(28)
    row_h = 64
    for i, row in enumerate(rows):
        fill = NAVY if i == 0 else (ALT if i % 2 else WHITE)
        colour = WHITE if i == 0 else INK
        f = head if i == 0 else body
        d.rectangle((PAD, y, PAD + width, y + row_h), fill=fill, outline=LINE)
        for c, cell in enumerate(row):
            x = PAD + c * col_w
            d.line((x, y, x, y + row_h), fill=LINE)
            d.text((x + 16, y + 16), cell, font=f, fill=colour)
        y += row_h
    return y + 16


def draw_answer(q, blocks):
    title, name, section = META[q]
    measure = ImageDraw.Draw(Image.new("RGB", (W, 10)))
    body_f = face(32)
    text_w = W - 2 * PAD
    # Measure height, then draw. Letters and essays share one flow.
    plan = []
    letterhead = False
    gap_before = 8
    for kind, payload in blocks:
        if kind == "blank":
            gap_before += 8 if letterhead else 18
            continue
        if kind == "table":
            letterhead = False
            plan.append(("table", payload, gap_before))
            gap_before = 8
            continue
        line = payload
        if is_firm(line):
            plan.append(("firm", line, gap_before))
            letterhead = True
            gap_before = 6
            continue
        # The centred lines are only the firm's own address. A date ends that block.
        if letterhead and not re.match(r"\d{1,2} [A-Z][a-z]+ \d{4}$", line) and not line.startswith(("Dear ", "Sub:", "Ref:")):
            plan.append(("address", line, gap_before))
            gap_before = 4
            continue
        letterhead = False
        term = re.match(r"(\d+)\.\s+\*\*(.+?)\*\*:?\s*(.*)", line)
        if term:
            num, label, rest = term.groups()
            plan.append(("term", (num, label.rstrip(":"), rest), gap_before))
        elif re.match(r"\d+\.\s+", line):
            plan.append(("item", line, gap_before))
        elif line.startswith(("Sub:", "Ref:")):
            plan.append(("subject", line, gap_before))
        elif line.startswith("Dear "):
            plan.append(("dear", line, gap_before))
        elif line.startswith("Yours "):
            plan.append(("close", line, gap_before))
        elif re.match(r"\d{1,2} [A-Z][a-z]+ \d{4}$", line):
            plan.append(("date", line, gap_before))
        else:
            plan.append(("para", line, gap_before))
        gap_before = 10

    y = 168
    heights = []
    for kind, payload, gap in plan:
        y += gap
        if kind == "firm":
            h = 58
        elif kind == "address":
            h = 42
        elif kind == "table":
            h = 64 * len(payload) + 16
        elif kind == "term":
            rest = payload[2]
            lines = wrap(measure, rest, body_f, text_w - 40) if rest else [""]
            h = 78 + 46 * len(lines)
        elif kind == "item":
            _, _, rest = payload.partition(" ")
            lines = wrap(measure, rest, body_f, text_w - 56)
            h = 46 * len(lines)
        elif kind == "para":
            lines = wrap(measure, payload, body_f, text_w)
            h = 46 * len(lines)
        else:
            h = 46
        heights.append(h)
        y += h
    im = Image.new("RGB", (W, y + 48), WHITE)
    d = ImageDraw.Draw(im)
    d.rectangle((0, 0, W, 140), fill=NAVY)
    d.text((PAD, 26), q, font=face(28), fill=(214, 226, 238))
    d.text((PAD, 62), title, font=face(44, True), fill=WHITE)
    d.text((PAD, 112), section + "   ·   Q.P. 54302", font=face(22), fill=(214, 226, 238))

    y = 168
    for (kind, payload, gap), h in zip(plan, heights):
        y += gap
        if kind == "firm":
            f = face(40, True)
            tw = d.textlength(payload, font=f)
            d.text(((W - tw) / 2, y), payload, font=f, fill=NAVY)
            d.line((PAD, y + 52, W - PAD, y + 52), fill=NAVY, width=2)
        elif kind == "address":
            f = face(28)
            tw = d.textlength(payload, font=f)
            d.text(((W - tw) / 2, y), payload, font=f, fill=MUTED)
        elif kind == "date":
            d.text((PAD, y), payload, font=face(30), fill=INK)
        elif kind == "dear":
            d.text((PAD, y), payload, font=face(32, True), fill=INK)
        elif kind == "subject":
            label, _, rest = payload.partition(":")
            d.text((PAD, y), label + ":", font=face(32, True), fill=NAVY)
            lw = d.textlength(label + ": ", font=face(32, True))
            d.text((PAD + lw, y), rest.strip(), font=face(32), fill=INK)
        elif kind == "close":
            d.text((PAD, y), payload, font=face(32, True), fill=INK)
        elif kind == "term":
            num, label, rest = payload
            d.rounded_rectangle((PAD, y, W - PAD, y + h - 8), radius=12, fill=ALT)
            d.text((PAD + 20, y + 14), f"{num}.  {label}", font=face(32, True), fill=NAVY)
            yy = y + 58
            for ln in (wrap(d, rest, body_f, text_w - 40) if rest else []):
                d.text((PAD + 20, yy), ln, font=body_f, fill=INK)
                yy += 46
        elif kind == "item":
            mark, _, rest = payload.partition(" ")
            d.text((PAD, y), mark, font=face(32, True), fill=NAVY)
            yy = y
            for ln in wrap(d, rest, body_f, text_w - 56):
                d.text((PAD + 56, yy), ln, font=body_f, fill=INK)
                yy += 46
        elif kind == "table":
            y = draw_table(d, payload, y, text_w) - h
        else:
            yy = y
            for ln in wrap(d, payload, body_f, text_w):
                d.text((PAD, yy), ln, font=body_f, fill=INK)
                yy += 46
        y += h
    OUT.mkdir(parents=True, exist_ok=True)
    path = OUT / name
    im.save(path, "PNG")
    print(path)


def main():
    sections = parse_sections(MD.read_text(encoding="utf-8"))
    found = [q for q, _ in sections]
    missing = [q for q in META if q not in found]
    extra = [q for q in found if q not in META]
    if missing or extra:
        raise SystemExit(f"question mismatch: missing {missing}, extra {extra}")
    for q, blocks in sections:
        draw_answer(q, blocks)


if __name__ == "__main__":
    main()
