# Traceable Customer Interview Round

Use this workflow when several customer interviews must support one product decision and the team needs a durable evidence trail. Use the lighter prompts in [discovery-methods.md](discovery-methods.md) when one conversation or a small informal study is sufficient.

This workflow supports discovery. It does not prove market demand, estimate prevalence from a convenience sample, or replace an executable validation test.

## Artifact model

Keep the round in one working document or a small folder. Let the user choose the location and filenames. Preserve these relationships even when the storage format changes:

```text
research decision
  -> goals (G)
    -> hypotheses (H)
      -> interview questions (Q)
        -> participant records (P)
          -> findings (F)
```

Use stable identifiers so later changes do not break citations. Do not reuse an identifier after deletion. Record important changes in a dated log.

A practical folder can contain:

```text
research-round.md
interviews/
  <date>-<participant-label>.md
findings.md
```

Do not put sensitive participant data in filenames. Collect only the personal data required for the research decision.

## 1. Define the research contract

Record:

- the product decision this round must inform
- the target user, buyer, situation, and relevant segments
- what the team already knows and what remains uncertain
- participant inclusion and exclusion rules
- consent, recording, retention, access, and deletion requirements
- the decision owner and the date when the evidence will be reviewed

Do not start with a broad goal such as “understand customers.” State what could change after the research.

## 2. Write goal questions

A goal is a question the research must help the team answer. It is not necessarily a question to ask a participant.

Use this register:

| ID | Goal question | Product decision affected | Evidence needed | Status |
| --- | --- | --- | --- | --- |
| G1 | | | | Open |

A useful goal:

- concerns a real product, audience, positioning, pricing, or workflow decision
- can be informed by recent behavior and concrete examples
- names the user or buyer role when roles differ
- does not ask participants to make the product decision for the team

Remove goals whose answers cannot change a decision. Keep exploratory goals only when the possible decision effect is clear.

## 3. Record current hypotheses

Write the team’s current best explanation before interviews begin. This makes confirmation bias visible.

| ID | Goal | Current hypothesis | Evidence for | Evidence against | Decision consequence | Status |
| --- | --- | --- | --- | --- | --- | --- |
| H1 | G1 | | | | | Untested |

A useful hypothesis:

- states one belief in specific terms
- can be supported, narrowed, or contradicted by customer-life evidence
- belongs to the decision owner or team, not to the agent
- changes a decision when wrong
- keeps unknown values and segment limits visible

Do not invent a hypothesis to complete the table. Record an open goal when the team has no current belief.

## 4. Build the interview guide

Map each planned question to a hypothesis or an explicitly exploratory goal.

| ID | Goal or hypothesis | Question | Evidence sought | Follow-up probes |
| --- | --- | --- | --- | --- |
| Q1 | H1 | | | |

Accept a question only when it:

1. uses neutral language and does not reveal the preferred answer
2. asks for a recent event, action, choice, workaround, or result
3. can produce a specific fact or story
4. leaves room for an unexpected answer
5. produces evidence that can be recorded against its goal or hypothesis

Prefer prompts such as:

- “Tell me about the last time this happened.”
- “What started it?”
- “What did you do next?”
- “Who else took part in the decision?”
- “What did you try before this?”
- “What did that cost in time, money, risk, or attention?”
- “What changed after the decision?”

Do not ask whether the participant likes a proposed feature or would buy an imagined product. If concept feedback is required, show a clear research prototype, state that it is not an available product, and ask the participant to complete or evaluate a realistic task.

Order the guide from context and recent behavior to workarounds, triggers, search, choice, result, and reflection. Keep standing probes separate from the main questions.

## 5. Create one record per interview

Create the participant record soon after each real conversation. Separate what the participant said from the researcher’s interpretation.

```markdown
# Participant P1

## Context
- Date:
- Relevant role and segment:
- Source type: direct participant | intermediary | expert
- Consent and recording status:
- Researcher:

## Answers
### Q1
- Evidence:
- Verbatim words:
- Research note:

## Unasked or unanswered questions
- Q#:

## Addenda
- Relevant evidence that did not fit a planned question:

## Limitations
- Recall, role, sample, access, or interpretation limits:
```

Apply these rules:

- Preserve important wording exactly and mark paraphrases.
- Distinguish `unasked` from `asked but unanswered`.
- Do not infer an answer from silence or from another answer.
- Mark secondhand claims and expert generalizations. Do not count them as direct customer behavior.
- Keep surprising off-guide evidence in Addenda.
- Do not update the research conclusion inside one participant record.

## 6. Synthesize across records

Cite participant IDs for every material finding. Use exact counts with a denominator when counting responses, and state when a question was not asked of everyone.

Use these evidence states:

| State | Meaning |
| --- | --- |
| Untested | No relevant interview evidence exists. |
| Watch | One relevant example or a weak signal needs more evidence. |
| Directional | Several records point the same way, but sample or segment limits remain material. |
| Supported | Repeated evidence survives contradiction and segment checks for this research decision. |
| Contradicted | Available evidence conflicts with the current hypothesis. |

Interview evidence never becomes market prevalence or demand proof by label alone.

For each hypothesis:

1. collect supporting, conflicting, and missing evidence
2. inspect negative cases and differences by role, situation, and segment
3. decide whether to retain, narrow, split, replace, or contradict the hypothesis
4. state the evidence that would change the new assessment
5. log the change without deleting the earlier state

Do not average incompatible segments. Split the finding or report that no stable pattern exists. A single unusual observation can create a new hypothesis, but it does not establish a pattern.

Use a finding register:

| ID | Goals or hypotheses | Finding | State | Evidence | Counterevidence | Limitations | Decision effect |
| --- | --- | --- | --- | --- | --- | --- | --- |
| F1 | H1 | | | P1, P3 | P2 | | |

## 7. Decide whether to continue, stop, or change direction

Choose one round status:

- **Continue:** a material hypothesis is unresolved, important segments are missing, or recent interviews still add decision-relevant evidence.
- **Stop:** the current evidence is sufficient for the stated discovery decision and another similar interview is unlikely to change it.
- **Change direction:** recruitment, segmentation, goals, or questions do not match the decision, or the interviews expose a different material uncertainty.

Do not use a universal interview count. State the reason, the next participants or evidence needed, and the next review date.

Stopping discovery does not mean the product is validated. Hand the riskiest remaining assumption to an executable validation test when demand or commitment evidence is required.

## 8. Produce the round report

Return a report that can stand without the interview session history:

1. **Decision and research question**
2. **Method, participants, consent limits, and sample limits**
3. **Findings with states and participant citations**
4. **Contradictions, negative cases, and segment differences**
5. **Customer language and Jobs-to-be-Done evidence**
6. **Hypotheses retained, changed, split, or contradicted**
7. **Unknowns and evidence gaps**
8. **Round status: continue, stop, or change direction**
9. **Next decision or evidence step**

Keep implications separate from observations. Do not turn an interview finding directly into a requirement, market-size claim, positioning promise, or product verdict.

## Quality gate

- Every planned question maps to a goal or hypothesis.
- Questions ask about behavior and do not lead the participant.
- Every interview has a separate record with provenance and limitations.
- Material findings cite participant records and include counterevidence.
- Counts use the correct denominator.
- Contradictions and segment differences remain visible.
- Stable identifiers and important changes remain traceable.
- The report states what interviews cannot establish.
- The round status includes a reason and next evidence step.
