---
name: rails-code-review
description: "Use when reviewing Rails changes for correctness, safety, and missing tests."
---

# Rails Code Review

Review a concrete Rails change set against its intended behavior and the application that will run it. Prioritize actionable defects and release risk over style commentary.

## Boundary

Review only the requested diff, patch, files, or comparison range, plus the callers, configuration, schema, tests, and framework code needed to validate changed behavior. Do not modify code unless the user explicitly asks for fixes.

Use this skill for Rails applications and engines. A Ruby gem or standalone Ruby program without Rails requires Ruby-specific review instead.

Do not treat a personal Rails style preference as a defect. A convention concern belongs in Findings only when it creates a concrete correctness, maintenance, security, performance, or operability consequence in this application.

## Required Context

Before reaching conclusions, establish:

- the exact review scope and comparison base
- the requested behavior, acceptance criteria, or issue being solved
- the Ruby and Rails versions from files such as `.ruby-version`, `Gemfile`, and `Gemfile.lock`
- repository instructions, configured Rails defaults, architectural boundaries, and established application patterns
- the database adapter, relevant database configuration, schema format, and deployment constraints
- the affected runtime components, such as the web server, Active Job adapter, cache and session stores, Action Cable, Active Storage, Action Mailer, and Hotwire or another frontend stack
- the authentication, authorization, tenancy, and request-context mechanisms that protect the changed path
- the test framework, relevant test commands, CI gates, checks already run, and known failures

Inspect only context relevant to the change. Do not inventory the whole application when the touched behavior is narrow.

If missing framework or application context materially prevents a safe conclusion, identify exactly what is missing and return `BLOCKED`. Do not substitute assumptions from another Rails version or from a different application.

## Framework Evidence

Use evidence in this order:

1. changed code and its reachable application paths
2. tests, schema, configuration, and existing repository patterns
3. behavior of the application's installed gem versions
4. official Rails or dependency documentation matching those versions

Consult current primary documentation when an API or lifecycle rule is version-specific or uncertain. Do not apply the latest Rails behavior to an older application without verifying compatibility. Record unresolved behavior as an open question or residual risk, not as a fabricated finding.

## Workflow

1. Read the complete change set before forming conclusions.
2. Map each changed behavior from entry point to persisted or rendered outcome. Include routes, controllers, policies, models, callbacks, jobs, views, broadcasts, mailers, and external boundaries when they participate.
3. Identify the Rails subsystems touched and apply only the relevant checks below.
4. Trace changed contracts through callers, dynamic dispatch, associations, callbacks, retries, transactions, and side effects. Missing evidence is residual risk, not proof of safety.
5. Compare the implementation with the stated requirement, installed framework behavior, and established application patterns.
6. Inspect tests for observable outcomes, important failure paths, persisted state, authorization, and regression protection.
7. Run the narrowest relevant repository checks when execution is available, followed by broader Rails tests, lint, or security checks when justified by the change.
8. Keep only findings supported by a concrete code path and user-visible or operational consequence.

## Rails Review Areas

### Requests, Controllers, And Authorization

Check relevant paths for:

- route and HTTP verb semantics, including Turbo and non-Turbo formats
- strong parameters, mass assignment, authentication, authorization, and tenant scoping
- response status, redirects, rendering, content negotiation, and double-render paths
- CSRF, open redirect, injection, unsafe deserialization, and information exposure
- request-local state such as `Current` leaking across requests or jobs

Authorization must protect the server-side action and data scope. Hidden controls in a view are not authorization.

### Active Record And Domain Behavior

Check relevant paths for:

- validations that disagree with database constraints or permit race conditions
- transaction boundaries, partial writes, external calls inside transactions, and lock duration
- callback ordering, recursion, hidden side effects, and work that must occur after commit
- optimistic or pessimistic locking where concurrent updates can violate an invariant
- association lifecycle, `dependent` behavior, counter caches, enums, and serialization compatibility
- query shape, N+1 behavior, unbounded loads, ordering, pagination, and tenant filters

Load [references/rails-conventions.md](references/rails-conventions.md) and [references/rails-architecture.md](references/rails-architecture.md) for application structure and convention checks.

### Migrations And Data Changes

When the change touches schema, backfills, destructive updates, constraints, or sensitive data, load [references/data-safety-checklist.md](references/data-safety-checklist.md). Verify:

- compatibility across rolling or phased deploys
- table-lock and rewrite risk for the actual adapter and expected data volume
- safe ordering of indexes, foreign keys, defaults, `NOT NULL`, and uniqueness enforcement
- resumability and idempotency of backfills
- behavior under concurrent writes and partial failure
- rollback or forward-recovery strategy

Migration reversibility alone does not prove deployment safety.

### Active Job And Asynchronous Work

Check relevant paths for:

- retry and duplicate-execution consequences, including idempotency of external side effects
- enqueue timing relative to transaction commit
- stale records, GlobalID serialization, queue selection, priority, timeout, and discard behavior
- exception handling that hides failed work or causes an uncontrolled retry loop
- authentication, tenant, locale, and request context that will not automatically exist in a worker
- jobs that assume execution order or exactly-once delivery

### Hotwire, Views, And Browser Behavior

Check relevant paths for:

- Turbo Frame and Turbo Stream targets, stable DOM IDs, response formats, and fallback navigation
- Stimulus lifecycle behavior across reconnects, cached pages, replacement, and repeated initialization
- server-rendered authorization and state consistency across HTML and stream responses
- escaping, unsafe HTML, duplicate element IDs, and stale broadcasts
- browser behavior that tests or manual verification must prove rather than infer from templates

### Cache, Sessions, Storage, Mail, And Integrations

When touched, verify cache keys and invalidation, session trust boundaries, signed or encrypted values, attachment lifecycle, mail delivery retries, webhook authenticity, timeout behavior, and duplicate external requests. Confirm secrets and sensitive values do not enter logs or job payloads.

### Rails Tests

Require tests at the narrowest level that proves application behavior. Check that tests:

- cover the changed outcome and material failure paths
- assert persisted state after reload when persistence matters
- exercise authorization and tenant boundaries
- account for callback, transaction, retry, broadcast, or delivery side effects
- do not merely retest Rails itself
- match the repository's Minitest, RSpec, fixture, factory, system-test, and mocking conventions

Passing tests do not prove correctness, but missing framework-specific coverage lowers shipping confidence.

## Optional Simplicity Lens

Load [references/dhh-rails-review-lens.md](references/dhh-rails-review-lens.md) only when the user requests DHH or 37signals style, or when that style is an explicit repository rule. Keep stylistic advice outside Findings unless it creates a concrete consequence.

## Finding Standard

Each finding must include:

- severity: critical, high, medium, or low
- file and line reference
- the incorrect or unsafe behavior
- the Rails and application conditions that trigger it
- the user-visible or operational consequence
- the evidence supporting the finding
- the smallest safe correction

Do not report optional refactors, generic Rails advice, personal preferences, or speculative concerns as defects. Risks without a demonstrated defect belong in Residual risk.

## Release Verdict

When asked for a quality gate, return exactly one verdict:

- `APPROVED`: no unresolved material defect, required Rails context was established, and relevant verification passed
- `NEEDS CHANGES`: one or more actionable defects must be corrected
- `BLOCKED`: missing scope, framework context, environment, or prerequisite prevents a responsible decision

Do not approve framework-dependent behavior using only a language-neutral review.

## Output

1. **Rails context**, limited to versions and components relevant to the change
2. **Findings**, ordered by severity and confidence
3. **Verdict**, when requested
4. **Open questions or assumptions**
5. **Checks run** and their results
6. **Residual risk**

If there are no findings, say so directly and identify any verification that was not possible.
