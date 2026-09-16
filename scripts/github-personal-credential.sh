#!/usr/bin/env bash
set -euo pipefail

action="${1:-}"
case "$action" in
  get)
    host=""
    while IFS='=' read -r key value; do
      if [[ "$key" == "host" ]]; then
        host="$value"
      fi
    done
    [[ "$host" == "github.com" ]] || exit 0
    printf 'username=alexrao2000\npassword='
    env -u GH_TOKEN gh auth token --hostname github.com --user alexrao2000
    printf '\n'
    ;;
  store|erase)
    ;;
  *)
    echo "credential helper: expected get, store, or erase" >&2
    exit 2
    ;;
esac
