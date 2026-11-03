#!/usr/bin/env python3
"""Single-column English notes PDF only. Does not change render.py or answer sheets.

    python notes/english/render_combined.py
"""
import io
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

import pymupdf
from reportlab.lib.colors import black, white
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import (BaseDocTemplate, CondPageBreak, Frame, HRFlowable, PageBreak,
                                PageTemplate, Paragraph)

import render as exam

# Larger than the answer sheets (body 10 pt, question line 8.5 pt), for reading these notes.
BODY, LEADING, INDENT = 13, 17, 16
Q_SIZE, Q_LEADING = 15, 19
H1_SIZE, SUB_SIZE = 18, 13

# Chapter titles (#) always start a page. These question-level titles do too.
# "Answer the following" stays with the chapter title so that page is not left blank.
MAJOR = re.compile(
    r"^(0\d\.\s|Unit\b|Part\b|SHORT NOTES\b|\d+\.\s+[A-Z][A-Z /()]{5,}|[IVX]{1,4}\.\s+[A-Z])"
)


def styles(font, bold):
    body = ParagraphStyle("body", fontName=font, fontSize=BODY, leading=LEADING, textColor=black,
                          spaceAfter=7, allowWidows=0, allowOrphans=0)
    answer = ParagraphStyle("answer", parent=body, leftIndent=8)
    return {
        "h1": ParagraphStyle("h1", fontName=bold, fontSize=H1_SIZE, leading=H1_SIZE + 4,
                             textColor=exam.NAVY, spaceBefore=0, spaceAfter=2),
        "q": ParagraphStyle("q", fontName=bold, fontSize=Q_SIZE, leading=Q_LEADING,
                            textColor=exam.QBLUE, spaceBefore=12, spaceAfter=1),
        "sub": ParagraphStyle("sub", fontName=bold, fontSize=SUB_SIZE, leading=SUB_SIZE + 3,
                              textColor=exam.QBLUE, spaceBefore=8, spaceAfter=2),
        "body": answer,
        "item": ParagraphStyle("item", parent=answer, leftIndent=INDENT + 8, firstLineIndent=-INDENT),
        "th": ParagraphStyle("th", fontName=bold, fontSize=11, leading=14, textColor=white),
        "td": ParagraphStyle("td", fontName=font, fontSize=11, leading=14, textColor=black),
        "td1": ParagraphStyle("td1", fontName=bold, fontSize=11, leading=14, textColor=black),
    }


def build(blocks, st, col_w):
    """Chapter and major-section titles start a new page. A question moves with its answer
    when the rest of the page is too short to hold the heading and the opening lines."""
    out, prev = [], None
    seen_h1 = False
    body_since_h1 = 0
    broke_in_chapter = False
    for kind, *rest in blocks:
        title = rest[0] if kind in ("h1", "q", "sub") else ""
        if kind == "h1":
            if seen_h1:
                out.append(PageBreak())
            seen_h1 = True
            body_since_h1 = 0
            broke_in_chapter = False
        elif kind == "q" and MAJOR.match(title) and (broke_in_chapter or body_since_h1 >= 2):
            # A new section starts on a fresh page. The first section stays with the chapter title.
            out.append(PageBreak())
            broke_in_chapter = True
        elif kind in ("q", "sub") and prev not in ("h1", "q", "sub"):
            out.append(CondPageBreak(0))
        if kind == "h1":
            out += exam.heading(
                Paragraph(exam.inline(title), st["h1"]),
                HRFlowable(width="100%", thickness=2.2, color=exam.NAVY, spaceBefore=4, spaceAfter=8))
        elif kind == "q":
            out += exam.heading(
                Paragraph(exam.inline(title), st["q"]),
                HRFlowable(width="100%", thickness=0.8, color=exam.GREY, spaceBefore=1, spaceAfter=6))
        elif kind == "sub":
            out += exam.heading(Paragraph(exam.inline(title), st["sub"]))
        elif kind == "para":
            out.append(Paragraph(exam.inline(rest[0]), st["body"]))
        elif kind == "item":
            mark = "•" if rest[0] in "-*•" else rest[0]
            out.append(Paragraph(f"<b>{mark}</b> {exam.inline(rest[1])}", st["item"]))
        else:
            out.append(exam.make_table(rest[0], st, col_w))
        if kind in ("para", "item", "table"):
            body_since_h1 += 1
        prev = kind

    for i, f in enumerate(out):
        if isinstance(f, CondPageBreak):
            j = i + 1
            while j < len(out) and getattr(out[j], "heading", False):
                f.height += out[j].wrap(col_w, 1e6)[1] + out[j].getSpaceBefore() + out[j].getSpaceAfter()
                j += 1
            # Keep the heading with a readable opening of the answer, not two stranded lines.
            if j < len(out):
                f.height += min(out[j].wrap(col_w, 1e6)[1], 6 * LEADING)
    return out


def main():
    md = Path(__file__).resolve().parent / "combined-notes.md"
    out_dir = md.parent / "output"
    out_dir.mkdir(parents=True, exist_ok=True)
    name = "combined-notes"
    for old in out_dir.glob(f"{name}-page-*.png"):
        old.unlink()
    pdf = out_dir / f"{name}.pdf"

    page_w, page_h = A4
    mx, mt, mb = 36, 36, 36
    col_w = page_w - 2 * mx
    frame = Frame(mx, mb, col_w, page_h - mt - mb, id="col0",
                  leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0)
    small = io.BytesIO()
    doc = BaseDocTemplate(small, pagesize=A4, pageTemplates=[PageTemplate(frames=[frame])])
    text = md.read_text(encoding="utf-8")
    st = styles(*exam.register_fonts(False))
    doc.build(build(exam.parse(text), st, col_w))

    pngs = []
    with pymupdf.open("pdf", small.getvalue()) as src, pymupdf.open() as dest:
        for i in range(len(src)):
            dest.new_page(width=page_w, height=page_h).show_pdf_page(
                pymupdf.Rect(0, 0, page_w, page_h), src, i)
        dest.set_metadata({"title": name})
        dest.save(pdf, garbage=3, deflate=True)
        for i, page in enumerate(dest, 1):
            png = out_dir / f"{name}-page-{i}.png"
            page.get_pixmap(matrix=pymupdf.Matrix(150 / 72, 150 / 72)).save(png)
            pngs.append(png)
    print(f"{pdf}  ({len(pngs)} pages)")


if __name__ == "__main__":
    main()
