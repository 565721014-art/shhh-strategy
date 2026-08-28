# Complexity, Evidence, and Stopping Gates

## Principle

Remove only inappropriate complexity. Preserve every component that is forced by the statement, produces a distinct deliverable, resolves a real structural ambiguity, provides independent corroboration, or yields validated marginal value.

Rules are dormant until evidence triggers them. A large audit library is not an instruction to build a large model.

## Separate four kinds of complexity

1. **Mechanism/representation**: state dimensions, geometry, network topology, modes, object heterogeneity. Preserve when forced by the problem.
2. **Statistical/parameter**: learned parameters, feature selection, model capacity, hyperparameters, arbitrary weights. Limit by effective independent information.
3. **Solver**: exact algorithms, global search, local refinement, heuristics, independent recomputation. Judge by optimization structure and verification duty, not sample size alone.
4. **Presentation**: equations, branches, figures, tables, and model count in the paper. Compress presentation without deleting necessary mathematics.

Never use a small sample to justify deleting a hard physical state. Never use a sophisticated solver to justify unsupported fitted parameters.

## Trigger record for every added component

Record:

| Field | Requirement |
|---|---|
| deliverable | exact subquestion and output served |
| source evidence | statement sentence, figure relation, attachment field, mathematical incompatibility, or independently reproduced data pattern |
| baseline defect or distinct role | what becomes wrong, infeasible, unidentifiable, unverifiable, or incomplete without it |
| minimum addition | smallest structure that repairs the defect |
| rejection condition | evidence under which the component is removed or downgraded |

“A past paper used it,” “it is advanced,” “it may exist,” or “it could improve the paper” is not a trigger.

## Six admission gates

An added route may support a final conclusion only when all relevant gates pass.

### 1. Evidence trigger

The problem, attachment, mathematics, or independent validation identifies the need.

### 2. Necessity or distinct responsibility

The route repairs a material baseline defect or carries a different responsibility such as lower bound, candidate construction, structural branch, error bound, or independent recomputation. Similar outputs do not make routes redundant when proof responsibilities differ.

### 3. Capacity and identifiability

Count effective independent objects, batches, periods, or experiments rather than rows. Audit noise, missingness, class/event support, extrapolation, parameter identifiability, and resampling stability.

This gate limits learned or calibrated freedom. Geometry, conservation, dynamics, logic, and output-mandated states are not removed for lack of samples; validate them through derivation, boundary cases, convergence, and independent computation. If a mechanism model contains weakly identified parameters, shrink or bound those parameters without deleting the forced mechanism.

### 4. Fair comparison

Baseline and candidate must share decision-time information, split, target output, constraints, denominator, and evaluator. Learned preprocessing stays inside training folds. A candidate using extra future fields, looser constraints, or a different denominator is a different information scenario, not a superior algorithm.

Use a minimum credible baseline and, where relevant, a strong simple/domain-standard baseline. A deliberately weak or infeasible baseline invalidates the comparison.

### 5. Independent benefit

Freeze the primary criterion and meaningful difference before comparison. Show benefit on evidence not used for model selection.

Use task-appropriate certificates:

- data: leakage-safe out-of-sample performance, calibration, uncertainty, practical difference;
- physics/simulation: conservation, boundaries, back-test, convergence, identifiability;
- optimization: feasibility, common-evaluator objective, lower bound/gap, exact small case, multistart stability;
- construction: lower bound, feasible construction, proof, extreme cases;
- causal/policy: identification, common comparator, overlap, spillover, sensitivity.

### 6. Deliverable and communication value

The component must change a required output, feasibility decision, main recommendation, uncertainty bound, robustness conclusion, or essential explanation. A tiny secondary-score change with no decision effect defaults to the simpler route.

Multiple routes may pass when they serve different subquestions or responsibilities. There is no numeric model cap.

## Hard stopping conditions

Stop adding candidates when any of the following applies:

1. the simplest surviving route produces every required output, satisfies hard constraints, passes its validation, and has no evidenced remaining defect;
2. the next route lacks a source trigger or only renames an algorithm;
3. independent improvement is below the predeclared practical threshold, unstable, or decision-irrelevant;
4. effective information or identifiability cannot support added learned freedom;
5. final evaluation data has been used for selection or tuning—retire it from final-test status and stop best-model claims;
6. the route duplicates an existing function and adds no corroboration, robustness, proof, or boundary value;
7. remaining uncertainty comes from missing or non-identifying information that a different model cannot create;
8. additional presentation hides the route, evidence, or conclusion without adding mathematical value.

Stopping is based on marginal value, never model count.

## Anti-peeking protocol

- Register candidate roles, primary metric, split, and upgrade criterion before final comparison.
- Treat preprocessing, feature selection, model selection, and hyperparameter tuning as training.
- Use nested, temporal, spatial, grouped, or subject-blocked validation according to deployment.
- Evaluate the untouched final set once. Once viewed for selection, it is no longer final.
- Report how many candidates were tried and why they were rejected.
- With limited data, use nested resampling and uncertainty; do not claim universal best.
- When performance is practically tied, choose the simpler stable route unless another route carries a distinct proof duty.

## Baseline fairness checklist

- same question and output;
- same information available at decision time;
- same population, time window, and denominator;
- same hard constraints and feasibility definition;
- same high-fidelity evaluator;
- comparable preprocessing and tuning opportunity;
- transparent difference in compute, data, or assumptions.

## Stop certificate

At the end record:

- simplest retained route and all necessary companion routes;
- delivered outputs and validation passed;
- why no further candidate is justified;
- unresolved uncertainty that models cannot eliminate;
- permitted claim level: descriptive, predictive, causal, scenario, candidate, or proven.
