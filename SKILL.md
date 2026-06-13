---
name: codexflow-smart
description: Adaptive project execution workflow for local software projects. Use when Codex is asked to inspect, initialize, modify, debug, recover, import data into, verify, continue, or maintain a code project, especially FastAPI backends, React/Vite frontends, WeChat mini programs, MySQL-backed systems, automation tools, or repos with AGENTS.md, MEMORY_INDEX.md, NEXT_TASKS.md, PROJECT_CONTEXT.md, PROGRESS.md, DECISIONS.md, or VERIFICATION.md. Guides Codex to find the real project root, load only useful memory, route risk, make the smallest safe change, verify real behavior, and keep project memory concise.
---

# CodexFlow Smart

CodexFlow Smart is a faster project takeover workflow. It optimizes for working software with the least necessary context, smallest safe edit, strongest practical verification, and concise durable memory.

## Start Here

1. Confirm the real project root. Prefer the git top-level or the folder containing stack markers such as `package.json`, `pyproject.toml`, `requirements.txt`, `vite.config.*`, `main.py`, `docker-compose.*`, or mini program files.
2. Run the read-only planner when possible:

```bash
python scripts/flow_plan.py --root <project-root> --request "<user request>"
```

Use the bundled Python/runtime path if `python` is unavailable. If the script cannot run, apply the routing rules below manually.

3. Read only the memory files the selected mode needs.
4. Before editing, send a short pre-work note with likely cause, planned files, risk, and verification.
5. Edit narrowly, verify directly, then update project memory if it exists.

## Context Loading

Always treat project files as the source of truth.

- Read first when present: `AGENTS.md`, `MEMORY_INDEX.md`, `NEXT_TASKS.md`.
- Read `PROJECT_CONTEXT.md` when startup, architecture, module ownership, environment, API, database, or deployment details matter.
- Read `PROGRESS.md` only for relevant history. If long, search with `rg` and read nearby sections.
- Read `DECISIONS.md` for framework, database, auth, deployment, public API, or directory-structure decisions.
- Read `VERIFICATION.md` before claiming a code change is complete.
- Do not create memory files unless the user asked for initialization or approved it after missing memory is found.

## Mode Router

Use the lightest mode that can safely complete the request.

| Mode | Use when | Memory | Extra action |
| --- | --- | --- | --- |
| `Assess` | User says study, inspect, review, plan, analyze, or do not edit | Required files only | Read-only. Do not write files. |
| `Init` | User asks to create project memory or workflow files | Required files if present | Run `init_project_memory.py`; never overwrite without explicit approval. |
| `Light` | Copy, labels, small styles, isolated config, obvious local bug | Required files | Avoid broad modules and contracts. |
| `Standard` | Normal bug fix, feature, page/API integration, backend endpoint, tool improvement | Required files plus relevant context and verification | Update memory after code changes when memory exists. |
| `Deep` | Database schema, auth, permissions, payment, deployment, public API contract, security, performance, concurrency, large refactor | Required files plus `PROJECT_CONTEXT.md`, `DECISIONS.md`, `VERIFICATION.md`, relevant `PROGRESS.md` | Create a checkpoint before editing when possible. Stop for destructive or contract-changing steps. |
| `Recover` | Restore previous behavior, revert regression, compare last-known-good | Required files plus relevant history | Reconstruct evidence before rewriting. |
| `Import` | CSV, spreadsheet, PDF-extracted, scraped, or external data enters the real app/database | Required files plus database/API context | Preview, map fields, check duplicates/counts, then verify through real API/UI/database. |

For Deep, Recover, or Import work, read `references/risk-verification.md` if the task touches production, data integrity, or public behavior.

## Pre-Work Note

Before edits, keep the user update short. Match the user's language.

```text
Mode:
Files read:
Likely cause:
Planned edits:
Risk:
Verification:
```

If the user writes Chinese, answer in Chinese; keep code, identifiers, API paths, database fields, and commands in English.

## Stop Gates

Pause and ask before you:

- Delete, overwrite, migrate, or bulk-edit user/business data.
- Change auth, permissions, payment, security boundaries, or secrets handling.
- Replace framework, database, package manager, deployment model, or directory structure.
- Change public API request/response contracts.
- Touch production services without a rollback path.
- Write files during an Assess-only request.
- Continue after evidence shows the current checkout is not the running source of truth.

## Execution Rules

- Use `rg` or project-native search first.
- Keep edits local to the request and existing ownership boundaries.
- Prefer existing helpers, schemas, components, API clients, and naming style.
- Do not hard-code secrets. Use `.env` or environment variables.
- For APIs, state path, request params/body, response fields, and frontend/backend field mapping when relevant.
- For frontend changes, include usable loading, error, empty, disabled, and success feedback states where the changed flow needs them.
- For backend changes, run startup, tests, endpoint probes, or the smallest useful verification.
- For MySQL-backed work, keep MySQL unless the project already uses another database or the user explicitly asks to change it.

## Verification Ladder

Choose the strongest practical check from the project context:

1. Static sanity: lint, typecheck, syntax compile.
2. Targeted tests for changed modules.
3. Build/startup command.
4. API probe with realistic input.
5. Browser/UI check for frontend behavior.
6. Database readback/count check for data changes.
7. Live/deployment smoke check when production was touched and approved.

Before saying done, compare actual output or observed behavior with the user's goal. If verification cannot run, state the exact reason and the next command to run.

## Memory Updates

When root-level project memory exists and files changed:

- Append a compact `PROGRESS.md` entry with date, task, mode, changed files, root cause, verification, result, and follow-up.
- Update `NEXT_TASKS.md` only when priorities changed, a blocker remains, or a follow-up is important.
- Update `DECISIONS.md` only for durable choices.
- Update `MEMORY_INDEX.md` only when source of truth, current priority, key modules, or high-risk areas changed.
- Keep `MEMORY_INDEX.md` and `NEXT_TASKS.md` under 100 lines. Summarize old `PROGRESS.md` sections when they become too long.
- Never paste long logs, full diffs, stack traces, or temporary guesses into memory.

Use helper scripts when useful:

```bash
python scripts/init_project_memory.py --root <project-root>
python scripts/append_progress.py --root <project-root> --title "Task" --mode Standard
python scripts/make_checkpoint.py --root <project-root> --title "Risky task"
```

## Completion Format

End with a concise status in the user's language:

```text
Result:
Changed files:
Verification:
Memory updates:
Next step:
```
