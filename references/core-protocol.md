# Core Problem-to-Strategy Protocol

## 1. Establish the source of truth

The complete statement and attachments are the constraint truth. Separate confirmed facts, reasonable inferences, and unresolved items. Never fill a missing page, figure, coordinate convention, distribution, threshold, weight, or objective preference from memory.

Before modeling, confirm:

- all statement pages and subquestions;
- all attachment names and schemas;
- figures, arrows, coordinate directions, legends, footnotes, and table notes;
- units, time bases, index identities, missing-value codes, and output templates;
- precision, file, table, or algorithmic deliverables.

If anything material is missing, continue only with a provisional branch and state what cannot yet be concluded.

## 2. Lock every subquestion

For every subquestion record:

| Field | Required meaning |
|---|---|
| object | entity, system, population, path, event, or material being modeled |
| given input | statement facts and attachment fields available at the relevant time |
| information time | what is known before the decision and what happens later |
| state | quantities that evolve or encode the system condition |
| decision/control | quantities the proposed method may actually choose |
| hard constraints | conditions that cannot be traded away by weights |
| objective/question | explanation, estimation, prediction, optimization, control, identification, construction, or evaluation |
| output | exact number, route, table, file, proof, policy, interval, or comparison required |
| dependency | upstream output reused downstream, with uncertainty propagation |
| validation | direct identity, holdout, scenario, proof, bound, replay, or independent recomputation |

Do not proceed to final route selection while any required output lacks a mathematical producer.

## 3. Reconstruct the mechanism before naming algorithms

Replay one representative object from initialization to terminal state. Check:

- process clock, recording clock, decision clock, and event clock;
- initialization, transition, steady operation, terminal accounting;
- normal, abnormal, recovery, and irreversible states;
- continuous evolution versus event-triggered equation changes;
- object identity, repeated measurements, exposure windows, and denominators;
- observation, latent state, control action, and evaluation metric as distinct roles.

Write a one-sentence mother problem only after this replay. The sentence should name the mechanism and required decision, not a historical problem or algorithm.

## 4. Adversarial interpretation check

Before accepting the first reading:

1. propose at least one plausible alternative interpretation;
2. identify which fact, figure, field, or output would distinguish the branches;
3. test a boundary or degenerate case;
4. write the most damaging counterexample to the proposed route;
5. check whether a proxy objective can improve while the real objective worsens;
6. for minimum-count questions, start at 0 and 1 and close with impossibility plus construction;
7. for inverse problems, check whether the requested quantity is identifiable or only a product, ratio, integral, or equivalence class;
8. for optimization, verify that the objective exists, is not constant on the feasible set, and has an authorized tie-breaker.

Keep unresolved structural branches. Do not force a unique route merely for presentation.

## 5. Build the route

Start with a credible baseline that can answer the deliverable under the same information and constraints as the proposed route. A baseline is not required to be simplistic; it must be legitimate.

For every additional component record:

- exact problem evidence that triggers it;
- the baseline defect it repairs or the distinct proof responsibility it carries;
- variables, units, domains, relations, constraints, and boundaries;
- algorithm entry, exit, termination, and output schema;
- validation evidence and the condition that would make the component unnecessary.

Use one or many models according to the problem. Multistage pipelines, structural branches, lower-bound/candidate pairs, independent solvers, and validated ensembles are allowed when their roles are distinct. Model count itself is never a quality criterion.

## 6. Validation is route-specific

Choose evidence that matches the route:

- physics/geometry: units, conservation, special cases, continuous-event boundaries, mesh or step convergence, independent formula or solver;
- statistical learning: independent experimental units, leakage-safe preprocessing, nested/blocked validation, calibration, uncertainty, support shift;
- optimization: feasibility replay, common evaluator, lower bound or gap, exact small case, multistart stability, perturbation;
- construction: lower bound, explicit construction, correctness proof, extreme cases;
- policy/causal: intervention and comparator, identification assumptions, overlap, spillover, sensitivity, scenario boundary.

The final candidate must be recomputed with the same legal information, constraints, denominator, and high-fidelity evaluator as its baseline.

## 7. Quality states

- `draft`: source coverage, locks, or routes are incomplete.
- `understanding_locked`: deliverables and interpretations are locked; no final model yet.
- `audit_complete`: risks and candidate routes are known; not yet executable.
- `route_executable`: variables, mathematics, constraints, algorithm, output, and validation are complete; no numerical result is implied.
- `solved_unvalidated`: a result exists but has not passed independent validation.
- `solved_and_validated`: reproducible result and required checks exist.

Never infer a later state from a detailed audit. If the user asks only for ideas, stop at `route_executable` and say that numerical solution remains.

For local-file, multi-checkpoint, or multi-session work, maintain the ledger defined in `state-ledger.md`. A state name in prose does not count unless the current ledger validates and all transition gates pass.

## 8. Freeze and stop at the requested mode

When an auditable record is useful, save the statement/attachment hashes, the independent interpretation, selected route, rejected routes, open ambiguity, and current quality state. Use `scripts/freeze_analysis.py` when files are local. Freezing completes the independent record; it does not unlock or imply a historical-paper step.

Stop at the user's requested output mode. Do not recommend same-problem papers, award papers, expert reviews, or official commentary as a default continuation. Historical comparison is a separate retrospective-training task and requires an explicit user request even when the problem is old or recognizable.

If that retrospective mode is explicitly requested and historical evidence changes the route, preserve the original freeze and record the correction separately. Upgrade a general rule only if it survives at least two structurally different problems and does not degrade existing cases.
