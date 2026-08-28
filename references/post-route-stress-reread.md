# Post-Route Stress Test and Source Reread

Use this pass after the first executable strategy exists. Its purpose is to falsify and repair the route before numerical solving, not to add sophistication for appearance. Completing this pass does not trigger or justify a same-problem historical comparison; that is a separate explicit retrospective-training request.

## 1. Preserve the pre-test route

Record the current quality state, locked interpretations, selected route, rejected alternatives, and source hashes when local files are available. The stress test may correct the route, but it must not erase what changed or why.

## 2. Reread the source of truth

Reread every in-scope statement page and re-inspect every relevant attachment, figure, table, formula, note, unit, time label, coordinate convention, and output verb. For visual or spreadsheet evidence, inspect the rendered page or sheet as well as extracted values. Rebuild the deliverable ledger from the source without relying on the earlier summary.

Check specifically whether the route silently introduced any of the following without support:

- coordinate direction, handedness, origin, orthogonality, scale, or translation;
- time zone, calendar convention, sampling clock, synchronization, or date meaning;
- measurement error, probability distribution, independence, weights, tolerance, or confidence level;
- shared identity or parameters across attachments, repeated rows, objects, or experiments;
- geographic, physical, policy, or feasible-region restrictions;
- uniqueness, causal wording, optimality, or accuracy beyond what the output requests.

Displayed decimal places are data formatting unless the source explicitly identifies them as measurement resolution or rounding. Do not turn the last shown digit into a noise bound or statistical model without evidence.

## 3. Attack the route rather than its wording

For each active modeling component, attempt at least one failure test that could change the result:

1. an alternative source-compatible interpretation;
2. a boundary or degenerate case;
3. a symmetry, invariance, mirror, scale, or parameter-compensation transformation;
4. a counterexample where the fitted objective is small but the requested quantity is wrong or non-identifiable;
5. a replay with information, constraints, or attachments isolated exactly as the statement requires;
6. a simpler route that produces the same deliverable, or a missing component forced by the source.

Do not activate every possible test mechanically. Select tests whose triggers are present in the current source or mathematics.

## 4. Classify each finding

Place every finding into one category:

- **confirmed**: the route survives and needs no change;
- **correction**: source evidence or mathematics disproves part of the route;
- **material ambiguity**: multiple source-compatible branches remain and user confirmation is required before dependent work;
- **optional refinement**: it may improve convenience or precision but is not yet justified for the main route.

Reopen a previously locked decision only when the new evidence conflicts with it. Show the conflict, consequences, and recommended replacement under the Mandatory Confirmation Contract.

## 5. Revise minimally and regress

For every correction or admitted component, record its trigger, repaired defect, minimum change, and removal condition. Then rerun the subquestion locks and verify that:

- every required output still has a mathematical producer;
- no source-given quantity or attachment has been dropped;
- necessary complexity was not pruned merely to simplify presentation;
- the baseline and final candidate still use the same legal information and evaluator;
- validation does not masquerade as estimation or proof;
- unresolved non-identifiability is reported as candidates, ranges, branches, or additional-data requirements.

If a stress-test finding cannot affect a required output, feasibility, identifiability, validation conclusion, or claim boundary, keep it out of the main route.

## 6. Exit state

End with a short change ledger: what survived, what was corrected, what remains unresolved, and why no further change is currently justified. The route returns to `route_executable` only after the regression checks pass. Numerical results are still absent unless the user separately requested solving.
