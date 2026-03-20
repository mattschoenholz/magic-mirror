# Ideation backlog — Magic Mirror

**Purpose:** Capture product ideas, integration patterns, and prioritization **before** they become formal requirements in [FSD.md](FSD.md).  
**Last updated:** 2026-03-20

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

- Keep **roles split**: e.g. **mirror** = glance + tight HA controls + custom UI feedback; **Echo** = music + general Alexa + some HA scenes.
- Document in FSD later: which **intents** are mirror-only vs Echo-only to reduce “two bosses in one room.”

**Reference**

- [Home Assistant — Alexa integration](https://www.home-assistant.io/integrations/alexa/) (cloud + smart home options vary by setup).

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

---

## Next steps (process)

1. Pick **one** Alexa + HA slice: e.g. **IB-01** as **Should** — implement helpers + routines, then **promote** to FSD with FR IDs.  
2. Decide **LD4020** exact integration path in HA; add to [PROJECT_BRIEF.md](PROJECT_BRIEF.md) inventory when confirmed.  
3. Defer **gesture** until kiosk + HA + modes are stable (Planner **Phase 4+**).  
4. Update this doc when ideas change; **FSD** remains the contract for what’s actually built.
