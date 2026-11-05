---
name: godot-physics-frame-input-pulses
description: Releasing and pressing an action at every physics_frame boundary can erase its just-pressed edge before a character sees it.
metadata:
  type: observation
  subject: Godot 4.5.1 headless input injection with fixed-fps 60 on macOS
  observed: 2026-11-04
  status: active
  recheck_after_days: 90
---

## Observed

A SceneTree coroutine that released and re-pressed an action on every physics_frame signal kept the action held but never let a CharacterBody3D observe is_action_just_pressed. Keeping each injected press across three physics frames delivered the edge and started the attack on the next tick.

## Evidence

A 30-frame probe in Coffin Princess called Input.action_release("heavy") and Input.action_press("heavy") before awaiting each physics_frame. Each immediate query printed just=false, and the character remained idle with 100 stamina. With the same calls only when the frame index modulo three was zero, the following frame printed just=true, the character entered attack, and stamina became 66. Both runs used the same scene and engine with --headless --fixed-fps 60. Held movement was unaffected. This is an injection-order issue, not evidence that hardware keyboard presses fail.

The Input reference describes simulated presses and frame/physics-tick queries but does not specify this coroutine scheduling edge: https://docs.godotengine.org/en/4.5/classes/class_input.html.

## Re-check

Create an action and a node that increments a counter in _physics_process when is_action_just_pressed is true. From a SceneTree coroutine, release and press the action at each physics_frame boundary for 30 frames. Repeat with the pulse issued only every third frame and held between pulses. Compare the counter and immediate just-pressed queries. If both modes reliably deliver edges, narrow or retire this observation.

## Apply

Hold injected button presses across complete physics ticks. For scripted combat controllers, make decisions every third physics frame and count actual state transitions, not attempted presses. Do not infer combat difficulty from a controller that erases its own attack edges.

## History

- 2026-11-04 — Codex measured per-boundary pulses against three-frame holds and recorded the distinction.
