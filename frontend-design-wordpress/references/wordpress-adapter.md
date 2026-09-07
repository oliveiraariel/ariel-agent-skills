# WordPress Adapter

Use this reference whenever the target runs in WordPress. The goal is to make frontend design native to the site's actual WordPress architecture instead of pasting framework assumptions on top of it.

## 1. Identify the WordPress surface

Classify before editing:

| Surface | Primary integration points | Design implications |
|---|---|---|
| Block theme / Site Editor | `theme.json`, templates, template parts, patterns, block styles | Global design tokens and editor/frontend parity matter most. |
| Classic theme | `style.css`, PHP templates, `functions.php`, hooks, enqueued assets | Respect theme hierarchy and existing PHP/CSS architecture. |
| Custom Gutenberg block | `block.json`, edit/save or server render, block supports, block styles | Editor state and frontend output must remain semantically and visually coherent. |
| Plugin-rendered frontend | plugin templates/shortcodes/blocks, scoped CSS/JS, conditional enqueue | Avoid relying on theme internals unless the plugin explicitly integrates with them. |
| Page builder | builder-native structure/styles plus theme constraints | Avoid brittle overrides; keep changes compatible with the builder's generated markup. |
| Custom HTML block/content | local wrapper + scoped CSS, minimal JS | Treat as constrained embedding, not a substitute for maintainable theme/plugin code. |

If more than one surface is involved, identify which layer owns global tokens and which layer owns the component being changed.

## 2. WordPress-wide rules

- Never modify WordPress core files.
- Preserve the active theme/plugin architecture unless the user explicitly requests an architectural migration.
- Prefer WordPress APIs, hooks, block supports, Global Styles, and asset enqueueing over hard-coded workarounds.
- Do not put project-wide CSS into a single page's Custom HTML block when proper theme/plugin access exists.
- Avoid unscoped selectors such as `.button`, `h2`, or `table` in plugin/custom-HTML styles unless the project intentionally owns those globals.
- Keep editable content editable. Do not hard-code user-managed copy into PHP/CSS/JS merely to reproduce a mockup.
- Frontend code that emits dynamic WordPress data must follow appropriate escaping and output-safety conventions; frontend design does not exempt code from WordPress security standards.
- Preserve plugin/theme updateability. Avoid edits to third-party vendor files that will be overwritten by updates.

## 3. Block themes and `theme.json`

When a block theme or Global Styles is the design authority:

1. Read the existing `theme.json` before defining new tokens.
2. Reuse semantic presets for color, typography, spacing, layout, shadow, and other supported design properties.
3. Prefer changes at the narrowest correct scope: global → element → block → style variation.
4. Keep editor and frontend output visually aligned.
5. Avoid duplicating the same token in `theme.json` and unrelated CSS unless a browser/feature fallback requires it.
6. Before using newer Global Styles capabilities, confirm the WordPress/Gutenberg version used by the project.

Current WordPress developer documentation supports responsive Global Styles scoped to named mobile/tablet viewports. Treat this as a platform capability, not permission to scatter arbitrary breakpoint values. Reuse the project's viewport settings and verify generated frontend behavior.

## 4. Classic themes

For classic themes:

- locate the relevant template and stylesheet before editing;
- enqueue styles/scripts through WordPress rather than injecting duplicate `<link>` or `<script>` tags into arbitrary templates;
- preserve template hierarchy, hooks, and child-theme strategy;
- if the active theme is third-party and must remain updateable, prefer a child theme or plugin-level customization over direct vendor edits;
- do not migrate to a block theme simply because the design would be easier there.

## 5. Gutenberg blocks

For custom blocks:

- use semantic markup and appropriate block supports before inventing custom controls;
- preserve editor/frontend parity for spacing, typography, colors, alignment, states, and responsive behavior;
- decide intentionally between static saved markup and dynamic/server rendering;
- avoid storing presentational duplication in attributes when the design can come from presets/supports;
- ensure keyboard operation and accessible labels for custom controls;
- test both the editor experience and rendered frontend;
- avoid JavaScript-driven layout when CSS Grid/Flexbox/intrinsic layout is sufficient.

## 6. Plugin frontend UI

Plugin UIs often live inside themes they do not control. Therefore:

- wrap the plugin surface in a stable namespace/class and scope styles beneath it;
- use semantic CSS custom properties for plugin-owned tokens when theme tokens are unavailable;
- inherit sensible typography/colors from the theme when compatible, but explicitly define states that must remain accessible;
- enqueue assets only where needed when feasible;
- do not reset the entire page or override global theme selectors to make one plugin screen work;
- account for both narrow content columns and full-width templates.

For application-like plugins, prioritize form semantics, data readability, state feedback, focus management, table behavior, and dense-layout responsiveness over marketing-page aesthetics.

## 7. Page builders and Custom HTML

Treat these as constrained environments.

For page builders:

- inspect the actual generated markup/classes before writing overrides;
- prefer builder-native responsive and design controls when they produce maintainable output;
- use custom CSS only for gaps the builder cannot express cleanly;
- verify the published frontend, not only the editor preview.

For Custom HTML:

- add a unique root wrapper;
- scope all custom selectors to that wrapper;
- keep CSS responsive and content-tolerant;
- avoid fixed widths/heights that work only in the editor canvas;
- avoid scripts that depend on undocumented editor DOM;
- if the component grows beyond a contained snippet, recommend moving it into theme/plugin code rather than expanding an unmaintainable blob.

## 8. Responsive WordPress implementation

WordPress can introduce nested content widths, block alignment rules, editor wrappers, and theme spacing. Diagnose overflow at the actual source instead of hiding it globally.

Check:

- `alignwide` / `alignfull` behavior;
- content and wide-size constraints;
- nested Group/Columns/Grid blocks;
- images/video intrinsic sizing;
- tables and long unbreakable values;
- admin bar/sticky headers when evaluating focus and viewport height;
- block gap and preset spacing interactions;
- responsive styles saved in Global Styles versus CSS media/container rules.

Do not use `overflow-x: hidden` as the primary fix for unknown overflow; identify the offending element first.

## 9. Accessibility and WordPress

WordPress's own coding standards expect new/updated ecosystem interfaces to target WCAG 2.2 AA. Follow `references/accessibility.md` and additionally verify:

- editor-generated heading order after templates/patterns are composed;
- navigation block/menu keyboard behavior;
- visible focus against theme colors;
- form plugin markup rather than assuming the plugin emits accessible labels/errors;
- alt text behavior for media managed through WordPress;
- landmark structure across header/main/navigation/footer template parts.

## 10. Source anchors

Revalidate implementation details against current official documentation when platform versions matter:

- Theme Handbook: https://developer.wordpress.org/themes/
- `theme.json`: https://developer.wordpress.org/themes/global-settings-and-styles/introduction-to-theme-json/
- Block Editor Handbook: https://developer.wordpress.org/block-editor/
- Global Settings & Styles: https://developer.wordpress.org/block-editor/how-to-guides/themes/global-settings-and-styles/
- WordPress Coding Standards: https://developer.wordpress.org/coding-standards/wordpress-coding-standards/
- WordPress Accessibility Coding Standards: https://developer.wordpress.org/coding-standards/wordpress-coding-standards/accessibility/

Platform documentation changes. When a recommendation depends on a recently added WordPress/Gutenberg feature, confirm the project's installed version before treating the feature as available.
