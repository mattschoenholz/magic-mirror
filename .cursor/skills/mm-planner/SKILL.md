---
name: mm-planner
description: >-
  Plan phases, milestones, and risks for the wall Magic Mirror project (Pi 4,
  AIY Voice HAT, Home Assistant). Use when sequencing work, controlling scope,
  or updating docs/PROJECT_BRIEF.md and docs/FSD.md priorities.
---

# Magic Mirror — Planner skill

## When to apply

- Starting a new milestone or sprint.
- Scope creep appears; need MoSCoW reprioritization.
- Cross-disciplinary blocker (enclosure vs electronics vs software).

## Instructions

1. Read `magic-mirror/docs/PROJECT_BRIEF.md` and `magic-mirror/docs/FSD.md` (or paths relative to workspace root).
2. Produce milestones with **exit criteria** tied to FR/UC IDs when possible.
3. Maintain a short **risk register** (probability, impact, mitigation).
4. Prefer **frugal** choices: reuse Home Assistant; avoid new paid APIs unless marked Must in FSD.
5. Log recurring mistakes in `magic-mirror/docs/LESSONS_LEARNED.md` when the user confirms.

## Outputs

- Numbered milestone list, decision questions for the owner, and which agent should act next.

## References

- `magic-mirror/agents/planner.md`
- `magic-mirror/AGENTS.md`
