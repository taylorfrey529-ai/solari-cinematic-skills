---
description: "Export format map. Read to pick json, csv, html, pdf, contact, or unity."
connections: [qc, director-html]
---

# Formats

| Flag | File | Job |
| --- | --- | --- |
| `json` | `storyboard.json` | Canonical Storyboard object |
| `csv` | `shots.csv` | Spreadsheet shot list (`#`, rung, code, slug, action, camera, duration, step) |
| `html` | `director.html` | Printable Panel 5 pages. See [[director-html]] |
| `pdf` | `director.pdf` | Same chrome, one page per shot (PIL) |
| `contact` | `contact-sheet.jpg` | Grid of plates + captions in the sheet chrome |
| `unity` | `unity/StoryboardExport.json` | Shots + ladder + optional identity lock |
| `all` | folder + `MANIFEST.json` | Everything |

`--frames-dir` copies local stills into `frames/NN-code-slug.ext`. Never draw text onto those copies.

Default `--out` is `./<slug>-export`.
