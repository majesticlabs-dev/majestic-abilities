---
name: minto-pyramid
description: Restructure a draft or idea using the Minto Pyramid Principle into one governing answer, two to four supporting arguments, and matched evidence. Use when a memo, proposal, presentation, or complex explanation has a buried conclusion, overlapping sections, or weak support.
---

# Minto Pyramid

Make the governing answer and its support visible before polishing voice or prose.

## Boundary

Use this skill for argument structure, not factual validation or stylistic imitation.

- Use `style-writer` after the structure is sound and a voice profile should be applied.
- Use `reasoning-verifier` when the main question is whether a completed conclusion follows from its requirements and evidence.

## Inputs

Identify:

1. The document, draft, or raw idea.
2. The intended audience.
3. The decision, understanding, or action the document should produce.
4. Available evidence and known gaps.
5. Format or length constraints.

Ask one concise question when the target or intended decision is genuinely ambiguous.

## Workflow

### 1. Extract the governing answer

State the main answer in one complete sentence. It should answer the audience's likely question, not merely name the topic.

If the source does not support a clear answer, label the missing decision rather than inventing one.

### 2. Group supporting arguments

Create two to four full-sentence arguments that jointly support the answer.

Test whether they are:

- distinct enough to avoid double counting
- collectively sufficient for the audience's decision
- ordered by audience logic rather than source order
- expressed at the same level of abstraction

Treat MECE as a diagnostic goal, not a reason to force a false partition. Report unavoidable overlap or missing coverage.

### 3. Match evidence

Attach the strongest relevant evidence to each argument. Separate:

- supplied evidence
- verified external evidence
- unsupported claim
- evidence still needed

Do not bundle unrelated facts merely to fill a branch.

### 4. Choose the logical order

Select the structure that fits the audience:

- importance order
- chronological order
- process order
- structural decomposition
- problem, cause, solution

State why the order helps the audience understand or decide.

### 5. Diagnose the source

Identify:

- buried, missing, or competing answers
- overlapping arguments
- unsupported branches
- dead weight
- evidence placed under the wrong claim
- sections to merge, split, move, or cut

### 6. Build the restructuring plan

Specify:

- replacement opener
- section sequence
- argument for each section
- evidence assigned to each section
- cuts and merges
- unresolved evidence gaps
- closing action or implication

## Output

```markdown
# Minto Pyramid Review

## Governing Answer
[One sentence]

## Pyramid
1. [Supporting argument]
   - Evidence: ...
   - Status: supported | partial | missing
2. ...

## Structural Diagnosis
- ...

## Recommended Order
[Order and rationale]

## Restructuring Plan
1. ...

## Evidence Gaps
- Claim: ...
  Evidence needed: ...
```

Save the review only when the user requests a file or provides an output path.

## Quality Gate

- The answer is one sentence and responds to the audience's actual question.
- Arguments are full sentences at a consistent level.
- Evidence is matched to claims and labeled honestly.
- Overlap and missing coverage are explicit.
- The restructuring plan tells the writer what to move, cut, merge, and support.
