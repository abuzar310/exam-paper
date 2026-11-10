#!/usr/bin/env python3
"""Turn an answers .md file into the exam-answer PDF + PNG pages (sized for 9-in-1 printing).

    python render.py papers/hrm-sem3-2026/answers.md
    python render.py answers.md --scale 1.6   # everything 1.6x bigger (more pages)

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
from reportlab.platypus import (BaseDocTemplate, CondPageBreak, Frame, HRFlowable, Image, PageTemplate,
                                Paragraph, Table, TableStyle)

# Colours and sizes measured from the reference pages (samples/hrm-question-bank/reference).
NAVY = HexColor("#1F4E79")   # "2 MARKS" titles, their thick rule, table header row
QBLUE = HexColor("#2B5683")  # question lines and sub-headings
GREY = HexColor("#B5B8B7")   # thin rule under each question
ALT = HexColor("#EAF1FA")    # every second table row
GRID = HexColor("#C3CCD6")   # table lines

MARGIN_X, MARGIN_TOP, MARGIN_BOTTOM, GUTTER = 11, 11, 12, 10.5  # pt
# Answer text: 10 pt, the user's choice (reference 8.5 pt / 10.25 leading / 10.9 indent,
# all three raised by the same 10/8.5). Everything else keeps its reference size.
BODY, LEADING, INDENT = 10, 12.05, 12.8                         # pt
PAPERS = {"a4": A4, "letter": LETTER}
KEEP_TABLE = 300  # pt; tables up to this tall never split across columns

# Everything above can be drawn this many times bigger (--scale). The user prints 9 pages
# per A4 sheet; on 2026-11-02 they tried 1.6-2.2x, then chose plain 1x with 10 pt
# answers: the HRM answers take 5 pages instead of 4. Two columns is the user's rule.
SCALE, COLUMNS = 1, 2


def register_fonts(hindi=False):
    """Arial from Windows, or Nirmala UI when the paper has Hindi (Arial has no Devanagari);
    without Windows fonts, the built-in Helvetica (same widths as Arial)."""
    win = Path("C:/Windows/Fonts")
    files = (("Nirmala.ttf", "NirmalaB.ttf", "Nirmala.ttf", "NirmalaB.ttf") if hindi
             else ("arial.ttf", "arialbd.ttf", "ariali.ttf", "arialbi.ttf"))
    faces = dict(zip(("Body", "Body-Bold", "Body-Italic", "Body-BoldItalic"), files))
    if not all((win / f).exists() for f in faces.values()):
        return "Helvetica", "Helvetica-Bold"
    for name, f in faces.items():
        pdfmetrics.registerFont(TTFont(name, str(win / f)))
    pdfmetrics.registerFontFamily("Body", normal="Body", bold="Body-Bold",
                                  italic="Body-Italic", boldItalic="Body-BoldItalic")
    return "Body", "Body-Bold"


def make_styles(font, bold):
    body = ParagraphStyle("body", fontName=font, fontSize=BODY, leading=LEADING, textColor=black, allowWidows=0)
    return {
        "h1": ParagraphStyle("h1", fontName=bold, fontSize=9.3, leading=11, textColor=NAVY, spaceBefore=1.5),
        # 8.5 pt, not the reference 7 pt: the line holds only "Q3." now, the user's way to find answers
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
    s = re.sub(r"~~(.+?)~~", r"<strike>\1</strike>", s)
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
        m = re.match(r"!\[([^\]]*)\]\(([^)]+)\)\s*$", s)
        if m:
            blocks.append(["image", m[2], m[1]])
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
    if isinstance(f, Table):                                # a short table is kept whole
        return h if h <= KEEP_TABLE else sum(f._rowHeights[:2])
    return h if h <= 3 * LEADING + 1 else 2 * LEADING        # 3 lines can't split 2+1


def make_image(path, caption, st, col_w, max_h):
    """A figure kept to the column width, and never taller than the column."""
    img = Image(str(path))
    iw, ih = img.imageWidth, img.imageHeight
    w = col_w
    h = ih * w / iw
    if h > max_h:
        h = max_h
        w = iw * h / ih
    img.drawWidth, img.drawHeight = w, h
    img.hAlign = "CENTER"
    img.spaceBefore, img.spaceAfter = 4, 2
    flow = [img]
    if caption:
        flow.append(Paragraph(inline(caption), st["body"]))
    return flow


def build(blocks, st, col_w, image_base=None, max_h=700):
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
        elif kind == "image":
            path = Path(rest[0])
            if not path.is_absolute():
                path = Path(image_base) / path
            out.extend(make_image(path, rest[1], st, col_w, max_h))
        else:
            t = make_table(rest[0], st, col_w)
            h = t.wrap(col_w, 1e6)[1]
            if h <= KEEP_TABLE and prev not in ("h1", "q", "sub"):
                # keep a short table in one piece, together with a one- or two-line lead-in
                lead = out[-1] if prev == "para" and out[-1].wrap(col_w, 1e6)[1] <= 2 * LEADING + 1 else None
                at = len(out) - 1 if lead else len(out)
                keep = CondPageBreak(h + (lead.wrap(col_w, 1e6)[1] if lead else 0))
                keep.whole = True
                out.insert(at, keep)
            out.append(t)
        prev = kind

    for i, f in enumerate(out):
        if isinstance(f, CondPageBreak) and not getattr(f, "whole", False):
            j = i + 1
            while j < len(out) and getattr(out[j], "heading", False):
                f.height += out[j].wrap(col_w, 1e6)[1] + out[j].getSpaceBefore() + out[j].getSpaceAfter()
                j += 1
            if j < len(out):
                nxt = out[j]  # a kept-whole table (with its lead-in) travels with its heading
                f.height += nxt.height if getattr(nxt, "whole", False) else first_piece(nxt, col_w)
    return out


def render(md, paper="a4", dpi=300, out_dir=None, scale=SCALE, columns=COLUMNS, name=None):
    md = Path(md)
    name = name or (md.parent.name if md.stem == "answers" else md.stem)
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
    text = md.read_text(encoding="utf-8")
    hindi = bool(re.search("[ऀ-ॿ]", text))
    st = make_styles(*register_fonts(hindi))
    for style in st.values():
        style.shaping = int(hindi)  # HarfBuzz puts Hindi vowel signs and joined letters in place
    frame_h = h - mt - mb - 8
    doc.build(build(parse(text), st, col_w, md.parent, frame_h))

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
    ap.add_argument("--name", help="output file name (default: the paper folder); e.g. <folder>-single")
    a = ap.parse_args()
    pdf, pngs = render(a.md, a.paper, a.dpi, a.out, a.scale, a.columns, a.name)
    print(f"{pdf}  ({len(pngs)} page{'s' * (len(pngs) != 1)})")
    for p in pngs:
        print(p)
