#!/usr/bin/env python3
"""Live integration: the deployed overlay must summon and see Hyprland windows."""
import json
import os
from pathlib import Path
import re
import subprocess
import tempfile

PLUGIN = "angelos.circle-search"

def run(args, timeout=30):
    return subprocess.run(args, capture_output=True, text=True, timeout=timeout)

plugins = run(["omarchy-shell", "shell", "listPlugins"])
if plugins.returncode:
    raise SystemExit("SKIP: no running Omarchy shell")
try:
    plugin = next(p for p in json.loads(plugins.stdout) if p["id"] == PLUGIN)
except (ValueError, StopIteration):
    raise SystemExit("SKIP: plugin is not installed")
if not plugin["enabled"]:
    raise SystemExit("SKIP: plugin is disabled")

processes = run(["pgrep", "-af", "quickshell -n -p /usr/share/omarchy/shell"])
pids = [line.split(None, 1)[0] for line in processes.stdout.splitlines() if "/usr/share/omarchy/shell" in line]
if not pids:
    raise SystemExit("SKIP: Omarchy shell process not found")
pid = pids[0]
marker = re.compile(r"Circle Search: output=(\S+) windows=(\d+)")

def openings():
    log = run(["qs", "log", "--pid", pid, "-t", "1000"])
    return marker.findall(log.stdout)

before = len(openings())
try:
    summoned = run(["omarchy-shell", "shell", "summon", PLUGIN, "{}"])
    assert summoned.returncode == 0 and summoned.stdout.strip() == "ok", summoned.stdout + summoned.stderr
    import time
    time.sleep(2)
    after = openings()
    assert len(after) > before, "overlay did not report a fresh open in the live shell log"
    output, windows = after[-1]
    assert output, "empty Hyprland output name"
    with tempfile.TemporaryDirectory() as tmp:
        frame = Path(tmp) / "circle.png"
        captured = run(["grim", str(frame)])
        assert captured.returncode == 0, captured.stderr
        assert frame.stat().st_size > 10000, "captured frame is unexpectedly small"
        frame_size = frame.stat().st_size
    print(f"PASS live overlay: output={output}, windows={windows}, grim={frame_size} bytes")
finally:
    run(["omarchy-shell", "shell", "hide", PLUGIN])
