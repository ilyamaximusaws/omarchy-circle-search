#!/usr/bin/env python3
"""Regenerate the small mechanical part of the Omarchy port from vendored angelOS sources."""
from pathlib import Path
import argparse
import sys

ROOT = Path(__file__).resolve().parents[1]
VENDOR = ROOT / "vendor/angelos"


def replace_once(text, old, new, label):
    if text.count(old) != 1:
        raise RuntimeError(f"{label}: expected one match, got {text.count(old)}")
    return text.replace(old, new, 1)


def imports(text, service=False):
    text = text.replace("import qs.config", 'import "../config"' if not service else "")
    text = text.replace("import qs.services", 'import "../services"' if not service else 'import "."')
    text = text.replace("import qs.widgets", 'import "../widgets"')
    return text


def circle_search():
    text = (VENDOR / "services/CircleSearch.qml").read_text()
    text = imports(text, service=True)
    text = text.replace('import "../plugins/web-search/Engines.js" as Engines', 'import "../vendor/Engines.js" as Engines')
    text = text.replace('Quickshell.shellPath("scripts/circle.py")', 'Config.script("circle.py")')
    text = text.replace('Quickshell.shellPath("scripts/capture_regions.py")', 'Config.script("capture_regions.py")')
    text = replace_once(text, 'root.frameUrl = "file://" + root.frame + "?" + Date.now();', 'root.frameUrl = "file://" + root.frame + ".png";', "cache-safe frame URL")
    text = replace_once(text, ' && head -c 64 "$3"', ' && python3 "$6" "$3" && head -c 64 "$3"', "PNG display frame")
    text = replace_once(text, 'Config.capture.shotCursor ? "-c" : ""];', 'Config.capture.shotCursor ? "-c" : "", Config.script("frame_png.py")];', "frame conversion argument")
    text = replace_once(text, "    property bool open: false\n", "    property bool open: false\n    property bool loaded: false\n", "loaded state")
    text = replace_once(text, "    // wait: seconds before the picture, so a menu that started it has gone from the screen\n", '''    // Omarchy overlay entry point (the upstream two-process host provided this wrapper).
    function placeOn(screen, mode, wait) {
        if (open)
            close();
        start(screen, wait || 0);
    }
    // wait: seconds before the picture, so a menu that started it has gone from the screen
''', "placeOn entry")
    text = replace_once(text, "        if (open || grab.running)\n            return;\n        screenName", "        if (open || grab.running)\n            return;\n        loaded = false;\n        screenName", "start loading")
    text = replace_once(text, "        open = false;\n        reader.running", "        open = false;\n        loaded = false;\n        reader.running", "close loading")
    text = replace_once(text, "                root.frameH = +m[2];\n", "                root.frameH = +m[2];\n                root.loaded = true;\n", "frame loaded")
    start = text.index("    function windowsOn(name) {")
    end = text.index("    // the smallest of the rects under a point", start)
    text = text[:start] + '''    // Hyprland adapter: global logical IPC geometry -> output-local frame pixels.
    function windowsOn(name) {
        return Niri.windowRects(name, root.scale);
    }
''' + text[end:]
    start = text.index("    // to a phone nearby (Quick Share)")
    end = text.index("    function say(title, body)", start)
    text = text[:start] + '''    // Reuse Omarchy's native annotator instead of porting angelOS's second editor.
    function edit() {
        if (!open)
            return;
        learnNow();
        Capture.saveShot(frame, rectOf(box), {
            "copy": false,
            "quiet": true,
            "noThumb": true
        }, r => {
            if (!r.path) {
                say(I18n.t("Не удалось сохранить снимок", "Could not save the screenshot"), r.error || "");
                return;
            }
            close();
            Quickshell.execDetached(["omasnap", "--file", r.path]);
        });
    }
''' + text[end:]
    return text


def circle_canvas():
    text = (VENDOR / "modules/circle/CircleCanvas.qml").read_text()
    text = imports(text)
    text = text.replace('import "../../widgets/Place.js" as Place', 'import "../widgets/Place.js" as Place')
    text = replace_once(text, "canvas.landAt = ShotEdit.placeOn(CircleSearch.screenName);", 'canvas.landAt = "bottom-right";', "preview landing")
    start = text.index('                "share": {')
    end = text.index('                "full": {', start)
    text = text[:start] + '''                "edit": {
                    "icon": "edit",
                    "text": I18n.t("Редактировать", "Edit"),
                    "on": true,
                    "shown": !behind("edit"),
                    "run": () => CircleSearch.edit()
                },
''' + text[end:]
    if text.count('"share",') != 4:
        raise RuntimeError("toolbar order: expected four share entries")
    text = text.replace('"share",', '"edit",')
    return text


def circle_overlay():
    text = (VENDOR / "modules/circle/CircleOverlay.qml").read_text()
    text = imports(text)
    text = text.replace('WlrLayershell.namespace: "angelos-circle-search"', 'WlrLayershell.namespace: "omarchy-circle-search"')
    return text


def generated():
    return {
        "lib/services/CircleSearch.qml": circle_search(),
        "lib/modules/CircleCanvas.qml": circle_canvas(),
        "lib/modules/CircleOverlay.qml": circle_overlay(),
        "lib/services/Links.js": (VENDOR / "services/Links.js").read_text(),
        "lib/services/CircleLearn.js": (VENDOR / "services/CircleLearn.js").read_text(),
        "lib/widgets/Icons.js": (VENDOR / "widgets/Icons.js").read_text(),
        "lib/widgets/Place.js": (VENDOR / "widgets/Place.js").read_text(),
        "lib/vendor/Engines.js": (VENDOR / "plugins/web-search/Engines.js").read_text(),
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true", help="fail if generated files differ; never write")
    args = parser.parse_args()
    expected = generated()
    different = []
    for name, text in expected.items():
        path = ROOT / name
        if not path.exists() or path.read_text() != text:
            different.append(name)
        elif not args.check:
            continue
        if not args.check:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(text)
    for name in ["circle.py", "capture_regions.py", "capture_save.py"]:
        src = VENDOR / "scripts" / name
        dst = ROOT / "scripts" / name
        if not dst.exists() or dst.read_bytes() != src.read_bytes():
            different.append("scripts/" + name)
        if not args.check:
            dst.write_bytes(src.read_bytes())
    if args.check:
        if different:
            print("out of date:\n" + "\n".join(sorted(set(different))), file=sys.stderr)
            return 1
        print(f"up to date: {len(expected) + 3} generated files")
        return 0
    print(f"generated {len(expected) + 3} files")
    return 0


if __name__ == "__main__":
    sys.exit(main())
