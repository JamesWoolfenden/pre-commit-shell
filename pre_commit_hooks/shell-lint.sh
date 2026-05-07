#!/usr/bin/env sh

set -eu

if ! command -v shellcheck >/dev/null 2>&1; then
	echo "shellcheck is not installed (https://www.shellcheck.net/)" >&2
	exit 1
fi

exec shellcheck "$@"
