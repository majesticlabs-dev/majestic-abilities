# Optional formal verification

Use this branch when a concrete proof gap involves event ordering, retries, state transitions, or a property that example-based tests do not establish. Formal methods supplement the verifier's real-interface evidence; they are not a prerequisite for ordinary verification.

## Select the property and method

Start with the requested subsystem or observed risk. State the intended property, its requirement source, and the user harm if it fails. Do not select a target merely because it is easy to model.

| Question | Suitable method |
| --- | --- |
| Can events interleave into a forbidden state? | Exhaustive exploration of a finite transition system |
| Does code satisfy a property for inputs within stated bounds? | A compatible code-level verifier or bounded solver |
| Must a property hold for arbitrary sizes? | A proof with explicit assumptions, when suitable tooling exists |

Prefer the project's existing tools. A small Python standard-library model can explore a finite transition system without an additional runtime or package. A visited-state search is exhaustive only when every reachable state and enabled transition in the declared finite model is explored. Sampling, an interrupted search, or an arbitrary depth cutoff is not exhaustive verification.

If no suitable verifier is available, report the formal check blocked. Generated tests against real code remain useful, but do not relabel them as formal proof. Disclose proposed dependencies before installing them.

## Preserve correspondence to the implementation

Record:

- model variables and the source fields or external facts they represent
- actions and their source functions, transaction boundaries, or event handlers
- initial states, guards, nondeterministic outcomes, and assumptions about the environment
- bounds on actors, retries, queue length, and data domains
- safety invariants, and any progress properties with their fairness assumptions
- excluded behavior and the revision plus relevant working changes inspected

Treat a step as atomic only when the implementation supports that claim. Split reads, decisions, and writes when another actor can intervene. Include failures or retries when they affect the property. A model copied from implementation logic still needs independently sourced expectations.

Separate subsystem checks when their contracts and rerun triggers are independent. When correctness crosses subsystem boundaries, retain a joint model or explicit composition assumptions. One skill per subsystem is not a default coverage rule.

## Make the check capable of failing

In a disposable copy, introduce a known defect relevant to each checked property, such as removing a guard or reordering an operation. Run the documented check and retain the counterexample. Restore the baseline and rerun it. Do not alter the expected property to accommodate a failure.

A mutation of the model proves that the model's check can fail; it does not prove that a changed implementation is checked. For a hand model, also trace the mutation to the corresponding code and demonstrate the mismatch through a real regression reproduction or an explicit model-to-code review. Report that review separately from automated detection. Never claim that a standalone model automatically catches source changes.

Report existing failures without changing product code during a verification-only task. Translate a counterexample into concrete actions and observable states. Replay it against the implementation where possible; if it does not reproduce, investigate the model's fidelity before calling it a product defect.

## Leave a rerunnable project contract

Keep the primary project `verifier` usable without optional dependencies. Add owned formal resources and, only when useful, separately named subsystem verification skills in the project's configured local skill directory. Preserve existing resources and authority boundaries.

For each check, record the exact command, tool version, inputs, expected failure signal, assumptions, checked properties, model-to-code map, and last confirmed source revision. Explain when to rerun it and when source changes require reviewing model fidelity. Advance the sync revision only after that review, not merely after a green model run.

Retain the model, configuration, completed-check output, state/transition counts when available, counterexamples, mutation evidence, and remaining limits. Distinguish verified properties, violations, tool failures, blocked checks, and unrun checks. A finite-state pass establishes only the stated properties of that model within its bounds; it does not prove the implementation or arbitrary sizes.
