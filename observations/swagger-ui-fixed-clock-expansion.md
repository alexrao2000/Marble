---
name: swagger-ui-fixed-clock-expansion
description: Swagger UI expansion can stay loading under a frozen Date.now in browser tests
metadata:
  type: observation
  subject: Swagger UI 5 and Playwright 1.62.1 on macOS
  observed: 2026-11-24
  status: active
  recheck_after_days: 30
---

## Observed

In Chromium, an API operation expanded into a persistent loading indicator when
Playwright setFixedTime held Date.now constant. The schema and operation list
had loaded, but parameter and response details stayed absent for over 10 seconds.

## Evidence

The same local API reference and schema expanded normally in a browser without
the fixed clock. Replacing setFixedTime with a Date subclass that shifts the
date while allowing Date.now to advance made the complete workflow pass in
Chromium and WebKit, on desktop and mobile. No application errors were reported.
The fixed-clock failure itself was measured in Chromium only.

## Re-check

Serve a local Swagger UI 5 reference with a synthetic schema. In Chromium,
set a fixed time, open an operation with parameters, and check whether its
loading indicator resolves within 10 seconds. Repeat with an advancing clock
shifted to the same date. Retire this observation if both reliably resolve.

## Apply

For tests that include this API reference, use a normally advancing date offset
when deterministic dates are needed. Avoid a constant Date.now for that flow.
This changes only test time handling and has no production cost.

## History

- 2026-11-24: Measured the fixed-clock loading state and verified the advancing-clock alternative in four browser profiles.
