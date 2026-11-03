# Scroll Indicator

A Noctalia bar widget for Hyprland's **scrolling layout**. On a workspace that uses the scrolling
layout it shows one dot per column: **●** for the focused column, **○** for the rest. On every other
layout it hides itself.

```
○ ● ○ ○      ← 4 columns, the 2nd is focused
```

Hover for "Scrolling: column 2 of 4".

## Why

Hyprland's scrolling layout has no built-in position indicator: you can't tell how many windows
are off-screen or where you are in the row. This adds one.

## Example setup

Built for one scrolling workspace with **2/3-width columns** on a large (4K) screen, used as a
parking spot for apps you want to keep open but don't need to look at often (Hyprland has no
minimize). Each window keeps plenty of room, and a slice of the next column stays visible.

```lua
-- Hyprland Lua config: workspace 10 (the ALT+0 key) uses the scrolling layout
hl.workspace_rule({ workspace = "10", layout = "scrolling", persistent = true })

hl.config({
  scrolling = {
    column_width = 2/3,
    follow_focus = true,
  },
})
```

The widget works with any column width and on any workspace using the scrolling layout.

## Install

```sh
noctalia msg plugins source add scroll-indicator git https://github.com/83raiders/hypr-scroll-indicator
noctalia msg plugins enable 83raiders/scroll-indicator
```

Then add the widget to a bar section in `settings.toml`:

```toml
[bar.default]
center = [ "workspaces", "scroll", "clock" ]

[widget.scroll]
type = "83raiders/scroll-indicator:dots"
```

## Requirements

- Hyprland **0.56+** (uses the `tiledLayout` field and workspace names from `hyprctl -j`)
- `hyprctl` (ships with Hyprland)
- `socat` (for live updates from Hyprland's event socket)

## What it runs

Everything the plugin does, for review:

| Process | When | Why |
|---|---|---|
| `sh -c "hyprctl -j activeworkspace; hyprctl -j activewindow; hyprctl -j clients"` | on each relevant Hyprland event, plus every 2 s as a safety net (every 0.4 s if `socat` is missing) | read the workspace layout, focused window and window positions |
| `socat -U - UNIX-CONNECT:$XDG_RUNTIME_DIR/hypr/$HYPRLAND_INSTANCE_SIGNATURE/.socket2.sock` | once, while the widget is loaded | listen to Hyprland's read-only event socket so the dots update instantly |

No network access and no file writes.

## Credit

Idea from [jtams/waybar-hyprland-scroll-indicator](https://github.com/jtams/waybar-hyprland-scroll-indicator)
(a Go module for Waybar). This is an independent Luau implementation for Noctalia.
