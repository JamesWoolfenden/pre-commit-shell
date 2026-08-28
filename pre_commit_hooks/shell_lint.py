"""Cross-platform entrypoint for the shell-lint hook.

Replaces the previous bash wrapper so the hook runs natively on Windows as well
as Linux/macOS, without requiring a POSIX shell.
"""

from __future__ import annotations

import os
import shutil
import subprocess
import sys
from typing import Sequence


def main(argv: Sequence[str] | None = None) -> int:
    argv = list(sys.argv[1:] if argv is None else argv)

    shellcheck = shutil.which("shellcheck")
    if shellcheck is None:
        print("shellcheck command not found", file=sys.stderr)
        return 1

    if not argv:
        return 0

    if os.environ.get("DEBUG") == "1":
        print(f"+ {shellcheck} {' '.join(argv)}", file=sys.stderr)

    return subprocess.call([shellcheck, *argv])


if __name__ == "__main__":
    raise SystemExit(main())
