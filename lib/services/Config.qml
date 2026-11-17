pragma Singleton
import QtQuick
import Quickshell

Singleton {
    readonly property string home: Quickshell.env("HOME")
    readonly property string stateDir: (Quickshell.env("XDG_STATE_HOME") || home + "/.local/state") + "/omarchy/circle-search"
    readonly property string pluginDir: {
        var url = String(Qt.resolvedUrl("."))
        if (url.indexOf("file://") === 0) {
            try { url = decodeURIComponent(url.substring(7)) } catch (e) {}
        }
        return url.replace(/\/lib\/services\/?$/, "")
    }

    readonly property QtObject capture: QtObject {
        property string shotDir: "~/Pictures/Screenshots"
        property string shotFormat: "png"
        property bool shotCopy: true
        property bool shotOpen: false
        property bool shotCursor: false
    }
    readonly property QtObject circle: QtObject {
        property string engine: "google"
        property string translateTo: "auto"
        property bool liveText: true
        property bool lens: true
    }
    readonly property QtObject quickshare: QtObject { property bool enabled: false }

    function script(name) { return pluginDir + "/scripts/" + name }
    Component.onCompleted: Quickshell.execDetached(["mkdir", "-p", stateDir])
}
