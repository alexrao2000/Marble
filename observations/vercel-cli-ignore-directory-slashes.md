---
name: vercel-cli-ignore-directory-slashes
description: Vercel CLI 65.0.0 skipped directories re-included with a trailing slash in .vercelignore
metadata:
  type: observation
  subject: Vercel CLI 65.0.0 on macOS and its source upload file tree
  observed: 2026-11-24
  status: active
  recheck_after_days: 30
---

## Observed

With a root-level `/*` ignore rule, directory exceptions such as `!/api/`
failed to include those directories in a CLI source upload. Exceptions such
as `!/api` included them.

## Evidence

Two upload attempts reported that the configured Python entry point was
missing. Vercel's deployment-files endpoint listed only the two allowlisted
root files in each upload. Git's ignore check accepted the intended source
files when the allowlist used trailing slashes. The installed Vercel CLI
passed relative directory names without a trailing slash to the Node
`ignore` API. A local fixture reproduced the mismatch on `api` and `api/`.
After removing the trailing slash from each directory exception, the next
deployment included the intended directories, excluded private files, and
reached Ready.

## Re-check

Use a disposable project with a source directory and an ignored root file.
Upload once with `/*` followed by `!/api/` and once with `!/api`.
Compare the deployment-files listings and record the exact CLI version.
An initial local check can run the installed CLI's ignore matcher against
both the root-relative directory name and the file beneath it.

## Apply

Use directory exceptions without trailing slashes in a Vercel CLI allowlist.
Keep child path restrictions where needed. Confirm the upload tree on the
provider when validating exclusions and resolving a missing function.

## History

- 2026-11-24 — Compared rejected uploads with a successful upload and reproduced the directory match locally.
