---
name: multi-agent-architecture
description: Design persistent multi-agent systems with explicit roles, ownership, handoffs, state, permissions, context budgets, and failure handling. Use when building an agent product or durable workflow whose work genuinely requires multiple specialized agents.
---

# Multi-Agent Architecture

Design durable multi-agent systems. Do not use this skill merely to delegate an ordinary task in the current coding session.

## Viability Gate

Start with one agent and deterministic software. Add another agent only when it owns a distinct job that benefits from separate context, permissions, lifecycle, or evaluation.

Reject multi-agent architecture when:

- a deterministic function or workflow can do the work
- roles share the same inputs, tools, and success criteria
- one agent can complete the task within its context budget
- coordination cost exceeds specialization value
- the design exists only to simulate an organization chart

## Inputs

Establish:

1. User outcome and service boundary.
2. Workstreams and why each requires agent judgment.
3. Data sources, tools, and external systems.
4. Latency, throughput, cost, and context constraints.
5. Security, privacy, approval, and audit requirements.
6. Failure recovery and human escalation expectations.

## Workflow

### 1. Write role contracts

Define each role as a job before choosing models or frameworks:

- purpose
- owned decisions
- inputs
- outputs
- tools and data access
- success criteria
- forbidden actions
- escalation conditions

If two roles own the same decision, fix the ownership model.

### 2. Choose the coordination topology

Select the smallest topology that fits dependencies:

- **Coordinator and workers:** centralized decomposition and synthesis
- **Pipeline:** ordered transformations with explicit stage contracts
- **Event-driven peers:** independent consumers reacting to durable events
- **Reviewer gate:** producer output requires separate acceptance
- **Hybrid:** justified combination of the above

Do not add direct peer communication without a concrete need. Every communication edge adds state, failure, and observability cost.

### 3. Define state and context

Separate:

- durable business state
- transient execution state
- shared artifacts
- agent-local working context
- audit history

Use references or artifact paths instead of relaying large outputs through a coordinator. Define retention, versioning, redaction, and concurrent-write rules.

Assign one writer to each mutable artifact or serialize competing writes.

### 4. Specify handoffs

For every handoff, define:

- producer and consumer
- input and output schema
- completion and acceptance criteria
- idempotency key
- timeout and retry policy
- error and escalation path
- provenance required for review

Treat natural-language summaries as data only when their schema and verification rules are explicit.

### 5. Bound permissions

Grant each role the minimum tools, credentials, records, and actions required. Separate read, propose, approve, and execute permissions for consequential operations.

Require human approval where errors create material financial, legal, security, safety, or trust harm.

### 6. Budget context and cost

Define limits for:

- input context
- generated output
- tool calls
- retries
- parallel work
- wall-clock time
- monetary cost

Choose degradation behavior when a budget is exhausted. Do not silently continue with truncated evidence.

### 7. Design failure handling

Cover:

- duplicate delivery
- partial completion
- stale state
- conflicting outputs
- unavailable tools or models
- poison tasks and retry loops
- coordinator failure
- human escalation
- rollback or compensation

Persist enough state to resume safely without replaying irreversible actions.

### 8. Define evaluation and observability

Measure role-level and system-level outcomes:

- task success and acceptance rate
- unsupported claims or policy violations
- handoff failures
- latency and cost
- retry and escalation rate
- user-visible outcome quality

Log decisions, evidence references, state transitions, and approvals without exposing secrets.

## Deliverable

Return:

1. Viability verdict and simpler alternative
2. Role contracts
3. Topology and sequence diagram
4. State and artifact model
5. Handoff schemas
6. Permission matrix
7. Context and cost budgets
8. Failure and recovery table
9. Evaluation plan
10. Open risks and implementation slices

## Quality Gate

- Every agent has a distinct owned job.
- One owner exists for each decision and mutable artifact.
- Handoffs are testable contracts.
- Permissions and approvals match consequence.
- Retry, resume, and duplicate-delivery behavior are defined.
- The design explains why one agent plus software is insufficient.
