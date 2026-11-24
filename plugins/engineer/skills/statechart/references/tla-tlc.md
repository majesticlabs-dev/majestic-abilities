# Checking a lifecycle with TLC

- Encode the extracted behavior as `Init` and named actions combined in `Next`. Keep source locations beside the actions. For a read-check-write sequence that can interleave, store the intermediate observation in model state so another actor can change the underlying data before the write. In PlusCal, place labels at the actual interleaving boundaries.
- In the `.cfg` file, select the specification and set finite constants that can exercise the relevant interactions. Include a type invariant for the represented state and separate invariants for the requirements. For a progress question, check a temporal property under fairness assumptions the implementation or environment actually supports. [TLC configuration](https://github.com/tlaplus/vscode-tlaplus/blob/master/resources/knowledgebase/tlc-config-files.md)
- Keep deadlock checking enabled. If an expected terminal outcome has no outgoing action, give that outcome an explicit self-loop guarded by its terminal predicate.

Use the project’s TLC command when available. With an available `tla2tools.jar` on a compatible Java runtime, run from the model directory, substituting the actual paths and module name. [TLA+ tools](https://github.com/tlaplus/tlaplus#use) · [TLC command-line options](https://github.com/tlaplus/tlaplus/blob/master/general/docs/current-tools.md#command-line-options)

```sh
java -jar /path/to/tla2tools.jar -config Lifecycle.cfg Lifecycle.tla
```

Record the generated and distinct state counts and whether exploration completed. Check that a known relevant intermediate state is reachable in the sensitivity run. A deliberately false invariant about that state should fail with a trace reaching it. For each real violation, map the action sequence back to the code and check its feasibility before attempting the implementation replay.
