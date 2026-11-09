#!/usr/bin/env python3
"""Build the website's catalogue from the papers/ folder.

    python site/build.py

Run it after a paper is solved and rendered, then commit and push: GitHub Pages
serves index.html from the repo root, and the page reads site/catalog.json.

- Solved papers: every papers/<folder>/output/<folder>.pdf. The subject comes from the
  folder name (see the prefixes in site/subjects.json); the title from answers.md.
- Question papers: listed in site/subjects.json. A page range is cut out of the
  combined PDF into site/question-papers/. Photos of a paper (question-paper-*.jpg)
  inside a solved folder are listed too.
- Page images get small thumbnails in site/thumbs/ so the site stays light on a phone.
"""
import json
import re
import subprocess
from datetime import datetime, timedelta, timezone
from pathlib import Path

import pymupdf
from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
SITE = ROOT / "site"
THUMB_W = 360
MONTHS = "January|February|March|April|May|June|July|August|September|October|November|December"


def rel(p):
    return p.relative_to(ROOT).as_posix()


def size_label(p):
    n = p.stat().st_size
    return f"{n / 1_000_000:.1f} MB" if n >= 1_000_000 else f"{max(1, round(n / 1000))} kB"


def updated(p):
    """Date the file was last committed; today for a file not committed yet."""
    out = subprocess.run(["git", "log", "-1", "--format=%cs", "--", rel(p)], cwd=ROOT,
                         capture_output=True, text=True).stdout.strip()
    day = datetime.strptime(out, "%Y-%m-%d") if out else datetime.now()
    return day.strftime("%d %b %Y").lstrip("0")


def pdf_pages(p):
    with pymupdf.open(p) as d:
        return len(d)


def subject_of(folder, subjects):
    hits = [(len(pre), s["id"]) for s in subjects for pre in s["prefixes"] if folder.startswith(pre)]
    return max(hits)[1] if hits else None


def title_of(folder):
    md = folder / "answers.md"
    head = md.read_text(encoding="utf-8")[:1500] if md.exists() else ""
    m = re.search(r"<!--(.*?)-->", head, re.S)
    note = " ".join(m[1].split()) if m else ""
    code = re.search(r"Q\.P\.?\s*(?:code\s*)?:?\s*([0-9]{5})", note, re.I)
    if "model" in note.lower():
        date = re.search(rf"(\d{{1,2}} )?({MONTHS}) (\d{{4}})", note)
        title = "College model exam" + (f", {date[0]}" if date else "")
    else:
        title = f"Q.P. {code[1]}" if code else folder.name.replace("-", " ").title()
        exam = re.search(rf"({MONTHS}) (\d{{4}})\s*/\s*({MONTHS}) (\d{{4}})|({MONTHS})\s*/\s*({MONTHS}) (\d{{4}})|({MONTHS}) (\d{{4}})", note)
        if exam:
            title += ", " + re.sub(r"\s*/\s*", " / ", exam[0])
    return title, answered(note)


def answered(note):
    """The 'Choice rule' line of answers.md, cut down to the part a classmate needs."""
    m = re.search(r"Choice rule:\s*(.*)", note)
    if not m:
        return ""
    rule = m[1]
    abc = re.search(r"A:\s*(.*?)\.\s*B:\s*(.*?)\.\s*C:\s*(.*?)\.", rule)
    if abc:
        return f"Answered: Section A {abc[1]}, Section B {abc[2]}, Section C {abc[3]}."
    sentences = re.findall(r"[^.]+\.", rule)
    keep = [s.strip() for i, s in enumerate(sentences) if i == 0 or s.strip().startswith("Section")]
    text = " ".join(keep)
    if text and not text.startswith("Section"):
        text = text[0].lower() + text[1:]
    return "Answered: " + text if text else ""


def thumbs_for(folder, name):
    out = folder / "output"
    pages = sorted(out.glob(f"{name}-page-*.png"), key=lambda p: int(p.stem.rsplit("-", 1)[1]))
    items = []
    for png in pages:
        t = SITE / "thumbs" / name / (png.stem.rsplit("-", 1)[1] + ".webp")
        if not t.exists() or t.stat().st_mtime < png.stat().st_mtime:
            t.parent.mkdir(parents=True, exist_ok=True)
            with Image.open(png) as im:
                im = im.convert("RGB")
                im.thumbnail((THUMB_W, THUMB_W * 2))
                im.save(t, "WEBP", quality=72)
        items.append({"full": rel(png), "thumb": rel(t)})
    return items


def cut_pages(src, first, last, dest):
    if dest.exists() and dest.stat().st_mtime >= src.stat().st_mtime:
        return
    dest.parent.mkdir(parents=True, exist_ok=True)
    with pymupdf.open(src) as d, pymupdf.open() as out:
        out.insert_pdf(d, from_page=first - 1, to_page=last - 1)
        out.save(dest, garbage=3, deflate=True)


def build():
    cfg = json.loads((SITE / "subjects.json").read_text(encoding="utf-8"))
    groups = cfg["subjects"] + cfg["earlier"]
    catalogue = {g["id"]: {**{k: g[k] for k in g if k != "prefixes"}, "solved": [], "questions": []} for g in groups}

    for folder in sorted(p for p in (ROOT / "papers").iterdir() if p.is_dir()):
        pdf = folder / "output" / f"{folder.name}.pdf"
        sid = subject_of(folder.name, groups)
        if not pdf.exists() or not sid:
            continue
        title, choice = title_of(folder)
        single = folder / "output" / f"{folder.name}-single.pdf"
        catalogue[sid]["solved"].append({
            "title": title,
            "answered": choice,
            "pdf": rel(pdf), "pdf_pages": pdf_pages(pdf), "pdf_size": size_label(pdf),
            "single": rel(single) if single.exists() else None,
            "images": thumbs_for(folder, folder.name),
            "updated": updated(pdf),
        })
        photos = sorted(p for p in folder.iterdir() if re.match(r"question-paper-\d+\.(jpe?g|png|webp)$", p.name, re.I))
        if photos:
            catalogue[sid]["questions"].append({"title": f"{title} (photo)", "photos": [rel(p) for p in photos]})

    for q in cfg["question_papers"]:
        src = ROOT / q["source"]
        if not src.exists():
            continue
        if "pages" in q:
            first, last = q["pages"]
            slug = re.sub(r"[^a-z0-9]+", "-", q["title"].lower()).strip("-")[:60]
            dest = SITE / "question-papers" / f"{slug}.pdf"
            cut_pages(src, first, last, dest)
            src = dest
        catalogue[q["subject"]]["questions"].append(
            {"title": q["title"], "pdf": rel(src), "pdf_pages": pdf_pages(src), "pdf_size": size_label(src)})

    ist = datetime.now(timezone(timedelta(hours=5, minutes=30)))
    data = {"built": ist.strftime("%d %B %Y, %I:%M %p IST"),
            "subjects": [catalogue[s["id"]] for s in cfg["subjects"]],
            "earlier": [catalogue[s["id"]] for s in cfg["earlier"]]}
    (SITE / "catalog.json").write_text(json.dumps(data, indent=1, ensure_ascii=False), encoding="utf-8")
    solved = sum(len(s["solved"]) for s in data["subjects"] + data["earlier"])
    qs = sum(len(s["questions"]) for s in data["subjects"] + data["earlier"])
    print(f"site/catalog.json: {solved} solved papers, {qs} question papers")


if __name__ == "__main__":
    build()
