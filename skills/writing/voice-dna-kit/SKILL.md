---
name: voice-dna-kit
description: Capture an existing personal or organizational writing voice from real samples and package it as reusable guidance. Use when preserving an established voice in AI output, extracting writing rules and bans, or creating a portable voice profile.
---

# Voice DNA Kit

Capture how a person or organization demonstrably writes. Produce a compact operating guide backed by observed samples instead of aspirational adjectives.

## Boundary

Use this skill to preserve an existing voice.

- To design how an organization should sound, use `brand-voice`.
- To produce a deeper quantitative report, use `style-forensics`.
- To draft new content from a completed profile, use `style-writer`.

This skill captures and packages a voice. It does not create a new brand identity or write the final long-form content.

## Inputs

Ask for:

1. Three to five representative samples from the same person or organization.
2. The contexts where the voice will be used.
3. Known phrases, structures, punctuation, or tones to avoid.
4. Any before-and-after edits that show what the owner changed.
5. The requested output location.

Use [sample-selection-guide.md](references/sample-selection-guide.md) to assess the corpus. Prefer writing created or substantially edited by the voice owner. State when AI-assisted or mixed-author samples weaken confidence.

## Deliverables

Create these files when the user requests a persisted kit:

- `voice-dna.md` with short, operational rules
- `style-dna.md` with measurements and supporting examples
- `banned-phrases.md` with generic and source-specific bans
- `voice-review-checklist.md` with final checks
- `voice-verification.md` with the comparison test and remaining mismatches

Place them in the user-selected directory. Do not assume a runtime-specific folder.

## Workflow

### 1. Select and label the corpus

Record the author, channel, audience, approximate date, and provenance of each sample. Exclude quoted third-party text, boilerplate, transcripts the owner did not edit, and samples from a different voice or register.

If the corpus contains distinct registers, label them. Preserve one stable core and document the controlled differences.

### 2. Extract clean prose

Remove navigation, metadata, signatures, code, URLs, quoted material, and repeated boilerplate. Keep paragraph boundaries and deliberate formatting where they carry style.

### 3. Measure before interpreting

Resolve [analyze-style.sh](scripts/analyze-style.sh) relative to this file and run it against the cleaned samples. Save its output as the initial `style-dna.md`.

Review the measurements manually. Sentence splitting and rhetorical-device detection are imperfect, so correct obvious parsing errors and attach examples to every important conclusion.

Measure at minimum:

- sentence and paragraph length
- short-sentence ratio
- punctuation frequency
- contractions and pronoun use
- hedging and confidence
- recurring openers, transitions, fragments, and landings
- vocabulary specificity and repeated terms

### 4. Extract operational rules

Use [voice-dna-template.md](references/voice-dna-template.md). Convert stable evidence into rules that can pass or fail review.

Separate:

- stable voice traits
- context-dependent tone dials
- measured tendencies
- strict bans
- uncertain observations that need more samples

Do not turn every observed quirk into a rule. Preserve patterns that recur or clearly carry identity.

### 5. Build the ban list

Start with [banned-ai-phrases.md](references/banned-ai-phrases.md), but keep only defaults relevant to the intended context. Add source-specific bans from rejected drafts, absent punctuation patterns, and repeated owner edits.

Concrete bans beat instructions such as "sound human."

### 6. Build the review checklist

Create checks for:

- banned patterns
- sentence and paragraph rhythm
- punctuation
- confidence and hedging
- vocabulary and specificity
- register selection
- factual and attribution integrity

### 7. Verify the kit

Run [voice-match-test.md](references/voice-match-test.md). Compare a baseline draft with a profile-guided draft against the source corpus.

Patch the profile when a mismatch cannot be explained by an existing rule. Do not copy distinctive phrases from source samples merely to improve resemblance.

## Quality Gate

The kit is ready when:

- every strong rule cites repeated evidence or a clear edit preference
- actual numbers or explicit unknowns support the style profile
- stable voice and contextual tone are separate
- bans are concrete and reviewable
- the guided test is closer to the samples without copying them
- the short guide is concise enough to load routinely
- corpus limitations are disclosed
