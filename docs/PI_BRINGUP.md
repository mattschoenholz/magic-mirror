# Mirror Pi 4 — bring-up (display + network foundation)

Goal: **Pi 4 booting**, **desktop on the Samsung TV**, **known HDMI resolution** (including **portrait** if the glass/TV is mounted vertically), **SSH from your Mac**, **LAN reachability to Home Assistant (Pi 5)**. No mirror app or HA token on the Pi yet — this is the hardware/OS baseline to design and build against.

See also: **`.cursor/skills/mm-kiosk-pi/reference.md`**, [PROJECT_BRIEF.md](PROJECT_BRIEF.md), [HA_DEV.md](HA_DEV.md).

---

## 1. What to flash

| Choice | Why |
|--------|-----|
| **Raspberry Pi OS (64-bit) with desktop** | You need a **GUI + Chromium** later; simplest path for HDMI verification. |
| **Not** Lite (for this phase) | Lite has no desktop; you’d add a window manager before you can sanely test the TV. |

Use **Raspberry Pi Imager** (Mac): select **Pi 4**, OS above, your **32 GB** card.

**Imager OS customization (gear icon)** — set before write:

- **Hostname** — e.g. `mirror-pi4` (or your convention).
- **SSH** — enable; **public key** preferred (paste your Mac `~/.ssh/id_ed25519.pub`).
- **User** — whatever you set in Imager (yours is **`pi`**). Use a strong password (or SSH keys).
- **Wi‑Fi** — only if the mirror will use wireless; **Ethernet is preferable** for a wall-mounted display if you can run a cable.

Write the image, eject safely, install SD in the Pi.

---

## 2. Physical hookup (first boot)

1. **HDMI** from Pi → **TV** (the input you’ll use behind the mirror). Try the **HDMI0** port closest to the USB-C power on the Pi 4 first if you get no signal.
2. **Power** Pi separately from TV (your brief: TV has its own **120 V** feed).
3. Turn the **TV on** and select the correct **HDMI input** before or right after powering the Pi.
4. **Ethernet** to the same LAN as the **HA Pi 5** (recommended).

**Black screen / no signal**

- Unplug/replug HDMI after boot; some TVs need a **hotplug** to negotiate.
- On another machine, edit **`/boot/firmware/config.txt`** on the SD card (or via SSH after first successful boot) and add or uncomment helpers such as:
  - `hdmi_force_hotplug=1`
  - If still wrong mode, force a mode (last resort — look up `hdmi_group` / `hdmi_mode` for your target, e.g. **CEA 720p**).
- **Overscan:** if the picture is **cropped**, use **Raspberry Pi OS** → **Preferences → Raspberry Pi Configuration → Display** (or **Screen Configuration**) and disable overscan / adjust; see [mm-kiosk-pi reference](../.cursor/skills/mm-kiosk-pi/reference.md).

---

## 3. First login

- If **keyboard + mouse** are connected: complete wizard (locale, updates prompt, etc.).
- If **headless**: wait ~1–2 minutes, then **`ssh pi@mirror-pi4.local`** (or `pi@<ip>` — use your hostname if different). Same LAN as the Pi.

Update the system:

```bash
sudo apt update && sudo apt full-upgrade -y
sudo reboot
```

---

## 4. Record display facts (for FSD / UX)

On the Pi **with desktop**:

1. **Preferences → Screen Configuration** (or **Display Settings** on your OS build) — note **resolution** and **refresh** reported for the TV.
2. Optional terminal (X11 session):

   ```bash
   xrandr
   ```

3. **Write these into** [PROJECT_BRIEF.md](PROJECT_BRIEF.md) inventory / “still to fill”: **Samsung model**, **native / negotiated resolution**, **Pi RAM** (`free -h`).

**Confirmed example (your rig):** panel negotiates **1920×1080**; mirror is **portrait** — after rotation, the browser **viewport** is typically **1080×1920** CSS pixels (short side horizontal, long side vertical). Use the **stub** below to read the exact numbers.

### Portrait orientation (match physical mount)

If the TV is mounted **vertically**, set rotation in software so text is upright (not “sideways landscape”).

**Success check:** reload the **stub** in Chromium. The readout should become **1080 × 1920** (tall portrait). If you still see **1920 × 1080**, the desktop is still **landscape** — rotation has not been applied (or Wayland is ignoring `xrandr`).

1. **GUI:** **Preferences → Screen Configuration** — HDMI → **90° Left** / **90° Right** until upright; **Apply** and save if offered.
2. **SSH + X11 (`xrandr`)** — same graphics session as Chromium (`DISPLAY=:0`). Use the helper script (copy via `scp` from [pi-display-rotate.sh](../scripts/pi-display-rotate.sh)):

   ```bash
   bash ~/pi-display-rotate.sh list
   bash ~/pi-display-rotate.sh left      # 90° CCW from default landscape
   bash ~/pi-display-rotate.sh right     # 90° CW from default landscape
   ```

   If the picture is wrong, run **`normal`** then try the **other** direction. To target a specific output from `list`:

   `bash ~/pi-display-rotate.sh left HDMI-2`

3. **Persist across reboot (firmware)** — after **`left`** or **`right`** looks correct, add **one** line under **`[all]`** in **`/boot/firmware/config.txt`** (then `sudo reboot`):

   | Value | Effect |
   |-------|--------|
   | `display_hdmi_rotate=0` | No firmware rotation (default) |
   | `display_hdmi_rotate=1` | 90° **clockwise** |
   | `display_hdmi_rotate=2` | 180° |
   | `display_hdmi_rotate=3` | 270° **clockwise** (= 90° **counter‑clockwise** from default landscape) |

   Map by trial: **`xrandr` `left`** often lines up with **`display_hdmi_rotate=3`**, and **`xrandr` `right`** with **`=1`** — confirm on your TV before locking in.

4. **Wayland-only session:** if **`xrandr`** errors or rotation does nothing, use **Screen Configuration** when you can attach input, or see Raspberry Pi docs for **labwc/wayfire** output rotation on Bookworm.

**Chromium kiosk** follows the rotated desktop; the stub should read **1080 × 1920** when portrait is correct.

---

## 5. End-to-end “something on screen” test (stub Chromium)

**What “stub Chromium” means:** a **minimal local HTML file** (no server required) opened with **`chromium --kiosk`**. It shows a short message and **live `innerWidth × innerHeight`** so you know the **real drawable area** in CSS pixels (critical for **portrait** and for later UI design). It is **not** the real mirror app — just a display/network smoke test.

**I can’t run this for you:** the AI environment has **no SSH access** to your Pi. One copy-paste path from your **Mac** (repo folder = magic-mirror):

```bash
# On your Mac: cd into the magic-mirror repo first (so scripts/ exists).
# User is **pi**; replace **mirror-pi4.local** with your Pi hostname or IP if different.

cd ~/Desktop/CurrentProjects/General/magic-mirror

scp scripts/pi-mirror-stub.sh pi@mirror-pi4.local:~/pi-mirror-stub.sh
ssh pi@mirror-pi4.local 'bash ~/pi-mirror-stub.sh --open'
```

That creates **`~/mirror-stub/index.html`** on the Pi and launches kiosk. The script sets **`DISPLAY=:0`** when you use SSH so Chromium targets the **HDMI desktop** (remote shells have no display by default).

**SSH only (no keyboard/mouse on the Pi)** — remote shells lack a display, and Chromium’s **sandbox** often breaks when started from **sshd** (e.g. `Failed global descriptor lookup`). Use the **full environment + flags** below (stub page only; **`--no-sandbox`** is for this local test, not general browsing):

**On the Pi** (interactive SSH session as `pi` — `ssh pi@…` then paste):

```bash
export DISPLAY=:0
export XAUTHORITY="$HOME/.Xauthority"
export XDG_RUNTIME_DIR="/run/user/$(id -u)"
chromium \
  --no-sandbox --disable-dev-shm-usage \
  --kiosk --noerrdialogs --disable-infobars \
  "file:///home/pi/mirror-stub/index.html"
```

**One shot from your Mac** (single command; replace host):

```bash
ssh pi@YOUR_PI_HOST 'export DISPLAY=:0 XAUTHORITY=$HOME/.Xauthority XDG_RUNTIME_DIR=/run/user/$(id -u); chromium --no-sandbox --disable-dev-shm-usage --kiosk --noerrdialogs --disable-infobars "file:///home/pi/mirror-stub/index.html"'
```

If `XDG_RUNTIME_DIR` is wrong, run `ls /run/user` on the Pi and use the numeric directory that matches **`id -u`** for `pi`.

Updated **`pi-mirror-stub.sh`** applies **`--no-sandbox`** and **`--disable-dev-shm-usage`** automatically when **`SSH_CONNECTION`** is set (i.e. you ran `bash ~/pi-mirror-stub.sh --open` over SSH).

**Autostart (optional):** if you want the stub every boot without SSH, add a **`.desktop`** file under **`~/.config/autostart/`** on the Pi with an `Exec=` line like the desktop case (you can omit **`--no-sandbox`** when the app is started by the graphical session). Example: [mirror-stub.desktop.example](../scripts/mirror-stub.desktop.example).

**Exit kiosk:** **Alt+F4**, or SSH: `pkill chromium` (or `pkill -f chromium`).

**Option — run only on the Pi** (if you already copied the repo or the script):

```bash
bash ~/pi-mirror-stub.sh          # create files only; prints the chromium command
bash ~/pi-mirror-stub.sh --open   # create + kiosk
```

If Chromium is missing: `sudo apt install -y chromium`

**Option B — Reach HA in browser (read-only sanity)**

```bash
chromium --kiosk "http://YOUR_HA_IP:8123"
```

Use the **IP** that works from the Pi (`ping` first). You only need to see the HA login page to prove **network + display**; **do not** leave HA credentials in kiosk mode for unattended use until you have the real mirror app.

---

## 6. Network check to Home Assistant

From the Pi:

```bash
ping -c 3 YOUR_HA_IP_OR_HOST
curl -sS -o /dev/null -w "%{http_code}\n" http://YOUR_HA_IP:8123/
```

Expect **200** or **302** (redirect to login) — not timeout. If **`homeassistant.local`** fails here but **IP** works, prefer **IP** or **/etc/hosts** on the Pi for production reliability (same idea as [HA_DEV.md](HA_DEV.md) for MCP).

---

## 7. Optional: static IP or DHCP reservation

For stable URLs and firewall rules, reserve **DHCP** on your router for the Pi’s MAC, or set a static IPv4 on the Pi (match your LAN scheme). Document the chosen address in your personal runbook (not in git with secrets).

---

## 8. What’s *not* in this doc yet

- **systemd** kiosk unit and **magic-mirror-backend** (comes with app implementation).
- **HA long-lived token** on the Pi — only after backend exists; file perms **600**, never in git ([MIRROR_CONTEXT.md](MIRROR_CONTEXT.md)).

---

## Checklist (copy to your notes)

- [ ] Imager: **64-bit Desktop**, SSH, user, hostname
- [ ] HDMI picture on Samsung; overscan acceptable
- [ ] Resolution + **innerWidth/height** from stub recorded
- [ ] **PROJECT_BRIEF** updated: TV model, res, Pi RAM
- [ ] **ping/curl** to HA Pi 5 succeeds
- [ ] Reboot test: Pi comes back with display OK

When this is green, **Phase 0 (baseline)** in [MIRROR_CONTEXT.md](MIRROR_CONTEXT.md) is essentially done and you can proceed to design + backend slices with confidence.
