# Pomodoro focus UI — planner handoff

**Goal:** A **focused** Pomodoro experience on the mirror: either a **dedicated view** (route/screen) or a **full-viewport overlay** with a **dark shim** behind the timer so the passive dashboard does not compete visually.

**Existing requirements (do not duplicate — refine in FSD if needed):**

| ID | Summary |
|----|---------|
| **FR-008** | Large countdown + phase when HA reports active focus/break; in `pomodoro_focus`, timer dominates ([FSD.md](FSD.md), [UI_MODES.md](UI_MODES.md)) |
| **FR-010** | Mode-driven UI; `pomodoro_focus` among **sleep_off** / **passive** / **active_engaged** / **pomodoro_focus** |
| **UC-6** | Echo → HA for start/pause/skip; mirror shows live countdown + phase |
| **M-004** | Milestone: HA `timer` / `input_select` / scripts (TBD) + UX |

**Design artifacts already in repo (UX reference):**

- [design/layout-1080x1920-pomodoro.svg](design/layout-1080x1920-pomodoro.svg)
- [design/exploration-pomodoro-stark.svg](design/exploration-pomodoro-stark.svg)

---

## Decision fork (Planner → UX → Architect)

| Option | Pros | Cons |
|--------|------|------|
| **A. Overlay + dark shim** | Stays on one URL; quick enter/exit; matches “mode” mental model | z-index, focus trap, ensuring FR-007 night mode still reads well |
| **B. Separate screen / route** | Clear separation; easy to exclude from “passive” layout logic | Navigation contract (how user “leaves” without Echo); two layouts to maintain |
| **C. Hybrid** | Overlay for entry; optional deep link for bookmark/debug | Most moving parts |

**Recommendation for Planner to lock in Phase 3 gate:** Pick **A or B** before Coder slice; default candidate is **A** if `pomodoro_focus` is already the intended HA-driven mode (FR-010).

---

## Planner task list (suggested)

1. **Confirm HA contract** (Architect handoff): which entities expose phase, remaining time, pause state — align with [IDEATION_BACKLOG.md](IDEATION_BACKLOG.md) Pomodoro notes if still accurate.
2. **Snapshot vs client timer:** FSD currently implies HA as source of truth; decide whether mirror polls `/api/snapshot` extensions, a small `/api/pomodoro` read, or subscribes via future WebSocket — document in [ARCHITECTURE.md](ARCHITECTURE.md).
3. **UX:** Tokens for shim opacity, typography scale for FR-005 at 10 ft; reduced motion preference if any animation on enter/exit.
4. **Tester:** Given Echo → HA, cases for “timer started,” “break begins,” “idle / no timer,” HA unreachable.

---

## Open questions (one pass with user)

- Should the dark shim be **solid** or **blur** (performance on Pi GPU)?
- **Echo-only** control v1 — confirm no on-glass tap targets required for MVP.
- **FR-007:** Does Pomodoro view use the same night dimming as passive, or a fixed high-contrast palette?

---

*Created 2026-03-20 — use with **Planner** agent (`agents/planner.md`) and `mm-planner` skill.*
