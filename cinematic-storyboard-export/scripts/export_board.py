#!/usr/bin/env python3
"""Export a Solari Storyboard after ladder QC.

Usage:
  export_board.py <board.json> --format json|csv|html|pdf|contact|unity|all \\
      --out <dir> [--frames-dir DIR] [--force]
"""
from __future__ import annotations

import argparse
import csv
import json
import re
import shutil
import subprocess
import sys
from html import escape
from pathlib import Path

CODES = ["ES", "EWS", "WS", "FS", "MFS", "CS", "MS", "MCU", "CU", "ECU"]
NAMES = [
    "Establishing Shot",
    "Extreme Wide Shot",
    "Wide Shot",
    "Full Shot",
    "Medium Full Shot",
    "Cowboy Shot",
    "Medium Shot",
    "Medium Close-Up",
    "Close-Up",
    "Extreme Close-Up",
]

ROOT = Path(__file__).resolve().parents[2]
VALIDATOR = ROOT / "cinematic-storyboard" / "scripts" / "validate_ladder.py"


def slugify(text: str) -> str:
    s = re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")
    return s or "storyboard"


def load_board(path: Path) -> dict:
    data = json.loads(path.read_text())
    if isinstance(data, list):
        data = {"title": "Untitled", "shots": data}
    if not isinstance(data, dict) or not isinstance(data.get("shots"), list):
        raise SystemExit("error: board must be an object with shots[]")
    data.setdefault("title", "Untitled")
    data.setdefault("logline", "")
    data.setdefault("visualStyle", "")
    data.setdefault("notes", "")
    return data


def rung_of(shot: dict, i: int) -> int:
    if "rung" in shot:
        n = int(shot["rung"])
    elif str(shot.get("code", "")).upper() in CODES:
        n = CODES.index(str(shot["code"]).upper())
    else:
        raise SystemExit(f"error: shot[{i}] missing rung/code")
    if n < 0 or n > 9:
        raise SystemExit(f"error: shot[{i}] rung out of range")
    return n


def steps(shots: list[dict]) -> list[str]:
    out, prev = [], None
    for i, shot in enumerate(shots):
        r = rung_of(shot, i)
        if prev is None:
            out.append("start")
        else:
            d = r - prev
            if d == 0:
                out.append("hold")
            elif abs(d) == 1:
                out.append("down" if d < 0 else "up")
            else:
                out.append("JUMP")
        prev = r
    return out


def qc(board_path: Path, force: bool) -> dict:
    if not VALIDATOR.exists():
        return {"pass": True, "note": "validator missing; skipped"}
    proc = subprocess.run(
        [sys.executable, str(VALIDATOR), str(board_path)],
        capture_output=True,
        text=True,
    )
    ok = proc.returncode == 0
    if not ok and not force:
        sys.stderr.write(proc.stdout + proc.stderr)
        raise SystemExit("error: ladder FAIL — will not export (pass --force to dump anyway)")
    return {"pass": ok, "forced": bool(force and not ok), "log": proc.stdout.strip()}


def resolve_frame(shot: dict, frames_dir: Path | None) -> Path | None:
    url = str(shot.get("imageUrl") or "")
    if not url:
        return None
    name = Path(url).name
    candidates = []
    if frames_dir:
        candidates.append(frames_dir / name)
    if url.startswith("/"):
        candidates.append(Path("/workspace/public") / url.lstrip("/"))
        candidates.append(Path.cwd() / "public" / url.lstrip("/"))
    candidates.append(Path(url))
    for c in candidates:
        if c.is_file():
            return c
    return None


def write_json(board: dict, out: Path) -> Path:
    p = out / "storyboard.json"
    p.write_text(json.dumps(board, indent=2) + "\n")
    return p


def write_csv(board: dict, out: Path) -> Path:
    p = out / "shots.csv"
    labels = steps(board["shots"])
    with p.open("w", newline="") as f:
        w = csv.writer(f)
        w.writerow(
            ["#", "rung", "code", "slug", "action", "camera", "lighting", "sound", "durationSec", "emotion", "step", "ruleBreak"]
        )
        for i, s in enumerate(board["shots"]):
            r = rung_of(s, i)
            w.writerow(
                [
                    i + 1,
                    r,
                    CODES[r],
                    s.get("slug") or "",
                    s.get("action") or "",
                    s.get("camera") or "",
                    s.get("lighting") or "",
                    s.get("sound") or "",
                    s.get("durationSec") or "",
                    s.get("emotion") or "",
                    labels[i],
                    "yes" if s.get("ruleBreak") else "",
                ]
            )
    return p


def panel_html(board: dict, i: int, shot: dict, rel_img: str | None) -> str:
    r = rung_of(shot, i)
    title = escape(str(board.get("title") or "Storyboard"))
    slug = escape(str(shot.get("slug") or f"Shot {i+1}"))
    img = (
        f'<img src="{escape(rel_img)}" alt="{slug}"/>'
        if rel_img
        else f'<div class="ph">{slug}</div>'
    )
    return f"""
<section class="panel">
  <header>
    <p class="kicker">SOLARI CINEMATIC STORYBOARD BREAKDOWN</p>
    <h1>PANEL {i+1} — {slug}</h1>
  </header>
  <div class="plate">{img}</div>
  <div class="meta">
    <div>
      <p><span>SHOT TYPE</span> {CODES[r]} {NAMES[r]}</p>
      <p><span>VISUAL</span> {escape(str(shot.get("action") or "—"))}</p>
      <p><span>INTENT</span> {escape(str(shot.get("emotion") or "—"))}</p>
    </div>
    <div>
      <p><span>CAMERA</span> {escape(str(shot.get("camera") or "—"))}</p>
      <p><span>LIGHTING</span> {escape(str(shot.get("lighting") or "—"))}</p>
      <p><span>DURATION</span> {escape(str(shot.get("durationSec") or "—"))}s</p>
    </div>
  </div>
  <div class="row">
    <p><span>AUDIO</span> {escape(str(shot.get("sound") or "—"))}</p>
    <p><span>BOARD</span> {escape(title)}</p>
  </div>
</section>
"""


def write_html(board: dict, out: Path, frame_rels: list[str | None]) -> Path:
    panels = [
        panel_html(board, i, s, frame_rels[i])
        for i, s in enumerate(board["shots"])
    ]
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8"/>
<title>{escape(str(board.get("title") or "Storyboard"))}</title>
<style>
  :root {{ --ink:#08090d; --gold:#c9a45c; --paper:#f3ead6; --muted:#9a8f78; }}
  * {{ box-sizing: border-box; }}
  body {{ margin:0; background:var(--ink); color:var(--paper);
    font-family: Outfit, Segoe UI, sans-serif; }}
  h1, .kicker {{ font-family: "Cormorant Garamond", Georgia, serif; }}
  .panel {{ page-break-after: always; padding: 24px 28px 32px; }}
  .kicker {{ letter-spacing:.28em; font-size:11px; color:var(--gold); margin:0; }}
  h1 {{ margin:6px 0 16px; font-size:28px; font-weight:600; }}
  .plate {{ aspect-ratio:16/9; background:#0c1018; overflow:hidden; border:1px solid #2c3448; }}
  .plate img {{ width:100%; height:100%; object-fit:cover; display:block; }}
  .ph {{ height:100%; display:flex; align-items:center; justify-content:center; color:var(--muted); }}
  .meta {{ display:grid; grid-template-columns:1fr 1fr; gap:16px; margin-top:16px; font-size:14px; }}
  .row {{ display:grid; grid-template-columns:1fr 1fr; gap:16px; margin-top:12px; font-size:14px; }}
  span {{ display:block; color:var(--gold); font-size:10px; letter-spacing:.16em; }}
  @page {{ size: landscape; margin: 12mm; }}
</style>
</head>
<body>
{''.join(panels)}
</body>
</html>
"""
    p = out / "director.html"
    p.write_text(html)
    return p


def _draw_page(shot: dict, i: int, board: dict, frame: Path | None):
    from PIL import Image, ImageDraw, ImageFont

    W, H = 1920, 1080
    im = Image.new("RGB", (W, H), (8, 9, 13))
    dr = ImageDraw.Draw(im)
    try:
        font_b = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 28)
        font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 18)
        font_s = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 14)
    except OSError:
        font_b = font = font_s = ImageFont.load_default()
    gold = (201, 164, 92)
    paper = (243, 234, 214)
    muted = (154, 143, 120)
    dr.text((48, 28), "SOLARI CINEMATIC STORYBOARD BREAKDOWN", fill=gold, font=font_s)
    slug = str(shot.get("slug") or f"Shot {i+1}")
    dr.text((48, 58), f"PANEL {i+1}  —  {slug.upper()}", fill=paper, font=font_b)
    # plate box
    px, py, pw, ph = 48, 110, 1824, 1026 - 280
    ph = 640
    dr.rectangle([px, py, px + pw, py + ph], outline=(44, 52, 72))
    if frame and frame.is_file():
        art = Image.open(frame).convert("RGB")
        art.thumbnail((pw - 2, ph - 2))
        x = px + (pw - art.size[0]) // 2
        y = py + (ph - art.size[1]) // 2
        im.paste(art, (x, y))
    r = rung_of(shot, i)
    y = py + ph + 24
    col = [
        (48, f"SHOT TYPE  {CODES[r]}  {NAMES[r]}", str(shot.get("action") or "")),
        (1000, "CAMERA", str(shot.get("camera") or "—")),
    ]
    dr.text((48, y), f"SHOT TYPE   {CODES[r]} {NAMES[r]}", fill=gold, font=font_s)
    dr.text((48, y + 22), str(shot.get("action") or "—")[:110], fill=paper, font=font)
    dr.text((1000, y), "CAMERA", fill=gold, font=font_s)
    dr.text((1000, y + 22), str(shot.get("camera") or "—")[:80], fill=paper, font=font)
    dr.text((48, y + 70), "INTENT", fill=gold, font=font_s)
    dr.text((48, y + 92), str(shot.get("emotion") or "—")[:110], fill=paper, font=font)
    dr.text((1000, y + 70), "AUDIO", fill=gold, font=font_s)
    dr.text((1000, y + 92), str(shot.get("sound") or "—")[:80], fill=muted, font=font)
    return im


def write_pdf(board: dict, out: Path, frames: list[Path | None]) -> Path:
    pages = [_draw_page(s, i, board, frames[i]) for i, s in enumerate(board["shots"])]
    p = out / "director.pdf"
    if not pages:
        raise SystemExit("error: no shots to PDF")
    rgb = [im.convert("RGB") for im in pages]
    rgb[0].save(p, save_all=True, append_images=rgb[1:], resolution=150)
    return p


def write_contact(board: dict, out: Path, frames: list[Path | None]) -> Path:
    from PIL import Image, ImageDraw, ImageFont

    shots = board["shots"]
    cols = min(4, max(1, len(shots)))
    rows = max(1, (len(shots) + cols - 1) // cols)
    cell_w, cell_h, pad = 420, 280, 16
    W = cols * cell_w + pad * 2
    H = rows * cell_h + 80
    im = Image.new("RGB", (W, H), (8, 9, 13))
    dr = ImageDraw.Draw(im)
    try:
        font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 14)
        font_b = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 20)
    except OSError:
        font = font_b = ImageFont.load_default()
    dr.text((pad, 20), str(board.get("title") or "Storyboard"), fill=(201, 164, 92), font=font_b)
    for i, shot in enumerate(shots):
        c, row = i % cols, i // cols
        x, y = pad + c * cell_w, 60 + row * cell_h
        box = (x, y, x + cell_w - 12, y + cell_h - 40)
        dr.rectangle(box, outline=(44, 52, 72))
        fp = frames[i]
        if fp and fp.is_file():
            art = Image.open(fp).convert("RGB")
            art.thumbnail((cell_w - 20, cell_h - 56))
            im.paste(art, (x + 4, y + 4))
        code = CODES[rung_of(shot, i)]
        dr.text((x, y + cell_h - 34), f"{i+1}  {code}  {shot.get('slug') or ''}", fill=(243, 234, 214), font=font)
    p = out / "contact-sheet.jpg"
    im.save(p, quality=90)
    return p


def write_unity(board: dict, out: Path) -> Path:
    d = out / "unity"
    d.mkdir(exist_ok=True)
    payload = {
        "title": board.get("title"),
        "logline": board.get("logline"),
        "visualStyle": board.get("visualStyle"),
        "shots": [
            {
                "index": i + 1,
                "rung": rung_of(s, i),
                "code": CODES[rung_of(s, i)],
                "slug": s.get("slug"),
                "durationSec": s.get("durationSec"),
                "action": s.get("action"),
                "camera": s.get("camera"),
                "image": Path(str(s.get("imageUrl") or "")).name or None,
                "ruleBreak": bool(s.get("ruleBreak")),
            }
            for i, s in enumerate(board["shots"])
        ],
    }
    p = d / "StoryboardExport.json"
    p.write_text(json.dumps(payload, indent=2) + "\n")
    return p


def copy_frames(board: dict, out: Path, frames: list[Path | None]) -> list[str | None]:
    dest = out / "frames"
    dest.mkdir(exist_ok=True)
    rels: list[str | None] = []
    for i, (shot, src) in enumerate(zip(board["shots"], frames)):
        r = rung_of(shot, i)
        slug = slugify(str(shot.get("slug") or f"shot-{i+1}"))
        if src and src.is_file():
            name = f"{i+1:02d}-{CODES[r].lower()}-{slug}{src.suffix.lower() or '.jpg'}"
            shutil.copy2(src, dest / name)
            rels.append(f"frames/{name}")
        else:
            rels.append(None)
    return rels


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("board")
    p.add_argument("--format", default="all", choices=["json", "csv", "html", "pdf", "contact", "unity", "all"])
    p.add_argument("--out", required=True)
    p.add_argument("--frames-dir")
    p.add_argument("--force", action="store_true")
    args = p.parse_args()
    board_path = Path(args.board)
    board = load_board(board_path)
    gate = qc(board_path, args.force)
    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    frames_dir = Path(args.frames_dir) if args.frames_dir else Path("/workspace/public/frames")
    frames = [resolve_frame(s, frames_dir) for s in board["shots"]]
    want = {"json", "csv", "html", "pdf", "contact", "unity"} if args.format == "all" else {args.format}
    files: dict[str, str] = {}
    rels = copy_frames(board, out, frames)
    if "json" in want:
        files["json"] = str(write_json(board, out))
    if "csv" in want:
        files["csv"] = str(write_csv(board, out))
    if "html" in want:
        files["html"] = str(write_html(board, out, rels))
    if "pdf" in want:
        files["pdf"] = str(write_pdf(board, out, frames))
    if "contact" in want:
        files["contact"] = str(write_contact(board, out, frames))
    if "unity" in want:
        files["unity"] = str(write_unity(board, out))
    manifest = {
        "title": board.get("title"),
        "shots": len(board["shots"]),
        "qc": gate,
        "files": files,
        "framesCopied": sum(1 for r in rels if r),
    }
    (out / "MANIFEST.json").write_text(json.dumps(manifest, indent=2) + "\n")
    print(json.dumps(manifest, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
