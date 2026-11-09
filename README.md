# Exam Paper

Solved question papers in one fixed look: blue question numbers, bold point labels,
navy tables. Every paper comes out as a **PDF** and as **high-quality PNG pages**
(300 DPI, 2481 × 3508 px on A4).

**Answer text is 10 pt** (your original pages used 8.5 pt), in the original two-column
layout. Everything else keeps its original size. The HRM answers take 5 pages
(`samples/hrm-question-bank/output/numbers-only.pdf`), one sheet when printed 9-in-1.

The look was copied from the HRM pages in
[samples/hrm-question-bank/reference](samples/hrm-question-bank/reference); the same
answers rebuilt by this project are in
[samples/hrm-question-bank/output](samples/hrm-question-bank/output).

## How it works (the flow)

1. **You send your notes** (photos, PDFs, typed notes, links) for a subject.
   They are saved in `notes/<subject>/`.
2. **You send the question paper.** It is saved in `papers/<subject>-<exam>/`.
3. **Claude writes the answers** in `papers/<subject>-<exam>/answers.md`:
   - first from your notes,
   - then from older solved papers in this repo,
   - and only when your notes don't cover a question, from the internet.

   Each answer is headed by its number only (`Q1.`, `Q2.`), not the question text.
4. **`render.py` makes the PDF and PNGs** in `papers/<subject>-<exam>/output/`.
5. Everything is committed and pushed to GitHub (`abuzar310/exam-paper`), and
   the session is written up in `sessions/`.

## Website

All solved papers and question papers, by subject: **https://exam-paper-bcom.vercel.app/**
(also at https://abuzar310.github.io/exam-paper/)

Vercel (project `exam-paper-bcom`, old account `abuzaarfirooz-4986`) and GitHub Pages both deploy `main` on every push; `vercel.json` ships only `index.html`, `site/` and `papers/`. The page reads `site/catalog.json`,
which `python site/build.py` writes from the `papers/` folder (subjects and question papers
are set in `site/subjects.json`). Run it after rendering a paper, then commit and push.

## Folders

| Folder | What goes there |
|---|---|
| `notes/<subject>/` | Your notes and sources for that subject |
| `papers/<subject>-<exam>/` | One exam: the question paper, `answers.md`, and `output/` (PDF + PNGs) |
| `samples/hrm-question-bank/` | The format sample: your 4 reference pages and the rebuilt copy |
| `sessions/` | What was done in each Claude session |

## Make the PDF and images yourself

Needs Python 3 with `pip install -r requirements.txt` (reportlab, pymupdf).

```
python render.py papers/hrm-sem3-2026/answers.md
```

Options: `--scale 1.6` (draws everything 1.6× bigger, more pages), `--columns 1`
(default 2), `--paper letter` (default A4), `--dpi 200` (default 300),
`--out some/folder`.

## Answer file format

Plain text, one answer file per paper:

```
# 2 MARKS                                   ← section title with the thick blue line
## Q1.                                      ← question number with the thin grey line
**Human Resource Management (HRM)** is the process of ...   ← paragraph

## Q2.
1. **High attrition:** Employees leave quickly for higher pay.   ← numbered point
2. **Work-life balance:** Long working hours ...

## Q3.
| Basis | HRM | Personnel Management |       ← table: first row = navy header
|---|---|---|
| Nature | Modern and proactive | Traditional and reactive |

# 10 MARKS
## Q1.
### Managerial functions                    ← small blue sub-heading
1. **Planning:** ...
### Operative functions
6. **Procurement:** ...

<!-- anything in here is never printed -->
```

`**bold**` and `*italic*` work inside any line. `- ` makes a bullet point.
