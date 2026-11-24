---
name: godot-viewport-before-control-resize
description: An early Godot 4.5.1 Viewport.size_changed listener can see the new viewport size while an anchored Control still has its old dimensions.
metadata:
  type: observation
  subject: Godot 4.5.1 SubViewport and Control resize signals on macOS
  observed: 2026-11-24
  status: active
  recheck_after_days: 90
---

## Observed

A callback registered on a SubViewport before its anchored controls were attached saw the new viewport height of 640 with both controls still at height 960. The nested control's resized callback saw height 640 for the viewport and both controls.

## Evidence

An isolated Godot 4.5.1 headless scene resized a 720 × 960 SubViewport to 720 × 640. It contained a CanvasLayer, a full-rect Control and a nested full-rect Control. The early viewport subscriber printed sizes `[720×640, 720×960, 720×960]`. The nested control's callback printed `[720×640, 720×640, 720×640]`. In Poem the first callback could fit the battle camera to the old forecast card positions after a resize. Refitting after the forecast layout signal passed when resizing in both directions. The [Viewport signal](https://docs.godotengine.org/en/4.5/classes/class_viewport.html#class-viewport-signal-size-changed) and [Control signal](https://docs.godotengine.org/en/4.5/classes/class_control.html#class-control-signal-resized) describe their own size changes.

## Re-check

Create a 720 × 960 SubViewport and connect its size_changed callback before adding a CanvasLayer and nesting two Controls with PRESET_FULL_RECT. Connect resized on the inner Control. Set the viewport to 720 × 640 and record all three dimensions in each callback. Use headless mode with an explicit writable log file if running in a sandbox.

## Apply

Update geometry that depends on a particular Control after that Control has laid out its children. A callback that only needs the viewport's new dimensions can still use the viewport signal directly.

## History

- 2026-11-24 — Codex isolated the order while fixing a forecast camera that retained the preceding portrait layout after resize.
