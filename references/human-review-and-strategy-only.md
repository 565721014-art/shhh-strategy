# Human Review and Strategy-Only Boundary

Read this for every substantive problem run. It makes human judgment observable without turning every reversible choice into an interruption, and it fixes `route_executable` as the terminal state of this skill.

## Strategy-only scope

This skill produces a directly implementable mathematical-modeling specification. It may write variable definitions, equations, constraints, pseudocode, solver or estimator interfaces, initialization, tolerances to determine, validation experiments, exception branches, file schemas, and an implementation handoff. It must not:

- execute modeling programs, notebooks, optimizers, simulations, model fitting, or numerical solvers;
- calculate the problem's requested numerical or constructive results;
- generate result tables or figures that imply the proposed model was run;
- promote a planned validation into observed validation evidence;
- ask at completion whether the user wants calculation, code execution, or numerical solving.

Read-only source inspection, deterministic skill-maintenance checks, project initialization, inventory, ledger validation, and file hashing are operational support, not problem solving. They remain allowed. If the user separately asks for computation, treat that as a different workflow outside this skill; do not expand this skill's state machine.

## Consequential decision test

A decision requires user review before dependent reasoning when changing it can materially alter at least one of:

- modeled object, population, time axis, information set, or identity unit;
- hard feasible region, objective, preference ordering, risk attitude, or tie-breaker;
- interpretation of an official output or its permitted claim level;
- selected route family, structural branch, identifiability assumption, or necessary complexity;
- validation target, independence unit, evaluator, or pass standard.

Do not ask about source-fixed facts or reversible notation, filenames, layout, implementation convenience, or a sensitivity-tested default that cannot change those items. A missing numeric preference is consequential when it changes the optimizer or conclusion, even if software would normally demand a value.

## Review packet

Ask one consequential decision, or one tightly coupled group, as soon as its dependency boundary is reached. Every packet must contain:

1. **decision**: the exact fork and what downstream work it controls;
2. **evidence**: source pointers and established facts;
3. **live options**: at least two real choices, unless the question is whether to accept a single necessary assumption;
4. **consequences**: what each option changes in variables, feasible set, objective, validation, complexity, or claim ceiling;
5. **recommendation**: one preferred option, why its evidence/risk tradeoff is strongest, and when the alternative would be better;
6. **lock effect**: the exact interpretation, assumption, route, preference, or claim boundary that approval will fix.

Do not use vague approval prompts such as “这样可以吗”. Do not bundle unrelated decisions to reduce the apparent number of questions. Do not repeatedly reopen an approved point without conflicting new evidence. While waiting, continue only work that cannot be invalidated by the pending choice.

## Ledger contract

Record each material packet in `human_review.decision_points` with stable ID, kind, summary, options, recommendation, consequences, evidence, dependencies, status, and resolution. Valid kinds are `interpretation`, `objective`, `preference`, `route`, `complexity`, `validation`, and `claim_boundary`.

- `pending`: asked or ready to ask; dependent work must not cross it.
- `user_confirmed`: the user selected or accepted an option; create or update the corresponding lock.
- `reopened`: new evidence conflicts with the prior resolution; ask again and preserve history.
- `superseded`: the decision became immaterial because a higher-level approved choice removed the branch.

`human_review.status` is `pending`, `approved`, or `blocked`. Do not set it to `approved` while any decision point is pending/reopened or while final route review is incomplete.

## Final route review

After every source-triggered audit, repair, regression, competition-readiness check, excellence check, and executable-field check passes:

1. freeze the exact detailed route artifact that would be handed to an implementer;
2. present its path or complete user-visible content, main route, decisive assumptions, validation plan, exception handling, and honest claim limits;
3. recommend either **approve** or **revise**, naming any residual risk;
4. ask the user to approve that exact artifact or request a concrete revision;
5. record `final_route_review.reviewed_artifact`, recommendation, evidence, and status.

The final review cannot be inferred from earlier approvals. `route_executable` requires `final_route_review.status = user_approved`, a specific reviewed artifact, a specific recommendation, evidence, and no unresolved material decision.

## Direct completion notice

Once the final artifact is approved and the ledger validates, immediately tell the user:

- `完整落地版建模方案已完成`;
- which artifact was approved and where it is stored;
- that variables, mathematics, constraints, data pipeline, algorithm, validation plan, exception handling, outputs, and stopping conditions are closed;
- any retained assumption or claim boundary;
- `待你确认/下一步：无需确认；完整落地版建模方案已完成`.

End there. Do not turn completion into a sales question and do not ask whether to calculate, run code, draw result figures, or continue solving.
