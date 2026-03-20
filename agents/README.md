# Agent role definitions

Each file is a **role prompt** with **YAML frontmatter** (`name`, `description`, `skills`) for **Claude Code** compatibility. Bodies are shared with [`.claude/agents/`](../.claude/agents/) via symlinks.

| File | Role |
|------|------|
| [planner.md](planner.md) | Phases 0–5, tasks, risks, quality gates |
| [ux-designer.md](ux-designer.md) | Mirror glass, night mode, optional 1280×720 SVG |
| [architect.md](architect.md) | HA, voice, kiosk, MCP-dev; loads multiple domain skills |
| [coder.md](coder.md) | Implementation; HA/kiosk/voice skills |
| [tester.md](tester.md) | FSD traceability; HA skill for API tests |

**Shared context:** [docs/MIRROR_CONTEXT.md](../docs/MIRROR_CONTEXT.md)

**Reference skills** (`.cursor/skills/`): `mm-mirror-context`, `mm-home-assistant`, `mm-kiosk-pi`, `mm-voice-aiy-google`, `mm-dev-mcp-ha`

**Stack:** Custom web UI + local HA backend (not MagicMirror²) — see [docs/ARCHITECTURE.md](../docs/ARCHITECTURE.md).
