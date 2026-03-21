#!/usr/bin/env bash
# One-shot deploy: web + backend + config to the Pi, optional venv, HA token copy,
# start API on :8780, open Chromium. Run from your Mac (keyboard not required on Pi).
#
# Usage (Mac Terminal):
#   ./scripts/deploy-mirror-to-pi.sh --all
# Optional override: export PI=pi@other-host
#
# First-time Pi: use --all. Later, only files changed:
#   ./scripts/deploy-mirror-to-pi.sh
# With venv refresh + restart + browser:
#   ./scripts/deploy-mirror-to-pi.sh --install-deps --start-backend --open
# Enable boot-time recovery (systemd backend + kiosk):
#   ./scripts/deploy-mirror-to-pi.sh --install-deps --enable-autostart
#
# Remote layout: ~/mirror-app/{web,backend,config}  (matches MIRROR_REPO_ROOT on Pi)
#
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
TARGET="${PI:-pi@mirror-pi4.local}"
RDIR="${MIRROR_APP_DIR:-mirror-app}"

# Reuse one SSH session for all rsync/ssh/scp in this run → one password prompt (until you use ssh-copy-id).
# Disable: MIRROR_SSH_NO_MUX=1 ./scripts/deploy-mirror-to-pi.sh
if [[ "${MIRROR_SSH_NO_MUX:-0}" == "1" ]]; then
  _SSH_EXTRA=()
  export RSYNC_RSH="ssh"
else
  _SSH_EXTRA=(
    -o ControlMaster=auto
    -o "ControlPath=${HOME}/.ssh/cm-mirror-deploy-%C"
    -o ControlPersist=120
  )
  export RSYNC_RSH="ssh ${_SSH_EXTRA[*]}"
fi

INSTALL_DEPS=0
COPY_HA_TOKEN=0
START_BACKEND=0
OPEN_BROWSER=0
ENABLE_AUTOSTART=0

for a in "$@"; do
  case "$a" in
    --install-deps) INSTALL_DEPS=1 ;;
    --copy-ha-token) COPY_HA_TOKEN=1 ;;
    --start-backend) START_BACKEND=1 ;;
    --open) OPEN_BROWSER=1 ;;
    --enable-autostart) ENABLE_AUTOSTART=1 ;;
    --all)
      INSTALL_DEPS=1
      COPY_HA_TOKEN=1
      START_BACKEND=1
      OPEN_BROWSER=1
      ;;
    -h|--help)
      echo "Usage: $0 [--all] [--install-deps] [--copy-ha-token] [--start-backend] [--open] [--enable-autostart]"
      echo "  Default SSH: pi@mirror-pi4.local  Override: export PI=pi@host"
      echo "  SSH multiplexing (fewer passwords): on by default; MIRROR_SSH_NO_MUX=1 to disable"
      exit 0
      ;;
  esac
done

# Rsync does not always create missing parent dirs on the receiver; ensure tree exists.
echo "==> mkdir -p ~/${RDIR}/{web,backend,config,scripts} on Pi"
# shellcheck disable=SC2029
ssh "${_SSH_EXTRA[@]}" "$TARGET" "mkdir -p \"\$HOME/${RDIR}/web\" \"\$HOME/${RDIR}/backend\" \"\$HOME/${RDIR}/config\" \"\$HOME/${RDIR}/scripts\""

echo "==> rsync → ${TARGET}:~/${RDIR}/"
rsync -avz --delete "${ROOT}/web/" "${TARGET}:~/${RDIR}/web/"
rsync -avz --delete --exclude ".venv" "${ROOT}/backend/" "${TARGET}:~/${RDIR}/backend/"
rsync -avz "${ROOT}/config/" "${TARGET}:~/${RDIR}/config/"
rsync -avz "${ROOT}/scripts/" "${TARGET}:~/${RDIR}/scripts/"

if [[ "$INSTALL_DEPS" -eq 1 ]]; then
  echo "==> Python venv + pip on Pi"
  # shellcheck disable=SC2029
  ssh "${_SSH_EXTRA[@]}" "$TARGET" "cd ~/${RDIR}/backend && python3 -m venv .venv && .venv/bin/pip install -U pip && .venv/bin/pip install -r requirements.txt"
fi

if [[ "$COPY_HA_TOKEN" -eq 1 ]]; then
  if [[ -f "${HOME}/.config/mirror/ha_token" ]]; then
    echo "==> Copy HA token to Pi ~/.config/mirror/ha_token"
    # shellcheck disable=SC2029
    ssh "${_SSH_EXTRA[@]}" "$TARGET" 'mkdir -p ~/.config/mirror && chmod 700 ~/.config/mirror'
    scp "${_SSH_EXTRA[@]}" "${HOME}/.config/mirror/ha_token" "${TARGET}:~/.config/mirror/ha_token"
    # shellcheck disable=SC2029
    ssh "${_SSH_EXTRA[@]}" "$TARGET" 'chmod 600 ~/.config/mirror/ha_token'
  else
    echo "WARN: No ${HOME}/.config/mirror/ha_token on this Mac — skipping (--copy-ha-token)." >&2
  fi
fi

if [[ "$ENABLE_AUTOSTART" -eq 1 ]]; then
  echo "==> Install/enable systemd autostart services on Pi"
  # shellcheck disable=SC2029
  ssh "${_SSH_EXTRA[@]}" "$TARGET" "chmod +x \"\$HOME/${RDIR}/scripts/install-pi-autostart.sh\" \"\$HOME/${RDIR}/scripts/pi-launch-kiosk.sh\" && MIRROR_APP_DIR=\"\$HOME/${RDIR}\" \"\$HOME/${RDIR}/scripts/install-pi-autostart.sh\""
fi

if [[ "$START_BACKEND" -eq 1 ]]; then
  echo "==> Start backend on Pi :8780 (nohup, log /tmp/mirror-backend.log)"
  # shellcheck disable=SC2029
  ssh "${_SSH_EXTRA[@]}" "$TARGET" bash -s -- "$RDIR" <<'REMOTE'
set -euo pipefail
RDIR="${1:?}"
export MIRROR_REPO_ROOT="${HOME}/${RDIR}"
export PYTHONPATH="${MIRROR_REPO_ROOT}/backend"
cd "${MIRROR_REPO_ROOT}/backend"
rm -rf mirror_backend/__pycache__ tests/__pycache__ 2>/dev/null || true
pkill -f "uvicorn mirror_backend.main:app" 2>/dev/null || true
sleep 1
nohup .venv/bin/python -m uvicorn mirror_backend.main:app --host 0.0.0.0 --port 8780 \
  >>/tmp/mirror-backend.log 2>&1 &
sleep 2
echo "Last lines of /tmp/mirror-backend.log:"
tail -8 /tmp/mirror-backend.log 2>/dev/null || echo "(no log yet)"
REMOTE
fi

if [[ "$OPEN_BROWSER" -eq 1 ]]; then
  echo "==> Open Chromium on Pi → http://127.0.0.1:8780/"
  PREVIEW_WINDOWED_FLAG="${PREVIEW_WINDOWED:-0}"
  PREVIEW_KEEP_CHROMIUM_STDERR_FLAG="${PREVIEW_KEEP_CHROMIUM_STDERR:-0}"
  # shellcheck disable=SC2029
  ssh "${_SSH_EXTRA[@]}" "$TARGET" bash -s -- "$PREVIEW_WINDOWED_FLAG" "$PREVIEW_KEEP_CHROMIUM_STDERR_FLAG" <<'REMOTE'
set -euo pipefail
PREVIEW_WINDOWED="${1:-0}"
KEEP_CHROMIUM_STDERR="${2:-0}"
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
fi
URL="http://127.0.0.1:8780/"
pkill -f "chromium.*127.0.0.1:8780" 2>/dev/null || true
sleep 0.5
if [[ "$KEEP_CHROMIUM_STDERR" == "1" ]]; then
  exec "$CHROME" "${FLAGS[@]}" "${KIOSK_FLAGS[@]}" "$URL"
else
  exec "$CHROME" "${FLAGS[@]}" "${KIOSK_FLAGS[@]}" "$URL" 2>/dev/null
fi
REMOTE
fi

echo "Done."
