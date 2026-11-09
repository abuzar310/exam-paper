# Tasks

Open items first. When a task is finished, move it to Done with the date. Dates are in IST.

## Waiting for Abuzar

- [ ] **Accounting Standards model paper, November 2026:** add 3 blank pages to the print PDF and to the single-column PDF? Asked on 7 November 2026; not answered.
- [ ] **Accounting Standards model paper, Section B:** Q5 (borrowing cost, Rs. 50,00,000 at 10%) and Q6 (lawsuit, AS 29) were left out under the first-four rule. Answer them too?
- [ ] **Branches not merged into `main`** (the solved papers were merged on 9 November 2026):

  | Branch | What it adds |
  | --- | --- |
  | `cursor/corporate-admin-grok-cbe8` | A test answer of Corporate Administration Q.P. 54224 in `papers/corporate-administration-grok-test/`. `main` already has this paper solved, so this branch may not be needed |
  | `cursor/goregaon-notes-merge-cbe8` | Goregaon lesson summary merged with the exam answers |
- [ ] **Old branches already inside `main`:** `as29-notes-md`, `as9-slides-md`, `as-7-notes`, `correlation-regression-md`, `english-54302-answers`, `english-notes-pdf`, `log-tables-md`, `print-blank-ask`, `scan-notes-md`, `sem3-notes`, `spot-check-by-subject`, `stats-papers-md`, `syllabi-photos-md` (all `cursor/…-cbe8`). They hold nothing new and can be deleted when he agrees.

## To collect

- [ ] Notes for AS 2, AS 10, AS 13, the standard-setting process, and the non-company Levels I to IV.
- [ ] Notes for Kannada / Hindi. None sent yet.
- [ ] The real exam dates. The timetable photo lists the subjects in order but no dates.

## To solve

- [ ] Human Resource Development Q.P. 50374.
- [ ] Personality Development Q.P. 54324.

## Done

- 2026-11-06: Accounting Standards I, Q.P. 54323, solved in the notes' shape. Print PDF with 3 blank pages, and a single-column reading copy.
- 2026-11-06: AS 7 full chapter added to `notes/accounting-standards/` on `main`.
- 2026-11-06: Rule added: ask before adding 3 blank pages to a print PDF.
- 2026-11-07: Accounting Standards model paper of 7 November 2026 solved. Print and single-column PDFs.
- 2026-11-08: `PROJECT_CONTEXT.md` and `TASKS.md` added and merged into `main`.
- 2026-11-09: Session record `sessions/2026-11-06-accounting-standards.md` added and merged into `main`.
- 2026-11-09: Business Statistics Q.P. 54322 solved: 1(a)-(j), Q2-Q7, Q10-Q12. Print PDF, 2 pages, no blank pages (his choice). `render.py` now keeps tables up to 300 pt whole, with their heading and a short lead-in.
- 2026-11-09: Statistics 54322 theory answers (1(a)-(c), (g)-(i), Q2, Q3) redone in the words of the teacher's notes; Module 4 and the 39-page Statistics notes added to `notes/business-statistics/`.
- 2026-11-09: At his request the Statistics 54322 answers went back to the first version (standard textbook wording). The teacher's notes stay in `notes/business-statistics/`.
- 2026-11-09: Merged into `main` at his request: `as-54323-answers`, `as-model-nov-2026`, `english-model-nov-2026`, `corporate-accounting-54321`, `stats-54322-answers`. Website added: `index.html`, `site/` (builder, catalogue, thumbnails), GitHub Pages from `main`.
- 2026-11-09: Website on Vercel at https://bcom3.vercel.app/ (project `exam-paper-bcom`, old account, auto-deploys `main`). Every solved paper now has both versions (two-column print and single column), each with PDF and full-quality PNG downloads; single-column copies rendered for Statistics 54322, Corporate Accounting 54321 and Corporate Administration 54224. `render.py --name` added.
- 2026-11-09: Camera upload: a floating button on the site photographs question papers; they go to `exam-paper-upload.vercel.app` (new Vercel account, Blob store `exam-paper-uploads`, Mumbai) and show under "Just landed" until `python site/inbox.py done <id>`. Two test uploads are hidden via `site/solved-uploads.json`.
