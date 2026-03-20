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

**Safer patterns**

- Store the token in **Cursor MCP server config** (local only) or a **`.env`** file that is **gitignored**.
- In repo: only **`.env.example`** with empty `HA_URL=` and `HA_TOKEN=` placeholders if needed for scripts later.

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
