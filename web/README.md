# Mirror web UI (v1 shell)

**Passive-mode** layout prototype: **12-hour clock**, **Now playing** (art + current track + **Next up**), **weather** (condition + feels / precip + **6-hour today** + colored SVG icons), **calendar** (**today + next 4 days**, today highlighted), **To-Do** (**2×3** grid), **Video radar** (3 recent subscription-style cards with **N hours ago**). Styling follows [docs/design/tokens.md](../docs/design/tokens.md) and the **teal / dark** direction in [docs/design/inspiration-dashboard-ui.md](../docs/design/inspiration-dashboard-ui.md).

**Status:** Static **demo data** only — no HA token in the browser. Production wiring: **local backend** on the Pi (**FR-006**) feeding this UI over same-origin `fetch` or WebSocket.

**Locked runtime contract (no guessing):** [docs/MIRROR_RUNTIME.md](../docs/MIRROR_RUNTIME.md) · example config [config/mirror.runtime.example.yaml](../config/mirror.runtime.example.yaml).

## Run locally (Mac)

### Recommended: backend + UI (live HA / ICS)

From **repo root** (serves `web/` and **`/api/snapshot`**):

```bash
./scripts/run-mirror-backend.sh
```

Open **`http://127.0.0.1:8780/`**. Put your HA token in **`~/.config/mirror/ha_token`** (see [docs/MIRROR_RUNTIME.md](../docs/MIRROR_RUNTIME.md)).

### Static files only (demo data)

```bash
cd web
python3 -m http.server 8765
```

Open **`http://127.0.0.1:8765/`**. The page calls **`/api/snapshot`**; without a backend, it **falls back** to `js/demo-data.js`.

---

## Preview on the mirror Pi **without a keyboard**

Do this from your **Mac** in Terminal (Chromium opens on the Pi’s HDMI display over SSH).

**Use the repo root, not `web/`** — scripts live in **`scripts/`** next to `web/`. If your prompt is `web %`, run `cd ..` first (or use `../scripts/…`). Otherwise zsh reports **no such file or directory**.

**One command** (sync + kiosk):

```bash
cd ~/Desktop/CurrentProjects/General/magic-mirror
./scripts/sync-web-to-pi.sh --open
```

From inside `web/` without changing directories:

```bash
../scripts/sync-web-to-pi.sh --open
```

Design **SVG** gallery (different script): `../scripts/sync-design-preview-to-pi.sh --open` from `web/`, or `cd` to repo root and `./scripts/sync-design-preview-to-pi.sh --open`.

That copies `web/` to **`~/mirror-web/`** on the Pi and opens **`file:///home/pi/mirror-web/index.html`** in Chromium (same flags as the design preview: kiosk, keyring-safe, etc.). **No URL to type on the Pi.**

**If you specifically want `http://127.0.0.1:8765/` on the Pi** (e.g. to match how you test on the Mac): the server must run **on the Pi**. Use:

```bash
cd ~/Desktop/CurrentProjects/General/magic-mirror
./scripts/sync-web-to-pi.sh --open --http
```

That starts **`python3 -m http.server 8765`** in `~/mirror-web` on the Pi (background) and opens Chromium to **`http://127.0.0.1:8765/`**. Logs: **`/tmp/mirror-web-http.log`** on the Pi. Stop the server later:  
`ssh pi@mirror-pi4.local 'pkill -f "python3 -m http.server 8765"'`

**Windowed** (browser chrome / back button):  
`PREVIEW_WINDOWED=1 ./scripts/sync-web-to-pi.sh --open`

**Exit kiosk:** from the Mac, `ssh pi@mirror-pi4.local 'pkill -f chromium || pkill -f chromium-browser'`, or plug in a keyboard briefly (**Alt+F4**).

Helper script: [scripts/sync-web-to-pi.sh](../scripts/sync-web-to-pi.sh).

## Demo data shape (`MIRROR_DEMO`)

| Key | Purpose |
|-----|---------|
| `nowPlaying` | `title`, `artist`, `artworkUrl`, `isIdle`. `nextUp`: `{ artist, title }` (artist line above title; no art). Cleared when idle. |
| `weather.today` | `condition`, `feelsLikeF`, `precipChance`, `icon` (keys in [js/weather-icons.js](js/weather-icons.js)). |
| `weather.hourlyToday` | ~6 slots: `hourLabel`, `tempF`, `icon`. |
| `calendar.events` | `offsetFromToday` (0 = today), `time`, `title` → **5 columns** (today … today+4). |
| `todos.items` | `text`, `done` — fills a **3×2** grid (six slots typical). |
| `videoRadar.videos` | Up to **3** items: `title`, `creator`, and **`hoursAgo`** (demo) or **`publishedAt`** (ISO; UI formats as *N hours ago* under 24h). |

Weather symbols use **`var(--wx-*)`** in [css/tokens.css](css/tokens.css) for multi-color icons.

## Layout choices (exploration)

| Module | Presentation | Rationale |
|--------|----------------|-----------|
| **Clock** | **12-hour** + **AM/PM** | Glanceable from across the room. |
| **Now playing** | Art + current title/artist; **Next up** column (artist, then title) | Queue from HA / Spotify / etc. |
| **Weather — today** | Icon + condition + feels + precip | Compact. |
| **Weather — 6h** | Hour slots for **today** | Rest-of-day trend. |
| **Calendar** | **Five** columns: **today** (left) + **next 4 days** | Wider cells; always forward-looking. |
| **To-Do** | **2 rows × 3 columns** | Full-width daily board. |
| **Video radar** | **3** cards: title, creator, *N hours ago* | Subscription feed stub for YouTube/API later. |

**Wood frame:** `--mm-frame-inset: 36px` in [css/tokens.css](css/tokens.css) — align with [preview/preview-dock.css](../docs/design/preview/preview-dock.css).

## Files

| Path | Role |
|------|------|
| [index.html](index.html) | Shell + inline **weather SVG sprite** (`#wx-*` symbols) |
| [css/tokens.css](css/tokens.css) | CSS variables + **weather palette** |
| [css/mirror.css](css/mirror.css) | Layout + modules |
| [js/demo-data.js](js/demo-data.js) | `MIRROR_DEMO` shape for HA replacement |
| [js/weather-icons.js](js/weather-icons.js) | Condition key → symbol id + `<use>` helper |
| [js/app.js](js/app.js) | Clock tick + hydrate from demo |

## HA integration (later)

- **Media:** Art + current track; **next** from queue / `media_player` attributes.
- **M-002:** `weather.today` + `hourlyToday`.
- **M-005 / M-006:** School ICS (backend) + HA **`todo.elliot`** — see [MIRROR_RUNTIME.md](../docs/MIRROR_RUNTIME.md).
- **Video radar:** RSS / YouTube Data API / n8n → `videoRadar.videos` with `publishedAt` or `hoursAgo`.
- **Night mode:** toggle `class="mirror--night"` on `<html>` or `body` from HA helper (**FR-007**).

## Traceability

- **FR-005** — type sizes in CSS variables from tokens.
- **FR-009** — weather + calendar + todo modules present.
- **UI_MODES** — this page is **passive** hierarchy; Pomodoro / `active_engaged` layouts can reuse tokens in separate HTML or routed view later.
