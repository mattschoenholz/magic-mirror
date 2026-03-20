#!/usr/bin/env bash
# Run ON THE PI (SSH ok). Sets DISPLAY=:0 and rotates the primary connected output.
# Usage:
#   ./pi-display-rotate.sh list              # show outputs + modes
#   ./pi-display-rotate.sh left|right|normal # rotate first "connected" output
#   ./pi-display-rotate.sh left HDMI-2       # explicit output name from `list`
#
# After you find the correct setting, persist with /boot/firmware/config.txt — see docs/PI_BRINGUP.md

set -euo pipefail

export DISPLAY="${DISPLAY:-:0}"
if [[ -f "${HOME}/.Xauthority" ]]; then
  export XAUTHORITY="${XAUTHORITY:-$HOME/.Xauthority}"
fi
if [[ -d "/run/user/$(id -u)" ]]; then
  export XDG_RUNTIME_DIR="${XDG_RUNTIME_DIR:-/run/user/$(id -u)}"
fi

cmd="${1:-list}"
explicit_out="${2:-}"

pick_output() {
  if [[ -n "$explicit_out" ]]; then
    echo "$explicit_out"
    return
  fi
  # First line that looks like "NAME connected ..."
  xrandr --query 2>/dev/null | awk '/^[^ ].* connected/{print $1; exit}'
}

case "$cmd" in
  list)
    xrandr --query
    ;;
  left | right | normal | inverted)
    out="$(pick_output)"
    if [[ -z "$out" ]]; then
      echo "No connected output found. Run: $0 list" >&2
      exit 1
    fi
    echo "Rotating $out → $cmd"
    xrandr --output "$out" --rotate "$cmd"
    ;;
  *)
    echo "Usage: $0 list | left | right | normal | inverted [OUTPUT]" >&2
    exit 1
    ;;
esac
