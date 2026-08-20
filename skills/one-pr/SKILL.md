---
name: one-pr
description: >-
  Bundle all changes from the current task into a single pull request. Create one branch,
  one commit (or a small sequence of related commits), and one PR with a structured body.
  Use when the user says "put these in one PR", "single PR", or "bundle everything".
---

# One PR

## When to run

Run this skill when the user asks for all changes to go into a single pull request rather
than multiple PRs. The trigger is bundling intent: "one PR", "single PR", "put these changes
in one PR".

## Procedure

### 1. Verify green

Run the project's check script (`scripts/check.sh` or equivalent) before creating the PR.
Do not proceed if the suite is red. Fix failures first.

### 2. Branch

Create one branch from `origin/main` (or the project's base branch). Use a descriptive
slug, not a ticket number.

### 3. Commit

Stage all changed files. Write a commit message whose subject says what the PR does and
whose body lists the individual items. Follow the repository's commit conventions.

If the changes span logically separable items (a spec amendment, a code change, a fixture
update), multiple commits on the same branch are acceptable. One commit per logical unit,
not one commit per file.

### 4. Push and create

Push the branch and create the PR. The PR body follows the project's template:

- **Problem**: one paragraph on what was missing or wrong.
- **Fix**: one paragraph on what this PR does about it.
- **Changes**: one section per logical group, each with a file reference and a plain
  sentence describing the change.
- **Verification**: the check script result (pass count, fail count).

### 5. Report

Return the PR URL to the user.
