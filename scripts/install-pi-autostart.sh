#!/usr/bin/env bash
# Run on the mirror Pi to enable boot-time recovery after power loss:
# - mirror-backend.service (uvicorn API + static web)
# - mirror-kiosk.service (Chromium kiosk pointing at local API)
set -euo pipefail

APP_DIR="${MIRROR_APP_DIR:-$HOME/mirror-app}"
RUN_USER="${MIRROR_RUN_USER:-$USER}"
SERVICE_DIR="/etc/systemd/system"
BACKEND_SERVICE="${SERVICE_DIR}/mirror-backend.service"
KIOSK_SERVICE="${SERVICE_DIR}/mirror-kiosk.service"

if ! command -v sudo >/dev/null 2>&1; then
  echo "sudo is required to install systemd services." >&2
  exit 1
fi

if [[ ! -x "${APP_DIR}/backend/.venv/bin/python" ]]; then
  echo "Missing backend venv python at ${APP_DIR}/backend/.venv/bin/python" >&2
  echo "Run deploy with --install-deps first." >&2
  exit 1
fi

if [[ ! -x "${APP_DIR}/scripts/pi-launch-kiosk.sh" ]]; then
  echo "Missing kiosk launcher at ${APP_DIR}/scripts/pi-launch-kiosk.sh" >&2
  echo "Re-deploy so scripts/ is synced to the Pi." >&2
  exit 1
fi

echo "Installing ${BACKEND_SERVICE}"
sudo tee "${BACKEND_SERVICE}" >/dev/null <<EOF
[Unit]
Description=Magic Mirror Backend API
After=network-online.target
Wants=network-online.target

[Service]
Type=simple
User=${RUN_USER}
WorkingDirectory=${APP_DIR}/backend
Environment=PYTHONPATH=${APP_DIR}/backend
Environment=MIRROR_REPO_ROOT=${APP_DIR}
ExecStart=${APP_DIR}/backend/.venv/bin/python -m uvicorn mirror_backend.main:app --host 0.0.0.0 --port 8780
Restart=always
RestartSec=3

[Install]
WantedBy=multi-user.target
EOF

echo "Installing ${KIOSK_SERVICE}"
sudo tee "${KIOSK_SERVICE}" >/dev/null <<EOF
[Unit]
Description=Magic Mirror Chromium Kiosk
After=graphical.target mirror-backend.service
Wants=mirror-backend.service

[Service]
Type=simple
User=${RUN_USER}
Environment=DISPLAY=:0
Environment=XAUTHORITY=/home/${RUN_USER}/.Xauthority
Environment=XDG_RUNTIME_DIR=/run/user/%U
ExecStart=${APP_DIR}/scripts/pi-launch-kiosk.sh http://127.0.0.1:8780/
Restart=always
RestartSec=5

[Install]
WantedBy=graphical.target
EOF

echo "Enabling services"
sudo systemctl daemon-reload
sudo systemctl enable mirror-backend.service mirror-kiosk.service
sudo systemctl restart mirror-backend.service
sudo systemctl restart mirror-kiosk.service

echo
echo "Autostart enabled. Verify:"
echo "  systemctl status mirror-backend.service --no-pager"
echo "  systemctl status mirror-kiosk.service --no-pager"
echo "  curl -sS http://127.0.0.1:8780/api/health"
