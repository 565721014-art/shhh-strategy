# Task Semantics and Problem Lock Gates

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
