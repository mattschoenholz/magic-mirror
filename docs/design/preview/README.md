# Design preview (mirror + laptop)

Static **gallery** and **fullscreen** viewer for SVG wireframes in the parent [`docs/design/`](../) folder.

## On your Mac (quick)

From the repo root:

```bash
open docs/design/preview/index.html
```

Or in Cursor: right-click `index.html` → Open with Live Server (if you use it). Relative paths require opening the **file** (or serving `docs/design/` below); do not move `preview/` without the SVG siblings in `../`.

## On the mirror Pi (1:1 on glass)

Copy the **whole** `docs/design/` tree so `preview/index.html` keeps valid `../` paths to the SVGs:

```bash
# From repo root on your Mac (host: mirror-pi4.local)
rsync -avz --delete ./docs/design/ pi@mirror-pi4.local:~/mirror-design-preview/
```

### Kiosk by default (no browser chrome)

From your Mac, the helper syncs and opens Chromium in **`--kiosk`** (fullscreen, no toolbars or back button).

**Run from the repo root** (`magic-mirror/`, where the `scripts/` folder lives). If you `cd` into `web/` or `docs/design/preview/`, use `../scripts/…` or `cd` back — otherwise you’ll get **no such file or directory**.

```bash
cd ~/Desktop/CurrentProjects/General/magic-mirror
./scripts/sync-design-preview-to-pi.sh --open
```

- **Gallery** → **Fullscreen** on a card → **`viewer.html`** shows the SVG. **Tap anywhere on the preview** (full-area link over the artboard) to return to the gallery — the bottom **← Gallery** dock is optional if the wood frame hides it.
- **Exit kiosk:** web pages **cannot** close Chromium. Use the bottom **Exit kiosk…** panel (SSH one-liner, **Alt+F4**, or windowed mode below).

**Windowed** (normal browser UI / back button) for debugging:

```bash
PREVIEW_WINDOWED=1 ./scripts/sync-design-preview-to-pi.sh --open
```

### Wood frame / safe inset

The physical frame can cover **~20–30 px** of the LCD. Preview chrome uses **`preview-dock.css`** (`--preview-frame-inset: 36px`). Increase that value if controls sit under the wood. Product UI should follow [tokens.md](../tokens.md) safe-area note.

### Manual Chromium (Pi)

Same flags as the script; add **`--kiosk`** unless you want windowed:

```bash
chromium --password-store=basic --no-sandbox --disable-dev-shm-usage \
  --no-first-run --disable-sync --disable-background-networking \
  --noerrdialogs --disable-infobars --disable-logging --kiosk \
  "file://${HOME}/mirror-design-preview/preview/index.html"
```

## Keyboard

- **Alt+F4** (or `pkill chromium`) to exit kiosk on the Pi.

## Chromium stderr (`Opening:`, `Failed global descriptor lookup`, `DEPRECATED_ENDPOINT`, `GetVSyncParameters…`)

- **`Opening: file://...`** is printed by **this repo’s sync script**, not an error.
- The other lines are common **Chromium noise** on the Pi if the page still appears. See [PI_BRINGUP.md](../../PI_BRINGUP.md) (Chromium stderr on the Pi). **`--disable-logging`** does not silence all of them.
- **Quiet terminal (default):** `sync-design-preview-to-pi.sh --open` runs Chromium with **`stderr` discarded** on the Pi so those three lines do not spam your SSH session. The UI is unchanged.
- **Show Chromium stderr again (debug):** `PREVIEW_KEEP_CHROMIUM_STDERR=1 ./scripts/sync-design-preview-to-pi.sh --open`
