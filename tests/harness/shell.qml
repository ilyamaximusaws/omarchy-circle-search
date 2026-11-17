import QtQuick
import Quickshell
import Quickshell.Io
import Quickshell.Wayland
import "../../lib/services"
import "../../"

ShellRoot {
    id: root
    settings.watchFiles: false

    Variants {
        model: Quickshell.screens
        PanelWindow {
            id: win
            required property ShellScreen modelData
            screen: modelData
            implicitWidth: 800
            implicitHeight: 600
            color: "#202028"
            WlrLayershell.layer: WlrLayer.Overlay
            CircleSearchOverlay { id: plugin; anchors.fill: parent }

            Connections {
                target: CircleSearch
                function onLoadedChanged() {
                    if (!CircleSearch.loaded || root.finished) return
                    console.log("T loaded", CircleSearch.frameW, CircleSearch.frameH)
                    root.assert(CircleSearch.frameW === 640 && CircleSearch.frameH === 480, "frame dimensions")
                    root.assert(typeof plugin.open === "function" && typeof plugin.close === "function", "Omarchy open/close contract")
                    CircleSearch.pickRect({"x": 40, "y": 40, "w": 200, "h": 100}, "rect")
                    root.assert(CircleSearch.box.x === 40 && CircleSearch.box.y === 40 && CircleSearch.box.w === 200 && CircleSearch.box.h === 100, "manual region")
                    editTimer.start()
                }
            }
            Connections {
                target: Capture
                function onShotSaved(path) {
                    if (root.finished) return
                    console.log("T saved", path)
                    root.assert(path.indexOf(Quickshell.env("TEST_DIR")) === 0, "save directory")
                    root.savedPath = path
                    root.finishSoon()
                }
            }
        }
    }

    property bool finished: false
    property string savedPath: ""
    function assert(ok, name) {
        if (ok) { console.log("PASS", name); return }
        console.error("FAIL", name)
        finished = true
        Qt.exit(1)
    }
    function finishSoon() {
        finished = true
        finalTimer.start()
    }

    Timer {
        interval: 80
        running: true
        repeat: false
        onTriggered: {
            if (!Quickshell.screens.length) { console.error("FAIL no screens"); Qt.exit(1); return }
            Config.circle.liveText = false
            Config.capture.shotDir = Quickshell.env("TEST_DIR")
            CircleSearch.placeOn(Quickshell.screens[0].name, "screen", 0)
        }
    }
    Timer {
        id: editTimer
        interval: 80
        onTriggered: CircleSearch.edit()
    }
    Timer {
        id: finalTimer
        interval: 150
        onTriggered: {
            root.assert(!CircleSearch.open, "editor closes overlay")
            Qt.exit(0)
        }
    }
    Timer {
        interval: 15000
        running: true
        onTriggered: { console.error("FAIL timeout"); Qt.exit(1) }
    }
}
