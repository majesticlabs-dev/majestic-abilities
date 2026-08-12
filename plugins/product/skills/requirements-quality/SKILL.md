---
name: requirements-quality
description: Audit and repair individual requirements and requirement sets without inventing missing decisions. Use when requirements in a PRD, specification, user-story set, acceptance criteria, BRD, FRD, or catalogue need statement-level or set-level review for ambiguity, consistency, traceability, testability, evidence, abstraction fit, or coverage. Not for whole-document or implementation-plan readiness.
---

# Requirements Quality

Review requirements as evidence-backed obligations, not sentences to polish mechanically.

## Boundary

Use this skill when requirements or candidate requirements already exist and need a quality gate before approval, decomposition, or delivery handoff.

Do not use it to discover the problem, choose among product directions, or assess whole-document or implementation-plan readiness. Review requirement statements and their set as a bounded part of a larger artifact. If the input mixes requirements with notes, classify the statements before auditing them. Do not silently promote an idea, preference, assumption, or question into an approved requirement.

Missing context narrows the verdict rather than blocking the review. Never claim factual correctness, feasibility, currency, ownership, or stakeholder approval without supporting evidence.

## Inputs

Establish what is available:

- requirements artifact and any stable identifiers
- intended next consumer or decision
- project purpose, scope, and exclusions
- source evidence, constraints, glossary, and applicable standards
- owner or approving authority, baseline, and review history

Ask only when the intended abstraction level or next consumer would materially change the review. Infer the next consumer from explicit artifact evidence when possible. If neither the request nor artifact identifies one, default to an **internal quality review** at the level written and state that this cannot establish handoff readiness. Under that default, use Blocker only for a defect that prevents stable interpretation or creates an intrinsic contradiction; treat consumer-specific readiness gaps as Major and Unknown.

## Status and Severity

Use exactly these evidence statuses:

- **Pass:** available evidence supports the characteristic.
- **Fail:** the supplied material contains an observable defect.
- **Unknown:** required evidence is missing or cannot be verified.
- **Not applicable:** the characteristic does not apply at this level or stage.

Absence from the input is not automatically a failure. Do not convert `Unknown` into `Fail` to make the review look decisive.

Classify impact separately:

- **Blocker:** prevents the stated next decision or handoff.
- **Major:** creates material risk of dispute, rework, or incorrect delivery.
- **Minor:** improves wording or maintenance without changing the obligation.

## Workflow

### 1. Set the review depth

Use a quick pass only when the user asks for triage. Report the highest-impact findings and proposed corrections. Otherwise perform the full workflow and use [quality-model.md](references/quality-model.md).

### 2. Classify before judging

Classify each source statement as a **goal, need, requirement, constraint, assumption, decision, risk, question, or proposal**. A need describes a stakeholder capability gap or problem without imposing an obligation. A requirement is presented by its wording or source context as an obligation on the organization, product, or solution. A hedged idea or preference about possible behavior is a proposal, an explicit request for an answer is a question, and a belief treated as true is an assumption. Record lifecycle or approval state separately as candidate, proposed, approved, rejected, superseded, or Unknown. Preserve the original wording, status, and source.

For each requirement, assign its level:

- **Business:** outcome or organizational obligation
- **Stakeholder:** capability or quality a user or stakeholder needs
- **Solution:** observable behavior or constraint the delivered system must satisfy

Classify per item. A catalogue may legitimately contain all three levels.

Compare the assigned level with any source label and with the detail required by the next consumer. Report an **abstraction mismatch** when the label, wording, and intended stage do not align. Do not silently preserve a wrong label or force valid higher-level intent into solution detail.

### 3. Build the trace

Where evidence permits, map:

```text
source -> business goal -> stakeholder need -> solution requirement -> acceptance evidence
```

Do not call parent and child requirements duplicates merely because they address the same intent. Evaluate duplication among requirements at the same level that impose the same obligation.

### 4. Audit at the requirement's level

Apply only evidence appropriate to that level:

- Business requirements need measurable outcomes and business validation evidence.
- Stakeholder requirements need a clear capability and enough boundaries to support decomposition.
- Solution requirements need observable behavior and a concrete verification method.

Treat unresolved solution detail beneath a valid higher-level requirement as deferred decomposition, not automatically as a defect.

Use **Not applicable** only when a check has no meaningful obligation at the current level or stage. Use **Unknown** when the check applies but the evidence needed to decide it is missing.

### 5. Audit the set

Review consistency, same-level duplication, coverage for the intended next phase, terminology, organization, modifiability, traceability, and governance metadata.

Run the coverage sweep in [quality-model.md](references/quality-model.md) in the listed order and mark every category `Covered`, `Gap`, or `Not applicable`. Do not stop at the categories that produced findings. The order exists to reach the categories a reviewer habitually skips.

Completeness is relative to the intended consumer and is never fully provable from prose alone. State the evidence that was unavailable.

### 6. Propose repairs

Preserve identifiers, intent, scope, and every valid abstraction level. When an abstraction mismatch exists, preserve the original for auditability and propose relabeling or decomposition separately. Split only obligations that can vary, be approved, or be verified independently.

Do not invent actors, thresholds, priorities, owners, dates, failure behavior, or scope. Preserve named implementation choices when their authority is Unknown, flag the evidence gap, and ask whether they are approved constraints. When a repair depends on a decision, provide the safest partial rewrite and an explicit open question. Label unapproved rewrites as proposed.

### 7. Verify the review

Before returning the result:

- every finding cites the affected requirement and observable evidence
- every conclusion uses Pass, Fail, Unknown, or Not applicable correctly
- set-level defects are not misreported as statement defects
- proposed rewrites do not add unsupported commitments
- higher-level intent remains intact

## Output

Match the user's requested format. Select the verdict deterministically:

- If no statement is classified as a requirement, produce **Unverifiable** for requirements quality and return the classification and open decisions instead of a readiness claim.
- Any Blocker with `Fail` produces **Needs revision**.
- With no blocking failure, any Blocker with `Unknown` produces **Unverifiable**.
- With no Blocker, one or more Major failures, Major unknowns, or deferred decisions required by the next phase produce **Ready with explicit gaps**.
- With no Blocker, no Major failure or unknown, and no phase-required deferred decision, produce **Ready**; Minor findings and optional future decomposition may remain.

For a full audit, default to:

1. **Verdict:** `Ready`, `Ready with explicit gaps`, `Needs revision`, or `Unverifiable`
2. **Evidence boundary:** intended next phase, supplied sources, and unavailable evidence
3. **Inventory:** statement type, requirement level, source, and validation status when useful
4. **Proposed requirements:** repaired statements, preserving stable IDs
5. **Findings:** requirement or set, status, severity, characteristic, evidence, and correction
6. **Open decisions:** stakeholder questions and deferred decomposition
7. **Traceability gaps:** missing upstream or downstream links

List passed checks only when the user asks for a scorecard or audit trail. An empty defect list is valid when the evidence supports it.

## Quality Gate

- Unknowns remain unknown.
- No requirement is declared correct solely because its wording is clean.
- No missing metadata is failed unless the intended stage requires it.
- Rewrites preserve both provenance and abstraction level.
- Readiness follows from blockers, not an averaged score.
