# Design readiness — before visual theme work

Use this as a **gate** so theme and layout work with the **UX Designer** agent (or `mm-ux-designer` skill) stays aligned with glass, bedroom context, and FSD — **before** any application code.

---

## What you already have (good foundation)

| Asset | Location |
|-------|----------|
| Module list (clock, weather, todo, calendar, Pomodoro, …) | [FSD.md](FSD.md) §7 |
| **UI modes & dual distance** | [UI_MODES.md](UI_MODES.md) |
| Constraints (glass **32.5×59 cm**, **1080×1920 portrait** viewport, night mode, child bedroom) | [PROJECT_BRIEF.md](PROJECT_BRIEF.md), [MIRROR_CONTEXT.md](MIRROR_CONTEXT.md) |
| UX rules (contrast, night mode, Pomodoro tone) | [agents/ux-designer.md](../agents/ux-designer.md) |
| Canvas target for mockups | **1080×1920** (portrait FHD) — confirm with [PI_BRINGUP.md](PI_BRINGUP.md) stub on device |

---

## Checklist — complete (or consciously waive) before theme design

### A. Physical / viewing (drives type size and layout)

- [x] **Viewing distances locked:** **~10 ft** (bed/desk) **and** **~2–3 ft** (at mirror); **far** sets minimum readable type for clock / today’s weather / Pomodoro — [UI_MODES.md](UI_MODES.md).
- [ ] **Photo** of the mirror area in **day** and **dim** light (optional but helps reflection/contrast judgment).
- [x] **Effective resolution** — **1920×1080** panel, **portrait** → design at **1080×1920** unless stub shows otherwise.

### B. Content & priority (drives hierarchy on screen)

- [x] **Mode-driven hierarchy:** **sleep_off**, **passive**, **active_engaged**, **pomodoro_focus** — [UI_MODES.md](UI_MODES.md), **FR-010** / **M-007** in [FSD.md](FSD.md). UX should produce **per-mode** or **annotated** layouts where hierarchy differs materially.
- [ ] **Passive “hero”** emphasis with family (e.g. clock + **today** weather vs clock + next calendar — still fine-tune within passive mode).
- [ ] **School calendar:** which HA `calendar` entity name(s) will feed **M-005** (can be “TBD” in design if you use placeholder labels in mockups).
- [ ] **Todo source:** e.g. HA `todo`, `shopping_list`, or helpers — **pattern** agreed with Architect (placeholders OK for SVG).
- [x] **Weather:** **Today** primary; **next few days** smaller secondary — locked in [UI_MODES.md](UI_MODES.md) / **FR-009**.

### C. Household / brand (drives color and tone)

- [ ] **Night mode:** time window or “manual only” for v1 (affects how dark the default theme can be).
- [ ] Any **hard nos** (e.g. no red except alarms, no gamification, favorite accent color).
- [ ] **Son’s input** (even rough): colors he likes / dislikes, or “keep it minimal.”

### D. Agent session setup (Cursor)

- [ ] Open **`magic-mirror`** as **workspace root** (so `.cursor/skills/` apply).
- [ ] In chat, **@** reference: `agents/ux-designer.md`, `docs/FSD.md` §7, `docs/PROJECT_BRIEF.md`, `docs/MIRROR_CONTEXT.md`.
- [ ] Optional: enable **`mm-ux-designer`** skill and **`mm-mirror-context`** for the session.

---

## Expected outputs from the UX agent (commit to repo)

Place artifacts under **`docs/design/`** (created for this purpose):

| Deliverable | Purpose |
|-------------|---------|
| **`tokens.md`** | Semantic colors, type scale (min sizes), spacing rhythm, night-mode deltas |
| **`layout-1080x1920.svg`** (or `.md` embedding SVG) | Portrait wireframe with **realistic** sample data (time, timer, tasks, weather snippet) |
| **`module-priority.md`** | Ordered list: what draws the eye first → second → third |

Naming is flexible; keep everything **versioned in git** so Coder agent can implement against it later.

---

## Smooth development — beyond the theme

These support **implementation** after design; start some in parallel if you want.

| Need | Why |
|------|-----|
| **HA reachable from dev machine** | `mm-dev-mcp-ha` / MCP against HA Pi 5 — [HA_DEV.md](HA_DEV.md) |
| **Long-lived tokens** (mirror Pi + optional dev/MCP) | Stored **only** on device / local MCP config — never in repo; `.env.example` lists key names only |
| **Branch habit** | `feature/ui-theme`, `feature/backend-proxy` — see [GITHUB.md](GITHUB.md) |
| **Pi imaged when ready** | Raspberry Pi Imager, SSH on, hostname known — not required **before** SVG/theme work |
| **Tester mindset** | When code starts, cases link to **FR** IDs (see [agents/tester.md](../agents/tester.md)) |

---

## Suggested order (Planner-aligned)

1. **Fill checklist A–C** (can be quick family decisions + one photo).  
2. **UX Designer agent** → `docs/design/*` deliverables.  
3. **Architect** → confirm HA entity strategy matches module layout; update [ARCHITECTURE.md](ARCHITECTURE.md) with entity **templates**.  
4. **Coder** → only after FSD + design tokens are stable enough to avoid thrash.

---

## Waiving items

If something is unknown (e.g. exact `calendar.entity_id`), note **“placeholder in design; entity TBD”** in `docs/design/module-priority.md` and proceed — **viewing distances** and **weather hierarchy** are now locked in [UI_MODES.md](UI_MODES.md); refine **passive-mode hero** emphasis with the family if needed.
