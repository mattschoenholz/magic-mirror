# Home Assistant — reference for Magic Mirror (runtime)

Official docs (bookmark and re-check for your HA version):

- [REST API](https://developers.home-assistant.io/docs/api/rest)
- [WebSocket API](https://developers.home-assistant.io/docs/api/websocket)
- [Auth — long-lived access tokens](https://developers.home-assistant.io/docs/auth_api#long-lived-access-token)

---

## Security (non-negotiable)

| Rule | Detail |
|------|--------|
| Token storage | On Pi only; file e.g. `/etc/magic-mirror/ha.env` or user-readable `~/.config/...` with **`chmod 600`**; owned by service user |
| Git | Never commit token; `.env.example` lists keys with empty or `REPLACE_ME` |
| Browser | **FR-006:** do not ship token to Chromium. Use a **local backend** (small Node/Python server on localhost) that holds the token and exposes only what the UI needs, or server-rendered snippets |
| Scope | Prefer dedicated HA user + minimal entities exposed via [restrictions](https://www.home-assistant.io/docs/authentication/) where your version allows |

---

## REST (basics)

- Base URL: `http(s)://<ha-host>:8123` (or your internal hostname).
- Header: `Authorization: Bearer <LONG_LIVED_TOKEN>`  
- `Content-Type: application/json` for POST bodies.
- Common calls:
  - `GET /api/` — sanity check
  - `GET /api/states` — all states (heavy; prefer WebSocket + targeted entities for refresh)
  - `GET /api/states/<entity_id>`
  - `POST /api/services/<domain>/<service>` — JSON body with `entity_id` / `target` per service docs

Use REST for **one-shot** actions; use WebSocket for **live** updates.

---

## WebSocket (pattern)

1. Connect to `ws(s)://<ha-host>:8123/api/websocket`.
2. Server sends `type: auth_required` with `ha_version`.
3. Send `{"type":"auth","access_token":"<token>"}`.
4. On `auth_ok`, subscribe to updates:
   - Listen for **`state_changed`** events and filter client-side by `entity_id`, **or**
   - Use documented subscribe patterns for your HA version (see WebSocket doc index for `subscribe_events` / entity filters).

Implement **exponential backoff** on disconnect and a **visible UI state** (“Home Assistant unreachable”) per Architecture.

---

## Mirror-specific checklist

- [ ] List **entity_ids** for v1 modules in `docs/ARCHITECTURE.md` (templates only).
- [ ] Whitelist **service domains** the mirror may call (voice + any UI actions).
- [ ] Define behavior when HA returns 401 (token rotated) — ops note to refresh token.
- [ ] Rate-limit or debounce UI updates if many entities fire at once.

---

## Testing (Tester agent)

- With HA dev tools / logs: confirm service calls match FSD whitelist.
- Disconnect LAN to Pi or stop HA container: mirror shows defined degraded state within **TBD** seconds (set in FSD).
