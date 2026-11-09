# Project context

Read this first in every new chat, then `CLAUDE.md` for the full rules and `TASKS.md` for what is open. Update `TASKS.md` before you finish.

## Who and what

- **Student:** Abuzar, III B.Com (third semester), Don Bosco College, Chitradurga, affiliated to Davangere University.
- **Repo:** `abuzar310/exam-paper`. Default branch `main`.
- **Purpose:** keep the semester notes in one place and turn question papers into solved answer PDFs that he prints.
- **Third-semester subjects:** Kannada/Hindi, Corporate Accounting, English, Accounting Standards I, Business Statistics, Human Resource Development, Personality Development.

## How a paper is solved

1. The question paper is saved in `papers/<subject>-<exam>/` with a typed copy, `question-paper.md`.
2. Answers go in `answers.md` in that folder.
3. `python render.py papers/<folder>/answers.md` makes the PDF and 300 dpi PNG pages in `output/`.
4. Every page is looked at before hand-over: no heading alone at the foot of a column, no table cut so a row sits alone, no missing question.
5. The work is committed, pushed, and checked on GitHub before any link is given.

## Rules that must not be lost

- **Sources, in order:** his notes in `notes/<subject>/`, then older answers in this repo, then outside textbooks only where the notes are silent. Never invent a fact, figure or section. Never name the source on the page or in chat.
- **Question line:** the number only, for example `## Q1.` or `## Q1. (a)`. Never the question text.
- **Choice questions:** answer only the first N in paper order. Where the paper says answer all, answer every question printed under that heading.
- **Shape by subject:**
  - Accounting Standards: a short paragraph, then points where the standard itself lists items. A problem is a working table with one result line. Do not force exactly 5 or 10 points.
  - English: paragraphs.
  - HRM-style theory: exactly 5 points for 5 marks, exactly 10 for 10 marks, as in `CLAUDE.md`.
- **Style:** British spelling, short exam English, no filler.
- **Print sheet:** A4, two columns, 10 pt answer text. He prints 9 pages per sheet, so the text ends up about 3.2 pt. Do not change the size or columns without asking.
- **Reading copy:** when he asks for one, render a copy named `<folder>-single` with `--columns 1`. Use `--scale 1.25` only when he asks for larger type.
- **Printing:** send the PDF, not the PNGs. PNG text is a picture and goes soft when nine pages share a sheet.
- **Three blank pages:** each time a PDF is ready, ask: "Add 3 blank white pages at the end for printing?" Add them only after he says yes.
- **Links:** never give a GitHub link until the push is done and the link has been opened without logging in. One link that 404'd has already cost his trust.
- **Commits:** as `Abuzar <abuzaarfirooz@gmail.com>`, with no AI co-author line. Never leave a token in `.git/config`.
- **Merging:** work on a branch. Merge into `main` only when he asks, and only what he names.
- **Scope:** these files record exam-paper work only. Other projects and general chat stay out.
- **Times:** report them in India time (IST, UTC+5:30).

## Where things are

| Path | What |
| --- | --- |
| `notes/accounting-standards/` | AS 7 (full chapter), AS 9 (slides and study material), AS 16 with AS 19 lease pages, AS 26, AS 28, AS 29, employee benefits, construction-contracts extract |
| `notes/business-statistics/` | Correlation, regression, log and antilog tables; teacher's Module 4 (collection of data, classification) and 39-page Introduction to Statistics (definitions, primary data, tabulation), scanned PDFs with typed `.md` copies |
| `notes/corporate-accounting/` | Profit prior to incorporation, two syllabus scans |
| `notes/english/` | The Overcoat, Kirubunkal, On the Way to Goregaon, Harvest II, semester notes, model letters, combined notes PDF |
| `notes/human-resource-development/` | Modules 1 and 2, Aarav Retail case, syllabus |
| `notes/personality-development/` | Short notes and the question bank |
| `papers/sem3-dec-2025-jan-2026/` | December 2025 / January 2026 papers, combined, plus the timetable |
| `papers/english-sem3-dec-2025/` | English Q.P. 54302, solved |
| `papers/corporate-administration-sem2-may-2026/` | Corporate Administration, second semester, solved |
| `papers/business-statistics/` | Older statistics papers |
| `spot-check.md` | Every markdown copy beside its original, to check by eye |
| `sessions/` | Records of earlier sessions |

The other solved papers are still on their own branches, listed in `TASKS.md`, until they are merged.

## Notes that do not exist yet

AS 2 (inventories), AS 10 (property, plant and equipment; only a short passage is in `as-9-study-material.md`), AS 13 (investments), the standard-setting process, and the non-company Levels I to IV. Answers on these came from outside textbooks.

## Old paper pattern

December 2025 / January 2026, third semester:

- Statistics 54322, HRD 50374, Corporate Accounting 54321, Accounting Standards 54323: 3 hours, 80 marks. Any 10 two-mark parts, any 6 five-mark questions, any 3 ten-mark questions.
- Personality Development 54324: 2 hours, 40 marks. Any 5 two-mark parts, any 6 five-mark questions.
- English 54302: 3 hours, 80 marks. Any 4 short notes, any 3 long answers, every writing-skills question.

## Pushing from a cloud agent

The Cursor bot account cannot push to this repo; a plain `git push` returns 403. A push needs his own GitHub access. After any push, check the branch on GitHub and open the file link without logging in before sharing it.
