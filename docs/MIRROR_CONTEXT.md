# Magic Mirror — shared context (read first)

Single reference for agents and skills. **Update this file** when hardware facts or baseline assumptions change; bump `docs/FSD.md` when requirements change.

---

## Stack (locked)

| Layer | Choice |
|-------|--------|
| **Mirror UI** | **Custom web app** (vanilla or light framework) in **Chromium kiosk** on Pi |
| **Home Assistant** | **REST + WebSocket** from a **local backend** on the Pi; token **never** in the browser bundle (**FR-006**) |
| **Voice (v1)** | **Echo Dot** (“**Echo**”) → **Alexa** → **Home Assistant** — Pi has **no** mirror-mounted mic |
| **Pi role (v1)** | **Display** (Chromium) + **local HA backend** only |
| **Not used (v1)** | **MagicMirror²**; **AIY HAT** on mirror (optional **later**) |

Domain reference skills: `mm-home-assistant`, `mm-kiosk-pi`, `mm-dev-mcp-ha`. **`mm-voice-aiy-google`** = if AIY returns to scope.

---

## Hardware & assumptions (from PROJECT_BRIEF)

| Topic | Value / status |
|--------|----------------|
| Mirror viewable area | **32.5 cm × 59 cm** |
| Display | **1920×1080** HDMI; **portrait** use → **1080×1920** viewport (verify with [PI_BRINGUP.md](PI_BRINGUP.md) stub) |
| TV | Samsung (model TBD); **120 V**; HDMI wake **unknown** |
| Pi | Raspberry Pi 4 Model B (2018); **RAM TBD** |
| AIY Voice HAT | **Deferred** — not part of v1 install |
| Voice (v1) | **Echo → HA** only |
| Audio | **Echo + room speakers** for music / Alexa TTS |
| Night mode | **FR-007** — softer UI + restrained audio (see FSD) |
| **Room** | **Child’s bedroom** — supportive UX; see [PROJECT_BRIEF.md](PROJECT_BRIEF.md) |
| **Echo Dot** | Wake word **“Echo”**; **Pomodoro** voice via **Echo → HA**; mirror shows **FR-008** countdown |
| **Viewing distance** | **~10 ft** (bed/desk) + **~2–3 ft** (at mirror) — see [UI_MODES.md](UI_MODES.md) |
| **Home Assistant** | **Pi 5** on LAN; mirror **Pi 4** is display + local HA API client only |

---

## Canonical docs

| File | Use |
|------|-----|
| [PROJECT_BRIEF.md](PROJECT_BRIEF.md) | Inventory, risks, goals |
| [FSD.md](FSD.md) | FR/UC/NFR, acceptance |
| [ARCHITECTURE.md](ARCHITECTURE.md) | Diagrams, decisions, security |
| [LESSONS_LEARNED.md](LESSONS_LEARNED.md) | Postmortems |
| [GITHUB.md](GITHUB.md) | Remotes, HTTPS workflow |
| [IDEATION_BACKLOG.md](IDEATION_BACKLOG.md) | Future ideas, MoSCoW, Alexa/camera — before FSD promotion |
| [DESIGN_READINESS.md](DESIGN_READINESS.md) | Checklist before UX theme; outputs in [design/](design/) |
| [UI_MODES.md](UI_MODES.md) | Four UI modes, dual viewing distance, weather hierarchy |
| [HA_DEV.md](HA_DEV.md) | HA on Pi 5 vs mirror Pi 4, MCP, token hygiene |
| [MIRROR_RUNTIME.md](MIRROR_RUNTIME.md) | **Locked** HA entity IDs, ICS URLs, timezone, secrets layout, Spotify/YouTube policy |
| [BACKEND_HA_INTEGRATION_2026-03.md](BACKEND_HA_INTEGRATION_2026-03.md) | **Snapshot / HA handoff:** weather-now vs hourly, todos overflow, API shapes, code map, new-machine checklist |
| [PI_BRINGUP.md](PI_BRINGUP.md) | Mirror Pi 4 OS + display + network baseline |
| [MAC_VS_PI_COMMANDS.md](MAC_VS_PI_COMMANDS.md) | **Copy-paste**: Mac Terminal vs SSH (no keyboard on Pi) |

---

## Planner phases (summary)

Full detail in `agents/planner.md`. Phases **0–5**:

0. **Baseline** — Follow [PI_BRINGUP.md](PI_BRINGUP.md): HDMI/video mode, TV power behavior, Pi RAM, HA reachable from Pi.  
1. **Requirements** — Lock v1 modules, voice whitelist shape, night mode rules.  
2. **Architecture** — OS/kiosk, HA client, voice stack, audio output, secrets.  
3. **UX** — Zones, type scale, tokens, **1080×1920 portrait** layout artifact.  
4. **Implementation** — Vertical slices per FSD.  
5. **Test & polish** — Tester exit criteria, glass + voice in room.

---

## Home Assistant integration (checklist)

- [ ] Long-lived token on Pi only; file perms **600**; never in git or browser bundle  
- [ ] Prefer WebSocket for live state; define reconnect/backoff  
- [ ] Whitelist service calls / intents; entity IDs for mirror tiles: **[MIRROR_RUNTIME.md](MIRROR_RUNTIME.md)**  
- [ ] Behavior when HA unreachable: show stale state + indicator vs blank (decide in FSD)  
- [ ] See **`.cursor/skills/mm-home-assistant/reference.md`** for API patterns

---

## Voice & Google cloud (checklist)

- [ ] AIY / Assistant software path pinned in ARCHITECTURE when chosen  
- [ ] OAuth / credentials on device only; pattern documented, values never committed  
- [ ] Fallback when cloud fails (retry, user message, push-to-talk only — decide in FSD)  
- [ ] See **`.cursor/skills/mm-voice-aiy-google/reference.md`**

---

## UX constraints (mirror)

- Treat glass as **lower contrast** and **reflection-prone**; target **≥3:1** luminance contrast for body text where feasible  
- **Night mode:** lower peak luminance, no decorative use of alarm reds/oranges  
- **Voice:** always pair listening / success / error with **on-screen** state  
- Layout safe area: account for bezel; canvas **1080×1920** portrait (verify with [PI_BRINGUP.md](PI_BRINGUP.md) stub)
- **Wood / mechanical frame** can cover **~20–30 px** of the LCD at edges — keep touch targets and critical UI inside an **extra inset** (see [design/tokens.md](design/tokens.md) safe area)

---

## Resources

Add vetted links under [resources/reference/](resources/reference/links.md).
