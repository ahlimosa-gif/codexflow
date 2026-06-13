#!/usr/bin/env python3
"""Read-only CodexFlow Smart planner."""

from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
from pathlib import Path
from typing import Any


MEMORY_FILES = [
    "AGENTS.md",
    "MEMORY_INDEX.md",
    "NEXT_TASKS.md",
    "PROJECT_CONTEXT.md",
    "PROGRESS.md",
    "DECISIONS.md",
    "VERIFICATION.md",
]

STACK_MARKERS = [
    "package.json",
    "vite.config.js",
    "vite.config.ts",
    "next.config.js",
    "next.config.mjs",
    "requirements.txt",
    "pyproject.toml",
    "main.py",
    "manage.py",
    "docker-compose.yml",
    "docker-compose.yaml",
    ".git",
]

MODE_KEYWORDS = {
    "assess": [
        "study",
        "inspect",
        "review",
        "analyze",
        "analyse",
        "look",
        "plan",
        "do not edit",
        "read-only",
        "audit",
        "explain",
    ],
    "init": ["initialize", "initialise", "init memory", "create memory", "project memory", "workflow files"],
    "recover": ["recover", "restore", "rollback", "regression", "previous", "last-known-good", "revert behavior"],
    "import": ["import", "csv", "spreadsheet", "excel", "xlsx", "pdf extracted", "scrape", "upload data"],
    "deep": [
        "migration",
        "schema",
        "database schema",
        "auth",
        "permission",
        "payment",
        "security",
        "deploy",
        "production",
        "public api",
        "api contract",
        "performance",
        "concurrency",
        "refactor",
    ],
    "light": ["copy", "label", "typo", "css", "style", "color", "text", "small config"],
}


def run(cmd: list[str], cwd: Path, timeout: int = 5) -> tuple[int, str]:
    try:
        result = subprocess.run(
            cmd,
            cwd=str(cwd),
            text=True,
            capture_output=True,
            timeout=timeout,
            check=False,
        )
    except Exception as exc:  # noqa: BLE001 - diagnostics only
        return 1, f"unavailable: {exc}"
    output = (result.stdout or result.stderr).strip()
    return result.returncode, output


def read_json(path: Path) -> dict[str, Any]:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return {}
    return data if isinstance(data, dict) else {}


def find_root(start: Path) -> Path:
    current = start.resolve()
    if current.is_file():
        current = current.parent
    for candidate in [current, *current.parents]:
        if any((candidate / marker).exists() for marker in STACK_MARKERS):
            return candidate
    return current


def package_scripts(root: Path) -> dict[str, str]:
    data = read_json(root / "package.json")
    scripts = data.get("scripts", {})
    return scripts if isinstance(scripts, dict) else {}


def detect_stack(root: Path) -> list[str]:
    names = {p.name.lower() for p in root.iterdir()} if root.exists() else set()
    stack: list[str] = []
    if "package.json" in names:
        stack.append("Node.js")
    if any(name.startswith("vite.config") for name in names):
        stack.append("Vite")
    if "next.config.js" in names or "next.config.mjs" in names:
        stack.append("Next.js")
    if "requirements.txt" in names or "pyproject.toml" in names:
        stack.append("Python")
    if "main.py" in names or any(root.glob("**/main.py")):
        stack.append("FastAPI/Python candidate")
    if any(root.glob("**/*.wxml")):
        stack.append("WeChat mini program candidate")
    if "docker-compose.yml" in names or "docker-compose.yaml" in names:
        stack.append("Docker Compose")
    return stack


def keyword_hit(request: str, group: str) -> bool:
    text = request.lower()
    return any(keyword in text for keyword in MODE_KEYWORDS[group])


def classify_mode(request: str) -> tuple[str, list[str]]:
    reasons: list[str] = []
    if keyword_hit(request, "assess"):
        reasons.append("read-only or analysis wording")
        return "Assess", reasons
    if keyword_hit(request, "init"):
        reasons.append("project memory initialization wording")
        return "Init", reasons
    if keyword_hit(request, "recover"):
        reasons.append("recovery or rollback wording")
        return "Recover", reasons
    if keyword_hit(request, "import"):
        reasons.append("external data import wording")
        return "Import", reasons
    if keyword_hit(request, "deep"):
        reasons.append("high-risk system boundary wording")
        return "Deep", reasons
    if keyword_hit(request, "light") and not re.search(r"\b(api|backend|database|auth|deploy|import)\b", request.lower()):
        reasons.append("small isolated wording")
        return "Light", reasons
    reasons.append("default for normal code change")
    return "Standard", reasons


def memory_plan(root: Path, mode: str) -> list[str]:
    present = {name for name in MEMORY_FILES if (root / name).exists()}
    plan: list[str] = [name for name in ["AGENTS.md", "MEMORY_INDEX.md", "NEXT_TASKS.md"] if name in present]

    def add(name: str) -> None:
        if name in present and name not in plan:
            plan.append(name)

    if mode in {"Standard", "Deep", "Recover", "Import"}:
        add("PROJECT_CONTEXT.md")
        add("VERIFICATION.md")
    if mode in {"Deep", "Recover", "Import"}:
        add("DECISIONS.md")
        add("PROGRESS.md")
    return plan


def verification_plan(root: Path, mode: str) -> list[str]:
    scripts = package_scripts(root)
    checks: list[str] = []
    for name in ["lint", "typecheck", "test", "build"]:
        if name in scripts:
            checks.append(f"npm run {name}")
    if (root / "requirements.txt").exists() or (root / "pyproject.toml").exists():
        checks.append("python -m compileall <changed-python-paths>")
    if mode in {"Standard", "Deep"}:
        if "dev" in scripts:
            checks.append("npm run dev and browser/API smoke check")
        if any(root.glob("**/main.py")):
            checks.append("start backend or probe affected FastAPI endpoint")
    if mode == "Import":
        checks.extend(["preview rows", "duplicate/count check before write", "post-import API/UI/database readback"])
    if mode == "Recover":
        checks.append("compare restored behavior against old evidence")
    if not checks:
        checks.append("run the smallest project-specific check from VERIFICATION.md or changed module")
    return checks


def stop_gates(request: str, mode: str) -> list[str]:
    gates: list[str] = []
    text = request.lower()
    patterns = [
        ("delete/overwrite data", r"\b(delete|drop|truncate|overwrite|wipe)\b"),
        ("database migration/schema change", r"\b(migration|schema|alter table|migrate)\b"),
        ("auth/permission/payment/security boundary", r"\b(auth|permission|payment|security|secret)\b"),
        ("production/deployment change", r"\b(production|prod|deploy|restart service)\b"),
        ("public API contract change", r"\b(public api|api contract|breaking change)\b"),
    ]
    for label, pattern in patterns:
        if re.search(pattern, text):
            gates.append(label)
    if mode == "Assess":
        gates.append("read-only request")
    return gates


def inspect(root_arg: str, request: str) -> dict[str, Any]:
    root = find_root(Path(root_arg))
    markers = [marker for marker in STACK_MARKERS if (root / marker).exists()]
    mode, reasons = classify_mode(request)
    memory = {name: (root / name).exists() for name in MEMORY_FILES}
    code, git_top = run(["git", "rev-parse", "--show-toplevel"], root)
    _, branch = run(["git", "branch", "--show-current"], root) if code == 0 else (1, "")
    _, status = run(["git", "status", "--short"], root) if code == 0 else (1, "")
    gates = stop_gates(request, mode)

    return {
        "root": str(root),
        "markers": markers,
        "stack": detect_stack(root),
        "mode": mode,
        "mode_reasons": reasons,
        "memory_files": memory,
        "read_memory": memory_plan(root, mode),
        "need_checkpoint": mode == "Deep" and code == 0,
        "stop_gates": gates,
        "verification": verification_plan(root, mode),
        "git": {
            "present": code == 0,
            "top_level": git_top if code == 0 else "",
            "branch": branch,
            "status_short": status,
        },
    }


def print_markdown(info: dict[str, Any]) -> None:
    print("# CodexFlow Smart Plan")
    print()
    print(f"- Root: `{info['root']}`")
    print(f"- Mode: `{info['mode']}` ({'; '.join(info['mode_reasons'])})")
    print(f"- Stack: {', '.join(info['stack']) or 'unknown'}")
    print(f"- Markers: {', '.join(info['markers']) or 'none'}")
    print(f"- Need checkpoint: {info['need_checkpoint']}")
    print()
    print("## Memory To Read")
    if info["read_memory"]:
        for name in info["read_memory"]:
            print(f"- {name}")
    else:
        print("- none present")
    print()
    print("## Stop Gates")
    if info["stop_gates"]:
        for gate in info["stop_gates"]:
            print(f"- {gate}")
    else:
        print("- none detected")
    print()
    print("## Verification Candidates")
    for check in info["verification"]:
        print(f"- {check}")
    print()
    print("## Git")
    git = info["git"]
    print(f"- Present: {git['present']}")
    if git["top_level"]:
        print(f"- Top level: `{git['top_level']}`")
    if git["branch"]:
        print(f"- Branch: `{git['branch']}`")
    if git["status_short"]:
        print("```text")
        print(git["status_short"])
        print("```")


def main() -> int:
    parser = argparse.ArgumentParser(description="Plan CodexFlow Smart project work without writing files.")
    parser.add_argument("--root", default=os.getcwd())
    parser.add_argument("--request", default="")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    info = inspect(args.root, args.request)
    if args.json:
        print(json.dumps(info, ensure_ascii=False, indent=2))
    else:
        print_markdown(info)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
