---
name: cinematic-storyboard-export
description: "Create a Solari cinematic storyboard and export it to JSON, CSV, director HTML, PDF, contact sheet, or Unity package after ladder QC. Use when the user wants a storyboard plus export, or to download, print, dump, or package an existing shot list. NOT for sprites, UI mockups, Golden Master-only work, or a diner scene with no export."
type: workflow
lifecycle: active
user-invocable: true
when-to-use: export storyboard, download shot list, director PDF, contact sheet, Unity package
---

# Cinematic Storyboard Export — Board it, then ship a package

A board that cannot leave the chat is a mood. Export is the deliverable.

**QC the ladder before any file.** Grammar lives in [[cinematic-storyboard:]]. This skill packages a **legal** board.

## When to load what

- `references/INDEX.md` — graph map
- `references/qc.md` — refuse illegal jumps unless `--force`
- `references/formats.md` — json / csv / html / pdf / contact / unity
- `references/director-html.md` — Panel 5 page chrome (labels off the plate)

Run, do not rewrite:

```
python3 .grok/skills/cinematic-storyboard-export/scripts/export_board.py \
  <board.json> --format all --out <dir> [--frames-dir public/frames]
```

Formats: `json` `csv` `html` `pdf` `contact` `unity` `all`.

Sibling QC: `.grok/skills/cinematic-storyboard/scripts/validate_ladder.py`

## Output contract

Write a folder, then tell the user the paths.

```
<slug>-export/
  storyboard.json
  shots.csv
  director.html
  director.pdf
  contact-sheet.jpg
  unity/StoryboardExport.json
  frames/01-es-slug.jpg   # copies only, never relabel pixels
  MANIFEST.json
```

Print the director table (from cinematic-storyboard) **and** the manifest. Do not paste megabytes of HTML.

## Workflow

### Decide the path

1. **No board yet / brief / PDF / panel** → board with [[cinematic-storyboard:]] (or [[solari-cinematic-gateway:]] if they asked Gateway/Sunwell). Then export.
2. **Existing JSON / studio board** → Workflow B
3. **Export only, format named** → Workflow B with that `--format`

### B. Export

1. Materialize Storyboard JSON (studio store, attachment, or the board just made).
2. Run `validate_ladder.py`. **If FAIL:** do not export. Legalize or demand `ruleBreak` + reason. `--force` only when the user explicitly wants an illegal dump.
3. Resolve frames from `imageUrl` / `--frames-dir`. Missing frames are OK; chrome still exports.
4. `export_board.py --format … --out …`
5. Confirm MANIFEST.json lists every file. For HTML/PDF, chrome may show SHOT TYPE — **plates stay caption-free**.

### App pairing

Solari Board Export control: JSON, CSV, director HTML (print). Keep `src/lib/cinematic/export.ts` in sync with `formats.md`.

## What not to do

- Don't export an illegal ladder as if it passed.
- Don't stamp `CU` / timecode onto generated stills.
- Don't clone franchise casts in exported copy (Sunwell/Moonwell stay).
- Don't skip cinematic-storyboard and invent rungs at export time.

## Grok Ask

User-invocable. Trigger with `/cinematic-storyboard-export`. In Ask without a sandbox, emit JSON + CSV in the reply and a director HTML code block. Do not skip ladder QC.

## Knowledge Graph

Start at `references/INDEX.md`.

### Cross-Skill Connections

- [[cinematic-storyboard:]] — boarding, PDF import, ladder QC
- [[solari-cinematic-gateway:]] — tension + Golden Master before a mythic board
- [[imagine:]] — plates, then this skill packages them
- [[design-ui:]] — studio Export control
