# Backend + Home Assistant integration — decisions & handoff (March 2026)

**Audience:** You (or another machine) after `git clone` / `git pull`. This captures **product decisions**, **HA API gotchas**, **config keys**, **code locations**, and **ops** for the mirror snapshot pipeline (`/api/snapshot`).

**Related:** [MIRROR_RUNTIME.md](MIRROR_RUNTIME.md) (entity IDs, secrets), [MAC_VS_PI_COMMANDS.md](MAC_VS_PI_COMMANDS.md) (deploy, curl, Pi troubleshooting), [HA_DEV.md](HA_DEV.md) (MCP, tokens).

---

## 1. Resume on a new computer

1. **Clone** the repo (see [GITHUB.md](GITHUB.md)).
2. **Runtime config:** Copy `config/mirror.runtime.example.yaml` → `config/mirror.runtime.local.yaml` (gitignored) or use Pi paths under `/etc/mirror/` as you prefer. **Never commit** tokens.
3. **HA token (Mac dev):** `~/.config/mirror/ha_token`, mode `600` (see [MAC_VS_PI_COMMANDS.md](MAC_VS_PI_COMMANDS.md)).
4. **Backend tests:** From `backend/`, run `python3 -m pytest -q`.
5. **Local UI + API:** `./scripts/run-mirror-backend.sh` → open `http://127.0.0.1:8780/`.
6. **Pi deploy:** `./scripts/deploy-mirror-to-pi.sh` (see flags in MAC_VS_PI). Confirm **`mirror_backend_build`** on `/api/health` matches `MIRROR_BACKEND_BUILD` in `backend/mirror_backend/main.py`.

---

## 2. Product decisions (locked for current slice)

### 2.1 Weather: large tile = true “now”, strip = next six hours

| Decision | Rationale |
|----------|-----------|
| **Separate sources for “now” vs hourly** | Open-Meteo (`weather.home`) sometimes reported a **daytime** condition (e.g. sunny) **at night**. **Pirate Weather** (`weather.pirateweather`) matched real conditions and hourly buckets better in the field. |
| **`weather_now_entities`** | Ordered list: first entity with a **usable** `state` wins for **`weather.today`** (condition, icon, feels-like). **Default** in code: `weather.pirateweather` → `weather.home` → `weather.forecast_home`. If none work, backend falls back to **`weather_entities`**. |
| **`forecast_weather_entities`** | Ordered list for **`weather.get_forecasts`** (`type: hourly`). First entity that returns rows wins. **Example config** lists Pirate first. |
| **Implicit Pirate-first for hourly** | If **`forecast_weather_entities` is omitted**, backend uses **`weather_entities`** but **moves `weather.pirateweather` to the front** when it appears anywhere in that list—so old YAML with `weather.home` first still prefers Pirate for hourly when both exist. |
| **Six hourly slots, no “Now” in strip** | The **large card** is “now”. The **strip** shows **six** periods whose forecast **`datetime` is strictly after** the current instant (`America/Los_Angeles`). Labels are **clock times only** (no synthetic `"Now"`). Avoids duplicating the big tile and aligns with “next hour onward.” |
| **Relaxed fallback** | If strict `datetime > now` yields **no** slots (clock skew / sparse rows), a fallback allows buckets from **up to 1 hour in the past**, still with clock labels only. |

**Timezone:** Parsing and “now” comparisons use **`ZoneInfo("America/Los_Angeles")`** in `mirror_backend/snapshot.py` (`LA`).

### 2.2 Todos: overflow behavior

| Decision | Rule |
|----------|------|
| **≤ 6 items (after merge/dedupe)** | Show **all** (completed + incomplete) as returned. |
| **> 6 items** | Show **only incomplete** (`done: false`), **capped at 6**. Reduces clutter when the HA list is long and mostly historical completes. |

### 2.3 Multiple todo lists

- **`entities.todo_entities`:** ordered merge; **dedupe** by `uid` or by normalized title.
- **`entities.todo_list`:** single list when `todo_entities` not set.

---

## 3. Home Assistant API learnings

### 3.1 `weather.get_forecasts`

- **Correct invocation:** Weather entity goes in **`target`**, not only inside `service_data`. Service data is **`{ "type": "hourly" }`** (per HA `services.yaml`).
- **`return_response`:** Must be **`true`** on `call_service` or the client gets no forecast payload.
- **Response shape:** WebSocket returns data under **`result.response`** (nested by entity id → `forecast` list). REST may use **`service_response`**. Client normalizes both in **`_extract_forecast_list`** (`ha_client.py`).
- **Legacy retry:** Code tries **`target_entity_id`** first, then a WS variant with **`entity_id` in service_data**, then REST.

### 3.2 `todo.get_items`

- Same idea: **`return_response=True`**; unwrap **`response`** / **`service_response`**; recurse until **`items`** list is found (`_extract_todo_items`).

### 3.3 Empty hourly / empty todos on Pi but calendar works

- **Calendar** is **ICS** in the backend—no HA required for school columns.
- **Hourly + todos** require a **valid token**, correct **entity IDs**, and **current backend** on the Pi. Stale Python on disk, cached Chromium assets, or old **`mirror_backend_build`** are the usual split-brain causes. See [MAC_VS_PI_COMMANDS.md](MAC_VS_PI_COMMANDS.md) § Pi shows calendar but no hourly/todos.

---

## 4. Code map

| Area | File | Notes |
|------|------|--------|
| Snapshot assembly | `backend/mirror_backend/snapshot.py` | `build_snapshot`, `_weather_now_entity_chain`, `_forecast_entity_chain`, `_hourly_strip_next_six`, `_hourly_strip_relaxed`, todo filter |
| HA calls | `backend/mirror_backend/ha_client.py` | `ha_get_forecasts`, `ha_get_todo_items`, `ha_ws_call_service`, unwrappers |
| Weather labels/icons | `backend/mirror_backend/weather_map.py` | Condition → UI icon key / label |
| Build stamp | `backend/mirror_backend/main.py` | `MIRROR_BACKEND_BUILD` — bump when shipping behavior users must verify |
| Example config | `config/mirror.runtime.example.yaml` | `weather_now_entities`, `forecast_weather_entities`, `weather_entities`, todos |
| Tests | `backend/tests/test_snapshot_todos.py`, `test_snapshot_weather.py`, `test_ha_client_forecast.py`, `test_ha_client_todo.py` | |

---

## 5. Operations & caching

- **`GET /api/health`** returns **`mirror_backend_build`**. After deploy, if it **does not** match `main.py`, the Pi is not running the new code (rsync path, no restart, wrong host).
- **Static UI:** Middleware and/or query strings on assets may send **no-store** / version bumps so Chromium picks up new JS/CSS after deploy (see repo history around kiosk cache issues).
- **Secrets:** Token only on disk on Pi/Mac; **FR-006** — browser never holds HA tokens.

---

## 6. Session capsule (for chat / context limits)

Copy if you need a **short paste** into a new conversation:

- **Stack:** Pi runs FastAPI backend + static `web/`; HA on LAN; snapshot drives weather, todos, ICS calendar.
- **Weather:** `weather_now_entities` → big tile; `forecast_weather_entities` (or Pirate-first reorder) → `get_forecasts` hourly; **6** slots **after** now, no `"Now"` in strip; LA timezone.
- **Todos:** If **>6** merged items → **incomplete only**, max **6**.
- **HA:** `get_forecasts` / `get_items` need **`return_response`**; unwrap **`response`** (WS) vs **`service_response`** (REST).
- **Verify deploy:** `/api/health` → **`mirror_backend_build`** matches `main.py`.

---

*Last updated: 2026-03-20 — align with `MIRROR_RUNTIME.md` if entity defaults change.*
