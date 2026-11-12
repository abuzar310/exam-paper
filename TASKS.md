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

## To solve

- [ ] Kannada Q.P. 54301 (no Kannada notes yet).
- [ ] Extra Business Statistics papers: Q.P. 24CC72, BBA 56421, BBA 36220, older Fundamentals of Statistics papers.

## Done

- 2026-11-12: Personality Development question bank (Daneial D, B.Com. 3.5; photos sent in chat) solved in full: Section A 1-22, Section B 1-18, from the short notes. Single column only (4 pages; the two-column copy deleted at his request, 2026-11-12). On the site as "Personality Development Question Bank", with the photos under question papers. No blank pages (his choice).

- 2026-11-12: HRD notes added: full Module 3 notes (`module-3.pdf/.md`) and Modules 4-5 (`module-4-5.pdf/.md`). Both HRD papers now follow the notes' wording where textbook points were used: model exam A8-A10, B5, B6, C3 point 9, C4; Q.P. 50374 1(h), 1(j), Q6, Q7. 50374 still 2 print pages, model exam 3.
- 2026-11-12: Real exam dates checked against Davangere University's final UG timetable (Nov/Dec 2026, SEP): HRD 50374 25 Nov 2-5 pm; PD 54324 28 Nov 9:30-11:30; Kannada 54301 1 Dec 9:30-12:30; Hindi 54303 3 Dec; English 54302 5 Dec; Corporate Accounting 54321 8 Dec; Statistics 54322 10 Dec; Accounting Standards 54323 12 Dec (all 9:30-12:30 unless noted).
- 2026-11-12: HRD model exam of 12 November 2026 (Don Bosco, photo sent in chat; the site upload never arrived) solved: A Q1-Q10, B Q1-Q6, C Q1-Q4 (the paper's "any five / any four" do not match 6 x 5 and 3 x 10, so the larger number). Print 3 pages, single column 3. Training need analysis, outbound/attitudinal training and balanced scorecard from standard textbook points.
- 2026-11-10: Business Statistics 54322 Q4-Q12 redone in a friend's solved methods (photos in `notes/business-statistics/friend-54322/`); Q8 (subdivided bar diagram, drawn as `q8-bar-diagram.png`) and Q9 (tally table) added. His slips fixed: Q10 median 32 (not 30.61) so mode 14.67, Q11 σ 12.42 / CV 38.82%, Q12 r 0.983 / PE 0.0082. Print copy still 2 pages, single column 4. `render.py` now prints `~~text~~` struck through (tally gates).
- 2026-11-10: Human Resource Development Q.P. 50374 (2 pages) and Personality Development Q.P. 54324 (1 page) solved from the notes, both versions, on the website. HRD training types and techniques, HRD audit and recent trends came from standard textbook points (no notes for Modules 4-5).
- 2026-11-10: website moved to the second Vercel account (project `exam-paper-bcom`, scope `abuzar26`); bcom3.vercel.app and exam-paper-bcom.vercel.app point there. Pushes no longer deploy it: run the deploy command in README.md after each push.
- 2026-11-09: owner-only admin sign-in at bcom3.vercel.app/#/admin (remove Just landed papers, hide/show any paper). Password stored only as a hash on Vercel.
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
- 2026-11-09: Upload alerts: website banner + tab count + "Alert me" browser notifications (live). Discord alert live: it posts to the Hand Cricket games channel (webhook from `token/discord-webhook-games.env`, saved as `DISCORD_WEBHOOK_URL` on `exam-paper-upload`, his choice).
