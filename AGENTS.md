# Rules for other AI agents (Cursor, Codex, ...)

Read PROJECT_CONTEXT.md and TASKS.md first, then CLAUDE.md and README.md, and follow
every rule in them. Update TASKS.md before you finish. CLAUDE.md was written
for Claude, but the rules are the same for every agent: answers from the user's notes
first, 10 pt answers, question numbers only, only the first N of choice questions, no
sources mentioned.

Where a cloud agent works differently:

- **Setup:** `pip install -r requirements.txt`. There is no Arial on Linux;
  `render.py` falls back to Helvetica (same letter widths). That is fine.
- **Git:** work on your own branch and open a PR. Never merge into `main`; the user
  merges. Skip the session-export step.
- **Hand-over in chat:** you can't attach files, so end your final reply with a link to
  the PDF and to every page image on your branch, one per line:

  ```
  PDF: https://github.com/abuzar310/exam-paper/blob/<branch>/papers/<folder>/output/<folder>.pdf
  Page 1: https://github.com/abuzar310/exam-paper/blob/<branch>/papers/<folder>/output/<folder>-page-1.png
  Page 2: https://github.com/abuzar310/exam-paper/blob/<branch>/papers/<folder>/output/<folder>-page-2.png
  ```

  Fill in the real branch and folder names, and list every page the PDF has.
