---
name: tab-icon
description: Add and verify a browser tab icon (favicon). Use when the user asks to make or scaffold a browser app, including a browser-first app with a desktop wrapper, or explicitly asks for a tab icon.
---

# Browser tab icons

1. Check the app’s existing favicon and framework conventions. Reuse an intentional project icon where it fits. Replace framework placeholders for a new app.
2. Use the app’s name or visual identity to make an identifiable mark. Favor a clear silhouette, strong contrast, and simple geometry that reads at 16 and 32 pixels on light and dark tabs.
3. Store the icon with the app’s assets and register it through the framework’s favicon convention or the document head. Keep it in the app’s normal build and asset-serving paths. Choose SVG, PNG, or ICO based on the target browsers and the project’s conventions.
4. Verify the running app serves the icon from the registered URL with the correct media type and check its appearance at tab size. Cover browser tab icons here. Handle native desktop, installer, and home-screen icons when the task calls for them.
