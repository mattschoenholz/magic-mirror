# Scripts

| Script | Where it runs | Purpose |
|--------|----------------|--------|
| [pi-mirror-stub.sh](pi-mirror-stub.sh) | **Mirror Pi 4** | Create `~/mirror-stub/index.html` and optionally open **Chromium kiosk** to verify resolution (especially **portrait** viewport). |

Copy to the Pi from your Mac (**from the magic-mirror repo root** so `scripts/` exists — `cd` there first). Replace **`your_linux_login`** and **`pi-host`** with your real Pi user and hostname **or** IP (do not leave the words `USER` / `HOST`):

```bash
cd ~/Desktop/CurrentProjects/General/magic-mirror   # change if your clone path differs

scp scripts/pi-mirror-stub.sh your_linux_login@pi-host:~/pi-mirror-stub.sh
ssh your_linux_login@pi-host 'bash ~/pi-mirror-stub.sh --open'
```

**Sanity checks:** `ls scripts/pi-mirror-stub.sh` should succeed before `scp`. If `pi-host.local` fails, use the Pi’s **IP** from your router or `ping mirror-pi4.local`.

See [docs/PI_BRINGUP.md](../docs/PI_BRINGUP.md).
