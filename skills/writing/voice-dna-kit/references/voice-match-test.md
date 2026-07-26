# Voice Match Test

Use this test before treating a Voice DNA kit as ready.

## Inputs

- a representative holdout excluded from profile construction, when available
- source samples or `style-dna.md` for context when no holdout is defensible
- `voice-dna.md`
- a brief for a representative 150 to 300 word draft

## Test

1. Confirm the holdout was not used to construct or tune `voice-dna.md`.
2. Write a baseline draft from the brief without the Voice DNA rules.
3. Write a second draft from the same brief using `voice-dna.md`.
4. Compare both drafts against the holdout. If no holdout is available, use representative source samples and disclose the weaker test.
5. Identify where the guided draft moved closer, stayed unchanged, or overfit.
6. Identify generic patterns or mismatches that survived.
7. Patch only rules supported by the construction corpus or explicit owner preference.
8. Repeat once when material mismatches remain.

Do not treat a distance score or subjective resemblance judgment as proof of quality, truth, or authorship.

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
- `Holdout status and limitations`
- `Ready` or `Not ready`
