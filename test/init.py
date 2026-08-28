"""End-to-end test: install the hook into a throwaway repo and assert it fires.

Python rather than bash so the suite runs on Windows as well as Linux/macOS.
"""

from __future__ import annotations

import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

# Each entry is a set of acceptable codes for one construct in test.sh; the
# assertion passes if any of them is reported. shellcheck renumbers findings
# between releases (the `var = 42` line has been SC1068, SC2034 and SC2283),
# so pinning a single code makes the suite fail on version bumps alone.
EXPECTED_CODES = (
    ("SC2115",),
    ("SC2086",),
    ("SC2283", "SC1068", "SC2034"),
)


def run(cmd, cwd=None, check=True):
    return subprocess.run(
        cmd, cwd=cwd, check=check, text=True, capture_output=True
    )


def main() -> int:
    if shutil.which("shellcheck") is None:
        print("shellcheck is not installed", file=sys.stderr)
        return 1

    repo_root = Path.cwd().resolve()
    repo_rev = run(["git", "rev-parse", "HEAD"]).stdout.strip()

    with tempfile.TemporaryDirectory(prefix="pre-commit-shell.") as tmpdir:
        tmp = Path(tmpdir)
        shutil.copy(repo_root / "test" / "test.sh", tmp / "test.sh")
        (tmp / ".pre-commit-config.yaml").write_text(
            "repos:\n"
            f"  - repo: {repo_root.as_posix()}\n"
            f"    rev: {repo_rev}\n"
            "    hooks:\n"
            "      - id: shell-lint\n",
            encoding="utf-8",
        )

        env = {**os.environ, "GIT_CONFIG_GLOBAL": os.devnull}
        run(["git", "init", "--quiet"], cwd=tmp)
        run(["git", "config", "user.email", "test@example.com"], cwd=tmp)
        run(["git", "config", "user.name", "test"], cwd=tmp)
        run(["pre-commit", "install"], cwd=tmp)
        run(["git", "add", ".pre-commit-config.yaml"], cwd=tmp)
        run(["git", "commit", "--quiet", "-m", "init test case"], cwd=tmp, check=False)
        run(["git", "add", "--all"], cwd=tmp)
        # Expected to fail: the hook should reject test.sh.
        result = subprocess.run(
            ["git", "commit", "-m", "begin test"],
            cwd=tmp,
            text=True,
            capture_output=True,
            env=env,
        )
        output = result.stdout + result.stderr

    failed = False
    for codes in EXPECTED_CODES:
        label = "/".join(codes)
        if any(code in output for code in codes):
            print(f"{label} PASSED")
        else:
            print(f"{label} FAILED", file=sys.stderr)
            failed = True

    if failed:
        print(output, file=sys.stderr)
        return 255
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
