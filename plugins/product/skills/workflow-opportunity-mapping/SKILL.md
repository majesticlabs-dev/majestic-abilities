---
name: workflow-opportunity-mapping
description: Map an observed operational workflow into actors, work objects, states, handoffs, evidence, burdens, automation choices, control points, and exceptions. Use when customer research, process notes, support evidence, or operator interviews need to become a grounded workflow model and a shortlist of software or AI opportunities. Not for conducting discovery research, validating demand, or writing requirements.
---

# Workflow Opportunity Mapping

Represent the work before proposing automation. Make the current workflow, its evidence, and its failure modes visible enough that product choices can be challenged.

## Boundary

Use this skill after relevant workflow evidence exists. It may expose research gaps, but it does not design the research study, establish market demand, select a roadmap priority, or write implementation requirements.

Do not assume that recurring work should be automated. Elimination, simplification, clearer ownership, or a deterministic integration may be better than adding AI. Do not turn a workflow-fit assessment into a market-size or ROI claim.

## Required Inputs

Establish:

- decision the map must inform and workflow scope
- user or operator segment and triggering situation
- supplied observations, interviews, artifacts, logs, tickets, or process documentation
- systems, policies, privacy limits, and operational constraints
- known failure consequences and definition of acceptable completion

Classify material inputs as:

- **Observed:** directly visible behavior or inspectable artifact
- **Reported:** a participant or stakeholder account
- **Inferred:** an interpretation supported by one or more inputs
- **Unknown:** required context that is unavailable

Do not relabel reported or inferred material as observed fact.

## Workflow

### 1. Frame the workflow

Name the triggering event, intended outcome, accountable actor, start boundary, end boundary, frequency, and consequence of delay or error. Split unrelated workflows rather than hiding them under a broad label.

### 2. Model the current work

Trace:

- actors and decision rights
- work objects and their states
- state transitions and handoffs
- systems and informal sources of truth
- required inputs, permissions, deadlines, and dependencies
- evidence that proves each material step is complete
- common exceptions, loops, abandonment points, and recovery paths

Preserve conflicting accounts. Do not invent a single canonical process when the evidence shows several variants.

### 3. Locate the burden

For each material step, identify:

- action being performed
- burden mechanism, such as search, re-entry, reconciliation, waiting, uncertainty, coordination, drafting, monitoring, approval, or recovery
- frequency and time or attention consumed
- error and delay consequences
- evidence status and confidence

A complaint without repeated behavior or consequence is a research lead, not a validated opportunity.

### 4. Choose an intervention posture

Consider, in order:

1. eliminate the step
2. simplify the policy or handoff
3. connect existing systems
4. use deterministic rules or computation
5. assist with probabilistic or generative behavior
6. keep the step human-led
7. do not automate

Evaluate ground-truth clarity, stakes, reversibility, data quality, privacy, security, relationship impact, required explanation, and accountability. High-consequence work with unclear ground truth must remain human-controlled.

### 5. Sketch the intervention

For each credible opportunity, describe enough to distinguish the proposed experience:

- trigger and available inputs
- system assistance or state change
- visible output
- user review, approval, override, or cancellation
- provenance and uncertainty shown
- escalation and recovery path

Keep this solution-direction level. Do not commit detailed requirements, acceptance criteria, architecture, fields, interfaces, or delivery scope. Labels such as “AI assistant” or “automate this” are too vague to evaluate.

### 6. Design the exception path

State what prevents straight-through completion, why the exception is surfaced, what evidence the user sees, what decision is required, who owns it, and how work resumes.

### 7. Shortlist without fake precision

Compare candidate opportunities using evidence strength, frequency, consequence, workflow leverage, apparent feasibility, operational risk, and reversibility. Default to at most three supported candidates. This is an evidence-readiness shortlist, not a roadmap priority or delivery commitment. Use qualitative judgments or ranges when the inputs cannot support numeric scoring.

### 8. Define the next evidence step

For the leading opportunity, identify the smallest observation, prototype, manual trial, or data check that could disprove the workflow model or intervention assumption.

## Output

1. **Scope and evidence boundary**
2. **Current workflow map** with states, handoffs, systems, and completion evidence
3. **Burden and opportunity table** with evidence status
4. **Candidate intervention sketches** with controls, provenance, and recovery
5. **Exception handling**
6. **Shortlist and rejected automations**
7. **Unknowns and next evidence step**

Default to one workflow table and at most three candidate interventions. Combine sections when that avoids repetition. Add a diagram only when sequence or branching is hard to understand in prose or a table. Expand beyond these defaults only when the user requests depth or the workflow risk requires it.

## Quality Gate

- Every material claim is labeled Observed, Reported, Inferred, or Unknown.
- The map distinguishes the current workflow from the proposed product.
- Automation follows workflow understanding rather than preceding it.
- High-stakes judgment retains visible human control.
- Every proposed behavior includes failure, override, and recovery handling.
- Ranking does not imply demand, ROI, or feasibility beyond the supplied evidence.
