---
name: lessons-learned
description: Extract evidence-based lessons from completed work or a resolved problem and convert them into specific future practices. Use after a project, incident, experiment, implementation, campaign, or operating cycle has enough evidence to assess what should be repeated, changed, or avoided. Not for judging whether a consequential decision process was sound.
---

# Lessons Learned

Turn completed work into practices that improve similar future work. A lesson must change future behavior or explicitly justify no change.

## Boundary

Use this skill when work is complete, a problem is resolved, or an experiment has produced enough evidence to compare expectations with results.

Do not use it to:

- choose among options that are still open
- judge whether a consequential decision was rational given what was known at the time
- assign blame or infer a person's motives
- write a chronology without extracting reusable guidance
- declare a lesson while the outcome or cause remains unknown
- create or maintain a repository knowledge store unless the user requests that artifact

Completed work can include decisions, but this skill evaluates what the work teaches. It does not audit decision quality.

## Required Inputs

Collect the available evidence for:

- intended outcome and scope
- actual outcome
- important actions, constraints, and changes during execution
- expected and unexpected effects
- failures, recoveries, and successful practices
- verification, measurements, feedback, or other outcome evidence
- unresolved unknowns

Separate contemporaneous records from later recollection. Missing evidence narrows the lesson and confidence.

## Workflow

### 1. Establish the evidence boundary

List what is directly observed, what is reported from memory, what is inferred, and what remains unknown.

Do not treat a later outcome as proof that an earlier action caused it. Name competing explanations when the evidence cannot distinguish them.

### 2. Compare intent with outcome

State:

```text
intended outcome -> actions and conditions -> observed outcome
```

Identify where the result matched, exceeded, or missed the intent. Include useful unexpected results. Do not treat every difference as a failure.

### 3. Identify candidate lessons

For each candidate, ask:

- What evidence supports it?
- What mechanism explains the result?
- Under what conditions should it apply?
- What would make it false or unsafe to reuse?
- Does it change a future action, check, or stopping rule?

Reject generic statements such as "communicate better," "test more," or "plan earlier" unless the evidence supports a specific practice and trigger.

### 4. Convert lessons into future practices

Classify each supported lesson as one of:

- **Repeat:** preserve a practice that contributed to the result.
- **Change:** modify a practice that caused avoidable cost or failure.
- **Stop:** remove a practice whose expected value was not supported.
- **Add evidence:** collect a missing signal before making the same inference again.
- **No change:** keep the current practice because the evidence does not justify a change.

For each practice, state where it applies and where it does not. Avoid turning one event into a universal rule.

### 5. Choose the output location

Return the lessons in the conversation unless the user requests a durable artifact or the project provides an explicit location and format for one.

When writing an artifact:

- use the requested or established project location
- update an existing relevant artifact instead of creating a duplicate when practical
- include the evidence and applicability boundary with each lesson
- do not edit instructions, code, or unrelated documentation automatically

## Output

1. **Work reviewed:** scope, intended outcome, and actual outcome
2. **Evidence boundary:** observed facts, recollections, inferences, and unknowns
3. **Lessons:** evidence, mechanism, applicability, and confidence
4. **Future practices:** repeat, change, stop, add evidence, or no change
5. **Artifact:** path when one was requested and written

If the evidence supports no reusable lesson, say so. Do not create a lesson to make the exercise appear productive.

## Quality Gate

- The work is complete enough to support reflection.
- Each lesson cites evidence and a plausible mechanism.
- Outcome and causation are not treated as the same thing.
- Each supported lesson changes a specific future practice or justifies no change.
- Applicability limits and unknowns remain visible.
- The result does not duplicate a decision-process retrospective.
- No durable artifact or repository change occurs without a requested or established destination.
