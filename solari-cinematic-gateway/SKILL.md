---
name: solari-cinematic-gateway
description: "Orchestrate the Solari Cinematic Gateway: tension model, Golden Master identity lock, Evermore palette, IP boundary, then a legal shot-ladder board. Use when the user mentions Solari Cinematic Gateway, CCL, Golden Master, Sunwell, Moonwell, Dawnwarden, Evermore palette, cinematic pipeline, resume cinematic development, or expanding a storyboard panel. NOT for generic one-off shot lists (use cinematic-storyboard), sprites, or UI mockups."
type: orchestrator
lifecycle: active
user-invocable: true
when-to-use: Solari Cinematic Gateway, Golden Master, Sunwell, Moonwell, Evermore, resume cinematic development
---

# Solari Cinematic Gateway — Tension to a legal cinematic

Do not start on a pretty frame. Start on **meaning constraints**, lock **identity**, apply the **IP boundary**, then board.

This skill **orchestrates**. Shot grammar lives in [[cinematic-storyboard:]]. Frame craft lives in [[imagine:]].

## When to load what

- `references/INDEX.md` — graph map
- `references/command-language.md` — CCL tension model (Step 1)
- `references/golden-master.md` — identity lock formula
- `references/evermore-palette.md` — hex tokens + Solari names
- `references/ip-boundary.md` — keep Sunwell/Moonwell; block franchise casts
- `references/pipeline.md` — panel expansion + engine export

Run, do not rewrite:

- `scripts/ip_scan.py <file|->` — flag blocked franchise tokens; keep Sunwell/Moonwell
- `scripts/validate_golden_master.py <master.json>` — required identity fields
- `scripts/init_gateway.py [--preset sunwell-birth|evermore] [--brief file.json]` — emit Gateway Package JSON

Then hand the package to **cinematic-storyboard** for the ladder. Run that skill's `validate_ladder.py` before shipping shots.

## Output contract

Return **one Gateway Package**, then a **Storyboard** (via cinematic-storyboard).

```
GatewayPackage
  id, title
  tensionModel: { coreTension, constraints[], forbiddenOutcomes[] }
  culture: { race, endonym, homeland, capital, guardians, sacredSource }
  palette: { name, hex[] }
  goldenMaster: GoldenMaster
  ipRewrite: { hits[], kept[], replacements[] }
  board: Storyboard | null
  notes
```

Print a director table for the board. Do not dump a mood collage.

## Workflow

### Decide the path

1. **Storyboard panel / still attached** → Workflow C (expand)
2. **Resume / Gateway / CCL / Golden Master / Evermore / Sunwell** → Workflow A (init)
3. **Only a shot list, no identity/tension** → stop and use [[cinematic-storyboard:]] instead

### A. Initialize the Gateway

1. Run `ip_scan.py` on any source text or panel copy.
2. Open `references/command-language.md`. Write the **tension model** before characters or shots.
3. Open `references/evermore-palette.md`. Lock palette + Solari names. Sacred source is **the Sunwell** (Moonwell allowed as sister well).
4. Open `references/golden-master.md`. Fill a Golden Master. Run `validate_golden_master.py`.
5. `init_gateway.py` emits the package. Keep `goldenMaster.lockPrompt` **verbatim** in every later imagePrompt.
6. Hand off to cinematic-storyboard Workflow A. Ladder is grammar; this package is look + meaning.

### B. Identity only

If the user asks for a Golden Master / CIP / Unity identity stack: do steps A.3–A.5. Do not board unless they also asked for shots.

### C. Expand a reference panel

1. Read the panel as **one shot**, not a bible. Strip on-pixel captions from any generated frames.
2. IP-scan overlay copy. **Keep Sunwell / Moonwell.** Rewrite Sin'dorei, Silvermoon, named Warcraft/StarCraft/Marvel casts. See [[ip-boundary]].
3. Place the panel on the ladder (Wide Establishing → rung 0 ES). A slow orbit is a **move inside the shot**, not a jump.
4. Build **lead-in** (walk toward the panel) and **release** (walk one step out, or a flagged geographic ES).
5. A smash back to ES is legal only with `ruleBreak` + reason (e.g. manifestation: the Sunwell ignites).
6. Generate the clean plate first (no text). Subsequent rungs: image-to-image from that plate.
7. QC with cinematic-storyboard `validate_ladder.py`.

### D. Frames

- 16:9 unless asked otherwise. No captions, timecodes, `SHOT TYPE`, or storyboard chrome in pixels.
- After two successful frames, lock from the plate via reference / i2i.

## What not to do

- Don't clone Warcraft / StarCraft / Marvel **characters, maps, or faction names**.
- Don't rename the Sunwell or Moonwell unless the user asks. They are this world's wells.
- Don't board before a tension model and a Golden Master exist.
- Don't skip cinematic-storyboard and emit rungs by vibe.
- Don't treat a ChatGPT screenshot PDF as a Gateway bible.
- Don't put panel labels into generated pixels.

## App pairing

Solari Board: `src/lib/cinematic/`. Seeded boards include Last Light, €V€RMØRE, and Birth of the Sunwell. Keep `ladder.ts` as rung math.

## Grok Ask

User-invocable. Trigger with `/solari-cinematic-gateway`. Keep **Sunwell** and **Moonwell**. Tension model and Golden Master before shots. Then [[cinematic-storyboard:]] then [[cinematic-storyboard-export:]].

## Knowledge Graph

Start at `references/INDEX.md`.

### Cross-Skill Connections

- [[cinematic-storyboard:]] — shot ladder, PDF import, ladder QC
- [[cinematic-storyboard-export:]] — director HTML/PDF, CSV, Unity after QC
- [[imagine:]] — plates after the board is legal
- [[xai-api:]] — in-app Grok + Imagine
- [[design-ui:]] — studio chrome, not the shots
