---
name: write-better
description: Rewrite existing informational, workplace, technical, or general prose for clarity, natural rhythm, and author fidelity while preserving facts and uncertainty. Use when asked to improve, tighten, simplify, polish, humanize this text, make writing less robotic, or make it more natural, and neither formal voice-profile compliance nor conversion strategy is primary; use style-writer for profile-led work and direct-response-copy for commercial persuasion.
---

# Write Better

Return a clearer version of existing prose without changing what the author knows, claims, or means.

## Boundary

Use this skill when the requested deliverable is revised prose.

- For a diagnosis with quoted findings and recommendations, use an editorial-review workflow.
- For drafting new long-form content from a topic, use a drafting workflow.
- For applying an existing measured voice profile, use a voice-matched workflow.
- Do not add factual research, translation, or a new argument unless the user asks for that work explicitly.

A request to "humanize this" means improve naturalness while preserving the author's demonstrated voice. Detector evasion is not a writing-quality objective. Never promise that prose will bypass or defeat a classifier.

## Inputs

Use:

1. The source text.
2. Its purpose, audience, and genre, when known.
3. Facts, quotations, terms, actions, and formatting that must remain intact.
4. A supplied style or voice guide.
5. The requested degree of change, if specified.

For a straightforward revision, proceed without an intake interview. Ask only when ambiguity could change meaning, obligations, or tone materially.

## Workflow

### 1. Lock factual anchors

Before rewriting, identify and preserve:

- names, dates, numbers, and technical terms
- quotations, citations, links, and attribution
- requirements, commitments, owners, and deadlines
- qualifications, uncertainty, exceptions, and warnings
- code, commands, identifiers, frontmatter, and structured data
- genuine opinions and first-person experiences already present

Do not replace a vague claim with invented specificity. Flag an unsupported claim instead of making it sound more credible.

### 2. Diagnose context and voice

Determine the genre, reader, relationship, and desired action. Observe the source's actual:

- formality and vocabulary
- sentence and paragraph tendencies
- confidence and hedging
- punctuation and transitions
- humor and meaningful irregularities

Respect a supplied guide. If no guide exists, preserve the source's defensible voice rather than imposing generic casualness.

Return the text unchanged when it already serves its purpose and no requested change would improve it.

### 3. Revise in ordered passes

#### Meaning

Preserve the central point, evidence, constraints, uncertainty, and necessary examples. Remove only material that does not change what the reader knows, decides, or does.

#### Structure

Lead with the request, result, decision, problem, or useful answer when context permits. Group related information, remove semantic repetition, and place support next to the claim it supports.

#### Language

Prefer concrete nouns, stable terminology, direct subjects, and active verbs when responsibility matters. Replace abstraction and promotional wording with observable information. Keep technical language when it is the precise term.

#### Rhetoric

Remove empty transitions, vague authority, fake depth, unsupported significance, automatic conclusions, and formulaic contrast when they add no reasoning. Do not flatten legitimate emphasis or persuasion that fits the genre.

#### Rhythm and formatting

Fix monotonous or obviously manufactured patterns. Use sentence length, fragments, punctuation, headings, lists, and tables only when they serve the information and supplied style. Do not enforce universal punctuation or vocabulary bans.

### 4. Run a naturalness pass

Diagnose clusters rather than isolated tokens. Mechanical prose may show several of these together:

- repeated sentence shapes
- uniform paragraph lengths
- paraphrase chains
- generic openings and conclusions
- abstract praise without evidence
- transitions that announce instead of connect
- every paragraph ending with a slogan or punch line

Repair the underlying meaning or structure. Do not manufacture opinions, anecdotes, caveats, fragments, quirks, named examples, slang, or personal details to signal human authorship. Preserve intentional irregularity when it belongs to the author.

### 5. Validate the revision

Compare the revision with the locked anchors:

- Every fact, number, quote, link, and attribution still means the same thing.
- No uncertainty became certainty.
- No action, deadline, warning, or exception disappeared.
- No new experience, endorsement, source, or claim appeared.
- Tone and directness fit the reader and genre.
- The ending stops when the work is complete.

## Output

Return the revised prose by default. Do not expose the internal audit, alternate drafts, change log, or self-critique unless the user asks for it.

When a requested change would alter meaning or cannot be made safely, preserve the text and state the blocker briefly.

## Quality Gate

The revision is ready when:

- the main point is easy to find
- every retained sentence contributes information or necessary relationship work
- facts, uncertainty, attribution, and authorship are intact
- actions and consequences are operational when the genre requires them
- the prose sounds natural without fabricated personality
- no style metric or generic AI-tell rule overrode clarity or source evidence
