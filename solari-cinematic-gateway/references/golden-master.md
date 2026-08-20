---
description: "Golden Master identity lock. Read when creating or validating a character CIP."
connections: [evermore-palette, command-language, pipeline]
---

# Golden Master — Identity, not appearance

A Golden Master is the immutable visual source for a character. Every later frame, portrait, or costume variation inherits it.

**Identity remains fixed.** Only clothing, pose, lighting, environment, camera, and expression may vary.

## Required schema

```
name, universe, race, sex, ageAppearance, height, bodyType, silhouette
identityLock:
  skull, proportions, eyes, hair, skin, marks, wardrobeCanon, forbidden[]
lockPrompt   // 1–2 sentences, repeated VERBATIM in every imagePrompt
palette      // evermore
```

Run `scripts/validate_golden_master.py <file.json>`. Exit 1 if any required field is empty.

## Solari Luminary (Sunwell rite)

- Race: Solari (Children of the Sun). Not Sin'dorei.
- Eyes: amber-gold with **solar** dawnlight. Never fel-green.
- Wardrobe: wine-crimson robe, gold plate, void-black field, moonsteel trim.
- Palette: [[evermore-palette]].
- `lockPrompt` must mention pointed ears, pale-gold hair, and the Sunwell plaza if the scene is the birth rite.

Do not write "make her look like the last frame." That is a prayer. Write the lock.
