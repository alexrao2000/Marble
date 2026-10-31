---
name: chromium-csp-webrtc-construction
description: Chromium 156 permits RTCPeerConnection construction in an opaque sandbox with Blob-only CSP and ignores the webrtc CSP directive
metadata:
  type: observation
  subject: Chromium 156 / iframe sandbox / Content Security Policy
  observed: 2026-10-31
  status: active
  recheck_after_days: 30
---

## Observed

In Chromium 156, an iframe with only `sandbox="allow-scripts"`, an opaque origin, and `connect-src blob:` could still construct and close an RTCPeerConnection with an empty ICE-server list. Adding a meta CSP of `webrtc 'block'` did not stop construction and logged an unrecognized-directive error. This measures constructor availability only, not successful peer connectivity or data exfiltration.

## Evidence

A nonce-authorized srcdoc analysis frame used default-src none, Blob-only connections/workers, no forms, no same-origin permission, and no HTTP image/script permissions. Ordinary HTTP execution inside it worked from preloaded Wasm Blobs. Calling `new RTCPeerConnection({iceServers:[]})` then close succeeded. The controlled comparison added a meta Content-Security-Policy of `webrtc 'block'` before repeating construction; it again succeeded and the browser console reported that the directive was unrecognized. No third-party STUN server, peer, or private data was contacted.

## Re-check

In the supported Chromium release, load a sandboxed srcdoc with only allow-scripts and a nonce-authorized bootstrap under `connect-src blob:`. Construct and immediately close RTCPeerConnection with `iceServers:[]`. Repeat after adding `webrtc 'block'` as CSP and capture console errors. Do not infer peer-network denial merely from fetch/WebSocket denial. A successful constructor does not itself prove connectivity.

## Apply

Describe CSP resource/network controls by their tested scope. Do not call Blob-only connect-src a universal network air gap. WebRTC and other untested channels need separate managed-browser/network controls or an audited runtime restriction for a stronger enterprise guarantee. Do not add an unsupported CSP directive and claim it enforces WebRTC denial.

## History

- 2026-10-31: Initial constructor and directive-support comparison recorded in Chromium 156.
