#!/usr/bin/env bash
# SessionStart hook: say when the current branch has changes but no UI harness, or a stale one.
# Read-only and silent outside a git repo, on an unchanged branch, or when the harness is current.
set -u

top=$(git rev-parse --show-toplevel 2>/dev/null) || exit 0
branch=$(git symbolic-ref --quiet --short HEAD 2>/dev/null) || exit 0

default=$(git symbolic-ref --quiet --short refs/remotes/origin/HEAD 2>/dev/null)
default=${default#origin/}
if [ -z "$default" ]; then
  for candidate in main master; do
    git show-ref --verify --quiet "refs/heads/$candidate" && default=$candidate && break
  done
fi
[ -n "$default" ] || exit 0

base=$(git merge-base HEAD "origin/$default" 2>/dev/null || git merge-base HEAD "$default" 2>/dev/null) || exit 0
git -C "$top" diff --quiet "$base" -- . ':(exclude).harness' 2>/dev/null && exit 0

slug=${branch//\//-}
dir="$top/.harness/$slug"
head=$(git rev-parse --short HEAD)

[ -f "$dir/SKIP" ] && exit 0
if [ -f "$dir/BUILT_AT" ]; then
  built=$(cat "$dir/BUILT_AT")
  [ "$built" = "$head" ] && exit 0
  state="is stale: built at $built, the branch is now at $head"
else
  state="has no UI harness yet"
fi

echo "Branch '$branch' $state. Use the pr-harness skill to build it in .harness/$slug/ before" \
     "or alongside the user's request, and end by giving the user the command that opens it."
