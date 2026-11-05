---
name: quaternius-standard-eye-normal-uri
description: The Standard base-character glTF names a missing eye normal texture; the correct Godot texture is included without the extra _png suffix.
metadata:
  type: observation
  subject: Quaternius Universal Base Characters Standard archive fdbf1804c90dfc1ea03e992bff7da2dfd1a79318e13270a660180f9308455f40
  observed: 2026-11-05
  status: active
  recheck_after_days: 90
---

## Observed

The female Superhero full-body glTF under `Base Characters/Godot - UE/` references `T_Eye_Normal_png.png`, which does not exist in the supplied Standard ZIP. That folder contains `T_Eye_Normal.png` instead. The archive README does not mention this mismatch.

## Evidence

Inspected the ZIP directory and parsed the glTF images array locally. The archive SHA-256 is `fdbf1804c90dfc1ea03e992bff7da2dfd1a79318e13270a660180f9308455f40`. Both the adjacent `T_Eye_Normal.png` and the copy under `Base Characters/Textures/Normals Unity - Godot/` hash to `9ed61f7726a54fe346a78b9e5a18905d8e2b88f86235d97f53cd207a26f3f8c7`. The generic Textures copy has a different hash, so blindly taking the first filename match could select the other normal convention.

## Re-check

Open the current Standard ZIP with Python zipfile, read the female full-body glTF, and resolve each images[].uri relative to its archive folder. Verify the extra-suffix URI is absent, the adjacent suffix-free file exists, and its SHA-256 matches the explicitly marked Unity/Godot normal map. If a new archive corrects the URI, record the new hash and retire this entry.

## Apply

For this verified archive, map the missing eye URI to the adjacent `T_Eye_Normal.png` during asset preparation. Preserve the source archive and document the correction with generated assets. Do not replace arbitrary missing image paths or select the generic normal-map copy by basename alone. No image pixels need editing.

## History

- 2026-11-05 — Codex measured the missing URI and matching Godot normal-map copies while preparing Poem's local authored-model assets.
