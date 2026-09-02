# Competition-Grade Route Readiness

Read this for every substantive contest-problem run after the first complete route exists. It converts the generalized lessons from the 23-problem/58-paper development archive, five held-out replays, five historically isolated cases, and the 34-case anti-overpruning audit into a forward-looking quality gate. It does not authorize same-problem retrieval, does not copy an old answer, and does not guarantee an award.

## Meaning of competition-grade

Competition-grade means the route is sufficiently specific, necessary, testable, reproducible, and communicable for a strong team to implement under contest conditions. It does **not** mean maximizing model count, equation count, runtime, or novelty. Complexity is retained only when the current statement, attachments, mathematics, or independent tests give it a distinct responsibility.

The route must reach a fixed point: a full reread or attack no longer reveals an unresolved defect that can change a required output, feasibility, identifiability, validation conclusion, or claim ceiling. If the remaining uncertainty comes from missing or non-identifying evidence, stop with a blocker, interval, branch, or scenario boundary instead of inventing precision.

## Two-pass minimum and repair fixed point

After the initial route draft, perform at least two materially different full passes:

1. **Source-triggered falsification pass**: reread the complete source and run the applicable counterexample, boundary, leakage, duplicate-unit, data-quality, identifiability, feasibility, robustness, abnormal-execution, and simplification tests.
2. **Competition-readiness pass**: audit every dimension and cross-case transfer check below from the final deliverables backward to variables, equations, algorithms, evidence, and claim boundaries.

When either pass finds a material defect, apply the smallest repair, replay every dependent subquestion and output, then repeat the affected pass. Add a structured `pass_records` entry with kind, scope, status, and evidence; `competition_readiness.audit_passes` must equal the number of completed records. A source-falsification record and a competition-readiness record are both mandatory. Do not count rereading a paragraph or renaming a method, and do not manufacture cycles when no material change is justified.

## Nine readiness dimensions

Every dimension is always applicable and must have a problem-specific method and evidence record before `competition_readiness.status` can be `ready`.

1. **source_and_deliverable_closure**: every official source inspection is complete; every subquestion and output field is locked; user, statement, attachment, and embedded-command channels remain separate.
2. **mechanism_state_information_fidelity**: representative-object lifecycle, state transitions, clocks, information sets, modes, abnormal branches, terminal accounting, quantifier order, and coordinate conventions reproduce the actual problem.
3. **mathematical_identifiability_closure**: variables, domains, units, assumptions, equations, objectives, constraints, initial/boundary conditions, degrees of freedom, identifiability, and well-posedness are explicit. Minimum/unique/optimal claims have the appropriate lower bound, construction, counterexample, or gap.
4. **necessary_complexity_and_proof_roles**: a credible simple baseline exists; every retained upgrade repairs a named defect or carries a distinct candidate, bound, branch, corroboration, or robustness duty; unsupported model-zoo complexity is removed.
5. **data_algorithm_operationality**: schemas, missingness, duplicates, outliers, independent unit, leakage controls, preprocessing scope, initialization, solver/estimator interface, termination, runtime risks, and deterministic artifact outputs are specified.
6. **falsification_validation_and_independence**: fatal counterexample, boundary and simplification challenges are recorded; the validation plan uses legal information, a common evaluator, pass/downgrade criteria, and an independent replay, exact small case, bound, held-out unit, or high-fidelity recalculation whenever the problem permits it.
7. **dependency_uncertainty_and_error_propagation**: subquestion dependencies, shared states/resources, upstream uncertainty, estimation error, scenario probability, and downstream decision consequences are propagated instead of resetting or combining independent answers after the fact.
8. **output_reproducibility_and_claim_consistency**: every requested number, table, figure, file, precision, and conclusion has a producer and consistency check; the result schema, validation schema, and descriptive/predictive/mechanism/causal/candidate/proven wording agree.
9. **contest_narrative_and_resource_feasibility**: the route can be explained as one coherent chain from problem to baseline, necessary upgrades, result, and validation; implementation order, compute/data needs, fallback, stopping condition, and paper-ready evidence responsibilities fit the contest setting.

## Cross-case national-first-prize experience checks

These checks are generalized reasoning duties, not old-problem templates. Record each as `pass` or `not_applicable` with a problem-specific reason.

- **mechanism_before_model_name**: infer mechanism and deliverable duties before naming algorithms.
- **information_clock_and_nonanticipativity**: separate process, observation, decision, event, and output clocks; prevent future information from entering earlier decisions.
- **ideal_realizable_true_evaluator**: when design or proxy states exist, separate the ideal target, constrained realizable state, and true/high-fidelity performance evaluator.
- **candidate_bound_corroboration_roles**: do not delete a second method merely because outputs look similar when it supplies a bound, construction, independent replay, or error certificate; do delete functional duplicates.
- **global_objective_and_coupling**: preserve shared capacity, global denominators, interfaces, connection costs, intersections/unions, and error propagation when decomposing subproblems.
- **minimum_from_smallest_case**: for minimum-number or necessity claims, start from 0/1 or the smallest legal case and pair impossibility/lower-bound reasoning with an attainable construction.
- **solver_complexity_separate_from_model_complexity**: allow global candidate generation, local refinement, exact small-case comparison, and independent replay when the optimization landscape requires them, while keeping one legal model and evaluator.
- **evidence_ceiling_and_no_old_answer_transfer**: historical experience may challenge the route but cannot supply current constants, assumptions, answers, or stronger claims than current evidence supports.

## Competition-readiness stop certificate

Promotion requires a concise stop certificate containing:

- retained route IDs and each route's unique responsibility, as structured route mappings;
- every official subquestion output and its selected producer route, as structured output mappings;
- unresolved limitations or `none supported by current evidence`;
- why another model, parameter, branch, or solver has no justified marginal value;
- the highest permitted conclusion level;
- the artifact that stores the executable specification and the validation handoff.

The certificate is invalid if it relies on “enough models,” “looks advanced,” “results seem reasonable,” or a generic `done/pass/N/A`. A machine validator can enforce presence, statuses, and coverage, but it cannot judge whether the mathematics or evidence is substantively correct. Blind new-case evaluation and expert review remain separate evidence.

## Promotion and state boundary

For a substantive contest run, `route_executable` promotion additionally requires:

- `competition_readiness.status = ready`;
- at least two complete audit passes;
- all nine readiness dimensions passed with problem-specific evidence;
- all eight cross-case checks passed or justified not applicable;
- a complete stop certificate;
- no blocked iteration, failed stress test, open critical ambiguity, or newly triggered unread structural gate.

After this gate, apply [excellence-assurance.md](excellence-assurance.md), then obtain final human approval of the exact frozen route before `route_executable` promotion. This skill remains strategy-only: it has no numerical-solving states and does not execute the proposed model.
