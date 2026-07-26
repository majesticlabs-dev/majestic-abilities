# Writing Skills Category Audit

- **Date:** 2026-07-25
- **Repository:** `/Users/dpaluy/projects/ai/skills/majestic-skills/abilities`
- **Source repository:** `/Users/dpaluy/projects/ai/hermes-assets`
- **Target category:** `skills/writing`
- **Status:** Implemented on 2026-07-25; results and verification are recorded below.

### Repository Snapshots

The audit was performed against these exact snapshots:

| Repository | Branch | Commit | Working tree before this document |
| --- | --- | --- | --- |
| `majestic-skills/abilities` | `master` | `b24f753f8f9f5b1ccf5366e8974ec4abc86bcd8f` (`feat: route reasoning capabilities`) | Clean |
| `hermes-assets` | `main` | `af8c7f2e78f9383af5e85901f1f8c11d4287bcdf` (`daily sync 2026-07-25 04:30`) | Clean |

## Review Request

Review the proposed routing of 16 writing-related Hermes skills into the
Majestic Abilities `writing` category.

The central question is not whether each source contains useful writing advice.
It is whether the source defines a distinct, portable Agent Skill that belongs
in this repository, should enrich an existing skill, or should remain
profile-local or omitted.

The proposed outcome is:

- update 4 existing target skills
- add 5 new target skills after rewriting them for portability
- skip 7 sources as standalone target skills
- keep the existing `minto-pyramid` unchanged
- grow the category from 5 to 10 skills

An independent reviewer should return either:

- `APPROVED`, with any non-blocking observations; or
- `REVISE`, with specific findings tied to a source, target, or portfolio
  boundary.

## Executive Verdict

Do not bulk-copy the 16 sources.

The target already has a coherent voice pipeline. The highest-value additions
are missing drafting, rewriting, editorial-review, commercial-copy, and
headline-generation workflows. The weakest candidates are profile-specific
runtime SOPs, duplicated editing skills, generic story templates, and universal
AI-tell rules that conflict with corpus-derived voice guidance.

### Decision Summary

| Decision | Count | Skills |
| --- | ---: | --- |
| Update existing target | 4 | `style-forensics`, `brand-voice`, `style-writer`, `voice-dna-kit` from `writing-style-profiles` |
| Add after portable rewrite | 5 | `content-writer`, `write-better`, `copy-editor`, `direct-response-copy`, `headline-generator` |
| Skip as standalone | 7 | James `humanizer`, `ogilvy-writing-audit`, `grammarly-browser-proofread`, `narrative-builder`, source `minto-pyramid`, `writing-audit`, shared `humanizer` |
| Existing target unchanged | 1 | `minto-pyramid` |

## Confirmed Target State

The current category contains five skills:

| Target skill | Current responsibility |
| --- | --- |
| [`brand-voice`](skills/writing/brand-voice/SKILL.md) | Define an aspirational organizational voice from positioning, audience, and desired perception. |
| [`minto-pyramid`](skills/writing/minto-pyramid/SKILL.md) | Restructure complex writing around a governing answer, supporting arguments, and evidence. |
| [`style-forensics`](skills/writing/style-forensics/SKILL.md) | Measure prose style and produce an evidence-backed style fingerprint. |
| [`style-writer`](skills/writing/style-writer/SKILL.md) | Draft or revise prose against an existing voice profile. |
| [`voice-dna-kit`](skills/writing/voice-dna-kit/SKILL.md) | Capture an existing voice from samples and package it as reusable guidance. |

The current voice boundaries are intentional:

- `brand-voice` defines how an organization should sound.
- `style-forensics` performs deep measurement of supplied prose.
- `voice-dna-kit` captures how a person or organization demonstrably writes.
- `style-writer` applies a completed profile to new prose.

`voice-dna-kit` and `style-forensics` use byte-identical copies of
`scripts/analyze-style.sh`. The duplication is currently intentional because
each installed skill must remain self-contained.

## Repository Decision Rules

The audit applies the local guidance in
[`skill-structure`](skills/misc/skill-structure/SKILL.md):

1. A skill must teach a reusable capability for a recognizable class of tasks.
2. Prefer updating an existing skill when users would not know which duplicate
   to choose.
3. Split skills only when their starting conditions, workflows, or deliverables
   are materially different.
4. Keep supporting files local to the skill.
5. Avoid mandatory dependencies on sibling skills.
6. Remove runtime-native commands, fixed user paths, model routing, and hidden
   repository dependencies from portable skills.
7. Keep the main `SKILL.md` focused; move detailed examples and policies to
   references.
8. A skill should remain useful when installed by itself.

Prior category migration work also established these repository expectations:

- do not migrate a pack blindly
- reject generic wrappers and runtime workflow packaging
- check duplicate names, weak descriptions, oversized files, copied
  boilerplate, broken links, and category fit
- retain a supporting reference only when a concrete skill directly consumes it

## Source Inventory

All paths below are under `/Users/dpaluy/projects/ai/hermes-assets`.

| # | Requested source | Resolved source path | Main file size | Supporting material |
| ---: | --- | --- | ---: | --- |
| 1 | `style-forensics` | `profiles/james/skills/style-forensics/SKILL.md` | 228 lines | None |
| 2 | `brand-voice` | `profiles/james/skills/brand-voice/SKILL.md` | 157 lines | `references/restored-examples.md`, 423 lines |
| 3 | `style-writer` | `profiles/james/skills/style-writer/SKILL.md` | 178 lines | None |
| 4 | `content-writer` | `profiles/james/skills/content-writer/SKILL.md` | 235 lines | Sibling dependency on `copy-editor` reference |
| 5 | `write-better` | `profiles/james/skills/write-better/SKILL.md` | 578 lines | None |
| 6 | `humanizer` (James) | `profiles/james/skills/humanizer/SKILL.md` | 302 lines | Two references totaling 318 lines |
| 7 | `copy-editor` | `profiles/james/skills/copy-editor/SKILL.md` | 197 lines | Two references totaling 1,126 lines |
| 8 | `ogilvy-writing-audit` | `profiles/james/skills/editing/ogilvy-writing-audit/SKILL.md` | 153 lines | None |
| 9 | `grammarly-browser-proofread` | `profiles/james/skills/content-production/grammarly-browser-proofread/SKILL.md` | 206 lines | None |
| 10 | `direct-response-copy` | `profiles/james/skills/direct-response-copy/SKILL.md` | 309 lines | None |
| 11 | `headline-generator` | `profiles/james/skills/editing/headline-generator/SKILL.md` | 168 lines | Evidence reference and port notes |
| 12 | `narrative-builder` | `profiles/james/skills/narrative-builder/SKILL.md` | 199 lines | `references/detailed-reference.md`, 171 lines |
| 13 | `minto-pyramid` | `skills/minto-pyramid/SKILL.md` | 65 lines | HTML template |
| 14 | `writing-audit` | `profiles/kb-curator/skills/writing-audit/SKILL.md` | 193 lines | Grammarly/CDP reference and a 256-line fixer script |
| 15 | `writing-style-profiles` | `skills/writing/writing-style-profiles/SKILL.md` | 120 lines | Author-source patterns reference |
| 16 | `humanizer` (shared) | `skills/creative/humanizer/SKILL.md` | 679 lines | MIT license and David-specific handoff reference |

The shared `minto-pyramid` file is byte-identical to the copies installed in
the James and product-strategist profiles.

## Proposed Target Portfolio

```text
Voice
  observed samples -> style-forensics -> voice-dna-kit
  brand strategy ---------------------> brand-voice
  completed voice profile ------------> style-writer

Structure
  brief or draft -> minto-pyramid

Drafting
  general article or guide -> content-writer
  commercial asset --------> direct-response-copy
  fact-bound title options -> headline-generator
  voice-matched prose -----> style-writer

Finishing
  requested prose revision -> write-better
  editorial diagnosis -----> copy-editor
```

### Required Boundaries

These boundaries are necessary to prevent ambiguous activation:

- `content-writer` drafts general articles, blog posts, and guides.
- `style-writer` drafts or revises only when a voice profile already exists.
- `direct-response-copy` creates conversion-oriented assets such as landing
  pages, email copy, CTAs, and product microcopy.
- `headline-generator` produces multiple evidence-bound headline or subject-line
  candidates; it does not write the complete asset.
- `write-better` returns a revised version of existing prose.
- `copy-editor` returns an evidence-backed editorial report; it applies edits
  only when requested.
- No standalone `humanizer` is proposed. It would accept the same starting
  condition and produce the same default deliverable as `write-better`: existing
  prose in, revised prose out.
- Requests such as "humanize this," "make this sound less robotic," or "make
  this sound more natural" should activate `write-better`. Its description must
  include those triggers without promising AI-detector evasion.
- `write-better` optimizes for clearer, natural, author-faithful prose. It must
  not manufacture opinions, anecdotes, quirks, examples, or other signals of
  human authorship.

## Skill-by-Skill Recommendations

### 1. `style-forensics`

**Decision:** Update the existing target narrowly. Do not replace it.

**Why the target is stronger**

- It states corpus limitations.
- It prohibits identity, demographic, personality, and intent inference from
  prose.
- It treats the analyzer as a baseline rather than ground truth.
- It requires parsing review.
- It requires examples for qualitative and recurrence claims.
- It distinguishes stable traits from contextual variation.
- It reports confidence and unresolved questions.

**Useful source material**

- optional common-word and long-word diagnostics
- a more explicit signature-pattern search catalogue
- an explicit cross-article comparison presentation

**Do not import**

- `$ARGUMENTS` prompt framing
- mandatory `humanizer` and `copy-editor` integration
- contradictory instructions about saving output immediately versus waiting for
  confirmation
- rigid frequency thresholds that are weaker than the current target's
  provisional-finding rules

**Highest-value change**

Add an optional cross-sample comparison table showing stable traits, contextual
dials, outliers, and confidence. Keep vocabulary diagnostics optional so they do
not inflate every report.

### 2. `brand-voice`

**Decision:** Update the existing target narrowly. Do not replace it.

**Why the target is stronger**

- It cleanly separates an aspirational organizational voice from observed
  current writing.
- It derives the voice from positioning, audience, and desired perception.
- It turns traits into observable behavior.
- It separates stable identity from contextual tone.
- It includes claims, evidence, accessibility, terminology, and legal
  constraints.
- It already has a contextual tone matrix and calibration examples.

**Useful source material**

- source-bank quality checks and outlier handling
- draft-versus-approved-edit comparison
- converting repeated stakeholder edits into concrete rules
- more explicit editing-preference capture

**Do not import**

- admired-brand research as permission to imitate another voice
- mixed personal and organizational voice ownership
- persona anthropomorphism
- stock calibration examples
- fixed `docs/` output paths
- runtime-specific prompt and integration language

**Highest-value change**

Add a calibration step that compares a proposed draft with the version approved
or edited by the brand owner. Promote repeated edits into rules only after they
are confirmed across examples.

### 3. `style-writer`

**Decision:** Update the existing target narrowly. Do not replace it.

**Why the target is stronger**

- It requires source material for factual claims.
- It prohibits invented companies, statistics, quotations, anecdotes,
  experiences, endorsements, and authorship claims.
- It treats metrics as guardrails.
- It handles zero targets without division-by-zero logic.
- It uses length-appropriate tolerances.
- It rejects a single false-precision "voice accuracy" score.
- It presents a plan only when approval or unresolved strategy warrants one.

**Useful source material**

- a concrete target-versus-actual audit table
- a focused correction loop that changes the largest meaningful deviations
  first

**Do not import**

- mandatory user approval before drafting
- 85% and 70% scoring gates
- divide-by-zero-prone accuracy formulas
- mandatory historical anchors, named entities, data, or quotations
- fixed punctuation and rhythm quotas
- mandatory `humanizer` or `copy-editor` calls

**Highest-value change**

Add a compact audit table for applicable profile constraints:

| Constraint | Target | Actual | Disposition |
| --- | --- | --- | --- |
| Example | Range, ban, or tendency | Measured result | Fix, retain with reason, or not applicable |

### 4. `content-writer`

**Decision:** Add a new portable skill after rewriting the source.

**Distinct capability**

Draft a general article, blog post, or guide through a brief, outline, and
section-writing workflow when no voice-specific or commercial-copy workflow
owns the request.

**Keep**

- outline-first and direct-write modes
- brief clarification
- section purpose and evidence planning
- readability and useful formatting
- source-aware fact checking
- checking for an existing voice profile before applying generic defaults

**Remove or change**

- David-specific article package
- James profile requirements
- mandatory Grammarly browser proofread
- mandatory `writing-audit`
- commit and push instructions
- fixed title, section, sentence, and word counts
- universal AI-word blacklist
- sibling link to `../copy-editor/references/AI_WRITING_TELLS.md`

**Boundary**

The skill may optionally route a completed draft to:

- `style-writer` when a voice profile should govern the prose
- `write-better` when the user wants a revised final version
- `copy-editor` when the user wants an editorial report

It must not require those sibling skills to function.

### 5. `write-better`

**Decision:** Add after condensing and narrowing its trigger.

**Distinct capability**

Return a clearer, more direct revision of existing informational, workplace,
technical, or general prose while preserving facts, uncertainty, genre, and the
author's real voice.

**Keep**

- lead with the useful part
- preserve information rather than length
- use concrete nouns, direct subjects, and direct verbs
- make requested actions operational
- preserve evidence and uncertainty
- avoid semantic repetition, fake depth, vague authority, promotional language,
  and rhetorical packaging
- use a meaning, structure, language, rhetoric, and reader-test editing sequence

**Add from James `humanizer`**

- lock factual anchors before rewriting
- detect and respect an existing voice profile
- distinguish intentional voice devices from mechanical AI patterns
- allow a no-change result

**Remove or change**

- universal ban on em dashes
- broad "humanize" language that promises detector evasion
- any instruction to manufacture fragments, opinions, caveats, quirks, or
  examples
- enough examples and repetition to bring the 578-line main file down to a
  focused core; move detailed examples to a reference

**Boundary**

`write-better` produces the revised prose. It does not return a full editorial
issue report unless the user asks for explanations. Its frontmatter should
explicitly include "humanize this," "less robotic," and "more natural" as
activation language so users do not need a separately named `humanizer` skill.
These triggers refer to writing quality and author-faithful revision, not
classifier evasion.

### 6. `humanizer` (James)

**Decision:** Skip as a standalone skill. Fold only safe mechanics into
`write-better`.

**Useful material**

- style-context detection
- factual-anchor locking
- early exit when the text does not need rewriting
- ordered transformation and rescan loop

**Reasons to skip**

- It has the same starting condition and default deliverable as `write-better`:
  existing prose in, revised prose out. Users would not have a reliable reason
  to choose one over the other.
- Detector-evasion positioning optimizes for an unstable classifier rather than
  for clarity, accuracy, or the author's actual voice. Claims that a rewrite
  defeats detection or reaches a "human baseline" are not supportable.
- Fixed burstiness and sentence-length targets can make prose less appropriate
  for its genre merely to vary its surface form.
- Instructions to inject opinions, caveats, named examples, personal quirks, or
  fragments can alter facts, tone, and implied authorship.
- Installing a second overlapping skill would make routing less reliable while
  adding no distinct workflow or deliverable.

**Capability retained elsewhere**

Skipping the standalone skill does not remove natural-language revision.
`write-better` should retain factual-anchor locking, style-context detection,
pattern-cluster diagnosis, preservation of intentional irregularity, and the
option to return the text unchanged. It should also activate for ordinary
"humanize this" requests, but it must interpret them as requests for clearer,
less mechanical, author-faithful prose rather than requests to evade a detector.

### 7. `copy-editor`

**Decision:** Add after rewriting and sharply narrowing the deliverable.

**Distinct capability**

Review an existing public-facing or business draft and return an evidence-backed
editorial report with exact quotations, categorized issues, severity,
recommended fixes, recurring patterns, and top priorities.

**Keep**

- resolve an applicable project or voice guide first
- inspect context and audience before applying defaults
- quote the exact text that triggered a finding
- distinguish grammar, clarity, specificity, structure, attribution, voice, and
  style-guide findings
- avoid overfitting to generic AI-tell lists
- offer report-only, inline-edit, or clean-copy modes when the user chooses

**Do not import**

- the 529-line `AI_WRITING_TELLS.md` as a mandatory policy
- the 597-line `DEFAULT_STYLE_GUIDE.md`
- James-specific zero-dash rules
- contradictory transition advice
- generic rewrite and "humanize" triggers that belong to `write-better`

**Boundary**

Default output is a report. Apply edits only when the user asks for an edited
version.

### 8. `ogilvy-writing-audit`

**Decision:** Skip as a standalone skill. Fold selected gates into `copy-editor`.

**Keep as editorial checks**

- verify quotations and attribution
- make the requested action explicit
- consider whether writing is the correct communication medium
- cold reread for important material
- obtain a second lens for high-stakes copy

**Reasons to skip**

- substantial overlap with `copy-editor`
- universal two-page, sentence-length, paragraph-length, and punctuation rules
- James and David-specific delivery behavior
- fixed local KB source path
- attribution to an external framework adds a skill choice without a distinct
  workflow or deliverable

### 9. `grammarly-browser-proofread`

**Decision:** Skip from Majestic Abilities. Keep profile-local if still useful.

**Reasons**

- requires the user's authenticated Brave session
- requires CDP on `127.0.0.1:9222`
- assumes `agent-browser`
- contains process-kill and browser-relaunch commands
- depends on current Grammarly Coda/Slate behavior
- contains James model and profile routing
- sends article text to a third-party service
- is a runtime integration SOP, not a portable writing capability

**Reusable principle**

External grammar recommendations must be reviewed individually. They do not
override factual meaning, technical terminology, attribution, or a supplied
voice guide.

### 10. `direct-response-copy`

**Decision:** Add after sanitizing the source.

**Distinct capability**

Create conversion-oriented landing pages, email copy, sales copy, CTAs, and
product microcopy from a defined reader moment, evidence set, offer, and desired
action.

**Keep**

- context-first intake
- reader-moment gate
- evidence and proof inventory
- specific-benefit and "so what" reasoning
- story pressure test
- product microcopy guidance
- CTA specificity
- no invented proof or testimonials
- separate modes for new copy, rewrite, file edit, and embedded handoff

**Remove or change**

- unsupported conversion statistics
- universal headline myths
- manipulative "velvet rope" defaults
- David and James profile references
- mandatory `writing-audit`
- mandatory style gates that are not installed with the skill

**Provenance**

The local source says parts were adapted from `mikiarlo3/ai-copywriter` v1.5.1
under MIT. If wording or structure is copied, preserve the required attribution
and license material. The current audit has not independently verified the
upstream license beyond the local source note.

### 11. `headline-generator`

**Decision:** Add after sanitizing the source.

**Distinct capability**

Generate multiple fact-bound news headlines, press-release headlines, feature
headlines, and pitch subject lines by identifying the strongest true tension in
the supplied facts.

**Keep**

- lay out actors, event, numbers, stakes, and supplied proof
- identify the factual "charge"
- generate materially different candidates rather than synonyms
- size claims to proof
- distinguish formats
- provide character counts for subject lines
- lead with candidates and recommend a best option
- preserve the evidence reference and its caveats

**Remove or change**

- newsjack desk persona
- `skills/ETHICS.md` dependency
- handoffs to nonexistent `meanest-editor`, `fact-check`, or other newsjack
  skills
- unsupported certainty about headline performance
- required news-style candidates when the requested format does not benefit

**Provenance**

`PORT_NOTES.md` identifies `elvisun/newsjack` as the upstream source and records
an observed MIT license. Preserve attribution and license requirements if the
skill is ported. The current audit has not independently verified the upstream
license text.

### 12. `narrative-builder`

**Decision:** Skip as a standalone skill for now.

**Useful material**

- story-mining questions
- three-beat and five-beat micro-story formats
- transformation, failure, discovery, and mentor arcs

**Reasons to skip**

- generic and template-heavy
- unsupported "22x more memorable" claim
- substantial overlap with `content-writer` and the story sections of
  `direct-response-copy`
- insufficient safeguards against inventing first-person experiences, conflict,
  dialogue, or emotional details

**Possible future route**

If repeated social-story work justifies a separate capability, create an
evidence-safe `story-writer` with explicit rules against fabricated experience
and attribution. Do not port the current source unchanged.

### 13. `minto-pyramid`

**Decision:** Skip the source. Keep the current target unchanged.

**Why the target is stronger**

- captures the audience's decision or question
- records required conclusions and constraints
- treats MECE as a diagnostic rather than a forced partition
- separates supplied evidence, verified evidence, unsupported claims, and
  evidence still needed
- chooses and explains logical ordering
- diagnoses misplaced evidence and structural dead weight
- returns a complete Markdown restructuring plan

**Do not import**

- default HTML output
- the HTML template
- the shorter source workflow

### 14. `writing-audit`

**Decision:** Skip.

**Reasons**

- universal em-dash ban conflicts with source-observed voice rules
- deterministic word substitutions can alter meaning
- hardcoded David and KB assumptions
- fixed `~/.hermes` and `/Users/clawbot/projects/writing-eval` paths
- script defaults tied to `~/Documents/kb`
- James-only Grammarly SOP dependency
- authenticated Brave/CDP integration
- overlap with `write-better` and `copy-editor`

**Reusable idea**

A deterministic rescan can be useful for explicit, context-specific bans.
Implement such checks only when a user-supplied or corpus-derived guide defines
the prohibited pattern. Do not create a universal AI-tell linter from this
source.

### 15. `writing-style-profiles`

**Decision:** Update `voice-dna-kit` narrowly. Do not add a separate target
skill.

**Useful material**

- prefer first-party canonical sources
- define the corpus before collection
- store provenance separately from prose
- preserve structure while excluding wrappers and duplicate parent/child text
- hash normalized text and remove exact duplicates
- validate with a holdout
- state that distance metrics do not prove quality, truth, or authorship

**Do not import**

- `/Users/clawbot/projects/writing-eval`
- `uv run writing-eval` commands
- fixed corpus storage paths
- Hermes metadata and `writing-audit` dependency
- scraping and extractor implementation details

**Highest-value change**

Add an optional corpus manifest, exact-deduplication step, and holdout comparison
to `voice-dna-kit`. Keep the implementation tool-neutral.

### 16. `humanizer` (shared v2.8)

**Decision:** Skip as-is and do not add a second Humanizer.

**Useful material**

- diagnose pattern clusters rather than isolated tokens
- document false positives
- preserve intentional human irregularity
- allow a no-change result
- distinguish generic AI patterns from supplied voice evidence

**Reasons to skip**

- 679-line main file
- broad overlap with `write-better`
- Hermes-native tool names
- David, Atlas, and James handoff lane
- universal zero-dash rule
- generic bans that may contradict the source voice
- worked example and pattern catalogue are too large for a routinely loaded
  portable skill

**Provenance**

The shared source identifies `blader/humanizer` v2.8 as MIT and includes a
`LICENSE` file. Preserve the license and attribution if text is adapted into
`write-better`.

## Duplicate and Boundary Adjudications

### `write-better` versus `humanizer`

Retain `write-better`; skip both Humanizer variants as standalone skills.

**Why one skill is sufficient**

Both Humanizers and `write-better` accept existing prose and return revised
prose intended to sound less mechanical. They do not have materially different
starting conditions, workflows, or default deliverables. Keeping both would
violate the repository preference for updating one capability when users would
not know which duplicate to choose.

`write-better` is the stronger owner because it treats clarity, accuracy,
uncertainty, genre, and the author's demonstrated voice as the objective. The
Humanizer sources instead include detector-evasion claims and mechanical
variation tactics. Those tactics can produce superficial irregularity while
changing meaning or inventing signs of authorship.

**How the familiar request remains supported**

`write-better` should explicitly activate for "humanize this," "make this sound
less robotic," and equivalent requests. It should interpret them as requests
for natural, author-faithful revision, not as requests to defeat a classifier.
No useful user-facing capability is lost by omitting the duplicate name.

**Safe mechanics to retain**

- lock facts and required claims before revising
- detect and respect supplied or demonstrated voice
- diagnose clusters of mechanical patterns rather than banning isolated words
- preserve intentional irregularity
- allow a no-change result

Do not retain detector-evasion promises, universal punctuation bans, fixed
burstiness targets, or instructions to invent opinions, experiences, examples,
quirks, or fragments.

### `write-better` versus `copy-editor`

Retain both only with different default deliverables:

- `write-better`: return revised prose
- `copy-editor`: return an editorial diagnosis with evidence and proposed fixes

If their descriptions both promise generic review, editing, rewriting, and
humanization, they become duplicates. Their frontmatter must encode the
boundary.

### `writing-style-profiles` versus `voice-dna-kit`

Update `voice-dna-kit`.

Both own corpus selection, clean-prose extraction, profile construction, and
validation. The shared source's distinct value is methodological rigor around
provenance, exact deduplication, and holdout testing, not a separate user-facing
workflow.

### `ogilvy-writing-audit` versus `copy-editor`

Update `copy-editor`.

The Ogilvy source contributes several useful gates but does not define a
materially different input, workflow, or output. A named-framework audit would
increase routing ambiguity.

### `headline-generator` versus `direct-response-copy`

Retain both.

- `headline-generator` produces a set of fact-bound title or subject-line
  candidates across editorial formats.
- `direct-response-copy` produces a complete conversion-oriented asset.

`direct-response-copy` may create a working headline as part of an asset, but it
should route to `headline-generator` only when the user wants a deliberate
candidate sprint or editorial headline formats.

### `content-writer` versus `style-writer`

Retain both.

- `content-writer` owns the article or guide workflow.
- `style-writer` owns application of an existing voice profile.

When both conditions apply, `content-writer` may define the format and factual
plan while `style-writer` supplies the voice constraints. Neither should require
the other to be installed.

## Proposed Implementation Order

### Phase 1: Complete the finishing lane

1. Add a condensed `write-better` whose description includes "humanize this"
   and equivalent natural-prose triggers without detector-evasion claims.
2. Add a report-first `copy-editor`.
3. Verify their descriptions and outputs do not overlap.

This phase provides the broadest reusable value across informational,
technical, business, and public-facing prose.

### Phase 2: Add general drafting

4. Add a sanitized `content-writer`.
5. Make routing to voice and editing skills optional.

### Phase 3: Add commercial and headline capabilities

6. Add `direct-response-copy` with evidence and claims safeguards.
7. Add `headline-generator` with provenance, evidence caveats, and no missing
   sibling dependencies.

### Phase 4: Enrich the existing voice pipeline

8. Add cross-sample comparison to `style-forensics`.
9. Add owner-edit calibration to `brand-voice`.
10. Add a target-versus-actual audit table to `style-writer`.
11. Add manifest, deduplication, and holdout guidance to `voice-dna-kit`.

## Implementation Constraints

Any implementation should:

- treat each source as raw material, not a file to copy wholesale
- preserve the current target's stronger safeguards
- keep every skill useful when installed by itself
- use minimal frontmatter unless a standard optional field is necessary
- remove model names, profile names, Hermes commands, fixed user paths, and
  mandatory sibling-skill dependencies
- retain user-supplied facts, uncertainty, attribution, and authorship
- prohibit invented testimonials, quotations, statistics, experiences, and
  specificity
- make punctuation and AI-tell rules contextual rather than universal
- optimize "humanize" requests for writing quality and author fidelity, never
  for classifier evasion
- prohibit manufactured opinions, experiences, anecdotes, examples, quirks, or
  other false signals of human authorship
- move long examples and policy catalogues into references only when directly
  consumed
- preserve applicable third-party licenses and attribution
- avoid changing unrelated categories

## Validation Required After Implementation

The implementation should not be considered complete until these checks pass:

1. Every `skills/writing/*/SKILL.md` name matches its directory.
2. Every description states both the capability and concrete activation
   triggers.
3. No two descriptions compete for the same starting condition and default
   deliverable.
4. All relative links resolve inside the installed skill.
5. No skill requires an uninstalled sibling skill.
6. No fixed James, David, Atlas, Hermes, Brave, Grammarly, Coda, local-KB,
   `/Users/clawbot`, or `/Users/dpaluy` dependency remains unless the target is
   deliberately nonportable and declares that compatibility.
7. Scripts pass syntax checks and a focused functional smoke test.
8. Third-party license and attribution requirements are preserved.
9. Category-scoped installation discovers every intended skill and copies all
   required support files.
10. A scratch installation proves each new skill remains self-contained.
11. `README.md` category count and Writing Skills table match the final tree.
12. The scoped diff contains no unrelated cleanup or category changes.
13. Routing smoke tests show that "humanize this" and "make this less robotic"
    select `write-better`, preserve factual anchors, and produce no
    detector-evasion claim.

## Evidence Already Checked

Before this document was created:

- the target category contained exactly 5 skills
- each current target skill's `name` matched its directory
- current target-relative links resolved
- both `analyze-style.sh` copies passed `bash -n`
- the two target analyzer scripts were byte-identical
- the shared, James, and product-strategist copies of the source
  `minto-pyramid` were byte-identical
- the two Humanizer sources were materially different, not duplicate copies
- the repository worktree was clean

The source audit also found:

- all 16 resolved `SKILL.md` names matched their directories
- local relative links resolved in the source tree
- some apparently valid links were still nonportable because they depended on
  sibling profile skills
- multiple sources contained fixed runtime paths, profile names, browser state,
  or third-party-service assumptions

## Implementation Record

The audit was implemented with these results:

- updated `style-forensics`, `brand-voice`, `style-writer`, and `voice-dna-kit`
- added `content-writer`, `write-better`, `copy-editor`,
  `direct-response-copy`, and `headline-generator`
- kept `minto-pyramid` unchanged
- kept both Humanizer variants and the other five rejected sources out of the
  target portfolio
- updated `seo-content` only where necessary to distinguish search-led drafting,
  replace its stale Humanizer handoff, add authorial-safety rules, and make its
  script instructions portable
- updated the README Writing count and table from 5 to 10 skills

### Licensing resolution

The upstream MIT licenses were verified and copied locally:

- `mikiarlo3/ai-copywriter` at main commit
  `201f89a07d7a8d792a11165270591b3684c886a1`
- `elvisun/newsjack` at main commit
  `0eebc3206437ae6544733a4e2280cf1bc8cc212d`

Each adapted skill records its pinned provenance and links to its local
`LICENSE`. No shared-Humanizer wording was copied into `write-better`.

### Verification completed

- strict YAML parsing, directory/name matching, description limits, and local
  link resolution passed for all 10 writing skills
- category discovery found exactly 10 writing skills
- a scratch copy installation included all 10 skills and their support files
- each of the 5 new skills installed independently in a separate scratch project
- both analyzer scripts passed syntax checks, remained byte-identical, and
  produced identical output on a focused fixture
- all 3 `seo-content` scripts compiled and passed a focused functional smoke test
- portability scans found no profile names, fixed user paths, runtime commands,
  or repository-relative pack paths in the implemented skills
- both local MIT license files matched the verified upstream license text
- blind routing selected the intended skill for general drafting, SEO drafting,
  profile-guided writing, natural-language revision, editorial review,
  conversion copy, and headline generation with no ambiguous cases
- a `write-better` behavioral smoke test preserved names, dates, numbers,
  quarantine state, obligation, and uncertainty while making no detector-evasion
  claim

### Shared-worktree scope note

A separate Data-category workstream appeared concurrently under `skills/data`
and in separate README hunks. Those changes were not created, modified, or
removed by this implementation. They must remain excluded when staging or
reviewing the writing-audit patch. Validation item 12 applies to the scoped
writing and adjacent `seo-content` changes, not to the aggregate shared
worktree.

## Remaining Decisions

1. **Naming:** `write-better` remains broad but now has explicit positive and
   negative routing language. Rename it only if real activation tests show
   persistent ambiguity.
2. **Narrative demand:** `narrative-builder` is skipped because its present form
   is weak, not because narrative writing can never justify a skill. Repeated
   social-story work could justify a safer future capability.
3. **External proofread:** Grammarly may remain valuable in a specific Hermes
   profile. This audit only rejects it as a portable Majestic Ability.

## Independent Reviewer Checklist

### Portfolio

- [ ] Are the proposed 10 skills distinct enough for reliable activation?
- [ ] Is any proposed new skill still a generic wrapper rather than a reusable
      capability?
- [ ] Is any skipped skill actually distinct enough to retain?
- [ ] Does any retained pair still have ambiguous inputs or outputs?

### Existing skill updates

- [ ] Do the four proposed updates add meaningful value without weakening the
      current safeguards?
- [ ] Should any proposed source addition be omitted as marginal complexity?
- [ ] Does the `voice-dna-kit` update preserve its tool-neutral, portable scope?

### New skills

- [ ] Is `write-better` preferable to a standalone `humanizer`?
- [ ] Is the rewrite-versus-audit boundary between `write-better` and
      `copy-editor` sufficient?
- [ ] Does `content-writer` remain distinct from `style-writer` and
      `seo-content`?
- [ ] Does `direct-response-copy` remain evidence-safe and non-manipulative?
- [ ] Is `headline-generator` useful outside its newsjack origin?

### Portability and safety

- [ ] Are all profile names, model routing, fixed paths, and runtime commands
      identified?
- [ ] Are external-service and privacy assumptions explicit?
- [ ] Do all transformations preserve facts, uncertainty, attribution, and
      authorship?
- [ ] Are punctuation and AI-tell rules contextual rather than universal?

### Provenance

- [ ] Are upstream licenses verified before implementation?
- [ ] Are attribution and license files included where required?
- [ ] Are evidence claims either supported by retained references or removed?

## Requested Reviewer Output

Use this format:

```markdown
# Writing Skills Audit Review

## Verdict
APPROVED | REVISE

## Findings

| ID | Severity | Skill or boundary | Finding | Required change |
| --- | --- | --- | --- | --- |
| W-001 | blocker/high/medium/low | ... | ... | ... |

## Disposition Check

- Updates: agree or proposed changes
- Additions: agree or proposed changes
- Skips: agree or proposed changes

## Portfolio Boundary Check

- ...

## Licensing and Portability Check

- ...

## Non-blocking Observations

- ...
```
