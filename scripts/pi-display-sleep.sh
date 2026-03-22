#!/usr/bin/env bash
# Turn the mirror "screen" off/on on a Raspberry Pi.
#
# Default method: HDMI output power via vcgencmd (no extra packages). Works even if the TV
# ignores CEC; the panel usually shows black / no-signal until morning.
#
# Optional: MIRROR_DISPLAY_SLEEP_METHOD=cec|both — use cec-utils (cec-client) to ask the TV
# to standby/wake over HDMI-CEC (Samsung Anynet+ must be on). May require sudo for /dev/cec0.
#
# Usage: pi-display-sleep.sh off | on | status
#
# If mirror-kiosk.service is installed (systemd Chromium), it must be stopped before HDMI
# blanking — otherwise Chromium/Wayland can turn the panel back on within seconds
# (Restart=always + DRM repaint). Set MIRROR_DISPLAY_SLEEP_STOP_KIOSK=0 to skip.
set -euo pipefail

METHOD="${MIRROR_DISPLAY_SLEEP_METHOD:-both}"

stop_mirror_kiosk_if_configured() {
  [[ "${MIRROR_DISPLAY_SLEEP_STOP_KIOSK:-1}" != "1" ]] && return 0
  if ! command -v systemctl >/dev/null 2>&1; then
    return 0
  fi
  if systemctl cat mirror-kiosk.service &>/dev/null; then
    systemctl stop mirror-kiosk.service || true
    echo "Stopped mirror-kiosk.service (so HDMI blank can stick)."
  fi
}

start_mirror_kiosk_if_configured() {
  [[ "${MIRROR_DISPLAY_SLEEP_STOP_KIOSK:-1}" != "1" ]] && return 0
  if ! command -v systemctl >/dev/null 2>&1; then
    return 0
  fi
  if systemctl cat mirror-kiosk.service &>/dev/null; then
    systemctl start mirror-kiosk.service || true
    echo "Started mirror-kiosk.service."
  fi
}

vcgencmd_display_power() {
  local state="$1" # 0 = off, 1 = on
  if ! command -v vcgencmd >/dev/null 2>&1; then
    echo "vcgencmd not found (not a Pi or wrong PATH?)" >&2
    return 1
  fi
  # Preferred: all HDMI outputs (-1 = all). Fallback: primary HDMI (0).
  local out
  if out=$(vcgencmd display_power -1 "$state" 2>&1); then
    echo "$out"
    return 0
  fi
  out=$(vcgencmd display_power 0 "$state" 2>&1) || {
    echo "vcgencmd display_power failed: $out" >&2
    return 1
  }
  echo "$out"
}

cec_standby() {
  if ! command -v cec-client >/dev/null 2>&1; then
    echo "cec-client not installed. Install: sudo apt install -y cec-utils" >&2
    return 1
  fi
  # Device 0 = TV in CEC topology for most setups.
  if echo "standby 0" | cec-client -s -d 1 2>/dev/null; then
    echo "CEC: sent standby to TV (device 0)"
    return 0
  fi
  if sudo -n true 2>/dev/null; then
    echo "standby 0" | sudo cec-client -s -d 1
    echo "CEC: sent standby (via sudo cec-client)"
    return 0
  fi
  echo "CEC standby failed (try: sudo usermod -aG video pi, or run cec-client as root)" >&2
  return 1
}

cec_on() {
  if ! command -v cec-client >/dev/null 2>&1; then
    echo "cec-client not installed." >&2
    return 1
  fi
  if echo "on 0" | cec-client -s -d 1 2>/dev/null; then
    echo "CEC: sent on to TV (device 0)"
    return 0
  fi
  if sudo -n true 2>/dev/null; then
    echo "on 0" | sudo cec-client -s -d 1
    echo "CEC: sent on (via sudo cec-client)"
    return 0
  fi
  echo "CEC on failed" >&2
  return 1
}

ACTION="${1:-}"
case "$ACTION" in
  off|sleep)
    stop_mirror_kiosk_if_configured
    case "$METHOD" in
      hdmi)
        vcgencmd_display_power 0
        ;;
      cec)
        cec_standby || exit 1
        ;;
      both)
        vcgencmd_display_power 0 || true
        cec_standby || true
        ;;
      *)
        echo "Unknown MIRROR_DISPLAY_SLEEP_METHOD=$METHOD (use hdmi|cec|both)" >&2
        exit 1
        ;;
    esac
    ;;
  on|wake)
    case "$METHOD" in
      hdmi)
        vcgencmd_display_power 1
        ;;
      cec)
        cec_on || exit 1
        ;;
      both)
        vcgencmd_display_power 1 || true
        cec_on || true
        ;;
      *)
        echo "Unknown MIRROR_DISPLAY_SLEEP_METHOD=$METHOD (use hdmi|cec|both)" >&2
        exit 1
        ;;
    esac
    start_mirror_kiosk_if_configured
    ;;
  status)
    if command -v vcgencmd >/dev/null 2>&1; then
      vcgencmd display_power
    else
      echo "vcgencmd not available"
    fi
    ;;
  *)
    echo "Usage: $0 off|on|status" >&2
    echo "  MIRROR_DISPLAY_SLEEP_METHOD=hdmi|cec|both  (default: both)" >&2
    echo "  MIRROR_DISPLAY_SLEEP_STOP_KIOSK=0 to not stop/start mirror-kiosk.service" >&2
    exit 1
    ;;
esac
