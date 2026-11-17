pragma Singleton
import QtQuick
import Quickshell
import Quickshell.Hyprland

Singleton {
    readonly property string primaryName: Hyprland.focusedMonitor ? Hyprland.focusedMonitor.name : (Quickshell.screens.length ? Quickshell.screens[0].name : "")
    function screenByName(name) {
        for (var i = 0; i < Quickshell.screens.length; ++i)
            if (Quickshell.screens[i].name === name) return Quickshell.screens[i]
        return null
    }
}
