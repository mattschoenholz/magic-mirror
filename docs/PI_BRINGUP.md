# Mirror Pi 4 — bring-up (display + network foundation)

Goal: **Pi 4 booting**, **desktop on the Samsung TV**, **known HDMI resolution**, **SSH from your Mac**, **LAN reachability to Home Assistant (Pi 5)**. No mirror app or HA token on the Pi yet — this is the hardware/OS baseline to design and build against.

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
- **User** — not the legacy `pi` user; pick a normal username + strong password (or key-only if you prefer).
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
- If **headless**: wait ~1–2 minutes, then **`ssh youruser@mirror-pi4.local`** (or hostname you set). Use the **same LAN** as the Pi.

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

Planning baseline remains **1280×720** until you confirm the panel actually prefers **1080p** or something else.

---

## 5. End-to-end “something on screen” test

Confirms **Chromium + URL loading** without your final app.

**Option A — Local stub page**

```bash
mkdir -p ~/mirror-stub && printf '%s\n' '<!DOCTYPE html><html><head><meta charset="utf-8"><title>Mirror stub</title></head><body style="background:#111;color:#eee;font-family:sans-serif;text-align:center;padding:2rem;"><h1>Mirror Pi OK</h1><p id="r"></p><script>document.getElementById("r").textContent=innerWidth+" x "+innerHeight;</script></body></html>' > ~/mirror-stub/index.html
chromium --kiosk "file:///home/YOUR_USER/mirror-stub/index.html"
```

Replace **`YOUR_USER`**. You should see **full-screen** page and **innerWidth × innerHeight** (useful for verifying drawable pixels).

Press **Alt+F4** to exit Chromium if stuck in kiosk (or SSH in and `pkill chromium`).

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
