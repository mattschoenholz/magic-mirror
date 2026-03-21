#!/usr/bin/env bash
# Run on the mirror Pi: launch Chromium kiosk against mirror backend URL.
# Intended for systemd use after power loss / reboot recovery.
set -euo pipefail

URL="${1:-http://127.0.0.1:8780/}"
DISPLAY_NUM="${DISPLAY:-:0}"
export DISPLAY="$DISPLAY_NUM"
export XAUTHORITY="${XAUTHORITY:-$HOME/.Xauthority}"
if [[ -d "/run/user/$(id -u)" ]]; then
  export XDG_RUNTIME_DIR="${XDG_RUNTIME_DIR:-/run/user/$(id -u)}"
fi

chromium_bin() {
  if command -v chromium >/dev/null 2>&1; then
    echo "chromium"
    return
  fi
  if command -v chromium-browser >/dev/null 2>&1; then
    echo "chromium-browser"
    return
  fi
  echo ""
}

CHROME="$(chromium_bin)"
if [[ -z "$CHROME" ]]; then
  echo "No chromium binary found in PATH" >&2
  exit 1
fi

# Wait for local X session if boot is still bringing up desktop.
for _ in $(seq 1 60); do
  if [[ -S "/tmp/.X11-unix/${DISPLAY_NUM#:}" ]]; then
    break
  fi
  sleep 1
done

exec "$CHROME" \
  --password-store=basic \
  --kiosk --noerrdialogs --disable-infobars \
  --disable-dev-shm-usage \
  --no-first-run --disable-sync --disable-background-networking \
  --disable-logging \
  "$URL"
