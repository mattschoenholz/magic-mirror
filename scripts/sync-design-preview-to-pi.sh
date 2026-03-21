#!/usr/bin/env bash
# Sync docs/design/ to the mirror Pi and optionally open the preview gallery in Chromium.
# Run from your dev machine (repo root recommended).
#
# Usage:
#   ./scripts/sync-design-preview-to-pi.sh
#   ./scripts/sync-design-preview-to-pi.sh --open
#   PREVIEW_WINDOWED=1 ./scripts/sync-design-preview-to-pi.sh --open   # browser chrome (back button)
# Optional: PI=pi@other-host ./scripts/sync-design-preview-to-pi.sh
#   PREVIEW_KEEP_CHROMIUM_STDERR=1 … --open   # show Chromium ERROR lines (descriptor / GCM / vsync) for debugging
#
# Remote directory: ~/mirror-design-preview/ (same structure as docs/design/)

set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
TARGET="${PI:-pi@mirror-pi4.local}"
REMOTE_DIR="${REMOTE_DESIGN_DIR:-mirror-design-preview}"

if ! command -v rsync >/dev/null 2>&1; then
  echo "rsync not found. Install or use: scp -r ${ROOT}/docs/design/* ${TARGET}:~/${REMOTE_DIR}/" >&2
  exit 1
fi

rsync -avz --delete "${ROOT}/docs/design/" "${TARGET}:~/${REMOTE_DIR}/"
echo "Synced to ${TARGET}:~/${REMOTE_DIR}/"

if [[ "${1:-}" == "--open" ]]; then
  PREVIEW_WINDOWED_FLAG="${PREVIEW_WINDOWED:-0}"
  PREVIEW_KEEP_CHROMIUM_STDERR_FLAG="${PREVIEW_KEEP_CHROMIUM_STDERR:-0}"
  # shellcheck disable=SC2029
  ssh "$TARGET" bash -s -- "$REMOTE_DIR" "$PREVIEW_WINDOWED_FLAG" "$PREVIEW_KEEP_CHROMIUM_STDERR_FLAG" <<'REMOTE'
set -euo pipefail
RD="${1:-mirror-design-preview}"
PREVIEW_WINDOWED="${2:-0}"
KEEP_CHROMIUM_STDERR="${3:-0}"
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
# Stub/preview only: sandbox, /dev/shm, keyring, less Google background/GCM noise on stderr.
FLAGS=(
  --noerrdialogs --disable-infobars
  --no-sandbox --disable-dev-shm-usage
  --password-store=basic
  --no-first-run
  --disable-sync
  --disable-background-networking
  --disable-logging
)
URL="file://${HOME}/${RD}/preview/index.html"
KIOSK_FLAGS=(--kiosk)
if [[ "$PREVIEW_WINDOWED" == "1" ]]; then
  KIOSK_FLAGS=()
  echo "PREVIEW_WINDOWED=1 — opening windowed (no --kiosk)." >&2
fi
echo "Opening: $URL"
# Harmless Pi/Chromium noise still hits stderr; hide it unless debugging (see PI_BRINGUP.md).
if [[ "$KEEP_CHROMIUM_STDERR" == "1" ]]; then
  exec "$CHROME" "${FLAGS[@]}" "${KIOSK_FLAGS[@]}" "$URL"
else
  exec "$CHROME" "${FLAGS[@]}" "${KIOSK_FLAGS[@]}" "$URL" 2>/dev/null
fi
REMOTE
fi
