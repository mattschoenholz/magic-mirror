# Home Assistant — development and tokens

## Topology (this project)

| Role | Hardware | Notes |
|------|----------|--------|
| **Home Assistant** | **Raspberry Pi 5** (your HA server) | Hub for entities, Alexa integration, Pomodoro helpers, UI mode helpers |
| **Magic Mirror** | **Raspberry Pi 4** (wall display) | Chromium + local backend → talks to **HA over LAN** |

These are **two different Pis**.

---

## MCP (Cursor on your dev machine)

- You have an **MCP server** configured against **HA** on the Pi 5.
- Use it to **inspect entities**, **test services**, and **validate** automations while editing this repo.
- **Never** commit the long-lived token, **never** paste it into markdown or chat logs you might save publicly.

### Where to put the token (Cursor + `ha-mcp`)

On **macOS**, Cursor’s MCP config is usually:

**`~/.cursor/mcp.json`**

Add or edit the server that runs **`ha-mcp`** (often installed via `uvx ha-mcp@latest`). Set **environment variables** there — **not** in the magic-mirror git repo:

| Variable | Value |
|----------|--------|
| `HOMEASSISTANT_URL` | Your HA base URL, e.g. `http://<pi5-hostname-or-ip>:8123` (use `https://` if you terminate TLS) |
| `HOMEASSISTANT_TOKEN` | Long-lived token from HA → **Profile** (user menu) → **Security** → **Long-lived access tokens** |

Alternatively: **Cursor Settings → MCP** and configure the same server/env in the UI (Cursor writes `mcp.json`).

After saving, **restart Cursor** or reload MCP so the new token is picked up.

**Safer patterns**

- Keep tokens **only** in `~/.cursor/mcp.json` (or UI equivalent) / a **gitignored** `.env` — never in this repo.
- In repo: only **`.env.example`** with empty `HA_URL=` and `HA_TOKEN=` placeholders if needed for scripts later.

---

## Mirror Pi runtime (entity IDs & ICS)

Do not guess IDs in code: see **[MIRROR_RUNTIME.md](MIRROR_RUNTIME.md)** and [config/mirror.runtime.example.yaml](../config/mirror.runtime.example.yaml) for **`weather.pirateweather`**, **`todo.elliot`**, school ICS URLs, and token file layout on the **mirror Pi 4**.

---

## Tokens (two contexts)

| Context | Where token lives | Purpose |
|---------|-------------------|---------|
| **Dev (MCP / laptop)** | Your machine / MCP config | Explore HA while building |
| **Mirror Pi 4 runtime** | On the mirror Pi only (`chmod 600`) | Backend subscribes to HA WebSocket for the kiosk UI |

Use **separate** long-lived tokens if HA allows (recommended): one scoped for dev, one for mirror **least privilege**.

---

## SD card (mirror Pi 4)

- **32 GB Lexar SDHC** is acceptable; flash **Raspberry Pi OS** when you start bring-up (see **`mm-kiosk-pi`** skill).
- HA **stays** on the Pi 5; no need to move HA to the mirror Pi.

---

## References

- [Home Assistant — Authentication](https://developers.home-assistant.io/docs/auth_api#long-lived-access-token)
- Skill **`mm-dev-mcp-ha`** — MCP is **not** used on the mirror Pi at runtime.
- [GITHUB.md](GITHUB.md) — what must not be committed.
