#!/usr/bin/env python3
"""Turn an answers .md file into the two-column exam-answer PDF + PNG pages.

    python render.py papers/hrm-sem3-2026/answers.md
    python render.py answers.md --paper letter --dpi 200

The .md format is described in README.md ("Answer file format").
Output: <out>/<name>.pdf and <out>/<name>-page-N.png (300 dpi by default).
"""
import argparse
import re
from pathlib import Path

import pymupdf
from reportlab.lib.colors import HexColor, black, white
from reportlab.lib.pagesizes import A4, LETTER
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (BaseDocTemplate, CondPageBreak, Frame, HRFlowable, PageTemplate,
                                Paragraph, Table, TableStyle)

# Colours and sizes measured from the reference pages (samples/hrm-question-bank/reference).
NAVY = HexColor("#1F4E79")   # "2 MARKS" titles, their thick rule, table header row
QBLUE = HexColor("#2B5683")  # question lines and sub-headings
GREY = HexColor("#B5B8B7")   # thin rule under each question
ALT = HexColor("#EAF1FA")    # every second table row
GRID = HexColor("#C3CCD6")   # table lines

MARGIN_X, MARGIN_TOP, MARGIN_BOTTOM, GUTTER = 11, 11, 12, 10.5  # pt
BODY, LEADING, INDENT = 8.5, 10.25, 10.9                        # pt
PAPERS = {"a4": A4, "letter": LETTER}


def register_fonts():
    """Arial from Windows if present, else the built-in Helvetica (same widths)."""
    win = Path("C:/Windows/Fonts")
    faces = {"Arial": "arial.ttf", "Arial-Bold": "arialbd.ttf",
             "Arial-Italic": "ariali.ttf", "Arial-BoldItalic": "arialbi.ttf"}
    if not all((win / f).exists() for f in faces.values()):
        return "Helvetica", "Helvetica-Bold"
    for name, f in faces.items():
        pdfmetrics.registerFont(TTFont(name, str(win / f)))
    pdfmetrics.registerFontFamily("Arial", normal="Arial", bold="Arial-Bold",
                                  italic="Arial-Italic", boldItalic="Arial-BoldItalic")
    return "Arial", "Arial-Bold"


def make_styles(font, bold):
    body = ParagraphStyle("body", fontName=font, fontSize=BODY, leading=LEADING, textColor=black, allowWidows=0)
    return {
        "h1": ParagraphStyle("h1", fontName=bold, fontSize=9.3, leading=11, textColor=NAVY, spaceBefore=1.5),
        "q": ParagraphStyle("q", fontName=bold, fontSize=7, leading=8.4, textColor=QBLUE, spaceBefore=3.15),
        "sub": ParagraphStyle("sub", fontName=bold, fontSize=7.4, leading=10.25, textColor=QBLUE),
        "body": body,
        "item": ParagraphStyle("item", parent=body, leftIndent=INDENT, firstLineIndent=-INDENT),
        "th": ParagraphStyle("th", fontName=bold, fontSize=6.45, leading=7.8, textColor=white),
        "td": ParagraphStyle("td", fontName=font, fontSize=6.45, leading=7.8, textColor=black),
        "td1": ParagraphStyle("td1", fontName=bold, fontSize=6.45, leading=7.8, textColor=black),
    }


def inline(s):
    """Escape for ReportLab and turn **bold** / *italic* into tags."""
    s = s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    s = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", s)
    return re.sub(r"(?<![*\w])\*(?!\s)(.+?)(?<!\s)\*(?![*\w])", r"<i>\1</i>", s)


def parse(text):
    """Split the .md into blocks: h1, q, sub, para, item, table."""
    text = re.sub(r"<!--.*?-->", "", text, flags=re.S)  # comments = private notes, never printed
    blocks, cont = [], None  # cont = block that a following line continues
    for raw in text.splitlines():
        s = raw.strip()
        if not s:
            cont = None
            continue
        if s.startswith("|"):
            cells = [c.strip() for c in s.strip("|").split("|")]
            if all(re.fullmatch(r":?-+:?", c) for c in cells):
                continue
            if cont and cont[0] == "table":
                cont[1].append(cells)
            else:
                cont = ["table", [cells]]
                blocks.append(cont)
            continue
        m = re.match(r"(#{1,3})\s+(.*)", s)
        if m:
            blocks.append([("h1", "q", "sub")[len(m[1]) - 1], m[2]])
            cont = None
            continue
        m = re.match(r"(\d+[.)]|[-*•])\s+(.*)", s)
        if m:
            cont = ["item", m[1], m[2]]
            blocks.append(cont)
        elif cont and cont[0] in ("para", "item"):
            cont[-1] += " " + s
        else:
            cont = ["para", s]
            blocks.append(cont)
    return blocks


def make_table(rows, st, col_w):
    n = max(len(r) for r in rows)
    rows = [r + [""] * (n - len(r)) for r in rows]
    first = col_w * (0.22 if n >= 3 else 0.32) if n > 1 else col_w
    widths = [first] + [(col_w - first) / (n - 1)] * (n - 1)
    data = [[Paragraph(inline(c), st["th"]) for c in rows[0]]]
    data += [[Paragraph(inline(r[0]), st["td1"])] + [Paragraph(inline(c), st["td"]) for c in r[1:]]
             for r in rows[1:]]
    t = Table(data, colWidths=widths, repeatRows=1, spaceBefore=1.5, spaceAfter=1)
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), NAVY),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [white, ALT]),
        ("GRID", (0, 0), (-1, -1), 0.5, GRID),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("LEFTPADDING", (0, 0), (-1, -1), 4),
        ("RIGHTPADDING", (0, 0), (-1, -1), 4),
        ("TOPPADDING", (0, 0), (-1, -1), 1.6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 1.8),
    ]))
    return t


def build(blocks, st, col_w):
    # CondPageBreak = "start a new column unless this much room is left", so a heading
    # always has at least two lines of its answer under it, but long answers may split.
    out = []
    for kind, *rest in blocks:
        if kind == "h1":
            out += [CondPageBreak(54), Paragraph(inline(rest[0]), st["h1"]),
                    HRFlowable(width="100%", thickness=1.6, color=NAVY, spaceBefore=2.4, spaceAfter=3.2)]
        elif kind == "q":
            out += [CondPageBreak(35), Paragraph(inline(rest[0]), st["q"]),
                    HRFlowable(width="100%", thickness=0.55, color=GREY, spaceBefore=0.6, spaceAfter=1.2)]
        elif kind == "sub":
            out += [CondPageBreak(31), Paragraph(inline(rest[0]), st["sub"])]
        elif kind == "para":
            out.append(Paragraph(inline(rest[0]), st["body"]))
        elif kind == "item":
            mark = "•" if rest[0] in "-*•" else rest[0]
            out.append(Paragraph(f"<b>{mark}</b> {inline(rest[1])}", st["item"]))
        else:
            out.append(make_table(rest[0], st, col_w))
    return out


def render(md, paper="a4", dpi=300, out_dir=None):
    md = Path(md)
    name = md.parent.name if md.stem == "answers" else md.stem
    out_dir = Path(out_dir) if out_dir else md.parent / "output"
    out_dir.mkdir(parents=True, exist_ok=True)
    pdf = out_dir / f"{name}.pdf"

    page_w, page_h = PAPERS[paper]
    col_w = (page_w - 2 * MARGIN_X - GUTTER) / 2
    frames = [Frame(MARGIN_X + i * (col_w + GUTTER), MARGIN_BOTTOM, col_w,
                    page_h - MARGIN_TOP - MARGIN_BOTTOM, id=f"col{i}",
                    leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0) for i in (0, 1)]
    doc = BaseDocTemplate(str(pdf), pagesize=(page_w, page_h), title=name, author="",
                          pageTemplates=[PageTemplate(frames=frames)])
    st = make_styles(*register_fonts())
    doc.build(build(parse(md.read_text(encoding="utf-8")), st, col_w))

    for old in out_dir.glob(f"{name}-page-*.png"):
        old.unlink()
    pngs = []
    with pymupdf.open(pdf) as d:
        for i, page in enumerate(d, 1):
            png = out_dir / f"{name}-page-{i}.png"
            page.get_pixmap(matrix=pymupdf.Matrix(dpi / 72, dpi / 72)).save(png)
            pngs.append(png)
    return pdf, pngs


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("md", help="answers .md file")
    ap.add_argument("--paper", choices=PAPERS, default="a4")
    ap.add_argument("--dpi", type=float, default=300, help="PNG resolution (default 300)")
    ap.add_argument("--out", help="output folder (default: <md folder>/output)")
    a = ap.parse_args()
    pdf, pngs = render(a.md, a.paper, a.dpi, a.out)
    print(f"{pdf}  ({len(pngs)} page{'s' * (len(pngs) != 1)})")
    for p in pngs:
        print(p)
