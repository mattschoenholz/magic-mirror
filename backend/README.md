# Mirror backend (Python / FastAPI)

Serves **`web/`** as static files and **`GET /api/snapshot`** — HA + merged school ICS. **No tokens in the browser** (**FR-006**).

## Quick start (Mac / dev)

From **repo root**:

```bash
./scripts/run-mirror-backend.sh
```

Open **`http://127.0.0.1:8780/`** — the UI loads and replaces demo data with live snapshot when HA token is present.

## Configuration

- **Defaults:** [config/mirror.runtime.example.yaml](../config/mirror.runtime.example.yaml) (committed).
- **Overrides:** `config/mirror.runtime.local.yaml` (gitignored) — e.g. `home_assistant.base_url` with Pi 5 IP.
- **Secrets:** [docs/MIRROR_RUNTIME.md](../docs/MIRROR_RUNTIME.md) — create `~/.config/mirror/ha_token` (mode `600`) with your long-lived HA token, or set `MIRROR_SECRETS_DIR` / `MIRROR_HA_TOKEN_FILE`.

## Endpoints

| Path | Purpose |
|------|---------|
| `GET /api/snapshot` | JSON payload matching `web/js/demo-data.js` shape (weather, calendar, todos, stubs for Spotify/YouTube). |
| `GET /api/health` | `{ "ok": true }` |

## Tests

```bash
cd backend
python3 -m pip install -r requirements.txt -r requirements-dev.txt
python3 -m pytest -q
```

## Manual venv (without script)

```bash
cd backend
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
export PYTHONPATH="$(pwd)"
.venv/bin/python -m uvicorn mirror_backend.main:app --host 127.0.0.1 --port 8780
```

## Pi deployment (from your Mac, no keyboard on Pi)

```bash
export PI=pi@mirror-pi4
cd ~/Desktop/CurrentProjects/General/magic-mirror
./scripts/deploy-mirror-to-pi.sh --all
```

Uses **`~/mirror-app/`** on the Pi (`web`, `backend`, `config`) and sets **`MIRROR_REPO_ROOT`** when starting **uvicorn**. Logs: **`/tmp/mirror-backend.log`** on the Pi.

**systemd** (auto-start on boot) is still optional — see **`mm-kiosk-pi`**.

## Stack

Chosen **2026-03-21** — **Python 3** + **FastAPI** + **httpx** + **icalendar** + **websocket-client** (see [docs/MIRROR_RUNTIME.md](../docs/MIRROR_RUNTIME.md) §7).
