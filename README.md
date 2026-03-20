# Wall Magic Mirror (Pi 4 + AIY Voice Hat)

A **planning and documentation** home for a wall-mounted smart mirror: mirror glass in front of an existing HDMI display, driven by a Raspberry Pi with optional hands-free voice via the **Google AIY Voice Kit HAT**, integrated with **Home Assistant** (including MCP where useful).

> **Status:** Ideation / specification only — no application implementation in this phase.  
> **Note:** This folder lives inside the SailboatServer workspace for now; treat it as its **own product**. When ready, move this directory to a dedicated repo or open it as the Cursor workspace root so `.cursor/skills/` apply cleanly.

---

## Purpose (draft)

- **Primary:** Glanceable, calm “dashboard on the wall” for time, weather, calendar highlights, and home state — readable at arm’s length in a bedroom.
- **Secondary:** Hands-free commands for common actions (lights, scenes, climate) via voice, aligned with Home Assistant automations.
- **Non-goals (for v1):** Full conversational assistant, heavy video, or replacing the phone for complex HA admin.

Refine purpose after you answer the checklist in [docs/PROJECT_BRIEF.md](docs/PROJECT_BRIEF.md).

---

## Quick links

| Document | Role |
|----------|------|
| [PROJECT_BRIEF.md](docs/PROJECT_BRIEF.md) | Purpose, scope, constraints, frugal stack, open questions |
| [ARCHITECTURE.md](docs/ARCHITECTURE.md) | High-level system diagram and component choices |
| [FSD.md](docs/FSD.md) | Living functional specification (update as you build) |
| [GITHUB.md](docs/GITHUB.md) | Version control and GitHub workflow |
| [LESSONS_LEARNED.md](docs/LESSONS_LEARNED.md) | Mistakes and fixes during the project |
| [agents/](agents/README.md) | Multi-agent role definitions (Planner → Tester) |
| [resources/reference/](resources/reference/README.md) | Curated links and downloaded refs |

---

## Frugal / free-leaning practices (starting point)

- **UI:** Open web stack on the Pi (e.g. Chromium kiosk) or a maintained Magic Mirror–style framework only if it fits voice + HA cleanly — decide in architecture phase.
- **Voice:** Prefer **on-device or low-cost** paths: AIY HAT historically pairs with Google Assistant APIs (account/cloud); alternatives (local wake word + HA conversation) exist — capture the tradeoff in FSD §Non-functional.
- **Home Assistant:** Use your existing server; prefer **local WebSocket/API** and **long-lived tokens** stored on-device securely — never commit tokens.
- **Weather / calendar:** Prefer HA entities or self-hosted calendars; avoid new paid APIs unless necessary.
- **CAD / enclosure:** You already have CNC, laser, 3D printer — budget is materials + time, not tooling.

---

## Home Assistant & MCP

- **HA:** Primary integration surface for sensors, scenes, and voice-routed actions.
- **MCP (Cursor):** Useful for **development-time** queries and docs — not a runtime dependency on the mirror unless you explicitly design that later.

Details: [docs/PROJECT_BRIEF.md](docs/PROJECT_BRIEF.md#home-assistant--mcp).

---

## Using agents in Cursor

1. Read [AGENTS.md](AGENTS.md) for when to invoke which role.
2. Point the chat at the relevant file under [agents/](agents/) or rely on [`.cursor/skills/`](.cursor/skills/) if this folder is the workspace root.

---

## License

Specify before first public push (e.g. MIT for docs-only phase).
