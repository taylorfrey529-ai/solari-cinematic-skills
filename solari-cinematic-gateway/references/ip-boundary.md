---
description: "IP boundary: keep Sunwell/Moonwell; rewrite franchise characters and maps. Read before any prompt."
connections: [evermore-palette, pipeline, command-language]
---

# IP boundary

User canon: **Sunwell** and **Moonwell** are this world's wells. Keep those words.

Do **not** clone franchise **characters, maps, or faction names**.

## Keep

| Token | Status |
| --- | --- |
| Sunwell | Sacred source. Keep. |
| Moonwell | Sister well. Keep. |
| Solari | Original race. Keep. |
| Children of the Sun, Dawnlands, Dawnspire, Dawnwarden, Luminary, Dawnlight | Original. Keep. |

## Rewrite / drop

| Source token | Do this |
| --- | --- |
| Sin'dorei, blood elf (as Warcraft race) | Solari |
| Silvermoon, Quel'Thalas | Dawnspire, Dawnlands |
| Kael'thas, Sylvanas, Anasterian, Lor'themar, Liadrin | Original names only — never these |
| Warcraft, Blizzard, WoW, StarCraft, Terran, Zerg, Protoss | Drop |
| Fel-green eyes | Solar-gold dawnlight |
| Marvel / DC named faces | Original faces |

`scripts/ip_scan.py` prints `kept` (Sunwell/Moonwell) and `hits` (blocked). A hit must be replaced before `lockPrompt` is written.

Structural grammar (ladder, gold hour, orbital ES) may stay. Faces and heraldry must be original.
