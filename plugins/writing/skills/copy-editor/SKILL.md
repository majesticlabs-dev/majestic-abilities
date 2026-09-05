---
name: copy-editor
description: "Use when reviewing existing prose and delivering editorial findings rather than revisions."
---

# Copy Editor

Review existing prose and explain the smallest changes that would make it more correct, clear, trustworthy, and fit for purpose. The default deliverable is an editorial report, not rewritten prose.

## Boundary

Use this skill when the user wants diagnosis and evidence.

- For a clean revised version without a full issue report, use `prose-reviser` when available.
- For new articles or guides, use `content-writer` when available.
- For conversion-oriented assets whose persuasion strategy is in scope, use `direct-response-copy` when available.

The skill must remain useful by itself. Other skills are optional routing suggestions, not dependencies.

Apply edits only when the user explicitly requests inline edits or a clean copy. If a broad request such as "make this better" does not reveal whether the user wants findings or revised copy, ask which deliverable they want. Do not silently choose.

## Inputs

Collect or infer document context, but never infer permission to edit or rewrite:

1. The document or passage to review.
2. Its audience, purpose, channel, and publication stakes.
3. The requested review depth: full report, quick scan, category focus, inline edits, or clean copy. When no mode is stated for an explicit review request, default to a full report.
4. Any supplied voice guide, style guide, terminology list, or claims policy.
5. Sections or structured material that must not change.

When the prose is in a project, inspect nearby documented conventions if available. Do not require a fixed file name or location. If no guide exists, use genre-appropriate conventions and label judgment calls as recommendations rather than violations.

## Workflow

### 1. Establish the editorial contract

State the document's apparent purpose, intended reader, and requested mode. Identify high-stakes areas such as legal language, health or financial claims, public commitments, security instructions, or attributed quotations.

Assess whether writing is the right communication medium. Recommend a conversation, demonstration, interface change, specialist review, or another medium when prose alone cannot resolve the reader's need or risk.

Do not claim subject-matter correctness beyond the available evidence. Mark claims for verification when necessary.

### 2. Resolve applicable guidance

Use this precedence:

1. Explicit user instructions.
2. Supplied legal, claims, terminology, accessibility, or formatting constraints.
3. Supplied voice or style guide.
4. Established project conventions.
5. Genre-appropriate defaults.

When rules conflict, protect factual meaning and higher-priority constraints. Report the conflict instead of choosing silently.

### 3. Review line by line

Check only categories relevant to the document:

- **Grammar and mechanics:** agreement, punctuation, spelling, capitalization, and number formatting.
- **Clarity:** unclear subjects, buried actions, ambiguity, jargon, and unnecessary complexity.
- **Specificity:** vague claims, missing owners, weak verbs, and unsupported praise.
- **Structure:** order, repetition, transitions, headings, paragraph jobs, and ending.
- **Attribution and evidence:** when verification is requested or required by the review stakes, verify quotations against a supplied or retrieved source; check citations, factual support, uncertainty, and claim size. Never verify from model recall. When verification is unavailable, flag the quotation or attribution instead of treating it as confirmed.
- **Voice and tone:** audience fit, register consistency, warmth, confidence, and supplied voice rules.
- **Style-guide compliance:** exact rule violations, terminology, formatting, accessibility, and channel conventions.

Treat so-called AI tells as contextual symptoms, not proof of authorship. Fix pattern clusters toward clarity and the supplied voice. Do not apply generic word lists, punctuation bans, forced fragments, or artificial sentence variation.

### 4. Prioritize findings

Use three levels:

- **High:** changes meaning, creates factual or legal risk, hides the required action, or violates an explicit constraint.
- **Medium:** materially harms comprehension, trust, structure, or audience fit.
- **Low:** optional consistency or polish with limited reader impact.

Quote the exact triggering text. Cite the applicable rule when one exists. Otherwise explain the reader-facing consequence.

### 5. Add an independent validation pass

After the first analysis, perform a separate cold-read pass without relying on the existing issue list. Check whether the opening, logic, requested action, quotations, and ending still create a problem when read as a whole.

For high-stakes copy, recommend independent review by the relevant subject-matter, legal, safety, accessibility, or brand owner. Do not present the same review repeated by the same agent as a genuinely independent second lens.

### 6. Produce the requested mode

#### Full report

Return:

```markdown
## Editorial report

**Document:** [name or description]
**Purpose and audience:** [brief statement]
**Overall assessment:** [one or two sentences]

### Findings

| Location | Exact text | Category | Severity | Finding and evidence | Recommended fix |
| --- | --- | --- | --- | --- | --- |
| | | | | | |

### Recurring patterns
- [pattern, count or scope, and consequence]

### Top priorities
1. [highest-impact change]
2. [next change]
3. [next change]

### Ambiguities, verification, or high-stakes review needs
- [unresolved rule, claim, source question, or owner-review requirement]

### Cold-read check
- [whole-document issue confirmed or cleared on the separate cold-read pass]
```

#### Quick scan

Return only the highest-impact findings, normally no more than five.

#### Category focus

Review only the requested categories and say what was not assessed.

#### Inline edits or clean copy

Apply only supported fixes. Preserve facts, quotations, links, code, frontmatter, and structured data. For legal, medical, financial, safety, security, compliance, or public-commitment prose, make only explicitly authorized light-touch edits, preserve the substantive meaning of obligations, conditions, and warnings, and keep defined terms exact. Do not imply specialist validation; recommend review by the appropriate owner when wording changes materially. Required owner-review notes remain visible even when the user requests copy only. Otherwise, summarize material changes after the edited text unless the user requested copy only.

## Quality Gate

The review is ready when:

- in modes that produce findings, each finding quotes the exact source text and cites a rule or concrete reader consequence
- severity reflects impact rather than preference
- factual uncertainty and guide conflicts are explicit
- repeated patterns are not inflated into duplicate findings
- recommendations and applied edits preserve facts, attribution, uncertainty, and authorial voice
- the cold-read pass is proportional to the requested depth and reported when the output includes findings
- high-stakes edits remain bounded and carry any necessary owner-review note
- the output mode matches the user's explicit request or the documented review default
