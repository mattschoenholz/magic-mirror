#!/usr/bin/env bash
# Turn the mirror "screen" off/on on a Raspberry Pi.
#
# Default method: HDMI output power via vcgencmd (no extra packages). Works even if the TV
# ignores CEC; the panel usually shows black / no-signal until morning.
#
# Optional: MIRROR_DISPLAY_SLEEP_METHOD=cec|both — use cec-utils (cec-client) to ask the TV
# to standby/wake over HDMI-CEC (Samsung Anynet+ must be on). May require sudo for /dev/cec0.
#
# Usage: pi-display-sleep.sh off | on | status | cec-scan
#
# Wayland (labwc): if wlr-randr is available, we also disable the HDMI output as user `pi`
# (MIRROR_DISPLAY_SLEEP_USE_WLR=1, default). This often darkens the TV when CEC sees no TV.
#
# If mirror-kiosk.service is installed (systemd Chromium), it must be stopped before HDMI
# blanking — otherwise Chromium/Wayland can turn the panel back on within seconds
# (Restart=always + DRM repaint). Set MIRROR_DISPLAY_SLEEP_STOP_KIOSK=0 to skip.
set -euo pipefail

METHOD="${MIRROR_DISPLAY_SLEEP_METHOD:-both}"
CEC_DEV="${MIRROR_CEC_DEVICE:-}"
WLR_OUT="${MIRROR_WLR_OUTPUT:-HDMI-A-1}"

run_cec_pipe() {
  local pipe="$1"
  if [[ -n "$CEC_DEV" ]]; then
    echo "$pipe" | cec-client "$CEC_DEV" -s -d 1 2>/dev/null && return 0
    echo "$pipe" | sudo cec-client "$CEC_DEV" -s -d 1 && return 0
  else
    echo "$pipe" | cec-client -s -d 1 2>/dev/null && return 0
    echo "$pipe" | sudo cec-client -s -d 1 && return 0
  fi
  return 1
}

wlr_randr_as_pi() {
  local wlr_args=("$@")
  command -v wlr-randr >/dev/null 2>&1 || return 0
  id pi &>/dev/null || return 0
  local uid run
  uid=$(id -u pi)
  run="/run/user/${uid}"
  [[ -d "$run" ]] || return 0
  sudo -u pi env DISPLAY=:0 XAUTHORITY=/home/pi/.Xauthority XDG_RUNTIME_DIR="$run" \
    wlr-randr "${wlr_args[@]}" 2>/dev/null
}

wayland_output_off() {
  [[ "${MIRROR_DISPLAY_SLEEP_USE_WLR:-1}" != "1" ]] && return 0
  wlr_randr_as_pi --output "$WLR_OUT" --off && echo "wlr-randr: output $WLR_OUT off (Wayland)."
}

wayland_output_on() {
  [[ "${MIRROR_DISPLAY_SLEEP_USE_WLR:-1}" != "1" ]] && return 0
  if wlr_randr_as_pi --output "$WLR_OUT" --on --preferred; then
    echo "wlr-randr: output $WLR_OUT on (Wayland)."
  fi
}

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
  if run_cec_pipe "standby 0"; then
    echo "CEC: sent standby to TV (device 0)${CEC_DEV:+ on $CEC_DEV}"
    return 0
  fi
  echo "CEC standby failed (TV may be missing from CEC bus — run: $0 cec-scan)" >&2
  return 1
}

cec_on() {
  if ! command -v cec-client >/dev/null 2>&1; then
    echo "cec-client not installed." >&2
    return 1
  fi
  if run_cec_pipe "on 0"; then
    echo "CEC: sent on to TV (device 0)${CEC_DEV:+ on $CEC_DEV}"
    return 0
  fi
  echo "CEC on failed" >&2
  return 1
}

ACTION="${1:-}"
case "$ACTION" in
  off|sleep)
    stop_mirror_kiosk_if_configured
    wayland_output_off
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
    wayland_output_on
    start_mirror_kiosk_if_configured
    ;;
  cec-scan)
    if ! command -v cec-client >/dev/null 2>&1; then
      echo "cec-client not installed." >&2
      exit 1
    fi
    for dev in /dev/cec0 /dev/cec1; do
      [[ -e "$dev" ]] || continue
      echo "=== scan $dev ==="
      echo scan | sudo cec-client "$dev" -s -d 3 2>&1 | tail -30
    done
    echo "If you only see 'Recorder 1' (the Pi), the TV is not on the CEC bus — check Anynet+, HDMI port (Pi HDMI0), and cable CEC pin."
    exit 0
    ;;
  status)
    if command -v vcgencmd >/dev/null 2>&1; then
      vcgencmd display_power
    else
      echo "vcgencmd not available"
    fi
    ;;
  *)
    echo "Usage: $0 off|on|status|cec-scan" >&2
    echo "  MIRROR_DISPLAY_SLEEP_METHOD=hdmi|cec|both  (default: both)" >&2
    echo "  MIRROR_DISPLAY_SLEEP_STOP_KIOSK=0 to not stop/start mirror-kiosk.service" >&2
    echo "  MIRROR_CEC_DEVICE=/dev/cec0|/dev/cec1  MIRROR_WLR_OUTPUT=HDMI-A-1" >&2
    echo "  MIRROR_DISPLAY_SLEEP_USE_WLR=0 to skip wlr-randr" >&2
    exit 1
    ;;
esac
