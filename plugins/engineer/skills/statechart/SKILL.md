---
name: statechart
description: "Model a bounded stateful flow, check its safety rules, and explain reachable behavior or counterexamples with a Mermaid statechart. Use for checked user flows, retry or concurrency paths, and bugs expressed as state transitions."
---

# Checked Statecharts

Turn a stateful user flow, protocol, or subsystem into a reviewable finite model, checked safety properties, and a diagram grounded in the results. Do not require a specific agent harness, renderer, external service, or additional runtime beyond the chosen checker. A small Python standard-library model is sufficient for finite-state exploration.

## Boundary

Use this workflow when the user wants rules checked as well as transitions explained. For a simple visual explanation, draw the evidence-supported flow without introducing a checker and label it unverified. A diagram alone is not model checking.

Work from the supplied requirements and current source. Keep temporary runs outside the checkout or in the project's ignored evidence directory. Do not install tools, access production, or change product code without the applicable authority. Leave reusable project resources only when requested.

## 1. Define the flow and rules

Select the named flow, or prioritize a user-important path using supplied goals and evidence of risk. Identify the initial conditions, actors, user-visible states, events, guards, and terminal outcomes. Include rejection, cancellation, retries, persistence, and concurrent actions only where relevant evidence supports them.

When recovering a lifecycle from existing code, inventory the relevant state before choosing model variables:

- Look past the status field to flags, timestamps, queued work, and external systems that hold their own view of the entity. Trace what observes expiry and what can still act after deletion.
- Trace each path that changes or reinterprets that state. Record its trigger, actual guard, writes or side effects, transaction or lock boundary, and source location. Include handlers, workers, callbacks, and scheduled jobs where they affect the flow.
- Account for environment behavior supported by the integration, such as duplicate or out-of-order delivery, crashes between writes, or a retry after a timeout when the original operation may have succeeded.

Write each safety rule in plain language, with its requirement source, before encoding its predicate. Distinguish intended behavior from observed implementation behavior and unresolved expectations. Ask only when an unknown expectation changes the result.

Map each variable and action to its requirement or source symbol. State what is atomic and why. Model independently interleavable operations as separate steps, and represent relevant environment outcomes as alternative transitions. Specify finite domains and initial states. A screen-only model cannot check a rule about stored data it does not represent.

## 2. Execute a finite-state check

Use a project-supported checker when available; otherwise a small explicit Python model can enumerate reachable states using the standard library. The runnable [finite-state example](references/finite-state-example.py) demonstrates this approach, not a universal runner or a model of the user's system. Adapt states, actions, and properties to actual evidence rather than treating the example's contract as a requirement.

When the project uses TLC or the user requests TLA+, read the [TLA+ and TLC reference](references/tla-tlc.md).

From this skill's directory, the example can be exercised with:

```sh
python3 references/finite-state-example.py
python3 references/finite-state-example.py --broken
```

The baseline exits 0 after exploring four states and three transitions. The broken variant exits 1 after exploring five states and four transitions, reporting `PaymentRequiresApproval` with the shortest path `Start → Pay request`. Each command prints JSON containing results and Mermaid source; neither changes files. This is an illustrative model, not implementation verification.

The checker must:

1. Start from every declared initial state.
2. Evaluate every named invariant on each discovered state, including initial and terminal states.
3. Enumerate every enabled successor, deduplicating by the complete modeled state, not diagram labels.
4. Retain predecessor/action records for counterexample reconstruction. A breadth-first search gives a shortest safety counterexample by modeled transition count, not elapsed time.
5. Distinguish legitimate terminal states from unintended deadlocks. Do not disable deadlock detection globally to excuse one terminal outcome.
6. Report complete only when the reachable-state worklist is exhausted. Record counts, bounds, checked properties, command, source identity, and tool version.

An infinite domain, truncated search, timeout, invalid model, or missing tool leaves affected checks incomplete or blocked, not passing. Prefer bounded domains justified by the question; disclose that the result says nothing about larger domains. Do not claim liveness or fairness from safety checks or absence of deadlock. A progress claim needs an appropriate temporal check and explicit environment/fairness assumptions.

Demonstrate sensitivity with a disposable broken variant that violates a named rule, then restore and rerun the baseline. Preserve genuine baseline violations. Model mutation validates the model check, not automatic detection of an implementation change.

## 3. Build the chart from checked results

Produce Mermaid `stateDiagram-v2` text and retain the model and run output alongside it. Translate model states into reader-facing labels and actions into meaningful events. Use stable diagram identifiers separately from labels. Use nesting or parallel regions only when supported by the model and useful to the reader.

Derive arrows from explored transitions. Distinguish a full reachable graph, an explicitly simplified projection, and a counterexample-only chart. If the checker stops at its first violation, do not present its partial graph as the complete flow or imply other properties passed.

When simplifying:

- Preserve the initial states, relevant terminal outcomes, and every step of the counterexample being explained.
- Keep distinctions needed to explain guards, different violations, or unsafe interleavings.
- Do not merge states in a way that creates an apparent executable path unsupported by concrete states. If a projection can combine incompatible paths, disclose that limit and show the concrete counterexample separately.
- Mark a merged node as potentially unsafe when only some underlying states violate the rule; never label the whole node safe.
- Disclose omitted transitions and hidden state changes. Do not silently suppress recovery or failure behavior to make a happy-path chart.

Use the smallest chart that answers the question; split by flow when needed rather than hiding the bug. No fixed chart-size threshold establishes correctness.

## 4. Interpret and reproduce

For each discovered violation, report the rule, its plain-language meaning, the initial conditions, and the numbered action/state trace. Claim a shortest path only when the search method supports it, and qualify it as shortest within the model. A deadlock is a separate finding unless the contract makes that state a legitimate terminal outcome.

For code-backed models, replay each reported bug path through an actual public interface or regression reproduction when the environment permits. If it does not occur, investigate modeling assumptions before asserting a product defect. Report source review, model checking, and implementation reproduction separately.

## Deliver

Return:

- the flow, requirement sources, and model-to-code map
- Mermaid source in a `mermaid` code block, plus a short explanation
- properties checked, result, bounds, assumptions, exclusions, and exploration counts
- counterexamples and their implementation reproduction status
- exact rerun commands, tool version, model/configuration paths, and evidence location
- incomplete, blocked, failed, and unrun work separately

Inspect rendered output only when a renderer is available or requested. Do not install a renderer merely to display Mermaid source. Report an unrendered chart honestly. A passing model check is evidence about the bounded model, not proof of the implementation or the entire product.

## Tool references

- [Mermaid state-diagram syntax](https://mermaid.js.org/syntax/stateDiagram.html): labels, transitions, terminal states, notes, and parallel regions.
- [Python deque](https://docs.python.org/3/library/collections.html#collections.deque): the FIFO worklist used by the executable example.
