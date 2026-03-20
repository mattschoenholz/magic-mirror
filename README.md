# Wall Magic Mirror (Pi 4 + Home Assistant + Echo)

A **planning and documentation** home for a wall-mounted smart mirror: two-way glass over an HDMI display, driven by a **Raspberry Pi 4** (**display + local HA backend**), with **voice through an Echo Dot** → **Home Assistant** for v1. **AIY Voice HAT** is **optional / later** — not part of the initial install.

> **Status:** Ideation / specification — application code comes later.  
> **GitHub:** [github.com/mattschoenholz/magic-mirror](https://github.com/mattschoenholz/magic-mirror)

---

## Local project path

Open this folder as the Cursor **workspace root** so `.cursor/skills/` load correctly:

`~/Desktop/CurrentProjects/General/magic-mirror`

**Layout:** `agents/` and `.cursor/skills/` live **here**; [`.claude/agents/`](.claude/agents/) symlinks to `agents/` for **Claude Code** (same files include YAML frontmatter).

---

## Purpose (draft)

- **Primary:** Glanceable “dashboard on the wall” — **weather** (**today** + compact **multi-day**), **school calendar**, **visual todo**, time, home state, **Pomodoro countdown** — in a **child’s bedroom**, readable at **~10 ft** and **~2–3 ft** ([UI_MODES.md](docs/UI_MODES.md)).
- **Voice (v1):** **Echo Dot** (“Echo”) → **HA** for music, Pomodoro, routines, and Alexa; the Pi **does not** run mirror-mounted voice in the first phase.
- **Secondary:** HA automations and Echo for lights, scenes, climate, etc.
- **Night mode:** Softer UI and restrained audio for overnight use.
- **Non-goals (v1):** Full conversational assistant, heavy video, or replacing the phone for complex HA admin.

Hardware notes (glass size, TV, Pi, audio): [docs/PROJECT_BRIEF.md](docs/PROJECT_BRIEF.md).

**Implementation stack (v1):** **Custom web UI** in **Chromium kiosk** + **local backend** on the Pi for **Home Assistant REST/WebSocket** (**FR-006**). **Not** MagicMirror². Skills: `mm-home-assistant`, `mm-kiosk-pi`, `mm-dev-mcp-ha`. **`mm-voice-aiy-google`** only if AIY returns to scope later.

---

## Quick links

| Document | Role |
|----------|------|
| [MIRROR_CONTEXT.md](docs/MIRROR_CONTEXT.md) | Shared facts + checklists (read first for deep work) |
| [PROJECT_BRIEF.md](docs/PROJECT_BRIEF.md) | Purpose, scope, constraints, inventory |
| [ARCHITECTURE.md](docs/ARCHITECTURE.md) | System diagram and component choices |
| [FSD.md](docs/FSD.md) | Living functional specification |
| [GITHUB.md](docs/GITHUB.md) | Remotes, branching, sync habits |
| [LESSONS_LEARNED.md](docs/LESSONS_LEARNED.md) | Mistakes and fixes |
| [IDEATION_BACKLOG.md](docs/IDEATION_BACKLOG.md) | Ideas, MoSCoW, Alexa / camera / gesture (pre-FSD) |
| [DESIGN_READINESS.md](docs/DESIGN_READINESS.md) | **Before theme work:** checklist + UX agent outputs (`docs/design/`) |
| [UI_MODES.md](docs/UI_MODES.md) | Sleep / passive / active / Pomodoro modes; dual viewing distance; weather hierarchy |
| [HA_DEV.md](docs/HA_DEV.md) | HA on Pi 5, mirror Pi 4, MCP + tokens (no secrets in git) |
| [agents/](agents/README.md) | Planner, UX, Architect, Coder, Tester |
| [resources/reference/](resources/reference/README.md) | Links and datasheets |

---

## Frugal / free-leaning practices (starting point)

- **UI:** **Custom** open web stack on the Pi + Chromium kiosk; you own the code path for glass and night mode.
- **Voice:** Cloud-backed Google path **accepted** for v1; document privacy boundaries in FSD.
- **Home Assistant:** Prefer **local WebSocket/API** and **long-lived tokens** on the Pi only — never commit tokens.
- **Weather / calendar:** Prefer HA entities or self-hosted calendars; avoid new paid APIs unless necessary.

---

## Home Assistant & MCP

- **HA:** Runs on a **Pi 5** on the LAN; mirror **Pi 4** displays state via local backend (**FR-006**). Details: [HA_DEV.md](docs/HA_DEV.md).
- **MCP (Cursor):** **Development-time** tooling pointed at HA — **never** commit tokens; not a mirror runtime dependency unless you add it explicitly later.

---

## Using agents in Cursor

1. Read [AGENTS.md](AGENTS.md) for when to invoke which role.  
2. Use [`.cursor/skills/`](.cursor/skills/) when this directory is the workspace root.

---

## License

Specify before wider publication (e.g. MIT for docs-only phase).
