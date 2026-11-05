---
name: godot-paused-crossfade-seek
description: Godot 4.5.1 paused AnimationPlayer seeks update clip time without progressing an active crossfade; explicit advance progresses the blend.
metadata:
  type: observation
  subject: Godot 4.5.1 stable f62fdbde1 AnimationPlayer
  observed: 2026-11-05
  status: active
  recheck_after_days: 90
---

## Observed

After starting a clip with a nonzero custom blend and pausing its AnimationPlayer, repeated `seek(time, true, true)` calls changed the clip cursor but retained the outgoing pose. Calling `advance(delta)` before the seek progressed the crossfade even while paused. This mattered for a jog sampled from ground distance rather than wall time.

## Evidence

A minimal SceneTree probe created one Node3D and two one-second value animations targeting `.:position:x`: old was constantly 0, new constantly 10. It called `play("old")`, `advance(0)`, `play("new", .1)`, `pause()`, then `seek(.5, true, true)`. Position remained 0. Calling `advance(.1)` then the same seek yielded 10. No skeleton, imported resource, rendering or frame wait was involved. Temporary probe/log: `/private/tmp/poem-paused-crossfade.gd` and `/private/tmp/poem-paused-crossfade.log` (may expire).

In Poem's imported jog, seek-only sampling similarly held the outgoing foot pose while the actor moved 0.6 m. Advancing the blend by the clip-time equivalent of travelled distance restored the changing bone pose. The Godot 4.5 AnimationPlayer reference documents seek's update flags and play's blend parameter, but does not explicitly describe their interaction with a paused active crossfade.

## Re-check

Repeat the two constant-value animation comparison above with only `advance(.1)` added between the two seeks. If the first seek now reaches 10 without advance, this observation no longer holds for that version.

## Apply

For distance-driven paused playback that retains crossfades, advance the blend clock by the clip-time equivalent of actual travel before seeking the desired clip phase. For a pure fixed-pose query, avoid an active crossfade instead. Do not assume a changed animation cursor proves the rendered bone/property pose changed. Explicit advance can also process animation events; restrict this approach to appropriate clips.

## History

- 2026-11-05 — Codex isolated the paused-crossfade behavior with a two-property-clip probe after measuring a frozen source-jog foot pose.
