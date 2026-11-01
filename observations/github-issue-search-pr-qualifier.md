---
name: github-issue-search-pr-qualifier
description: The GitHub connector issue-search response included ordinary issues despite an is:pr qualifier; direct PR listing confirmed no open PRs.
metadata:
  type: observation
  subject: Codex GitHub connector search_issues, version not exposed
  observed: 2026-11-01
  status: active
  recheck_after_days: 7
---

## Observed

A query containing `repo:<owner>/<repo> is:pr is:open` returned three ordinary issues, with `/issues/` URLs, from a repository with no open pull requests. The tool description says GitHub query qualifiers are supported. This measurement does not establish which qualifiers were ignored or why.

## Evidence

Called `search_issues` with the repository and qualifiers in its `query` field. The structured response contained three ordinary issues and no PR-specific type marker. Queried the same repository using `gh pr list --state open --json number,title,headRefName,baseRefName`; it returned an empty list. A second repository returned an empty result through both paths. No identifying repository names or issue contents are retained here.

## Re-check

Repeat the connector query on an authorized repository with known open issues, then compare with its direct open-PR list. The observation is contradicted if the connector correctly excludes those ordinary issues and matches the direct list.

## Apply

Use a direct PR listing or PR-specific endpoint to establish PR status. Do not infer that a connector issue-search result is a PR merely from the query qualifier. This costs one read-only request.

## History

- 2026-11-01: Codex recorded the issue-search/direct-list discrepancy and used direct PR listing for the release.
