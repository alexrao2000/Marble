---
name: feedback-keep-pr-metadata-current
description: "Update a PR's title and body yourself whenever its content changes; never leave a stale title standing and flag it instead"
metadata:
  node_type: memory
  type: feedback
  modified: 2026-08-21T00:00:00.000Z
---

When a PR's content changes, update its title and its body in the same pass. Standing permission, and Alex's word is "demand". This holds for titles he wrote himself.

**Why:** I pushed Sprint 5's specification onto a branch whose PR he had titled "Sprint 4 Spec and Harness", then reported that the title now understated the PR and said I had left it alone out of deference. He answered: "If 651 understates, update it. You have my blessing, in fact demand, to update titles and descriptions of PRs when the content is updated." Flagging a stale title is not a substitute for fixing one, and leaving his wording untouched is not respect - it leaves the PR misdescribing itself.

**How to apply:** after any push that widens or changes what a PR contains, rewrite the title and the body to match, keeping his register when he has set one - "Sprint 4 Spec and Harness" became "Sprint 4 and 5 Spec and Harness" rather than something of my own. A PR comment describing the new commits is still worth posting, but it is additional to the body and never a replacement for it. Title shape is [[feedback_pr_titles_short_and_plain]] and body shape is [[feedback_pr_body_template]].
