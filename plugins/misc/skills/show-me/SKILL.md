---
name: show-me
description: Explain the current topic with the smallest accurate visual. Use when the user asks to show, sketch, diagram, map, or visualize an algorithm, code path, architecture, file layout, state change, or comparison.
---

# Visual Explanations

Turn the current topic into one visual that makes the relevant structure, sequence, ownership, or difference clear.

## Boundary

Use this skill for explanatory visuals in the current conversation.

Do not use it to:

- design or implement a production interface
- validate rendered UI or screenshots
- create several visual formats when one answers the question
- invent names, paths, calls, states, or behavior not supported by the available evidence

## Choose One Format

| Need | Use |
| --- | --- |
| Algorithm, conditional logic, or state transition | Pseudocode |
| Call path or runtime control flow | Indented call tree |
| Component, module, or file ownership | Shallow tree |
| Interaction or data flow among actors | Mermaid diagram |
| Proposed change to an existing known shape | Focused `diff` |
| Dense comparison, layout, or concept that needs spatial grouping | Focused HTML, only when the user asks for it or the runtime can preview it |

Choose the simplest format that shows the point. Use a text tree instead of Mermaid when ordering and relationships remain clear. Use a whole code block when omitted context would hide ownership, order, or a copyable target shape.

## Build the Visual

1. Identify the question the visual must answer.
2. Extract only the verified calls, files, props, states, actors, or branches needed to answer it.
3. Create one labeled visual next to the short statement it supports.
4. Add one or two sentences that explain the visual's key point, when the visual does not stand alone.
5. Mark missing information as unknown. Do not fill gaps with plausible architecture.

## Accuracy Gate

Before sending, confirm:

- [ ] The selected format matches the question.
- [ ] Labels, ordering, and relationships match supplied evidence.
- [ ] The visual contains no unrelated detail.
- [ ] Exactly one visual is used unless the user requests alternatives or comparison.
- [ ] HTML is optional and does not assume a browser, shell command, file path, or preview capability.
