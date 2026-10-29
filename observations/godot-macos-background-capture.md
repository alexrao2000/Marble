---
name: godot-macos-background-capture
description: Godot native capture can wait indefinitely for frame_post_draw when its macOS window is covered; an explicit force_draw completes the capture
metadata:
  type: observation
  subject: Godot 4.5.1 Compatibility renderer on macOS 27.0.1 with Apple M4
  observed: 2026-10-29
  status: active
  recheck_after_days: 30
---

## Observed

A Godot capture harness continued processing timers but stopped at an awaited `RenderingServer.frame_post_draw` while its native window was in the background. Replacing that wait with `RenderingServer.force_draw(false)` allowed the same scene to save a screenshot and exit. No game rendering or animation change was needed.

## Evidence

In the fe-clone visual workshop, native 3D capture logged “renderer ready” and then waited for more than 40 seconds with no screenshot. Sampling the Godot process showed normal scene processing and frame delay, rather than a graphics-driver wait. The same scene and image-readback code completed immediately after the harness explicitly drew a frame. A headless gameplay suite also passed while the native screenshot wait was stalled. Repeated native 2D and 3D captures with explicit drawing completed successfully.

This establishes a capture-harness workaround. It does not establish a game FPS result or claim that every covered window suspends redraws. Foreground and window-occlusion behavior were not exhaustively tested.

## Re-check

Use a minimal Godot scene with a SubViewport. Launch with `open -g` to preserve application focus. Log before waiting for `frame_post_draw` and apply a five-second external deadline. Compare that run with a second run calling `RenderingServer.force_draw(false)` before `get_texture().get_image().save_png(...)`. Keep the renderer, window size, and scene identical. Record whether the first wait stalls and the explicit draw completes.

## Apply

For background native screenshots, explicitly draw a frame and then read the viewport image. Keep app launches in the background with `open -g`. Treat window-occluded FPS counters as unsuitable for a gameplay performance claim.

## History

- 2026-10-29: Codex recorded the timer, sample-stack, and explicit-draw comparison during the reusable sprite workshop build.
