#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
python3 tools/port_upstream.py --check
python3 tests/test_port.py
python3 tests/test_lens_page.py
python3 tests/test_capture_save.py .
node tests/test_learn.mjs
python3 tests/test_smoke.py
if [[ "${1:-}" == "--live" ]]; then
  python3 tests/test_hyprland.py
elif [[ $# -gt 0 ]]; then
  printf 'Usage: %s [--live]\n' "$0" >&2
  exit 2
fi
