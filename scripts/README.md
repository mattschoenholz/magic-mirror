# Scripts

| Script | Where it runs | Purpose |
|--------|----------------|--------|
| [pi-mirror-stub.sh](pi-mirror-stub.sh) | **Mirror Pi 4** | Create `~/mirror-stub/index.html` and optionally open **Chromium kiosk** to verify resolution (especially **portrait** viewport). |

Copy to the Pi from your Mac:

```bash
scp scripts/pi-mirror-stub.sh USER@mirror-pi4.local:~/
ssh USER@mirror-pi4.local 'bash ~/pi-mirror-stub.sh --open'
```

See [docs/PI_BRINGUP.md](../docs/PI_BRINGUP.md).
