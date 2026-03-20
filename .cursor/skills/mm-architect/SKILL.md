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
2. Load **`mm-home-assistant`**, **`mm-kiosk-pi`**; **`mm-dev-mcp-ha`** for Cursor MCP on a dev PC only. **`mm-voice-aiy-google`** only if **AIY** is back in scope (**v1 = Echo-only voice**).
3. Apply the **decision framework** and **edge cases** from `agents/architect.md`.
4. HA as source of truth; whitelisted mirror → HA actions; **no secrets** in git or frontend bundles.
5. Update **ARCHITECTURE.md** decision table when options are chosen.

## Outputs

- Architecture deltas, ADR notes, **template** entity/service lists (no live secrets).

## References

- `agents/architect.md`
- `docs/MIRROR_CONTEXT.md`
