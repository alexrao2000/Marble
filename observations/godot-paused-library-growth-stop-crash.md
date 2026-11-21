---
name: godot-paused-library-growth-stop-crash
description: Godot 4.5.1 can crash in AnimationPlayer.stop after a paused player's library grows from eleven to thirteen animations; stopping before mutation avoids the measured failure.
metadata:
  type: observation
  subject: Godot 4.5.1 stable f62fdbde1 AnimationPlayer on macOS headless
  observed: 2026-11-21
  status: active
  recheck_after_days: 90
---

## Observed

Adding animations to a library while its player retained a paused assignment could make the subsequent `stop()` crash with signal 11 in `AnimationPlayer::seek_internal` / `_stop_internal`. The controlled reproduction started with eleven animations and added two. Stopping the player before adding the same two animations passed. A smaller one-to-two-animation comparison passed in either order, so a small successful mutation is not evidence that a larger library is safe.

## Evidence

A standalone SceneTree probe used only a Node3D named Subject, an AnimationPlayer and an AnimationLibrary. The one-second source animation had a TYPE_VALUE track targeting `Subject:position`, with Vector3.ZERO at time 0 and Vector3.ONE at time 1. Ten copies named fill0 through fill9 brought the library to eleven entries. The probe called `play("source", 0)`, `seek(.5, true, true)` and `pause()`, and verified the subject position was Vector3.ONE * .5. Adding copies named copy and copy2, then calling `stop()`, produced the native crash. Moving `stop()` immediately before the two additions completed with exit 0. There was no imported scene, skeleton, GPU renderer, frame delay or game code in this comparison.

Temporary evidence (may expire): `/private/tmp/poem-animation-library-probe.gd`, `/private/tmp/poem-library-add-first-13.log`, and `/private/tmp/poem-library-stop-first-13.log`. A caster-clip baking experiment independently crashed at the same stop call after adding two variants to its eleven-entry library. Library growth or cache invalidation is a possible explanation, not an established engine root cause.

The [Godot 4.5 AnimationLibrary reference](https://docs.godotengine.org/en/4.5/classes/class_animationlibrary.html) describes adding animations without this ordering restriction. The [AnimationPlayer reference](https://docs.godotengine.org/en/4.5/classes/class_animationplayer.html) describes stop and pause but does not document this measured library-growth crash.

## Re-check

Recreate the eleven-entry library and paused value-animation probe above in the engine version in use. Compare add-two-then-stop against stop-then-add-two in separate processes, always using an explicit writable `--log-file`. If add-two-then-stop consistently completes without crashing, amend or retire the observation for that tested version. Keep the small-library control separate; it did not reproduce the failure here.

## Apply

When baking or replacing clips after sampling an AnimationPlayer, stop playback before mutating its AnimationLibrary. If more sampling is needed, select the source clip again after the mutation. Preserve or restore sampled bone/property state separately where the caller needs it. This ordering costs a stop/reselection during setup and avoids relying on paused playback caches across library growth.

## History

- 2026-11-21 — Codex isolated the native stop crash with a value-only eleven-to-thirteen-animation probe and verified the stop-before-mutation control.
