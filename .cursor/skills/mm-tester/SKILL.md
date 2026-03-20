---
name: mm-tester
description: >-
  Verify Magic Mirror against FSD with traceable tests; include mirror-glass
  readability and voice-in-room checks. Use when defining acceptance tests or
  validating a milestone.
---

# Magic Mirror — Tester skill

## When to apply

- Milestone exit, regression pass, or bug verification.
- Defining Given/When/Then cases for new FRs.

## Instructions

1. Read `magic-mirror/docs/FSD.md` acceptance criteria and NFRs.
2. Each case references **FR/UC/NFR** IDs.
3. Include **environment notes**: wall mount, mirror glass, lighting, mic behind glass.
4. Log failures with repro steps; suggest owning agent (UX vs Architect vs Coder).

## Outputs

- Test tables, exploratory notes, regression checklist updates.

## References

- `magic-mirror/agents/tester.md`
