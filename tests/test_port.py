#!/usr/bin/env python3
"""Structural contract for the angelOS -> Omarchy port."""
import hashlib
import json
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
failures = []


def check(condition, message):
    print(("PASS " if condition else "FAIL ") + message)
    if not condition:
        failures.append(message)


required = [
    "manifest.json",
    "CircleSearchOverlay.qml",
    "lib/services/CircleSearch.qml",
    "lib/services/Niri.qml",
    "lib/services/Capture.qml",
    "lib/services/Island.qml",
    "lib/services/Config.qml",
    "lib/config/Theme.qml",
    "lib/modules/CircleCanvas.qml",
    "lib/modules/CircleOverlay.qml",
    "lib/widgets/PxButton.qml",
    "scripts/circle.py",
    "scripts/capture_regions.py",
    "scripts/capture_save.py",
    "tools/port_upstream.py",
]
for name in required:
    check((ROOT / name).is_file(), f"exists: {name}")

manifest_path = ROOT / "manifest.json"
if manifest_path.is_file():
    manifest = json.loads(manifest_path.read_text())
    check(manifest.get("id") == "angelos.circle-search", "stable plugin id")
    check(manifest.get("kinds") == ["overlay"], "overlay-only plugin")
    check(manifest.get("keepLoaded") is True, "warm overlay lifecycle")
    check(manifest.get("entryPoints", {}).get("overlay") == "CircleSearchOverlay.qml", "overlay entry point")

for name in ["lib/services/CircleSearch.qml", "lib/modules/CircleCanvas.qml", "lib/modules/CircleOverlay.qml"]:
    path = ROOT / name
    if not path.is_file():
        continue
    text = path.read_text()
    for forbidden in ["import qs.config", "import qs.services", "import qs.widgets", "Quickshell.shellPath", "Niri.windowsOn", "= ShotEdit.placeOn(", "QuickShare.share"]:
        check(forbidden not in text, f"{name}: no {forbidden}")

search_path = ROOT / "lib/services/CircleSearch.qml"
if search_path.is_file():
    search = search_path.read_text()
    check("function edit(" in search and '"--file"' in search, "selection opens Omasnap editor by file")
canvas_path = ROOT / "lib/modules/CircleCanvas.qml"
if canvas_path.is_file():
    check('CircleSearch.edit()' in canvas_path.read_text(), "toolbar exposes the Omasnap editor")

for name in ["circle.py", "capture_regions.py", "capture_save.py"]:
    upstream = ROOT / "vendor/angelos/scripts" / name
    ported = ROOT / "scripts" / name
    if upstream.is_file() and ported.is_file():
        check(hashlib.sha256(upstream.read_bytes()).digest() == hashlib.sha256(ported.read_bytes()).digest(), f"upstream script preserved: {name}")

port = ROOT / "tools/port_upstream.py"
if port.is_file() and all((ROOT / p).is_file() for p in ["lib/services/CircleSearch.qml", "lib/modules/CircleCanvas.qml"]):
    before = {p: hashlib.sha256(p.read_bytes()).hexdigest() for p in ROOT.glob("lib/**/*.qml")}
    result = subprocess.run([sys.executable, str(port), "--check"], cwd=ROOT, capture_output=True, text=True)
    after = {p: hashlib.sha256(p.read_bytes()).hexdigest() for p in ROOT.glob("lib/**/*.qml")}
    check(result.returncode == 0, "generated port is up to date: " + result.stdout.strip() + result.stderr.strip())
    check(before == after, "--check never rewrites generated files")

print(f"SUMMARY {len(failures)} failures")
sys.exit(bool(failures))
