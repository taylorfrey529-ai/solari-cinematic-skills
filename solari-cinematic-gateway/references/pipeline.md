---
description: "Expand a storyboard panel into a legal walk, then optional engine export. Read for Workflow C."
connections: [command-language, golden-master, ip-boundary]
---

# Pipeline — panel to package

## Expand a panel

1. Strip overlay copy into notes (SHOT TYPE, CAMERA, AUDIO, NARRATION, TRANSITION). Those words do **not** go into pixels.
2. Map SHOT TYPE onto a rung (`Wide Establishing Shot` → 0 ES). A stated camera move (slow clockwise orbit) is **in-shot**, not extra cards.
3. IP-scan the copy. Keep Sunwell/Moonwell.
4. Lead-in: walk the ladder **toward** the panel (usually down from a darker ES).
5. The panel itself: if you smash back to ES for the manifestation, set `ruleBreak` + reason.
6. Release: one-step out, **or** a flagged geographic ES when the panel names a city-awakening transition.
7. Durations: boarded shots 2–8s. If the panel's timecode is longer (e.g. 02:05–02:40), note it as a live-action one-er on that card.

## Birth of the Sunwell (Panel 5 grammar)

| Beat | Rung | Job |
| --- | --- | --- |
| Wait | 0→1→2→3 | Dark plaza, circle, rim, Luminary |
| Birth | 0 JUMP | Orbital ES, Sunwell ignites |
| Witness | 1→2 | Silhouettes, lit circle |
| Release | 0 JUMP | Dawnspire catches the bloom |

Both jumps are sourced: manifestation smash + named transition out.

## Engine export

Golden Master + palette + shot list JSON is the Unity-facing package (geometry / appearance / stability). Do not emit C# unless asked. Identity lock is the CIP.
