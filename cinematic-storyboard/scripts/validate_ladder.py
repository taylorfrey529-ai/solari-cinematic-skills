#!/usr/bin/env python3
"""Validate a Storyboard JSON against the Solari one-step rule.

Usage:
  validate_ladder.py <board.json>
  validate_ladder.py -            # stdin
  cat board.json | validate_ladder.py -

Exit 0 if every adjacent pair is legal (delta <= 1, or ruleBreak with reason).
Exit 1 on illegal jumps or unreadable input.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

CODES = ["ES", "EWS", "WS", "FS", "MFS", "CS", "MS", "MCU", "CU", "ECU"]


def load(path: str) -> dict:
    raw = sys.stdin.read() if path == "-" else Path(path).read_text()
    data = json.loads(raw)
    if isinstance(data, list):
        return {"shots": data}
    if not isinstance(data, dict):
        raise ValueError("JSON must be an object or array of shots")
    return data


def rung_of(shot: dict, i: int) -> int:
    if "rung" in shot:
        n = int(shot["rung"])
    elif "code" in shot and str(shot["code"]).upper() in CODES:
        n = CODES.index(str(shot["code"]).upper())
    else:
        raise ValueError(f"shot[{i}] missing rung/code")
    if n < 0 or n > 9:
        raise ValueError(f"shot[{i}] rung {n} out of 0–9")
    return n


def step_label(prev: int | None, cur: int, rule_break: bool) -> tuple[str, bool]:
    if prev is None:
        return "start", True
    delta = cur - prev
    abs_d = abs(delta)
    if abs_d == 0:
        return "hold", True
    if abs_d == 1:
        return ("↓" if delta < 0 else "↑"), True
    reason = "JUMP (flagged)" if rule_break else "JUMP (illegal)"
    return reason, bool(rule_break)


def main() -> int:
    if len(sys.argv) != 2:
        print("Usage: validate_ladder.py <board.json>|-", file=sys.stderr)
        return 1
    try:
        board = load(sys.argv[1])
    except Exception as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1

    shots = board.get("shots")
    if not isinstance(shots, list) or not shots:
        print("error: no shots[]", file=sys.stderr)
        return 1

    print(f"{'#':<4}{'rung':<6}{'code':<6}{'step':<18}slug")
    illegal = 0
    prev = None
    for i, shot in enumerate(shots):
        if not isinstance(shot, dict):
            print(f"error: shot[{i}] is not an object", file=sys.stderr)
            return 1
        try:
            r = rung_of(shot, i)
        except ValueError as exc:
            print(f"error: {exc}", file=sys.stderr)
            return 1
        code = CODES[r]
        reason = str(shot.get("ruleBreakReason") or "").strip()
        flagged = bool(shot.get("ruleBreak")) and bool(reason)
        label, legal = step_label(prev, r, flagged)
        if not legal:
            illegal += 1
        slug = str(shot.get("slug") or "")
        mark = "" if legal else "  <-- ILLEGAL"
        print(f"{i + 1:<4}{r:<6}{code:<6}{label:<18}{slug}{mark}")
        prev = r

    if illegal:
        print(f"\nFAIL {illegal} illegal jump(s). Walk one rung, or set ruleBreak + reason.")
        return 1
    print(f"\nPASS {len(shots)} shots, one-step legal.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
