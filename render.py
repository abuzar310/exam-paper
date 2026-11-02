#!/usr/bin/env python3
"""Turn an answers .md file into the exam-answer PDF + PNG pages (sized for 9-in-1 printing).

    python render.py papers/hrm-sem3-2026/answers.md
    python render.py answers.md --scale 1 --columns 2   # the original small two-column size

The .md format is described in README.md ("Answer file format").
Output: <out>/<name>.pdf and <out>/<name>-page-N.png (300 dpi by default).
"""
import argparse
import io
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
BODY, LEADING, INDENT = 8.5, 9.8, 10.9                          # pt (reference leading 10.25)
PAPERS = {"a4": A4, "letter": LETTER}

# Everything above is drawn this many times bigger. The user prints 9 pages on one A4
# sheet (each page shrinks to about 0.31): 1x gave 2.8 pt text (unreadable), 1.8 gave
# 5 pt (readable, but 12 pages for what was 4), 1.6 with 9.8 pt leading gives 4.2 pt
# and fits the HRM sample on 9 pages = one sheet. Two columns per page is the user's rule.
SCALE, COLUMNS = 1.6, 2


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
        # question line holds only "Q3." now, the user's way to find answers: body size, not 7 pt
        "q": ParagraphStyle("q", fontName=bold, fontSize=8.5, leading=9.6, textColor=QBLUE, spaceBefore=3.15),
        "sub": ParagraphStyle("sub", fontName=bold, fontSize=7.4, leading=LEADING, textColor=QBLUE),
        "body": body,
        "item": ParagraphStyle("item", parent=body, leftIndent=INDENT, firstLineIndent=-INDENT),
        # tables: 6.45 pt in the reference, raised so they survive 9-in-1 printing
        "th": ParagraphStyle("th", fontName=bold, fontSize=7.4, leading=8.8, textColor=white),
        "td": ParagraphStyle("td", fontName=font, fontSize=7.4, leading=8.8, textColor=black),
        "td1": ParagraphStyle("td1", fontName=bold, fontSize=7.4, leading=8.8, textColor=black),
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
    # first column 22% as in the reference, but wide enough for its longest word
    longest = max(pdfmetrics.stringWidth(word, st["td1"].fontName, st["td1"].fontSize)
                  for r in rows for word in re.sub(r"[*_]", "", r[0]).split() or [""])
    first = max(col_w * (0.22 if n >= 3 else 0.32), longest + 9) if n > 1 else col_w
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


def heading(*flowables):
    for f in flowables:
        f.heading = True
    return list(flowables)


def first_piece(f, col_w):
    """Height of the smallest part of f that can start at a column bottom."""
    h = f.wrap(col_w, 1e6)[1]
    if isinstance(f, Table):
        return sum(f._rowHeights[:2])                       # header row + first row
    return h if h <= 3 * LEADING + 1 else 2 * LEADING        # 3 lines can't split 2+1


def build(blocks, st, col_w):
    # Each heading gets a CondPageBreak = "start a new column unless the heading plus the
    # first piece of its answer fits", so no heading is left alone at a column bottom
    # while long answers may still split. One check per run of headings: a break between
    # a section title and its first question would stop their spaces from overlapping.
    out, prev = [], None
    for kind, *rest in blocks:
        if kind in ("h1", "q", "sub") and prev not in ("h1", "q", "sub"):
            out.append(CondPageBreak(0))
        if kind == "h1":
            out += heading(Paragraph(inline(rest[0]), st["h1"]),
                           HRFlowable(width="100%", thickness=1.6, color=NAVY, spaceBefore=2.4, spaceAfter=3.2))
        elif kind == "q":
            out += heading(Paragraph(inline(rest[0]), st["q"]),
                           HRFlowable(width="100%", thickness=0.55, color=GREY, spaceBefore=0.6, spaceAfter=1.2))
        elif kind == "sub":
            out += heading(Paragraph(inline(rest[0]), st["sub"]))
        elif kind == "para":
            out.append(Paragraph(inline(rest[0]), st["body"]))
        elif kind == "item":
            mark = "•" if rest[0] in "-*•" else rest[0]
            out.append(Paragraph(f"<b>{mark}</b> {inline(rest[1])}", st["item"]))
        else:
            out.append(make_table(rest[0], st, col_w))
        prev = kind

    for i, f in enumerate(out):
        if isinstance(f, CondPageBreak):
            j = i + 1
            while j < len(out) and getattr(out[j], "heading", False):
                f.height += out[j].wrap(col_w, 1e6)[1] + out[j].getSpaceBefore() + out[j].getSpaceAfter()
                j += 1
            if j < len(out):
                f.height += first_piece(out[j], col_w)
    return out


def render(md, paper="a4", dpi=300, out_dir=None, scale=SCALE, columns=COLUMNS):
    md = Path(md)
    name = md.parent.name if md.stem == "answers" else md.stem
    out_dir = Path(out_dir) if out_dir else md.parent / "output"
    out_dir.mkdir(parents=True, exist_ok=True)
    pdf = out_dir / f"{name}.pdf"

    # Lay out at the reference sizes on a page `scale` times smaller, then enlarge each
    # page onto the real paper (still vector), so text, lines and gaps all grow together.
    # Margins and the gap between columns stay their reference size on paper (not enlarged).
    page_w, page_h = PAPERS[paper]
    w, h = page_w / scale, page_h / scale
    mx, mt, mb, gap = MARGIN_X / scale, MARGIN_TOP / scale, MARGIN_BOTTOM / scale, GUTTER / scale
    col_w = (w - 2 * mx - (columns - 1) * gap) / columns
    frames = [Frame(mx + i * (col_w + gap), mb, col_w, h - mt - mb, id=f"col{i}",
                    leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0) for i in range(columns)]
    small = io.BytesIO()
    doc = BaseDocTemplate(small, pagesize=(w, h), pageTemplates=[PageTemplate(frames=frames)])
    st = make_styles(*register_fonts())
    doc.build(build(parse(md.read_text(encoding="utf-8")), st, col_w))

    for old in out_dir.glob(f"{name}-page-*.png"):
        old.unlink()
    pngs = []
    with pymupdf.open("pdf", small.getvalue()) as src, pymupdf.open() as d:
        for i in range(len(src)):
            d.new_page(width=page_w, height=page_h).show_pdf_page(pymupdf.Rect(0, 0, page_w, page_h), src, i)
        d.set_metadata({"title": name})
        d.save(pdf, garbage=3, deflate=True)
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
    ap.add_argument("--scale", type=float, default=SCALE,
                    help=f"size vs the reference pages (default {SCALE}, readable when printed 9-in-1; 1 = original size)")
    ap.add_argument("--columns", type=int, default=COLUMNS, help=f"columns per page (default {COLUMNS})")
    a = ap.parse_args()
    pdf, pngs = render(a.md, a.paper, a.dpi, a.out, a.scale, a.columns)
    print(f"{pdf}  ({len(pngs)} page{'s' * (len(pngs) != 1)})")
    for p in pngs:
        print(p)
