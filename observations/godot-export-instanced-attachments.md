---
name: godot-export-instanced-attachments
description: Godot 4.5.1 exported glTF wrappers lose nested added attachments without an editable instance declaration.
metadata:
  type: observation
  subject: Godot 4.5.1 stable f62fdbde1 scene export
  observed: 2026-11-05
  status: active
  recheck_after_days: 90
---

## Observed

A hand-authored `.tscn` wrapper instantiated a glTF scene as `Rig` and added BoneAttachment3D children below `Rig/Armature/Skeleton3D`. Direct project loading retained the weapon, chest and face attachments. Loading the same wrapper from a release-exported Web PCK omitted every added attachment. Appending `[editable path="Rig"]` to each wrapper retained them in the exported PCK.

## Evidence

Measured in Poem with female and male Quaternius glTF wrappers. Both passed live project tests for wrist attachment, five sockets, animation replay and 720 viewport/pose layouts. The exported package failed the actual debug-preview smoke check. A small external SceneTree script loaded each wrapper from the PCK with `--path /private/tmp --main-pack <absolute PCK>`: the model adapter reported `Missing socket: impact` for both. Printing the exported scene tree showed the original eight skinned meshes and AnimationPlayer, but none of the added attachments. No missing-resource or script errors were emitted.

The only source change for the comparison was adding `[editable path="Rig"]` to each `.tscn`. Re-exporting Web and repeating the external adapter probe returned an actor and an empty issues list for both genders. Logs: `/private/tmp/poem-export-study-diagnostic-engine.log` (failure), `/private/tmp/poem-export-study-tree.log` (missing nodes), `/private/tmp/poem-export-study-fixed-engine.log` (success). These temporary logs may expire; the repository's `tests/test_export.gd` now exercises the actual packaged debug model studies.

The Godot 4.5 PackedScene reference describes owned-node packing and edit states, but does not describe this observed direct-load/export discrepancy for nested additions in hand-authored imported-scene wrappers. This observation is scoped to the measured structure/version, not all instancing or all export formats.

## Re-check

Create or use a wrapper with an imported glTF child `Rig` and a Marker3D/BoneAttachment3D added below one of its descendants. Confirm direct instantiation has the added node. Export Web and load the wrapper from its PCK using an external script and a different working directory. Compare absence/presence with only the editable declaration removed/added. Do not infer export correctness from direct project instantiation.

## Apply

Keep `[editable path="Rig"]` on these wrappers, or use editor-authored equivalent instance editability. Verify socket paths from the exported PCK. This adds a scene editability declaration and has no simulation or save-format effect.

## History

- 2026-11-05 — Codex measured the discrepancy on two independent wrappers, isolated the editable declaration, verified both packaged adapters and recorded it.
