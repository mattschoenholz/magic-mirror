---
name: mm-tester
description: >-
  Verify Magic Mirror against FSD with traceable tests; mirror glass, in-room
  voice, Planner phase exit criteria. Use for acceptance and regression.
---

# Magic Mirror — Tester skill

## When to apply

- Milestone exit, regression, bug verification.
- Defining Given/When/Then for new FRs.

## Instructions

1. Read **`docs/MIRROR_CONTEXT.md`**, then **`docs/FSD.md`** and **`docs/ARCHITECTURE.md`**.
2. Use **`mm-home-assistant/reference.md`** for HA disconnect/API test ideas.
3. Each case references **FR/UC/NFR**; use **phase bundles** from `agents/tester.md` where helpful.
4. Environment: wall mount, **mirror glass**, lighting, mic, **HAT vs TV audio**.
5. Failures: repro, owner hint (UX / Architect / Coder).

## Outputs

- Test tables; exploratory notes; regression checklist updates.

## References

- `agents/tester.md`
- `docs/MIRROR_CONTEXT.md`
