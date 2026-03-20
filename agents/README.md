# Agent role definitions

Each file is a **role prompt** with **YAML frontmatter** (`name`, `description`, `skills`) for **Claude Code** compatibility. Body is shared with [`.claude/agents/`](../.claude/agents/) via symlinks.

| File | Role |
|------|------|
| [planner.md](planner.md) | Phases 0–5, tasks, risks, quality gates |
| [ux-designer.md](ux-designer.md) | Mirror glass, night mode, optional 1280×720 SVG |
| [architect.md](architect.md) | HA, voice, audio, decision framework |
| [coder.md](coder.md) | Implementation discipline, no secrets |
| [tester.md](tester.md) | FSD traceability, phase-aligned bundles |

**Shared context:** [docs/MIRROR_CONTEXT.md](../docs/MIRROR_CONTEXT.md)

**Cursor skills:** [`.cursor/skills/`](../.cursor/skills/) — includes `mm-mirror-context` plus per-role skills.
