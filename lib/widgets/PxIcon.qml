import QtQuick
import "../config"
import "Icons.js" as Icons

Image {
    id: root
    property string name: "heart"
    property var bitmap: null
    property int pixel: Theme.u
    property real exactPixel: 0
    property bool hollow: false
    property color ink: Theme.text
    property color fill: Theme.accent
    property color fill2: Theme.accent2
    property color fill3: Theme.accent3
    property color light: "#ffffff"
    property color body: Theme.faceAlt
    property color bad: Theme.danger
    property var palette: ({})
    readonly property real _px: exactPixel > 0 ? exactPixel : pixel
    readonly property var _svg: Icons.svg(bitmap && bitmap.length ? bitmap : name, Object.assign({
        "#": Theme.hex(ink), "o": Theme.hex(fill), "x": Theme.hex(fill2), "y": Theme.hex(fill3),
        "w": Theme.hex(light), "f": Theme.hex(body), "r": Theme.hex(bad)
    }, palette || {}), hollow)
    source: _svg.url
    width: Math.round(_svg.width * _px)
    height: Math.round(_svg.height * _px)
    sourceSize: Qt.size(width, height)
    smooth: false
    mipmap: false
    asynchronous: false
}
