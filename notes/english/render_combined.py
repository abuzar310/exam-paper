#!/usr/bin/env python3
"""Temporary layout for the combined English notes only.

This is not the answer-sheet format. render.py is not used for these pages
and is left unchanged. Answer sheets stay two-column, 10 pt, 8.5 pt questions.

    python notes/english/render_combined.py

Textbook choices applied here (USWDS typography, KIT book layout, legibility research):
- one size step of at least 2 pt between chapter, question, subheading, and body
- line spacing about 1.4, paragraphs separated by space, not indents
- line length kept near 70 characters by wider side margins
- ragged right, so gaps in the line do not look like a texture
- more space above a heading than below it
- a question stays with the start of its answer
- each of the seven notes is one chapter: a new page, then one continuous section
- each answer ends with a short rule so the next question does not run into it
"""
import io
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

import pymupdf
from reportlab.lib.colors import white
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import (BaseDocTemplate, CondPageBreak, Frame, HRFlowable, PageBreak,
                                PageTemplate, Paragraph, Spacer)

import render as exam

INK = exam.HexColor("#1A1A1A")
NAVY = exam.HexColor("#14375C")
RULE = exam.HexColor("#8AA0B5")
# Chapter 22, question 18, subheading 15, body 13. Each step is at least 2 pt.
BODY, LEADING, INDENT = 13, 18, 16
CHAPTERS = (
    "Kirubunkal summary",
    "SEP III Sem English notes",
    "On the Way to Goregaon",
    "Harvest II workbook",
    "Model business letters",
    "The Overcoat",
    "Kirubunkal",
)


def styles(font, bold):
    body = ParagraphStyle(
        "body", fontName=font, fontSize=BODY, leading=LEADING, textColor=INK,
        spaceBefore=0, spaceAfter=11, alignment=0, allowWidows=0, allowOrphans=0)
    return {
        "h1": ParagraphStyle(
            "h1", fontName=bold, fontSize=22, leading=26, textColor=white,
            backColor=NAVY, borderPadding=10, spaceBefore=0, spaceAfter=14),
        "q": ParagraphStyle(
            "q", fontName=bold, fontSize=18, leading=22, textColor=white,
            backColor=NAVY, borderPadding=8, spaceBefore=14, spaceAfter=10),
        "sub": ParagraphStyle(
            "sub", fontName=bold, fontSize=15, leading=19, textColor=NAVY,
            spaceBefore=12, spaceAfter=3),
        "body": body,
        "item": ParagraphStyle(
            "item", parent=body, leftIndent=INDENT, firstLineIndent=-INDENT,
            spaceBefore=2, spaceAfter=4),
        "th": ParagraphStyle("th", fontName=bold, fontSize=12, leading=15, textColor=white),
        "td": ParagraphStyle("td", fontName=font, fontSize=12, leading=16, textColor=INK),
        "td1": ParagraphStyle("td1", fontName=bold, fontSize=12, leading=16, textColor=INK),
    }


def answer_end():
    """A short rule closes the answer so the next question starts as a new block."""
    return [
        Spacer(1, 4),
        HRFlowable(width="28%", thickness=1.25, color=NAVY, spaceBefore=2, spaceAfter=14, hAlign="LEFT"),
    ]


def build(blocks, st, col_w):
    """One chapter is one section. Questions are large, and each answer closes before the next."""
    out, prev = [], None
    seen_h1 = False
    answered = False
    for kind, *rest in blocks:
        title = rest[0] if kind in ("h1", "q", "sub") else ""
        if kind == "h1":
            if seen_h1:
                out.append(PageBreak())
            seen_h1 = True
            answered = False
        elif kind == "q" and answered:
            out.extend(answer_end())
            answered = False
        if kind in ("q", "sub") and prev not in ("h1", "q", "sub"):
            out.append(CondPageBreak(0))
        if kind == "h1":
            out += exam.heading(Paragraph(exam.inline(title), st["h1"]))
        elif kind == "q":
            out += exam.heading(Paragraph(exam.inline(title), st["q"]))
        elif kind == "sub":
            out += exam.heading(Paragraph(exam.inline(title), st["sub"]))
        elif kind == "para":
            out.append(Paragraph(exam.inline(rest[0]), st["body"]))
            answered = True
        elif kind == "item":
            mark = "•" if rest[0] in "-*•" else rest[0]
            out.append(Paragraph(f"<b>{mark}</b> {exam.inline(rest[1])}", st["item"]))
            answered = True
        else:
            out.append(exam.make_table(rest[0], st, col_w))
            answered = True
        prev = kind
    if answered:
        out.extend(answer_end())

    for i, f in enumerate(out):
        if isinstance(f, CondPageBreak):
            j = i + 1
            while j < len(out) and getattr(out[j], "heading", False):
                f.height += out[j].wrap(col_w, 1e6)[1] + out[j].getSpaceBefore() + out[j].getSpaceAfter()
                j += 1
            if j < len(out):
                f.height += min(out[j].wrap(col_w, 1e6)[1], 5 * LEADING)
    return out


MARK = (0.08, 0.22, 0.36)
GOLD = (0.72, 0.52, 0.12)
POTION = (0.42, 0.28, 0.62)


def _spark(page, x, y, r=1.7):
    page.draw_line(pymupdf.Point(x, y - r), pymupdf.Point(x, y + r), color=GOLD, width=0.7)
    page.draw_line(pymupdf.Point(x - r, y), pymupdf.Point(x + r, y), color=GOLD, width=0.7)


def _hat(page, x, y):
    """Wizard hat with three sparks. x, y is the top-left of a 16 by 14 box."""
    page.draw_polyline(
        [pymupdf.Point(x + 1, y + 11), pymupdf.Point(x + 8, y + 1), pymupdf.Point(x + 15, y + 11)],
        color=MARK, fill=MARK, width=0.3, closePath=True)
    page.draw_line(pymupdf.Point(x - 1, y + 12.5), pymupdf.Point(x + 17, y + 12.5), color=MARK, width=1.5)
    _spark(page, x + 18, y + 3, 1.5)
    _spark(page, x + 22, y + 8, 1.2)
    _spark(page, x - 3, y + 6, 1.2)


def _potion(page, x, y):
    """Tiny corked bottle. x, y is the top-left of a 12 by 16 box."""
    page.draw_rect(pymupdf.Rect(x + 4, y, x + 8, y + 3), color=(0.45, 0.28, 0.12),
                   fill=(0.55, 0.36, 0.16), width=0.3)
    page.draw_rect(pymupdf.Rect(x + 4.4, y + 3, x + 7.6, y + 6), color=MARK,
                   fill=(0.90, 0.94, 0.97), width=0.4)
    page.draw_oval(pymupdf.Rect(x + 1, y + 6, x + 11, y + 16), color=MARK,
                   fill=(0.86, 0.90, 0.96), width=0.6)
    page.draw_oval(pymupdf.Rect(x + 2.2, y + 10, x + 9.8, y + 15.2), color=POTION,
                   fill=POTION, width=0.2)


def stamp(doc):
    """Footer mark on every page: hat, 'brewed by Abuzar', potion, then the chapter and page."""
    chapter = ""
    for page in doc:
        head = page.get_text()[:500]
        for name in CHAPTERS:
            if name in head:
                chapter = name
                break
        y = page.rect.height - 28
        page.draw_line(pymupdf.Point(48, y - 10), pymupdf.Point(page.rect.width - 48, y - 10),
                       color=MARK, width=0.4)
        _hat(page, 50, y - 6)
        page.insert_text(pymupdf.Point(78, y + 6), "brewed by Abuzar", fontsize=9,
                         fontname="hebo", color=MARK)
        _potion(page, 172, y - 7)
        page.insert_text(pymupdf.Point(196, y + 6), chapter, fontsize=8, fontname="helv", color=MARK)
        label = str(page.number + 1)
        page.insert_text(pymupdf.Point(page.rect.width - 48 - len(label) * 5.2, y + 6), label,
                         fontsize=9, fontname="helv", color=MARK)


def main():
    md = Path(__file__).resolve().parent / "combined-notes.md"
    out_dir = md.parent / "output"
    out_dir.mkdir(parents=True, exist_ok=True)
    name = "combined-notes"
    for old in out_dir.glob(f"{name}-page-*.png"):
        old.unlink()
    pdf = out_dir / f"{name}.pdf"

    page_w, page_h = A4
    # Wider margins keep a line near 70 characters, the usual textbook measure.
    mx, mt, mb = 54, 42, 48
    col_w = page_w - 2 * mx
    frame = Frame(mx, mb, col_w, page_h - mt - mb, id="col0",
                  leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0)
    small = io.BytesIO()
    doc = BaseDocTemplate(small, pagesize=A4, pageTemplates=[PageTemplate(frames=[frame])])
    text = md.read_text(encoding="utf-8")
    doc.build(build(exam.parse(text), styles(*exam.register_fonts(False)), col_w))

    pngs = []
    with pymupdf.open("pdf", small.getvalue()) as src, pymupdf.open() as dest:
        for i in range(len(src)):
            dest.new_page(width=page_w, height=page_h).show_pdf_page(
                pymupdf.Rect(0, 0, page_w, page_h), src, i)
        stamp(dest)
        dest.set_metadata({"title": "English notes"})
        dest.save(pdf, garbage=3, deflate=True)
        for i, page in enumerate(dest, 1):
            png = out_dir / f"{name}-page-{i}.png"
            page.get_pixmap(matrix=pymupdf.Matrix(200 / 72, 200 / 72), alpha=False).save(png)
            pngs.append(png)
    print(f"{pdf}  ({len(pngs)} pages)")


if __name__ == "__main__":
    main()
