---
name: mm-planner
description: >-
  Plan phases, milestones, tasks, and risks for the wall Magic Mirror (Pi 4,
  AIY Voice HAT, Home Assistant). Coordinates UX, Architect, Coder, Tester with
  quality gates. Use when sequencing work or reviewing progress.
---

# Magic Mirror — Planner skill

## When to apply

- New milestone or sprint; scope creep; cross-disciplinary blockers.
- Progress review: blockers, next tasks, phase exit vs Tester.

## Instructions

1. Read **`docs/MIRROR_CONTEXT.md`**, then **`docs/PROJECT_BRIEF.md`** and **`docs/FSD.md`**.
2. Use **phases 0–5** and **task template** from `agents/planner.md`.
3. Every milestone lists **exit criteria** testable by **Tester** (FR/NFR IDs).
4. Maintain a short **risk register** (probability, impact, mitigation).
5. Prefer frugal choices; log recurring mistakes in **`docs/LESSONS_LEARNED.md`** when the user confirms.

## Outputs

- Numbered tasks by phase, dependencies, **handoff** agent, **Tester** preview.
- One focused clarifying question when blocked — not a long questionnaire.

## References

- `agents/planner.md`
- `AGENTS.md`
- `docs/MIRROR_CONTEXT.md`
