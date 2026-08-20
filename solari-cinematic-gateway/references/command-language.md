---
description: "Cinematic Command Language Step 1: tension model before characters or shots. Read before boarding."
connections: [golden-master, pipeline, ip-boundary]
---

# Cinematic Command Language — Tension model

CCL does not start with a script. Step 1 is **Story Foundation Layer Initialization — Tension Model Specification**.

Define the physics of meaning the cinematic is allowed to operate under. Constraints generate story. Plot is a side effect.

## Required fields

| Field | Job |
| --- | --- |
| `coreTension` | One sentence. Two forces that cannot both win. |
| `constraints[]` | Laws of this world the camera must obey (light, death, vow). |
| `forbiddenOutcomes[]` | Endings the system may not emit (cheap victory, smirk, fel-green). |
| `scale` | Personal / civic / mythic. Caps how wide the ES may feel. |
| `sacredSource` | For Solari: **the Sunwell**. Moonwell is the sister well. |

## Solari default

```
coreTension: The Sunwell is born as a shield against the void — light that costs.
constraints:
  - Gold hour / starlit rite only; no daylight cutaways unless geography jumps.
  - Light is earned. No smirking. No fel-green eyes.
  - One location family per scene unless a flagged geographic ES.
forbiddenOutcomes:
  - Franchise characters or maps
  - Sunwell used as a generic explosion with no vow
scale: mythic
sacredSource: the Sunwell
```

Write this **before** a Golden Master or a shot list. Then lock identity in [[golden-master]] and board via [[cinematic-storyboard:]].
