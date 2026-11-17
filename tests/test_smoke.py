#!/usr/bin/env python3
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[1]
HARNESS = ROOT / "tests/harness"

with tempfile.TemporaryDirectory() as tmp:
    tmp_path = Path(tmp)
    project = tmp_path / "project"
    project.mkdir()
    for name in ["lib", "scripts"]:
        shutil.copytree(ROOT / name, project / name)
    shutil.copy2(ROOT / "CircleSearchOverlay.qml", project / "CircleSearchOverlay.qml")
    shutil.copytree(HARNESS / "qs/Commons", project / "Commons")
    shell = (HARNESS / "shell.qml").read_text().replace('import "../../lib/services"', 'import "lib/services"').replace('import "../../"\n', "")
    (project / "shell.qml").write_text(shell)

    bin_dir = tmp_path / "bin"
    bin_dir.mkdir()
    shots = tmp_path / "shots"
    shots.mkdir()
    log = tmp_path / "commands.log"

    grim = bin_dir / "grim"
    grim.write_text("#!/usr/bin/env python3\nimport shutil,sys\nfrom pathlib import Path\nPath(r'" + str(log) + "').open('a').write('grim '+repr(sys.argv[1:])+'\\n')\nshutil.copyfile(r'" + str(HARNESS / "frame.ppm") + "',sys.argv[-1])\n")
    grim.chmod(0o755)
    omasnap = bin_dir / "omasnap"
    omasnap.write_text("#!/usr/bin/env python3\nimport sys\nfrom pathlib import Path\nPath(r'" + str(log) + "').open('a').write('omasnap '+repr(sys.argv[1:])+'\\n')\n")
    omasnap.chmod(0o755)
    wl_copy = bin_dir / "wl-copy"
    wl_copy.write_text("#!/usr/bin/env python3\nimport sys\nsys.stdin.buffer.read()\n")
    wl_copy.chmod(0o755)

    env = dict(os.environ)
    env.update({
        "PATH": str(bin_dir) + os.pathsep + env["PATH"],
        "QT_QPA_PLATFORM": "wayland",
        "WAYLAND_DISPLAY": f"/run/user/{os.getuid()}/wayland-1",
        "QT_QUICK_BACKEND": "software",
        "QML2_IMPORT_PATH": str(project) + os.pathsep + "/usr/lib/qt6/qml",
        "QML_IMPORT_PATH": str(project) + os.pathsep + "/usr/lib/qt6/qml",
        "XDG_RUNTIME_DIR": str(tmp_path),
        "TEST_DIR": str(shots),
    })
    try:
        result = subprocess.run(["qs", "-n", "-p", str(project)], cwd=ROOT, env=env, capture_output=True, text=True, timeout=20)
    except subprocess.TimeoutExpired as e:
        print((e.stdout or b"").decode() if isinstance(e.stdout, bytes) else (e.stdout or ""), end="")
        print((e.stderr or b"").decode() if isinstance(e.stderr, bytes) else (e.stderr or ""), end="", file=sys.stderr)
        raise SystemExit("QML smoke timed out")
    print(result.stdout, end="")
    print(result.stderr, end="", file=sys.stderr)
    if result.returncode != 0:
        raise SystemExit(result.returncode)
    combined = result.stdout + result.stderr
    assert "Cannot open:" not in combined, "the frozen frame did not render"
    assert "Unable to assign [undefined]" not in combined, "the theme adapter did not load"
    commands = log.read_text() if log.exists() else ""
    print(commands, end="")
    assert "grim" in commands, "grim was not invoked"
    assert "omasnap ['--file'," in commands, "Omasnap was not opened on the saved crop"
    assert "--file" in commands and str(shots) in commands, "editor did not receive the saved crop"
print("PASS QML smoke + crop + Omasnap integration")
