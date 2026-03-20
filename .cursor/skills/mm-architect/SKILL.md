---
name: mm-architect
description: >-
  System design for Magic Mirror on Raspberry Pi with Home Assistant and Google
  voice (AIY HAT). Decision framework, edge cases, security. Use when updating
  docs/ARCHITECTURE.md or FSD NFRs.
---

# Magic Mirror — Architect skill

## When to apply

- Kiosk OS, UI framework, voice pipeline, audio routing (HAT vs HDMI).
- HA integration, resilience, security review.

## Instructions

1. Read **`docs/MIRROR_CONTEXT.md`**, then **`docs/FSD.md`** and **`docs/ARCHITECTURE.md`**.
2. Apply the **decision framework** and **edge cases** from `agents/architect.md`.
3. HA as source of truth; whitelisted mirror → HA actions; **no secrets** in git or frontend bundles.
4. Treat **MCP** as dev-only unless FSD says otherwise.
5. Update **ARCHITECTURE.md** decision table when options are chosen.

## Outputs

- Architecture deltas, ADR notes, **template** entity/service lists (no live secrets).

## References

- `agents/architect.md`
- `docs/MIRROR_CONTEXT.md`
