---
name: godot-headless-pointer-coordinates
description: Godot headless pointer injection uses the physical window, which can be 64 by 64 despite a larger logical viewport.
metadata:
  type: observation
  subject: Godot 4.5.1 headless on macOS, canvas_items stretching
  observed: 2026-10-30
  status: active
  recheck_after_days: 30
---

## Observed

In Poem's Godot 4.5.1 headless tests, the root Window started at 64×64 while its visible logical viewport and UI were 1440×900. Input.parse_input_event transformed injected mouse coordinates from that physical window into the stretched logical viewport. Injecting the intended logical point (889, 450) therefore delivered (20002.5, 9855), outside the viewer. Keyboard injection was unaffected.

Setting root.size to Vector2i(1440, 900) before creating the app made the same injected event arrive at (889, 450), and the actual unhandled-input handler changed viewer zoom from 1.0 to 0.88. No product input code change was required for this discrepancy.

## Evidence

A temporary SceneTree probe loaded the local app and attached a Node logging both _input and _unhandled_input. It printed root.size, root.get_visible_rect(), UI size, viewer clear bounds and the received event coordinates. The only difference between controlled runs was explicitly sizing the root Window. Both handlers received the same transformed coordinates in each run; calling the handler directly with the logical point worked in the first run, isolating dispatch coordinate conversion from viewer logic.

Project settings were viewport_width=1440, viewport_height=900, window/stretch/mode="canvas_items". Engine: 4.5.1.stable.official.f62fdbde1. Logs: /private/tmp/poem-viewer-input-probe.log and /private/tmp/poem-viewer-input-probe-sized.log. These temporary logs may expire.

The larger gesture audit also crashed in Viewport::_gui_input_event when its synthetic sequence sent repeated wheel-up presses followed by wheel-down presses without releases. This occurred with both Window.push_input and Input.parse_input_event, even after fixing the window size. Adding a separate matching release event after each wheel press made the same complete audit pass. This establishes a valid test-event sequence, not a general defect in normal hardware input. A small paired-event probe and the complete 33,696-layout/gesture audit both exited successfully; actual tests instantiate a fresh event for each injection.

## Re-check

In a headless SceneTree test for a stretched 1440×900 project, log root.size and root.get_visible_rect(). Attach a Node with _input and _unhandled_input loggers, then inject a pressed InputEventMouseButton at (889, 450) through Input.parse_input_event followed by Input.flush_buffered_events. Compare the logged coordinates before and after setting root.size=Vector2i(1440,900) and awaiting a process frame. If initial physical and logical sizes already agree, the original environmental mismatch no longer applies.

## Apply

Set the test Window size explicitly before pointer-dispatch integration tests, or deliberately convert logical target coordinates into physical-window coordinates. Prefer actual dispatch for interaction checks; retain explicit SubViewport dimensions for projection-only tests. Do not infer that product mouse handling is broken from an off-window injected event. Use complete press/release pairs and fresh event instances when generating wheel input. These changes affect test setup only and do not alter production code.

## History

- 2026-10-30 — Codex measured the physical/logical mismatch and verified explicit Window sizing in a controlled comparison during Poem's viewer gesture work.

- 2026-10-30 — Codex isolated the additional synthetic-wheel issue: matching release events resolved the crash in the unchanged full gesture audit after Window sizing was already corrected.
