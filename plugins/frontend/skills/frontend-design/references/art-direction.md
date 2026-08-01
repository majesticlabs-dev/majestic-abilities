# Art Direction

Use this reference to commit to a visual direction before any layout or component work begins. Direction is a decision, not a mood. Make it explicit, write it down, then let every later choice answer to it.

## Direction Questions

1. What is the interface trying to achieve, and for whom?
2. Who uses it repeatedly, and what does repetition demand?
3. What tone should it communicate in one sentence?
4. What would make it recognizable next to a generic generated UI?

Request missing information only when it blocks correct execution. Otherwise state the assumption and proceed.

## Commit To One Direction

Pick one direction and execute it precisely. Bold maximalism and severe restraint are both valid. Averaging several directions is not.

Vary direction across builds. Two interfaces produced from similar prompts should not converge on the same fonts, palette, layout skeleton, and energy level. Treat repetition of a previous build's choices as a defect.

| Direction | Signals | Signature move |
| --- | --- | --- |
| Editorial | Asymmetric grids, typographic authority, dramatic whitespace | Oversized headline breaking the column grid |
| Neo-brutalist | Hard edges, utilitarian labels, exposed structure | Visible borders and raw system labels as decoration |
| Minimalist | Restrained, precise, essential | Hierarchy carried by spacing alone |
| Luxury | Spacious, premium materials, invisible complexity | Slow, confident motion and deep negative space |
| Maximalist | Layered, expressive, dense | Overlapping planes with controlled collision |
| Retro-futurist | Phosphor glow, angular geometry, mechanical rhythm | Scanline or CRT treatment tied to state |
| Organic tactile | Paper grain, irregular shapes, handmade warmth | Hand-cut edges and off-axis alignment |
| Punk zine | Collage energy, raw texture, deliberate imperfection | Photocopy contrast and taped-on elements |
| Bauhaus | Geometric discipline, functional clarity, primary color | Strict geometry with one primary accent |
| Psychedelic | Vivid contrast, fluid forms, controlled chaos | Warped type or flowing gradient fields |
| Playful | Animated, colorful, responsive to input | Character-driven feedback on interaction |

## Signature Element

Every build includes one memorable hook that does real work. Decorative flourishes do not qualify. The hook must carry function: navigation, hierarchy, feedback, discoverability, or comprehension.

Valid categories:

- morphing frame or border that responds to scroll position or component state
- typographic hero with deliberate kerning and optical rhythm
- navigation with spatial logic and animated affordances
- cursor behavior that improves discoverability
- texture system that reinforces hierarchy and focus
- branded data visualization language
- orchestrated scroll-triggered reveal with meaningful timing

Name the signature element in the art direction brief and point to where it lives in the code.

## Texture And Material

Flat sterile backgrounds are acceptable only when austerity is the stated direction. Otherwise give surfaces material.

Rules:

- texture supports hierarchy and focus, it does not add noise
- depth language stays consistent across the whole system
- glass effects are either fully committed and readable, or absent

Techniques that hold up in production:

- subtle grain overlay
- SVG parametric patterns
- noise-driven gradients
- paper fold shadows
- CRT scanlines for retro directions
- procedural canvas texture when the performance budget allows

Heavy techniques (canvas, WebGL, particles) require lazy initialization and a reduced-motion fallback. See `web-interface-standards.md`.

## Narrative Consistency

The build fails this test if any of the following is true:

- typography, motion, layout, and copy feel authored by different systems
- components are individually polished but conceptually unrelated
- microcopy tone contradicts the chosen direction

Every element reinforces the same story, mood, and intent.

## Authored Copy

All copy is written for this product, in the established voice. The build fails if any of the following is present:

- lorem ipsum or filler text
- vague marketing language with no product context
- empty states with no guidance toward the next action
- labels or helper text that ignore the established voice

## Anti-Patterns

Reject the output if any of these are true:

- default system fonts carry the entire identity
- purple or blue-purple gradient on white is the main visual idea
- centered hero, three feature cards, icon row
- rounded corners and subtle shadows applied uniformly everywhere
- emoji used as interface icons
- default framework appearance with minimal tokenization
- chat interfaces built as generic bubbles with no branded concept
- motion added because it was easy, not because it communicates
- missing focus states or keyboard access
- no error or loading states
- the result resembles a marketplace template
