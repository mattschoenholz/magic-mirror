# UI inspiration — dark dashboard (mirror adaptation)

**Reference image:** [reference/ui-inspiration-dashboard-dark.png](reference/ui-inspiration-dashboard-dark.png) (saved in-repo for offline use).

**Source mood:** deep charcoal canvas, **teal / cyan** data highlights, soft **rounded cards**, **pill** status chips, light typography hierarchy on black — reads as modern “glass” dashboard without browser chrome.

---

## What to carry into Magic Mirror

| From the reference | Mirror adaptation |
|--------------------|-------------------|
| **Near-black field** | Matches **`--mm-bg`**; keeps pixels visually “quiet” behind glass. |
| **Teal / cyan accents** | Use as **primary accent** for phase labels, links, small highlights, optional chart/forecast line — see optional tokens in [tokens.md](tokens.md). Stay **cool and desaturated** enough for a bedroom (not neon club). |
| **White / gray type ladder** | Same as existing **primary → secondary → muted**; bold **tabular** numbers for clock / temp / timer. |
| **Pill shapes** | **Status** (e.g. voice listening, HA stale), **preview “Exit kiosk…”**, Pomodoro phase — `border-radius: 9999px` or `height/2`, **min height 48px** for touch. |
| **Soft corners** | **12–16px** radius on **at most one** optional “surface” per screen if needed; avoid a wall of stacked cards (mirror is **glance**, not dense dashboard). |
| **Generous inner padding** | Aligns with **frame overlap** (~20–30px wood) + [tokens](tokens.md) safe area — treat padding like the reference cards’ gutters. |
| **Subtle depth** | **Very** soft shadow or 1-step **elevated** surface (`--mm-bg-elevated`); heavy blur + glass behind **large** body text **hurts mirror contrast** — prefer solid or near-solid surfaces for readable blocks. |

---

## What *not* to copy literally

- **Crypto / multi-widget grids** — wrong information architecture; passive mode stays **clock → weather → calendar/todo** hierarchy ([UI_MODES.md](../UI_MODES.md)).
- **Sparklines everywhere** — optional **one** compact forecast or trend line; no chart clutter at **~10 ft**.
- **Gold / purple as decoration** — keep palette **teal + neutrals**; warm hue only for **semantic** data if ever needed, never “alarm” tones ([agents/ux-designer.md](../../agents/ux-designer.md)).
- **Heavy glassmorphism** (big blur under small text) — **reflection + blur** = mush; reserve soft effects for **large** display type or decorative **non-critical** regions only.

---

## Component mapping (v1 targets)

| Mirror module | Inspiration cue |
|---------------|-----------------|
| **Clock** | Large numeric type like the reference’s KPI figures; optional **teal** dot or underline — not a full card frame. |
| **Weather today** | Big value + short line; teal could tint **iconography** or **trend** micro-line only. |
| **Calendar snippet** | **Calendar tile** in reference → **2–4 lines**, current day suggested with **teal circle or pill** (same language as “17” highlight). |
| **Todo** | **List rows** + **pill** for “due” or category — not avatars/roles. |
| **Pomodoro** | **Circular progress** in reference → optional **thin ring** around digits; keep **supportive** copy ([FR-008](../FSD.md)). |
| **Preview / kiosk dock** | **Pending**-style **pill** for secondary actions; bottom bar already inset for **wood frame** ([preview/preview-dock.css](preview/preview-dock.css)). |

---

## Traceability

- **FR-005** / glass readability — test teal accents **in room**; dial back saturation if glare wins.
- **FR-007** — night mode lowers luminance on accent teal too.
- **Child bedroom** — dashboard energy stays **calm**; no competitive / streak UI.

---

## Files to update when implementing

- [tokens.md](tokens.md) — optional inspiration tokens (accent teal, radii, pill).
- [explorations.md](explorations.md) — SVG explorations can pick up teal + pill language in a **passive** wireframe variant when Coder is ready.
- **[web/](../web/)** — **first implementation:** passive HTML/CSS/JS shell using teal icons, soft modules, calendar/todo patterns ([web/README.md](../web/README.md)).
