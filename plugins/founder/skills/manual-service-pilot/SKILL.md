---
name: manual-service-pilot
description: Turn an idea into a manual pilot offer and operator runbook that tests a customer outcome before automation.
---

# Manual Service Pilot

Design the smallest service that delivers one useful customer outcome by hand, document it so another operator can run it, then use pilot evidence to decide what to improve or automate.

## Boundary

Start from an idea, intended customer, and desired outcome. This skill designs the manual offer and runbook. It does not map an already observed workflow, issue a demand verdict, write product requirements, build automation, contact customers, send messages, collect payment, or deliver a live pilot unless the invoking task explicitly authorizes each action. A proposed pilot and its expected results are not evidence.

Keep the stages separate:

1. **Manual:** an operator performs the work.
2. **Documented:** the operator records a reproducible runbook.
3. **Automated:** a proven, stable step is automated while judgment and exceptions remain controlled.

## Required inputs

- The idea and the single customer outcome it should produce
- Intended customer, triggering situation, required input, and desired result
- Scope, eligibility, and explicit exclusions
- Operator capacity, available tools, access, dependencies, and constraints
- Delivery channel, turnaround expectation, and completion definition
- Pilot offer terms, price, and payment status when known
- Evidence needed to judge customer outcome, repeatability, operator burden, and automation readiness
- Any prior delivery evidence, with each step marked Proposed or Tested

## Workflow

1. **Define the service promise.** Write: “For [customer] when [trigger], the operator turns [input] into [result] and hands it off through [channel].” State the one outcome, boundary, customer obligations, and what is out of scope.
2. **Separate proposed from tested work.** Mark every step Proposed until it has been observed in an actual run. Mark it Tested only when the operator records its input, action, output, timing, exceptions, and handoff verification. Keep the two statuses visible in the runbook.
3. **Build the operator runbook.** For every step, record the trigger or input, action in order, tool, owner, timing, output, completion evidence, and status. Label timing as estimated or measured. Use concrete actions instead of “process the request.”
4. **Map material exceptions.** For missing or invalid input, ambiguity, out-of-scope requests, dependency failure, customer changes, and missed timing, state the trigger, response, owner, customer communication, recovery path, and stop condition. Include exceptions supported by the idea or observed runs; do not invent a catalogue of rare cases.
5. **Define delivery and verify the handoff.** Specify the result format, delivery channel, quality check, and recipient. Record how receipt, access, acceptance, or use is verified when it is part of the promised outcome. Sending a result alone does not prove a verified handoff. State what happens when verification fails.
6. **Write the pilot offer.** State the participant or customer context, promise, manual nature of delivery, scope, operator involvement, timing, required inputs, customer responsibilities, and terms that matter to this service. Include price, payment, cancellation, or refund terms only when decided. Calling this skill does not authorize outreach or charging.
7. **Define the evidence record.** For each run, record observed inputs, each step's status, measured time, rework, exceptions, output, handoff verification, customer-reported result, and operator burden. Keep observation, report, and inference separate. Define what result would support continuing, revising, or stopping the pilot.
8. **Choose automation candidates after testing.** Consider a step only when its inputs and outputs are clear, its behavior is stable across relevant runs, its exceptions are bounded, and the cost of an error is understood. Keep judgment, high-consequence decisions, and unresolved exceptions under explicit human control. State the service-specific evidence needed before automating; do not use a universal paying-customer count or time threshold.
9. **List open decisions and authorization gates.** Separate unknowns from assumptions. Identify the next smallest observation or authorized pilot action that can resolve the most important uncertainty.

## Output

Return:

1. **Service promise and pilot scope:** customer, trigger, input, outcome, exclusions, and completion definition.
2. **Operator runbook:** ordered steps with tools, owner, timing, output, completion evidence, and Proposed or Tested status.
3. **Exception map:** trigger, response, communication, recovery, and stop condition.
4. **Delivery and handoff verification:** result format, channel, quality check, recipient, verification evidence, and failed-handoff path.
5. **Pilot offer:** manual service description, participant terms, timing, obligations, and decided commercial terms.
6. **Evidence ledger and decision rules:** observed results, reported outcomes, operator burden, unknowns, and the evidence that would continue, revise, or stop the pilot.
7. **Automation candidates:** tested step, proof of stability, risk and control, and the first step to consider after the evidence supports it.
8. **Authorization gates:** external actions that still require explicit approval in the invoking task.

## Quality gate

- The service promises one clear customer outcome with a defined trigger and boundary.
- Every step has an input, action, output, tool, owner, timing, completion evidence, and Proposed or Tested status.
- Tested steps cite an actual run, and their handoff verification is recorded separately from sending the result.
- Estimated timing is not presented as measured timing.
- Material exceptions have an owner, response, recovery or stop path, and customer communication when needed.
- The offer identifies the service as manual and states the terms required for an informed pilot.
- Planned results, interest, and hypothetical willingness to pay are not reported as pilot evidence.
- Automation follows service-specific evidence of stable, bounded work. No fixed paying-customer count is used as a universal gate.
- The skill output plans work only. Outreach, messages, charges, and live delivery require explicit authorization.
