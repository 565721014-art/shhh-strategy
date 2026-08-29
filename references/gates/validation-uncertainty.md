# Validation, Uncertainty, and Evidence Closure Gates

## 16. Feasibility, candidate dominance, and common evaluator

Separate ideal design, constraint-realizable state, and true performance. Compute performance from the realizable state. If a validator or alternate solver finds a better feasible candidate under the same constraints, update the incumbent and weaken any unsupported optimality claim.

Use exact small cases, lower bounds, dual bounds, exhaustive enumeration, independent solver, or high-fidelity replay according to the problem. Report candidate, best known, proven optimal, relaxed, and infeasible states accurately.

## 17. Uncertainty and robustness

Vary only quantities whose uncertainty is supported. Name range/source, common baseline, stability metric, pass criterion, and downgrade rule. Distinguish aleatory scenario, parameter uncertainty, measurement error, structural ambiguity, and missing information.

Do not fabricate a probability distribution from a mean. Preserve tail mass, correlations, support, and nonanticipativity. If ambiguity cannot be resolved, report branches or bounds rather than average incompatible models.

## 18. Output and evidence closure

Every major conclusion must map to a required subquestion, formula/model, computed or proven evidence, validation, unit, denominator, scenario, and boundary sentence. Required files and tables must be generated from the same state and decision variables, not manually assembled.

Keep code/formula/table/abstract numbers consistent. A polished statement without a reproducible evidence chain remains unsupported.
