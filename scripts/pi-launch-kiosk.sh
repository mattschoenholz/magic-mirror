#!/usr/bin/env bash
# Run on the mirror Pi: launch Chromium kiosk against mirror backend URL.
# Intended for systemd use after power loss / reboot recovery.
# Supports Wayland (labwc) and X11.
set -euo pipefail

URL="${1:-http://127.0.0.1:8780/}"
UID_NUM="$(id -u)"
export XDG_RUNTIME_DIR="${XDG_RUNTIME_DIR:-/run/user/${UID_NUM}}"

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

# Wait for Wayland or X11 display to be ready (up to 60s).
for _ in $(seq 1 60); do
  if [[ -S "${XDG_RUNTIME_DIR}/wayland-0" ]] || [[ -S "/tmp/.X11-unix/X0" ]]; then
    break
  fi
  sleep 1
done

# Clear Chromium disk cache so CSS/JS changes are always picked up on restart.
rm -rf "${HOME}/.config/chromium/Default/Cache" \
       "${HOME}/.config/chromium/Default/Code Cache" \
       "${HOME}/.config/chromium/Default/GPUCache" 2>/dev/null || true

# Prefer Wayland; fall back to X11.
if [[ -S "${XDG_RUNTIME_DIR}/wayland-0" ]]; then
  export WAYLAND_DISPLAY="wayland-0"
  OZONE_FLAGS="--ozone-platform=wayland"
else
  export DISPLAY="${DISPLAY:-:0}"
  export XAUTHORITY="${XAUTHORITY:-$HOME/.Xauthority}"
  OZONE_FLAGS=""
fi

exec "$CHROME" \
  $OZONE_FLAGS \
  --password-store=basic \
  --kiosk --noerrdialogs --disable-infobars \
  --disable-dev-shm-usage \
  --disk-cache-size=1 --media-cache-size=1 \
  --no-first-run --disable-sync --disable-background-networking \
  --disable-logging \
  "$URL"
