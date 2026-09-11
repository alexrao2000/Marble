---
name: feedback-pr-titles-short-and-plain
description: "PR titles are a tag plus a short Title Case noun phrase; no internal reference numbers, no trailing status clause"
metadata:
  node_type: memory
  type: feedback
  modified: 2026-08-21T00:00:00.000Z
---

A PR title is the project tag plus a short noun phrase, roughly five to eight words, in Title Case. It names the subject. It never carries an internal reference number, and it never explains itself after a comma.

Alex rewrote both titles on the Sprint 4 stack:

- Mine: `[sample-project] ROUTE008 and ROUTE009: Sprint 4's embedding signal and question-type label, specified and unbuilt` → his: `[sample-project] Sprint 4: Text Embedding and New Question Tags as Heuristics`
- Mine: `[sample-project] Sprint 4: Statement 11's ruling and Observation 21, and the branch the sprint's specs land on` → his: `[sample-project] Sprint 4 Spec and Harness`

**Why:** three things were wrong, and length was only one. `Statement 11` and `Observation 21` are positions in this repository's own files, so they say nothing to anyone reading a PR list. `specified and unbuilt` and `the branch the sprint's specs land on` are body content in a title. And the plain subject, what the sprint actually adds, was buried behind the IDs.

**How to apply:** ask what the PR is *about*, in the words a reader outside the repository would use, and stop. `Text Embedding and New Question Tags as Heuristics` beats any ID list. `Harness` is his word for the plan, the gates and the bookkeeping around a spec. This does not repeal [[feedback_pr_titles_cite_task]]: a narrow PR amending one criterion still leads with `ROUTE002 c17:`, which is the established shape in this repo's history. Requirement and criterion IDs belong in a title; queue rows, statement numbers and observation numbers never do. See [[feedback_write_prs_for_outside_readers]] and [[feedback_terse_over_verbose]].
