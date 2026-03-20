# Project brief — Wall Magic Mirror

**Version:** 0.3  
**Last updated:** 2026-03-20

---

## 1. Problem statement

You want a **wall-mounted mirror** that doubles as a **low-distraction information surface** and optionally supports **hands-free control**, using hardware you already favor (Pi 4, AIY Voice HAT, spare HDMI panel) and **deep integration with Home Assistant**.

---

## 2. Goals (measurable when possible)

| ID | Goal | How we’ll know (later) |
|----|------|-------------------------|
| G1 | Readable at ~2–3 m in typical bedroom lighting | Subjective review + contrast checks on mirror glass |
| G2 | Reliable “at a glance” modules (time, weather, HA summary) | Uptime / refresh behavior documented in FSD |
| G3 | Voice triggers common HA actions without pulling out a phone | Test cases in FSD + Tester agent checklist |
| G4 | Maintainable software (updates, backups, secrets) | Runbook in README / ARCHITECTURE |

---

## 3. Scope

### In scope (candidate)

- **Enclosure:** Mirror glass + Samsung TV are **already mounted in a wooden frame** — remaining work is cabling, Pi placement, service access, and any trim tweaks.
- Pi OS image, **Chromium kiosk** hosting a **custom web UI** (not MagicMirror² for v1); auto-start UI + **local backend** for Home Assistant API (**FR-006**).
- HA integration (entities, scenes, possibly calendar via HA).
- Voice: **Google account / cloud** acceptable — AIY Voice HAT + Assistant-style flow (details in architecture phase).
- **Night mode:** calmer UI and restrained audio/TTS for bedroom use.
- Documentation, FSD, version control.

### Out of scope for v1 (unless you promote them)

- Facial recognition, camera inside mirror glass.
- Heavy animations or video wallpaper.
- Replacing HA as source of truth for complex logic.

---

## 4. Constraints & assumptions

- **Mirror glass — viewable area:** **32.5 cm × 59 cm** (two-way glass; thickness TBD if needed for CAD).
- **Display:** Older **Samsung TV** (model number and **native resolution not yet recorded**). **Planning assumption: 1280×720 (720p)** until confirmed; move UI/layout to **1080p** if the panel supports it.
- **Power:** TV has **120 V plug on the back** — separate from Pi power; **HDMI wake behavior unknown** (test: does panel show Pi signal only when TV is “on”?).
- **Compute:** **Raspberry Pi 4 Model B (2018)** — onboard RAM size TBD (`free -h` on device).
- **Voice HAT:** Google **AIY Voice Kit** HAT (revision **not marked** on board — identify from photos / pinout vs Google docs when flashing).
- **Audio:** **HAT speaker** available; **optional:** route output to **TV speakers** over HDMI (Architect: default output + switching rules in FSD).
- **Network:** Home LAN + Home Assistant reachable; prefer **no inbound exposure** from the internet to the Pi.

---

## 5. High-level architecture (one paragraph)

The Pi runs **Chromium in kiosk mode** showing a **custom-built web mirror UI**. A **local backend** on the Pi holds the HA token and talks to Home Assistant via **REST/WebSocket**; the browser talks only to loopback (**FR-006**). **Voice** uses the AIY HAT with **Google cloud–backed** recognition/Assistant and maps **whitelisted** intents to HA (often via the same backend). **Cursor + HA MCP** are for **development on your PC only**, not part of the wall-mounted runtime.

See [ARCHITECTURE.md](ARCHITECTURE.md) for diagrams and options.

---

## 6. Stack decisions

| Area | Decision | Notes |
|------|----------|--------|
| **Mirror UI** | **Custom web + local HA backend** | Full control for glass, night mode, FR-006; more code than MagicMirror² |
| **MagicMirror²** | **Deferred for v1** | Can revisit if maintenance cost of custom UI grows |
| Voice | **AIY + Google Assistant / cloud** | Account + cloud dependency *(accepted for v1)* |
| Voice (future) | Wake word + HA Assist | Fewer vendor ties; more integration later |
| Calendar / weather | Prefer **HA entities** | Avoid extra paid APIs |
| Remote admin | SSH over LAN / Tailscale | Keys only, no password SSH |

Reference skills in repo: **`mm-home-assistant`**, **`mm-kiosk-pi`**, **`mm-voice-aiy-google`**, **`mm-dev-mcp-ha`** (MCP dev-only).

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
| AIY Voice HAT | On hand; **revision unmarked** — identify from docs |
| Voice / cloud | **Google account + cloud OK** |
| Audio | HAT speaker **and/or** TV speakers via HDMI — **TBD default** |
| Night mode | **Required** (UI + audio behavior in FSD) |

**Still to fill**

- [ ] Samsung model + **confirmed resolution** (settings menu or label).
- [ ] Pi RAM: run `free -h` or read silkscreen / order records.
- [ ] AIY revision (v1 vs v2) from GPIO / audio codec / Google kit guide.
- [ ] HA URL (internal) + token storage path on Pi.
- [ ] Wall / outlet / cable concealment notes (if relevant for install doc).

---

## 9. Risks (early)

| Risk | Mitigation |
|------|------------|
| Mirror glass reduces contrast | High-contrast UI theme; limit small text; test fonts on actual glass |
| Voice false triggers in bedroom | Push-to-talk fallback; strict intent whitelist; LED/visual feedback |
| Heat in enclosed frame | Ventilation slots; Pi throttling; thermal test under load |
| AIY / Google API churn | Pin documented image + API versions; evaluate local alternative early |
| TV always-on vs Pi-only | Clarify power workflow; HDMI-CEC or manual TV power if no wake-on-HDMI |

---

## 10. Next steps (planning only)

1. Confirm **display resolution** and **Pi RAM**; update FSD + UX type scale for **59 cm tall** viewable area.
2. Lock **v1 module list** and **night mode** behavior in [FSD.md](FSD.md).
3. UX Designer: layout zones + typography for **32.5×59 cm** at viewing distance.
4. Architect: **custom web + backend** locked; next — **audio routing** (HAT vs HDMI) and voice stack details in ARCHITECTURE.md.
5. Keep **GitHub** in sync with local (see [GITHUB.md](GITHUB.md)).
