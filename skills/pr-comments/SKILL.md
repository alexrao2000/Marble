---
name: pr-comments
description: >-
  Address, respond to, and resolve unresolved review comments on a GitHub pull request.
  Fetches all threads, identifies which are unresolved, verifies whether each underlying
  issue is fixed in the code, fixes it if not, replies with what was done, and resolves the
  thread. Use when the user says "address the PR comments" or "resolve the comments on PR N".
---

# PR comments

## When to run

Run this skill when the user asks you to address, respond to, or resolve review comments on
a GitHub pull request. The trigger is any request about unresolved PR comments.

## Procedure

### 1. Fetch threads and identify unresolved ones

Use the GraphQL API to get all review threads with resolution status:

```bash
GH_REPO=<owner/repo> gh api graphql -f query='
{
  repository(owner: "<owner>", name: "<repo>") {
    pullRequest(number: <N>) {
      reviewThreads(first: 50) {
        nodes {
          id
          isResolved
          comments(first: 10) {
            nodes {
              databaseId
              body
              author { login }
            }
          }
        }
      }
    }
  }
}'
```

Also fetch the REST comments to see the reply structure:

```bash
GH_REPO=<owner/repo> gh api repos/<owner>/<repo>/pulls/<N>/comments --paginate
```

List the unresolved threads. If all are resolved, say so and stop.

### 2. For each unresolved thread

Read the original comment to understand what it asks for. Then:

1. **Check whether the issue is already fixed.** Read the relevant file, grep for the fix,
   or check git log for the commit that addressed it.
2. **If not fixed, fix it.** Make the code change. Run the project's check script to confirm
   green. Commit the fix.
3. **Reply to the thread.** Post a reply via the REST API explaining what was done:

```bash
GH_REPO=<owner/repo> gh api repos/<owner>/<repo>/pulls/<N>/comments/<comment_id>/replies \
  -X POST -f body="Fixed in <commit>. <one-sentence description of what changed>."
```

Lead with "Fixed in <commit>" when a code change was made. Lead with "Documented in <commit>"
when documentation was added. Lead with "Acknowledged" when the issue is a known limitation
that was intentionally accepted.

### 3. Resolve the threads

After replying to all unresolved threads, resolve them via GraphQL:

```bash
GH_REPO=<owner/repo> gh api graphql -f query='
mutation {
  resolveReviewThread(input: {threadId: "<thread_node_id>"}) {
    thread { isResolved }
  }
}'
```

Batch multiple resolves into one mutation when possible.

### 4. Verify

Run the GraphQL query from step 1 again and confirm zero unresolved threads remain.

## Rules

- Never resolve a thread without first verifying the underlying issue is addressed.
- Never resolve a thread without replying to it first.
- If a thread requires a code change, run the project's check script after the change.
- If a thread raises a valid issue that cannot be fixed in this PR, reply explaining why
  and leave it unresolved. Tell the user.
- Push any new commits to the PR branch after all fixes are made.
