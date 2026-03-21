# Commands: Mac vs Pi (no keyboard on the Pi)

## Default mirror Pi (copy-paste as-is)

Scripts default to **`pi@mirror-pi4.local`** (mDNS on your LAN). You do **not** need `export PI=…` unless you use a different SSH target.

**Repo root on the Mac** (change the path if your clone lives elsewhere):

`~/Desktop/CurrentProjects/General/magic-mirror`

---

## Do I run everything in order?

**No.** The sections below are **different jobs** (sync UI only, run backend on Mac, deploy full app to Pi, etc.). You only run what you need.

---

## Full deploy: web + backend + config + venv + token copy + API + Chromium

From your **Mac**:

```bash
cd ~/Desktop/CurrentProjects/General/magic-mirror
./scripts/deploy-mirror-to-pi.sh --all
```

**`--all`** = rsync `web/` + `backend/` + `config/` → **`~/mirror-app/`** on the Pi, create **venv + pip**, copy **`~/.config/mirror/ha_token`** from your Mac if it exists, **start** the API on **:8780**, **open Chromium** to `http://127.0.0.1:8780/`.

### After code changes (no new Python deps)

```bash
cd ~/Desktop/CurrentProjects/General/magic-mirror
./scripts/deploy-mirror-to-pi.sh
./scripts/deploy-mirror-to-pi.sh --start-backend
```

### After `requirements.txt` changes

```bash
cd ~/Desktop/CurrentProjects/General/magic-mirror
./scripts/deploy-mirror-to-pi.sh --install-deps --start-backend
```

### Flags (combine as needed)

**`--install-deps`** · **`--copy-ha-token`** · **`--start-backend`** · **`--open`** — see `./scripts/deploy-mirror-to-pi.sh --help`

### Enable auto-restart after power loss (recommended)

Install systemd units on the Pi so both backend and Chromium kiosk auto-start on boot:

```bash
cd ~/Desktop/CurrentProjects/General/magic-mirror
./scripts/deploy-mirror-to-pi.sh --install-deps --enable-autostart
```

Verify from your Mac:

```bash
ssh pi@mirror-pi4.local 'systemctl status mirror-backend.service --no-pager | sed -n "1,14p"'
ssh pi@mirror-pi4.local 'systemctl status mirror-kiosk.service --no-pager | sed -n "1,14p"'
```

Disable later if needed:

```bash
ssh pi@mirror-pi4.local 'sudo systemctl disable --now mirror-kiosk.service mirror-backend.service'
```

---

## Test the API from your Mac (same LAN)

```bash
curl -sS "http://mirror-pi4.local:8780/api/health"
curl -sS "http://mirror-pi4.local:8780/api/snapshot" | head -c 2500
```

`health` includes **`mirror_backend_build`** — after deploy + `--start-backend`, it should match the value in `backend/mirror_backend/main.py`. If it doesn’t change, the Pi is still running an old build (rsync path, wrong host, or backend didn’t restart).

If **`errors`** in the snapshot contains **`ha:forecast_hourly_empty`**, Home Assistant didn’t return hourly forecast rows (wrong token, entity list, or HA API shape). See **[BACKEND_HA_INTEGRATION_2026-03.md](BACKEND_HA_INTEGRATION_2026-03.md)** for **`get_forecasts`** / response unwrapping and weather entity chains; redeploy so the Pi runs the same backend as your Mac.

### Pi shows school calendar but **no hourly weather** and **no todos**

The calendar comes from **ICS** on the Pi; hourly + todos need **Home Assistant** + the **latest backend** (WebSocket `return_response` + `result.response` parsing). If the Mac snapshot is good but the mirror is not:

1. **`curl` the Pi from your Mac** — `mirror_backend_build` must match `backend/mirror_backend/main.py` (not an older date).
2. **Redeploy web + backend** — `./scripts/deploy-mirror-to-pi.sh` then `./scripts/deploy-mirror-to-pi.sh --start-backend`. Restarting uvicorn **without rsync** leaves old Python on disk.
3. **Hard-refresh Chromium** — use **`--open`** on deploy, or SSH `pkill` chromium and reopen **`http://127.0.0.1:8780/`**. Kiosk mode caches JS aggressively; the app now sends **no-cache** headers and versioned script URLs to force reload after deploy.
4. **Pi token** — `~/.config/mirror/ha_token` must be valid (same idea as the Mac). **`--copy-ha-token`** on deploy copies from your Mac if that file exists.

### Backend log on the Pi (from Mac)

```bash
ssh pi@mirror-pi4.local 'tail -80 /tmp/mirror-backend.log'
```

---

## Run the **backend + UI** on your Mac only (no Pi)

```bash
cd ~/Desktop/CurrentProjects/General/magic-mirror
./scripts/run-mirror-backend.sh
```

Then open: `http://127.0.0.1:8780/`

### HA token on the Mac (one-time)

```bash
mkdir -p ~/.config/mirror
chmod 700 ~/.config/mirror
nano ~/.config/mirror/ha_token
chmod 600 ~/.config/mirror/ha_token
```

---

## Copy **HA token** to the Pi (Mac → Pi, no typing on Pi)

Assumes **`~/.config/mirror/ha_token`** already exists on the Mac.

```bash
ssh pi@mirror-pi4.local 'mkdir -p ~/.config/mirror && chmod 700 ~/.config/mirror'
scp ~/.config/mirror/ha_token pi@mirror-pi4.local:~/.config/mirror/ha_token
ssh pi@mirror-pi4.local 'chmod 600 ~/.config/mirror/ha_token'
```

(Deploy with **`--copy-ha-token`** or **`--all`** does this automatically if the Mac file exists.)

---

## Sync **web UI only** to the Pi (`~/mirror-web/`)

```bash
cd ~/Desktop/CurrentProjects/General/magic-mirror
./scripts/sync-web-to-pi.sh
./scripts/sync-web-to-pi.sh --open
```

Windowed Chromium (easier to debug):

```bash
cd ~/Desktop/CurrentProjects/General/magic-mirror
PREVIEW_WINDOWED=1 ./scripts/sync-web-to-pi.sh --open
```

---

## Manual rsync (only if you skip the deploy script)

```bash
cd ~/Desktop/CurrentProjects/General/magic-mirror
rsync -avz --delete ./web/ pi@mirror-pi4.local:~/mirror-app/web/
rsync -avz --delete --exclude '.venv' ./backend/ pi@mirror-pi4.local:~/mirror-app/backend/
rsync -avz ./config/ pi@mirror-pi4.local:~/mirror-app/config/
```

---

## Design preview sync

See [docs/design/preview/README.md](design/preview/README.md). Typical:

```bash
cd ~/Desktop/CurrentProjects/General/magic-mirror
./scripts/sync-design-preview-to-pi.sh --open
```

---

## SSH shell on the Pi

```bash
ssh pi@mirror-pi4.local
```

Exit: `exit`

---

## Kill Chromium on the Pi from the Mac

```bash
ssh pi@mirror-pi4.local 'pkill -f chromium || pkill -f chromium-browser || true'
```

---

## Many SSH password prompts?

**Best fix:** install your Mac’s public key on the Pi (one-time):

```bash
ssh-copy-id pi@mirror-pi4.local
```

After that, `ssh` / `rsync` / `scp` stop asking each time.

**Without keys:** `deploy-mirror-to-pi.sh` reuses **one** SSH connection per run (multiplexing), so you should only enter the password **once** per script invocation (two runs = two passwords). If a run still asks repeatedly, try `MIRROR_SSH_NO_MUX=1 ./scripts/deploy-mirror-to-pi.sh` once to rule out a stuck control socket, then remove `~/.ssh/cm-mirror-deploy-*` if needed.

---

## `/api/snapshot` shows `ha:weather_missing` or empty todos

Your Home Assistant **entity IDs** may not match the committed example (`weather.pirateweather`, `weather.forecast_home`, `todo.elliot`). The mirror **does** reach HA when `source` is **`live`** — it just cannot find those entities.

1. In HA: **Developer tools → States** — search **`weather.`** and **`todo.`** and note the exact IDs (e.g. `weather.openweathermap`, `todo.shopping_list`).
2. On your Mac, create **`config/mirror.runtime.local.yaml`** (gitignored) next to the example file:

```yaml
home_assistant:
  base_url: http://homeassistant.local:8123   # or http://192.168.x.x:8123 if mDNS fails from the Pi

entities:
  weather_entities:
    - weather.YOUR_WEATHER_ENTITY
  todo_list: todo.YOUR_TODO_ENTITY
```

3. Deploy again so the Pi gets the new file:

```bash
cd ~/Desktop/CurrentProjects/General/magic-mirror
./scripts/deploy-mirror-to-pi.sh
./scripts/deploy-mirror-to-pi.sh --start-backend
```

If **`todo_list`** is correct but **`todos.items`** is still empty, the list may have no open tasks, or the integration may use a different item shape — check HA’s **To-do** UI and we can adjust parsing if needed.

---

## Use a **different** Pi or hostname

```bash
export PI=pi@192.168.1.50
cd ~/Desktop/CurrentProjects/General/magic-mirror
./scripts/deploy-mirror-to-pi.sh --all
```

Or one-shot: `PI=pi@other-host ./scripts/deploy-mirror-to-pi.sh`

---

## Related docs

- [MIRROR_RUNTIME.md](MIRROR_RUNTIME.md) — token path, HA URL, ICS settings  
- [PI_BRINGUP.md](PI_BRINGUP.md) — OS, HDMI, SSH keys  
- [web/README.md](../web/README.md) — local preview  
- [backend/README.md](../backend/README.md) — API + static `web/`  
- [scripts/deploy-mirror-to-pi.sh](../scripts/deploy-mirror-to-pi.sh)
