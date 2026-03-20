---
name: mm-kiosk-pi
description: >-
  Raspberry Pi 4 kiosk: Chromium fullscreen, autostart, systemd, display and
  audio gotchas for the wall Magic Mirror. Use for OS-level bring-up and ops.
---

# Magic Mirror — Raspberry Pi kiosk

## When to apply

- First boot path: **GUI loads mirror UI full screen** without login.
- Autostart, crash restart, HDMI resolution, or audio default device.

## Instructions

1. First-time display/OS path: **`docs/PI_BRINGUP.md`**.
2. Read **`docs/MIRROR_CONTEXT.md`** (720p planning baseline until TV native res known).
3. Follow **[reference.md](reference.md)**; adapt commands to **Raspberry Pi OS** version you install.
4. Mirror **app** is **custom web UI** + local backend for HA (see `docs/ARCHITECTURE.md`) — not MagicMirror².

## Outputs

- `systemd` unit examples (in repo **without** secrets), README runbook updates, Architect decision rows for OS variant (Lite + WM vs Desktop).
