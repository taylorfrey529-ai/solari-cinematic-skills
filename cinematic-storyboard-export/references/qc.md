---
description: "Ladder QC gate before export. Read when a board might be illegal."
connections: [formats, director-html]
---

# QC before export

Call cinematic-storyboard `validate_ladder.py` on the JSON.

| Result | Export |
| --- | --- |
| PASS | Proceed |
| FAIL | Stop. Offer legalize (`legalize_ladder.py`) or flagged `ruleBreak` + reason |
| `--force` | Allowed only if the user asked to dump anyway. MANIFEST.forced = true |

A jump with `ruleBreak` + non-empty `ruleBreakReason` is **legal** (flagged). A jump without both is **illegal**.

Do not "fix" rungs silently at export time. That belongs to boarding.
