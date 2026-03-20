---
name: mm-architect
description: >-
  System design for Magic Mirror on Raspberry Pi with Home Assistant and voice
  (AIY HAT). Use when choosing stack, drawing boundaries, or updating
  docs/ARCHITECTURE.md and security patterns.
---

# Magic Mirror — Architect skill

## When to apply

- Choosing kiosk OS, UI framework, or voice pipeline.
- Defining HA integration (WebSocket, REST, whitelisted services).
- Security review: tokens, SSH, network exposure.

## Instructions

1. Read `docs/FSD.md` (FR/NFR) and `docs/ARCHITECTURE.md`.
2. Prefer **HA as source of truth** for device state; mirror displays entities and sends limited service calls.
3. Document **secrets handling** — patterns only; never commit real tokens.
4. Treat Cursor **MCP** as development tooling unless FSD says otherwise.
5. Update the decision table in `ARCHITECTURE.md` when options are chosen.

## Outputs

- Architecture deltas, ADR notes, interface lists (entity IDs / service names) as *templates* without live secrets.

## References

- `agents/architect.md`
