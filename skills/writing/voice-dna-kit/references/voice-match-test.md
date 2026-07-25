# Voice Match Test

Use this test before treating a Voice DNA kit as ready.

## Inputs

- source samples or `style-dna.md`
- `voice-dna.md`
- a brief for a representative 150 to 300 word draft

## Test

1. Write a baseline draft from the brief without the Voice DNA rules.
2. Write a second draft from the same brief using `voice-dna.md`.
3. Compare both drafts against the source samples.
4. Identify which rules improved the second draft.
5. Identify generic patterns or mismatches that survived.
6. Patch only rules supported by the source or explicit owner preference.
7. Repeat once when material mismatches remain.

Do not improve resemblance by copying distinctive source phrases.

## Review Questions

- Is the rhythm closer to the source without becoming mechanical?
- Are paragraph length and punctuation consistent with the relevant register?
- Does the draft use the owner's normal confidence, warmth, and specificity?
- Did any banned phrase or structure appear?
- Are facts and attributions intact?
- Would the voice owner plausibly accept the draft after a light edit?

## Output

Return:

- `Baseline draft`
- `Voice-guided draft`
- `Evidence-backed improvements`
- `Remaining mismatches`
- `Voice DNA patches`
- `Ready` or `Not ready`
