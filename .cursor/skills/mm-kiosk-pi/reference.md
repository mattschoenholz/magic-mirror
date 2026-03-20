# Raspberry Pi kiosk — reference

Stack assumption: **custom web app** opened in **Chromium** (or equivalent) in **kiosk / fullscreen** mode on **Raspberry Pi 4**.

---

## Display

- **Planning resolution:** **1080×1920** portrait (1920×1080 panel rotated). Confirm with `xrandr` / **Screen Configuration** and the [pi-mirror-stub.sh](../../../scripts/pi-mirror-stub.sh) viewport readout.
- Chromium flags commonly used for kiosks (verify for your package):

  ```text
  chromium-browser --kiosk --noerrdialogs --disable-infobars \
    --autoplay-policy=no-user-gesture-required \
    http://127.0.0.1:PORT/
  ```

- **Overscan:** disable in `raspi-config` if the UI is cropped on the TV.

---

## Autostart options (pick one pattern)

| Pattern | Use case |
|---------|----------|
| **`~/.config/autostart/*.desktop`** | Simple user-session start on Desktop-based Pi OS |
| **`systemd` user or system service** | Restart on crash, logging, dependency on network |

Example **sketch** — adjust `User=`, paths, and Exec:

```ini
[Unit]
Description=Magic Mirror Chromium kiosk
After=network-online.target magic-mirror-backend.service
Wants=network-online.target

[Service]
Type=simple
User=pi
Environment=DISPLAY=:0
ExecStart=/usr/bin/chromium-browser --kiosk http://127.0.0.1:8080/
Restart=on-failure
RestartSec=5

[Install]
WantedBy=graphical.target
```

Do not commit **production** unit files with secrets; keep templates in `docs/` or `deploy/` when you add them.

---

## Backend + static UI

Typical split:

1. **Static or built frontend** (HTML/CSS/JS or light framework) — no HA token inside.
2. **Small local server** on loopback — holds HA token, proxies `/api/...` to HA REST/WebSocket as designed in `mm-home-assistant`.

Chromium loads only `http://127.0.0.1:...`.

---

## Audio (reminder)

- List devices: `aplay -l` / PulseAudio or PipeWire UI.
- Align with **`mm-voice-aiy-google`** for mic + TTS output choice (HAT vs HDMI).

---

## Reliability

- Enable **unattended upgrades** policy consciously (some prefer manual for boat/bedroom stability).
- Log rotation for custom services once implemented.
