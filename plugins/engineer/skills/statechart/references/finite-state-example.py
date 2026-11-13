#!/usr/bin/env python3
"""Executable example: finite approval flow, not a production-flow verifier.

Run with Python 3.10+:
  python3 finite-state-example.py
  python3 finite-state-example.py --broken

The broken variant permits payment before approval and must exit 1.
Output is JSON containing evidence and Mermaid source. No files are changed.
"""

import argparse
from collections import deque
from dataclasses import dataclass
import json
import platform


@dataclass(frozen=True)
class State:
    phase: str
    approved: bool


INITIAL = (State("review", False),)
TERMINAL = {"paid", "cancelled"}


def successors(state, broken):
    if state.phase == "review":
        yield "Approve request", State("approved", True)
        yield "Cancel request", State("cancelled", False)
    if state.phase == "approved" or (broken and state.phase == "review"):
        yield "Pay request", State("paid", state.approved)


def violations(state):
    if state.phase == "paid" and not state.approved:
        yield "PaymentRequiresApproval"


def describe(state):
    return {"phase": state.phase, "approved": state.approved}


def explore(broken):
    queue = deque(INITIAL)
    predecessor = {state: None for state in INITIAL}
    transitions = []
    findings = {}
    unsafe = {}
    while queue:
        state = queue.popleft()
        problems = list(violations(state))
        outgoing = list(successors(state, broken))
        if not outgoing and state.phase not in TERMINAL:
            problems.append("NoUnexpectedDeadlock")
        if problems:
            unsafe[state] = problems
        for rule in problems:
            if rule not in findings:
                findings[rule] = state
        for action, target in outgoing:
            transitions.append((state, action, target))
            if target not in predecessor:
                predecessor[target] = (state, action)
                queue.append(target)

    traces = {}
    for rule, target in findings.items():
        steps = []
        current = target
        while predecessor[current] is not None:
            previous, action = predecessor[current]
            steps.append({"action": action, "state": describe(current)})
            current = previous
        steps.append({"action": "Start", "state": describe(current)})
        traces[rule] = list(reversed(steps))

    # Each concrete state has its own node; no projection hides approval status.
    identifiers = {state: f"s{index}" for index, state in enumerate(predecessor)}
    chart = ["stateDiagram-v2"]
    for state, identifier in identifiers.items():
        approval = "approved" if state.approved else "not approved"
        chart.append(f'    state "{state.phase.title()} ({approval})" as {identifier}')
    for state in INITIAL:
        chart.append(f"    [*] --> {identifiers[state]}")
    for source, action, target in transitions:
        chart.append(f"    {identifiers[source]} --> {identifiers[target]}: {action}")
    for state, identifier in identifiers.items():
        if state.phase in TERMINAL:
            chart.append(f"    {identifier} --> [*]")
        if state in unsafe:
            chart.extend([
                f"    note right of {identifier}",
                "        Violates: " + ", ".join(unsafe[state]),
                "    end note",
            ])

    return {
        "model": "Approval flow example (not linked to product code)",
        "python": platform.python_version(),
        "variant": "broken payment guard" if broken else "baseline",
        "complete": True,
        "status": "violated" if findings else "passed",
        "properties": {
            "PaymentRequiresApproval": "Payment requires prior approval",
            "NoUnexpectedDeadlock": "Only paid or cancelled may have no next action",
        },
        "bounds": "One request; review, approved, paid or cancelled; approval boolean",
        "assumptions": "Each action is atomic; approval cannot be revoked",
        "exclusions": "Persistence, concurrent actors, retries, liveness, implementation fidelity",
        "states": len(predecessor),
        "transitions": len(transitions),
        "shortest_safety_traces": traces,
        "mermaid": "\n".join(chart) + "\n",
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--broken", action="store_true")
    args = parser.parse_args()
    result = explore(args.broken)
    print(json.dumps(result, indent=2))
    return 1 if result["status"] == "violated" else 0


if __name__ == "__main__":
    raise SystemExit(main())
