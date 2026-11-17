import QtQuick
import "../config"

Item {
    id: root
    property color color: Theme.face
    property bool shadow: false
    property int shadowSize: Theme.u * 2
    property color shadowColor: Qt.alpha(Theme.shadow, Theme.shadowAlpha)
    property int bevel: 1
    readonly property int inset: 1
    default property alias content: inner.data

    Rectangle {
        visible: root.shadow
        anchors.fill: parent
        anchors.margins: -root.shadowSize
        color: "transparent"
        border.width: root.shadowSize
        border.color: Qt.alpha(root.shadowColor, 0.35)
        radius: body.radius + root.shadowSize
    }
    Rectangle {
        id: body
        anchors.fill: parent
        color: root.color
        border.width: 1
        border.color: Theme.edge
        radius: Theme.macLook ? Theme.u * 3 : 0
    }
    Item { id: inner; anchors.fill: parent; anchors.margins: root.inset }
}
