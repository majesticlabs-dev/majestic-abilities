---
name: prose-reviser
description: Rewrite existing informational, workplace, technical, or general prose for clarity, natural rhythm, and author fidelity while preserving facts and uncertainty. Use when the user wants revised copy, including requests to rewrite, tighten, simplify, polish, humanize, make text less robotic, or make it more natural. Use copy-editor when findings are the primary deliverable, content-writer for new drafts, style-writer for measured voice-profile work, and direct-response-copy for commercial persuasion.
---

# Prose Reviser

Return a clearer version of existing prose without changing what the author knows, claims, or means.

## Boundary

Use this skill when the requested deliverable is revised prose.

- For a diagnosis with quoted findings and recommendations, use `copy-editor` when available.
- For drafting new long-form content from a topic, use `content-writer` when available.
- An ordinary style guide can constrain this revision. When measured compliance with a reusable voice profile is primary, use `style-writer` when available.
- For commercial copy whose persuasion strategy is in scope, use `direct-response-copy` when available.
- Do not add factual research, translation, or a new argument unless the user asks for that work explicitly.

The skill must remain useful by itself. Other skills are optional routing suggestions, not dependencies.

If a broad request such as "make this better" does not reveal whether the user wants revised copy or an editorial report, ask which deliverable they want. Do not silently choose.

A request to "humanize this" means improve naturalness while preserving the author's demonstrated voice. Detector evasion is not a writing-quality objective. If the user explicitly requests classifier bypass, state once that the revision targets writing quality rather than detector evasion, then proceed only with the useful revision work.

## Inputs

Use:

1. The source text.
2. Its purpose, audience, and genre, when known.
3. Facts, quotations, terms, actions, and formatting that must remain intact.
4. A supplied style or voice guide.
5. The requested scope and degree of change, if specified.

For a straightforward revision, proceed without an intake interview. Ask only when ambiguity could change meaning, obligations, tone, or the requested deliverable materially. For a long document, honor the requested selection; confirm scope before making substantial full-document changes when no scope is clear.

## Choose revision depth

Use the least invasive depth that fulfills the request:

- **Light touch:** Fix local clarity, grammar, awkwardness, and unnecessary wording. Preserve paragraph order and approximate length. Use for requests such as "polish," "clean up," or "lightly edit."
- **Standard:** Improve sentences and paragraphs, remove genuine repetition, and make moderate structural changes while preserving the document's scope and overall shape. Use for requests such as "rewrite," "tighten," "simplify," or "humanize."
- **Restructure:** Reorder, merge, cut, or rewrite substantially. Use only when the user requests it or confirms it after you explain why standard revision is insufficient.

When the request does not indicate depth, default to a light touch. Move to standard only when local fixes cannot fulfill the stated purpose without material structural change; ask before proceeding when that change could surprise the user.

Do not shorten text merely to demonstrate improvement. Preserve approximate length unless the user requests compression or redundant material interferes with the text's purpose.

For legal, medical, financial, safety, security, compliance, or public-commitment prose, default to a light touch unless the user clearly authorizes more. Preserve the substantive meaning of obligations, conditions, and warnings, and keep defined terms exact. Do not imply specialist validation; add an appropriate owner-review note when material wording changes.

## Instruction precedence

Apply guidance in this order:

1. Explicit user requirements for the deliverable, degree of change, and format.
2. Supplied legal, claims, terminology, accessibility, or formatting constraints.
3. Supplied style or voice guide.
4. Established project conventions.
5. The defaults in this skill.

When lower-priority guidance conflicts with a higher-priority constraint, follow the higher-priority constraint. If a requested style change would alter factual meaning, preserve the meaning and state the conflict briefly.

## Workflow

### 1. Lock factual anchors

Before rewriting, identify and preserve:

- names, dates, numbers, and technical terms
- quotations, citations, links, and attribution
- requirements, commitments, owners, and deadlines
- qualifications, uncertainty, exceptions, and warnings
- code, commands, identifiers, frontmatter, and structured data
- genuine opinions and first-person experiences already present

Treat direct quotations, code, commands, identifiers, links, and structured data as protected spans unless the user explicitly asks to edit them. Do not fix a quotation by changing its text.

Do not replace a vague claim with invented specificity. Absence of supplied evidence alone does not make a user-provided claim false or removable.

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

Apply only the changes permitted by the selected revision depth. A light touch does not authorize restructuring.

#### Meaning

Preserve the central point, evidence, constraints, uncertainty, and necessary examples. Remove only material that adds neither information nor a necessary relationship, navigation, accessibility, or emphasis function.

#### Structure

Lead with the request, result, decision, problem, or useful answer when context permits. Group related information, remove semantic repetition, and place support next to the claim it supports.

When the source requests action, surface any supplied owner, action, deadline, and completion condition. Flag missing operational details only when they block use. Never invent them.

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

Return the revised prose in the response by default. Write or edit a file only when the user requested a path or the surrounding task already establishes a target file.

Add a brief `Revision notes` section after the prose only when needed to:

- explain why the text was returned unchanged
- report a conflict between requested style and protected meaning
- identify a missing action detail that blocks use
- flag a material internal contradiction or an attribution that cannot be checked from supplied material
- state a safety blocker or recommend review by the appropriate owner

Preserve questionable claims in the prose unless the user authorizes factual changes. Do not silently delete, strengthen, or present them as verified.

Do not expose the internal audit, alternate drafts, full change log, or self-critique unless the user asks for it.

## Quality Gate

The revision is ready when:

- the requested improvement is visible without exceeding the selected revision depth
- no functional material was removed merely to shorten the text
- facts, uncertainty, attribution, and authorship are intact
- actions and consequences are operational when the genre requires them
- the prose sounds natural without fabricated personality
- no style metric or generic AI-tell rule overrode clarity or source evidence
