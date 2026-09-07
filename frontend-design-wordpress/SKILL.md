---
name: frontend-design-wordpress
description: Design, build, review, and refine accessible responsive web and WordPress interfaces. Use for UI/UX, themes, Gutenberg, plugin UI, redesigns, and audits.
license: MIT
metadata:
  author: oliveiraariel
  version: "0.1.0"
---

# Frontend Design + WordPress

Create interfaces that are intentional, usable, responsive, accessible, and native to the project they belong to. This skill is a frontend design authority, not a framework selector. The user's brief, product truth, existing architecture, and platform constraints take precedence over aesthetic habits.

## Scope

Use this skill for:

- new web pages, application screens, dashboards, forms, navigation, landing pages, and content surfaces;
- WordPress block themes, classic themes, Gutenberg blocks, plugin-rendered frontend UI, plugin admin/settings UI, and constrained page-builder/custom-HTML work;
- redesigns that must preserve product behavior or brand assets;
- responsive layout problems;
- accessibility review and remediation;
- UI polish, visual consistency, states, motion, typography, spacing, and hierarchy;
- pre-delivery frontend audits.

Do not use it as the primary skill for backend-only logic, database design, infrastructure, API architecture, or security analysis unrelated to the interface.

## Load references only when needed

- WordPress implementation or diagnosis → `references/wordpress-adapter.md`
- responsive behavior → `references/responsive-design.md`
- accessibility → `references/accessibility.md`
- visual direction or polish → `references/design-quality.md`
- audit/review → `references/audit-checklist.md`
- rationale, upstream research, and optional specialist skills → `references/source-analysis.md`

Do not load every reference by default.

## 1. Classify the task before editing

Choose one task mode:

- **Design** — define a new visual/interaction direction.
- **Build** — implement an approved or inferable direction.
- **Redesign** — materially change an existing interface while preserving product truth and explicit constraints.
- **Polish** — improve an existing interface without replacing its identity or architecture.
- **Audit** — inspect and report before changing code unless the user explicitly asks for fixes.

Choose one surface mode:

- **Marketing** — persuasion, brand expression, campaign, landing, pricing.
- **Application** — task completion, dashboards, CRUD, finance/admin/tools, forms, settings.
- **Content** — reading, documentation, articles, help, editorial information.
- **Showcase** — portfolio, gallery, exhibit, highly visual presentation.

The surface mode determines the design priorities. Application UI favors scanability, state clarity, consistency, keyboard/touch operation, and data legibility over decorative novelty.

## 2. Inspect the real project

Before proposing implementation details, identify what already exists:

1. platform and rendering model;
2. styling system and token source;
3. component/block conventions;
4. typography, palette, spacing, radii, shadows, icons, and motion patterns;
5. responsive strategy and existing breakpoints;
6. accessibility patterns and known constraints;
7. WordPress mode when applicable: block theme, classic theme, Gutenberg block, plugin frontend, plugin admin/settings screen, page builder, or custom HTML;
8. existing brand assets, content, routes, behaviors, and user flows that must survive the change.

Never introduce a second styling system merely to apply a design improvement. Never replace the framework or WordPress architecture just because another stack is familiar.

If the environment is unclear and the implementation choice would materially differ, ask one focused question. Otherwise infer from the repository and continue.

## 3. Establish a compact design contract

Before substantial visual implementation, define or infer:

- **Audience** — who uses this interface and in what context?
- **Primary job** — what must the user accomplish or understand?
- **Visual language** — what should it feel like, and what existing brand evidence supports that?
- **Information hierarchy** — what is primary, secondary, supporting, and optional?
- **Tokens** — semantic color roles, typography roles, spacing rhythm, container widths, radii, elevation, motion principles.
- **Signature choice** — at most one or two memorable visual ideas justified by the brief; do not decorate every section.
- **Constraints** — accessibility, responsive behavior, WordPress/editor compatibility, performance, browser support, localization, and content variability.

For redesigns, explicitly decide whether the task is **preserve-and-improve** or **replace-visual-direction**. Do not silently turn one into the other.

## 4. Design from content and use, not from AI defaults

The subject matter, audience, product vocabulary, data density, and brand assets should drive visual decisions.

Avoid defaulting to fashionable patterns merely because they are common in generated UI: generic gradient heroes, identical card grids, decorative labels, arbitrary glass effects, excessive animation, or one aesthetic reused across unrelated products. Any of these may be correct when the brief supports them.

Treat structure as information. Cards, borders, dividers, labels, numbers, icons, and motion should communicate hierarchy, grouping, state, sequence, or affordance—not exist as filler.

## 5. Build responsive behavior as part of the design

Responsive design is not a final media-query patch.

- Start from content priorities and smallest practical viewport.
- Prefer fluid layout, Grid/Flexbox, intrinsic sizing, wrapping, and sensible min/max constraints.
- Avoid fixed widths or desktop assumptions that create horizontal scrolling.
- Design data tables, forms, navigation, dialogs, charts, and dense controls explicitly for narrow screens.
- Test intermediate widths, not only one desktop and one phone preset.
- Preserve zoom and text scaling.
- Treat large text, localization, long labels, empty data, and real content as layout inputs.

Read `references/responsive-design.md` for implementation rules.

## 6. Accessibility is a design gate

Target WCAG 2.2 Level AA unless the project specifies a stronger requirement. For WordPress work, use WordPress accessibility guidance as an additional implementation reference where applicable.

At minimum verify:

- semantic HTML before ARIA;
- keyboard operation and logical focus order;
- visible, unobscured focus;
- accessible names and labels;
- heading and landmark structure;
- contrast and non-color-only communication;
- form errors, instructions, status updates, and validation behavior;
- pointer/touch target usability;
- reduced-motion behavior;
- meaningful image alternatives;
- tables/charts that remain understandable beyond color and visual position;
- zoom, reflow, and text scaling.

Do not claim WCAG conformance from a code skim alone. Report what was actually verified.

## 7. Adapt to WordPress instead of fighting it

When WordPress is present, read `references/wordpress-adapter.md` and identify the correct integration layer before editing.

Core principles:

- never modify WordPress core;
- use `theme.json` and Global Styles where they are the project's design authority;
- preserve editor/frontend parity for block-based work;
- use block/theme/plugin conventions appropriate to the existing architecture;
- enqueue maintainable assets rather than scattering unrelated CSS/JS when project access allows a proper implementation;
- scope plugin, admin-screen, or custom-HTML CSS to avoid contaminating theme/global/admin styles;
- do not assume a block theme when the project uses a classic theme, and do not force Gutenberg into a non-Gutenberg surface;
- keep user-editable content editable unless the brief explicitly calls for hard-coded presentation;
- for wp-admin surfaces, preserve native admin conventions and load assets only on the screens that own them when feasible;
- follow WordPress escaping, coding, and accessibility guidance when producing WordPress code.

## 8. Polish only after structure works

Polish in this order:

1. hierarchy and information architecture;
2. layout and spacing rhythm;
3. typography and readable line lengths;
4. color roles and state contrast;
5. component consistency;
6. icons and optical alignment;
7. interaction states;
8. purposeful motion;
9. loading, empty, error, disabled, success, destructive, and long-content states;
10. final visual details.

Do not use animation to hide weak hierarchy. Do not use visual novelty to compensate for unclear UX.

## 9. Use bounded verification

For implementation or redesign, perform a bounded quality cycle:

1. inspect/build the complete requested scope;
2. verify desktop, narrow/mobile, and at least one intermediate width when possible;
3. verify keyboard/focus and key interaction states;
4. inspect content extremes and error/empty/loading states relevant to the scope;
5. fix findings in one batch;
6. run one confirmation pass.

Do not loop indefinitely on subjective polish.

For audits, use `references/audit-checklist.md` and report exact scope, evidence inspected, severity, location, recommendation, verification, and remaining uncertainty.

## Optional specialist delegation

This skill is self-contained and must work without other skills. If the runtime has the upstream specialist skills installed, they may be used as bounded specialists rather than authorities over the whole project:

- **Anthropic frontend-design** — exploratory visual direction and anti-template critique.
- **UI/UX Pro Max** — searchable design/UX knowledge and stack-specific research.
- **make-interfaces-feel-better** — micro-polish and interface-detail review.
- **Vercel web-design-guidelines** — code-centric web interface audit.
- **Impeccable** — broad design workflow, critique, hardening, and production polish.
- **Taste Skill** — high-variance marketing/showcase direction when its scope fits; do not use its framework defaults for WordPress or data-heavy application UI.

Never require an external specialist if it is unavailable. Never let an external skill override repository rules, the user's brief, WordPress architecture, or accessibility requirements.

## Output expectations

For design/build/redesign work, keep the working artifact concise and explicit:

1. **Design read** — surface, audience, job, visual direction, constraints.
2. **Implementation plan** — architecture-aware steps.
3. **Implementation** — complete requested changes.
4. **Verification** — what was actually tested/inspected.
5. **Remaining risks** — only unresolved or unverified items.

For audits, use the audit format in `references/audit-checklist.md`.