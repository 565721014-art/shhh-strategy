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
6. claim boundary;
7. confirmation discipline;
8. state continuity.

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

## Promotion rule

Freeze the case pack, scoring rubric, targeted dimensions, and evaluator before comparing versions. Promote only when:

- both versions are scored on the same untouched cases and information;
- the candidate has no critical failure;
- no case regresses on source integrity, problem lock, trigger fidelity, or claim boundary;
- total score does not decrease;
- the targeted stability dimensions improve on at least two structurally different mechanism families;
- all deterministic script, schema, hash, and package validations pass.

If the evaluator has seen the candidate design or the case has been used to modify the candidate, label it development regression, not blind evidence. Keep at least one future case pack sealed outside the public skill.

Use `scripts/evaluate_regression.py` to validate observation files and apply the mechanical part of the promotion rule.
