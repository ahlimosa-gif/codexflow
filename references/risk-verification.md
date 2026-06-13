# Risk And Verification Reference

Read this file for Deep, Recover, and Import tasks that touch data integrity, production, public behavior, or rollback risk.

## Deep Work

- Before editing, identify the boundary: schema, auth, payment, deployment, public API, concurrency, performance, or shared module.
- Find the smallest reversible change. Avoid broad cleanup while fixing the risky issue.
- Create a checkpoint when git or project memory is available.
- Stop before destructive commands, migrations, production restarts, or contract changes unless the user clearly approved them.
- Verify the boundary directly: auth flow, permission check, migration dry run, API contract probe, deployment smoke test, or performance reproduction.

## Recover Work

- Reconstruct evidence before rewriting: git history, old assets, backups, deployment artifacts, logs, screenshots, hashes, or user-provided expected behavior.
- Restore the narrowest behavior first. Do not rewrite from scratch unless recovery evidence is unavailable.
- Verify both sides: the old regression is fixed and the adjacent current behavior still works.

## Import Work

- Treat the real app/database/API as source of truth.
- Preview source data and produce a field map before writing.
- Check duplicates, nullable fields, enum values, date/time zones, currency units, and encoding.
- Record counts before and after the write.
- Verify through the live path that users rely on: API response, dashboard, database readback, or admin UI.

## Public API Notes

When an API is involved, report:

- Path and method.
- Request params/body fields.
- Response fields.
- Frontend/backend field mapping.
- Any backward compatibility concern.
