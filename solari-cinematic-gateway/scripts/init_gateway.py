#!/usr/bin/env python3
"""Emit a Solari Cinematic Gateway Package JSON.

Usage:
  init_gateway.py --preset sunwell-birth
  init_gateway.py --preset evermore
  init_gateway.py --brief brief.json
"""
from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

PALETTE = [
    {"hex": "#010101", "token": "void"},
    {"hex": "#F5D623", "token": "solar gold"},
    {"hex": "#A1A19F", "token": "moonsteel"},
    {"hex": "#1A69AE", "token": "lake blue"},
    {"hex": "#E32E30", "token": "signal red"},
    {"hex": "#DADADA", "token": "pale stone"},
    {"hex": "#3E3E3E", "token": "iron"},
    {"hex": "#B13034", "token": "crimson"},
    {"hex": "#A12D6C", "token": "wine"},
]

CULTURE = {
    "race": "Solari",
    "endonym": "Children of the Sun",
    "homeland": "Dawnlands",
    "capital": "Dawnspire",
    "guardians": "Dawnwardens",
    "scholars": "Luminaries",
    "sacredEnergy": "Dawnlight",
    "sacredSource": "the Sunwell",
    "sisterWell": "the Moonwell",
}

LUMINARY_LOCK = (
    "Photoreal cinematic still of a Solari Luminary of the Children of the Sun: "
    "adult woman, long pale-gold hair, pointed ears, warm gold-olive skin, "
    "amber-gold irises with solar dawnlight, never green, never smirking. "
    "Wine-crimson robe over gold plate, void-black field, moonsteel trim. "
    "The Sunwell plaza at Dawnspire under a starfield. Anamorphic 16:9, no text, no watermark."
)


def luminary_master() -> dict:
    return {
        "name": "Lead Luminary of the Sunwell Rite",
        "universe": "Solari",
        "race": "Solari",
        "sex": "female",
        "ageAppearance": "ageless adult",
        "height": "tall elven",
        "bodyType": "lithe ceremonial warrior",
        "silhouette": "crimson robe, gold plate, spear optional, long pale-gold hair",
        "identityLock": {
            "skull": "long elven skull, high cheekbones, pointed ears",
            "proportions": "1:7.5, narrow shoulders under robe",
            "eyes": "amber-gold, solar dawnlight, never fel-green",
            "hair": "long pale-gold, unbraided ceremonial fall",
            "skin": "warm gold-olive",
            "marks": "none; lake-blue gem at throat optional",
            "wardrobeCanon": "wine-crimson robe, gold filigree plate, moonsteel trim",
            "forbidden": [
                "fel-green eyes",
                "Sin'dorei",
                "named Warcraft faces",
                "on-pixel captions",
            ],
        },
        "lockPrompt": LUMINARY_LOCK,
        "palette": "evermore",
    }


def package(preset: str) -> dict:
    now = datetime.now(timezone.utc).isoformat()
    if preset == "sunwell-birth":
        return {
            "id": "sunwell-birth",
            "title": "Birth of the Sunwell",
            "createdAt": now,
            "tensionModel": {
                "coreTension": "The Sunwell is born as a shield against the void — light that costs.",
                "constraints": [
                    "Starlit rite only.",
                    "Light is earned. No smirking.",
                    "One plaza family until the city-awakening ES.",
                ],
                "forbiddenOutcomes": [
                    "Franchise characters or maps",
                    "Sunwell as a generic explosion with no vow",
                ],
                "scale": "mythic",
                "sacredSource": "the Sunwell",
            },
            "culture": CULTURE,
            "palette": {"name": "evermore", "hex": PALETTE},
            "goldenMaster": luminary_master(),
            "ipRewrite": {
                "kept": ["Sunwell", "Moonwell", "Solari"],
                "hits": [],
                "replacements": [],
            },
            "boardId": "sunwell-birth",
            "notes": "Panel 5 expansion. Wide Establishing Shot of the birth is a 24mm orbital ES. Smash back to ES when the well ignites. City-awakening ES is the named transition out.",
        }
    if preset == "evermore":
        return {
            "id": "evermore-commercial",
            "title": "€V€RMØRE",
            "createdAt": now,
            "tensionModel": {
                "coreTension": "The sun does not set; neither does she.",
                "constraints": ["Gold hour only.", "One Dawnwarden.", "One citadel."],
                "forbiddenOutcomes": ["Franchise heraldry", "fel-green eyes"],
                "scale": "civic",
                "sacredSource": "the Sunwell",
            },
            "culture": CULTURE,
            "palette": {"name": "evermore", "hex": PALETTE},
            "goldenMaster": luminary_master(),
            "ipRewrite": {"kept": ["Solari"], "hits": [], "replacements": []},
            "boardId": "evermore-commercial",
            "notes": "Brand film. Walk 0–9, no jumps.",
        }
    raise SystemExit(f"unknown preset: {preset}")


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--preset", choices=["sunwell-birth", "evermore"])
    p.add_argument("--brief", type=Path)
    args = p.parse_args()
    if args.brief:
        brief = json.loads(args.brief.read_text())
        out = package("sunwell-birth")
        out["title"] = brief.get("title", out["title"])
        if brief.get("tension"):
            out["tensionModel"]["coreTension"] = brief["tension"]
    elif args.preset:
        out = package(args.preset)
    else:
        print("Usage: init_gateway.py --preset sunwell-birth|evermore", file=sys.stderr)
        return 1
    json.dump(out, sys.stdout, indent=2)
    print()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
