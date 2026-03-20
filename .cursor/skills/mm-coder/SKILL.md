---
name: mm-coder
description: >-
  Implement Magic Mirror per FSD/Architecture: small diffs, FR/NFR tags, no
  secrets, HA/voice error handling. Use after spec sign-off.
---

# Magic Mirror — Coder skill

## When to apply

- Implementation: features, configs, systemd, kiosk wiring.
- Bug fixes with linked FR/UC/NFR IDs.

## Instructions

1. Read **`docs/MIRROR_CONTEXT.md`**, then **`docs/FSD.md`** and **`docs/ARCHITECTURE.md`**.
2. Follow **non-negotiables** in `agents/coder.md` (no tokens in repo/bundles, reconnect behavior).
3. Map work to **FR/NFR**; bump **FSD** version table when behavior changes.
4. Add **`.env.example`** only; document install in **README**.

## Outputs

- Code + minimal docs + **suggested Tester cases** per FR.

## References

- `agents/coder.md`
- `docs/MIRROR_CONTEXT.md`
