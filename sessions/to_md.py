#!/usr/bin/env python3
"""Turn a Claude Code session export (transcript.jsonl from the app's Export zip)
into a readable Markdown log: your messages, Claude's replies, and one line per tool step.

    python sessions/to_md.py transcript.jsonl sessions/2026-11-02-setup-transcript.md "Exam Paper setup"

Left out on purpose: tool output, images, Claude's hidden reasoning, and system text
(memory, settings), so nothing private from other projects ends up in this repo.
"""
import json
import re
import sys


def text_of(content):
    if isinstance(content, str):
        return content
    return "\n".join(b.get("text", "") for b in content if b.get("type") == "text")


SECRET = re.compile(r"(vc[pkia]_[A-Za-z0-9]{20,}|gh[opsu]_[A-Za-z0-9]{20,}|github_pat_[A-Za-z0-9_]{20,}"
                    r"|sk-[A-Za-z0-9_-]{20,}|eyJ[A-Za-z0-9_-]{20,}\.[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+)")


# Private strings typed in chat (e.g. the admin password), one per line, in sessions/.redact.
# That file is gitignored and stays on this PC.
_REDACT_FILE = __import__("pathlib").Path(__file__).with_name(".redact")
REDACT = [x for x in _REDACT_FILE.read_text(encoding="utf-8").splitlines() if x.strip()] if _REDACT_FILE.exists() else []


def hide_private(s):
    for x in REDACT:
        s = s.replace(x, "[private]")
    return SECRET.sub("[token removed]", s)


def clean(s):
    s = hide_private(s)  # the repo is public: never publish a pasted key or password
    s = re.sub(r"<system-reminder>.*?</system-reminder>", "", s, flags=re.S)
    s = re.sub(r"\[Image: source: [^\]]*\]", "[image]", s)
    return s.strip()


def step(block):
    inp = block.get("input", {})
    what = inp.get("description") or inp.get("file_path") or inp.get("title") or inp.get("query") or ""
    return hide_private(f"- `{block['name'].split('__')[-1]}` {what}".rstrip())


def main(src, dst, title):
    out = [f"# {title}", ""]
    for line in open(src, encoding="utf-8"):
        rec = json.loads(line)
        msg = rec.get("message") or {}
        if rec.get("type") not in ("user", "assistant") or rec.get("isMeta"):
            continue
        content = msg.get("content")
        if rec["type"] == "user":
            if isinstance(content, list) and any(b.get("type") == "tool_result" for b in content):
                continue
            text = clean(text_of(content))
            if text:
                out += ["", "## You", "", text, ""]
        else:
            for b in content if isinstance(content, list) else []:
                if b.get("type") == "text" and clean(b["text"]):
                    out += ["", "**Claude:** " + clean(b["text"]), ""]
                elif b.get("type") == "tool_use":
                    out.append(step(b))
    with open(dst, "w", encoding="utf-8") as f:
        f.write(re.sub(r"\n{3,}", "\n\n", "\n".join(out)) + "\n")


if __name__ == "__main__":
    main(*sys.argv[1:4])
