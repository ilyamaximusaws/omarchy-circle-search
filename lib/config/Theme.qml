pragma Singleton
import QtQuick
import Quickshell
import qs.Commons as Omarchy

Singleton {
    readonly property int u: 2
    readonly property int pad: 10
    readonly property bool macLook: true
    readonly property int barHeight: 30
    readonly property bool dark: Omarchy.Color.background.hslLightness < 0.5
    readonly property color face: Omarchy.Color.background
    readonly property color faceAlt: Qt.alpha(Omarchy.Color.accent, 0.18)
    readonly property color sunken: Omarchy.Color.background
    readonly property color text: Omarchy.Color.foreground
    readonly property color textDim: Omarchy.Color.muted
    readonly property color hi: Qt.alpha(Omarchy.Color.foreground, 0.25)
    readonly property color lo: Qt.alpha(Omarchy.Color.background, 0.8)
    readonly property color edge: Omarchy.Color.muted
    readonly property color shadow: Omarchy.Color.background
    readonly property real shadowAlpha: 0.35
    readonly property color accent: Omarchy.Color.accent
    readonly property color accent2: Omarchy.Color.accent
    readonly property color accent3: Omarchy.Color.foreground
    readonly property color select: Omarchy.Color.accent
    readonly property color selectText: Omarchy.Color.background
    readonly property color danger: Omarchy.Color.urgent
    readonly property string fontBody: "Inter Display"
    readonly property string fontTitle: "Inter Display"
    readonly property string fontMono: "JetBrains Mono"
    readonly property int sizeTiny: 11
    readonly property int sizeBody: 14
    readonly property int sizeMono: 13
    readonly property int sizeMonoSmall: 12
    readonly property int sizeTitle: 16
    readonly property int sizeBig: 22
    readonly property int sizeHuge: 28

    function mix(a, b, t) {
        return Qt.rgba(a.r + (b.r - a.r) * t, a.g + (b.g - a.g) * t, a.b + (b.b - a.b) * t, a.a + (b.a - a.a) * t)
    }
    function hex(c) {
        function h(v) { return Math.round(v * 255).toString(16).padStart(2, "0") }
        return "#" + h(c.r) + h(c.g) + h(c.b)
    }
    function settingsSkinFor(parent) { return "classic" }
    function toneOf(skin, key) {
        if (key === "sunken") return sunken
        if (key === "edge") return edge
        if (key === "faceAlt") return faceAlt
        return text
    }
}
