# Accessibility Baseline

Use this checklist as an operational design/development gate. It is not a substitute for a formal accessibility audit or conformance evaluation.

## Standard and evidence hierarchy

Target **WCAG 2.2 Level AA** unless the project explicitly requires a stronger standard.

- **Normative accessibility source:** WCAG 2.2 — https://www.w3.org/TR/WCAG22/
- **WordPress implementation guidance:** https://developer.wordpress.org/coding-standards/wordpress-coding-standards/accessibility/

WordPress's Accessibility Coding Standards state that code integrated into the official WordPress ecosystem—including WordPress core, WordPress.org sites, and official plugins—is expected to conform to WCAG 2.2 AA. For third-party WordPress themes, plugins, and sites, this skill still uses WCAG 2.2 AA as its baseline, while treating WordPress guidance as an additional implementation reference rather than implying an official policy applies to every third-party project.

Keep these categories separate:

- **Normative requirement** — traceable to a WCAG success criterion or another standard explicitly required by the project.
- **Platform guidance** — WordPress or browser/platform conventions that improve implementation quality.
- **Usability heuristic** — a useful default that is not itself an AA requirement.

Do not present a heuristic as WCAG law.

## 1. Structure and semantics

- Use native semantic elements before ARIA: `button`, `a`, `label`, `nav`, `main`, `header`, `footer`, `table`, headings, lists.
- One interaction should have one clear semantic role.
- Heading levels communicate document structure; do not choose heading levels for visual size.
- Landmarks should cover the meaningful page structure without redundant landmark noise.
- Links navigate; buttons perform actions.
- Tables represent tabular relationships, not visual layout.

## 2. Keyboard and focus

Verify the primary flow without a mouse:

- all interactive controls are reachable;
- tab order follows the logical interaction order;
- custom widgets support expected keyboard behavior;
- focus is clearly visible;
- author-created sticky headers, footers, dialogs, banners, and overlays do not completely hide the focused control;
- opening/closing dialogs and disclosures moves or restores focus intentionally;
- focus is not trapped except within true modal contexts where trapping is appropriate;
- escape/cancel paths are available where expected.

WCAG 2.2 adds Level AA requirements such as Focus Not Obscured (Minimum). Do not treat a decorative focus style as enough if the focused control can still disappear behind fixed content.

## 3. Accessible names and instructions

- Every form control has an explicit accessible name.
- Visible labels are preferred for user-facing fields; placeholders are not labels.
- Icon-only controls have an accessible name.
- Decorative icons/images are hidden from assistive technology when appropriate.
- Instructions needed to complete a field appear before or with the interaction, not only after failure.
- Repeated controls use consistent naming.

## 4. Forms, errors, and feedback

- Error messages identify the field/problem and explain how to recover.
- Errors are associated programmatically with affected controls.
- Do not communicate validation only by color.
- After failed submission, users can locate errors efficiently; focus management may be needed.
- Loading/submitting states remain understandable.
- Important asynchronous status changes are announced using an appropriate live region or equivalent pattern.
- Destructive actions have proportionate confirmation or undo behavior.
- Do not block paste into credentials, codes, or form fields without an essential reason.

## 5. Color and contrast

- Verify text and UI contrast against actual rendered backgrounds, including hover/focus/disabled/error states.
- Do not rely on color alone for status, category, validation, chart series, or required fields.
- Preserve readable contrast in dark mode and user-customizable WordPress themes.
- Treat brand colors as inputs, not exemptions from accessibility.

Use a contrast checker rather than estimating by eye. When claiming WCAG conformance, evaluate against the WCAG 2 contrast requirements in force for the target criterion; do not substitute a different contrast model and still call the result WCAG 2.2 AA conformance.

## 6. Pointer and touch targets

WCAG 2.2 Level AA Target Size (Minimum), Success Criterion 2.5.8, uses a **24 × 24 CSS pixel** minimum with defined exceptions, including a spacing alternative for undersized targets.

For touch-heavy/mobile interfaces, prefer a more comfortable target such as approximately **44 × 44 CSS pixels** when layout permits. That is a useful usability target and also relates to the stricter WCAG Target Size (Enhanced) criterion at Level AAA; it is **not** the general WCAG 2.2 AA minimum.

Also verify:

- adjacent controls are not easily mis-tapped;
- drag/swipe interactions have non-drag alternatives unless dragging is essential;
- hover-only actions have keyboard/touch equivalents.

## 7. Reflow, zoom, and text scaling

- Never disable browser zoom with `user-scalable=no`, `maximum-scale=1`, or equivalent restrictions merely to control layout.
- Content remains usable when text is enlarged.
- Layout reflows without two-dimensional scrolling for ordinary reading/content use cases, except where two-dimensional layout is essential (for example certain data tables/diagrams).
- Long translations, large system text, validation messages, and dynamic values do not break controls.
- Avoid fixed-height text containers that clip content when font metrics change.

## 8. Images and media

- Meaningful images have concise alternatives that convey their purpose/content.
- Decorative images use empty alt text or an equivalent non-announced pattern.
- Complex charts/graphics need a textual equivalent or accessible data representation appropriate to the task.
- Captions, transcripts, and audio descriptions are provided when required by the media/content.
- Autoplaying or long-running motion/media provides appropriate pause/stop controls where required.

## 9. Motion and sensory safety

- Respect `prefers-reduced-motion` for non-essential animation as a strong implementation baseline; verify the actual WCAG criteria relevant to moving, blinking, flashing, and interaction-triggered motion when making a conformance claim.
- Motion is not the only way to communicate a state change.
- Avoid flashing or visual effects that can trigger photosensitive responses.
- Prefer user-triggered motion over continuous decorative motion.
- Keep routine interactions immediate; do not make frequent actions wait for ornamental animation.

## 10. Data-heavy application UI

For dashboards, finance/admin tools, and dense application interfaces:

- numeric columns should remain aligned and legible;
- status has text/icon semantics in addition to color;
- tables have meaningful headers and relationships;
- sortable columns communicate state;
- charts expose the underlying values or an equivalent accessible representation;
- responsive table transformations preserve relationships between labels and values;
- keyboard users can reach row actions without traversing excessive hidden controls.

## 11. WordPress-specific checks

- Test rendered frontend markup, not only the block editor preview.
- Verify heading hierarchy after patterns/template parts are composed.
- Check navigation/menu behavior with keyboard and screen-reader semantics.
- Ensure theme color customization cannot silently remove visible focus or contrast.
- Validate third-party form/plugin markup rather than assuming accessibility.
- Preserve accessible names when replacing native WordPress controls with custom styling.
- For wp-admin/plugin settings screens, verify notices, validation, focus, and control semantics after WordPress renders the complete screen.

## 12. Verification language

Do not state "WCAG compliant" or "accessible" solely because this checklist passed a source-code review.

Prefer precise statements such as:

- "Keyboard navigation and visible focus were verified on the requested flow."
- "Static review found no missing form labels in the inspected files; screen-reader behavior was not verified."
- "Contrast was checked for the documented palette; user-customized WordPress colors remain unverified."

Accessibility confidence must match the evidence actually inspected.