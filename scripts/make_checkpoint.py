#!/usr/bin/env python3
"""Create a CodexFlow Smart checkpoint with git state and rollback notes."""

from __future__ import annotations

import argparse
import os
import re
import subprocess
from datetime import datetime
from pathlib import Path


def run(cmd: list[str], cwd: Path) -> str:
    try:
        result = subprocess.run(
            cmd,
            cwd=str(cwd),
            text=True,
            capture_output=True,
            timeout=10,
            check=False,
        )
    except Exception as exc:  # noqa: BLE001 - diagnostics only
        return f"unavailable: {exc}"
    return (result.stdout or result.stderr).strip() or "-"


def slugify(value: str) -> str:
    value = value.lower()
    value = re.sub(r"[^a-z0-9]+", "-", value).strip("-")
    return value[:60] or "checkpoint"


def create_checkpoint(root: Path, title: str, mode: str, goal: str, risk_notes: str, rollback: str) -> Path:
    root = root.resolve()
    checkpoint_dir = root / "checkpoints"
    checkpoint_dir.mkdir(exist_ok=True)
    stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    path = checkpoint_dir / f"{stamp}-{slugify(title)}.md"

    branch = run(["git", "branch", "--show-current"], root)
    status = run(["git", "status", "--short"], root)
    head = run(["git", "rev-parse", "--short", "HEAD"], root)

    content = f"""# Checkpoint: {title}

- Time: {datetime.now().isoformat(timespec="seconds")}
- Root: `{root}`
- Mode: {mode}
- Goal: {goal or "-"}
- Git branch: {branch}
- Git HEAD: {head}

## Git Status

```text
{status}
```

## Risk Notes

{risk_notes or "-"}

## Rollback Suggestion

{rollback or "Inspect changed files first, then revert only the files changed by this task."}
"""
    path.write_text(content, encoding="utf-8", newline="\n")
    return path


def main() -> int:
    parser = argparse.ArgumentParser(description="Create a CodexFlow Smart checkpoint.")
    parser.add_argument("--root", default=os.getcwd(), help="Project root.")
    parser.add_argument("--title", required=True)
    parser.add_argument("--mode", default="Deep")
    parser.add_argument("--goal", default="-")
    parser.add_argument("--risk-notes", default="-")
    parser.add_argument("--rollback", default="-")
    args = parser.parse_args()

    path = create_checkpoint(
        Path(args.root),
        args.title,
        args.mode,
        args.goal,
        args.risk_notes,
        args.rollback,
    )
    print(f"Created checkpoint: {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
