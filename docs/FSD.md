# Functional Specification Document (FSD)

**Project:** Wall Magic Mirror (Pi 4 + AIY Voice Hat + Home Assistant)  
**Document type:** Living specification — update on every scope or behavior change.  
**Version:** 0.2  
**Last updated:** 2026-03-20

---

## Document control

| Version | Date | Author | Summary of change |
|---------|------|--------|-------------------|
| 0.1 | 2026-03-20 | — | Initial skeleton + placeholder requirements |
| 0.2 | 2026-03-20 | — | Hardware inventory; night mode FR; 720p planning assumption |

---

## 1. Purpose & scope

**Purpose:** Define *what* the system must do for users and *how* success is verified — without prescribing final implementation.

**Scope:** See [PROJECT_BRIEF.md](PROJECT_BRIEF.md). This FSD tracks **functional** and **non-functional** requirements and traceability to tests.

---

## 2. Definitions

| Term | Definition |
|------|------------|
| **Module** | A UI region showing one concern (e.g. clock, weather summary). |
| **Intent** | A voice-mapped action resolved to a Home Assistant service call. |
| **Kiosk mode** | Full-screen display with no casual OS chrome visible. |

---

## 3. Personas & primary use cases

| Persona | Goal |
|---------|------|
| **Occupant** | Glance at time, weather, and home state; optionally speak a short command. |

**Use cases (draft — expand with IDs):**

- UC-1: View current local time and date.
- UC-2: View weather summary (source via HA or approved API — TBD).
- UC-3: View selected HA entity states (list TBD).
- UC-4: Invoke HA scene or device action by voice (whitelist TBD).
- UC-5: Recover from network loss without manual reboot (behavior TBD).

---

## 4. Functional requirements

| ID | Requirement | Priority (MoSCoW) | Notes / source |
|----|-------------|-------------------|----------------|
| FR-001 | System shall show a full-screen mirror UI after boot without manual login | Must | Kiosk autostart |
| FR-002 | System shall display accurate local time | Must | NTP |
| FR-003 | System shall reflect HA entity updates within **TBD** seconds | Must | WebSocket preferred |
| FR-004 | User shall trigger **TBD** HA actions by voice | Should | Map to HA services |
| FR-005 | UI shall remain readable on mirror glass at **TBD** m viewing distance | Must | UX sign-off |
| FR-006 | System shall not expose HA token in client-side bundle | Must | Server-side proxy or equivalent |
| FR-007 | System shall provide **night mode** (reduced brightness/contrast of UI and restrained audio/TTS) | Must | SCHEDULE or manual toggle TBD; see PROJECT_BRIEF |

**Display planning assumption:** Design layouts for **1280×720** until Samsung TV **native resolution** is confirmed; scale to **1080p** if supported (viewable glass **32.5 cm × 59 cm**).

*Add rows as modules and voice intents are decided.*

---

## 5. Non-functional requirements

| ID | Requirement | Target | Verification |
|----|-------------|--------|--------------|
| NFR-001 | Availability (mirror UI) | **TBD** % monthly | Logs / HA ping |
| NFR-002 | Power loss recovery | Auto-boot to UI | Tester checklist |
| NFR-003 | Thermal stability | No sustained throttle under kiosk+voice idle | `vcgencmd` / stress notes |
| NFR-004 | Security | No secrets in repo; least-privilege HA token | Grep + HA audit |

---

## 6. Voice (functional subset)

| Intent ID | Example utterance | HA action | Enabled (Y/N) |
|-----------|-------------------|-----------|---------------|
| VI-001 | *TBD* | *TBD* | |

*Security rule:* only whitelisted intents; reject unknown commands with harmless feedback.

---

## 7. UI modules (inventory)

| Module ID | Content | Data source | Owner (agent) |
|-----------|---------|-------------|---------------|
| M-001 | Clock | System / HA | UX |
| M-002 | Weather | HA entity / API | Architect |
| M-003 | HA summary | HA | Architect |

---

## 8. Out of scope (reference)

Duplicated from brief; keep in sync with [PROJECT_BRIEF.md](PROJECT_BRIEF.md).

---

## 9. Acceptance criteria template

For each FR/UC, add:

- **Given** … **When** … **Then** …
- Link to Tester agent case ID when implemented.

---

## 10. Change log (running)

- **0.1** — Skeleton created; requirements to be refined after inventory and UX pass.
- **0.2** — Inventory filled (glass, TV, Pi, AIY, Google cloud, audio options); FR-007 night mode; 720p baseline.
