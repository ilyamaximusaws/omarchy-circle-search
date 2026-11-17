#!/usr/bin/env python3
"""Supply Omarchy settings to the vendored capture_save.py without modifying upstream."""
from pathlib import Path
import importlib.util
import sys

HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("angelos_capture_save", HERE / "capture_save.py")
capture = importlib.util.module_from_spec(spec)
spec.loader.exec_module(capture)

args = sys.argv[1:]
settings = {"shotDir": "~/Pictures/Screenshots", "shotFormat": "png", "shotCopy": True, "shotOpen": False}
forwarded = []
it = iter(range(len(args)))
skip = False
for i, arg in enumerate(args):
    if skip:
        skip = False
        continue
    if arg in ("--dir", "--format"):
        if i + 1 >= len(args):
            raise SystemExit(f"{arg} requires a value")
        settings["shotDir" if arg == "--dir" else "shotFormat"] = args[i + 1]
        skip = True
    else:
        forwarded.append(arg)

capture.settings = lambda: settings
raise SystemExit(capture.main(forwarded))
