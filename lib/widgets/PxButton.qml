import QtQuick
import "../config"

Item {
    id: root
    property string text: ""
    property string icon: ""
    property bool checked: false
    property bool checkable: false
    property bool accent: false
    property bool compact: false
    property bool flat: false
    property int iconPixel: Theme.u
    property alias hovered: mouse.containsMouse
    property alias pressed: mouse.pressed
    readonly property bool down: mouse.pressed || checked
    signal clicked
    signal rightClicked

    implicitWidth: row.implicitWidth + Theme.u * (compact ? 12 : 18)
    implicitHeight: Math.max(row.implicitHeight + Theme.u * 5, Theme.u * (compact ? 12 : 16))
    opacity: enabled ? 1 : 0.45

    Rectangle {
        anchors.fill: parent
        radius: Theme.u * 2
        color: root.down || root.accent ? Theme.accent : mouse.containsMouse ? Theme.mix(Theme.face, Theme.accent, 0.18) : Theme.face
        border.width: 1
        border.color: root.down || root.accent ? Theme.accent : Theme.edge
    }
    Row {
        id: row
        anchors.centerIn: parent
        spacing: Theme.u * 2
        PxIcon {
            visible: root.icon !== ""
            name: root.icon || "heart"
            pixel: root.iconPixel
            ink: root.down || root.accent ? Theme.selectText : Theme.text
            anchors.verticalCenter: parent.verticalCenter
        }
        PxText {
            visible: root.text !== ""
            text: root.text
            color: root.down || root.accent ? Theme.selectText : Theme.text
            font.bold: root.checked
            anchors.verticalCenter: parent.verticalCenter
        }
    }
    MouseArea {
        id: mouse
        anchors.fill: parent
        hoverEnabled: true
        acceptedButtons: Qt.LeftButton | Qt.RightButton
        cursorShape: Qt.PointingHandCursor
        onClicked: e => {
            if (e.button === Qt.RightButton) { root.rightClicked(); return }
            if (root.checkable) root.checked = !root.checked
            root.clicked()
        }
    }
}
