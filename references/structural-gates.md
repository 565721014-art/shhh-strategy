# Structural Trigger Gates

These gates preserve the fine-grained V26/V27 reasoning library. Read all headings, but activate a gate in the actual analysis only when the current statement, attachment, mathematics, or independently reproduced evidence triggers it.

## 1. Deliverable verb and quantifier

Translate establish, analyze, predict, identify, evaluate, optimize, control, influence, reasonable, at least, minimum, any, first, real-time, and adjust into an observable output and a proof/validation responsibility.

- “minimum” requires checking 0/1 and closing a lower bound with a construction;
- “any/all times” is a universal or trajectory condition, not sampled examples;
- “first” requires continuous or discrete event ordering;
- “real-time/online” requires decision-time information and runtime feasibility;
- “influence/effect” may require causal evidence rather than association;
- “reasonable/optimal” requires the criterion and tie-breaker to be authorized.

## 2. Given-quantity fate

Every nontrivial stated quantity must map to a state, parameter, constraint, boundary, validation, or output. If a quantity is intentionally ignored, explain why it cannot change the model family and validate the reduction. Geometry size, sampling rate, identity, batch, thickness, duration, and output precision often decide the structure.

## 3. Units, indexes, identities, and domains

Record symbol role, unit, index set, legal domain, and source. Check:

- object ID versus row order;
- physical coordinate versus array index;
- angle zero line, positive direction, quadrant, and handedness;
- percentages/compositions with closure;
- rates versus totals and irregular-time integration;
- transformed variables and inverse transforms;
- missing, not exposed, below detection, structural zero, and true zero.

An apparently accurate result with wrong identity, direction, denominator, or unit is invalid.

## 4. Multiple clocks and information capability

Separate process start, recording start, observation availability, decision time, action time, event time, and accounting cutoff. The first recorded row is not automatically initialization. Build an information ladder:

- prior fixed information;
- information observed before each decision;
- information revealed after the action;
- future outcomes unavailable to the real policy.

Replay a candidate with future fields masked at every decision. Distinguish static, rolling, adaptive, and clairvoyant policies.

## 5. Object lifecycle, phases, and terminal accounting

Replay initialization → transition → stable operation → terminal state, plus normal → abnormal → recovery. Check unfinished work, carryover inventory, already-triggered events, left/right censoring, and whether output after the official deadline is incorrectly counted.

For multi-stage objects, do not optimize each stage independently when an upstream choice changes downstream feasibility or error.

## 6. Objective well-posedness, minimality, and invariants

Before optimizing:

- count true degrees of freedom after constraints and eliminations;
- test whether the objective is constant or unbounded on the feasible set;
- test symmetry, mirror, permutation, scale, or label invariance;
- identify whether multiple solutions are equivalent;
- separate hard constraints from preferences;
- use authorized lexicographic/epsilon/Pareto treatment when weights are absent.

Do not invent a unique optimum or secondary objective. If the original objective is degenerate, prove it and label any relaxed extension as a changed problem.

## 7. Identifiability and inverse-problem factorization

Separate instrument/geometry, gain/noise, and target state. Determine whether observations identify the requested parameter, a product/ratio/integral, or only an equivalence class. Use known templates or analytic features for initialization before joint refinement when possible.

Low residual is insufficient. Require forward replay, perturbation sensitivity, parameter correlation/rank, holdout geometry/conditions, and an independent reconstruction or formula. When not identifiable, report a set, interval, conditional result, or required extra experiment.

## 8. Continuous dynamics, hybrid modes, and contact

When arrival, collision, threshold crossing, valve opening, failure, release, detonation, saturation, or contact changes equations, list each mode, entry condition, state update, exit condition, and invariant. Do not average mode changes into one smooth curve without an error bound.

For contact, check non-penetration, nonnegative contact force, and complementarity when relevant. For collisions and occlusion, use the full physical object, not only centers or sampled points, unless the reduction is proven safe.

## 9. Trajectory and event constraints

Endpoint feasibility does not imply path feasibility. Check first/last crossing, duration above/below threshold, continuous collision-free motion, coverage gaps, queue overflow, and constraint violation between samples. Use coarse grids only to bracket; refine event times and demonstrate step/tolerance convergence.

For segmented paths or regions, audit connections, seams, and cross-region interactions after recombination.

## 10. Experimental unit, repeated measurement, and feature lineage

Identify the independent experimental unit before splitting. Technical repeats estimate measurement error; they do not increase treatment replication or degrees of freedom. Keep subjects, specimens, batches, augmented copies, adjacent frames, repeated spectra, and longitudinal observations grouped as required by deployment.

Fit scaling, smoothing, imputation, feature selection, dimensionality reduction, label propagation, and hyperparameters inside the training fold. Trace derived features: RGB/HSV, ratios/totals, cumulative/daily, labels/scores, and multiple modalities may share the same evidence source.

Separate accuracy, precision, resolution, calibration, discrimination, and extrapolation range.

## 11. Exposure, denominator, censoring, and action-generated records

Before comparing totals or rates, lock object, opportunity, observation window, active time, stock availability, assignment, censoring, and denominator. Zero sales may mean no demand, stockout, or no listing; zero loss may mean no shipment.

Historical price, credit, assignment, display, inspection, or control actions are generated by an old policy. Their observed outcomes describe that policy's support. A predictive association is not automatically an intervention response, and optimization outside historical action support requires a structural model, designed experiment, or clearly labeled scenario.

## 12. Description, prediction, mechanism, and causality

- Description summarizes the observed population/time/denominator.
- Prediction requires leakage-safe performance on the intended unseen unit and support.
- Mechanism requires a defensible state or scientific relation but may still contain assumptions.
- Causality requires a defined intervention and comparator plus identification, overlap, spillover, and sensitivity checks.

Do not use predictive accuracy as causal proof. A policy recommendation based on an assumed response is a scenario recommendation until that response is identified or mechanistically validated.

## 13. Policy feedback and structural intervention

If a policy changes participation, demand, route, queue, price, credit, inspection, or future data, evaluate at least one loop:

`policy → behavior/arrival response → new state → constraints/outcome → reevaluation`.

For network or structural interventions, decompose direct capacity/structure gain, added friction/side effects, and behavior/flow redistribution. Compare under the same demand/object/window first; induced demand is a separate scenario.

## 14. Prediction-to-decision and action controllability

Prediction is useful only if its uncertainty enters the downstream decision and the final metric is evaluated. Separate immutable attributes, long-term state, short-term action, mediator, proxy, and artifact. A high-importance feature is not automatically controllable.

Actions must enter a forward state transition or response relation, remain in the joint feasible/safe support, and be replayed against a common baseline. If action response is unidentifiable, stop strategy superiority claims and provide scenarios, bounds, or data requirements.

## 15. Global objective preservation

Independent optimization of parts does not automatically preserve a union, intersection, maximum, minimum, fairness, or coupled-resource objective. Re-evaluate combined candidates with the original global objective and constraints.

Distinguish quantifier order, such as “for every target point there exists a resource” versus “there exists one resource covering every point.” Check code loop order against the mathematical statement.

## 16. Feasibility, candidate dominance, and common evaluator

Separate ideal design, constraint-realizable state, and true performance. Compute performance from the realizable state. If a validator or alternate solver finds a better feasible candidate under the same constraints, update the incumbent and weaken any unsupported optimality claim.

Use exact small cases, lower bounds, dual bounds, exhaustive enumeration, independent solver, or high-fidelity replay according to the problem. Report candidate, best known, proven optimal, relaxed, and infeasible states accurately.

## 17. Uncertainty and robustness

Vary only quantities whose uncertainty is supported. Name range/source, common baseline, stability metric, pass criterion, and downgrade rule. Distinguish aleatory scenario, parameter uncertainty, measurement error, structural ambiguity, and missing information.

Do not fabricate a probability distribution from a mean. Preserve tail mass, correlations, support, and nonanticipativity. If ambiguity cannot be resolved, report branches or bounds rather than average incompatible models.

## 18. Output and evidence closure

Every major conclusion must map to a required subquestion, formula/model, computed or proven evidence, validation, unit, denominator, scenario, and boundary sentence. Required files and tables must be generated from the same state and decision variables, not manually assembled.

Keep code/formula/table/abstract numbers consistent. A polished statement without a reproducible evidence chain remains unsupported.
