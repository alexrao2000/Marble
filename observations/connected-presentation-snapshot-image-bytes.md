---
name: connected-presentation-snapshot-image-bytes
description: "A reconnected presentation snapshot retained image references but omitted their bytes in a local export"
metadata:
  type: observation
  subject: "Codex Artifact Session presentations, bundled runtime 26.1119.11507"
  observed: 2026-11-23
  status: active
  recheck_after_days: 7
---

## Observed

After reconnecting a saved cloud presentation, `presentation.toProto()` returned PNG
media records with library-file URIs and empty Uint8Array data. A direct local export
from that snapshot produced zero-byte PNG entries inside an otherwise readable PPTX.
The live image metadata alone did not establish a portable image export.

## Evidence

A saved 15-slide deck contained six PNG images. All six snapshot data buffers had
byteLength 0 while their image references remained intact. Loading that snapshot into
the bundled local presentation runtime and exporting it produced six zero-byte
`ppt/media` files. Rehydrating each referenced media ID from its authorized original
PNG, then exporting again, embedded all six originals. Each embedded file matched a
source PNG by SHA-256. Package integrity, geometry, typography and first-party import
checks passed on the repaired export. This was a local export comparison, not a test
of the cloud viewer or its download UI.

## Re-check

Reconnect a saved presentation with a known PNG, inspect its toProto media data length,
and locally export it. Check the PPTX media member size and hash against the original.
A nonempty matching image without rehydration would contradict this behavior.

## Apply

Before saving a connected presentation as a local file, inspect actual image bytes and
validate the exported media members. If bytes are absent, rehydrate the corresponding
media IDs from authorized original assets or a supported connected-source download.
Map by slide image reference, not array order. Do not deliver an export merely because
its slide count and package structure pass.

## History

- 2026-11-23: Recorded the empty-buffer export and original-asset rehydration comparison.
