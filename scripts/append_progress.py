#!/usr/bin/env python3
"""Append a compact CodexFlow Smart entry to PROGRESS.md."""

from __future__ import annotations

import argparse
import os
from datetime import datetime
from pathlib import Path


def normalize(value: str) -> str:
    return value.replace("\r\n", "\n").replace("\r", "\n").strip() or "-"


def append_entry(
    root: Path,
    title: str,
    mode: str,
    goal: str,
    changed_files: str,
    root_cause: str,
    verification: str,
    result: str,
    follow_up: str,
) -> Path:
    path = root.resolve() / "PROGRESS.md"
    if not path.exists():
        raise FileNotFoundError(f"PROGRESS.md not found at {path}")

    today = datetime.now().strftime("%Y-%m-%d")
    entry = f"""

### {today} - {title}

- Mode: {mode}
- Goal: {normalize(goal)}
- Changed files: {normalize(changed_files)}
- Root cause: {normalize(root_cause)}
- Verification: {normalize(verification)}
- Result: {normalize(result)}
- Follow-up: {normalize(follow_up)}
"""
    with path.open("a", encoding="utf-8", newline="\n") as handle:
        handle.write(entry)
    return path


def main() -> int:
    parser = argparse.ArgumentParser(description="Append a PROGRESS.md entry.")
    parser.add_argument("--root", default=os.getcwd(), help="Project root.")
    parser.add_argument("--title", required=True)
    parser.add_argument("--mode", required=True)
    parser.add_argument("--goal", default="-")
    parser.add_argument("--changed-files", default="-")
    parser.add_argument("--root-cause", default="-")
    parser.add_argument("--verification", default="-")
    parser.add_argument("--result", default="-")
    parser.add_argument("--follow-up", default="-")
    args = parser.parse_args()

    path = append_entry(
        Path(args.root),
        args.title,
        args.mode,
        args.goal,
        args.changed_files,
        args.root_cause,
        args.verification,
        args.result,
        args.follow_up,
    )
    print(f"Appended progress entry to {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
