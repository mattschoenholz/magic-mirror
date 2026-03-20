# Project brief — Wall Magic Mirror

**Version:** 0.6  
**Last updated:** 2026-03-20

---

## 1. Problem statement

You want a **wall-mounted mirror** that doubles as a **low-distraction information surface** with **glanceable** content (time, **weather**, **school calendar**, **visual todo**, **Pomodoro timer**, etc.), powered by a **Raspberry Pi 4** and **deep integration with Home Assistant**.

**v1 voice simplification:** **All voice** is through the **Echo Dot** (“**Echo**” wake word) → **Home Assistant**. The Pi focuses on **display + local HA API backend** only — **no AIY Voice HAT** on the mirror for the initial project (HAT remains optional hardware for a **later** phase). See [ARCHITECTURE.md](ARCHITECTURE.md).

**Room & user context:** The mirror is installed in **your son’s bedroom**, alongside an **Echo Dot** he already uses with the **“Echo”** wake word (not “Alexa”). A key motivation is supporting **organization and time management**: he uses the **Pomodoro method**, and a **voice-driven Pomodoro** flow with a **large visual countdown** on the mirror may help more than phone-only timers.

---

## 2. Goals (measurable when possible)

| ID | Goal | How we’ll know (later) |
|----|------|-------------------------|
| G1 | Readable at ~2–3 m in typical bedroom lighting | Subjective review + contrast checks on mirror glass |
| G2 | Reliable “at a glance” modules (time, **weather**, **todo**, **calendar**, HA-backed tiles) | Uptime / refresh behavior documented in FSD |
| G3 | Voice (Echo → HA) supports common actions without a phone | Test cases in FSD + Tester; **no** mirror-mounted mic required for v1 |
| G4 | Maintainable software (updates, backups, secrets) | Runbook in README / ARCHITECTURE |
| G5 | **Pomodoro support:** voice (Echo → HA) + **visible countdown** on mirror during focus/break | FSD FR-008; Tester cases; son can complete a full cycle without phone |

---

## 3. Scope

### In scope (candidate)

- **Enclosure:** Mirror glass + Samsung TV are **already mounted in a wooden frame** — remaining work is cabling, Pi placement, service access, and any trim tweaks.
- Pi OS image, **Chromium kiosk** hosting a **custom web UI** (not MagicMirror² for v1); auto-start UI + **local backend** for Home Assistant API (**FR-006**). **Pi does not run voice recognition in v1.**
- HA integration for **tiles**: weather (day/week), **school calendar** (via HA calendar / entity), **visual todo list** (e.g. `todo` integration, `shopping_list`, or `input_text` patterns — Architect picks), Pomodoro/timer entities, modes/scenes.
- **Voice (v1):** **Echo Dot only** → HA (music, Pomodoro, routines, general Alexa). Mirror **displays** resulting HA state.
- **Night mode:** calmer UI for bedroom (TTS/chimes primarily on **Echo** in v1).
- **Child-bedroom UX:** calm, readable, **non-shaming** copy for focus/time tools; avoid surveillance framing (see risks).
- **Pomodoro (target):** HA-backed timer state + mirror **countdown module**; **Echo** (“Echo” wake word) as primary voice surface for start/pause/skip where possible — details [IDEATION_BACKLOG.md](IDEATION_BACKLOG.md) §Pomodoro.
- Documentation, FSD, version control.

### Out of scope for v1 (unless you promote them)

- **AIY Voice HAT** on the mirror / **Google Assistant** as mirror-mounted voice (defer to **v2+**; hardware can stay in a drawer until then).
- Facial recognition, camera inside mirror glass.
- Heavy animations or video wallpaper.
- Replacing HA as source of truth for complex logic.

### Related ideation (not yet full requirements)

Ideas, MoSCoW primer, Alexa/Echo-as-satellite, camera/LD4020/gesture concepts: **[IDEATION_BACKLOG.md](IDEATION_BACKLOG.md)**. Promote items to [FSD.md](FSD.md) when ready to build and test.

**Home:** **Alexa Devices** integration is set up in HA with discovered devices. In the **son’s room**, the Echo Dot uses the **“Echo”** wake word. The Dot is the preferred **music** output, **Pomodoro-related voice** (via HA, not generic Alexa-only kitchen timers if mirror must stay in sync), and other **Alexa-only** features; **routines** drive HA entities/scenes the mirror reflects (e.g. good morning / good night modes).

---

## 4. Constraints & assumptions

- **Mirror glass — viewable area:** **32.5 cm × 59 cm** (two-way glass; thickness TBD if needed for CAD).
- **Display:** Older **Samsung TV** (model number and **native resolution not yet recorded**). **Planning assumption: 1280×720 (720p)** until confirmed; move UI/layout to **1080p** if the panel supports it.
- **Power:** TV has **120 V plug on the back** — separate from Pi power; **HDMI wake behavior unknown** (test: does panel show Pi signal only when TV is “on”?).
- **Compute:** **Raspberry Pi 4 Model B (2018)** — onboard RAM size TBD (`free -h` on device). **v1:** display + backend only (no mic/speaker required on Pi for voice).
- **AIY Voice HAT:** **Optional / deferred** — on hand for a **later** phase if you add mirror-local voice.
- **Audio (v1):** **Echo Dot** (+ connected speakers) for music and Alexa TTS; Pi may be **HDMI video only** unless you add local UI sounds later.
- **Network:** Home LAN + Home Assistant reachable; prefer **no inbound exposure** from the internet to the Pi.

---

## 5. High-level architecture (one paragraph)

The Pi runs **Chromium in kiosk mode** showing a **custom-built web mirror UI**. A **local backend** on the Pi holds the HA token and talks to Home Assistant via **REST/WebSocket**; the browser talks only to loopback (**FR-006**). **Voice** is **Echo → Alexa cloud → HA**; the mirror **only displays** HA-backed state (timers, lists, calendar, weather, etc.). **Cursor + HA MCP** are for **development on your PC only**, not part of the wall-mounted runtime.

See [ARCHITECTURE.md](ARCHITECTURE.md) for diagrams and options.

---

## 6. Stack decisions

| Area | Decision | Notes |
|------|----------|--------|
| **Mirror UI** | **Custom web + local HA backend** | Full control for glass, night mode, FR-006; more code than MagicMirror² |
| **MagicMirror²** | **Deferred for v1** | Can revisit if maintenance cost of custom UI grows |
| **Voice (v1)** | **Echo Dot → HA only** | Single wake word in room; music + Pomodoro + Alexa on Echo |
| **Voice (future)** | **AIY HAT** + Google **or** HA Assist | Optional second phase on the Pi |
| Calendar / weather / todo | **HA** (`calendar`, `weather`, `todo` / helpers) | School calendar + week forecast + list tiles on mirror |
| Remote admin | SSH over LAN / Tailscale | Keys only, no password SSH |

Reference skills: **`mm-home-assistant`**, **`mm-kiosk-pi`**, **`mm-dev-mcp-ha`** (MCP dev-only). **`mm-voice-aiy-google`** = **future** (only if AIY returns to scope).

---

## 7. Home Assistant & MCP

- **Runtime:** Mirror should use HA **REST + WebSocket** with a **long-lived token** stored in a root-only file or OS secret mechanism — **never** in git.
- **MCP:** **Dev machine only** (Cursor). Skill **`mm-dev-mcp-ha`** — verify entities/services while editing; **never** paste tokens into chat. Not used on the Pi at runtime. Optional: document workflows in [GITHUB.md](GITHUB.md) or `docs/DEV_ENV.md`.

---

## 8. Inventory & decisions checklist

**Hardware (known)**

| Item | Status |
|------|--------|
| Two-way mirror glass — viewable **32.5 × 59 cm** | Installed in frame |
| Samsung TV | In frame; model & **native res TBD**; plan at **720p** first |
| TV power | **120 V** rear plug |
| HDMI wake from Pi | **Unknown** — test when Pi image ready |
| Raspberry Pi 4B (2018) | On hand; **RAM size TBD** |
| AIY Voice HAT | **Deferred (v2+)**; on hand if you add Google/mirror voice later |
| Voice (v1) | **Echo Dot** → HA only |
| Audio | **Echo + speakers** for v1 voice/music |
| Night mode | **Required** (UI + audio behavior in FSD) |
| **Echo Dot** | **Son’s bedroom**; wake word **“Echo”**; **Alexa Devices** in HA authenticated; **music**, **Pomodoro voice → HA**, **routines → HA** (see [IDEATION_BACKLOG.md](IDEATION_BACKLOG.md)) |
| **Camera** | USB or **Pi Camera v2.1** — presence / gesture ideation only until promoted to FSD |
| **LD4020** | Presence sensor (confirm exact model / HA integration path; often mmWave-class — see ideation doc) |

**Still to fill**

- [ ] Samsung model + **confirmed resolution** (settings menu or label).
- [ ] Pi RAM: run `free -h` or read silkscreen / order records.
- [ ] *(If AIY returns to scope)* revision (v1 vs v2) from GPIO / audio codec / Google kit guide.
- [ ] HA URL (internal) + token storage path on Pi.
- [ ] Wall / outlet / cable concealment notes (if relevant for install doc).

---

## 9. Risks (early)

| Risk | Mitigation |
|------|------------|
| Mirror glass reduces contrast | High-contrast UI theme; limit small text; test fonts on actual glass |
| Voice false triggers | **v1:** Echo-only; use HA + Alexa phrase design; optional mute hours on Echo for bedroom |
| **Child bedroom — privacy & trust** | Camera/gesture **opt-in**; todo/calendar content agreed with family; Pomodoro UI **supportive** language |
| **Dual voice (future)** | If AIY is added later, split **roles** (Echo vs mirror) in FSD to avoid two wake words doing the same job |
| Heat in enclosed frame | Ventilation slots; Pi throttling; thermal test under load |
| **Google / AIY (if reintroduced)** | API churn; pin images — **N/A for v1** |
| TV always-on vs Pi-only | Clarify power workflow; HDMI-CEC or manual TV power if no wake-on-HDMI |

---

## 10. Next steps (planning only)

1. Confirm **display resolution** and **Pi RAM**; update FSD + UX type scale for **59 cm tall** viewable area.
2. Lock **v1 module list** and **night mode** behavior in [FSD.md](FSD.md).
3. UX Designer: layout zones + typography for **32.5×59 cm** at viewing distance.
4. Architect: **v1** Pi display + HA backend + **Echo-only voice** locked in ARCHITECTURE.md; define HA entities for **todo / school calendar / weather** tiles.
5. Keep **GitHub** in sync with local (see [GITHUB.md](GITHUB.md)).
