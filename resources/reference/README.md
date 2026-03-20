# Reference materials

Store **curated** research here so it survives chat sessions and survives onboarding a future you (or a collaborator).

---

## How to use this folder

| Type | Suggested location | Notes |
|------|--------------------|--------|
| **Bookmarks** | `links.md` (create) | Title, one-line summary, URL, date accessed |
| **PDFs / datasheets** | `pdfs/` | AIY HAT, display, Pi power, mirror glass specs |
| **Screenshots** | `images/` | UX inspiration only; no secrets in screenshots |
| **API notes** | `apis.md` | HA endpoints, rate limits, auth headers — **no tokens** |

---

## Starter `links.md` skeleton

Create `links.md` with sections such as:

- Raspberry Pi kiosk / Chromium
- AIY Voice Kit (your revision)
- Home Assistant REST / WebSocket
- **Custom web + HA** (this project — not MagicMirror² for v1); see `.cursor/skills/mm-*`
- Local voice stacks (optional)

Example row:

`| 2026-03-20 | HA WebSocket API | https://... | Dev docs for subscriptions |`

---

## Git

- Prefer **links** over committing large PDFs when licensing/size is unclear.
- If you vendor PDFs, add a one-line **source** comment in `pdfs/README.md`.
