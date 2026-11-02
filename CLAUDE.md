# Exam Paper: how to work in this repo

The user sends notes, then a question paper. You answer the paper in their fixed format
and hand back a PDF plus PNG pages. Read README.md for the folder layout and the
answer-file syntax.

## The flow, every time

1. **Notes arrive** → save the originals untouched in `notes/<subject>/` (kebab-case
   subject, e.g. `hrm`, `financial-accounting`). For photos or scanned PDFs, also write
   a text copy next to them (`unit-2.jpg` → `unit-2.md`) so later sessions can search
   the notes without re-reading images.
2. **Question paper arrives** → make `papers/<subject>-<exam>/` (e.g.
   `papers/hrm-sem3-nov-2026/`), save the paper there as `question-paper.<ext>`.
   Read every question; keep the paper's own question numbers and section order.
3. **Write `answers.md`** in that folder (rules below).
4. **Render**: `python render.py papers/<folder>/answers.md` → `output/<folder>.pdf`
   and `output/<folder>-page-N.png` (A4, 300 DPI). Look at every PNG before handing
   it over: no heading stranded at a page bottom, no table cut badly, no missing
   question.
5. **Hand over** with SendUserFile: the PDF and the PNGs.
6. **Save**: write `sessions/<date>-<topic>.md` (what was asked, what was made).
   For the full step list, export this session (export_transcript "self"),
   unzip it to the scratchpad and run
   `python sessions/to_md.py <unzipped>/transcript.jsonl sessions/<date>-<topic>-transcript.md "<title>"`.
   Never commit the raw export (it holds images and private system text).
   Then commit and push to `origin main` (`abuzar310/exam-paper`, private).
   Commit as `Abuzar <abuzaarfirooz@gmail.com>` via GIT_AUTHOR_*/GIT_COMMITTER_* env
   vars, no AI co-author trailer.

## Where answers come from (in this order)

1. The user's notes in `notes/<subject>/`. Use their wording and their points.
2. Earlier answers in this repo (`papers/*/answers.md`, `samples/*/answers.md`).
3. Only if neither covers the question: the internet (standard Indian university
   textbook answers). Never invent facts, sections or case laws.

Don't mark or mention sources, on the page or in chat (the user's call, 2026-11-02).

## How answers look (copy samples/hrm-question-bank/answers.md)

- **2 marks**: a 2–3 sentence definition that opens with the **bold term**
  ("**Recruitment** is the process of ..."). If the question says "any two", give
  exactly 2 numbered points instead.
- **5 marks**: exactly 5 numbered points, each `N. **Short label:** one sentence`
  (one or two printed lines).
- **10 marks**: exactly 10 numbered points. When the topic splits naturally
  (internal/external, causes/settlement, traditional/modern, on-the-job/off-the-job),
  put a `###` sub-heading over each half and keep counting 1–10 across both.
- **Differences / distinguish / compare**: a table with a `Basis` first column.
  2 marks → 2 rows, 5 marks → 5 rows, 10 marks → 8–10 rows. Add an `Example` row when
  the question asks for examples.
- Simple exam English, short sentences, British spelling (organisation, labour,
  programme). No filler intros or conclusions; the page is meant to be crammed.
- Section titles: the paper's own (e.g. `# SECTION A`) if it has them, else
  `# 2 MARKS`, `# 5 MARKS`, `# 10 MARKS`.
- Question line = the number only: `## Q3.` (parts as on the paper, `## Q3. (a)`).
  Never copy the question text; the user matches answers to the paper by number.
  (The sample has full question text only because it rebuilds the user's old pages.)
  For "answer any N of M" papers, answer all of them unless the user says otherwise.

## Size: the user prints 9-in-1

The user prints 9 pages per A4 sheet (each page shrinks to ~0.31). History, all on
2026-11-02: 1× printed at 2.8 pt, unreadable. 2.2× was "too big, more pages". 1.8× was
readable but 12–14 pages for what was 4. One column was rejected: two columns per page
is the user's rule ("1 sheet divided into 2"). Now 1.6× with 9.8 pt leading and two
columns (≈ 4.2 pt on paper): the HRM answers fit 9 pages = one sheet. Pages grow with
scale², so don't change the size or columns without asking. Margins and the column gap
stay their reference size on paper.

## Don't change the look by accident

Colours, sizes and spacing in `render.py` were measured off the reference pages in
`samples/hrm-question-bank/reference/` (Letter, 1236 × 1600 px). Deliberate changes
since: the question line is 8.5 pt (it holds only the number now), table text 7.4 pt
(was 6.45), line spacing 9.8 pt (was 10.25), and a table's first column widens to fit
its longest word. After any change to `render.py`, re-render the sample with
`python render.py samples/hrm-question-bank/answers.md --scale 1 --paper letter --dpi 145.41 --out <scratch>`
and compare it with the reference pages side by side before committing. To check the
printed result, put the PDF pages 3×3 on A4 at 300 DPI, read a crop at 1:1, and make
sure no column ends with a question number or sub-heading.
