---
name: godot-label-billboard-bounds
description: Godot 4.5.1 Label3D billboard AABBs expand into cubes; generated text triangles retain the actual flat quad.
metadata:
  type: observation
  subject: Godot 4.5.1 stable, headless, macOS
  observed: 2026-10-30
  status: active
  recheck_after_days: 90
---

## Observed

Enabling Label3D billboarding changes its local AABB from a flat text rectangle to a cube. Projecting that box as though it were the text produces false screen-clipping results. `generate_triangle_mesh().get_faces()` retains the same six flat text vertices in both modes.

## Evidence

Measured on Godot 4.5.1.stable.official.f62fdbde1 with a single Label3D, text `999`, font size 110, pixel size 0.0055, and two process frames after each billboard-mode change. Disabled returned position (-0.517, -0.41525, 0), size (1.034, 0.8305, 0). Enabled returned position (-0.517, -0.517, -0.517), size (1.034, 1.034, 1.034). Generated vertices stayed at x ±0.517, y ±0.41525, z 0. No rendered capture was used.

A combat-layout probe initially reported 246 failing projected box corners and a minimum y of -225 px. Using actual text quads reduced this to 36 failing vertices and -26 px, distinguishing real text clipping from the oversized culling bounds. The [Label3D reference](https://docs.godotengine.org/en/4.5/classes/class_label3d.html#class-label3d-method-generate-triangle-mesh) documents generated text vertices but does not describe this billboard AABB expansion.

## Re-check

Create the label described above in a minimal SceneTree. Print `get_aabb()` and `generate_triangle_mesh().get_faces()` after two process frames with billboarding disabled, then enabled. Run the current binary headlessly with an explicit writable log path. If the enabled AABB remains flat or generated vertices change with billboard mode, revise this observation for that version.

## Apply

For text framing checks, project generated text vertices through the camera-facing basis and the label scale. Include the outline separately. Use the AABB for culling, not as exact visible lettering. This is a small geometry-query cost and does not establish rendered appearance or frame rate.

## History

- 2026-10-30 — Codex measured the disabled/enabled comparison while fixing combat-text framing and recorded the distinction.
