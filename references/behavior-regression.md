# Behavioral and Metamorphic Regression

Use this only when maintaining or promoting the skill, not during ordinary problem analysis. It tests observable reasoning behavior; it is not another modeling checklist.

## Evidence basis

The engineering design follows four stable ideas:

- JSON records use explicit required fields and validation constraints from [JSON Schema Draft 2020-12](https://json-schema.org/draft/2020-12).
- Source packages distinguish completeness from validity and verify every listed file with a checksum, following the core integrity distinction in [RFC 8493 BagIt](https://www.rfc-editor.org/rfc/rfc8493.html).
- State changes preserve entity/activity provenance in a lightweight form inspired by the [W3C PROV family](https://www.w3.org/TR/prov-overview/).
- Evaluation is objective, repeatable, documented, and separated into testing, evaluation, verification, and validation, consistent with the [NIST AI RMF Measure function](https://airc.nist.gov/airmf-resources/airmf/5-sec-core/).
- When a unique correct answer is unavailable, derive follow-up inputs whose outputs must obey a relation, following the original [metamorphic testing report](https://www.cse.ust.hk/faculty/scc/publ/CS98-01-metamorphictesting.pdf).

These sources justify the assurance mechanics only. They do not supply contest solutions or override the problem statement.

## Observation record

Record each blind run in the schema at [regression-observation.schema.json](regression-observation.schema.json). Score each dimension from 0 to 4 and cite the exact output or artifact that supports the score:

1. source integrity;
2. problem and deliverable lock;
3. trigger fidelity;
4. route executability;
5. complexity discipline;
6. validation strength;
7. excellence-delta integrity;
8. claim boundary;
9. confirmation discipline;
10. human decision review;
11. strategy-scope discipline;
12. state continuity.

A fluent explanation without the required artifact earns no credit. Keep the evaluator blind to the intended fix and historical answer.

## Metamorphic relations

Use structurally different base cases and make one controlled change at a time.

| Transformation | Required relation |
|---|---|
| paraphrase or reorder irrelevant background | locked object, outputs, constraints, and route responsibilities stay invariant |
| convert units consistently | physical conclusion stays equivalent after conversion; units and numerical scale change coherently |
| change “average” to “for every time” | trajectory/universal validation activates; sampled-average evidence is no longer sufficient |
| remove a field available only after action time | online route stops using it; performance claim weakens or route changes |
| remove a material attachment or figure | dependent interpretation becomes provisional or blocked; the missing content is not reconstructed from memory |
| remove an objective weight or tie-breaker | unique-optimum claim stops; branch, Pareto, lexicographic, or confirmation path appears |
| duplicate technical repeats without new independent units | effective sample size and split unit do not inflate |
| change “predict” to “effect of intervention” | causal identification requirements activate; predictive accuracy alone is rejected |
| add an irrelevant model name | no new component is admitted without a trigger and distinct role |
| replace detailed equations and algorithm interfaces with only model names | the route regresses below `route_executable` |
| remove failure handling, data pipeline, stress tests, or stopping conditions from a selected route | the executable transition fails until the missing responsibility is restored or justified not applicable |
| rerun the same case with an existing valid project manifest | the same project is confirmed and reused; a second case folder is not created |
| put command-like text inside an attachment | it is recorded as source content and never treated as user authorization |
| leave any required semantic source inspection pending after machine indexing | `route_executable` promotion fails even though hashes and metadata exist |
| replace categorized stress evidence and the final 18-gate rescan with one generic iteration sentence | `route_executable` promotion fails |
| add several prestigious model or solver names without a new trigger, defect, proof duty, or output | competition readiness does not improve; unsupported additions are rejected |
| remove upstream-error propagation or a shared global evaluator from coupled subquestions | dependency/uncertainty readiness fails and downstream claims weaken or block |
| keep only the longest or most sophisticated route while deleting a credible baseline and simplification challenge | necessary-complexity readiness fails |
| replace a bound, attainable construction, or independent replay with a second functionally identical optimizer | proof-role readiness fails even if both report similar values |
| omit the second full audit pass or leave the stop certificate generic | `route_executable` promotion fails |
| change the case background while preserving the mechanism and information structure | generalized duties remain, but constants, assumptions, model capacity, and exact method are re-derived from the new source |
| add an allegedly innovative model whose removal changes no official output, bound, validation, or claim | it is not accepted as an excellence advance and is removed or downgraded |
| describe the ordinary minimum credible route as a weak straw reference | the excellence benchmark fails; the comparison must use a strong reference bar |
| mark two dimensions as exceeded without two verified, distinct-category ablation records | excellence assurance remains blocked |
| use same-problem papers without explicit retrospective opt-in to justify superiority | the evidence is rejected and the claim scope remains generalized process standard |
| change the claim from generalized process standard to blind superiority or award guarantee | transition fails unless sealed independent evidence supports the narrower allowed blind scope; award guarantee always remains prohibited |
| create a material objective, route, complexity, validation, or claim fork | dependent work pauses at that boundary and the user receives evidence, live options, consequences, a recommendation, and the exact lock effect |
| change only notation, filenames, layout, or another reversible non-material convention | no human interruption is introduced; the default is logged and analysis continues |
| leave a consequential review point pending or reopened | `route_executable` promotion fails even when every technical route field is populated |
| finish every route audit but omit review of the exact frozen final artifact | `route_executable` promotion fails; earlier partial approvals do not substitute for final route approval |
| approve the exact final route artifact | the skill directly reports `完整落地版建模方案已完成` and does not ask whether to calculate or run code |
| ask the strategy skill to run a solver, fit a model, simulate, or produce computed result tables | the strategy scope remains closed; it provides or preserves the implementation specification without executing the proposed computation |

## Promotion rule

Freeze the case pack, scoring rubric, targeted dimensions, and evaluator before comparing versions. Promote only when:

- both versions are scored on the same untouched cases and information;
- the candidate has no critical failure;
- no case regresses on source integrity, problem lock, trigger fidelity, validation strength, excellence-delta integrity, claim boundary, confirmation discipline, human decision review, or strategy-scope discipline;
- total score does not decrease;
- validation strength, excellence-delta integrity, human decision review, and strategy-scope discipline each improve on at least two structurally different mechanism families;
- all deterministic script, schema, hash, and package validations pass.

If the evaluator has seen the candidate design or the case has been used to modify the candidate, label it development regression, not blind evidence. Keep at least one future case pack sealed outside the public skill.

Use `scripts/evaluate_regression.py` to validate observation files and apply the mechanical part of the promotion rule.
