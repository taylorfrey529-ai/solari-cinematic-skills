---
description: "The ten Solari rungs, valid one-step moves, and when a jump is allowed. Read before boarding any sequence."
connections: [pdf-import, prompt-craft]
---

# Solari Cinematic Shot Ladder

Move from shot to shot like steps on a ladder. Only one up or only one down.
Start with an establishing shot.

Source diagram: `assets/shot-ladder.jpg` (and `/shot-ladder.jpg` in the app).

After the walk is legal, write frames with [[prompt-craft]]. If the source was a PDF whose own calls jump rungs, remap using [[pdf-import]] instead of preserving the jump.

## The rungs

| Rung | Code | Name | Framing | Job |
|------|------|------|---------|-----|
| 0 | ES | Establishing Shot | Entire environment; subject tiny or absent | Place and scale. Geography. Time of day. |
| 1 | EWS | Extreme Wide Shot | Very wide; subject small in frame | Subject enters the world. Still about the space. |
| 2 | WS | Wide Shot | Subject plus generous surroundings | Blocking and traffic. Where they stand in the room. |
| 3 | FS | Full Shot | Head to toe | Body language. Costume silhouette. Walks and falls. |
| 4 | MFS | Medium Full Shot | Knees to head | Gesture with more face. The "character poster." |
| 5 | CS | Cowboy Shot | Mid-thigh to head | Hands + holster line + face. Readiness, weapons, stance. |
| 6 | MS | Medium Shot | Waist to head | Balance of expression and gesture. Conversation default. |
| 7 | MCU | Medium Close-Up | Chest / shoulders to head | Emphasis on expression. Decision, reaction. |
| 8 | CU | Close-Up | Head fills the frame | Emotion. The line that matters. |
| 9 | ECU | Extreme Close-Up | Eyes, mouth, hands, object | Maximum intimacy or a story-critical detail. |

## The rule

You may move **only one step** up or **only one step** down per cut.

```
VALID (one step)          NOT VALID (multi-step)
4 ↔ 5                     4 ↔ 6
6 ↔ 5                     7 ↔ 4
2 ↔ 1                     0 ↔ 3
```

Same-rung recuts (new angle, new beat, reverse) are legal and do not count
as a jump.

### Example sequences

Down (closer, building intimacy):

`0 → 1 → 2 → 3 → 4 → 5 → 6 → 7 → 8 → 9`

Up (wider, releasing / revealing geography):

`9 → 8 → 7 → 6 → 5 → 4 → 3 → 2 → 1 → 0`

A scene does not have to walk every rung. A 6-shot scene might be
`0 → 1 → 2 → 3 → 4 → 5` or `4 → 5 → 6 → 7 → 8 → 7`. What it must not do is
`0 → 4 → 8`.

QC the JSON with `scripts/validate_ladder.py`. Repair a source jump with
`scripts/legalize_ladder.py` (inserts bridge rungs; still write action).

## Why it matters

- Spatial continuity — the audience always knows where they are.
- Visual rhythm — professional coverage has a pulse, not a jump-cut collage.
- Emotional intimacy is **earned** one step at a time.
- A broken step becomes a **deliberate** creative choice (shock, comedy,
  rupture). If you break it, say why on the card.

## When a jump is justified (flag `ruleBreak`)

- Smash cut: violence, explosion, a door kicked in.
- Dream / memory puncture.
- Match cut on action or shape across time.
- Montage with a declared graphic engine (not "random cool shots").

If you cannot write the reason in one clause, it is not justified. Walk the
ladder instead.

## Coverage recipe (dialogue scene)

1. ES or WS of the room.
2. FS or MFS of both bodies.
3. CS / MS of the speaker.
4. MCU of the listener (hold or one step).
5. CU on the line that changes the scene.
6. Climb back to MS or WS for the button.

Singles still obey the step from whatever you just cut off of.

## Camera moves vs. cuts

A **move** (dolly in, crane down) can travel more than one rung *inside a
shot* — that is a continuous change of size, not a jump cut. On the board,
mark it as one shot with `camera: "slow dolly-in from WS toward MCU"` and
do not list fake in-between cards unless you need them for previz.

Cuts still obey the one-step rule relative to the **end size** of the
previous shot.
