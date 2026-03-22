# Mirror runtime configuration (single source of truth)

**Purpose:** Remove guesswork for Coder, Architect, and ops. Values here are **locked for v1** unless explicitly changed in this file and noted in `ARCHITECTURE.md`.

**FR-006:** The browser **never** holds HA, Spotify, or YouTube tokens. A **local backend** on the mirror Pi reads secrets from disk / env and exposes a **same-origin** API to the static UI.

---

## 1. Time & locale

| Key | Value |
|-----|--------|
| **Mirror timezone** | `America/Los_Angeles` |
| **Home Assistant** | Also `America/Los_Angeles` (verified via MCP) |

Use this timezone for: clock (if not purely client local), calendar column boundaries, “today”, and parsing ICS `DTSTART` into wall time.

---

## 2. Secrets on the mirror Pi (never in git)

### 2.1 Recommended layout

| Path | Contents | Permissions |
|------|----------|----------------|
| **`/etc/mirror/`** (preferred) **or** **`~/.config/mirror/`** | Directory for runtime secrets | `chmod 700` |
| **`ha_token`** (in that directory) | HA long-lived access token, one line | `chmod 600` |
| **Spotify** (when enabled) | e.g. `spotify_client_id`, `spotify_client_secret`, `spotify_refresh_token` — exact filenames TBD when backend lands | `600` |
| **YouTube / Google** (when enabled) | OAuth client JSON + refresh token file — exact layout TBD when backend lands | `600` |

You add the HA token **once** on the Pi after install.

### 2.2 Environment variables (suggested contract)

Backend SHOULD support:

| Variable | Meaning |
|----------|---------|
| `MIRROR_SECRETS_DIR` | Directory containing `ha_token` and future secret files (default e.g. `/etc/mirror` or `~/.config/mirror`) |
| `MIRROR_HA_TOKEN_FILE` | Optional override: full path to token file if not `$MIRROR_SECRETS_DIR/ha_token` |
| `MIRROR_HA_URL` | Optional override for HA base URL (default from committed example config) |

Do **not** put token values in environment variables if avoidable (process lists); **file on disk** is preferred.

---

## 3. Home Assistant

### 3.1 Base URL

| Key | Value |
|-----|--------|
| **Default base URL** | `http://homeassistant.local:8123` |

Mirror Pi must resolve **`homeassistant.local`** (mDNS). If it fails in the field, set **`MIRROR_HA_URL`** to the Pi 5’s **static IP** (document the IP on the hardware label or home network docs — not in this public repo).

### 3.2 Entity IDs (verified 2026-03-20 via HA MCP)

Use **exact** `entity_id` strings:

| Role | `entity_id` | Friendly name | Notes |
|------|-------------|---------------|--------|
| **Weather (Open-Meteo)** | **`weather.home`** | Home | Hourly + daily via HA **`weather.get_forecasts`**; common secondary / hourly source. |
| **Weather (Pirate Weather)** | **`weather.pirateweather`** | PirateWeather | Default first choice for **`entities.weather_now_entities`** and **`entities.forecast_weather_entities`** (often better *current* condition at night). Attribution in HA: *Powered by Pirate Weather* |
| **“Now” tile chain** | **`entities.weather_now_entities`** | ordered list | Backend tries each entity’s **`state` → large tile** (condition, feels like, icon). Default: Pirate → `weather.home` → `weather.forecast_home`. If none work, falls back to **`entities.weather_entities`**. |
| **Hourly strip chain** | **`entities.forecast_weather_entities`** | ordered list | **`weather.get_forecasts`** (`type: hourly`). First entity that returns rows wins. **Six** slots: forecast periods **strictly after** “now” (no second “Now” in the strip). If this key is **omitted**, backend uses **`weather_entities`** but tries **`weather.pirateweather` first** when it appears anywhere in that list. |
| **Legacy fallbacks** | **`entities.weather_entities`** | e.g. `weather.forecast_home` | Used when **`weather_now_entities`** yields nothing usable; also drives the default hourly chain when **`forecast_weather_entities`** is omitted (with Pirate reordered first if listed). |
| **Todo list** | **`todo.elliot`** (default) | e.g. Elliot / “Local To-do” in HA UI | **Friendly name ≠ `entity_id`.** Configure **`entities.todo_list`** or **`entities.todo_entities`**. Backend calls **`todo.get_items`**; parses HA’s **`service_response`** wrapper. **Empty list** usually means **no open (needs_action) tasks** — check HA’s To-do UI and entity state. |

**Out of scope unless product changes:** `todo.shopping_list` as the primary list. **`weather.forecast_home`** remains an optional fallback in **`entities.weather_entities`**.

### 3.3 Mapping → first-screen UI (weather)

Current UI expects **condition**, **feels like**, **precip %** (see `web/`).

| UI field | Source |
|----------|--------|
| Condition label | `state` (e.g. `cloudy` → humanize “Cloudy”) + icon map |
| Feels like | `attributes.apparent_temperature` or `temperature` + `temperature_unit` |
| Hourly row | Same as above, from **`forecast_weather_entities`** (or **`weather_entities`**). **Six** entries: next forecast buckets after the current time (clock labels only). |
| Precipitation % | From hourly/daily forecast rows when present (`precipitation_probability`, etc.). Open-Meteo hourly may expose **`precipitation`** (amount) instead of a probability — mirror may show **“—”** for POP. |

Other useful attributes on the entity today: `temperature`, `humidity`, `wind_speed`, etc. — optional for future tiles.

### 3.4 Mapping → first-screen UI (todos)

| UI field | Source |
|----------|--------|
| To-Do grid | Items from configured todo entity(ies), default **`todo.elliot`**, via **`todo.get_items`**. Map `status` / `completed` to done styling. Text from `title` / `summary` / `name` / `subject`. If **more than six** items are returned after merge/dedupe, the mirror shows **only incomplete** tasks, up to **six**. |

### 3.5 Alexa / Echo (v1)

**Display-only.** No Alexa Skill or push to the Pi for slice 1. Echo → HA automations may still drive **other** entities later; **now playing** for the mirror is **Spotify-only** (below).

---

## 4. School calendar — ICS (no HA calendar for this slice)

The mirror **backend** fetches and merges these feeds. **Do not** require HA `calendar.*` for school for v1.

### 4.1 Feed URLs & calendar names

| # | `X-WR-CALNAME` (from feed) | URL |
|---|-----------------------------|-----|
| 1 | CP - Community Period | [calendar_356.ics](https://www.bishopblanchet.org/calendar/calendar_356.ics) |
| 2 | Gold Day | [calendar_358.ics](https://www.bishopblanchet.org/calendar/calendar_358.ics) |
| 3 | Green Day | [calendar_352.ics](https://www.bishopblanchet.org/calendar/calendar_352.ics) |
| 4 | Special Schedule | [calendar_377.ics](https://www.bishopblanchet.org/calendar/calendar_377.ics) |
| 5 | Unified Day | [calendar_360.ics](https://www.bishopblanchet.org/calendar/calendar_360.ics) |

### 4.2 Fetch policy

| Key | Value |
|-----|--------|
| **Refresh interval** | **15 minutes** |
| **HTTP User-Agent** | `MagicMirrorFamily/1.0` (identify politely; adjust if host blocks) |
| **Referer** | Optional `school_calendar.http_referer` in runtime YAML (e.g. school site origin) if feeds return **403** without it |
| **Failure** | Retry with backoff; serve **last good merged calendar** if available; UI may show stale indicator (align with FSD if added) |
| **Max events / day** | `school_calendar.max_events_per_day` (default **4**) | Caps columns after all feeds are merged. |

### 4.3 Parsing & display rules

- **Timezone:** interpret and display in **`America/Los_Angeles`**.
- **All-day events** (`DTSTART;VALUE=DATE` or date-only): show **no** time pill; title only (e.g. Gold Day / Green Day).
- **Timed events** (`DTSTART` datetime): show **local** start–end or start + duration per UI design.
- **Merge:** Union all events from all feeds. If the same logical event appears twice, prefer **dedupe by `UID`** when present.
- **UI columns:** **Today (left) + next 4 days** — filter merged events into those five local dates.

---

## 5. Spotify (your account — not HA integration)

| Key | Decision |
|-----|----------|
| **Source of truth** | **Spotify Web API** from the mirror backend, using **your** OAuth app + **refresh token** on the Pi |
| **HA Spotify integration** | **Do not use** for mirror now playing (wrong account) |
| **Echo / other players** | **Do not** mix in for v1 — **Spotify only** for “Now playing” / “Next up” |
| **Auth timing** | User will provide **client id/secret + refresh token** later; until then backend may return empty / placeholder |

---

## 6. YouTube — Video radar (subscriptions API)

| Key | Decision |
|-----|----------|
| **API** | YouTube Data API v3 (subscriptions / activity — exact endpoints chosen in implementation) |
| **Account** | Same Google account as OAuth |
| **On quota error, API error, or no auth** | **Hide** the Video Radar section entirely (no empty shell with error text required) |

Auth files on Pi when enabled — same secrets dir pattern as §2.

---

## 7. Backend stack

**Chosen 2026-03-21:** **Python 3** + **FastAPI** (`backend/`), serving static `web/` and **`GET /api/snapshot`**. See [backend/README.md](../backend/README.md) and [scripts/run-mirror-backend.sh](../scripts/run-mirror-backend.sh).

---

## 8. Display sleep (Pi — optional)

**Goal:** After a chosen local time (default **23:00**), turn the **screen off** for the bedroom; restore in the morning (default **06:00**). Times follow the **Pi system timezone** — set **`America/Los_Angeles`** with `sudo timedatectl set-timezone America/Los_Angeles` so they match `timezone:` in the runtime YAML.

| Method | Behavior |
|--------|----------|
| **`hdmi`** | **`vcgencmd display_power`** — blanks Pi HDMI output. TV may show **no signal** or dim; no extra packages. |
| **`cec`** | **`cec-client`** (package **`cec-utils`**) — asks the TV to **standby** over **HDMI-CEC** (Samsung **Anynet+** on). May need **`sudo`** for `/dev/cec0`; wake is TV‑model dependent. |
| **`both`** | HDMI blank **and** CEC standby — use when the **backlight stays on** with HDMI-only or Chromium keeps re-enabling the output; install **`sudo apt install -y cec-utils`** on the Pi first. |

**Deploy profile** (`MIRROR_SLEEP_PROFILE` — written to **`/etc/systemd/system/mirror-display-sleep.env`** by the install script):

| Profile | Effect |
|---------|--------|
| **`instant`** (default) | **`METHOD=cec`**, **`STOP_KIOSK=0`**, **`USE_WLR=0`** — TV standby via CEC only; **kiosk keeps running**; **fast wake**. |
| **`both`** | **`METHOD=both`**, **`STOP_KIOSK=1`**, **`USE_WLR=1`** — stop kiosk, Wayland output off, **`vcgencmd`**, and CEC — **harder blank**, **slower wake**. |

**TV checklist (required for CEC to do anything):**

1. On the **Samsung**: turn **HDMI-CEC / Anynet+** **ON** (you had it off — that matches **`cec-scan`** showing only the Pi, not a TV).
2. **Input** on the TV must be the **Pi’s HDMI** when you test.
3. **Pi:** prefer **HDMI0** (the port **next to USB-C**) for CEC.
4. Re-check: **`sudo ~/mirror-app/scripts/pi-display-sleep.sh cec-scan`** — you want to see a **TV** (or similar), not only **Recorder 1**.

**Why “instant” is the default:** **HDMI blanking** (`vcgencmd` / `wlr-randr`) can fight **Chromium** — the compositor turns the output back on — which is why the **`both`** profile **stops `mirror-kiosk`** before a hard blank. If you **only** send CEC `standby`/`on` to the TV (**`instant`**), Chromium can keep running; wake is **faster** (no cold start). Tradeoff: Pi uses **full power** overnight; if CEC fails, the **mirror image may still be visible** until you fix CEC or switch to **`MIRROR_SLEEP_PROFILE=both`**.

From the Mac, default install is **`instant`**: `./scripts/deploy-mirror-to-pi.sh --install-display-sleep`. For the harder blank: `MIRROR_SLEEP_PROFILE=both ./scripts/deploy-mirror-to-pi.sh --install-display-sleep`. On the Pi you can edit **`mirror-display-sleep.env`** or re-run the install script with the same variable. The oneshot services read **`EnvironmentFile`** on each run; **`sudo systemctl restart mirror-display-sleep-off.timer mirror-display-sleep-on.timer`** is optional after edits.

**TV OSD / banners when the set comes on:** There is **no standard Pi/CEC command** to suppress Samsung’s **on-screen menus** (input name, Anynet+, “new device,” etc.) — that’s **TV firmware**. Reduce noise in the TV’s own menus: **disable Store/Demo mode**, use **Home** (not retail) mode, turn off **logo/indicator** options if listed, **reduce HDMI CEC notifications** / device discovery prompts where the model allows, and **disable Smart Hub** startup banners if present. Exact paths vary by **Samsung model year**; treat as a one-time TV setup task, not something the mirror repo can automate.

**Install:** [scripts/install-pi-display-sleep-schedule.sh](../scripts/install-pi-display-sleep-schedule.sh) (creates `mirror-display-sleep-off.timer` / `mirror-display-sleep-on.timer`). From Mac: `./scripts/deploy-mirror-to-pi.sh --install-display-sleep` (see [MAC_VS_PI_COMMANDS.md](MAC_VS_PI_COMMANDS.md)).
**Manual test:** `~/mirror-app/scripts/pi-display-sleep.sh off` then `on` (env matches **`mirror-display-sleep.env`** / your profile).

**Disable:** `sudo systemctl disable --now mirror-display-sleep-off.timer mirror-display-sleep-on.timer`

**Troubleshooting — blanking “doesn’t stick”:** If **`mirror-kiosk.service`** is running (Chromium), it can **re-enable HDMI** right after `vcgencmd` turns it off. The sleep script **stops `mirror-kiosk` before** blanking and **starts it again after** wake (see `MIRROR_DISPLAY_SLEEP_STOP_KIOSK` in `/etc/systemd/system/mirror-display-sleep.env`). Requires **root** (or `sudo`) for `systemctl`.

**Troubleshooting — TV stays on, CEC “does nothing”:** Run **`sudo ~/mirror-app/scripts/pi-display-sleep.sh cec-scan`**. If the list only shows **Recorder 1** (the Pi) and **no TV**, HDMI-CEC is not reaching the set (Anynet+ off, wrong **Pi HDMI port** — use **HDMI0** next to USB-C — bad cable/passthrough, or mirror hardware blocking the CEC pin). In that case **`cec-client` cannot turn the TV off**; the script also uses **`wlr-randr --output HDMI-A-1 --off`** (Wayland) and **`vcgencmd`** to drop the signal. If the **backlight** still stays on, use a **smart plug**, **Samsung network / SmartThings** via Home Assistant, or fix the HDMI/CEC path.

---

## 9. Related files in repo

| File | Role |
|------|------|
| [config/mirror.runtime.example.yaml](../config/mirror.runtime.example.yaml) | **Committed** defaults: URLs, entity IDs, ICS list, intervals — **no secrets** |
| `config/mirror.runtime.local.yaml` | **Gitignored** — optional local overrides (IP instead of `.local`, etc.) |
| [scripts/deploy-mirror-to-pi.sh](../scripts/deploy-mirror-to-pi.sh) | **Mac → Pi**: rsync app tree, venv, token copy, start API, open Chromium |
| [scripts/pi-display-sleep.sh](../scripts/pi-display-sleep.sh), [scripts/install-pi-display-sleep-schedule.sh](../scripts/install-pi-display-sleep-schedule.sh) | Nightly HDMI blank + morning restore; optional CEC |
| [ARCHITECTURE.md](ARCHITECTURE.md) | Diagrams, high-level boundaries |
| [HA_DEV.md](HA_DEV.md) | Dev machine MCP token (not mirror Pi) |

---

## 10. Changelog

| Date | Change |
|------|--------|
| 2026-03-21 | Initial locked spec: HA entities, five ICS feeds, timezone, secrets layout, Spotify/YouTube rules. |
| 2026-03-21 | Backend = Python FastAPI; `/api/snapshot` + static `web/`. |
| 2026-03-21 | §8 Display sleep: `vcgencmd` + optional CEC; systemd timers; deploy flag. |
| 2026-03-22 | §8 Deploy default **`MIRROR_SLEEP_PROFILE=instant`** (CEC-only); **`both`** still available; **`cec-utils`** on Pi for CEC path. |
| 2026-03-22 | §8 Wayland **`wlr-randr`** output off/on; **`cec-scan`** when TV missing from CEC bus. |
| 2026-03-22 | §8 TV checklist: Samsung **Anynet+/HDMI-CEC must be ON** for CEC control. |
| 2026-03-22 | §8 CEC-only instant profile (no kiosk kill); TV OSD note (firmware). |
