#!/usr/bin/env bash
# Install systemd timers to blank the HDMI output nightly (local wall clock) and restore in the morning.
# Requires the Pi system timezone to match your home (e.g. timedatectl set-timezone America/Los_Angeles).
#
# Env (optional):
#   MIRROR_APP_DIR       — default ~/mirror-app
#   MIRROR_SLEEP_OFF     — "HH:MM" default 23:00
#   MIRROR_SLEEP_ON      — "HH:MM" default 06:00
#   MIRROR_SLEEP_PROFILE — instant | both (default: instant)
#     instant = CEC TV standby only; kiosk keeps running; fast wake (see MIRROR_RUNTIME.md §8)
#     both    = stop kiosk + wlr-randr + vcgencmd + CEC (harder blank, slower wake)
#
set -euo pipefail

APP_DIR="${MIRROR_APP_DIR:-$HOME/mirror-app}"
SCRIPT="${APP_DIR}/scripts/pi-display-sleep.sh"
SERVICE_DIR="/etc/systemd/system"
OFF_SVC="${SERVICE_DIR}/mirror-display-sleep-off.service"
ON_SVC="${SERVICE_DIR}/mirror-display-sleep-on.service"
OFF_TIMER="${SERVICE_DIR}/mirror-display-sleep-off.timer"
ON_TIMER="${SERVICE_DIR}/mirror-display-sleep-on.timer"
ENV_FILE="${SERVICE_DIR}/mirror-display-sleep.env"

MIRROR_SLEEP_OFF="${MIRROR_SLEEP_OFF:-23:00}"
MIRROR_SLEEP_ON="${MIRROR_SLEEP_ON:-06:00}"
PROFILE="${MIRROR_SLEEP_PROFILE:-instant}"

case "$PROFILE" in
  instant)
    METHOD=cec
    STOP_KIOSK=0
    USE_WLR=0
    ;;
  both)
    METHOD=both
    STOP_KIOSK=1
    USE_WLR=1
    ;;
  *)
    echo "MIRROR_SLEEP_PROFILE must be 'instant' or 'both' (got: $PROFILE)" >&2
    exit 1
    ;;
esac

if ! command -v sudo >/dev/null 2>&1; then
  echo "sudo is required." >&2
  exit 1
fi

if [[ ! -x "$SCRIPT" ]]; then
  echo "Missing executable $SCRIPT — deploy the repo to the Pi first." >&2
  exit 1
fi

if [[ "$METHOD" == "cec" || "$METHOD" == "both" ]] && ! command -v cec-client >/dev/null 2>&1; then
  echo "WARN: method uses CEC but cec-client missing." >&2
  echo "      Install: sudo apt-get install -y cec-utils" >&2
fi

parse_hhmm() {
  local s="$1"
  if [[ "$s" =~ ^([0-1]?[0-9]|2[0-3]):([0-5][0-9])$ ]]; then
    local h m
    h=$((10#${BASH_REMATCH[1]}))
    m=$((10#${BASH_REMATCH[2]}))
    printf '%02d:%02d' "$h" "$m"
    return 0
  fi
  echo "Invalid time (use HH:MM 24h): $s" >&2
  return 1
}

OFF_CAL="$(parse_hhmm "$MIRROR_SLEEP_OFF")" || exit 1
ON_CAL="$(parse_hhmm "$MIRROR_SLEEP_ON")" || exit 1
IFS=: read -r OFF_H OFF_M <<<"$OFF_CAL"
IFS=: read -r ON_H ON_M <<<"$ON_CAL"

echo "Using profile=${PROFILE}  schedule OFF ${OFF_H}:${OFF_M}  ON ${ON_H}:${OFF_M}  method=${METHOD}  STOP_KIOSK=${STOP_KIOSK}  USE_WLR=${USE_WLR}"
if command -v timedatectl >/dev/null 2>&1; then
  timedatectl status --no-pager | sed -n '1,6p' || true
fi

echo "Installing ${ENV_FILE}"
sudo tee "$ENV_FILE" >/dev/null <<EOF
# Managed by install-pi-display-sleep-schedule.sh
# MIRROR_SLEEP_PROFILE=${PROFILE}
MIRROR_DISPLAY_SLEEP_METHOD=${METHOD}
MIRROR_DISPLAY_SLEEP_STOP_KIOSK=${STOP_KIOSK}
MIRROR_DISPLAY_SLEEP_USE_WLR=${USE_WLR}
# If CEC scan shows no TV, try the other HDMI: MIRROR_CEC_DEVICE=/dev/cec1
#
# Harder blank (stop kiosk + Wayland + vcgencmd + CEC): reinstall with
#   MIRROR_SLEEP_PROFILE=both ${APP_DIR}/scripts/install-pi-display-sleep-schedule.sh
# or set METHOD=both, STOP_KIOSK=1, USE_WLR=1 by hand.
EOF
sudo chmod 644 "$ENV_FILE"

echo "Installing ${OFF_SVC}"
sudo tee "$OFF_SVC" >/dev/null <<EOF
[Unit]
Description=Magic Mirror — display sleep (off)

[Service]
Type=oneshot
EnvironmentFile=-${ENV_FILE}
ExecStart=${SCRIPT} off
EOF

echo "Installing ${ON_SVC}"
sudo tee "$ON_SVC" >/dev/null <<EOF
[Unit]
Description=Magic Mirror — display wake (on)

[Service]
Type=oneshot
EnvironmentFile=-${ENV_FILE}
ExecStart=${SCRIPT} on
EOF

echo "Installing ${OFF_TIMER}"
sudo tee "$OFF_TIMER" >/dev/null <<EOF
[Unit]
Description=Magic Mirror — nightly display off timer

[Timer]
OnCalendar=*-*-* ${OFF_H}:${OFF_M}:00
Persistent=true

[Install]
WantedBy=timers.target
EOF

echo "Installing ${ON_TIMER}"
sudo tee "$ON_TIMER" >/dev/null <<EOF
[Unit]
Description=Magic Mirror — morning display on timer

[Timer]
OnCalendar=*-*-* ${ON_H}:${ON_M}:00
Persistent=true

[Install]
WantedBy=timers.target
EOF

sudo systemctl daemon-reload
sudo systemctl enable mirror-display-sleep-off.timer mirror-display-sleep-on.timer
sudo systemctl start mirror-display-sleep-off.timer mirror-display-sleep-on.timer

echo
echo "Timers enabled. Check:"
echo "  systemctl list-timers 'mirror-display-sleep-*'"
echo "  sudo ${SCRIPT} status"
echo "Test: sudo ${SCRIPT} off   then   sudo ${SCRIPT} on"
