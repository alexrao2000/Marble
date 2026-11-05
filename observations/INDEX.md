# Observations index

One line per entry. Read this first; open an entry only when its subject is in scope. Run an
entry's re-check before relying on it if it is older than its `recheck_after_days`.

## Active

- [Godot exported wrappers need editable declarations for nested attachments](godot-export-instanced-attachments.md) — Godot 4.5.1 scene export · observed 2026-11-05 · project loading alone did not detect dropped sockets

- [Quaternius Standard base-character normal URIs are mismatched](quaternius-standard-eye-normal-uri.md) — Universal Base Characters Standard · observed 2026-11-05 · use the verified adjacent Godot normal textures

- [Godot physics-frame input pulses can erase attack edges](godot-physics-frame-input-pulses.md) — Godot 4.5.1 headless · observed 2026-11-04 · hold injected presses across full physics ticks

- [npm ci can clear a shared node_modules symlink target](npm-ci-node-modules-symlink-cleanup.md) — npm 11.19.1 / Node 24.22.2 on macOS · observed 2026-11-04 · unlink directory symlinks before clean installs

- [A direct Page token lookup can succeed when the managed-Page list is empty](graph-api-direct-page-token-lookup.md) — social platform Graph API v26.0 · observed 2026-11-04 · verify the derived token against the known Page ID

- [Hosted Windows ACL queries can exceed a ten-second deadline](windows-runner-acl-query-timeout.md) — Windows hosted runner / PowerShell 5 · observed 2026-11-03 · peer jobs passed; permission checks must still fail closed

- [CUA viewport overrides may affect a different bound tab](cua-viewport-selected-tab.md) — Codex desktop in-app browser · observed 2026-11-03 · measure the intended tab after setting its viewport

- [GitHub issue search can return ordinary issues for an is:pr query](github-issue-search-pr-qualifier.md) — Codex GitHub connector · observed 2026-11-01 · direct PR listing confirmed no open PRs

- [Chromium approvals above opaque iframes can miss input](chromium-sandbox-overlay-input.md) — Chromium 156 / Playwright 1.64.1 · observed 2026-10-31 · overlays missed parent events; permanently separate ingress controls passed measured workflows

- [Chromium Blob-only CSP does not disable WebRTC construction](chromium-csp-webrtc-construction.md) — Chromium 156 · observed 2026-10-31 · opaque sandbox permits an empty-ICE RTCPeerConnection; webrtc CSP directive is unrecognized; connectivity was not tested

- [DuckDB-Wasm Blob extension URLs need filename fragments](duckdb-wasm-blob-extension-entrypoint.md) — DuckDB-Wasm 1.32.0 / Chromium 156 · observed 2026-10-31 · signed JSON/Parquet readers run under Blob-only connect policy when fragments preserve entrypoint names

- [Bundled Python sandbox startup needs a literal root read](python-sandbox-root-read.md) — CPython 3.12.14 / macOS 27.0.1 · observed 2026-10-31 · filesystem allowlist needs the root directory itself; home data and network restrictions still hold

- [CUA live tab access can recover after a REPL reset](cua-browser-user-repl-reset.md) — Codex desktop · observed 2026-10-30 · browser.user unavailable cleared after resetting JavaScript handles and rebinding the same tab

- [Slack classifies uploaded .md by content, not extension](slack-md-upload-classification.md) — Slack · observed 2026-09-14 · non-ASCII bytes read as Binary; a few Pascal reserved words in prose read as Pascal; both hide the document

- [Godot background native capture can wait for redraw](godot-macos-background-capture.md) — Godot 4.5.1 / macOS 27.0.1 · observed 2026-10-29 · timers continue while frame_post_draw waits; explicit force_draw completes the capture

- [Godot headless MultiMesh readback returns defaults](godot-headless-multimesh-readback.md) — Godot 4.5.1 headless · observed 2026-10-29 · individual transform/color getters return defaults; bulk buffers retain submitted data

- [Godot initial timers can precede tween updates](godot-initial-timer-before-tween.md) — Godot 4.5.1 headless · observed 2026-10-29 · short startup timers are not evidence that new tweens advanced; observe process frames

- [Godot headless audio needs a mixer drain before immediate test exit](godot-headless-audio-shutdown.md) — Godot 4.5.1 headless · observed 2026-10-29 · imported WAV playback can survive one-frame shutdown; explicit stop plus 200 ms drain clears it

- [Godot sphere primitives include collapsed pole triangles](godot-spheremesh-collapsed-poles.md) — Godot 4.5.1 SphereMesh · observed 2026-10-29 · filter zero-area pole triples before strict topology/normal checks

- [Godot preload call site can retain visual resources at shutdown](godot-preload-shutdown-retention.md) — Godot 4.5.1 / Poem · observed 2026-10-30 · direct shared-backdrop preload leaks in this dependency graph; runtime load exits cleanly

- [Godot sandbox log rotation can crash before script startup](godot-sandbox-log-rotation.md) — Godot 4.5.1 / macOS sandbox · observed 2026-10-30 · explicit writable --log-file avoids the measured default-user-log failure

- [Godot billboard label bounds expand into cubes](godot-label-billboard-bounds.md) — Godot 4.5.1 headless · observed 2026-10-30 · culling AABBs overestimate lettering; generated triangles retain the text quad

- [Godot headless pointer injection uses physical window coordinates](godot-headless-pointer-coordinates.md) — Godot 4.5.1 headless · observed 2026-10-30 · a 64×64 Window can back a 1440×900 logical viewport; explicit test Window sizing fixes dispatch

- [Godot headless gradient readback depends on early binding](godot-headless-gradient-readback.md) — Godot 4.5.1 headless · observed 2026-10-30 · early RID/material binding can produce null readback; later gradient changes can retain stale pixels

## Retired

(none)
