# Design artifacts

Store **visual theme** and **layout** outputs from the UX Designer agent here before implementation.

Suggested files (see [../DESIGN_READINESS.md](../DESIGN_READINESS.md)); **modes** in [../UI_MODES.md](../UI_MODES.md):

- [`tokens.md`](tokens.md) — color, type, spacing, night mode; **minimum sizes for ~10 ft** vs **~2–3 ft**
- [`layout-1080x1920.md`](layout-1080x1920.md) — overview + **passive** / **pomodoro_focus** wireframes  
  - [`layout-1080x1920-passive.svg`](layout-1080x1920-passive.svg)  
  - [`layout-1080x1920-pomodoro.svg`](layout-1080x1920-pomodoro.svg)
- [`module-priority.md`](module-priority.md) — visual hierarchy **per mode** (`sleep_off`, `passive`, `active_engaged`, `pomodoro_focus`)
- [`explorations.md`](explorations.md) — **minimal / modern** directions + SVGs (`exploration-*.svg`)
- [`inspiration-dashboard-ui.md`](inspiration-dashboard-ui.md) — dark **dashboard / teal** UI mood from [reference/ui-inspiration-dashboard-dark.png](reference/ui-inspiration-dashboard-dark.png); maps to tokens + mirror constraints
- [`preview/`](preview/) — gallery + SVG viewer; **kiosk by default** on Pi (`--open`), bottom **Exit kiosk…** help + frame-safe dock ([`preview/README.md`](preview/README.md)); [`../../scripts/sync-design-preview-to-pi.sh`](../../scripts/sync-design-preview-to-pi.sh)
- **[`../../web/`](../../web/)** — **implemented passive UI** (clock, weather + 5-day icons, calendar, todo) styled with tokens + dashboard inspiration ([`web/README.md`](../../web/README.md))

Do **not** commit secrets, internal HA URLs with tokens, or photos that identify the child if you prefer privacy — use crops or synthetic room shots if needed.
