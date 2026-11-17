import QtQuick
import "../config"

Item {
    id: root
    property alias text: editor.text
    property alias readOnly: editor.readOnly
    property alias input: editor
    property string placeholder: ""
    property bool monospace: false
    property bool spell: false
    signal edited
    implicitHeight: Theme.u * 65
    implicitWidth: Theme.u * 180

    Rectangle {
        anchors.fill: parent
        color: Theme.sunken
        border.width: 1
        border.color: editor.activeFocus ? Theme.accent : Theme.edge
        radius: Theme.u
    }
    Flickable {
        id: flick
        anchors.fill: parent
        anchors.margins: Theme.u * 4
        clip: true
        contentWidth: width
        contentHeight: Math.max(height, editor.contentHeight)
        boundsBehavior: Flickable.StopAtBounds
        TextEdit {
            id: editor
            width: flick.width
            height: Math.max(flick.height, contentHeight)
            wrapMode: TextEdit.Wrap
            textFormat: TextEdit.PlainText
            selectByMouse: true
            color: Theme.text
            selectionColor: Theme.select
            selectedTextColor: Theme.selectText
            font.family: root.monospace ? Theme.fontMono : Theme.fontBody
            font.pixelSize: root.monospace ? Theme.sizeMonoSmall : Theme.sizeBody
            onTextChanged: root.edited()
            onCursorRectangleChanged: {
                if (cursorRectangle.y < flick.contentY) flick.contentY = cursorRectangle.y
                else if (cursorRectangle.y + cursorRectangle.height > flick.contentY + flick.height)
                    flick.contentY = cursorRectangle.y + cursorRectangle.height - flick.height
            }
        }
        PxText { visible: editor.text === ""; width: parent.width; text: root.placeholder; dim: true; wrapMode: Text.Wrap }
    }
}
