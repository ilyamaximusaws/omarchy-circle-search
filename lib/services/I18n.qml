pragma Singleton
import QtQuick

QtObject {
    function t(ru, en) {
        return String(Qt.locale().name).toLowerCase().indexOf("ru") === 0 ? ru : en
    }
}
