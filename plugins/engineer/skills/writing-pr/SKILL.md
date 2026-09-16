---
name: writing-pr
description: "Write PR titles and descriptions from the final diff using the repository template."
---

# Writing a Pull Request

Explain the final change so a reviewer can assess its purpose, behavior, and supporting evidence.

## Read Before Writing

- Read the repository's PR guidance and applicable local template. Preserve required sections, fields, checklists, and issue links. Apply the writing rules below within that structure. If several templates exist, select the one that matches the change; ask only when the choice is unclear.
- Inspect the complete diff against the intended target branch. Read enough surrounding code to confirm the behavior described.
- When editing an existing PR, read its current title and body. Preserve required references and valid attachments.

## Title and Body

- Write a specific title that names the problem fixed or behavior added. Follow repository title conventions.
- Lead with the concrete problem and resulting behavior. Use a short before/after example when it makes the change easier to understand.
- Describe the final aggregate change. Omit intermediate commits, abandoned approaches, and reductions in earlier diff size unless they explain a decision that still affects review. Do not assume a merge strategy.
- Keep simple changes to a short paragraph or a few bullets. Add detail only when complexity or risk requires it.
- Use code references, short snippets, or Mermaid diagrams when they clarify behavior. Do not add them as decoration.
- Omit routine test logs and generic claims such as "tests passed." Include required validation fields, relevant results, failed checks, and material verification limits. Never claim a check ran without evidence.

## Evidence

- For rendered UI or interaction changes, include verified before/after screenshots or video when available. Use a comparison table for screenshots and separate links for videos. If evidence is missing, state the gap; do not invent attachment links or claim visual verification.
- For performance claims, show baseline and candidate measurements in a table. Identify the target-branch baseline, candidate revision, and relevant test conditions so the comparison is meaningful. If measurements are unavailable, omit the improvement claim or mark it as unverified.

## Final Check

Check the title and body against the final diff and local template. Remove unsupported claims and repeated information. Confirm that required fields and links remain intact; leave checkboxes unchecked when their conditions are not met.

Return the requested title and body. Drafting does not authorize publishing or changing a remote PR. After an authorized remote update, read back the saved text and verify its links and attachments.
