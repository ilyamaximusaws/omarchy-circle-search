pragma Singleton
import QtQuick

QtObject {
    readonly property color background: "#181820"
    readonly property color foreground: "#eeeeee"
    readonly property color accent: "#8a8ae8"
    readonly property color muted: "#a0a0b0"
    readonly property color urgent: "#e06060"
    readonly property QtObject popups: QtObject {
        readonly property color background: "#282832"
        readonly property color text: "#eeeeee"
        readonly property color border: "#666678"
    }
    readonly property QtObject menu: QtObject {
        readonly property color selectedBackground: "#55558a"
        readonly property color selectedText: "#ffffff"
        readonly property color selectedBorder: "#8a8ae8"
    }
}
