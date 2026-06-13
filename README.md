# CodexFlow Smart

CodexFlow Smart is a Codex Skill for safer, faster local project work. It helps Codex take over an existing software project, load only the context that matters, choose the lightest safe risk mode, make focused changes, verify real behavior, and keep project memory up to date.

This repository is itself the installable skill folder.

## Why This Skill Exists

AI coding sessions often slow down or go wrong because the assistant starts in the wrong folder, reads too much context, misses project rules, edits before understanding risk, or finishes without a real verification trail.

CodexFlow Smart turns that into a repeatable workflow:

- confirm the real project root
- read only relevant project memory
- route the task into a risk mode
- explain likely cause and planned files before editing
- make the smallest useful change
- verify with concrete checks
- update project memory with concise conclusions

## Good Fit

Use CodexFlow Smart for:

- FastAPI backends
- React/Vite frontends
- WeChat mini programs
- MySQL-backed business systems
- local automation tools
- data import workflows
- recovery of previous good behavior
- projects with persistent memory files such as `AGENTS.md`, `MEMORY_INDEX.md`, `NEXT_TASKS.md`, `PROJECT_CONTEXT.md`, `PROGRESS.md`, `DECISIONS.md`, and `VERIFICATION.md`

## Install

Clone this repository into your Codex skills directory.

Windows:

```powershell
git clone https://github.com/ahlimosa-gif/codexflow.git "$env:USERPROFILE\.codex\skills\codexflow-smart"
```

macOS/Linux:

```bash
git clone https://github.com/ahlimosa-gif/codexflow.git ~/.codex/skills/codexflow-smart
```

Restart Codex after installing so the skill list refreshes.

## Quick Use

Ask Codex to use the skill:

```text
Use $codexflow-smart to inspect this project, choose the safest mode, fix the issue, verify it, and update project memory.
```

For a read-only project plan:

```text
Use $codexflow-smart to study this repo and tell me the risk mode, files to read, and verification plan before editing.
```

## What Makes It Smarter

The main upgrade is `scripts/flow_plan.py`, a read-only planner that produces a compact execution plan from the current project and user request.

Example:

```bash
python scripts/flow_plan.py --root <project-root> --request "fix login API and verify endpoint"
```

It reports:

- likely project root
- detected stack markers
- task mode
- memory files to read
- stop gates
- verification candidates
- git state when available

## Task Modes

CodexFlow Smart uses the lightest mode that can safely solve the request:

- `Assess`: read-only inspection, review, planning, or explanation
- `Init`: create missing project memory files
- `Light`: small copy, style, label, config, or obvious isolated fixes
- `Standard`: normal bug fixes, features, page/API work, and integrations
- `Deep`: database, auth, permissions, payment, deployment, public API contracts, performance, concurrency, or large refactors
- `Recover`: restore previous good behavior from evidence
- `Import`: import external CSV, spreadsheet, PDF-extracted, scraped, or uploaded data into a real system

## Project Memory

The skill supports this root-level memory set:

```text
AGENTS.md
MEMORY_INDEX.md
NEXT_TASKS.md
PROJECT_CONTEXT.md
PROGRESS.md
DECISIONS.md
VERIFICATION.md
checkpoints/
```

Memory is meant to stay short. Store conclusions, current source of truth, verification commands, decisions, and follow-ups. Do not store long logs, full diffs, stack traces, or temporary guesses.

## Scripts

Plan work without writing files:

```bash
python scripts/flow_plan.py --root <project-root> --request "<user request>"
```

Initialize memory files without overwriting existing files:

```bash
python scripts/init_project_memory.py --root <project-root>
```

Append a compact progress entry:

```bash
python scripts/append_progress.py --root <project-root> --title "Task" --mode Standard
```

Create a checkpoint before high-risk work:

```bash
python scripts/make_checkpoint.py --root <project-root> --title "Risky task"
```

## Repository Structure

```text
codexflow/
  SKILL.md
  agents/
    openai.yaml
  references/
    risk-verification.md
  scripts/
    append_progress.py
    flow_plan.py
    init_project_memory.py
    make_checkpoint.py
  templates/
    AGENTS.template.md
    MEMORY_INDEX.template.md
    NEXT_TASKS.template.md
    PROJECT_CONTEXT.template.md
    PROGRESS.template.md
    DECISIONS.template.md
    VERIFICATION.template.md
```

## Suggested Default Prompt

```text
Use $codexflow-smart to inspect this project, choose the lightest safe mode, read only needed memory, make a minimal verified change, and update project memory.
```
