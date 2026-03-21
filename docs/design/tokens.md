# Design tokens — Magic Mirror (1080×1920 portrait)

**Canvas:** logical viewport **1080×1920** (portrait), Chromium kiosk on mirror Pi.  
**Glass:** treat as **lower effective contrast** than a raw monitor; prefer **weight + size** over thin strokes and gray-on-gray.

**Visual direction:** **dark base**, **high contrast** primary copy, **minimal chrome** — no heavy borders, decorative panels, or skeuomorphic cards. Use **type hierarchy**, **spacing**, and **opacity** to separate regions. Reserve strong hue for **voice state** and **real alerts** only.

---

## Color (semantic)

| Token | Role | Example | Notes |
|-------|------|---------|--------|
| `--mm-bg` | Page background | `#0f0f10` | Near-black; slight lift from pure `#000` to reduce OLED smear and harsh reflections |
| `--mm-bg-elevated` | Scrolling / rare overlays only | `#161618` | Use sparingly; prefer whitespace (negative space) over new surfaces |
| `--mm-text-primary` | Time, temps, timer digits, key values | `#f2f2f4` | Slight off-white; softer than pure white at night |
| `--mm-text-secondary` | Day/date, labels, hints | `#a8a8b0` | Must stay **≥ ~3:1** vs `--mm-bg` for large type after glass loss (floor, not target) |
| `--mm-text-muted` | Tertiary / “nice to have” | `#6e6e78` | **Near / 2–3 ft only** — not for clock, today weather headline, or Pomodoro |
| `--mm-accent` | Non-alarm emphasis (e.g. phase label) | `#7eb8ff` | Cool, calm; **decorative use discouraged** — mostly for small highlights |
| `--mm-voice-listening` | “Echo / HA is doing something” | `#9ad8ff` | Distinct from danger; pair with **on-screen** copy (FR-004 / UX principles) |
| `--mm-success` | Confirmed action (subtle) | `#8fd4a8` | Low chroma; avoid celebratory gamification |
| `--mm-danger` | Real problem only (HA down, stale critical) | `#ff6b5c` | **Not** for Pomodoro “break” or weather heat — alarm / error semantics only |

**Night mode (FR-007) — deltas:** reduce **peak luminance**, not legibility of Must-tier content.

| Token | Day (default) | Night |
|-------|----------------|-------|
| `--mm-bg` | `#0f0f10` | `#0a0a0c` (or same with global dim via compositor if used) |
| `--mm-text-primary` | `#f2f2f4` | `#d8d8dc` (~8–12% lower luminance) |
| `--mm-text-secondary` | `#a8a8b0` | `#94949c` |
| `--mm-accent` / `--mm-voice-listening` | saturated as above | **−15–25% luminance** or slightly desaturate |

**Forbidden patterns:** full-screen **white** flashes; **red/orange/yellow** as decoration; thin **1px hairlines** for critical data.

### Optional palette — dashboard inspiration

Reference: [reference/ui-inspiration-dashboard-dark.png](reference/ui-inspiration-dashboard-dark.png) · Adaptation rules: [inspiration-dashboard-ui.md](inspiration-dashboard-ui.md). Use **sparingly** with existing “minimal chrome” direction — mirror is not a dense widget board.

| Token | Role | Example | Notes |
|-------|------|---------|--------|
| `--mm-accent-teal` | Primary accent (highlights, phase, links, “today” marker) | `#2dd4bf` | Calm teal; **validate on glass** at 10 ft; soften for night mode |
| `--mm-surface-soft` | Optional single module backdrop | `#141418` at **90–95%** opacity or solid `#16161c` | Prefer **one** soft surface per screen, not a card grid |
| `--mm-radius-pill` | Pills (status, exit affordances) | `9999px` or `height / 2` | Pair with **≥48px** touch height where tapped |
| `--mm-radius-md` | Rare rounded container | `12px`–`16px` | **Not** 24px+ stacks — keeps mirror calm |
| `--mm-shadow-soft` | Optional depth | `0 8px 32px rgba(0,0,0,0.35)` | **Low** on mirror; glass flattens — often **skip** shadow |

**Warm accent from the reference (gold/amber):** do **not** use for decoration. If a metric truly needs warmth, pick a **muted** amber and keep it **secondary** to teal — never confuse with **`--mm-danger`**.

---

## Typography

**Families (implementation suggestion):** one **neo-grotesque or humanist sans** system stack (e.g. `system-ui` with a single webfont later if needed). **Tabular figures** for clock and Pomodoro.

### Minimum sizes — **~10 ft (~3 m)** (“far” — FR-005)

These are **minimum** `font-size` values (CSS px at 1:1 viewport) for **glance** reading on glass. Validate in room; bump if reflection wins.

| Content | Min size | Weight | Rationale |
|---------|----------|--------|-----------|
| **Clock — time numerals** | **112 px** | Semibold (600) or bold (700) | Largest recurring passive anchor; ~1.3–1.5 cm equivalent on 59 cm-tall glass at 1080×1920 |
| **Today’s weather — primary value** (e.g. `72°`) | **72 px** | Semibold | Value-before-label; pair with condition line below |
| **Today’s weather — condition** (short phrase, e.g. `Partly cloudy`) | **40 px** | Medium (500) | Single line preferred; wrap only at near distance if needed |
| **Pomodoro — countdown digits** | **128 px** | Bold (700) | Must dominate in `pomodoro_focus`; slightly larger than clock OK |
| **Pomodoro — phase label** (`Focus` / `Short break`) | **36 px** | Medium | Supportive, not loud (child bedroom) |

**Rule of thumb used:** signage-style **~1 in equivalent letter height at ~10 ft** mapped to this panel (~37 mm tall ≈ **110–120 px** tall glyphs for the clock — we standardize on **112 px** minimum with bold weight).

### Sizes — **~2–3 ft** (“near”)

| Role | Typical range | Notes |
|------|----------------|-------|
| Multi-day forecast row | 26–30 px | Compact strip (**5 days** in [web/](../../web/) prototype; 3–5 per product) |
| Calendar lines (`calendar.school` placeholder) | 28–34 px | 2–4 events visible passive |
| Todo lines (`todo.kid_chores` placeholder) | 28–34 px | No checkbox chrome required — **leading** + indent |
| Voice / error one-liner | 30–36 px | Must read without audio |

### Line height & tracking

- **Display sizes (≥72 px):** `line-height` **1.05–1.1**; **slight** negative letter-spacing only if font looks loose.
- **Body / lists (26–36 px):** `line-height` **1.35–1.45**.

---

## Spacing rhythm

**Base unit:** **8 px** (all spacing multiples of 4; prefer 8).

| Token | Value | Use |
|-------|-------|-----|
| `--mm-space-xs` | 8 px | Tight stack (label to value) |
| `--mm-space-sm` | 16 px | Related lines in a module |
| `--mm-space-md` | 24 px | Between modules in a column |
| `--mm-space-lg` | 40 px | Section breaks (clock block → weather) |
| `--mm-space-xl` | 64 px | Major vertical rhythm (top breathing room) |

**Safe area:** inset content **≥ 40 px** from top/sides; **≥ 48 px** bottom (bezel / chin unknown).

**Mechanical frame (measured on device):** the wood bezel can cover **~20–30 px** of the active LCD along edges. For **touch** or on-screen controls, add that overlap to the inset (e.g. **≥ 64–72 px** from each edge) so controls stay in the visible region. Re-measure after final frame install; the design preview dock uses **`--preview-frame-inset: 36px`** as a middle value — bump in `preview-dock.css` if your frame is thicker.

---

## Motion

- Prefer **instant** or **≤ 200 ms** opacity / layout cross-fades on mode change.
- **No** looping ambient animation in peripheral vision (bedroom).

---

## Touch (future)

If on-glass touch is added: minimum target **48×48 px**; keep primary actions away from extreme corners.

---

## Traceability

- **FR-005** / **NFR-005:** far + near readability; min sizes above.
- **FR-007:** night mode deltas.
- **FR-008 / UI_MODES:** Pomodoro scale in `pomodoro_focus`.
- **UI_MODES.md:** weather today vs forecast hierarchy.
