---
name: chromium-sandbox-overlay-input
description: Automated approval clicks above an opaque iframe intermittently missed the parent; permanently separate controls passed the exercised workflow
metadata:
  type: observation
  subject: Chromium 156.0.8078.4 / Playwright 1.64.1 / macOS
  observed: 2026-10-31
  status: active
  recheck_after_days: 30
---

## Observed

In the Niche browser-containment workflow, some automated clicks on a parent download-approval control above a sandboxed opaque srcdoc iframe produced no parent pointerdown, pointerup, or click event. Playwright reported the click completed. Fixed overlays and a native dialog both exhibited missed approvals; iframe inert and pointer-events:none did not eliminate them. A permanently allocated ingress strip above the frame, with no overlap or expansion over its previous screen area, passed the full workflow and a later enterprise-only run. This is an application-layout mitigation in measured runs, not a universal browser fix or a deterministic reproduction rate.

## Evidence

The app served from loopback HTTP, with sandbox allow-scripts only and strict CSP. Capture listeners installed before page load recorded the toolbar's complete click sequence but no approval events in failing runs. The form remained open with its URL populated and no source request. Programmatic field filling worked. A native top-layer dialog still failed intermittently. The permanent-strip layout passed all 16 browser checks, including real personal Ollama and separate-origin CSV/JSON/Parquet ingress; a subsequent seven-test enterprise run also passed after offline and public-message checks were added. No sleeps, click retries, or programmatic click substitutes were added to make approvals pass.

A related primary report documents sandboxed iframe input routing even behind native dialogs: https://github.com/microsoft/playwright/issues/43642. That report has stronger child-event instrumentation; our parent-only diagnostic does not establish which child/widget received missing clicks or the underlying Chromium defect.

## Re-check

Run the enterprise browser suite in /Users/alexr/Niche on the supported browser. To compare an overlay, use synthetic data and capture parent and child pointer/mouse events plus a source request receipt. Do not accept Playwright click completion or a single screenshot as proof of delivery. Preserve a passing positive control and actual receiver assertions. Reproduce without arbitrary sleeps or retries before changing browser recommendations.

## Apply

Keep sensitive approval controls in an area that never overlaps an opaque iframe's screen rectangle. Do not rely on modal appearance, DOM hit testing, inert, or pointer-events alone as proof of correct input routing. This mitigates a UI reliability issue; sandbox/CSP/message validation remain the security controls. The cost is persistent space for the ingress controls.

## History

- 2026-10-31: Parent-event diagnostics, overlay/native-dialog comparisons, and permanent-strip workflow results recorded. Related upstream report linked; no internal browser root cause assigned.
