#!/usr/bin/env bash
set -euo pipefail

cd "$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

if [[ ! -d "venv" ]]; then
  echo "[ERROR] venv not found. Run ./setup.sh first." >&2
  exit 1
fi

source venv/bin/activate
python app.py
