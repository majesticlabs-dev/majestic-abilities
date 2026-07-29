---
name: headline-generator
description: Generate multiple fact-bound news headlines, press-release headlines, feature headlines, and pitch subject lines from supplied evidence, then recommend the strongest candidate. Use when a story, launch, data point, press pitch, or existing flat headline needs a deliberate candidate sprint, not a complete asset.
---

# Headline Generator

Find the strongest true tension in supplied facts and express it through materially different headline or subject-line candidates.

## Boundary

Use this skill when the deliverable is a candidate set plus a recommended option. It does not write the complete asset.

A complete landing page, sales email, or ad belongs to a direct-response workflow. A complete general article belongs to a drafting workflow. Those workflows may create a working title, but use this skill when the user wants deliberate headline exploration across distinct factual angles.

## Inputs

Collect:

1. The subject, event, or change in one plain sentence.
2. Actors, affected groups, verified numbers, dates, and named entities.
3. Stakes, consequences, costs, savings, limitations, and supplied proof.
4. What the facts contradict, reverse, reveal, or put on a deadline.
5. Requested formats and channel constraints.
6. Audience, outlet, voice, claim limits, and words that must appear or remain absent.

If the facts cannot support a useful headline, ask for the missing evidence or say the story is not ready. Do not invent a stronger story.

## Workflow

### 1. Lay out the factual materials

Create a private fact sheet:

| Fact or term | Source or status | Allowed claim | Limitation |
| --- | --- | --- | --- |
| | | | |

Treat this as the candidate vocabulary. A headline may compress supplied meaning, but it may not create a quotation, causal claim, comparison, or certainty the evidence does not support.

### 2. Find the charge

Identify two to four true tensions, such as:

- expected result versus actual result
- promise versus supported cost
- belief versus measured finding
- small cause versus large consequence
- deadline versus affected group
- old state versus verified change
- two concrete ideas that become meaningful together

State each charge in plain language before styling it. If no tension is supported, lead with the strongest useful fact instead.

### 3. Generate distinct directions

Explore only moves that fit the facts:

- consequence rather than internal procedure
- concrete image rather than abstraction
- verified number as the lead
- setup followed by a truthful turn
- reader relevance without unsupported assumptions
- a precise name for a demonstrated pattern
- an open question whose subject remains clear
- a channel-appropriate spoken register
- sound or rhythm that does not obscure meaning
- restrained wording that sizes the claim to proof

Generate 10 to 20 raw candidates when the user wants a full sprint. Vary what leads: actor, verb, number, consequence, affected person, deadline, or image. Do not merely replace synonyms in one sentence.

### 4. Apply the evidence gate

For every keeper:

- trace each claim to the fact sheet
- distinguish quotation from editorial compression
- remove unsupported causation and superlatives
- preserve relevant timeframe and scope
- avoid blind teases that hide the subject
- avoid a full giveaway only when a legitimate question remains
- flag terms that require legal, factual, or stakeholder approval

Use the empirical findings in [evidence.md](references/evidence.md) as weak priors, not universal rules. Audience, format, trust, and evidence outrank click-through generalizations.

### 5. Tighten for format

Cut words until further cutting would remove truth, subject, or necessary context. Put strong concrete words near the edges. Read each candidate aloud.

Format rules:

- **News headline:** Present tense when appropriate; actor and change clear; strongest true fact first.
- **Press-release headline:** Organization may be the actor, but the news must remain legible to an outside reader.
- **Feature headline:** May create curiosity, but must not misrepresent or conceal the subject completely.
- **Pitch subject line:** Follow the supplied inbox limit; show character count; lead with the peg, finding, or relevance.

Do not generate news-style candidates when the requested format would not benefit from them.

## Output

Lead with the candidates. Group them by requested format.

For each format, return three to five keepers:

```markdown
- **[Candidate]** ([character count when relevant])
  - Angle: [charge and generation move]
  - Support: [fact or evidence that permits the wording]
```

End each group with:

```markdown
**Pick:** [candidate]
**Why:** [one sentence connecting truth, audience, and format]
```

Then list any fact-check or approval blockers. Do not route to nonexistent sibling skills.

## Quality Gate

The candidate set is ready when:

- every claim is traceable to supplied or verified facts
- candidates explore materially different angles
- claim size matches proof
- the subject remains identifiable
- quotations and editorial compression are distinguished
- subject lines include character counts
- the recommendation explains audience and format fit, not merely punchiness
