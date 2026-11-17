pragma Singleton
import QtQuick
import Quickshell
import Quickshell.Io

Singleton {
    id: root
    property var callback: null
    property var lastOpts: ({})
    signal shotSaved(string path)

    function saveShot(frame, rect, opts, done) {
        opts = opts || {}
        if (saver.running) {
            if (done) done({path: "", copied: false, error: "another capture is still being written"})
            return
        }
        callback = done
        lastOpts = opts
        var args = ["python3", Config.script("save_shot.py"), "save", frame, "--quiet", "--dir", Config.capture.shotDir, "--format", Config.capture.shotFormat]
        if (rect) args.push("--rect", [Math.round(rect.x), Math.round(rect.y), Math.round(rect.width !== undefined ? rect.width : rect.w), Math.round(rect.height !== undefined ? rect.height : rect.h)].join(","))
        if (opts.copy === false || Config.capture.shotCopy === false) args.push("--no-copy")
        if (opts.save === false) args.push("--no-save")
        saver.command = args
        saver.running = true
    }

    function notify(path) {
        if (!path) return
        Quickshell.execDetached([
            "omarchy-notification-send", "--app-name", "Circle Search", "--image", path,
            I18n.t("Снимок сохранён", "Screenshot saved"), path,
            "--action", I18n.t("Открыть", "Open"), "xdg-open", path,
            "--action", I18n.t("Редактировать", "Edit"), "omasnap", "--file", path
        ])
    }

    Process {
        id: saver
        stdout: StdioCollector {
            onStreamFinished: {
                var result = {path: "", copied: false, error: "capture helper returned no result"}
                try { result = JSON.parse(text.trim().split("\n").pop()) } catch (e) {}
                var done = root.callback
                var opts = root.lastOpts
                root.callback = null
                if (result.path) {
                    if (!opts.quiet && !opts.noNotify) root.notify(result.path)
                    root.shotSaved(result.path)
                }
                if (done) done(result)
            }
        }
    }
}
