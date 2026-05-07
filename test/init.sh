#!/usr/bin/env bash

set -euo pipefail

if ! command -v shellcheck >/dev/null 2>&1; then
    echo "shellcheck is not installed" >&2
    exit 1
fi

repo_root=$(pwd)
repo_rev=$(git rev-parse HEAD)

tmpdir=$(mktemp -d "${TMPDIR:-/tmp}/pre-commit-shell.XXXXXX")
tmpfile=$(mktemp "${TMPDIR:-/tmp}/pre-commit-shell.XXXXXX")
trap 'rm -rf -- "$tmpdir" "$tmpfile"' EXIT

cp test/test.sh "$tmpdir"
cat > "$tmpdir/.pre-commit-config.yaml" <<EOS
repos:
  - repo: ${repo_root}
    rev: ${repo_rev}
    hooks:
      - id: shell-lint
EOS

(
    cd "$tmpdir"
    git init --quiet
    git config user.email "test@example.com"
    git config user.name "test"
    pre-commit install
    git add .pre-commit-config.yaml
    git commit --quiet -m "init test case"
    git add --all
    git commit -m "begin test" >"$tmpfile" 2>&1 || true
)

check() {
    if grep -q "$1" "$tmpfile"; then
        echo "$1 PASSED"
    else
        echo "$1 FAILED" >&2
        cat "$tmpfile" >&2
        exit 255
    fi
}

check SC2115
check SC2086
check SC2034
