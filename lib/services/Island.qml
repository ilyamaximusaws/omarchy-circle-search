pragma Singleton
import QtQuick
import Quickshell
import Quickshell.Io

Singleton {
    id: root
    function open(url) { if (url) Quickshell.execDetached(["xdg-open", String(url)]) }
    function search(text) {
        var q = String(text || "").trim()
        if (q) open("https://www.google.com/search?q=" + encodeURIComponent(q.replace(/\s+/g, " ")))
    }
    function lens(png) {
        if (!png) return
        lenser.command = ["python3", Config.script("lens_page.py"), png]
        lenser.running = true
    }
    Process {
        id: lenser
        stdout: StdioCollector {
            onStreamFinished: {
                var path = text.trim()
                if (path) root.open(path)
            }
        }
    }
}
