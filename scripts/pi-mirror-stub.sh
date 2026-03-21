#!/usr/bin/env bash
# Run ON THE MIRROR PI (after copy: scp scripts/pi-mirror-stub.sh pi@mirror-pi4.local:~/ )
# Creates a tiny local HTML page and optionally opens it in Chromium kiosk mode.
# Purpose: verify resolution, portrait viewport (innerWidth x innerHeight), and Chromium.

set -euo pipefail

STUB_DIR="${STUB_DIR:-$HOME/mirror-stub}"
mkdir -p "$STUB_DIR"

cat >"$STUB_DIR/index.html" <<'HTML'
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>Mirror stub</title>
  <style>
    * { box-sizing: border-box; }
    body {
      margin: 0;
      min-height: 100vh;
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      background: #111;
      color: #eee;
      font-family: system-ui, sans-serif;
      padding: 1rem;
    }
    h1 { font-size: clamp(1.5rem, 6vw, 3rem); margin: 0 0 0.5rem; }
    .big { font-size: clamp(2rem, 12vw, 6rem); font-weight: 700; color: #7cb8ff; }
    p { font-size: clamp(1rem, 3vw, 1.25rem); opacity: 0.9; }
    code { background: #222; padding: 0.2em 0.4em; border-radius: 4px; }
  </style>
</head>
<body>
  <h1>Mirror Pi — stub OK</h1>
  <p class="big" id="dims"></p>
  <p>Viewport CSS pixels (for layout). Target portrait FHD: often <code>1080 × 1920</code> after rotation.</p>
  <p id="extra"></p>
  <script>
    function show() {
      var o = screen.orientation;
      document.getElementById("dims").textContent = innerWidth + " × " + innerHeight;
      document.getElementById("extra").textContent =
        "devicePixelRatio=" + devicePixelRatio +
        (o ? (" | orientation.type=" + o.type) : "");
    }
    show();
    addEventListener("resize", show);
  </script>
</body>
</html>
HTML

chromium_bin() {
  if command -v chromium >/dev/null 2>&1; then echo chromium; return; fi
  if command -v chromium-browser >/dev/null 2>&1; then echo chromium-browser; return; fi
  echo ""
}

CHROME="$(chromium_bin)"
if [[ -z "$CHROME" ]]; then
  echo "No chromium or chromium-browser in PATH. Install: sudo apt install -y chromium" >&2
  exit 1
fi

FILE_URL="file://${STUB_DIR}/index.html"
echo "Stub written: ${STUB_DIR}/index.html"
echo "On the Pi desktop (Terminal app):  ${CHROME} --password-store=basic --disable-logging --kiosk \"${FILE_URL}\""
echo "From SSH: see PI_BRINGUP.md — needs DISPLAY, XAUTHORITY, runtime dir, and extra Chromium flags."

if [[ "${1:-}" == "--open" ]]; then
  # SSH: no $DISPLAY; attach to the HDMI session. Chromium often needs these env vars when
  # the parent is sshd. Stub-only; --no-sandbox is for this local test, not general browsing.
  if [[ -z "${DISPLAY:-}" ]]; then
    export DISPLAY=:0
    echo "DISPLAY was unset — using :0 (HDMI session)." >&2
  fi
  if [[ -z "${XAUTHORITY:-}" && -f "${HOME}/.Xauthority" ]]; then
    export XAUTHORITY="${HOME}/.Xauthority"
  fi
  if [[ -z "${XDG_RUNTIME_DIR:-}" && -d "/run/user/$(id -u)" ]]; then
    export XDG_RUNTIME_DIR="/run/user/$(id -u)"
  fi

  # Kiosk-only: keyring, less sync/GCM stderr noise (see PI_BRINGUP.md).
  common_flags=(
    --password-store=basic
    --kiosk --noerrdialogs --disable-infobars
    --no-first-run --disable-sync --disable-background-networking
    --disable-logging
  )
  ssh_chromium_flags=()
  if [[ -n "${SSH_CONNECTION:-}" ]]; then
    ssh_chromium_flags+=(--no-sandbox --disable-dev-shm-usage)
    echo "SSH session detected — adding --no-sandbox --disable-dev-shm-usage for Chromium." >&2
  fi

  exec "$CHROME" \
    "${ssh_chromium_flags[@]}" \
    "${common_flags[@]}" \
    "$FILE_URL"
fi
