---
name: duckdb-wasm-blob-extension-entrypoint
description: DuckDB-Wasm Blob extension URLs need a fragment containing the extension filename to select the correct entrypoint
metadata:
  type: observation
  subject: DuckDB-Wasm 1.32.0 / DuckDB 1.4.3 / Chromium 156
  observed: 2026-10-31
  status: active
  recheck_after_days: 30
---

## Observed

DuckDB-Wasm can instantiate its worker, main Wasm module, and signed JSON/Parquet extensions entirely from browser-owned Blob URLs under `connect-src blob:`. A plain extension Blob URL fails because its random UUID becomes the extension entrypoint name. Appending `#/json.duckdb_extension.wasm` or `#/parquet.duckdb_extension.wasm` selects the expected entrypoint while the browser resolves the same Blob bytes.

## Evidence

A Chromium 156 page used a CSP with `default-src 'none'`, nonce-authorized inline bootstrap, `script-src blob: 'wasm-unsafe-eval'`, `worker-src blob:`, and `connect-src blob:`. Public worker/Wasm/extension bytes were preloaded before the probe. The worker and main module instantiated from Blob URLs. `LOAD` with a plain extension Blob URL returned an IO error expecting `<uuid>_duckdb_cpp_init`. With the filename fragments, both signed readers loaded and returned a sum of 6 from two-row synthetic JSON and Parquet inputs. Captured non-Blob requests and browser console errors were both empty. No unsigned-extension override was enabled.

## Re-check

Use DuckDB-Wasm 1.32.0 and its matching signed v1.4.3 wasm_eh extensions in a Chromium page. Create a Blob URL for the worker source and main Wasm, instantiate AsyncDuckDB, and disable automatic extension installation/loading. Create Blob URLs for each extension. Confirm that the plain JSON Blob URL fails with the UUID entrypoint error. In a fresh worker, load `blobUrl + "#/json.duckdb_extension.wasm"` and the corresponding Parquet URL, register synthetic input buffers, and check both sums equal 6. Capture requests and require no HTTP(S) request during the probe. The page policy must allow only Blob connections.

## Apply

Preload public engine assets before admitting private data. Create the worker and Wasm from browser-owned Blobs and name extension Blob URLs with filename fragments. This avoids granting HTTP access to the private analysis runtime. Keep signed-extension checks enabled. Revoke Blob URLs when their worker is disposed.

## History

- 2026-10-31: Initial controlled comparison recorded; plain Blob name failed, filename-fragment loads succeeded without network access.
