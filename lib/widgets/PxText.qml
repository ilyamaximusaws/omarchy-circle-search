import QtQuick
import "../config"

Text {
    property string kind: "body"
    property bool dim: false
    color: dim ? Theme.textDim : Theme.text
    font.family: kind === "mono" ? Theme.fontMono : kind === "body" ? Theme.fontBody : Theme.fontTitle
    font.pixelSize: kind === "tiny" ? Theme.sizeTiny : kind === "mono" ? Theme.sizeMono : kind === "title" ? Theme.sizeTitle : kind === "big" ? Theme.sizeBig : kind === "huge" ? Theme.sizeHuge : Theme.sizeBody
    verticalAlignment: Text.AlignVCenter
    textFormat: Text.PlainText
}
