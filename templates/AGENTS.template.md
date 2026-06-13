# Project Agent Rules

Use the user's language for user-facing summaries. Keep code, identifiers, API paths, database fields, and commands in English.

## Working Rules

1. Confirm the real project root before editing.
2. Read `AGENTS.md`, `MEMORY_INDEX.md`, and `NEXT_TASKS.md` first when they exist.
3. Read `PROJECT_CONTEXT.md`, `PROGRESS.md`, `DECISIONS.md`, and `VERIFICATION.md` only when the task needs them.
4. Do not start with broad refactors. Locate the issue and make the smallest effective change.
5. Preserve the existing framework, database, package manager, directory structure, API contracts, and naming style unless explicitly asked to change them.
6. Use the project's existing database. If unclear and database work is requested for a typical business system, prefer MySQL unless the user says otherwise.
7. Do not hard-code secrets, accounts, database passwords, or API keys. Use `.env` or environment variables.
8. Before editing, briefly state the likely cause, planned files, risk, and verification method.
9. After editing, run the strongest practical verification and summarize the result.
10. Update `PROGRESS.md` and `NEXT_TASKS.md` after completed code work when project memory exists.
11. Update `DECISIONS.md` only for durable technical decisions.
12. Update `MEMORY_INDEX.md` only when source of truth, priority, major known issue, or project state changes.

## Stop Before Proceeding

Ask before deleting data, running migrations, changing auth/permissions/payment, replacing the stack, changing public API contracts, or touching production without a rollback path.
