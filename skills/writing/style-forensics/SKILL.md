---
name: style-forensics
description: Measure and explain the writing style of one or more prose samples using quantitative metrics and cited examples. Use when analyzing sentence rhythm, punctuation, vocabulary, tone, rhetorical devices, or producing a detailed Style DNA report.
---

# Style Forensics

Produce an evidence-backed style fingerprint. Measure first, then interpret the numbers with examples from the supplied prose.

## Boundary

Use this skill for deep analysis.

- To define a desired organizational voice, use `brand-voice`.
- To package an existing voice as concise reusable guidance, use `voice-dna-kit`.
- To draft against an existing profile, use `style-writer`.

Do not infer personality, demographics, identity, or intent from prose style.

## Inputs

Collect:

1. One or more samples believed to come from the same author or organizational voice.
2. The analysis goal and intended use.
3. Relevant context such as channel, audience, date, and editing history.
4. The requested output location, if the report should be saved.

State corpus limitations. A short, mixed-author, translated, or heavily AI-assisted sample cannot support a confident fingerprint.

## Workflow

### 1. Prepare clean prose

Work from a temporary copy. Remove:

- frontmatter and metadata
- navigation and repeated boilerplate
- code blocks and inline code
- URLs while preserving meaningful link text
- headings and formatting markers
- quotations not written by the target author

Preserve paragraph boundaries. Record the final prose word count and excluded material.

### 2. Generate baseline measurements

Resolve [analyze-style.sh](scripts/analyze-style.sh) relative to this file and run it against the cleaned source files.

Treat the script as a baseline, not ground truth. Validate sentence boundaries around abbreviations, decimals, initials, headings, and quotations. The bundled token categories are most useful for English prose. Adapt the tokenizer for other languages and disclose the change.

### 3. Measure sentence rhythm

Report:

| Metric | Required result |
| --- | --- |
| Sentences | Count |
| Sentence length | Mean, median, minimum, and maximum words |
| Distribution | 1 to 7, 8 to 15, 16 to 25, and 26 or more words |
| Short-sentence ratio | Percentage below 8 words |
| Rhythm | Where short and long sentences occur |

Explain clusters, alternation, punch lines, and unusually long constructions with examples.

### 4. Measure punctuation and paragraphs

Report counts and per-100-word rates for:

- commas
- colons
- semicolons
- em and en dashes
- exclamation marks
- question marks
- parenthetical asides

Separately identify rhetorical questions through inspection. A question mark is not proof of a rhetorical question.

Report paragraph count, average and median paragraph length, and one-sentence paragraph ratio. Exclude pure lists when they would distort prose structure.

### 5. Profile vocabulary and tone signals

Report:

- total and unique words
- lexical diversity, with corpus-size caveat
- long-word ratio
- frequently repeated content words
- recurring jargon, colloquialisms, metaphors, and anchoring terms
- first-person singular, first-person plural, and second-person rates
- contractions and hedges with examples
- observable warmth, certainty, formality, and emotional intensity

Describe textual behavior, not hidden personal traits.

### 6. Identify signature devices

Search for:

- frequent sentence openers
- conjunction openers
- fragments and fragment stacks
- recurring launchers and landing lines
- contrast structures
- repetition and anaphora
- question clusters
- setup-and-payoff patterns
- temporal or narrative sequencing

Report absence when it is meaningful. Require at least two examples before calling a device recurring, unless the corpus is too short, in which case mark the observation provisional.

### 7. Describe macro-structure

Explain how samples tend to:

- open
- organize sections or paragraphs
- introduce evidence and examples
- transition
- close

For multiple samples, distinguish stable traits from channel-specific or time-specific variation.

### 8. Compile the report

Return:

1. Sources and corpus limitations
2. Cleaning and measurement notes
3. Core metrics table
4. Sentence distribution
5. Punctuation and paragraph profile
6. Vocabulary and tone signals
7. Signature devices with examples
8. Structural blueprint
9. Stable traits versus contextual dials
10. Quick-reference metrics
11. Confidence and unresolved questions

If the user requested a file, save it as `<source-name>-style-dna.md` or to the supplied path. Otherwise present the report without writing files.

## Quality Gate

The report is ready when:

- every reported number is reproducible
- parsing errors were reviewed rather than trusted blindly
- every qualitative claim cites examples
- frequency claims distinguish counts from impressions
- sample limitations and uncertainty are explicit
- the report describes prose without making identity claims
