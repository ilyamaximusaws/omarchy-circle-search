pragma Singleton
import QtQuick
import Quickshell
import Quickshell.Hyprland

// Keeps the upstream Niri-facing name while sourcing native Hyprland objects.
Singleton {
    readonly property string focusedOutput: Hyprland.focusedMonitor ? Hyprland.focusedMonitor.name : ""

    function windowRects(name, frameScale) {
        var screen = Shell.screenByName(name)
        var monitor = screen ? Hyprland.monitorFor(screen) : null
        var workspace = monitor ? monitor.activeWorkspace : null
        if (!monitor || !workspace) return []
        var info = monitor.lastIpcObject || ({})
        var ox = Number(info.x) || 0, oy = Number(info.y) || 0
        var k = Number(frameScale) || 1
        var out = []
        var list = Hyprland.toplevels ? Hyprland.toplevels.values : []
        for (var i = 0; i < list.length; ++i) {
            var top = list[i]
            if (!top.workspace || top.workspace.id !== workspace.id) continue
            var ipc = top.lastIpcObject || ({})
            if (!ipc.at || !ipc.size) continue
            out.push({
                x: Math.round((Number(ipc.at[0]) - ox) * k),
                y: Math.round((Number(ipc.at[1]) - oy) * k),
                w: Math.round(Number(ipc.size[0]) * k),
                h: Math.round(Number(ipc.size[1]) * k),
                title: String(ipc.title || ""),
                app_id: String(ipc["class"] || ""),
                focused: top === Hyprland.activeToplevel
            })
        }
        return out
    }
}
