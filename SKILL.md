---
name: shhh-strategy
description: Analyze unfamiliar mathematical-modeling contest problems from the complete statement and attachments, lock deliverables and ambiguity, adjudicate justified solution routes, control complexity, and pressure-test independent reasoning. Use for new-problem understanding and strategy design; historical-paper comparison is off by default and activates only for an explicit retrospective-training request. Do not use as a substitute for numerical implementation, full-paper drafting, or submission compliance.
---

# Shhh Strategy

## Purpose

Turn an unfamiliar contest problem into a defensible, executable modeling strategy without copying a historical answer or accumulating models for appearance. Preserve necessary complexity, reject unsupported complexity, and state honestly whether the work is only an audit, an executable route, or a solved and validated result.

This skill encapsulates the user's V27.2 stability-guarded strategy engine, the V27.1 reasoning core, and its 34-problem anti-overpruning regression. It does not train model weights and does not guarantee an award.

## Absolute Boundary

Do not read, invoke, cite, or rely on any other locally installed mathematical-modeling skill. Work from the supplied problem, its attachments, this skill's references, and the mapped local evidence archive only.

## Always Read

1. [references/core-protocol.md](references/core-protocol.md) for the problem lock and route workflow.
2. [references/structural-gates.md](references/structural-gates.md) as the low-cost trigger router; then read every detailed gate group it activates.
3. [references/complexity-stop-gates.md](references/complexity-stop-gates.md) before selecting or comparing models.
4. [references/output-modes.md](references/output-modes.md) to match the user's requested stopping point.

## Read Only When Triggered

- Read [references/input-visual-integrity.md](references/input-visual-integrity.md) whenever the input contains PDFs, Word files, spreadsheets, figures, formulas, templates, or multiple attachments.
- Read [references/state-ledger.md](references/state-ledger.md) when the problem has local attachments, more than one material confirmation, more than one working session, or an auditable freeze.
- Read [references/post-route-stress-reread.md](references/post-route-stress-reread.md) after a route first reaches `route_executable`, or whenever the user asks to test, reread, strengthen, or optimize an established strategy. Perform this pass before numerical solving unless the user explicitly changes the order.
- Read [references/historical-transfer-index.md](references/historical-transfer-index.md) only when the user explicitly requests retrospective training from past problems after an independent route exists.
- Read [references/paper-comparison.md](references/paper-comparison.md) only when the user explicitly requests retrospective comparison with prior papers, expert reviews, or official commentary. A problem being old or previously published is not enough.
- Read [references/knowledge-source-map.md](references/knowledge-source-map.md) only when an explicitly requested retrospective comparison needs exact historical evidence, a paper card, an original figure, or archive integrity.

## Operating Invariants

- Problem statement and attachments outrank historical papers.
- Treat every supplied problem as an independent/current task by default. Do not search for, suggest, or unlock same-problem solutions, papers, reviews, or commentary merely because the problem is historically identifiable.
- Historical comparison is a separate opt-in retrospective-training mode. Activate it only when the user explicitly asks to learn from or compare against past-problem evidence; never make it a completion gate or default next step.
- Do not choose a model name before every subquestion has an output, information time, dependency, and validation route.
- Keep all necessary multistage, branching, corroborative, or ensemble routes. Remove only parts lacking a problem trigger, data capacity, independent value, or contribution to a required conclusion.
- Audit findings are not a solution. A route without variables, relations, constraints, algorithm exit, output schema, and validation remains a route draft.
- Label high-value claims internally as descriptive, predictive, or causal and never upgrade their wording beyond the available evidence.
- Treat confirmation as part of the analysis, not as a final courtesy: do not silently settle a material ambiguity, preference, assumption, route fork, complexity upgrade, or claim boundary on the user's behalf.
- For a ledger-triggering task, a quality-state claim is valid only when the current ledger passes `scripts/analysis_state.py validate`. Preserve superseded locks and rejected routes instead of rewriting history.
- File inventory completeness and semantic understanding are different claims. Hashes prove identity; machine metadata proves indexing; required text, visual, formula, data, and schema inspections prove coverage only after they are explicitly completed.

## Mandatory Confirmation Contract

Apply this contract whenever this skill is active.

### What must be verified with the user

Pause before dependent work and explicitly verify any item that meets at least one condition:

- source material is missing, unreadable, internally inconsistent, or open to more than one materially different interpretation;
- an assumption would change the object, information set, feasible region, objective, output, validation standard, or downstream route;
- the statement does not determine a preference such as weights, tie-breakers, risk attitude, accuracy/runtime tradeoff, or acceptable approximation;
- two credible routes answer different versions of the task or support different levels of conclusion;
- adding or removing a component would materially change complexity, identifiability, robustness, or the paper's main line;
- historical evidence, expert commentary, or a counterexample would overturn a previously locked decision;
- the permitted conclusion could be confused between description, prediction, mechanism, causality, scenario, candidate, or proof.

For each confirmation point, give the local evidence, explain the consequence of each live option, recommend one option, and state exactly what will be locked if approved. Do not present an unsupported preference as the only choice.

### What does not require a question

First resolve facts that can be settled by rereading supplied materials, checking attachments, calculating an identity, or performing another safe read-only check. Do not ask the user to confirm facts already fixed unambiguously by the source. Do not interrupt for wording, notation, formatting, or reversible details that cannot change the reasoning. Combine only tightly coupled confirmation items; never accumulate unrelated forks into one opaque approval request.

### Locking and continuation

- Record an approved decision as locked and use it consistently downstream.
- Reopen a locked decision only when new evidence conflicts with it; show the conflict and request confirmation again.
- While waiting, continue only work independent of the unresolved decision. Do not cross the dependency boundary.
- If no material uncertainty exists, proceed autonomously to the next genuine confirmation point.

### Required status footer

Every user-facing response produced while this skill is active must end with a compact status block containing:

- `本次做了什么：` the concrete analysis, check, comparison, or modification just completed;
- `当前得到什么：` the locked result and current quality state, without overstating completion;
- `待你确认/下一步：` the exact pending decision, or `无需确认` plus the next action when no decision is pending.

Keep the block brief and specific. It supplements the substantive answer and must not replace evidence or reasoning.
When the current request is complete and no decision remains, write `无需确认；当前请求已完成` or name the next already-requested in-scope action. Do not propose historical-paper comparison unless retrospective comparison is already explicitly in scope.

## Default Workflow

1. Inventory every page, attachment, figure, table, formula, note, unit, field, and output template. For local files, use `scripts/inventory_problem.py`; do not call the inventory complete while a required inspection remains pending or blocked.
2. When the state-ledger trigger applies, initialize or resume one ledger and validate it before relying on previous locks.
3. Build the per-subquestion lock: object, input, available information, state, decision, hard constraints, objective, output, and dependency.
4. Scan the structural gate router, record exact triggers, and read only the detailed gate groups supported by current evidence.
5. Replay one representative object's lifecycle and all relevant clocks, modes, abnormal states, and terminal conditions.
6. Attack the first interpretation with at least one alternative reading, boundary case, and fatal counterexample.
7. Establish a credible baseline, identify its concrete defect, and admit only upgrades that pass the complexity gates.
8. Provide executable mathematics and validation interfaces; scan all 18 gate names, read any newly triggered group, and mark the current quality state honestly.
9. Pressure-test the executable route, reread the complete statement and attachments, and revise only findings supported by source evidence, mathematics, or a reproduced counterexample.
10. Validate and seal the ledger, freeze the strengthened independent analysis and source hashes when an auditable record is useful, then stop at the user's requested output mode.
11. Only under an explicit retrospective-training request, separately audit problem understanding and solution method; promote only cross-problem mechanisms, never a memorized answer.

Apply the Mandatory Confirmation Contract at every material dependency boundary in this workflow. A numbered step is not automatically a checkpoint; a decision that can change downstream reasoning is.

Use the scripts in `scripts/` for deterministic inventory, state, freeze, regression, and archive checks. Read [references/behavior-regression.md](references/behavior-regression.md) only when maintaining or promoting the skill; never expose its case expectations as a substitute for independent analysis.
