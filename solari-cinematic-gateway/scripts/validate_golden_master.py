#!/usr/bin/env python3
"""Validate a Golden Master JSON for required identity fields.

Usage:
  validate_golden_master.py <master.json>
  validate_golden_master.py -
Exit 0 if complete; 1 if any required field is empty.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

TOP = [
    "name",
    "universe",
    "race",
    "sex",
    "ageAppearance",
    "height",
    "bodyType",
    "silhouette",
    "lockPrompt",
    "palette",
]
LOCK = ["skull", "proportions", "eyes", "hair", "skin", "wardrobeCanon"]


def missing(master: dict) -> list[str]:
    gaps = []
    for k in TOP:
        if not str(master.get(k) or "").strip():
            gaps.append(k)
    lock = master.get("identityLock") or {}
    if not isinstance(lock, dict):
        gaps.append("identityLock")
        return gaps
    for k in LOCK:
        if not str(lock.get(k) or "").strip():
            gaps.append(f"identityLock.{k}")
    forbidden = lock.get("forbidden")
    if not isinstance(forbidden, list) or len(forbidden) == 0:
        gaps.append("identityLock.forbidden")
    return gaps


def main() -> int:
    if len(sys.argv) != 2:
        print("Usage: validate_golden_master.py <master.json>|-", file=sys.stderr)
        return 1
    raw = sys.stdin.read() if sys.argv[1] == "-" else Path(sys.argv[1]).read_text()
    try:
        data = json.loads(raw)
    except json.JSONDecodeError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1
    if not isinstance(data, dict):
        print("error: JSON must be an object", file=sys.stderr)
        return 1
    # Allow a wrapper { goldenMaster: {...} }
    master = data.get("goldenMaster") if isinstance(data.get("goldenMaster"), dict) else data
    gaps = missing(master)
    if gaps:
        print("FAIL missing:")
        for g in gaps:
            print(f"  - {g}")
        return 1
    print(f"PASS Golden Master '{master.get('name')}' lock complete.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
