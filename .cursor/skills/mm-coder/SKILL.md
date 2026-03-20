---
name: mm-coder
description: >-
  Implement Magic Mirror software per FSD/Architecture. Use only after specs
  are set; produce small diffs, no secrets in git, and update docs when
  behavior changes.
---

# Magic Mirror — Coder skill

## When to apply

- Implementation phase: features, configs, systemd, kiosk wiring.
- Bug fixes with linked FR/UC IDs.

## Instructions

1. Map work to `docs/FSD.md` requirement IDs; bump FSD version if behavior changes.
2. Add `.env.example` (no real secrets); document install in `README.md`.
3. Match stack conventions once chosen (document in README).
4. Never embed HA tokens in client-visible bundles.

## Outputs

- Code changes + minimal doc updates + suggested test cases for Tester.

## References

- `agents/coder.md`
