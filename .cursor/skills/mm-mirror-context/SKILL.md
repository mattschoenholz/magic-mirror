---
name: mm-mirror-context
description: >-
  Shared project facts, hardware assumptions, and HA/voice checklists for the
  wall Magic Mirror (Pi 4, AIY Voice HAT, Home Assistant). Read before
  architecture, UX, coding, or test design.
---

# Magic Mirror — context skill

## When to apply

- Any substantial change to architecture, UI, voice, or tests.
- Onboarding a new session on a different machine.

## Instructions

1. Read **`docs/MIRROR_CONTEXT.md`** end-to-end.
2. For **entity IDs, ICS URLs, secrets paths, Spotify/YouTube policy**, read **`docs/MIRROR_RUNTIME.md`** (and `config/mirror.runtime.example.yaml`).
3. Then open the role-specific doc (`docs/FSD.md`, `docs/ARCHITECTURE.md`, etc.) as needed.
4. Load **domain reference skills** when work touches that layer:

| Skill | Use |
|-------|-----|
| **`mm-home-assistant`** | Runtime HA REST/WebSocket, tokens, FR-006 proxy pattern |
| **`mm-kiosk-pi`** | Chromium kiosk, systemd autostart, HDMI/audio on Pi |
| **`mm-voice-aiy-google`** | **Future** — AIY on Pi only if scope returns |
| **`mm-dev-mcp-ha`** | Cursor + HA MCP **only** (never Pi runtime) |

## Stack reminder

**Custom web UI** + **local backend** for HA — **not** MagicMirror². **v1:** **Echo** = all voice; Pi = **display only** (see `docs/ARCHITECTURE.md`).

## Outputs

- Decisions and new facts flow **back** into `docs/MIRROR_CONTEXT.md` or the canonical docs it references — avoid orphan knowledge in chat only.
