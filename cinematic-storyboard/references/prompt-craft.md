---
description: "Per-rung Imagine prompt language, identity lock, and continuity rules. Read when writing imagePrompt or generating frames."
connections: [shot-ladder, pdf-import]
---

# Frame prompt craft (per rung)

One shot = one prompt = one image. Present-tense, photographic, no shot
labels in the pixels.

Framing language below maps 1:1 onto the [[shot-ladder]] rungs. If the
board came from a PDF, bake [[pdf-import]] tokens (wardrobe, palette,
location) into the identity lock — do not fall back to generic epic-fantasy.

## Shared lock (repeat in every prompt of a board)

Write a 1–2 sentence **identity block** once, then reuse it verbatim:

- Subject: species/age, hair, armor or wardrobe, distinctive mark
- Place: architecture, era, climate
- Light: time of day + color temperature
- Stock: "photoreal cinematic still, anamorphic 16:9, no text, no watermark"

Do not rename the hero between rungs. Do not change the weather unless
the scene does.

## Size language to put in the prompt

The model does not know "rung 5". Speak in **framing**:

| Rung | Prompt size language |
|------|----------------------|
| 0 ES | ultra-wide establishing landscape; figure tiny or absent; environment is the subject |
| 1 EWS | extreme wide; subject small in frame; architecture dwarfs them |
| 2 WS | wide shot; subject and full surroundings both readable |
| 3 FS | full shot, head to toe, complete silhouette, feet in frame |
| 4 MFS | knees-to-head, medium-full, three-quarter figure |
| 5 CS | cowboy shot, mid-thigh to head, hands visible |
| 6 MS | medium shot, waist to head |
| 7 MCU | medium close-up, chest to head, shallow depth of field |
| 8 CU | close-up, face fills the frame, eyes sharp |
| 9 ECU | extreme close-up of one detail (an eye, a hand, an object) |

Add **one** camera note: lock-off, slow push, low angle, over-shoulder.
Never two moves.

## Continuity

1. Generate rung 0 (or the widest shot) first.
2. Subsequent rungs: image-to-image / reference from that frame when a
   tool allows it, with a prompt that **only** changes framing.
3. If a face drifts, stop and re-lock from the last good CU before
   continuing down to ECU.

Pair with [[imagine:]] for the actual generate/edit calls.

## Forbidden in pixels

Text, subtitles, black storyboard borders, "SHOT 04", arrows, letterboxed
bars unless the user asked for 2.39 and you are actually generating that
ratio, extra limbs, a second wardrobe.

## Example (rung 6)

> Photoreal cinematic still, medium shot waist-to-head of a golden-armored
> elven sentinel, long blonde hair, pointed ears, amber eyes, ornate gold
> filigree breastplate. Quiet grief. Dawn light in a gilded cathedral hall,
> shallow depth, anamorphic 16:9, no text, no watermark.
