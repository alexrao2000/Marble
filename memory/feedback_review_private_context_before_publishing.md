---
name: review-private-context-before-publishing
description: Keep private conversational context out of published repository content and metadata
metadata:
  node_type: memory
  type: feedback
  modified: 2026-11-17
---

Never disclose private conversational context in public repositories without explicit
authorization for that disclosure. This includes company names, interview details,
personal information, identifying details, and the private origin of ideas.

Review code, documentation, file paths, branch names, commit messages, pull request
titles and descriptions, issues, and generated artifacts for such disclosures.
Before pushing or publishing, verify the destination repository's visibility
and inspect the exact files, diff, and metadata that will be exposed.

Use generic technical descriptions when the private source of an idea is not
needed. Permission to implement an idea does not imply permission to disclose
its origin. Keep unrelated private context out of private repositories, too.
If visibility or the final changes cannot be checked, say so; do not claim
the review was completed.
