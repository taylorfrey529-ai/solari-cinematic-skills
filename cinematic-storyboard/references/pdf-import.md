---
description: "Extract and parse cinematic design from PDFs: text bibles, lookbooks, and empty ChatGPT screenshot exports. Read when a PDF is attached."
connections: [shot-ladder, prompt-craft]
---

# Import cinematic design from PDF

Use this when the user attaches or names a PDF: shot bible, lookbook,
screenplay, director notes, or a ChatGPT/conversation export.

The [[shot-ladder]] remains grammar after parse. Every extracted visual token
must land in [[prompt-craft]] identity locks so frames match the bible.

## Extract

Prefer the bundled script (deterministic, flags empty exports):

```bash
node .grok/skills/cinematic-storyboard/scripts/extract_pdf_design.mjs path/to.pdf
```

It prints JSON: `empty`, `screenshotLikely`, `chatExportLikely`,
`cinematicLikely`, `tokens.shotCalls`, `warnings`. Treat as a bible only when
`cinematicLikely` is true (or the user pastes a scene).

In the Solari Board app, the same extract lives in `src/lib/cinematic/pdf.ts`
via `unpdf`:

```ts
import { extractText, getDocumentProxy } from "unpdf";

const pdf = await getDocumentProxy(bytes);
const { text, totalPages } = await extractText(pdf, { mergePages: true });
const blob = Array.isArray(text) ? text.join("\n\n") : text;
```

Then:

1. Count characters after whitespace-collapse.
2. If `< 400` chars for a multi-page PDF, treat as **image-only / empty**.
   Common failure: "Print to PDF" of a ChatGPT thread — pages are blank
   screenshots. Tell the user; do not hallucinate a bible.
3. If text exists, keep a 1–2k excerpt in `source.excerpt` so the board
   stays auditable.

Optional: `extractImages` when the PDF is a lookbook of frames. Use those
as Imagine **references**, not as the storyboard itself (they may already
break the ladder).

## Screenshot / empty / chat dumps

If `screenshotLikely`, `empty`, or `chatExportLikely` with `cinematicLikely=false`:

- Say the PDF is not a usable cinematic bible.
- Do **not** invent StarCraft / Warcraft / franchise lore from the filename.
- Sample at most 3–5 pages as images (first, a middle page, last) if a
  raster tool exists. Never dump 100 blank pages into context.
- Ask for a paste of the scene, or proceed from the user's prompt + the
  ladder only.

A 110-page ChatGPT export titled like "World of Starcraft FOR SALE" is this
case until proven otherwise. Thousands of characters of hotfix notes, auth QA,
or chat timestamps still do **not** make a bible — board only if
`cinematicLikely` is true.

## Parse into design tokens

Pull, in this order, whatever the document actually contains:

| Token | Look for |
|-------|----------|
| World / setting | locations, time of day, architecture |
| Cast | names, silhouettes, costume, age |
| Palette | stated colors, film stock, LUT language |
| Camera grammar | existing shot sizes, lenses, "one-er" notes |
| Story beats | numbered scenes, action lines, VFX briefs |
| Constraints | "never show X", brand/IP limits, rating |

Map any existing shot-size language onto rungs:

`establishing → 0`, `extreme wide / aerial → 1`, `wide / long → 2`,
`full / long shot of figure → 3`, `cowboy / American → 5`,
`medium → 6`, `medium close / bust → 7`, `close-up → 8`,
`insert / extreme close / ECU → 9`. "Medium full / 3/4" → 4.

If the PDF's own sequence jumps rungs, **reboard** it onto a legal walk
(`scripts/legalize_ladder.py`) and list the original calls in `notes` so
the user can see what changed. Only preserve a jump when the PDF itself
marks it as a smash / match cut.

## Empty or IP-heavy PDFs

- Empty ChatGPT export: ask for a paste of the scene, or proceed from the
  user's prompt + the Solari ladder only.
- Copyrighted franchise mashups (named Warcraft / StarCraft / Marvel /
  etc. characters, maps, factions): keep the **structural** design
  (ladder, lighting, pacing) and rebuild **original** names, faces, and
  heraldry. Say that you did this.

## After parse

Run the standard storyboard workflow in `SKILL.md` section A, with the
PDF as `source.type = "pdf"`. Every `imagePrompt` must include the visual
tokens you extracted (wardrobe, palette, location) so frames match the
bible, not a generic epic-fantasy default.
