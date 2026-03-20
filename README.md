# Wall Magic Mirror (Pi 4 + AIY Voice Hat)

A **planning and documentation** home for a wall-mounted smart mirror: two-way glass over an HDMI display, driven by a **Raspberry Pi 4** with voice via the **Google AIY Voice Kit HAT**, integrated with **Home Assistant**. Voice may use **Google account / cloud** per project decision.

> **Status:** Ideation / specification — application code comes later.  
> **GitHub:** [github.com/mattschoenholz/magic-mirror](https://github.com/mattschoenholz/magic-mirror)

---

## Local project path

Open this folder as the Cursor **workspace root** so `.cursor/skills/` load correctly:

`~/Desktop/CurrentProjects/General/magic-mirror`

**Layout:** `agents/` and `.cursor/skills/` live **here** (not inside any other repo).

---

## Purpose (draft)

- **Primary:** Glanceable, calm “dashboard on the wall” for time, weather, calendar highlights, and home state — readable at arm’s length in a bedroom.
- **Secondary:** Hands-free commands for common actions (lights, scenes, climate) via voice, aligned with Home Assistant automations.
- **Night mode:** Softer UI and restrained audio for overnight use.
- **Non-goals (v1):** Full conversational assistant, heavy video, or replacing the phone for complex HA admin.

Hardware notes (glass size, TV, Pi, audio): [docs/PROJECT_BRIEF.md](docs/PROJECT_BRIEF.md).

---

## Quick links

| Document | Role |
|----------|------|
| [PROJECT_BRIEF.md](docs/PROJECT_BRIEF.md) | Purpose, scope, constraints, inventory |
| [ARCHITECTURE.md](docs/ARCHITECTURE.md) | System diagram and component choices |
| [FSD.md](docs/FSD.md) | Living functional specification |
| [GITHUB.md](docs/GITHUB.md) | Remotes, branching, sync habits |
| [LESSONS_LEARNED.md](docs/LESSONS_LEARNED.md) | Mistakes and fixes |
| [agents/](agents/README.md) | Planner, UX, Architect, Coder, Tester |
| [resources/reference/](resources/reference/README.md) | Links and datasheets |

---

## Frugal / free-leaning practices (starting point)

- **UI:** Open web stack on the Pi (e.g. Chromium kiosk) or a maintained Magic Mirror–style framework — decide in architecture phase.
- **Voice:** Cloud-backed Google path **accepted** for v1; document privacy boundaries in FSD.
- **Home Assistant:** Prefer **local WebSocket/API** and **long-lived tokens** on the Pi only — never commit tokens.
- **Weather / calendar:** Prefer HA entities or self-hosted calendars; avoid new paid APIs unless necessary.

---

## Home Assistant & MCP

- **HA:** Primary integration for sensors, scenes, and voice-routed actions.
- **MCP (Cursor):** **Development-time** tooling — not a runtime dependency on the mirror unless you add that explicitly later.

---

## Using agents in Cursor

1. Read [AGENTS.md](AGENTS.md) for when to invoke which role.  
2. Use [`.cursor/skills/`](.cursor/skills/) when this directory is the workspace root.

---

## License

Specify before wider publication (e.g. MIT for docs-only phase).
