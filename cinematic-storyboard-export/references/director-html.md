---
description: "Director HTML/PDF chrome modeled on Panel 5. Read when printing or PDFing."
connections: [formats, qc]
---

# Director page (Panel 5 grammar)

One shot per printed page. Landscape 16:9-ish. Dark ink, gold rules.

```
HEADER     SOLARI CINEMATIC STORYBOARD BREAKDOWN
           PANEL N — SLUG
PLATE      16:9 still. No captions on the pixels.
META       SHOT TYPE | VISUAL | INTENT | CAMERA | MOTION | DOF
AUDIO      MUSIC / SFX
NARRATION  optional VO
TRANSITION optional
```

SHOT TYPE is `{code} {rung name}` (e.g. `ES  Establishing Shot`). CAMERA comes from the shot. VISUAL is `action`. INTENT is `emotion`.

The plate is the art. The chrome is the board. Do not flatten labels into `imagePrompt` or into exported stills.

Print CSS: `@page { size: landscape; margin: 12mm; }`
