---
name: feedback-browser-first-desktop
description: Build the browser app first and wrap it for desktop unless the project is desktop-only. Always include hot reload for desktop development.
metadata:
  type: feedback
  modified: 2026-11-23
---

For a product that should work in a browser and on desktop, make the browser app the
default interface. Use the same interface and application logic in a thin desktop
wrapper. Keep platform-specific input, notifications, and packaging in the wrapper.
Treat native shortcuts and gestures as enhancements with visible alternatives.

A project that is explicitly desktop-only can use a native interface when it fits
the work. Always give desktop apps a hot-reload development loop. Verify that a
source edit reaches the running window without rebuilding a package or manually
relaunching. Keep workspace state available across interface reloads.
