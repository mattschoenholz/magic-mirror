# Scripts

| Script | Where it runs | Purpose |
|--------|----------------|--------|
| [install-pi-autostart.sh](install-pi-autostart.sh) | **Mirror Pi 4** | Install + enable systemd services so backend + Chromium kiosk recover automatically after reboot/power loss. |
| [pi-launch-kiosk.sh](pi-launch-kiosk.sh) | **Mirror Pi 4** | Chromium launcher used by `mirror-kiosk.service` (waits for display, starts kiosk URL). |
| [pi-mirror-stub.sh](pi-mirror-stub.sh) | **Mirror Pi 4** | Create `~/mirror-stub/index.html` and optionally open **Chromium kiosk** to verify resolution (especially **portrait** viewport). |
| [pi-display-rotate.sh](pi-display-rotate.sh) | **Mirror Pi 4** | **`xrandr`** over SSH: `list` / `left` / `right` / `normal` for portrait. See [PI_BRINGUP.md](../docs/PI_BRINGUP.md). |
| [sync-design-preview-to-pi.sh](sync-design-preview-to-pi.sh) | **Dev machine → Pi** | `rsync` [docs/design/](../docs/design/) to `~/mirror-design-preview/`; `--open` launches Chromium in **`--kiosk`** (use **`PREVIEW_WINDOWED=1`** for normal window + back button). See [preview/README.md](../docs/design/preview/README.md). |
| [sync-web-to-pi.sh](sync-web-to-pi.sh) | **Dev machine → Pi** | `rsync` [web/](../web/) to `~/mirror-web/`; **`--open`** = `file://` UI (no Pi keyboard); **`--open --http`** = `python3 -m http.server` on Pi + **`http://127.0.0.1:8765/`**. See [web/README.md](../web/README.md). |

Copy to the Pi from your Mac (**from the magic-mirror repo root** so `scripts/` exists — `cd` there first). Deploy/sync scripts default to **`pi@mirror-pi4.local`**; use **`export PI=pi@<ip>`** if mDNS does not resolve.

```bash
cd ~/Desktop/CurrentProjects/General/magic-mirror   # change if your clone path differs

scp scripts/pi-mirror-stub.sh pi@mirror-pi4.local:~/pi-mirror-stub.sh
ssh pi@mirror-pi4.local 'bash ~/pi-mirror-stub.sh --open'
```

**Sanity checks:** `ls scripts/pi-mirror-stub.sh` should succeed before `scp`. Example with IP: `pi@192.168.1.50`.

See [docs/PI_BRINGUP.md](../docs/PI_BRINGUP.md). **SSH-only:** Chromium needs extra flags — see bring-up doc.
