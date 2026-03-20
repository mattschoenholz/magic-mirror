# Functional Specification Document (FSD)

**Project:** Wall Magic Mirror (Pi 4 display + Home Assistant + Echo Dot)  
**Document type:** Living specification — update on every scope or behavior change.  
**Version:** 0.9  
**Last updated:** 2026-03-20

---

## Document control

| Version | Date | Author | Summary of change |
|---------|------|--------|-------------------|
| 0.1 | 2026-03-20 | — | Initial skeleton + placeholder requirements |
| 0.2 | 2026-03-20 | — | Hardware inventory; night mode FR; 720p planning assumption |
| 0.3 | 2026-03-20 | — | Agent/skill refresh; see [MIRROR_CONTEXT.md](MIRROR_CONTEXT.md) for shared baselines |
| 0.4 | 2026-03-20 | — | **Custom web UI + local HA backend** stack; reference skills `mm-home-assistant`, `mm-kiosk-pi`, `mm-voice-aiy-google`, `mm-dev-mcp-ha` |
| 0.5 | 2026-03-20 | — | Link [IDEATION_BACKLOG.md](IDEATION_BACKLOG.md); Alexa/Echo + camera ideas pending promotion |
| 0.6 | 2026-03-20 | — | Child bedroom context; Echo wake word; **FR-008** Pomodoro countdown; personas + UC-6 |
| 0.7 | 2026-03-20 | — | **v1:** Pi = display + HA backend only; **Echo-only** voice; AIY deferred; **FR-009** tiles; todo/calendar/weather modules |
| 0.8 | 2026-03-20 | — | [DESIGN_READINESS.md](DESIGN_READINESS.md); [design/](design/) for pre-code theme artifacts |
| 0.9 | 2026-03-20 | — | Dual viewing distances; [UI_MODES.md](UI_MODES.md); weather today+forecast; [HA_DEV.md](HA_DEV.md) MCP/Pi5 |

---

## 1. Purpose & scope

**Purpose:** Define *what* the system must do for users and *how* success is verified — without prescribing final implementation.

**Scope:** See [PROJECT_BRIEF.md](PROJECT_BRIEF.md). **UI modes & hierarchy:** [UI_MODES.md](UI_MODES.md). **HA dev / MCP / tokens:** [HA_DEV.md](HA_DEV.md). Shared context: [MIRROR_CONTEXT.md](MIRROR_CONTEXT.md). **Ideas:** [IDEATION_BACKLOG.md](IDEATION_BACKLOG.md). **Design gate:** [DESIGN_READINESS.md](DESIGN_READINESS.md) → [design/](design/). This FSD tracks **functional** and **non-functional** requirements and traceability to tests.

---

## 2. Definitions

| Term | Definition |
|------|------------|
| **Module** | A UI region showing one concern (e.g. clock, weather summary). |
| **Mirror app** | **Custom web frontend** (HTML/CSS/JS or light framework) shown in Chromium kiosk — **not** MagicMirror² for v1. |
| **Local backend** | Process on the Pi that holds the HA token and exposes a minimal API to the browser (**FR-006**). |
| **Intent** | A voice-mapped action resolved to a Home Assistant service call. |
| **Kiosk mode** | Full-screen display with no casual OS chrome visible. |
| **MoSCoW** | **Must / Should / Could / Won’t** — priority labels in §4–§5; explained in [IDEATION_BACKLOG.md](IDEATION_BACKLOG.md). |
| **Pomodoro session** | A timed **focus** or **break** interval driven by **Home Assistant** (`timer` / `input_select` / scripts — see [IDEATION_BACKLOG.md](IDEATION_BACKLOG.md) §Pomodoro). |
| **UI mode** | One of **sleep_off**, **passive**, **active_engaged**, **pomodoro_focus** — controls which modules are prominent or hidden ([UI_MODES.md](UI_MODES.md)). |

---

## 3. Personas & primary use cases

| Persona | Goal |
|---------|------|
| **Student (occupant)** | Use the mirror for **time, focus, and calm cues** in the bedroom; rely on **Echo** (“Echo” wake word) for voice; benefit from **Pomodoro** visibility without a phone. |
| **Parent / household** | Maintain privacy boundaries, night mode, and HA automations that support (not nag) the occupant. |

**Use cases (draft — expand with IDs):**

- UC-1: View current local time and date.
- UC-2: View **today’s weather** as primary; **small** multi-day forecast secondary ([UI_MODES.md](UI_MODES.md) passive mode).
- UC-3: View selected HA entity states (list TBD).
- UC-4: Invoke HA scene or device action by voice (whitelist TBD); **in this room, Echo → HA is primary** for daily voice (see [IDEATION_BACKLOG.md](IDEATION_BACKLOG.md)).
- UC-5: Recover from network loss without manual reboot (behavior TBD).
- UC-6: **Pomodoro:** start/pause/skip via **Echo** voice to **HA**; see **live countdown and phase** (focus / break) on the mirror.
- UC-7: View **weather** for the day or week (HA `weather` or equivalent entities).
- UC-8: View **school calendar** (HA `calendar` / CalDAV-backed calendar exposed in HA).
- UC-9: View a **todo / task list** driven by HA (`todo`, `shopping_list`, or agreed helper entities).
- UC-10: Experience **fluid UI modes** — sleep/off, passive, active/engaged after voice or list work, Pomodoro focus with minimal chrome ([UI_MODES.md](UI_MODES.md)).

---

## 4. Functional requirements

| ID | Requirement | Priority (MoSCoW) | Notes / source |
|----|-------------|-------------------|----------------|
| FR-001 | System shall show a full-screen **custom web** mirror UI after boot without manual login | Must | Chromium kiosk + autostart; see **`mm-kiosk-pi`** |
| FR-002 | System shall display accurate local time | Must | NTP |
| FR-003 | System shall reflect HA entity updates within **TBD** seconds | Must | WebSocket preferred |
| FR-004 | **v1:** Occupant shall use **Echo** (“Echo” wake word) → **HA** for voice actions; mirror does **not** require on-device mic | Must | Phrases / exposed entities TBD; mirror **displays** HA state |
| FR-005 | UI shall remain readable on mirror glass at **~10 ft (~3 m)** (bed/desk) **and** at **~2–3 ft** standing; **far** distance drives minimum type for clock/weather/Pomodoro | Must | Dual-distance Tester checks; [UI_MODES.md](UI_MODES.md) |
| FR-006 | System shall not expose HA token in client-side bundle | Must | Server-side proxy or equivalent |
| FR-007 | System shall provide **night mode** (reduced brightness/contrast of UI); **v1** audio/TTS is primarily on **Echo**, not the Pi | Must | SCHEDULE or manual toggle TBD; see PROJECT_BRIEF |
| FR-008 | When HA reports an **active Pomodoro / focus timer** (or equivalent entity set), the mirror shall show a **large, readable countdown** and **phase** (e.g. focus vs short break); in **pomodoro_focus** mode, UI is **dominated** by timer + pause/resume/new prompts ([UI_MODES.md](UI_MODES.md)) | Should | Echo → HA; entity IDs TBD |
| FR-009 | Mirror shall show **HA-backed** **weather** (**today** primary layout; **next few days** smaller secondary), **school calendar**, and **visual todo** per agreed entity IDs | Should | Matches passive-mode hierarchy in [UI_MODES.md](UI_MODES.md) |
| FR-010 | Mirror shall implement **fluid, mode-driven** presentation: **sleep_off**, **passive**, **active_engaged**, **pomodoro_focus** — hierarchy and visible modules change per mode; mode driven by **HA state** (entity or derived rule) | Should | [UI_MODES.md](UI_MODES.md); `input_select` or equivalent TBD |

**Display planning assumption:** Design layouts for **1280×720** until Samsung TV **native resolution** is confirmed; scale to **1080p** if supported (viewable glass **32.5 cm × 59 cm**).

*Add rows as modules and voice intents are decided.*

---

## 5. Non-functional requirements

| ID | Requirement | Target | Verification |
|----|-------------|--------|--------------|
| NFR-001 | Availability (mirror UI) | **TBD** % monthly | Logs / HA ping |
| NFR-002 | Power loss recovery | Auto-boot to UI | Tester checklist |
| NFR-003 | Thermal stability | No sustained throttle under **kiosk + backend** idle | `vcgencmd` / stress notes |
| NFR-004 | Security | No secrets in repo; least-privilege HA token | Grep + HA audit |
| NFR-005 | Readability | **10 ft** and **2–3 ft** both pass mirror-glass review for Must-tier content | UX + Tester |

---

## 6. Voice (functional subset)

**v1:** Voice is **not** processed on the Pi. Document **Echo → HA** mappings (Alexa app / HA Alexa integration) here or in `docs/` runbook as you implement.

| Intent ID | Example (Echo) | HA action | Notes |
|-----------|----------------|-----------|--------|
| VI-001 | *TBD — e.g. start focus* | Start Pomodoro / `timer` / script | Must sync mirror **FR-008** |
| VI-002 | *TBD* | *TBD* | |

*Security / sanity:* Prefer HA-controlled scripts; avoid relying on **Alexa-only** timers for anything the mirror must display.

---

## 7. UI modules (inventory)

| Module ID | Content | Data source | Owner (agent) |
|-----------|---------|-------------|---------------|
| M-001 | Clock | System / HA | UX |
| M-002 | **Weather** — **today** prominent; **multi-day** compact secondary | HA `weather.*` / forecast entities | Architect |
| M-003 | HA / home summary (optional) | HA | Architect |
| M-004 | **Pomodoro** — countdown + phase | HA `timer` / `input_select` / scripts (TBD) | UX + Architect |
| M-005 | **School calendar** | HA `calendar.*` | Architect + household (which calendar) |
| M-006 | **Visual todo / tasks** | HA `todo`, `shopping_list`, or helpers | Architect |
| M-007 | **Mode shell** (layout / which regions visible) | HA `input_select` / automations for UI mode | Architect + UX |

---

## 8. Out of scope (reference)

Duplicated from brief; keep in sync with [PROJECT_BRIEF.md](PROJECT_BRIEF.md).

- **MagicMirror²** (or similar mirror frameworks) for **v1** — custom web UI only; may revisit later.
- **AIY Voice HAT / mirror-mounted Google voice** for **v1** — deferred; see [PROJECT_BRIEF.md](PROJECT_BRIEF.md).

---

## 9. Acceptance criteria template

For each FR/UC, add:

- **Given** … **When** … **Then** …
- Link to Tester agent case ID when implemented.

---

## 10. Change log (running)

- **0.1** — Skeleton created; requirements to be refined after inventory and UX pass.
- **0.2** — Inventory filled (glass, TV, Pi, AIY, Google cloud, audio options); FR-007 night mode; 720p baseline.
- **0.3** — Planner phases + task template; UX/architect/coder/tester rigor; [MIRROR_CONTEXT.md](MIRROR_CONTEXT.md); `.claude` symlinks.
- **0.4** — Stack locked: custom web + local HA API backend; domain reference skills; MagicMirror² out of scope for v1.
- **0.5** — [IDEATION_BACKLOG.md](IDEATION_BACKLOG.md): Alexa satellite, routines, camera/LD4020/gesture ideation; MoSCoW definition.
- **0.6** — Child bedroom + Echo wake word; **FR-008** / **M-004** Pomodoro; **UC-6**; personas.
- **0.7** — **v1 voice = Echo only**; Pi display-only; **FR-009**; **M-005** / **M-006**; **UC-7–9**; AIY out of scope v1.
- **0.8** — Design gate: **DESIGN_READINESS** + **docs/design/** for UX outputs before implementation.
- **0.9** — **UI_MODES** (4 modes, fluid hierarchy); dual viewing distances **FR-005** / **NFR-005**; weather today+forecast; **HA_DEV** (HA on Pi 5, MCP, tokens); **FR-010**, **M-007**.
