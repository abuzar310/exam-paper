# Exam Paper: how to work in this repo

The user sends notes, then a question paper. You answer the paper in their fixed format
and hand back a PDF plus PNG pages. Read README.md for the folder layout and the
answer-file syntax.

Start every session by reading PROJECT_CONTEXT.md (the standing context) and TASKS.md
(what is open). Before you finish, update TASKS.md with what you did and what is left.

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
4b. **Website**: run `python site/build.py` so the new paper appears on https://exam-paper-bcom.vercel.app/ (and the GitHub Pages copy) once it reaches `main`. A new subject folder must start with one of the prefixes in `site/subjects.json`; a new question paper goes in that file's `question_papers` list.
5. **Hand over** with SendUserFile: the PDF and the PNGs. Before that, ask whether to add 3 blank pages (the rule below). Do not skip the question.
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
  Choice questions ("answer any 10 of 12", "any 6 of 8"): answer **only the first N**
  in paper order and skip the rest (the user's rule, 2026-11-02).

## Which shape, by subject (the user's call, 2026-11-06)

The 2 / 5 / 10 point layout above is for HRM-style theory papers. Two subjects differ:

- **Accounting standards:** follow the notes. A theory answer opens with a short paragraph, then points where the standard itself lists items (benefits, types, conditions, methods, levels). A problem is a working and a table, with one line for the result. Do not force exactly 5 or exactly 10 points.
- **English:** paragraphs. Short notes and long answers are written in prose, the way the English notes are written. Do not turn them into numbered points.

## Size: the user prints 9-in-1

The user prints 9 pages per A4 sheet (each page shrinks to ~0.31). History, all on
2026-11-02: 1× (8.5 pt answers) printed at 2.8 pt, blurred. 2.2× was "too big, more
pages"; 1.8× readable but 12–14 pages for what was 4; 1.6× gave 9 pages. One column was
rejected: two columns per page is the user's rule ("1 sheet divided into 2"). The user
then said only the answers matter (question numbers and section titles just need to be
identifiable) and chose **10 pt answer text in the original layout** (`SCALE` 1): the
HRM answers take 5 pages, about 3.2 pt on the 9-in-1 sheet, sent for a test print.
Don't change the size or columns without asking.

## Three blank pages (the user's call, 2026-11-06)

When a PDF is ready, ask in the same message: "Add 3 blank white pages at the end for printing?" Add them only after the user says yes. The blanks are empty A4 pages so one print job is easy to tell apart from the next. Never add them silently. Leave the type size, columns, and the answer pages as they are. The PNG previews stay of the answer pages only.

## Hindi papers

Write Hindi answers in Devanagari as usual. `render.py` sees the Devanagari, switches to
Windows' Nirmala UI font (Arial has no Hindi letters) and turns on HarfBuzz shaping
(`uharfbuzz` in requirements.txt). Without shaping, vowel signs land in the wrong place
("किसी" prints as "कसिी"), so check that `uharfbuzz` imports before rendering Hindi.

## Don't change the look by accident

Colours, sizes and spacing in `render.py` were measured off the reference pages in
`samples/hrm-question-bank/reference/` (Letter, 1236 × 1600 px). Deliberate changes
since: answer text 10 pt with 12.05 pt lines and 12.8 pt hanging indent (was 8.5 /
10.25 / 10.9), the question line 8.5 pt (it holds only the number now), table text
7.4 pt (was 6.45), and a table's first column widens to fit its longest word. After any
change to `render.py`, re-render `samples/hrm-question-bank/numbers-only.md` (the real
format) and `answers.md`, look at the pages, and make sure no column ends with a
question number or sub-heading. To judge the 9-in-1 print, put the PDF pages 3×3 on A4
at 300 DPI and read a crop at 1:1.
