#!/usr/bin/env bash
set -euo pipefail

repo="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$repo"

if [[ "$(git branch --show-current)" != "main" ]]; then
  echo "sync: refusing outside main" >&2
  exit 1
fi

git_dir="$(git rev-parse --git-dir)"
if [[ -f "$git_dir/MERGE_HEAD" || -d "$git_dir/rebase-merge" || -d "$git_dir/rebase-apply" ]]; then
  echo "sync: refusing during a merge or rebase" >&2
  exit 1
fi

if ! git diff --quiet || ! git diff --cached --quiet || [[ -n "$(git ls-files --others --exclude-standard)" ]]; then
  echo "sync: working tree is dirty; commit explicit paths first" >&2
  exit 1
fi

remote="https://github.com/alexrao2000/memory-and-skills.git"
helper="$repo/scripts/github-personal-credential.sh"
git_personal() {
  env -u GH_TOKEN git -c credential.helper= -c "credential.helper=$helper" "$@"
}

git_personal fetch "$remote" main
read -r ahead behind < <(git rev-list --left-right --count HEAD...FETCH_HEAD)

if (( ahead > 0 && behind > 0 )); then
  echo "sync: local and remote main diverged; refusing to rewrite either" >&2
  exit 1
fi

if (( behind > 0 )); then
  git merge --ff-only FETCH_HEAD
  echo "sync: fast-forwarded main by $behind commit(s)"
elif (( ahead > 0 )); then
  git_personal push "$remote" HEAD:main
  echo "sync: pushed main by $ahead commit(s)"
else
  echo "sync: main is current"
fi
