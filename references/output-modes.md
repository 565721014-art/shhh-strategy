# Output Modes and Checkpoints

Select the smallest mode that satisfies the user, but do not treat a conceptual outline as a finished strategy. For a substantive new-problem request with no narrower stopping instruction, Mode B is the default. This skill ends at an approved executable strategy and never performs numerical solving or a full paper.

The analysis ledger may be structured for consistency, but user-facing prose remains problem-shaped and need not expose every ledger field. Report only the evidence and decision needed at the current checkpoint.

## Mode A: explicitly limited audit or brief strategy

Use only when the user explicitly asks for a quick reading, candidate ideas, risk audit, or an early checkpoint rather than a complete code-ready strategy.

Return:

1. what the problem truly asks and the easiest serious misreading;
2. each subquestion's deliverable, information time, and dependency;
3. a credible baseline;
4. necessary route(s), their roles, and the exact trigger for each;
5. variables, relationships, constraints, algorithm exit, and expected output;
6. fatal counterexample and validation gate;
7. current state: normally `audit_complete`, not `route_executable` and not solved.

Use the Mandatory Confirmation Contract from `SKILL.md`: pause at every material interpretation, assumption, route, complexity, or claim-boundary decision that requires user judgment. Do not wait until the end of the mode to surface it.

## Mode B: executable route — default for a new problem

Use when the user wants a complete modeling specification ready for code.

Add:

- full symbol, domain, index, unit and information-time table;
- assumptions with evidence status and critical labels;
- equations/recurrences, objective, constraints and boundary/initial conditions;
- data-quality, missingness, duplicate, outlier, lineage, leakage and split-unit handling when data exist;
- ordered solver or algorithm sequence with initialization, interfaces, termination and tolerances to determine;
- counterexample, boundary, identifiability, feasibility, robustness and simpler-route tests, with repairs recorded;
- abnormal-input, infeasibility, non-convergence and unsupported-extrapolation handling as applicable;
- input-to-output file schema, units, precision and consistency checks;
- validation baseline, evaluator, metric, pass criterion and downgrade rule;
- explicit unresolved parameters that code must not invent;
- a stop certificate showing why no triggered defect or justified upgrade remains.

The first complete-looking route is not the exit. Run the autonomous route-deepening loop, post-route reread, competition-readiness pass, and supra-reference excellence audit; store the concise iteration record, stop certificate, verified deltas and ablations, then present the frozen detailed artifact for final human review. Only explicit approval permits the ledger transition to `route_executable`; immediately report completion after the transition.

## Mode C: explicit retrospective historical comparison

This mode is off by default. Use it only when the user explicitly asks to train on, learn from, or compare against prior papers, expert reviews, or official commentary for a past problem. The problem being old, named, searchable, or previously used for practice does not activate this mode. Never suggest it as the automatic next step after Mode A, B, or D.

After an independent freeze, separately score:

- problem understanding: objects, information, constraints, dependencies, outputs, and ambiguities;
- solution route: mathematical closure, feasibility, efficiency, validation, robustness, and clarity.

Classify each difference as independent omission, paper omission, genuine ambiguity, or optional method choice. A prestigious paper is evidence, not ground truth.

## Mode D: out-of-scope computation request

This strategy skill still prepares only the complete route. A request to run code, solve numerically, fit models, generate computed result tables, or validate observed outputs belongs to a separate workflow and must not add execution states to this skill. Do not ask the user whether to start that work when Mode B completes. Full paper drafting, formatting, and submission compliance are also outside this skill.

## Internal claim labels

- `D` descriptive: observed sample, period, and denominator only.
- `P` predictive: unseen/future performance under stated population, time, information, and support, with leakage-safe validation.
- `C` causal: defined intervention and comparator with an identification argument and sensitivity boundary.

If causal identification is absent, downgrade to D/P or a labeled model scenario. Prediction-driven optimization without an identified or mechanistic action response is a scenario recommendation, not a real-world causal promise.

## Writing style

Do not force a fixed paper template. Let the structure match the problem:

- mechanism problems: state evolution and boundary conditions;
- data problems: evidence and decision chain;
- optimization: feasible set, objective, algorithm, and certificate;
- construction: lower bound, construction, and proof;
- mixed problems: dependency graph and error propagation.

Keep the main line visible. Retain multiple necessary routes but explain whether they are sequential, branching, corroborative, or integrated.

## Confirmation-shaped delivery

For long tasks, deliver the smallest complete unit that exposes the next consequential decision. A useful checkpoint contains:

1. what has been established from evidence;
2. what remains genuinely undecided;
3. the live options and their downstream consequences;
4. the recommended option and reason;
5. the exact approval or correction requested.

After approval, do not repeatedly ask about the same locked point. Before `route_executable`, obtain one final review of the exact complete route artifact even if earlier forks were approved. After that approval, report completion directly instead of asking what to do next. Every response still ends with the required compact status block from `SKILL.md`.
