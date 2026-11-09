#!/usr/bin/env python3
"""Question papers uploaded from the website's camera button ("Just landed").

    python site/inbox.py                     list papers waiting to be solved
    python site/inbox.py fetch <id> [folder] download its photos into papers/<folder>/
    python site/inbox.py done <id>           mark it solved (removes it from "Just landed")

`fetch` saves the photos as papers/<folder>/question-paper-1.jpg, -2.jpg ... The default
folder is <subject>-upload-<date>. `done` adds the id to site/solved-uploads.json; commit and
push it with the solved paper. No key is needed: the photos are public, like the site.
"""
import json
import sys
import urllib.request
from pathlib import Path

API = "https://exam-paper-upload.vercel.app/api"
ROOT = Path(__file__).resolve().parent.parent
SOLVED = ROOT / "site" / "solved-uploads.json"


def get(url):
    req = urllib.request.Request(url, headers={"User-Agent": "exam-paper-inbox"})
    with urllib.request.urlopen(req, timeout=60) as r:
        return r.read()


def waiting():
    return json.loads(get(f"{API}/inbox"))["items"]


def show():
    items = waiting()
    if not items:
        print("Nothing waiting. No new question papers have landed.")
    for u in items:
        print(f"{u['id']}  {u['subject']:<24} {len(u['photos'])} photo(s)  {u['uploaded'][:16]}Z  {u['note']}")


def fetch(pid, folder=None):
    u = next((x for x in waiting() if x["id"] == pid), None)
    if not u:
        sys.exit(f"No waiting upload with id {pid}.")
    folder = folder or f"{u['subject']}-upload-{pid[:8]}"
    dest = ROOT / "papers" / folder
    dest.mkdir(parents=True, exist_ok=True)
    for i, url in enumerate(u["photos"], 1):
        ext = url.rsplit(".", 1)[-1].lower()
        (dest / f"question-paper-{i}.{ext}").write_bytes(get(url))
    (dest / "upload.json").write_text(json.dumps(u, indent=1), encoding="utf-8")
    print(f"{len(u['photos'])} photo(s) saved in papers/{folder}/  (subject: {u['subject']}, note: {u['note'] or '-'})")


def done(pid):
    ids = json.loads(SOLVED.read_text(encoding="utf-8")) if SOLVED.exists() else []
    if pid not in ids:
        ids.append(pid)
    SOLVED.write_text(json.dumps(ids, indent=1) + "\n", encoding="utf-8")
    print(f"{pid} marked solved in site/solved-uploads.json. Commit and push to update the site.")


if __name__ == "__main__":
    args = sys.argv[1:]
    if not args:
        show()
    elif args[0] == "fetch" and len(args) in (2, 3):
        fetch(*args[1:])
    elif args[0] == "done" and len(args) == 2:
        done(args[1])
    else:
        sys.exit(__doc__)
