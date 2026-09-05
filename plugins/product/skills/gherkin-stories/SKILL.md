---
name: gherkin-stories
description: "Use when drafting or repairing ticket-ready user stories with Gherkin acceptance scenarios."
---

# Gherkin Stories

Turn settled product intent into small behavioral contracts that product, engineering, and QA can interpret the same way.

## Boundary

Use this skill to generate atomic stories from a source requirement or to audit an existing story set. The behavior must be settled enough to describe observable results.

Do not use it to choose product policy, write a whole PRD, prioritize a backlog, prescribe technical architecture, or perform a general requirements-quality review. Do not claim that a story set is implementation-ready when repository, design, security, data, or operational evidence is unavailable.

Treat missing policy as an open decision. Never turn a plausible default, example, or implementation guess into acceptance criteria.

## Inputs

Establish what the supplied material supports:

- source requirements with stable IDs or quoted source text
- actor, goal, trigger, approved rules, and observable outcomes
- permissions, state transitions, thresholds, timing, and exact copy when authoritative
- dependencies, constraints, exclusions, and delivery boundaries
- known failure, boundary, retry, cancellation, and recovery behavior
- applicable product-analytics or operational-observability conventions

Choose **generation** or **audit** mode. In audit mode, preserve the original IDs and wording before proposing changes. Missing context narrows the result; it does not authorize invention.

## Atomicity Standard

Treat each scenario as one testable behavioral example:

- Use relevant `Given` clauses only for preconditions and state.
- Use one `When` for one actor action or external event.
- Use `Then` for one observable behavioral outcome.
- Use additional `Then` or `And` assertions only for observable facets of that same outcome.
- Split distinct triggers or outcomes into separate scenarios.

Treat each story as one user-visible behavioral rule or capability. Keep scenarios together only when they exercise that same rule under different relevant states. Split a story when an actor, trigger, policy, or outcome could be understood and accepted independently.

Require stories to be independently understandable and testable, not independently deployable. Record legitimate dependencies instead of hiding them.

## Generation Workflow

1. **Set the evidence boundary.** Record the supplied sources, stable requirement IDs, authoritative rules, assumptions, and unavailable evidence.
2. **Inventory behavior.** Extract actors, triggers, states, outcomes, constraints, and unresolved decisions without rewriting them yet.
3. **Decompose the requirement.** Create the smallest stories that preserve the approved intent. Check applicable variations in actor or permission, state, validity or timing, repetition, empty or missing input, cancellation, retry, recovery, and dependency failure. Do not create a variation merely to fill a checklist.
4. **Write the primary scenario.** Name the condition and behavior. Keep `Given` factual, `When` singular, and `Then` externally observable. Replace words such as “gracefully,” “properly,” “normally,” and “successfully” with the concrete behavior they imply.
5. **Assess edge coverage.** Select the highest-risk meaningful alternate, failure, boundary, permission, retry, cancellation, or recovery path. Add a scenario when the expected behavior is supported. If the behavior is unknown, record the decision needed instead of writing speculative Gherkin. If no meaningful edge applies, state why.
6. **Add connective tissue.** Record dependencies, out-of-scope behavior, and open decisions. Add instrumentation only when it is applicable and supported by a product or operational need; describe the signal and purpose without inventing an event schema.
7. **Build traceability.** Map every source requirement to its stories and scenario IDs. Mark obligations as covered, partially covered, or deferred with a reason.
8. **Run the quality gate.** Split compound behavior, remove unsupported detail, and confirm that another reader can test each scenario without guessing the expected result.

## Gherkin Rules

- Name scenarios for the condition and expected behavior, not generic labels such as “happy path” or “error case.”
- Keep setup in `Given`, the trigger in `When`, and observable product behavior in `Then`.
- Avoid UI copy, thresholds, timing, roles, or retry policy unless the source approves them.
- Avoid implementation details unless they are explicit product constraints.
- Do not use telemetry as the `Then`; instrument the behavior separately.
- Use data tables or scenario outlines only when examples share one rule and make a meaningful boundary clearer.
- Keep unresolved placeholders outside executable Gherkin.

## Audit Workflow

1. Inventory the source stories and scenarios as written.
2. Check each story for one coherent behavioral rule and each scenario for one trigger and one outcome.
3. Flag compound scope, multiple triggers, distinct outcomes joined as assertions, vague or non-observable results, implementation prescriptions, and unsupported product rules.
4. Check whether risk-relevant negative behavior, dependencies, exclusions, applicable instrumentation, and requirement-to-scenario traces are present.
5. Distinguish a structural defect from a missing product decision. Do not “repair” the latter by choosing an answer.
6. Return evidence-backed findings and label every rewrite as proposed. Preserve source intent, IDs, and trace links.

## Output

For generation, default to:

1. **Evidence boundary:** supplied sources, authoritative rules, assumptions, and unavailable evidence
2. **Story inventory:** story ID, title, actor or intent, source requirement, and coverage status
3. **Story details:** primary scenario, risk-relevant edge scenario or rationale, instrumentation when applicable, dependencies, out of scope, and open decisions
4. **Traceability table:** source requirement -> story -> scenario -> coverage status
5. **Open decisions:** question, affected stories, decision owner when known, and effect on acceptance

Use conventional `As a / I want / so that` wording only when the actor, capability, and value are supported. Otherwise use a factual title and intent without fabricating a benefit.

For an audit, return:

1. **Verdict:** `Ready`, `Needs revision`, or `Needs decisions`
2. **Evidence boundary**
3. **Findings:** item, observable defect or gap, evidence, impact, and proposed repair
4. **Proposed stories or scenarios** when requested or needed to make the repair concrete
5. **Traceability gaps and open decisions**

## Quality Gate

- Every source obligation is covered, partially covered, or explicitly deferred.
- Stable IDs link requirements, stories, and scenarios.
- Each scenario contains one triggering action or event and one behavioral outcome.
- Multiple assertions verify facets of the same outcome rather than hiding more behavior.
- Edge coverage is risk-driven, explicit, and supported by evidence.
- Unknown behavior remains an open decision outside executable Gherkin.
- Instrumentation is applicable, separate from product behavior, and does not invent a schema.
- Dependencies and exclusions are visible.
- Proposed repairs preserve approved intent and do not conceal uncertainty.
