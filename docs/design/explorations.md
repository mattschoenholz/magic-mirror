# Visual explorations — minimal, modern

**Goal:** Stretch the **baseline** ([tokens.md](tokens.md), [layout-1080x1920.md](layout-1080x1920.md)) toward a **calm, contemporary** feel without adding panels, borders, or decorative chrome. These are **options**, not replacements — pick one direction (or mix traits) before implementation.

**Constraints carried forward:** dark field, **high contrast** for Must-tier content at **~10 ft**, **FR-007** night discipline, no alarm colors as decoration.

---

## Shared “modern minimal” traits

| Trait | What it does on glass |
|--------|------------------------|
| **Negative space as structure** | Large gaps between modules replace boxes; easier to parse with peripheral vision. |
| **Typographic voice** | Tracking, caps for micro-labels, **tabular figures** — reads “designed” without new components. |
| **Restrained palette** | One cool neutral background family; **at most one** non-neutral accent (e.g. phase or listening state). |
| **Duotone within primary** | Muted colon or AM/PM in the clock keeps one hero line from feeling flat **without** extra UI. |

---

## Direction A — Editorial rail (left-aligned)

**Feel:** Magazine column, **intentional asymmetry**; good if the mirror sits off-center in the room or you want a calmer left-to-right read.

**Traits:** Start at **x = 72–80**; micro-labels in **small caps + letter-spacing**; lists align with the clock’s left edge.

**SVG:** [exploration-passive-editorial.svg](exploration-passive-editorial.svg)

---

## Direction B — Airy center (breathing room)

**Feel:** Same centered axis as the baseline, but **more vertical air** between clock, weather, and lists; background **slightly cooler** (`#0a0b0f`) for a crisp, “2020s product” mood.

**Traits:** Section gaps **~96–112 px**; secondary copy stays in [tokens](tokens.md) muted roles for far/near rules.

**SVG:** [exploration-passive-airy.svg](exploration-passive-airy.svg)

---

## Direction C — Swiss / numeric compact

**Feel:** **Date as a compact badge line** above the time (`FRI / MAR 20`); time uses **duotone** (digits bright, separators softer). Weather sits in a **tighter block** under a single “TODAY” micro-label.

**Traits:** Feels **dense-modern**, not cluttered — still respects **minimum** sizes for clock numerals, temp, and condition on the hero lines.

**SVG:** [exploration-passive-swiss.svg](exploration-passive-swiss.svg)

---

## Direction D — Pomodoro stark (focus)

**Feel:** **Almost monochrome** — phase as **uppercase tracked** neutral; countdown is the only “bright” element; **no blue accent** (reserve hue for voice / errors if you adopt this route).

**Traits:** Supportive copy stays small; hints at bottom. Pairs with **night mode** well (lower chroma overall).

**SVG:** [exploration-pomodoro-stark.svg](exploration-pomodoro-stark.svg)

---

## Optional token tweaks (per direction)

Only use if you commit to a direction; keep [tokens.md](tokens.md) as default until then.

| Token | Baseline | Editorial / Airy | Swiss | Pomodoro stark |
|-------|----------|------------------|-------|----------------|
| `--mm-bg` | `#0f0f10` | `#0a0b0f` (airy) or keep | keep | `#0c0c0d` |
| `--mm-text-primary` | `#f2f2f4` | same | same | `#ececee` on digits |
| Micro-label | secondary | `#7a7a85` at **24–26 px** + `letter-spacing: 0.14em` | same | uppercase phase `#8f8f98` |
| Pomodoro accent | `#7eb8ff` phase | keep or neutral | keep or neutral | **omit**; phase = secondary neutral |

---

## Recommendation (UX)

- **Default passive:** **B (airy center)** is the smallest jump from the approved baseline and stays **symmetric** for a centered mirror.
- **If the install feels “static”:** add **C’s** duotone colon / date line only — low implementation cost, clearly modern.
- **Pomodoro:** Try **D** in room at night; if it feels too cold, revert phase to **`--mm-accent`** from tokens.

---

## Files in this exploration set

| File | Mode |
|------|------|
| [exploration-passive-editorial.svg](exploration-passive-editorial.svg) | passive |
| [exploration-passive-airy.svg](exploration-passive-airy.svg) | passive |
| [exploration-passive-swiss.svg](exploration-passive-swiss.svg) | passive |
| [exploration-pomodoro-stark.svg](exploration-pomodoro-stark.svg) | pomodoro_focus |

Baseline references: [layout-1080x1920-passive.svg](layout-1080x1920-passive.svg), [layout-1080x1920-pomodoro.svg](layout-1080x1920-pomodoro.svg).

**Preview in browser / on the Pi:** [preview/index.html](preview/index.html) — see [preview/README.md](preview/README.md).

**Teal / “dashboard” mood (sparingly):** [inspiration-dashboard-ui.md](inspiration-dashboard-ui.md) + optional tokens in [tokens.md](tokens.md) — next exploration SVG could swap `--mm-accent` for **`--mm-accent-teal`** on phase / highlights only.
