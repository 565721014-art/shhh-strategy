# Output Modes and Checkpoints

Select the smallest mode that satisfies the user. Do not inflate a strategy request into a full paper.

The analysis ledger may be structured for consistency, but user-facing prose remains problem-shaped and need not expose every ledger field. Report only the evidence and decision needed at the current checkpoint.

## Mode A: strategy only

Use when the user asks for thinking, reading analysis, or a plan but not numerical solving.

Return:

1. what the problem truly asks and the easiest serious misreading;
2. each subquestion's deliverable, information time, and dependency;
3. a credible baseline;
4. necessary route(s), their roles, and the exact trigger for each;
5. variables, relationships, constraints, algorithm exit, and expected output;
6. fatal counterexample and validation gate;
7. current state: normally `route_executable`, not solved.

Use the Mandatory Confirmation Contract from `SKILL.md`: pause at every material interpretation, assumption, route, complexity, or claim-boundary decision that requires user judgment. Do not wait until the end of the mode to surface it.

## Mode B: executable route

Use when the user wants a complete modeling specification ready for code.

Add:

- full symbol and unit table;
- equations/recurrences and boundary conditions;
- solver or algorithm sequence with termination and tolerances to determine;
- input-to-output schema;
- validation and robustness tests;
- explicit unresolved parameters that code must not invent.

## Mode C: explicit retrospective historical comparison

This mode is off by default. Use it only when the user explicitly asks to train on, learn from, or compare against prior papers, expert reviews, or official commentary for a past problem. The problem being old, named, searchable, or previously used for practice does not activate this mode. Never suggest it as the automatic next step after Mode A, B, or D.

After an independent freeze, separately score:

- problem understanding: objects, information, constraints, dependencies, outputs, and ambiguities;
- solution route: mathematical closure, feasibility, efficiency, validation, robustness, and clarity.

Classify each difference as independent omission, paper omission, genuine ambiguity, or optional method choice. A prestigious paper is evidence, not ground truth.

## Mode D: full solve requested

The strategy skill may prepare the complete route and continue solving only when the user explicitly requests it and the available tools/data make it possible. Do not claim completion until results are reproduced and validated. Full paper drafting, formatting, and submission compliance remain outside this skill's default scope.

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

After approval, do not repeatedly ask about the same locked point. Every response still ends with the required compact status block from `SKILL.md`.
