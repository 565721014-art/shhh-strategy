# Supra-Reference Excellence Assurance

Read this after competition readiness for every substantive contest-problem run. Its purpose is to make the route exceed the **generalized process and evidence standard** learned from high-level national-prize work, not to promise a prize or claim superiority over every unseen paper.

This protocol does not authorize same-problem retrieval. Unless the user explicitly requests retrospective comparison, the benchmark basis is `generalized_historical_process`: cross-problem responsibilities distilled from the existing development archive, held-out replays, and 34-case anti-overpruning audit. A same-problem or blind-expert superiority claim needs separate evidence and a different claim scope.

## Strong reference bar

Use a strong, not deliberately weak, reference bar. A route merely matching these items is not yet above the generalized bar:

- correct task and information-set interpretation;
- coherent variables, assumptions, equations, objective, constraints, and feasible algorithm;
- an evidence-supported baseline and necessary upgrades;
- basic sensitivity or robustness analysis;
- outputs that answer every subquestion;
- a readable modeling narrative.

The route must first meet this bar without regression. It then needs verifiable excellence deltas that improve correctness, falsifiability, decision value, robustness, efficiency, reproducibility, or insight.

## Seven excellence dimensions

Record a problem-specific reference bar, route evidence, delta, method, and status for every dimension:

1. **interpretation_precision**: alternative readings, scope, clocks, information permissions, object lifecycle, exceptional states, and deliverable semantics are resolved more precisely than a conventional problem restatement.
2. **mechanism_fidelity**: the selected state, geometry, stochastic, causal, event, network, or decision mechanism preserves the actual process and uses a true/high-fidelity evaluator where proxies could mislead.
3. **mathematical_rigor**: well-posedness, degrees of freedom, identifiability, existence/attainability, bounds, construction, optimality gap, or impossibility duties are explicit rather than implied by solver output.
4. **computational_reliability**: algorithms have reproducible interfaces, convergence/failure handling, fair baselines, small exact cases or independent recalculation, and common evaluation precision.
5. **validation_and_falsification**: validation can overturn the route; it includes fatal counterexamples, boundary/invariance tests, leakage or data-lineage controls, and independent or out-of-sample evidence appropriate to the task.
6. **uncertainty_and_decision_value**: upstream uncertainty and model error propagate to decisions, feasibility, risk, and claim strength; the improvement matters to an official output or decision rather than only a training score.
7. **reproducibility_and_communication**: a third party can reproduce the route, outputs, checks, and paper evidence from the stored specification without inventing missing choices; the main line remains compressed and auditable.

Statuses are `meets_reference`, `exceeds_reference`, `below_reference`, or `not_comparable`. An ordinary route cannot pass with `below_reference` or `not_comparable`. At least two dimensions must be `exceeds_reference` with verified advances; one must be `mathematical_rigor` or `validation_and_falsification` so that superiority is not cosmetic.

## Verified excellence advances

Record at least two distinct advances. Each advance must contain:

- the current-problem trigger and the strong-reference limitation it addresses;
- the affected excellence dimension and category;
- the smallest improvement added to the route;
- a removal/ablation counterfactual: what becomes wrong, weaker, unverifiable, or less useful if the improvement is removed;
- an independent verification method and problem-specific evidence;
- the cost or complexity introduced and why it is justified.

Allowed categories are `correctness`, `validation`, `decision_value`, `robustness`, `efficiency`, `reproducibility`, and `interpretability`. At least one verified advance must be in `correctness` or `validation`; the advances must cover at least two categories. Model novelty without a measurable responsibility is not an advance.

Examples of legitimate deltas include a lower bound plus attainable construction, high-fidelity replay that changes the chosen candidate, explicit nonanticipativity that removes clairvoyance, group/time-aware validation that eliminates leakage, uncertainty propagation that changes a decision, or a closed-form reduction that improves reliability and contest-time efficiency. These are examples, not mandatory models.

## Non-regression and stopping

An excellence improvement may not weaken source fidelity, hard-constraint feasibility, information legality, identifiability, validation independence, claim honesty, or reproducibility. If a proposed improvement does so, reject it even when a score improves.

Stop when:

- all seven dimensions meet or exceed the strong reference bar;
- at least two distinct advances are verified, including a correctness/validation advance;
- removing each advance demonstrably weakens a required responsibility;
- no further triggered improvement has positive marginal value under the contest resource budget;
- competition readiness and the ordinary stop certificate still pass after regression.

If evidence cannot support a genuine delta, set `excellence_assurance.status = blocked` and report the exact missing evidence. Do not manufacture innovation or add a model zoo to satisfy the count.

## Claim boundary

Use one of three claim scopes:

- `generalized_process_standard`: the route meets/exceeds the generalized process-and-evidence bar learned from the archive. This is the default and does not prove award superiority.
- `same_problem_comparative`: allowed only after explicit opt-in comparison using the same problem, inputs, outputs, and evaluation rules.
- `blind_external_validated`: allowed only after a sealed unseen-case evaluation by an independent evaluator with stored evidence.

`award_guarantee` must remain false. The skill may target a standard higher than weaknesses observed in high-level papers; it may never convert that target into a guaranteed result.
