# Analysis State Ledger

Use a state ledger when the problem has local attachments, more than one material confirmation point, more than one working session, or an auditable freeze. The ledger is an internal reasoning record; it does not force the user-facing prose into a fixed template.

## Why it exists

The ledger prevents four failures: silently changing an approved interpretation, forgetting a blocking ambiguity, promoting an audit to a solution, and losing the evidence that activated or rejected a route. It records provenance and consistency, not truth by itself.

## Create and maintain it

```text
python scripts/analysis_state.py init --case-id <id> --output <analysis-state.json> [--inventory <source-inventory.json>]
python scripts/analysis_state.py validate <analysis-state.json>
python scripts/analysis_state.py transition <analysis-state.json> --to <quality-state> --reason <evidence-based reason>
python scripts/analysis_state.py summary <analysis-state.json>
```

Populate the JSON with the schema at [analysis-state.schema.json](analysis-state.schema.json). Use stable IDs for subquestions, ambiguities, locks, routes, and validation items. Prefer concise source pointers over copied passages.

## State rules

- `draft`: sources or locks are still incomplete.
- `understanding_locked`: every subquestion has a locked deliverable record and no blocking ambiguity remains open.
- `audit_complete`: the interpretation is locked, a credible baseline and triggered route candidates exist, and risks are recorded; the route may still be non-executable.
- `route_executable`: every selected route has trigger evidence, variables, relations, constraints, algorithm exit, output schema, and validation.
- `solved_unvalidated`: numerical or constructive outputs exist but independent checks are incomplete.
- `solved_and_validated`: required results are reproducible and every blocking validation has passed.

State transitions are monotone unless new evidence explicitly reopens a lock. A later state may regress to an earlier state, but the change event must name the conflicting evidence and affected dependencies.

## Confirmation and change discipline

- Put material unresolved choices in `ambiguities`; do not hide them in notes.
- Put approved interpretations, assumptions, route choices, complexity upgrades, and claim ceilings in `locks` with confirmation status and evidence.
- Record activated structural gates with exact triggers; never record a gate merely because its topic sounds relevant.
- Use `supersedes` rather than deleting an old lock. Keep rejected routes and their removal conditions.
- Keep the append-only `events` hash chain valid. The helper script appends transition events atomically; manual semantic edits must be followed by validation and a new event before freezing.

## Required exit checks

Before a user-facing quality-state claim, validate the ledger and ensure its state matches the actual work. A valid ledger proves structural completeness and preserved history, not analytical correctness.
