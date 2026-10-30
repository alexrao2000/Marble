---
name: godot-headless-gradient-readback
description: Godot 4.5.1 headless GradientTexture2D readback can be null after early RID/material binding, or stale after changes.
metadata:
  type: observation
  subject: Godot 4.5.1 stable official, headless dummy renderer on macOS
  observed: 2026-10-30
  status: active
  recheck_after_days: 30
---

## Observed

A valid, configured GradientTexture2D returned null from `get_image()` when its RID was requested, or it was assigned to a StandardMaterial3D, before the first image generation. Waiting four process frames did not repair readback. An otherwise identical texture read with `get_image()` first returned the expected image. Changing that texture's gradient afterward returned the previous image instead of updated pixels.

This was a headless data-readback result, not evidence that the rendered game shows a solid rectangle or a missing gradient. An isolated software asset preview had incorrectly treated the null image as an untextured quad.

## Evidence

A controlled 32 × 32 radial white-to-transparent gradient comparison on the same engine/process measured:

- Image first: non-null immediately and after four frames.
- `get_rid()` first: null immediately and after four frames.
- StandardMaterial3D `albedo_texture` assignment first: null immediately and after four frames.
- Image-first texture, then reverse its endpoint alphas: original corner alpha 0, readback corner alpha still 0, current `gradient.sample(1).a` equals 1.
- An ImageTexture created from a known Image retained its source pixels in the same environment.

The official [gradient implementation](https://raw.githubusercontent.com/godotengine/godot/4.5-stable/scene/resources/gradient_texture.cpp) requests a placeholder from `get_rid()` and replaces an existing texture during updates. The [dummy texture storage](https://raw.githubusercontent.com/godotengine/godot/4.5-stable/servers/rendering/dummy/storage/texture_storage.h) implements `texture_replace` by freeing the replacement without transferring its image. This supports the measured distinction. The public Texture2D docs' general invalid-texture/null note does not describe this valid-resource, headless order dependency.

## Re-check

Run a temporary SceneTree script with `--headless --log-file /private/tmp/gradient-check.log`. Build three identical GradientTexture2D resources, each with width/height 32, a two-point `[Color.WHITE, Color(1,1,1,0)]` Gradient, radial fill, `fill_from=(.5,.5)` and `fill_to=(1,.5)`.

1. Call the first resource's `get_image()` before any binding.
2. Call the second resource's `get_rid()` before `get_image()`.
3. Assign the third to a retained StandardMaterial3D's `albedo_texture` before `get_image()`.
4. Print whether all three return images immediately and after four `process_frame` waits.
5. Reverse the first gradient's colors, then compare its readback corner alpha with `gradient.sample(1).a`.

The original probe is `/private/tmp/poem-gradient-readback.gd` when available; the instructions above are sufficient to recreate it. A headless implementation returning fresh images in all cases falsifies this observation for that version.

## Apply

For headless geometry/artwork studies, inspect the configured gradient or generate a CPU sample from its actual fill/offset/color properties. For an immutable gradient, a first image snapshot before RID/material binding also supplies valid pixels on this measured engine. Never substitute an opaque fallback for missing readback and treat it as rendered evidence. Do not rewrite runtime materials merely to satisfy this dummy-renderer artifact. Cost: a small one-time CPU image snapshot or gradient sampling in the inspection helper.

## History

- 2026-10-30: Codex measured image-first/RID-first/material-first and post-mutation controls while inspecting an original Poem spell asset; recorded the null/stale readback limitation and the misleading software-preview fallback.
