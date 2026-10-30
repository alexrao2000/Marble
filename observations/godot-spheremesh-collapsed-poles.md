---
name: godot-spheremesh-collapsed-poles
description: Godot SphereMesh includes collapsed pole triangles that need filtering before strict topology and normal checks.
metadata:
  type: observation
  subject: Godot 4.5.1 stable SphereMesh
  observed: 2026-10-29
  status: active
  recheck_after_days: 90
---

## Observed

A full SphereMesh with radius 1, height 2, 12 radial segments and 4 rings produced 120 indexed triangles. After scaling to a small palm, 24 triangles at the two poles had zero or numerically negligible area. Their geometric normals could not satisfy an outward-winding assertion. The remaining triangles retained outward normals. The [4.5 SphereMesh property documentation](https://docs.godotengine.org/en/4.5/classes/class_spheremesh.html) describes subdivisions but does not state this topology detail.

## Evidence

An isolated headless probe inspected each indexed triangle after the palm scale (0.046, 0.050, 0.027). It found twelve collapsed triangles at each pole in both mirrored hand builds. All failures came from the sphere portion, not the original finger lofts. Filtering these triangles while copying the primitive reduced each combined hand from 300 to 276 triangles. Strict nonzero-area, outward-winding and closed-edge checks then passed for both hands, followed by 900 live caster pose samples.

## Re-check

Create that SphereMesh, retrieve ARRAY_VERTEX and ARRAY_INDEX, and transform vertices by Basis.from_scale(Vector3(.046,.050,.027)). For each indexed triple a,b,c, count `(c-a).cross(b-a).length_squared() < 1e-18`. Godot 4.5.1 measured 24 of 120. Run this in a headless SceneTree with the current engine; no renderer or project assets are required. If the count becomes zero, recheck strict winding and closed-edge checks before retiring this observation.

## Apply

When converting a sphere primitive into custom geometry that requires nondegenerate triangles, skip collapsed triples before generating tangents or validating manifold edges. Use a threshold appropriate to the destination scale. This is unnecessary for ordinary rendering of an untouched SphereMesh; do not rewrite every sphere in a project solely because of this observation.

## History

- 2026-10-29 — Codex measured collapsed pole triangles during procedural hand construction and verified filtered topology with closed-edge and outward-normal checks.
