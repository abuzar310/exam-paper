# Exam Paper

Solved question papers in one fixed look: blue question numbers, bold point labels,
navy tables. Every paper comes out as a **PDF** and as **high-quality PNG pages**
(300 DPI, 2481 × 3508 px on A4).

**Sized for 9-in-1 printing.** You print 9 pages on one A4 sheet, which shrinks each
page to about a third. Pages keep two columns, and the text is 1.6× the original size,
just big enough to read after that (about 4.2 pt on paper). The original size printed
at 2.8 pt and could not be read. The HRM answers fit on 9 pages = one sheet.

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
5. Everything is committed and pushed to GitHub (`abuzar310/exam-paper`, private), and
   the session is written up in `sessions/`.

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

Options: `--scale 1.8` (text size; default 1.6, bigger = easier to read but more
pages), `--columns 1` (default 2), `--paper letter` (default A4), `--dpi 200`
(default 300), `--out some/folder`. `--scale 1` gives the original small pages.

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
