# Multi-agent workflow — Magic Mirror project

Use this file to decide **which role** to invoke in Cursor (paste the relevant `agents/*.md` into context or @-mention files).

---

## Agent roster

| Agent | Focus | Primary inputs | Primary outputs |
|-------|--------|----------------|-----------------|
| [Planner](agents/planner.md) | Phases, risks, dependencies, “what next” | PROJECT_BRIEF, FSD backlog | Milestones, decision log prompts |
| [UX Designer](agents/ux-designer.md) | Readability on glass, calm UI, voice feedback | Viewing distance, room lighting notes | Wireframes, type scale, motion rules |
| [Architect](agents/architect.md) | Stack choices, HA boundaries, security | FSD NFRs, HA capabilities | ARCHITECTURE.md updates, ADRs |
| [Coder](agents/coder.md) | Implementation *when you start coding* | FSD, ARCHITECTURE | PR-sized changes, configs (no secrets) |
| [Tester](agents/tester.md) | Traceability, acceptance, regression | FSD acceptance criteria | Test checklists, bug reports |

---

## Suggested order (planning phase)

1. **Planner** — freeze v1 scope and milestones.  
2. **UX Designer** — layout + contrast rules for mirror glass.  
3. **Architect** — lock UI + voice path; update diagrams.  
4. **Coder** — *after* FSD sign-off for v1 features.  
5. **Tester** — parallel with Coder for each FR.

---

## Cursor skills

Project-local skills live under [`.cursor/skills/`](.cursor/skills/). They mirror these roles so the model loads concise instructions automatically when this folder is the **workspace root**.

This repo’s root is `~/Desktop/CurrentProjects/General/magic-mirror`. If you ever nest it inside a monorepo, copy or symlink `.cursor/skills/` or reference `agents/*.md` manually.
