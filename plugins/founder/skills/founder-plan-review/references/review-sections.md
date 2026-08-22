# Founder Plan Review Sections

Use these sections after the plan premise, alternatives, review posture, and proposed scope are clear.

Evaluate every section. Mark a section `Not applicable` and state why when the plan has no relevant surface. Do not invent implementation detail to fill a section.

For each material finding, record:

- severity: Critical, High, Medium, or Low
- evidence from the plan, repository, or verified source
- affected outcome, user, system, or operation
- plausible failure and consequence
- smallest correction, decision, or verification step
- owner or unresolved decision when known

Ask the user only about material scope decisions that block continued review. Complete the report without forcing approval for each finding.

## 1. Architecture And Boundaries

Review:

- system shape, component responsibilities, and dependency direction
- new coupling and whether it is justified
- reuse of existing flows, services, data, and operating capabilities
- state ownership and invalid state transitions
- trust and authorization boundaries
- single points of failure and external integration boundaries
- behavior under credible growth or load change
- immediate rollback posture
- whether accepted expansion creates reusable leverage or a speculative platform

For each new data flow, trace:

```text
input -> validation -> transformation -> persistence or side effect -> output
```

Cover the normal path plus missing input, empty input, invalid input, upstream failure, partial completion, stale state, and duplicate execution when applicable.

Use a component, state, or flow diagram when relationships cannot be explained clearly in prose. Do not require a diagram for a trivial linear change.

## 2. Errors And Recovery

Map every material fallible path. Name the actual error or protocol response when the plan and technology establish it. Otherwise mark the error identifier unresolved instead of inventing one.

Use this registry when several failure paths exist:

| Codepath or operation | Failure | Error or signal | Recovery | Operator visibility | User impact | Test |
| --- | --- | --- | --- | --- | --- | --- |

Check:

- timeouts, rate limits, malformed responses, unavailable dependencies, and exhausted resources
- missing records, conflicts, duplicate work, and partial writes
- retry eligibility, backoff, idempotency, and retry exhaustion
- graceful degradation and restoration behavior
- added context when an error is re-raised or propagated
- catch-all handling that hides distinct recovery needs
- logs that omit the attempted operation, request, actor, or relevant identifiers

For AI or model calls, distinguish empty output, malformed structured output, refusal, safety block, timeout, tool failure, and content that fails validation.

Every failure must be visible to operators. Require user-visible feedback when the failure changes the user's result, latency, or state. Transparent recovery does not need an unnecessary user message.

## 3. Security And Privacy

For each new endpoint, input, data access, mutation, background task, external call, or file operation, assess:

- added attack surface
- accepted types, sizes, encodings, and rejection behavior
- authentication and authorization scope
- direct object reference and tenant-isolation risk
- SQL, command, template, path, and prompt injection
- secret storage, access, rotation, and accidental exposure
- dependency provenance and material vulnerability exposure
- personal, financial, credential, confidential, or regulated data
- retention, deletion, export, and audit requirements
- abuse, replay, automation, and denial-of-service paths

For each finding, state threat, likelihood, impact, existing control, and required mitigation or verification. Escalate legal, privacy, or specialist questions rather than implying clearance.

## 4. Data And Interaction Edge Cases

Trace each data path through validation, transformation, persistence, and output. Check where relevant:

- nil or missing value
- present but empty value
- wrong type or unsupported encoding
- maximum and minimum boundaries
- stale or conflicting state
- duplicate request or job
- concurrent mutation
- timeout or interrupted work
- partial batch completion
- locked, unavailable, or inconsistent storage
- stale, partial, or differently encoded output

For each user-visible interaction, check applicable states and interruptions:

- repeated submission or double activation
- navigation away during work
- slow or lost connection
- retry while work is in flight
- stale browser or client state
- back and forward navigation
- expired session or authorization change
- zero results and very large result sets
- deploy while an interaction is active
- background work that runs twice, fails partway, or waits in a backlog

Do not list hypothetical edge cases without a path and consequence. Require a correction or test for each material unhandled path.

## 5. Maintainability And Implementation Shape

Review the proposed implementation shape without turning the review into line-level code review.

Check:

- fit with established repository patterns and boundaries
- duplicated behavior or parallel systems
- names that hide responsibility or business meaning
- abstractions without a current second use or clear boundary need
- fragile shortcuts that assume only the normal path
- excessive branching or state complexity supported by the plan
- new files, services, packages, or configuration without a necessary role
- comments or diagrams that will become stale or duplicate executable behavior

Challenge both over-engineering and under-engineering. Recommend the smallest shape that meets the accepted scope and risk standard.

## 6. Verification Strategy

Inventory applicable new surfaces:

```text
user flows
business and data flows
branches and state transitions
background or asynchronous work
external integrations
failure and recovery paths
security and permission paths
```

Map each material surface to suitable unit, integration, system, end-to-end, contract, load, security, or evaluation coverage.

Check:

- normal behavior
- named failures and recovery
- missing, empty, and boundary inputs
- authorization failures
- duplicate and concurrent execution
- migration and rollback behavior
- mixed-version behavior during deployment
- time, randomness, ordering, and external-service flakiness
- load or stress evidence for capacity-sensitive paths
- evaluation cases and baselines for model or prompt behavior

Require evidence proportionate to risk. Do not require every test type for every path.

## 7. Performance And Capacity

Assess only concrete paths introduced or materially changed by the plan.

Check:

- query count, association traversal, and N+1 risk
- index support for new filters, joins, ordering, and uniqueness rules
- maximum in-memory collection or payload size
- streaming or batching requirements
- cache value, invalidation, and stale-result risk
- background job payload, runtime, retries, and queue pressure
- slow external calls and critical-path latency
- database, cache, queue, and HTTP connection pressure
- retry storms, fan-out, and downstream rate limits

Do not fabricate latency or capacity numbers. State which measurement, production evidence, or load test is needed when a bound is unknown.

## 8. Operations And Debuggability

Determine whether an operator can detect, diagnose, and recover from the plan's failures.

Check:

- structured logs at material state changes and failure points
- correlation identifiers across requests, jobs, and services
- success, failure, latency, saturation, and business-outcome metrics
- traces for cross-service or asynchronous paths
- alerts tied to actionable conditions
- dashboards needed for launch or ongoing operation
- diagnostic context sufficient to reconstruct an incident
- administrative or repair operations
- runbooks for material failure and recovery paths
- audit records for sensitive actions

Do not require logs at every entry, exit, or branch. Require only evidence that closes a concrete detection or diagnosis gap.

## 9. Deployment And Rollback

Review the complete transition from old state to new state.

Check:

- backward-compatible schema and data changes
- table locks, long migrations, backfills, and partial migration state
- compatibility while old and new versions run together
- deployment and migration order
- feature flags or staged exposure when risk justifies them
- configuration, secret, and dependency readiness
- environment parity for material behavior
- rollback steps and whether rollback loses or corrupts data
- post-deploy smoke tests and verification
- checks for the first minutes and first operating cycle
- cleanup after safe adoption

Use a deployment or rollback diagram when ordering has several dependent stages or irreversible transitions.

## 10. Long-Term Trajectory

Review what becomes easier or harder after this plan ships.

Check:

- technical, operating, testing, and documentation debt
- path dependency and switching cost
- knowledge concentrated in one person or undocumented process
- reversibility of the product and technical decisions
- fit with current framework, platform, market, and company direction
- clarity for a new team member after twelve months
- next likely product or operating phase
- whether accepted expansion creates reusable capability
- whether deferred work is truly optional or required by accepted scope

State the future-state delta and the evidence that would cause the company to revisit the direction.

## 11. Design, UX, And Accessibility

Apply this section only when the plan changes a user-visible interface or interaction.

Review:

- information priority and what the user sees first, second, and third
- loading, empty, error, success, partial, stale, and permission states
- journey continuity across screens, channels, and interruptions
- product-specific interaction choices versus generic interface defaults
- design-system fit and reuse
- responsive behavior and touch interaction
- keyboard access, focus, labels, announcements, contrast, and target size
- trust signals around identity, destructive actions, privacy, and recovery

Use a user-flow diagram when several screens or states interact. State `Not applicable` when the plan has no interface scope.

## Final Review Assembly

After all sections are evaluated, produce:

1. verdict and selected posture
2. premise and future-state assessment
3. recommended approach
4. accepted, deferred, rejected, and pending scope decisions
5. what already exists and should be reused
6. severity-ranked findings by section
7. error and recovery registry when applicable
8. rollout and rollback assessment
9. explicit exclusions
10. unresolved decisions with owners and deadlines when known
11. residual risks and next decision

Do not edit the reviewed plan or claim that proposed changes were accepted. Distinguish recommendations from user-approved scope decisions.
