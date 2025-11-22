#!/usr/bin/env bash
set -euo pipefail

# Optional: pass a version like "0.28.3" as the first arg. Blank means latest.
FLET_VERSION="${1:-}"
if [[ -z "$FLET_VERSION" ]]; then
  FLET_PKG=("flet" "flet-desktop")
  FLET_LABEL="latest"
else
  FLET_PKG=("flet==${FLET_VERSION}" "flet-desktop==${FLET_VERSION}")
  FLET_LABEL="$FLET_VERSION"
fi

cd "$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

if ! command -v python3 >/dev/null 2>&1; then
  echo "[ERROR] python3 not found." >&2
  exit 1
fi

# Create venv if needed
if [[ ! -d "venv" ]]; then
  python3 -m venv venv
fi

# Activate venv
source venv/bin/activate

python -m pip install --upgrade pip
echo "Installing Flet (${FLET_LABEL})..."
pip install --upgrade "${FLET_PKG[@]}"

echo "Setup complete. Run ./run_app.sh to start the app."
