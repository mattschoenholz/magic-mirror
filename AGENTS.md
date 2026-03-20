# Multi-agent workflow — Magic Mirror project

Use this file to decide **which role** to invoke in Cursor (paste the relevant `agents/*.md` into context or @-mention files).

---

## Shared context (all agents)

Read **`docs/MIRROR_CONTEXT.md`** first on any deep task — hardware baselines, doc map, HA/voice checklists.

**Cursor skill:** [`mm-mirror-context`](.cursor/skills/mm-mirror-context/SKILL.md) — loads the same intent.

**Domain reference skills** (like ESPHome’s `esphome-lvgl` pattern):

| Skill | Folder |
|-------|--------|
| [`mm-home-assistant`](.cursor/skills/mm-home-assistant/SKILL.md) | HA REST/WebSocket, token hygiene, FR-006 |
| [`mm-kiosk-pi`](.cursor/skills/mm-kiosk-pi/SKILL.md) | Chromium kiosk, systemd, Pi display/audio |
| [`mm-voice-aiy-google`](.cursor/skills/mm-voice-aiy-google/SKILL.md) | **Future** — AIY on Pi if scope returns (**v1 = Echo-only**) |
| [`mm-dev-mcp-ha`](.cursor/skills/mm-dev-mcp-ha/SKILL.md) | HA MCP on **dev machine only** |

**Claude Code:** [`.claude/agents/`](.claude/agents/) → symlinks to `agents/*.md`. [`.claude/skills/`](.claude/skills/) → symlinks to `.cursor/skills/*` (see `.claude/README.md`).

---

## Agent roster

| Agent | Focus | Primary inputs | Primary outputs |
|-------|--------|----------------|-----------------|
| [Planner](agents/planner.md) | Phases 0–5, tasks, risks, Tester handoff | MIRROR_CONTEXT, PROJECT_BRIEF, FSD | Milestones, task breakdown, exit criteria |
| [UX Designer](agents/ux-designer.md) | Glass, 720p layout, night mode, voice UI | MIRROR_CONTEXT, FSD, BRIEF | Tokens, zones, optional SVG |
| [Architect](agents/architect.md) | Stack, HA, voice, audio, resilience | MIRROR_CONTEXT, FSD, ARCHITECTURE | ADRs, decision table |
| [Coder](agents/coder.md) | Implementation post sign-off | MIRROR_CONTEXT, FSD, ARCHITECTURE | Diffs, no secrets, FR traceability |
| [Tester](agents/tester.md) | FSD + phase-aligned verification | MIRROR_CONTEXT, FSD, ARCHITECTURE | Cases, glass/voice passes |

---

## Suggested order

1. **Planner** — phases and tasks.  
2. **UX** + **Architect** in parallel when Phase 2–3 overlap.  
3. **Coder** after FSD/Architecture sign-off for the slice.  
4. **Tester** through Phase 5; **Planner** closes milestones only with Tester exit criteria met or waived.

---

## Cursor skills

Project-local skills: [`.cursor/skills/`](.cursor/skills/). Each role skill starts by reading **`docs/MIRROR_CONTEXT.md`**.

Repo root: `~/Desktop/CurrentProjects/General/magic-mirror`. If nested in a monorepo, copy or symlink `.cursor/skills/` and `docs/MIRROR_CONTEXT.md` paths accordingly.
