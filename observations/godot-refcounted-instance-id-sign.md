---
name: godot-refcounted-instance-id-sign
description: Godot 4.5.1 exposes valid reference-counted object IDs as negative signed GDScript integers.
metadata:
  type: observation
  subject: Godot 4.5.1 GDScript Object.get_instance_id on macOS
  observed: 2026-11-24
  status: active
  recheck_after_days: 90
---

## Observed

A live `AudioStreamPlayback` and a plain `RefCounted` both returned negative IDs to GDScript. Their enclosing `AudioStreamPlayer` node returned a positive ID. Passing the negative playback ID to `instance_from_id()` returned the same live object.

## Evidence

A headless Godot 4.5.1 probe created an `AudioStreamPlayer`, played a local WAV, and compared the player, playback and plain reference-counted object in the same process. One run returned `24628954475`, `-9223372012041271954` and `-9223372012007717520`, respectively. The positive-only check in Poem's campaign replay discarded evidence for a live finale decoder.

The [4.5 Object method documentation](https://docs.godotengine.org/en/4.5/classes/class_object.html#class-object-method-get-instance-id) describes identity and lifetime. The [4.5.1 implementation](https://github.com/godotengine/godot/blob/4.5.1-stable/core/object/object_id.h#L38-L54) places the reference-counted flag in the high bit and exposes a signed 64-bit conversion.

## Re-check

Create `Node.new()` and `RefCounted.new()` in GDScript. Compare their IDs and check that `instance_from_id(ref.get_instance_id()) == ref`. Release the node after the check. Repeat with `get_stream_playback()` if investigating audio.

## Apply

Check object presence and compare identities directly. An ID used as an optional token can use zero as its sentinel. If a test report serializes a live ID, write it as a string and keep its comparison scoped to that process.

## History

- 2026-11-24 — Codex isolated a full-campaign audio assertion to the sign assumption, measured three object types, and verified the version-pinned implementation.
