---
name: cinematic-storyboard
description: "Create cinematic storyboards and shot lists using the Solari Cinematic Shot Ladder, and import cinematic design from PDFs (shot bibles, screenplays, lookbooks, ChatGPT exports). Use when the user mentions storyboard, shot list, shot ladder, animatic, previz, coverage, cinematic sequence, or wants to turn a script, scene, or PDF into boarded shots. NOT for single-image generation, game sprites, or UI mockups."
type: workflow
lifecycle: active
user-invocable: true
when-to-use: storyboard, shot ladder, animatic, previz, coverage, cinematic sequence
---

# Cinematic Storyboard — Solari Shot Ladder

Camera is language. The ladder is grammar. Break it only when you mean it.

Produce a **boarded sequence** — ordered shots a director or image model can shoot — not a mood collage. Every shot has a rung, a purpose, and a legal step from the shot before it.

## When to load what

Do not dump every reference into context. Read on demand:

- `references/INDEX.md` — graph map
- `references/shot-ladder.md` — ten rungs, valid steps, when a jump is allowed
- `references/pdf-import.md` — extract + parse cinematic design from PDFs
- `references/prompt-craft.md` — per-rung Imagine prompts and continuity

Run, do not rewrite:

- `scripts/extract_pdf_design.mjs <file.pdf>` — text extract + empty/screenshot flag
- `scripts/validate_ladder.py <board.json>` — one-step QC (exit 1 on illegal jumps)
- `scripts/legalize_ladder.py <board.json>` — insert bridge rungs so a jump becomes a walk

## Output contract

Return **one Storyboard**. Print a **board table** first (director-facing), then JSON.

```
Storyboard
  id, title, logline, visualStyle
  source: { type: pdf|script|brief, name?, excerpt? }
  shots: Shot[]
  notes?

Shot
  index                  // 1-based
  rung                   // 0–9
  code                   // ES | EWS | WS | FS | MFS | CS | MS | MCU | CU | ECU
  slug                   // 2–5 words, title case
  action                 // present tense, in-frame
  camera                 // one move max
  lighting, sound, emotion
  durationSec            // 2–8 typical
  imagePrompt            // self-contained (see prompt-craft)
  ruleBreak              // true only for a deliberate jump
  ruleBreakReason        // required if ruleBreak
```

| # | Rung | Code | Slug | Action | Camera | Step |
|---|------|------|------|--------|--------|------|
| 1 | 0 | ES | The Citadel at Dawn | … | Lock-off, 24mm feel | start |

`Step` is `start` | `↓` | `↑` | `hold` | `JUMP (reason)`.

## Workflow

### Decide the path

1. **PDF attached / named** → Workflow B
2. **Brief, scene, or script** → Workflow A
3. **Existing board / JSON** → QC with `validate_ladder.py`; legalize only if the user wants jumps repaired

### A. From a brief, scene, or script

1. Identify location, subject, emotional arc (arrive → intimacy, or reverse).
2. Open `references/shot-ladder.md`. Start on **rung 0 (ES)** unless the scene is already inside an intimate space — then start on the widest *true* shot of that space.
3. Walk **one rung per cut** toward the peak, then climb out if the scene releases. Holds (same rung, new beat) are legal.
4. One subject, one location family, one lighting condition unless a cut is a geographic jump (then a new ES).
5. Write `imagePrompt` for every shot from `references/prompt-craft.md`.
6. Generate frames only after the board is approved **or** when the user asked for images in the same breath. Generate the ES first; reuse it as reference.
7. Run ladder QC (below) before presenting.

### B. Import cinematic design from PDF

Follow `references/pdf-import.md`. Short version:

1. Run `scripts/extract_pdf_design.mjs <pdf>`.
2. If `empty`, `screenshotLikely`, or `chatExportLikely` with `cinematicLikely=false`: say so. Do **not** invent a franchise bible from a ChatGPT export (including one whose only usable text is a title plus unrelated notes). Ask for a paste, or sample a few pages as images — never rasterize 100 blank pages.
3. If `cinematicLikely`: pull setting, cast, palette, existing shot calls. Treat the PDF as **canon for look and story**, the ladder as **canon for grammar**.
4. If the PDF's own sequence jumps rungs, **reboard** onto a legal walk (`legalize_ladder.py`) and list original calls in `notes`. Preserve a jump only when the source marks a smash / match cut.
5. Copyrighted mashups (named StarCraft / Warcraft / Marvel characters, maps, factions): keep structural grammar; rebuild original names, faces, heraldry. Say that you did this.
6. Continue with Workflow A using `source.type = "pdf"`.

### C. Frames (when generating art)

- Aspect **16:9** unless the user specified 2.39 / 9:16.
- No captions, letters, UI, or storyboard-scribble borders in the pixels.
- Same character recipe and location recipe in every prompt.
- After two rungs, lock identity from the first successful frame via image-to-image / reference.

## Ladder QC (mandatory)

For each adjacent pair `(shot[i], shot[i+1])`:

- `|rung[i+1] - rung[i]| <= 1` → pass
- `== 0` → hold (OK)
- `> 1` → illegal unless `ruleBreak` + a **specific** reason

Never skip rungs to save frames. A 3-shot trailer still obeys the step (e.g. `0 → 1 → 2` or `6 → 7 → 8`), never `0 → 7 → 9`.

Valid: `4 ↔ 5`, `6 ↔ 5`, `2 ↔ 1`. Invalid: `4 ↔ 6`, `7 ↔ 4`, `0 ↔ 3`.

Run `scripts/validate_ladder.py` on the JSON before shipping.

## What not to do

- Don't clone copyrighted characters, armor, faction names, or maps.
- Don't emit a shot list without rungs and codes.
- Don't start on a close-up because it's cooler.
- Don't put shot numbers or `CU` labels into generated pixels.
- Don't generate 20 frames when 8 boarded shots will tell the beat.
- Don't hallucinate design from an empty PDF.

## App pairing

This workspace ships **Solari Board** (`src/lib/cinematic/`). Keep `src/lib/cinematic/ladder.ts` as the single source of rung math; mirror rule changes here.

## Grok Ask

User-invocable. In Ask, trigger with `/cinematic-storyboard` or by intent. If `scripts/` cannot run, apply the one-step rule by hand and print the director table. Export packages live in [[cinematic-storyboard-export:]].

## Knowledge Graph

Start at `references/INDEX.md`.

### Cross-Skill Connections

- [[cinematic-storyboard-export:]] — JSON, CSV, director HTML/PDF, contact sheet, Unity package
- [[imagine:]] — frame generation after the board is legal
- [[xai-api:]] — in-app Grok + Imagine calls
- [[design-ui:]] — Solari Board chrome, not the shots themselves
