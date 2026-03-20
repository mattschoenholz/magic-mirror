# Scripts

| Script | Where it runs | Purpose |
|--------|----------------|--------|
| [pi-mirror-stub.sh](pi-mirror-stub.sh) | **Mirror Pi 4** | Create `~/mirror-stub/index.html` and optionally open **Chromium kiosk** to verify resolution (especially **portrait** viewport). |
| [pi-display-rotate.sh](pi-display-rotate.sh) | **Mirror Pi 4** | **`xrandr`** over SSH: `list` / `left` / `right` / `normal` for portrait. See [PI_BRINGUP.md](../docs/PI_BRINGUP.md). |

Copy to the Pi from your Mac (**from the magic-mirror repo root** so `scripts/` exists — `cd` there first). Examples use user **`pi`** and hostname **`mirror-pi4.local`**; swap in your Pi’s **IP** if `.local` fails.

```bash
cd ~/Desktop/CurrentProjects/General/magic-mirror   # change if your clone path differs

scp scripts/pi-mirror-stub.sh pi@mirror-pi4.local:~/pi-mirror-stub.sh
ssh pi@mirror-pi4.local 'bash ~/pi-mirror-stub.sh --open'
```

**Sanity checks:** `ls scripts/pi-mirror-stub.sh` should succeed before `scp`. Example with IP: `pi@192.168.1.50`.

See [docs/PI_BRINGUP.md](../docs/PI_BRINGUP.md). **SSH-only:** Chromium needs extra flags — see bring-up doc; optional boot autostart: [mirror-stub.desktop.example](mirror-stub.desktop.example).
