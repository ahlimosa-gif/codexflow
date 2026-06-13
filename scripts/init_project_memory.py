#!/usr/bin/env python3
"""Initialize CodexFlow Smart project memory without overwriting existing files."""

from __future__ import annotations

import argparse
import os
import shutil
from pathlib import Path


FILES = {
    "AGENTS.template.md": "AGENTS.md",
    "MEMORY_INDEX.template.md": "MEMORY_INDEX.md",
    "NEXT_TASKS.template.md": "NEXT_TASKS.md",
    "PROJECT_CONTEXT.template.md": "PROJECT_CONTEXT.md",
    "PROGRESS.template.md": "PROGRESS.md",
    "DECISIONS.template.md": "DECISIONS.md",
    "VERIFICATION.template.md": "VERIFICATION.md",
}


def skill_root() -> Path:
    return Path(__file__).resolve().parents[1]


def initialize(root: Path, force: bool = False) -> tuple[list[str], list[str]]:
    root = root.resolve()
    templates = skill_root() / "templates"
    created: list[str] = []
    skipped: list[str] = []
    root.mkdir(parents=True, exist_ok=True)

    for template_name, target_name in FILES.items():
        source = templates / template_name
        target = root / target_name
        if target.exists() and not force:
            skipped.append(target_name)
            continue
        shutil.copyfile(source, target)
        created.append(target_name)

    checkpoints = root / "checkpoints"
    if checkpoints.exists():
        skipped.append("checkpoints/")
    else:
        checkpoints.mkdir()
        created.append("checkpoints/")

    return created, skipped


def main() -> int:
    parser = argparse.ArgumentParser(description="Create CodexFlow Smart memory files.")
    parser.add_argument("--root", default=os.getcwd(), help="Project root.")
    parser.add_argument("--force", action="store_true", help="Overwrite existing memory files.")
    args = parser.parse_args()

    created, skipped = initialize(Path(args.root), force=args.force)
    print("CodexFlow Smart project memory initialization")
    print(f"Root: {Path(args.root).resolve()}")
    print("Created:")
    for item in created:
        print(f"- {item}")
    print("Skipped:")
    for item in skipped:
        print(f"- {item}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
