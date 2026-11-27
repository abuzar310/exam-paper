# Tasks

Open items first. When a task is finished, move it to Done with the date. Dates are in IST.

## Waiting for Abuzar

- [ ] **Accounting Standards model paper, Section B:** Q5 (borrowing cost, Rs. 50,00,000 at 10%) and Q6 (lawsuit, AS 29) were left out under the first-four rule. Answer them too?
- [ ] **Branches not merged into `main`** (the solved papers were merged on 9 November 2026):

  | Branch | What it adds |
  | --- | --- |
  | `cursor/corporate-admin-grok-cbe8` | A test answer of Corporate Administration Q.P. 54224 in `papers/corporate-administration-grok-test/`. `main` already has this paper solved, so this branch may not be needed |
  | `cursor/goregaon-notes-merge-cbe8` | Goregaon lesson summary merged with the exam answers |
- [ ] **Old branches already inside `main`:** `as29-notes-md`, `as9-slides-md`, `as-7-notes`, `correlation-regression-md`, `english-54302-answers`, `english-notes-pdf`, `log-tables-md`, `print-blank-ask`, `scan-notes-md`, `sem3-notes`, `spot-check-by-subject`, `stats-papers-md`, `syllabi-photos-md` (all `cursor/…-cbe8`). They hold nothing new and can be deleted when he agrees.

## To collect

- [ ] Notes for AS 2, AS 10, AS 13, the standard-setting process, and the non-company Levels I to IV.
- [ ] Hindi textbook: contents page, Do Kalakar, Rajrani Sita, माँ, and the Bank essay. Send as photos in chat (batches of about 6–10 pages), not one giant file. Asked 18 Nov 2026.

- [ ] Old Davangere papers for prediction: NEP 3rd-semester B.Com and BBA papers (2023–2025), any May/June 2026 supplementary 3rd-semester papers, and BBA HRM papers. Ask seniors or the college library; none are online. Asked 20 Nov 2026. See `research/pyq-repeat-check.md`.

## To solve

- सूखी डाली: the retaken photos (`notes/hindi/ekanki-kunj-retake.pdf`) are sharper; re-reading its left-hand pages 130–150 would clear most `[?]` marks. Optional: every exam line was already read clearly.
- Predicted papers made for all subjects (HRD, Corporate Accounting, Personality Development, English, Business Statistics, Accounting Standards, Hindi).

## Done

- 2026-11-27: Solved HRD Q.P. 50374 (November / December 2026), first choices in each section. Saved the original upload, upright paper, English transcription and both answer layouts.

- 2026-11-27: Removed the semester schedule dates from the current question sheets, generated PDFs, notes and session transcripts on the cleanup branch. Git history cleanup and GitHub publication are pending.

- 2026-11-24: "Predicted Questions" for all seven subjects (`papers/<subject>-predicted-questions/`), replacing the Important Questions docs (all deleted) and the old HRD prediction list. Each has a question paper (questions only, tagged [PYQ] / [College] / [Predicted]) and an answers-only sheet in two columns and single column. Short answers: 2 marks = short definition, 5 = 5 points (heading + one line), 10 = 10 one-line points; English and Hindi = short paragraphs, letters kept whole; problems = full working. Accounting Standards keeps the standard's own lists whole. Two-column pages: HRD 8, PD 4, Hindi 7, English 7, CA 9, Statistics 5, AS 6. Newly solved along the way: CA 54321 Q13 (Rohit Ltd. balance sheet, 17,80,000) and Q14 (Sources Ltd., pre 38,300 / post 81,700); Statistics 54322 Q13 (regression) and Q14 (primary data), A(k), A(l); AS 54323 Q8 (actual return 2,60,000), Q9 (revenue 10,41,000), Q13 (gratuity, projected unit credit), Q14 (Yodha, loss 17,50,000), college B5 (3,25,000) and B6 (provision 6,00,000). The old Statistics important-questions doc had answers to the wrong data for C Q13/Q14 and B Q8; not reused. CA mock paper renamed to `corporate-accounting-predicted-paper`. All deployed to bcom3 and checked live. Branch not yet merged into `main` (GitHub Pages behind, along with the offline/website work).
- 2026-11-24: His follow-up: the answer sheets now show a one-line question label after each number (`## Q12. Akaki's office`). Short questions unchanged; long ones (problems, letters) cut to the instruction, e.g. "Rohit Ltd.: Balance Sheet as per Schedule III". His rule for these sheets; the solved-paper sheets still show the number only. Page counts unchanged.
- 2026-11-24: Website lighter and offline (his request; choices: both phones, keep only what is opened, current font self-hosted). Font served from the site (34 kB, no Google). Photo question papers: small previews (Accounting Standards model exam ~10 MB → 177 kB to open) and ~0.3 MB screen copies in the viewer; Download still gives the original. Installable app with offline support (`sw.js`, manifest, icons): opened papers are saved on the phone and marked "Saved on this phone"; offline the site shows a note and hides upload/alerts. Tested in Chromium (Pixel/iPhone emulation): first load 189 kB, saved PDF opens offline.

- 2026-11-24: Branch `claude/blissful-archimedes-xb1i1j` merged into `main` at his request (fast-forward, 34 commits: Hindi textbook and corrections, predicted papers, important-questions docs, Statistics expected paper, session history). GitHub Pages now matches bcom3.

- 2026-11-24: Session history saved: `sessions/2026-11-23-predictions-and-important-questions.md` (summary) and `sessions/2026-11-20-to-11-24-session-transcript.md` (full log, Gmail blanked).

- 2026-11-23: Business Statistics expected paper (`papers/business-statistics-expected-paper/`), set "in the shoes of" last year's setter after comparing all nine statistics papers: question paper first, then the answer sheet; problems reused from older papers with their own numbers (as the setter did in 2025); gap topics he skipped (CV consistency, histogram mode, median, functions and limitations, GM/HM). Single column only (his choice), 6 pages. Every figure checked a second way in a script.

- 2026-11-23: मम्मीजी puzzle settled from the retaken photos: she is in no play of एकांकी कुंज (all nine cast lists checked). The teacher's माँ one-liners come from another version; the 2025 paper used that source, so keep her answer विदेश. Recorded in `notes/hindi/ekanki-kunj.md`. Not answered by him and left as is: his choices on per-subject docs only, no further PYQ search (23 Nov).

- 2026-11-23: "Important Questions & PYQ" revision doc for every subject (`papers/<subject>-important-questions/`): the actual Davangere Dec 2025 paper at the top, then the important questions ranked by where they actually appeared ([PYQ] = university paper, [College] = college exam) with answers, all from Davangere-grounded sources (the real paper + Don Bosco college exams + the textbook-checked banks). On the site, single column. His stated priority: PYQ + important questions from Davangere.

- 2026-11-23: Predicted papers for the remaining subjects, each a full mock in its own blueprint, both versions, on the site: Personality Development (54324, 40 marks), English (54302, three texts + writing skills), Business Statistics (54322, computed problems checked in a script), Accounting Standards (54323, all standards + computed problems), Hindi (54303, most-likely items from the bank). render.py now uses Liberation Sans on Linux so x̄/Σ/√ render in cloud PDFs. No blank pages.

- 2026-11-23: HRD predicted **paper** (`papers/human-resource-development-predicted-paper/`): a full exam-style mock in the Q.P. 50374 blueprint (Section A 12 two-markers answer 10, Section B 8 five-markers answer 6, Section C 5 ten-markers answer 3), one per module in C, tiered Very likely/Likely. Answers from the HRD theory bank. Questions-only PDF + answers, both versions, on the site. Companion to the earlier ranked list (kept). No blank pages.

- 2026-11-23: Corporate Accounting predicted questions (`papers/corporate-accounting-predicted-questions/`): full mock paper in the Q.P. 54321 blueprint — Section A 12 two-markers (answer 10), Section B Q2-Q9 (answer 6), Section C Q10-Q14 (answer 3) — one problem per module at 5 and 10 marks, gap topics flagged (goodwill average-profit method, liquidator's final statement). Every figure computed and asserted in a script; conventions match the solved 54321 (notional call, yield formula, firm underwriting, x/(100+x) remuneration). Questions-only PDF plus answers; both versions on the site. No blank pages (his standing choice).

- 2026-11-22: Corporate Accounting teacher's notes saved in `notes/corporate-accounting/` (PDF + text copy each): underwriting-of-shares, liquidation-of-companies, valuation-of-shares-and-goodwill, profit-prior-to-incorporation-teacher. Clean typed notes (meaning, features, methods, formulas, problems). These cover the main Corporate Accounting problem chapters the repo previously had only from textbooks. Use them when solving Q.P. 54321 topics and the Corporate Accounting prediction.

- 2026-11-21: Retaken textbook photos saved (`notes/hindi/ekanki-kunj-retake.pdf`, 84 upright photos, about 1080 px). माँ pp.102–103 transcribed: no मम्मीजी or बलदेव there either, so the teacher's माँ one-markers about them are not from this play. Bank II Q14 ("सच्ची बात…बक-बक") rewritten: मंजु to मनीषी, p.103.

- 2026-11-21: HRD predicted questions now have a questions-only PDF (`question-paper.pdf`, 2 pages), shown as that entry's "Question paper" on the site. A friend's HRD practice paper (not official) was checked: every question is covered by the HRD bank; not solved (his call).

- 2026-11-20: Hindi question bank checked against the textbook and corrected (₹50; राजनाथ; शीला taught रामायण-महाभारत at home; निरंजन an M.A. student, not a lawyer; राजरानी सीता: no gifts, मन्दोदरी gives the तृण and compares रावण with शंकर, "चुप रह दुष्ट"; मोरोपंत पेशवा; माता के समान; माँ by विष्णु प्रभाकर, summary rewritten; बुलाकीदास, चूड़ामणि, मार्तण्ड, निरंजन notes fixed). 11 pages, single column. Not confirmable from the scan and left as the teacher wrote: माँ one-markers about मम्मीजी, बलदेव, मंजु's age (the book's cast list has none of them; pp.102–103 missing). Also fixed in Q.P. 54303: III.2 माता के समान and the last stage direction.

- 2026-11-20: Hindi Q.P. 54303 redone from the textbook एकांकी कुंज: I.1 पचास रुपये (not सात), I.2 "चुप रह दुष्ट!…", I.3 अशोक वाटिका, I.10 माता के समान; II now passages 1, 2, 3 (passage 2 traced: राजरानी सीता p.49, रावण to सीता); II.1 context fixed; III.2 मोरोपंत पेशवा, मेणा; IV.1 मन्दोदरी and IV.2 शीला rewritten from the play (राजनाथ). Both versions 3 pages, rendered in the cloud with Noto Sans Devanagari + Noto Sans (render.py falls back to it when Nirmala UI is missing). Transcription of the plays cost about 385k tokens; stopped after एक दिन (his call).

- 2026-11-20: HRD predicted questions: `papers/human-resource-development-predicted-questions/` (10 ten-mark, two per module; 19 five-mark; 30 two-mark), ranked by topic overlap between Q.P. 50374 and the 12 Nov college exam, then gap topics; answers copied from the HRD theory bank. Print 7 pages, single column 9. On the site (deployed from the cloud session). No blank pages (his standing choice).

- 2026-11-20: Hindi textbook एकांकी कुंज (84 photographed pages) saved as `notes/hindi/ekanki-kunj.pdf` with its contents; माँ is by विष्णु प्रभाकर; the बैंक essay is not in it. Commit email changed to the GitHub no-reply address (GitHub refuses the Gmail). Research: SEP began 2024-25, so Dec 2025 is the only SEP 3rd-semester paper; the Dec 2025 Statistics paper copied two problems word for word from BBA Q.P. 36220 (Jan 2024, NEP); college model exams share only 1–2 questions with the university papers (`research/pyq-repeat-check.md`).

- 2026-11-20: Formula notebook merged into `main`. Kannada dropped (subject not taken). Extra Statistics papers not to be solved. No blank pages on any PDF (including the AS model paper).

- 2026-11-19: Business Statistics formula notebook (6 pages, sent in chat) saved in `notes/business-statistics/formula-notebook/`: exam pointers for theory and problems, then formulas for mean, median, mode, quartiles, range, QD, SD, CV, GM, HM, correlation and regression. Typed copy beside the photos.

- 2026-11-18: Hindi Q.P. 54303 (Dec 2025) solved provisionally, both versions (3 pages each): Section I all 10, Section II passages 1, 3, 4 (passage 2 "मैं अपने प्रस्ताव की स्वीकृति चाहता हूँ" not traced without the textbook), III Q1-Q2 (सूखी डाली, शिवाजी), IV Q1-Q2, V Q1-Q2 (बीमा from the teacher's textbook PDF, कर from her essay), VI both. **Redo from the textbook photos he will send on 19 Nov**, then also fix the Hindi bank (Do Kalakar and Rajrani Sita stories, माँ author, Bank essay). No blank pages asked yet.

- 2026-11-18: Hindi 3rd-semester sources taken from the class WhatsApp group (13 Aug – 6 Nov 2026) into `notes/hindi/` with text copies: the teacher's one-mark Q&A and annotations PDF, notebook photos, summary format, internal test pattern, teacher's essays (कर, नई शिक्षा नीति), and the Dec 2025 university paper Q.P. 54303 (`papers/hindi-sem3-dec-2025/`, on the site as a question paper). The teacher's 10-page essay PDF could not be downloaded (no longer on his phone). Hindi question bank `papers/hindi-theory-bank/` (106 questions, 10 pages, single column; every 2025 question tagged). Open: author of माँ not confirmed; 2025 passage "मैं अपने प्रस्ताव की स्वीकृति चाहता हूँ" not matched to an ekanki; four essays (बीमा, कुटीर, बैंक, विदेशी विनिमय) and all व्याख्याएँ written in exam style, not the teacher's.
- 2026-11-18: Website subject page redesigned: one closed row per paper (question paper and answers joined by title), tap it, then choose Question paper or Answers. Look only; files, links and admin buttons unchanged.

- 2026-11-18: Theory question banks (questions and answers, single column only, his choice) for HRD (`human-resource-development-theory-bank`, 179 questions, 16 pages; Q.P. 50374 and the 12 Nov college exam tagged), Accounting Standards (`accounting-standards-theory-bank`, 183 questions, 24 pages; Q.P. 54323 and the 7 Nov college exam tagged; AS 2 and AS 13 from textbook points, no notes) and Personality Development (`personality-development-theory-bank`, 145 questions, 13 pages; Q.P. 54324, the 13 Nov college exam, Model paper 2 and Daneial D's question bank tagged). No blank pages (he was asleep; none asked).

- 2026-11-18: Corporate Accounting theory question bank (`papers/corporate-accounting-theory-bank/`): 79 theory questions over all 5 modules (2, 5 and 10 marks), every theory question of Q.P. 54321 tagged "(Dec 2025)". Questions and answers both printed, single column only (8 pages), his choice for this file. Module 2 from the teacher's slides; Modules 1, 3, 4, 5 from standard textbook points (no notes). No teacher's important-questions list was found; ask him for it.

- 2026-11-13: Personality Development model exam of 13 November 2026 (Don Bosco, photo sent in chat; same as Model Question Paper 1 in the notes) solved: A 1(a)-(e), B Q2-Q7 (first five / first six). Print 1 page, single column 2. Q7 negotiation uses a fest sound-system example. No blank pages (his choice).

- 2026-11-12: Personality Development question bank (Daneial D, B.Com. 3.5; photos sent in chat) solved in full: Section A 1-22, Section B 1-18, from the short notes. Single column only (4 pages; the two-column copy deleted at his request, 2026-11-12). On the site as "Personality Development Question Bank", with the photos under question papers. No blank pages (his choice).

- 2026-11-12: HRD notes added: full Module 3 notes (`module-3.pdf/.md`) and Modules 4-5 (`module-4-5.pdf/.md`). Both HRD papers now follow the notes' wording where textbook points were used: model exam A8-A10, B5, B6, C3 point 9, C4; Q.P. 50374 1(h), 1(j), Q6, Q7. 50374 still 2 print pages, model exam 3.
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
