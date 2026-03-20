# Ideation backlog — Magic Mirror

**Purpose:** Capture product ideas, integration patterns, and prioritization **before** they become formal requirements in [FSD.md](FSD.md).  
**Last updated:** 2026-03-20  

**Room context:** Mirror lives in **child’s bedroom** with an Echo Dot using the **“Echo”** wake word — see [PROJECT_BRIEF.md](PROJECT_BRIEF.md) §1.

---

## Owner decisions (captured from planning)

These are **directional** until promoted to the FSD with acceptance criteria.

| Topic | Decision |
|-------|----------|
| **Alexa / Echo** | Use Echo Dot as a **satellite to Home Assistant** — you added the **Alexa Devices** integration and authenticated; discovered devices are in HA. |
| **Music** | Prefer playing music **through the Echo Dot** (connected to better speakers), not necessarily through the mirror’s Pi audio path. |
| **Routines** | Use **Alexa Routines** (or equivalent) to drive **mirror modes** — e.g. **Good morning** / **Good night** — by setting HA entities the mirror already displays or reacts to. |
| **Alexa-only features** | Lean on Alexa for **music, timers, shopping list, intercom, alarms**, and other skills where the mirror UI is unnecessary. |
| **Camera (USB or Pi Camera v2.1)** | Interest in **presence detection**; optional path toward **gesture** (e.g. point + voice “click”) to compensate for **no touchscreen**. |
| **LD4020** | You have this device — treat as **additional presence sensing** alongside or instead of camera for some use cases (see §Hardware notes). |
| **Occupant needs** | Son benefits from support for **organization and time management**; **Pomodoro** is already in use — mirror should reinforce with **glanceable** feedback, not nagging. |
| **Pomodoro + voice** | **Echo** (wake word **“Echo”**) drives **HA** for start/pause/skip; mirror shows **large visual countdown** and phase (work / short break / long break). **Promoted** to [FSD.md](FSD.md) as **FR-008** (Should). |

---

## What is MoSCoW?

**MoSCoW** is a **prioritization** acronym used in agile and product planning. It sorts ideas into four buckets so the team knows what to build first and what to explicitly **defer**.

| Letter | Meaning | Typical use in this project |
|--------|---------|------------------------------|
| **M — Must** | Required for the release to be considered successful | Example: kiosk UI, HA-backed tiles, FR-006 token safety, night mode (FR-007) |
| **S — Should** | Important; include if capacity allows; painful to omit | Example: reliable HA reconnect indicator, Alexa-driven mode scenes |
| **C — Could** | Nice-to-have; drop first if schedule slips | Example: gesture “point to module,” camera-based lux hint |
| **W — Won’t** | **Not** in this timeframe — intentionally out of scope (may revisit later) | Example: always-on facial recognition, cloud video upload of bedroom |

**Why it helps**

- Stops “everything is priority 1” — forces **tradeoffs**.
- **Won’t** is as valuable as **Must**: it records *we decided not to*, so the idea doesn’t creep back without a formal change.
- Works well with your **Planner** agent (phases) and **Tester** agent (Must items get acceptance tests first).

**How to integrate MoSCoW with the FSD**

1. In [FSD.md](FSD.md), the **Priority** column on requirements already uses MoSCoW labels (**Must / Should / Could**). **Won’t** items usually live in **Out of scope** or this ideation doc until promoted.
2. When an idea here **matures**, add a row to FSD §4 (functional) or §5 (non-functional) with a new **FR/NFR ID** and set **MoSCoW**.
3. **Promote** from this file to FSD in **small chunks** (one vertical slice at a time), then **remove or mark “→ FSD FR-xxx”** here to avoid duplicate truth.

**Example MoSCoW table for a future “Alexa + modes” slice**

| Idea | MoSCoW | Notes |
|------|--------|--------|
| HA `input_select` or `scene` for mirror mode (morning/day/evening/night) | **Must** (if Alexa routines are Must) | Routines set HA; mirror subscribes like any other entity |
| Echo plays Spotify / Amazon Music via speakers | **Should** | Alexa-only; mirror might only show “now playing” if desired |
| Gesture point-to-module | **Could** | Depends on camera placement, lighting, CV effort |
| Continuous video recording to cloud | **Won’t** (v1) | Bedroom privacy |

---

## Alexa + Home Assistant — integration patterns

**Current state:** Alexa Devices integration authenticated; devices available in HA.

**Satellite model (your preference)**

- **Echo** = voice + music + Amazon ecosystem; **HA** = automation hub; **mirror** = glanceable display driven by HA state.
- Mirror **does not** need direct Alexa API access if **HA** exposes everything the UI needs (mode, playing state optional, etc.).

**Routines → mirror modes**

1. Define **HA helpers**: e.g. `input_select.mirror_mode` with options `morning | day | evening | night` **or** use **scenes** (`scene.mirror_good_night`).
2. **Alexa Routine:** “When I say Good night” → **Home Assistant** action → call service to set that input_select or activate scene.
3. **Mirror app** subscribes to the entity via existing **backend + WebSocket** stack; UI theme / layout density follows mode (extends FR-007 night mode concept).

**Music through Echo + speakers**

- Playback is **Alexa-native** (voice or app). Optional mirror tile: **media_player** entity in HA (if exposed) for **title/artist** or “playing / paused” — **Could** MoSCoW.
- Avoid duplicating playback on Pi speakers unless you explicitly want dual output.

**Alexa-only features (use freely)**

- Timers, alarms, announcements, Drop In, skills, shopping list.
- **HA automation** can still **trigger** announcements on Echo for rare events (e.g. leak sensor) while mirror shows a calm alert UI.

**Voice overlap (mirror AIY vs Echo)**

- In **this bedroom**, **Echo + “Echo” wake word** is the **primary voice surface** for **daily use** (music, Pomodoro via HA, general Alexa).
- **Mirror AIY / Google path** can complement (e.g. glance-specific commands) but **avoid duplicating** the same Pomodoro start phrase on two devices unless you enjoy wake-word races.
- **FSD** now includes **FR-008** (mirror shows Pomodoro); voice control path is **Echo → HA**, not Amazon’s generic timer unless you accept **no mirror sync**.

**Reference**

- [Home Assistant — Alexa integration](https://www.home-assistant.io/integrations/alexa/) (cloud + smart home options vary by setup).

---

## Pomodoro timer — voice + mirror countdown

**Goal:** Support the **Pomodoro method** with **voice** (son already uses Echo) and a **clear, calm countdown** on the mirror (no phone unlock).

### Principles

- **Home Assistant = source of truth** for “is a focus session running?” and **remaining time** (or derivable state). The mirror **only renders** HA state (same stack as other tiles).
- **Echo** handles **voice**; phrases should trigger **HA scripts/services** (via Alexa → HA integration), **not** only the built-in Alexa kitchen timer — otherwise the mirror cannot subscribe to that timer.
- **UX:** Large digits, high contrast on glass, **supportive** labels (“Focus”, “Short break”) — avoid shaming or streak pressure unless the family wants it.

### HA implementation patterns (pick one family; refine in implementation)

1. **`timer` entities** — e.g. `timer.pomodoro_focus` (25 min), `timer.pomodoro_short_break` (5 min). Services: `timer.start`, `timer.pause`, `timer.cancel`, `timer.finish`. While **active**, the `timer` exposes a **`remaining`** attribute ideal for WebSocket-driven countdown UIs.
2. **`input_select`** for **phase** (`idle` | `focus` | `short_break` | `long_break`) + automations to start the correct timer and chain cycles (optional long break every N focus rounds via `input_number`).
3. **Scripts** `script.pomodoro_start`, `script.pomodoro_pause`, etc., exposed to **Alexa** as **scenes** or **entities** per your HA Alexa config.

### Voice phrases (examples — map in HA/Alexa)

- “Echo, start focus” → start 25 min focus timer + set phase.  
- “Echo, pause focus” / “Echo, skip break” → call matching HA services.  
Exact utterances depend on [Alexa Smart Home](https://www.home-assistant.io/integrations/alexa/) entity names and routines.

### Mirror module

- Subscribe to `timer.*` and/or `input_select.pomodoro_phase` (names TBD).  
- When the focus/break **timer is active** (or paused with `remaining` available), render **MM:SS** from attributes; show **phase label**; optional subtle progress ring (Could).

### MoSCoW (this slice)

| Piece | MoSCoW | FSD |
|-------|--------|-----|
| Visible countdown + phase from HA | **Should** | **FR-008** |
| Echo voice → HA for Pomodoro | **Should** | tied to FR-004 / FR-008 + HA config |
| Long-break cadence, per-task labels | **Could** | later rows |
| Streaks / parental reporting | **Won’t** (unless family asks) | privacy/trust |

---

## Camera — presence, gesture, “point to module”

**Hardware:** USB camera or **Raspberry Pi Camera v2.1** (pick one mounting + cable path in frame).

**Presence detection (Could → Should depending on ambition)**

- Run **lightweight** logic on Pi or a companion service: motion / occupancy signal → **binary_sensor** or **occupancy** in HA.
- Mirror UI: optional “room occupied” affects **dimming**, **screensaver**, or **pause sensitive info** — **policy decision** with household.

**Gesture / point + voice “click” (Could)**

- **Problem:** Mirror is **not touch**; pointing at on-screen **modules** could select focus before a **voice command** (“that one” / “open”).
- **Approach sketch:** camera sees hand/arm; estimate **screen region** (homography after calibration); map to **module bounding boxes** in layout; **confirm** with voice to avoid false positives.
- **Risks:** mirror **reflection**, **lighting**, **angle**, CPU/heat. Start with **one** gesture (e.g. palm up = wake region picker) before multi-gesture grammar.

**Privacy**

- Default **camera off** or **physically shuttered** when not needed; schedule aligned with **night** / **sleep**.
- Prefer **local processing**; avoid uploading continuous video. Document **Won’t** for cloud DVR in bedroom unless explicitly agreed.

---

## LD4020 + camera (complementary sensing)

**LD4020:** You identified this part — **verify exact model and datasheet** (similar consumer lines include LD2410 / LD2450-class **mmWave** presence sensors, often paired with ESPHome → HA). If LD4020 is **mmWave / radar**:

| Sensor | Strength | Typical role |
|--------|----------|--------------|
| **LD4020 (or similar)** | Presence / motion without optics | **Primary occupancy** for “someone in room” with fewer privacy concerns than camera |
| **Camera** | Richer signal for **gesture** / optional scene context | **Secondary** — use when gesture or calibration features justify it |

**Integration:** Expose presence entities to HA; mirror and Alexa routines can both **read** the same truth (“if occupied, don’t blast bright morning layout at 2am”).

---

## Candidate feature list (unprioritized — assign MoSCoW when ready)

| ID | Idea | Suggested first MoSCoW |
|----|------|-------------------------|
| IB-01 | HA entity for **mirror mode** driven by Alexa routines | Should |
| IB-02 | **Music** on Echo; optional “now playing” on mirror via HA | Could |
| IB-03 | **Presence** via LD4020 → HA → mirror behavior | Could |
| IB-04 | **Presence** via camera (motion / simple CV) | Could |
| IB-05 | **Gesture** region select + voice confirm | Could |
| IB-06 | **Point-to-module** activation | Could (high effort) |
| IB-07 | Camera-based **ambient / glare** hint for auto-contrast | Won’t (v1) unless promoted |
| IB-08 | **Pomodoro** HA timers + mirror countdown | **Should** → **FR-008** |
| IB-09 | Echo phrases / routines for Pomodoro control | **Should** |
| IB-10 | Pomodoro **chime** on Echo at phase end (optional) | **Could** |

---

## Next steps (process)

1. Implement **HA** `timer` + `input_select` (or equivalent) + scripts; expose to **Echo**; validate with son’s phrasing.  
2. Mirror UI: **FR-008** module subscribing to those entities.  
3. Pick **one** Alexa + HA slice for **modes** if not done: **IB-01** — helpers + routines.  
4. Decide **LD4020** exact integration path in HA; add to [PROJECT_BRIEF.md](PROJECT_BRIEF.md) inventory when confirmed.  
5. Defer **gesture** until kiosk + HA + modes are stable (Planner **Phase 4+**).  
6. Update this doc when ideas change; **FSD** remains the contract for what’s actually built.
