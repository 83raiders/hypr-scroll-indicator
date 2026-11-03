# Scroll Indicator

A Noctalia bar widget for Hyprland's **scrolling layout**. On a workspace that uses the scrolling
layout it shows one dot per column: **●** for the focused column, **○** for the rest. On every other
layout it hides itself.

```
○ ● ○ ○      ← 4 columns, the 2nd is focused
```

Hover for "Scrolling: column 2 of 4".

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
