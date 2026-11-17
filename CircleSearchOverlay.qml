import QtQuick
import Quickshell
import "lib/services"
import "lib/modules"

// Omarchy overlay contract. The service stays loaded; only its layer window is lazy.
Item {
    id: root
    readonly property bool opened: CircleSearch.open

    function open(payload) {
        var args = {}
        if (payload) {
            try { args = JSON.parse(payload) || {} } catch (e) { args = {} }
        }
        var output = args.screen || Niri.focusedOutput || Shell.primaryName
        console.log("Circle Search: output=" + output + " windows=" + Niri.windowRects(output, 1).length)
        CircleSearch.placeOn(output, args.mode || "screen", Number(args.delay) || 0)
    }

    function close() {
        CircleSearch.close()
    }

    CircleOverlay {}
}
