---
name: godot-web-splash-imported-pixels
description: Godot Web exports can write the imported boot splash pixels into their external PNG, including lossy texture import changes.
metadata:
  type: observation
  subject: Godot 4.5.1 stable official Web exporter
  observed: 2026-11-23
  status: active
  recheck_after_days: 60
---

## Observed

A Web release exported an external PNG whose decoded RGBA matched the imported boot splash texture. The decoded original PNG differed, even though all three images had the same size.

## Evidence

A 1536 × 1024 boot splash used a lossy import at quality 0.98. A headless script compared the raw source via `Image.load_from_file`, the imported texture via `ResourceLoader.load(path).get_image()`, and the exported PNG via `Image.load_from_file`. It converted each image to RGBA8 and removed mipmaps before comparing bytes. The exported and imported pixels were identical. The source differed by 1.495 mean absolute RGB levels on a 0–255 scale, with fully opaque alpha throughout.

The [Web export guide](https://docs.godotengine.org/en/4.5/tutorials/export/exporting_for_web.html) leaves this distinction unspecified. The engine's [icon and splash loader](https://github.com/godotengine/godot/blob/4.5.1-stable/editor/export/editor_export_platform.cpp#L82-L101) gets the image from the imported texture when available and falls back to the original file.

## Re-check

Export a Web project with a custom boot splash and a lossy import that visibly changes its pixels. Compare the exported external PNG, the imported texture image and the source PNG as decoded RGBA8 with no mipmaps. The observation fails if the source and imported images differ and the export matches the source.

## Apply

When converting an emitted Web splash while preserving its displayed pixels, encode the exported PNG or the imported texture image. A conversion from the raw project PNG can match dimensions and still change color values.

## History

- 2026-11-23: Codex measured the three images in the same checkout and checked the official exporter source.
