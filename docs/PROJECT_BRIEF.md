# Project brief — Wall Magic Mirror

**Version:** 0.1 (draft)  
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

- Enclosure / mounting (wood + optional 3D-printed bezels or standoffs).
- Pi OS image, kiosk display, auto-start UI.
- HA integration (entities, scenes, possibly calendar via HA).
- Voice pipeline: wake / intent / action (exact stack TBD — AIY + cloud vs local).
- Documentation, FSD, version control.

### Out of scope for v1 (unless you promote them)

- Facial recognition, camera inside mirror glass.
- Heavy animations or video wallpaper.
- Replacing HA as source of truth for complex logic.

---

## 4. Constraints & assumptions

- **Display:** Existing HDMI TV/monitor behind one-way / mirror glass — bezel and viewing angles drive enclosure design.
- **Compute:** Raspberry Pi 4 (assumed adequate for kiosk + light voice).
- **Audio:** AIY Voice HAT — verify microphone array and speaker impedance match your mirror cavity (acoustic reflections matter).
- **Network:** Home LAN + Home Assistant reachable; prefer **no inbound exposure** from the internet to the Pi.

---

## 5. High-level architecture (one paragraph)

The Pi renders a **full-screen web UI** (or equivalent) on the HDMI display. A **local service** subscribes to Home Assistant (WebSocket/REST) for entity state and optional actions. **Voice** captures audio via the HAT, runs wake word / STT / intent routing, and maps allowed phrases to HA service calls. **Cursor MCP** supports developers working on automations and docs, not the mirror runtime unless explicitly added later.

See [ARCHITECTURE.md](ARCHITECTURE.md) for diagrams and options.

---

## 6. Frugal stack — options to compare (no decision lock yet)

| Area | Low-cost / free-leaning | Tradeoff |
|------|-------------------------|----------|
| Mirror UI | Static or light SPA + HA data | You build/maintain more vs off-the-shelf mirror framework |
| Voice | AIY + Google Assistant path | Account + cloud dependency |
| Voice (alt.) | Wake word on Pi + HA “Assist” / conversation | More integration work, fewer vendor ties |
| Calendar | HA + local CalDAV / family shared calendar | Privacy-friendly; setup complexity |
| Remote admin | SSH over LAN / Tailscale (if you already use it) | Policy: keys only, no password SSH |

---

## 7. Home Assistant & MCP

- **Runtime:** Mirror should use HA **REST + WebSocket** with a **long-lived token** stored in a root-only file or OS secret mechanism — **never** in git.
- **MCP:** Use during development to inspect entities, test services, and pull docs into `resources/reference/`. Document any “dev-only” workflows in [GITHUB.md](GITHUB.md) or a future `docs/DEV_ENV.md`.

---

## 8. Inventory & decisions checklist *(please fill in)*

**Already purchased / on hand**

- [ ] Two-way mirror glass (size / thickness):
- [ ] HDMI display model & resolution:
- [ ] Raspberry Pi 4 RAM size:
- [ ] AIY Voice Kit version (v1 / v2) & HAT fits Pi 4 case?
- [ ] PSU for Pi (official / other) and cable routing plan:
- [ ] Speakers: HAT only vs external?

**Home Assistant**

- [ ] HA URL (internal):
- [ ] Token storage approach agreed (file path, permissions):

**Room & install**

- [ ] Wall structure (stud spacing):
- [ ] Power outlet location vs cable concealment:

---

## 9. Risks (early)

| Risk | Mitigation |
|------|------------|
| Mirror glass reduces contrast | High-contrast UI theme; limit small text; test fonts on actual glass |
| Voice false triggers in bedroom | Push-to-talk fallback; strict intent whitelist; LED/visual feedback |
| Heat in enclosed frame | Ventilation slots; Pi throttling; thermal test under load |
| AIY / Google API churn | Pin documented image + API versions; evaluate local alternative early |

---

## 10. Next steps (planning only)

1. Complete §8 checklist.
2. Lock **v1 module list** in [FSD.md](FSD.md).
3. UX Designer agent: layout zones + typography scale for mirror viewing distance.
4. Architect agent: choose UI framework path + voice path; update ARCHITECTURE.md.
5. Initialize git remote (see [GITHUB.md](GITHUB.md)) and first tagged “docs-only” release.
