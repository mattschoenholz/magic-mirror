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
| Display planning resolution | **1280×720** until Samsung TV native resolution confirmed |
| TV | Samsung (model TBD); **120 V**; HDMI wake **unknown** |
| Pi | Raspberry Pi 4 Model B (2018); **RAM TBD** |
| AIY Voice HAT | **Deferred** — not part of v1 install |
| Voice (v1) | **Echo → HA** only |
| Audio | **Echo + room speakers** for music / Alexa TTS |
| Night mode | **FR-007** — softer UI + restrained audio (see FSD) |
| **Room** | **Child’s bedroom** — supportive UX; see [PROJECT_BRIEF.md](PROJECT_BRIEF.md) |
| **Echo Dot** | Wake word **“Echo”**; **Pomodoro** voice via **Echo → HA**; mirror shows **FR-008** countdown |

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

---

## Planner phases (summary)

Full detail in `agents/planner.md`. Phases **0–5**:

0. **Baseline** — Confirm HDMI/video mode, TV power behavior, Pi RAM.  
1. **Requirements** — Lock v1 modules, voice whitelist shape, night mode rules.  
2. **Architecture** — OS/kiosk, HA client, voice stack, audio output, secrets.  
3. **UX** — Zones, type scale, tokens, optional 1280×720 layout artifact.  
4. **Implementation** — Vertical slices per FSD.  
5. **Test & polish** — Tester exit criteria, glass + voice in room.

---

## Home Assistant integration (checklist)

- [ ] Long-lived token on Pi only; file perms **600**; never in git or browser bundle  
- [ ] Prefer WebSocket for live state; define reconnect/backoff  
- [ ] Whitelist service calls / intents; document entity IDs in ARCHITECTURE as templates only  
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
- Layout safe area: account for bezel; design at **1280×720** until 1080p confirmed

---

## Resources

Add vetted links under [resources/reference/](resources/reference/links.md).
