# Agent Skills Suite Integration

**Integration ID:** SOLARI-AGENT-SUITE-001  
**Contract version:** 1.0.0  
**Status:** SPECIFIED — cross-repository contract documented; no runtime adapter is claimed.

## Purpose

Solari Cinematic Skills remains the authoritative domain workflow for Solari canon, Golden Master identity, IP boundaries, shot-ladder grammar, storyboard QC, and cinematic exports.

The companion Agent Skills Suite provides broader orchestration and specialist reasoning: NFD narrative-field design, CCL workflow coordination, ACD-AI direction, MACS specialist collaboration, LATTUS deterministic-state discipline, and Neural Audio Ecosystem design.

Companion repository: https://github.com/taylorfrey529-ai/agent-skills-suite  
Integration contract in companion repository: INTEGRATION/SOLARI_INTEGRATION.md

## Responsibility map

| Solari component | Agent Skills Suite partner | Handoff |
|---|---|---|
| solari-cinematic-gateway | CCL + NFD | CCL coordinates; NFD supplies narrative field; Solari Gateway specializes tension/canon initialization. |
| command-language.md | NFD | Solari tension fields are a constrained project profile of the broader narrative charter. |
| golden-master.md | ACD-AI | Immutable identity lock is a director constraint and must be copied verbatim. |
| ip-boundary.md + ip_scan.py | Shared Operating Contract + World of StarCraft Orchestration | Solari IP scan remains the project-specific gate; original Solari canon is preserved. |
| cinematic-storyboard | ACD-AI + MACS | Director and specialists provide approved direction; Solari owns shot-rung grammar and board validation. |
| cinematic-storyboard-export | CCL + production governance | Export follows Solari QC; suite governance tracks evidence and release status. |
| Solari sound cues | Neural Audio Ecosystem | Audio plan annotates approved shots and narrative state; it cannot change story/simulation authority. |
| Board state references | LATTUS | Optional authoritative event/tick references support replayable continuity. |

## Required integrated sequence

1. CCL intake and scope.
2. NFD narrative field charter.
3. Solari Gateway tension model and canon profile.
4. Reconcile constraints; stop on unresolved contradictions.
5. Run Solari IP scan.
6. Create and validate Golden Master.
7. ACD-AI direction; optional MACS specialist proposals.
8. Create storyboard with Solari shot ladder.
9. Run Solari ladder validator.
10. Add audio/technical annotations without changing approved narrative or simulation facts.
11. Export with Solari exporter only after QC.
12. Record evidence and status honestly.

## Non-negotiable Solari gates

- Keep Sunwell and Moonwell as established Solari canon.
- Preserve Golden Master lockPrompt verbatim in every later image prompt.
- Use Solari's ten-rung shot ladder; adjacent shots move no more than one rung unless a deliberate jump has a specific ruleBreakReason.
- Run the supplied validator; do not claim QC passed without running it.
- Do not export an illegal board as a normal validated deliverable.
- Never place labels, shot codes, or timecodes into generated image pixels.
- Do not imply a private companion repository is publicly accessible.

## Handoff format

The shared logical envelope is documented in the companion repository at INTEGRATION/SOLARI_INTEGRATION.md. It carries project/source identity and version; NFD charter reference and Solari tension fields; IP scan status and hits; Golden Master ID/version and verbatim lock prompt; director decision, approved variants, and invariants; storyboard ID/version, shots, and QC status; authoritative simulation snapshot/tick reference; audio plan and export manifest references; and validation statuses.

This is a documented contract example, not an implemented API or schema validator.

## Conflict and failure policy

- Solari canon, Golden Master, and ladder rules remain authoritative within Solari production.
- NFD/Solari constraint conflicts block progression until reconciled.
- ACD-AI and MACS cannot bypass Solari validation.
- Missing/stale simulation state must remain unknown; never fabricate it.
- Failed IP, identity, ladder, or export checks block the corresponding downstream stage.
- Human approval is required for canon/identity changes and high-impact exceptions.

## Compatibility scenarios

- Valid sequence: NFD → Gateway → Golden Master → legal board → QC → export.
- Invalid ladder jump: reject or explicitly legalize; never silently pass.
- Identity paraphrase: reject and restore verbatim Golden Master lock.
- IP collision: rewrite blocked terms before prompt creation.
- Stale event tick: request current authoritative state.
- Audio contradiction: reject the cue if it violates approved narrative constraints.

## Implementation status

The two repositories now have a documented integration contract. A live runtime adapter, machine-validated shared schema, automated cross-repository CI, and end-to-end execution remain NOT IMPLEMENTED until built and tested.
