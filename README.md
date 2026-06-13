# CodexFlow Smart

CodexFlow Smart is a Codex Skill for safer, faster local project work. It helps Codex take over an existing software project, load only the context that matters, choose the lightest safe risk mode, make focused changes, verify real behavior, and keep project memory up to date.

This repository is itself the installable skill folder.

## About / 關於

**English:** CodexFlow Smart is an Ah Limosa Codex Skill that helps AI coding sessions stay focused, safer, and easier to verify. It guides Codex to understand a project first, choose the right risk mode, make minimal changes, and record what was verified.

**中文：** CodexFlow Smart 是 Ah Limosa 的 Codex Skill，幫助 AI 開發流程更聚焦、更安全、更容易驗證。它會引導 Codex 先理解專案、判斷風險模式、做最小有效修改，並記錄已完成的驗證結果。

Website: [ahlimosa.com](https://ahlimosa.com)  
網站：[ahlimosa.com](https://ahlimosa.com)

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

Clone this repository into your Codex skills directory. Personal skills should live in `$HOME/.agents/skills`; repo-scoped skills can live in `.agents/skills` inside the project that should use them.

Recommended Windows personal install:

```powershell
mkdir "$env:USERPROFILE\.agents\skills" -Force
git clone https://github.com/ahlimosa-gif/codexflow.git "$env:USERPROFILE\.agents\skills\codexflow-smart"
```

Recommended repo-scoped install:

```powershell
mkdir ".agents\skills" -Force
git clone https://github.com/ahlimosa-gif/codexflow.git ".agents\skills\codexflow-smart"
```

macOS/Linux:

```bash
mkdir -p ~/.agents/skills
git clone https://github.com/ahlimosa-gif/codexflow.git ~/.agents/skills/codexflow-smart
```

Restart Codex after installing so the skill list refreshes.

## Quick Use

This skill disables implicit invocation in `agents/openai.yaml`, so Codex should use it only when you explicitly ask for `$codexflow-smart`.

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

## When Not To Use

Do not reach for this skill when the task is intentionally tiny or conceptual:

- changing one line of copy
- generating a quick component prototype
- asking a coding concept question
- doing a small UI tweak where the full project workflow would slow you down

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

CodexFlow Smart does not replace `AGENTS.md`. Keep project rules in `AGENTS.md`, and keep durable project state in the memory files.

For a repo-scoped install, the recommended structure is:

```text
your-project/
  AGENTS.md
  MEMORY_INDEX.md
  NEXT_TASKS.md
  PROJECT_CONTEXT.md
  PROGRESS.md
  DECISIONS.md
  VERIFICATION.md
  .agents/
    skills/
      codexflow-smart/
```

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
codexflow-smart/
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
