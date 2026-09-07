# Design Quality and Visual Direction

This reference translates the strongest recurring ideas from the researched design skills into a framework-neutral, WordPress-aware design process.

## 1. Design from the brief, not from the model's habits

Before visual work, identify:

- subject/product;
- audience;
- primary task;
- brand evidence;
- emotional/visual language;
- information density;
- accessibility and trust constraints;
- existing visual system that must be preserved.

A design should be explainable in terms of these inputs. If the same design could be dropped onto five unrelated products with only the logo changed, the visual direction is probably under-specified.

## 2. Distinctive does not mean decorative

Distinctiveness can come from:

- typography;
- proportion and whitespace;
- information architecture;
- an unusual but useful layout relationship;
- photography/illustration/art direction;
- color restraint;
- interaction behavior;
- data presentation;
- copy tone;
- one memorable component or moment.

Do not spend visual emphasis everywhere. One strong idea usually benefits from quiet supporting structure.

## 3. Surface mode changes the priority

### Marketing

Prioritize:

1. message clarity;
2. brand identity;
3. visual hierarchy;
4. trust/evidence;
5. primary conversion action;
6. purposeful visual signature;
7. performance and accessibility.

### Application

Prioritize:

1. task completion;
2. state clarity;
3. information hierarchy;
4. consistency and predictability;
5. data legibility;
6. keyboard/touch operation;
7. responsive behavior;
8. restrained brand expression;
9. polish.

Do not apply landing-page visual theatrics to repetitive operational workflows.

### Content

Prioritize comprehension, navigation, typography, reading rhythm, anchors, hierarchy, and content width.

### Showcase

The work/artifact may dominate the interface, but navigation, accessibility, and performance still need a quality floor.

## 4. Typography

Choose typography based on brand, content, language, density, and platform—not a universal font blacklist or favorite pair.

Define roles, not just font names:

- display/hero when needed;
- heading hierarchy;
- body;
- labels/control text;
- numeric/data text;
- code/monospace only where semantically useful.

Verify:

- actual glyph coverage and localization needs;
- body readability;
- heading wrapping;
- numeric alignment for dynamic financial/data values;
- font loading behavior;
- fallback metrics;
- contrast and weight in light/dark contexts.

Avoid using typography effects solely because they are common in current AI-generated design.

## 5. Spacing and geometry

Build a coherent spacing rhythm rather than random local values.

- nearby items should look related;
- sections should have stronger separation than elements inside them;
- nested surfaces should have geometrically/optically coherent radii and padding;
- repeated components should share rules;
- dense application surfaces need tighter but still legible spacing than marketing pages.

Optical alignment can legitimately differ from mathematical centering when icon shapes or typography make geometric centering look wrong.

## 6. Color

Use semantic roles:

- background/surface;
- foreground/text;
- muted/supporting text;
- border/divider;
- accent/action;
- success/warning/error/info;
- focus;
- selection/active;
- chart/data series when needed.

Do not use raw brand colors directly in every component if semantic tokens would make states and theming safer.

A muted palette is not automatically professional; a saturated palette is not automatically childish. Judge by product, audience, contrast, and hierarchy.

## 7. Cards, borders, and surfaces

A surface needs a reason: grouping, hierarchy, interaction, elevation, or containment.

Avoid card-on-card layouts when whitespace or a divider would communicate structure better.

Use borders for structure/state and shadows/elevation when depth is actually needed. Do not apply identical shadows, radii, and cards to every section merely to create visual consistency.

## 8. Icons

- Prefer one coherent icon family per surface/project unless the design system explicitly mixes families.
- Match icon optical weight to nearby text/control weight.
- Use SVG/icon components that inherit color when practical.
- Do not use emoji as a substitute for interface icons unless the product language intentionally uses emoji.
- Icon-only controls still require an accessible name.
- Active/inactive states should remain understandable without color alone.

## 9. Motion

Motion should explain state, hierarchy, continuity, or causality.

Prefer:

- feedback after user action;
- transitions that preserve spatial context;
- a small number of intentional entrance moments;
- interruptible interaction transitions;
- reduced-motion alternatives.

Avoid:

- animating every card/section on scroll;
- long decorative delays in routine workflows;
- animation as the only state signal;
- `transition: all`;
- continuous motion with no product purpose.

Do not impose one fixed duration/scale value globally. Tune to control size, frequency, platform, and interaction purpose.

## 10. States are part of the design

For interactive UI, design at least the states relevant to the component:

- default;
- hover where hover exists;
- focus-visible;
- active/pressed;
- disabled;
- loading;
- success;
- warning/error;
- selected/current;
- empty;
- destructive confirmation;
- long-content/overflow;
- offline/failed request if applicable.

A beautiful default state with undefined error/loading/focus behavior is incomplete frontend design.

## 11. Redesign protocol

Before redesigning an existing interface, separate:

### Preserve

- product facts;
- navigation/routes unless scope says otherwise;
- user tasks and capabilities;
- existing brand assets explicitly retained;
- content the user did not authorize replacing;
- platform constraints;
- accessibility behavior that already works.

### Reconsider

- layout;
- hierarchy;
- visual tokens;
- typography;
- density;
- surface treatment;
- navigation presentation;
- component composition;
- motion;
- responsive strategy.

Do not quietly change business meaning or invent marketing claims while redesigning.

## 12. Polish protocol

Polish is a bounded pass after structure works. Inspect:

- inconsistent padding/gaps;
- awkward wrapping;
- optical alignment;
- nested radius relationships;
- visual weight of icons;
- number alignment;
- image edges/cropping;
- focus/hover/pressed states;
- motion restraint;
- loading/error/empty states;
- mobile/intermediate widths;
- dark/theme variants when present.

If the project has browser animation tooling, slow motion can reveal subtle timing/easing problems; use that as evidence, not as a mandatory requirement.

## 13. Anti-template self-critique

Before shipping a visually expressive surface, ask:

- Which decisions come directly from this product/brief?
- Which decisions are just current design fashion?
- Is any decoration pretending to be information?
- Is there one clear visual priority?
- Did I accidentally reuse a familiar AI layout pattern without justification?
- Would removing one effect improve hierarchy?
- Does the mobile version preserve the same design intent rather than merely stack everything?

Revise only where these questions reveal a concrete weakness; do not chase novelty for its own sake.
