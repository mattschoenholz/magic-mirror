# UI modes — fluid hierarchy and presentation

The mirror UI is **mode-driven**: layout and **information hierarchy** change with mode. Modes should be reflected in **Home Assistant** (e.g. `input_select.mirror_ui_mode` or derived from timer/todo state) so **Echo → HA** and automations can switch the mirror without code deploys — exact entity TBD in [ARCHITECTURE.md](ARCHITECTURE.md).

---

## Viewing distances (UX baseline)

| Context | Approx. distance | Design intent |
|---------|------------------|---------------|
| **Far** | **~10 ft** (~3 m) — in bed or at desk | **Glanceable** type: clock, big Pomodoro digits, today’s weather headline must read without approaching the mirror. |
| **Near** | **~2–3 ft** — standing at mirror | **Detail** OK: secondary forecast strip, more calendar lines, todo checkboxes — still mirror-glass safe contrast. |

Typography and component scale should be validated at **both** distances (Tester checklist).

---

## Mode catalog (v1 target)

### 1. Sleep / off

- **Purpose:** Bedroom at rest; minimal distraction and light emission.
- **Presentation:** Dim/blank screen, clock-off or **very** dim time-only — **exact** behavior in FSD acceptance (tie to night / `sleep` helper).
- **Entry/exit:** HA scene, schedule, Echo routine, or manual — TBD.

### 2. Passive (default “at rest”)

- **Purpose:** General ambient information; no active task focus.
- **Hierarchy (typical):** Time + day/date prominent → **today’s weather** (primary) → small **multi-day** forecast → optional calendar snippet / home summary.
- **Weather:** **Today** is **most important**; **next few days** as **secondary / smaller** (per product direction).

### 3. Active / engaged

- **Purpose:** After **voice-driven** or HA-driven context that needs attention — e.g. **todo** interaction, confirmation, list focus, “what’s next” for school.
- **Hierarchy:** **Contextual** — elevate the module that matches the action (e.g. todo list + highlight completed item, calendar jump). De-emphasize non-relevant tiles **fluidly** (same design system, different weights/layout).
- **Entry:** HA entity change after Echo → HA service (e.g. `script.mirror_show_todos`); **auto-revert** to passive after timeout TBD.

### 4. Pomodoro focus

- **Purpose:** Deep focus; remove competing information.
- **Presentation:** **Large** Pomodoro countdown + phase; **prompts** for pause / resume / new timer (labels or soft buttons if ever touch; v1 is Echo-driven — prompts are **visual hints** for what to say).
- **Entry:** HA reports active Pomodoro / focus timer (**FR-008**).
- **Exit:** Timer idle / complete → return to **passive** (or **active** if chained — TBD).

---

## Implementation notes

- **Single responsive layout** with **CSS/container** or component visibility by mode — avoid four unrelated pages unless UX chooses otherwise.
- **Mode** is the **single source of hierarchy** for which modules are large vs small vs hidden.
- Link to design artifacts: [design/README.md](design/README.md) (`tokens.md`, mockups per mode if UX produces them).
