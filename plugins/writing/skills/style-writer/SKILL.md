---
name: style-writer
description: Draft and revise prose against an existing voice or Style DNA profile while preserving facts and readability. Use when writing in an established personal or brand voice, applying a voice guide, or checking a draft against measured style constraints.
---

# Style Writer

Apply an existing voice profile to new prose. Treat measured style as a set of guardrails, not proof that a draft authentically reproduces a person.

## Boundary

Use this skill to write from an existing profile.

- To define a desired organizational voice, use `brand-voice`.
- To capture an existing voice from samples, use `voice-dna-kit`.
- To produce a deep measurement report, use `style-forensics`.

Do not fabricate facts, quotations, experiences, endorsements, or authorship claims to make a draft resemble the source voice.

## Inputs

Require:

1. A voice guide, `voice-dna.md`, or `style-dna.md` file.
2. The writing brief, audience, channel, purpose, and desired action.
3. Source material for factual claims.
4. Target length and required structure, when relevant.
5. Any strict terminology, legal, or formatting constraints.

If no profile exists, stop and request one or route to the appropriate profile-building skill. Do not infer a reusable voice from a single short excerpt while drafting.

## Workflow

### 1. Select the correct register

Extract:

- stable voice rules
- context-specific tone
- sentence and paragraph tendencies
- punctuation rules
- signature devices and their frequency
- vocabulary preferences
- strict bans
- confidence limitations in the profile

When multiple registers exist, choose the one matching the audience and stakes. State the selection briefly.

### 2. Build an evidence-safe plan

Define:

- the central claim or purpose
- the audience's relevant context
- the required evidence and supplied sources
- the section or paragraph sequence
- the intended opening and closing behavior
- where signature devices would be natural

Do not add named companies, statistics, quotations, or anecdotes merely to imitate a pattern. Use supplied evidence or research facts that need to be current.

Present the plan first only when the user asks for approval, the piece is high stakes, or the brief leaves material strategic choices unresolved.

### 3. Draft for meaning first

Write a complete draft that:

- fulfills the brief
- preserves supplied facts and attribution
- uses the selected register
- follows the profile's structural tendencies
- uses signature devices at natural rather than mechanical frequency
- avoids strict bans

Never sacrifice clarity to hit a metric.

### 4. Measure the draft

Compare the draft with the profile where targets exist:

- average sentence length and distribution
- short-sentence ratio
- paragraph length
- punctuation rates
- pronoun and contraction rates
- hedging
- recurring openers and signature devices
- banned phrases and structures

Report only applicable constraints:

| Constraint | Target | Actual | Disposition |
| --- | --- | --- | --- |
| [profile rule or tendency] | [range, ban, or tendency] | [measured or observed result] | Fix, retain with reason, or not applicable |

Use `not applicable` when the draft is too short, the profile has no usable target, or the feature does not belong to the selected register. Use `retain with reason` when accuracy, readability, genre, or evidence justifies a deviation.

Handle zero targets explicitly:

- If the profile marks an item as prohibited, the allowed count is exactly zero.
- If a measured tendency happened to be zero but is not prohibited, report the new count instead of dividing by zero or declaring automatic failure.
- For nonzero targets, use ranges or tolerances appropriate to the draft length.

Do not calculate a single "voice accuracy" score. A weighted average creates false precision and can hide a serious violation.

### 4a. Check for generic AI-shaped prose

Run a separate editorial check for patterns that can make otherwise correct prose feel generic:

- uniform sentence lengths or rectangular paragraphs
- repeated previews, recaps, or signposted conclusions
- abstract claims without a supplied concrete detail
- automatic both-sides framing or tidy optimism
- repeated contrast frames such as "not X, but Y"
- stock phrases, prompt residue, or unnecessary self-commentary
- anecdotes that are too neat to support the supplied evidence

Treat these as review signals, not universal prohibitions. Do not ban em dashes, Oxford commas, semicolons, contractions, or any other feature without evidence from the selected voice profile and register. Do not add facts, names, numbers, anecdotes, or awkward substitutions to make prose appear more human. If a concrete detail is needed, request it or use one from the source material.

### 5. Revise selectively

Fix the largest meaningful deviations first:

1. wrong register or stance
2. factual or attribution problems
3. banned patterns
4. generic AI-shaped patterns that conflict with the profile or brief
5. structure and paragraph rhythm
6. sentence rhythm and punctuation
7. vocabulary and minor frequency differences

Re-measure only the passages affected. Stop when further metric chasing would make the prose worse.

### 6. Return the result

Provide:

1. The draft
2. Register used
3. Target-versus-actual audit table for applicable constraints
4. Material profile constraints followed
5. Remaining deviations and why they were retained
6. Factual assumptions or unsupported claims requiring review

Save the draft only when the user requested a file or confirms a proposed path.

## Quality Gate

The draft is ready when:

- it accomplishes the brief without invented evidence
- the selected register is consistent
- strict bans are absent
- high-signal style patterns are recognizable but not forced
- generic AI-shaped patterns were reviewed without applying universal bans
- facts and attribution remain intact
- the audit table distinguishes fixes, justified deviations, and non-applicable constraints
- deviations are disclosed when readability or accuracy required them
- the prose does not copy distinctive source wording unnecessarily
