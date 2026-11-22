---
name: godot-tween-queued-owner-custom-step
description: Godot 4.5.1 custom_step can return true after the final callback queues its bound owner for deletion.
metadata:
  type: observation
  subject: Godot 4.5.1 Tween on macOS headless
  observed: 2026-11-21
  status: active
  recheck_after_days: 90
---

## Observed

A paused, node-bound Tween returned `true` from `custom_step` after its final callback called `queue_free()` on the owner. The owner was already queued for deletion and the target property had reached its endpoint. The return value alone did not prove the intended lifetime/timing effect had failed.

## Evidence

Poem's map-arrow tween has a linear property step followed by an owner `queue_free()` callback. With travel endpoint 1.35, duration 0.162 seconds and speed scale 1.35, manual steps of 0.11 and 0.02 seconds produced:

- First step: return true, progress 1.23749994635582, owner not queued.
- Second step: return true, progress 1.35, owner queued.

A separate ordinary run reached its finished signal. The focused probe was `/private/tmp/poem-map-timing-probe.gd`; its behavior was measured with the Godot 4.5.1 stable macOS binary. The failed package assertion combined an expected false return with a queued-owner assertion; the latter condition was already satisfied. No game timing change was needed.

The [4.5 Tween documentation](https://docs.godotengine.org/en/4.5/classes/class_tween.html#class-tween-method-custom-step) describes true as remaining unfinished tweeners, but does not detail this queued-owner case. Scope this observation to bound-owner deletion; do not infer that all final callbacks behave this way.

## Re-check

Create a Node3D owner, bind a Tween with `owner.create_tween()`, tween a numeric property to 1.35 over 0.162 seconds, append `owner.queue_free`, set speed scale to 1.35, and pause. Step 0.11 then 0.02 seconds, printing the return values, property and `is_queued_for_deletion()`. Await a process frame and inspect a WeakRef to establish actual cleanup. Use an explicit writable Godot log file.

## Apply

For effects whose final callback deletes their owner, verify the property endpoint and queued state, then WeakRef release after a frame. Do not require `custom_step` to return false as an additional cleanup assertion. This changes only the test and is inexpensive.

## History

- 2026-11-21 — Codex measured the queued-owner return during Poem's packaged map-projectile check and recorded the narrower assertion guidance.
