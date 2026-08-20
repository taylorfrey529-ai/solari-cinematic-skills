#!/usr/bin/env python3
"""Insert bridge rungs so a Storyboard JSON obeys the one-step rule.

Does not invent story — copied fields stay on original shots; bridges are
marked slug 'Bridge — CODE' so a human (or the LLM) can write action later.

Usage:
  legalize_ladder.py <board.json> [--out out.json]
  legalize_ladder.py -            # stdin → stdout
"""

from __future__ import annotations

import argparse
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


def rung_of(shot: dict) -> int:
    if "rung" in shot:
        n = int(shot["rung"])
    elif "code" in shot and str(shot["code"]).upper() in CODES:
        n = CODES.index(str(shot["code"]).upper())
    else:
        raise ValueError("shot missing rung/code")
    return max(0, min(9, n))


def bridge(rung: int, src: dict, dst: dict) -> dict:
    code = CODES[rung]
    return {
        "rung": rung,
        "code": code,
        "slug": f"Bridge — {code}",
        "action": (
            f"Bridge shot ({code}) between "
            f"{src.get('slug') or CODES[rung_of(src)]} and "
            f"{dst.get('slug') or CODES[rung_of(dst)]}."
        ),
        "camera": "Lock-off, one size step.",
        "lighting": str(src.get("lighting") or dst.get("lighting") or ""),
        "sound": str(src.get("sound") or ""),
        "durationSec": 2,
        "emotion": str(src.get("emotion") or ""),
        "imagePrompt": "",
        "ruleBreak": False,
        "bridge": True,
    }


def legalize(shots: list) -> tuple[list, int]:
    if not shots:
        return [], 0
    out = [dict(shots[0])]
    out[0]["rung"] = rung_of(out[0])
    out[0]["code"] = CODES[out[0]["rung"]]
    inserted = 0
    for nxt in shots[1:]:
        nxt = dict(nxt)
        target = rung_of(nxt)
        nxt["rung"] = target
        nxt["code"] = CODES[target]
        cur = out[-1]["rung"]
        if abs(target - cur) <= 1:
            out.append(nxt)
            continue
        step = 1 if target > cur else -1
        walk = cur + step
        while walk != target:
            out.append(bridge(walk, out[-1], nxt))
            inserted += 1
            walk += step
        out.append(nxt)
    return out, inserted


def main() -> int:
    parser = argparse.ArgumentParser(description="Insert one-step bridge rungs")
    parser.add_argument("board")
    parser.add_argument("--out")
    args = parser.parse_args()
    try:
        board = load(args.board)
    except Exception as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1
    shots = board.get("shots")
    if not isinstance(shots, list):
        print("error: no shots[]", file=sys.stderr)
        return 1
    new_shots, inserted = legalize(shots)
    board["shots"] = new_shots
    notes = str(board.get("notes") or "")
    if inserted:
        extra = f"Legalized: inserted {inserted} bridge rung(s) to keep the one-step rule."
        board["notes"] = f"{notes}\n{extra}".strip()
    text = json.dumps(board, indent=2)
    if args.out:
        Path(args.out).write_text(text + "\n")
    else:
        sys.stdout.write(text + "\n")
    print(f"# inserted {inserted} bridge shot(s); now {len(new_shots)} shots", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
