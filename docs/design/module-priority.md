# Module priority — by UI mode

**Modes:** `sleep_off`, `passive`, `active_engaged`, `pomodoro_focus` ([UI_MODES.md](../UI_MODES.md), **FR-010** / **M-007**).  
Order below is **visual hierarchy**: what should read **first → second → third** at a glance. Modules align with [FSD.md](../FSD.md) §7.

**Placeholders (entity TBD per Architect / household):**

| Placeholder label | Module | Typical HA pattern (document in ARCHITECTURE) |
|-------------------|--------|-----------------------------------------------|
| `calendar.school` | M-005 School calendar | `calendar.*` |
| `todo.kid_chores` | M-006 Visual todo | `todo.*`, `shopping_list`, or helpers |

---

## `sleep_off` — sleep / off

**Intent:** Minimal distraction and light; bedroom at rest.

| Priority | Module | Presentation |
|----------|--------|----------------|
| 1 (optional) | M-001 Clock | **Very dim** time-only **or** hidden — exact behavior = FSD acceptance + night helper |
| — | M-002 Weather | Hidden or extremely dim |
| — | M-005 / M-006 | Hidden |
| — | M-004 Pomodoro | Hidden unless household explicitly wants dim hint (default: hidden) |
| — | M-003 Home summary | Hidden |

**Note:** Hierarchy is trivial; **dominance = darkness**. Any visible time must still meet **night** tokens (`tokens.md`), not day contrast targets.

---

## `passive` — default at rest

**Intent:** Ambient answers: *What time is it? What’s the day like? Anything soon?*

| Priority | Module | Notes |
|----------|--------|--------|
| 1 | **M-001 Clock** | Time largest; day/date secondary under or beside (no box) |
| 2 | **M-002 Weather — today** | **Today** headline: temp + short condition (**FR-009** / UI_MODES) |
| 3 | **M-002 Weather — multi-day** | Smaller strip; 3–4 days; muted tertiary |
| 4 | **M-005** `calendar.school` | 2–4 next lines; smaller than weather today |
| 5 | **M-006** `todo.kid_chores` | Compact list or top 3; below calendar or split column — **family preference** can swap 4 vs 5 |
| 6 | **M-003** Home summary | Optional; never louder than clock + today weather |

**Hero fine-tuning:** If family prefers **next event** over **weather** as #2, elevate M-005 and demote M-002 — still within passive; document decision here when locked.

---

## `active_engaged` — voice or HA-driven focus

**Intent:** After Echo → HA or automation, show **contextual** detail; then **auto-revert** to passive (timeout TBD).

| Priority | Module | Notes |
|----------|--------|--------|
| 1 | **Context module** | Whatever triggered engagement: e.g. **M-006** full list + highlight row, or **M-005** jump-to-date range |
| 2 | **M-001 Clock** | Stays visible but **smaller / higher** or corner — not competing with context |
| 3 | **M-002 Weather** | **De-emphasize**: today line only or single line; strip forecast if cramped |
| 4 | Other lists | Non-relevant modules **fade or hide** (same tokens, lower opacity / off-screen) |
| 5 | **M-004 Pomodoro** | If timer running concurrently, **either** small corner **or** elevate to `pomodoro_focus` — product rule TBD |

**Principle:** One **primary story**; no second hero at equal weight.

---

## `pomodoro_focus` — deep focus

**Intent:** Remove competition; **supportive** copy (**FR-008**, child bedroom).

| Priority | Module | Notes |
|----------|--------|--------|
| 1 | **M-004 Pomodoro** | **Largest** digits on screen; phase label (`Focus` / `Short break`); optional soft **voice hints** (“Say …”) — not touch chrome for v1 |
| 2 | **M-001 Clock** | Small, corner or omitted if clutter — **optional** |
| 3 | **M-002 / M-005 / M-006** | Hidden or **very** muted single line max (household policy) — default **hidden** |
| 3 | **M-003** | Hidden |

**Exit:** Timer idle / complete → **passive** (or **active_engaged** if chained — TBD).

---

## Cross-mode summary

| Mode | Dominant module(s) | Typical hidden / dim |
|------|--------------------|----------------------|
| `sleep_off` | None or dim clock | All else |
| `passive` | Clock + today weather | — |
| `active_engaged` | Triggered list/calendar | Weather detail, secondary lists |
| `pomodoro_focus` | Pomodoro | Calendar, todo, forecast |

---

## Implementation note

**M-007** mode shell should drive **visibility + scale** from one layout system ([UI_MODES.md](../UI_MODES.md) — single responsive layout, not four unrelated pages unless Coder/UX later decides otherwise).
