#!/usr/bin/env bash
# Sync web/ (mirror UI shell) to the Pi and optionally open Chromium on the HDMI display.
# Run from your Mac — no keyboard needed on the Pi (all over SSH).
#
# Usage:
#   ./scripts/sync-web-to-pi.sh
#   ./scripts/sync-web-to-pi.sh --open              # file:// (no Python server)
#   ./scripts/sync-web-to-pi.sh --open --http     # http://127.0.0.1:8765/ on the Pi
#   PREVIEW_WINDOWED=1 ./scripts/sync-web-to-pi.sh --open
# Optional: PI=pi@other-host ./scripts/sync-web-to-pi.sh
#
# Remote directory: ~/mirror-web/

set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
TARGET="${PI:-pi@mirror-pi4.local}"
REMOTE_DIR="${MIRROR_WEB_DIR:-mirror-web}"
WEB_PORT="${MIRROR_WEB_PORT:-8765}"

OPEN=0
USE_HTTP=0
for a in "$@"; do
  case "$a" in
    --open) OPEN=1 ;;
    --http) USE_HTTP=1 ;;
  esac
done

if ! command -v rsync >/dev/null 2>&1; then
  echo "rsync not found. Use: scp -r ${ROOT}/web/* ${TARGET}:~/${REMOTE_DIR}/" >&2
  exit 1
fi

rsync -avz --delete "${ROOT}/web/" "${TARGET}:~/${REMOTE_DIR}/"
echo "Synced to ${TARGET}:~/${REMOTE_DIR}/"

if [[ "$OPEN" -eq 1 ]]; then
  PREVIEW_WINDOWED_FLAG="${PREVIEW_WINDOWED:-0}"
  PREVIEW_KEEP_CHROMIUM_STDERR_FLAG="${PREVIEW_KEEP_CHROMIUM_STDERR:-0}"
  # shellcheck disable=SC2029
  ssh "$TARGET" bash -s -- "$REMOTE_DIR" "$PREVIEW_WINDOWED_FLAG" "$PREVIEW_KEEP_CHROMIUM_STDERR_FLAG" "$USE_HTTP" "$WEB_PORT" <<'REMOTE'
set -euo pipefail
RD="${1:-mirror-web}"
PREVIEW_WINDOWED="${2:-0}"
KEEP_CHROMIUM_STDERR="${3:-0}"
USE_HTTP="${4:-0}"
WEB_PORT="${5:-8765}"
export DISPLAY="${DISPLAY:-:0}"
export XAUTHORITY="${XAUTHORITY:-$HOME/.Xauthority}"
if [[ -d "/run/user/$(id -u)" ]]; then
  export XDG_RUNTIME_DIR="${XDG_RUNTIME_DIR:-/run/user/$(id -u)}"
fi
CHROME=""
command -v chromium >/dev/null 2>&1 && CHROME="chromium"
command -v chromium-browser >/dev/null 2>&1 && CHROME="chromium-browser"
if [[ -z "$CHROME" ]]; then
  echo "No chromium on PATH." >&2
  exit 1
fi
FLAGS=(
  --noerrdialogs --disable-infobars
  --no-sandbox --disable-dev-shm-usage
  --password-store=basic
  --no-first-run
  --disable-sync
  --disable-background-networking
  --disable-logging
)
KIOSK_FLAGS=(--kiosk)
if [[ "$PREVIEW_WINDOWED" == "1" ]]; then
  KIOSK_FLAGS=()
  echo "PREVIEW_WINDOWED=1 — opening windowed (no --kiosk)." >&2
fi
WEB_ROOT="${HOME}/${RD}"
if [[ "$USE_HTTP" == "1" ]]; then
  if ! command -v python3 >/dev/null 2>&1; then
    echo "python3 not found on Pi; use --open without --http for file:// instead." >&2
    exit 1
  fi
  pkill -f "python3 -m http.server ${WEB_PORT}" 2>/dev/null || true
  cd "$WEB_ROOT"
  nohup python3 -m http.server "$WEB_PORT" >>/tmp/mirror-web-http.log 2>&1 &
  sleep 1
  URL="http://127.0.0.1:${WEB_PORT}/"
  echo "HTTP server on Pi port ${WEB_PORT} (log: /tmp/mirror-web-http.log)"
else
  URL="file://${WEB_ROOT}/index.html"
fi
echo "Opening: $URL"
if [[ "$KEEP_CHROMIUM_STDERR" == "1" ]]; then
  exec "$CHROME" "${FLAGS[@]}" "${KIOSK_FLAGS[@]}" "$URL"
else
  exec "$CHROME" "${FLAGS[@]}" "${KIOSK_FLAGS[@]}" "$URL" 2>/dev/null
fi
REMOTE
fi
