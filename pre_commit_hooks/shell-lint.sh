#!/usr/bin/env sh

set -o errexit
set -o nounset

check () {
command which shellcheck
}

if check; then
	shellcheck "$@"
else
	echo "Shellcheck missing"
	exit 1
fi	
