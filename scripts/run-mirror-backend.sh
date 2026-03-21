#!/usr/bin/env bash
# Run local API + static UI (FR-006). From repo root:
#   ./scripts/run-mirror-backend.sh
# Optional: MIRROR_SECRETS_DIR, MIRROR_HA_URL, MIRROR_HA_TOKEN_FILE
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT/backend"
if [[ ! -d .venv ]]; then
  python3 -m venv .venv
  .venv/bin/pip install -r requirements.txt
fi
export PYTHONPATH="$ROOT/backend"
exec .venv/bin/python -m uvicorn mirror_backend.main:app --host 0.0.0.0 --port 8780
