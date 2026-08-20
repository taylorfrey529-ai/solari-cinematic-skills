#!/usr/bin/env python3
"""Scan text for Solari IP boundary tokens.

Keeps Sunwell / Moonwell. Flags franchise casts and maps.

Usage:
  ip_scan.py <file>
  ip_scan.py -          # stdin
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

KEEP = [
    (r"\bsunwell\b", "Sunwell"),
    (r"\bmoonwell\b", "Moonwell"),
    (r"\bsolari\b", "Solari"),
    (r"\bdawnspire\b", "Dawnspire"),
    (r"\bdawnlands\b", "Dawnlands"),
    (r"\bdawnwarden", "Dawnwarden"),
]

BLOCK = [
    (r"\bsin['’]?dorei\b", "Solari"),
    (r"\bblood elves?\b", "Solari"),
    (r"\bsilvermoon\b", "Dawnspire"),
    (r"\bquel['’]?thalas\b", "Dawnlands"),
    (r"\bkael['’]?thas\b", "(original name)"),
    (r"\bsylvanas\b", "(original name)"),
    (r"\banasterian\b", "(original name)"),
    (r"\blor['’]?themar\b", "(original name)"),
    (r"\bwarcraft\b", "(drop)"),
    (r"\bblizzard\b", "(drop)"),
    (r"\bstarcraft\b", "(drop)"),
    (r"\bzerg\b", "(drop)"),
    (r"\bterran\b", "(drop)"),
    (r"\bfel[- ]?green\b", "solar-gold dawnlight"),
]


def scan(text: str) -> dict:
    kept, hits = [], []
    for pat, label in KEEP:
        for m in re.finditer(pat, text, re.I):
            kept.append({"token": m.group(0), "keep": label, "span": [m.start(), m.end()]})
    for pat, repl in BLOCK:
        for m in re.finditer(pat, text, re.I):
            hits.append(
                {
                    "token": m.group(0),
                    "replace": repl,
                    "span": [m.start(), m.end()],
                }
            )
    return {
        "kept": kept,
        "hits": hits,
        "ok": len(hits) == 0,
        "summary": f"{len(kept)} kept, {len(hits)} blocked",
    }


def main() -> int:
    if len(sys.argv) != 2:
        print("Usage: ip_scan.py <file>|-", file=sys.stderr)
        return 1
    raw = sys.stdin.read() if sys.argv[1] == "-" else Path(sys.argv[1]).read_text()
    result = scan(raw)
    json.dump(result, sys.stdout, indent=2)
    print()
    return 0 if result["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
