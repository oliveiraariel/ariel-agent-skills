# Source Analysis and Architecture Rationale

Current identity: **`web-frontend-design`** (`0.2.0`).

This skill is an independent synthesis of several frontend-design projects. Its core is deliberately **framework-neutral for browser-based interfaces**. WordPress is implemented as an optional first-class platform adapter rather than being part of the skill identity.

The complete research snapshot from the original `0.1.0` release is preserved in [`source-analysis-v0.1.md`](./source-analysis-v0.1.md) for provenance, observed upstream SHAs, licensing notes, and the detailed keep/reject rationale.

## Current architectural interpretation

The skill has four conceptual layers:

```text
web-frontend-design
├── design / UX core
├── web-platform behavior
│   ├── responsive design
│   └── accessibility
├── project/framework adaptation
│   └── preserve the real stack; do not impose one
└── optional platform adapters
    └── WordPress
```

The design/UX and web-platform layers apply across web frameworks and server languages. React, Vue, Angular, Svelte, Next.js, Nuxt, Laravel Blade, Django templates, Rails, ASP.NET, Java template systems, Go/Rust web stacks, and plain HTML/CSS/JavaScript can all use the core guidance because the skill does not require a particular rendering framework or styling library.

WordPress requires dedicated guidance because its block/theme/plugin/admin architecture introduces platform-specific ownership, editor/frontend parity, Global Styles, hooks, asset enqueueing, updateability, and version-sensitive APIs. Those rules remain isolated in [`wordpress-adapter.md`](./wordpress-adapter.md) and should be loaded only when WordPress is actually present.

The skill does **not** claim equal expertise for native mobile or desktop UI frameworks such as SwiftUI, Jetpack Compose, Flutter native, WPF, Qt, or JavaFX. Those platforms need their own interaction, accessibility, layout, lifecycle, and platform conventions.

## Research basis

The original research pass revalidated these sources:

| Source | Main contribution used here |
|---|---|
| Anthropic `frontend-design` | subject-grounded visual direction, anti-template critique, bounded design review |
| UI/UX Pro Max | progressive disclosure, stack detection, UX/accessibility/responsive coverage |
| `make-interfaces-feel-better` | architecture-preserving polish, optical detail, bounded review |
| Vercel `web-design-guidelines` | code-centric web interface audit and high-signal findings |
| Impeccable | lifecycle/hardening, surface classification, bounded QA |
| Taste Skill v2 | brief inference and anti-generic visual direction, used only within its appropriate scope |

The current skill does not vendor those projects and does not require them at runtime. If installed separately, they may be invoked only as bounded specialists under the authority of the current project, user brief, accessibility requirements, and architecture.

## Decisions retained from the research

- design must be driven by product, audience, task, content, and existing brand evidence rather than model defaults;
- the current project's framework, component system, and styling architecture are preserved unless migration is explicitly in scope;
- responsive design and accessibility are core design gates rather than late patches;
- platform-specific rules are disclosed only when their platform is detected;
- normative requirements, platform guidance, and author heuristics remain distinct;
- audit and polish are bounded by evidence and completion criteria;
- framework defaults from external skills are not promoted into universal rules.

## Rename rationale

The original name, `frontend-design-wordpress`, correctly reflected the presence of a deep WordPress adapter but overstated WordPress in the skill's identity. The implementation was already broader: its design, responsive, accessibility, audit, and visual-quality rules were framework-neutral.

Version `0.2.0` therefore renames the skill to **`web-frontend-design`**. The rename changes discovery and routing semantics, not the underlying design philosophy:

```text
old interpretation risk:
frontend-design-wordpress
→ may look WordPress-only

current architecture:
web-frontend-design
→ general web frontend design authority
   + optional WordPress adapter
```

This naming matters for orchestrated selection: an agent or Adaptive AI Orchestrator should be able to select the skill for a React, Vue, Django, Laravel, or other web project without a WordPress keyword being treated as a prerequisite.

## Standards and platform sources

The active skill continues to use:

- WCAG 2.2 as the normative accessibility baseline;
- browser/web-platform behavior for responsive and semantic implementation;
- current WordPress Developer/Make Core documentation when the WordPress adapter is active.

Version-sensitive platform recommendations must be revalidated against the actual target environment before being treated as available.

## Provenance and licensing

The repository skill is MIT-licensed under this repository's license. That license covers the independently written material here; it does not relicense upstream projects.

Do not copy upstream skill files into this repository without separately satisfying their licenses and attribution/NOTICE obligations. Prefer linking to upstream projects or installing them as optional external specialists.
