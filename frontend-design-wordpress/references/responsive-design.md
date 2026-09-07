# Responsive Design

Responsive behavior is part of the design contract, not a patch added after desktop implementation.

## 1. Start with content priorities

Before choosing breakpoints, identify:

- what must remain visible on small screens;
- what can wrap, stack, collapse, scroll, or move behind disclosure;
- what must keep its relationship to nearby labels/actions;
- what is dense by necessity and what is dense only because of desktop habits.

Do not preserve a desktop composition at the expense of readability or interaction.

## 2. Prefer intrinsic layout

Use CSS capabilities that adapt naturally before adding viewport-specific overrides:

- Grid and Flexbox;
- `minmax()`, `auto-fit`, `auto-fill`;
- `min()`, `max()`, `clamp()` where appropriate;
- sensible `min-width: 0` on flex/grid children that must shrink;
- `max-width` for readable content;
- responsive images and intrinsic aspect ratios;
- wrapping and content-aware gaps;
- container queries when component behavior should depend on available container space rather than the whole viewport.

Avoid complex width arithmetic and fixed pixel dimensions when the layout can express the same intent intrinsically.

## 3. Breakpoints are evidence, not fashion

Do not copy a framework's default breakpoints into an unrelated project unless the project already uses them.

Choose or preserve breakpoints based on where the composition stops working:

1. narrow mobile;
2. wide mobile/small tablet where needed;
3. tablet/intermediate layout;
4. desktop/content max-width;
5. wide layouts only when the product truly benefits.

Test widths between named breakpoints. A layout that works only at 375 px and 1440 px is not responsive.

## 4. Typography

- Use a readable base size and line height appropriate to the font and content.
- Keep text measure comfortable; avoid full-width long paragraphs on large displays.
- Allow headings to wrap naturally; test long product names and translations.
- Fluid type can use `clamp()` but should not create extreme jumps or tiny small-screen text.
- Do not fix container heights around text.
- Check zoom and browser text scaling.

## 5. Navigation

For narrow screens:

- preserve the primary destination/action;
- avoid shrinking desktop navigation until labels become unusable;
- use disclosures/drawers only when they reduce cognitive and spatial load;
- ensure menu triggers and items remain keyboard accessible;
- manage focus when modal/drawer navigation opens and closes;
- avoid hover-only submenus.

## 6. Forms

- Prefer single-column flow on narrow screens unless paired fields truly benefit from a row.
- Keep visible labels with controls.
- Ensure input, helper, error, and action text can wrap.
- Do not make submit actions disappear below fixed overlays or keyboards.
- Use appropriate input types and `inputmode`.
- Check date, currency, select, autocomplete, and validation behavior on touch devices.

## 7. Tables and dense data

Choose a strategy based on the information relationship, not a generic "turn rows into cards" rule.

Possible strategies:

- preserve the table with controlled horizontal scroll when column relationships are essential;
- freeze or repeat key identifiers;
- hide only genuinely secondary columns, with a way to access them;
- switch to labeled stacked rows when each record is independently understandable;
- use summary + detail disclosure;
- provide a dedicated narrow-screen view for complex operational tables.

Never destroy header/value relationships or remove financially/operationally important data just to avoid horizontal scrolling.

## 8. Cards, grids, and sidebars

- Cards should wrap based on minimum useful content width, not arbitrary equal-column counts.
- A sidebar may become a disclosure, top section, bottom section, or persistent narrow rail depending on task priority.
- Avoid nested cards merely to preserve desktop grouping.
- Do not let decorative min-widths force page overflow.

## 9. Media and images

- Use intrinsic dimensions/aspect ratios to prevent layout shifts.
- Provide appropriately sized responsive image sources when the platform supports them.
- Avoid background images containing essential text.
- Crop intentionally with `object-fit` only when the focal content survives the crop.
- Test portrait and landscape content, not one ideal asset.

WordPress already provides responsive image features for media; do not replace them with a custom image pipeline without a project-specific reason.

## 10. Viewport height and safe areas

- Prefer modern dynamic viewport units where full-height UI truly needs them; verify target-browser support/fallbacks.
- Account for mobile browser chrome and on-screen keyboards.
- Respect safe-area insets for fixed/full-bleed controls on devices with display cutouts.
- Do not pin critical controls behind sticky headers/footers.

## 11. Overflow diagnosis

When horizontal overflow appears:

1. identify the element wider than its containing block;
2. inspect fixed widths, `min-width`, long tokens/URLs, transformed elements, tables, images, negative margins, and full-bleed rules;
3. fix the source;
4. use scrolling at the component level only when the content legitimately requires it.

Do not start with global `overflow-x: hidden`; that can hide broken content and focus indicators.

## 12. WordPress responsive behavior

WordPress layout may combine:

- theme content/wide sizes;
- block alignment (`wide`, `full`);
- Global Styles and `theme.json`;
- block-specific CSS;
- plugin CSS;
- builder-generated responsive rules.

### WordPress 7.1+

WordPress 7.1 introduced responsive block style states for `@mobile` and `@tablet` in Global Styles and individual block instances. It also introduced configurable top-level `settings.viewport` breakpoints. Core defaults are 480px mobile and 782px tablet unless valid theme settings replace them.

Treat those values as WordPress defaults, **not** as universal design breakpoints. Use them when the site's Global Styles strategy owns responsive block styling; otherwise preserve the project's real responsive system.

### WordPress 7.0 and earlier

Do not generate `@mobile`, `@tablet`, or `settings.viewport` responsive-style instructions as if they were available in core. Use the existing theme/plugin strategy, CSS media queries, container queries, or a compatible Gutenberg feature only when the installed environment actually provides it.

Before relying on version-sensitive WordPress/Gutenberg behavior, detect the target version and theme strategy. Do not duplicate the same responsive rule across Global Styles and unrelated CSS without a deliberate compatibility reason.

## 13. Minimum responsive verification matrix

When tools permit, verify at least:

| Area | Narrow | Intermediate | Desktop |
|---|---|---|---|
| Navigation | usable, no hidden primary action | no awkward transition state | full intended hierarchy |
| Typography | readable, wraps | stable scale | controlled line length |
| Forms | labels/errors/actions fit | paired fields intentional | efficient layout |
| Tables/data | relationships preserved | no accidental clipping | density appropriate |
| Media | no overflow/crop failure | stable | correct dimensions |
| Dialogs/overlays | fit viewport, focus visible | stable | stable |

Also test long content, empty content, large text, and at least one real interaction state.

## 14. Version-sensitive source

For WordPress 7.1 responsive block styles and configurable viewports, revalidate against:

https://make.wordpress.org/core/2026/08/05/responsive-block-styles-and-configurable-viewports-in-wordpress-7-1/