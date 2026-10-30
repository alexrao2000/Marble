---
name: godot-headless-multimesh-readback
description: Godot 4.5.1 headless MultiMesh individual transform/color getters return defaults; bulk buffers retain submitted values.
metadata:
  type: observation
  subject: Godot 4.5.1 stable, headless dummy renderer, macOS
  observed: 2026-10-29
  status: active
  recheck_after_days: 90
---

## Observed

Under `--headless`, a MultiMesh configured for 3D transforms and colors returned an identity transform and black opaque color after explicit per-instance writes. Assigning a PackedFloat32Array to `buffer` and reading `buffer` back retained the exact submitted array. This is not evidence about rendered output.

## Evidence

Measured with Godot 4.5.1.stable.official.f62fdbde1 on 2026-10-29. An atmosphere test's elapsed time advanced and its Node3D was visible, but individual readback stayed at defaults. A separate minimal SceneTree reproduced it: configure one instance, write translation (3,4,5) and color (0.2,0.4,0.6,0.8), then read the individual values. Defaults returned. Submitting `[1,0,0,3,0,1,0,4,0,0,1,5,.2,.4,.6,.8]` as `buffer` round-tripped exactly. No rendered/native capture was used.

The [4.5 dummy mesh storage source](https://raw.githubusercontent.com/godotengine/godot/4.5-stable/servers/rendering/dummy/storage/mesh_storage.h) has no-op individual setters and default-returning individual getters, while bulk buffer functions have implementations. The public MultiMesh class reference did not describe this headless distinction.

## Re-check

Run a minimal SceneTree with the current Godot binary and `--headless`: create MultiMesh, set `transform_format=TRANSFORM_3D`, `use_colors=true`, `instance_count=1`; write a nonidentity transform and nondefault color, then print their getters. Compare with a full 16-float transform/color buffer round trip. If individual getters now retain their data, this observation is no longer applicable to that binary.

## Apply

Do not assert headless animation correctness through individual MultiMesh readback. Validate the actual bulk submission buffer or explicit calculated transforms/colors. Bulk upload can also reduce renderer calls. Verify buffer layout against the engine's current API; this observation does not establish a layout contract for every version/backend. Runtime data checks still do not verify rendered appearance or frame rate.

## History

- 2026-10-29 — Codex measured individual versus bulk readback on Godot 4.5.1 and recorded the headless distinction.
