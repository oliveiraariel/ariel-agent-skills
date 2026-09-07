# Frontend Design + WordPress Skill

A portable Agent Skill for designing, implementing, reviewing, and refining frontend interfaces with first-class support for **UI/UX, responsive design, accessibility, and WordPress**.

## Purpose

Most frontend-design skills are either aesthetically focused, tied to a JavaScript framework, or specialized in auditing/polish. This skill separates **design judgment** from **platform implementation** so an agent can work naturally in WordPress without defaulting to React, Next.js, Tailwind, or another unrelated stack.

It is designed for:

- web applications and dashboards;
- landing/marketing pages;
- content sites;
- WordPress block themes and Global Styles;
- classic themes;
- Gutenberg blocks;
- plugin-rendered frontend interfaces;
- page-builder or Custom HTML constraints;
- redesigns;
- responsive/accessibility remediation;
- frontend audit and final polish.

## Design principles

1. **Brief first** — product, audience, task, brand, and constraints drive design.
2. **Detect the real stack** — never replace or duplicate the project's styling architecture by default.
3. **Application UI is not a landing page** — data-heavy/task-heavy surfaces prioritize clarity and operation over visual spectacle.
4. **Responsive by design** — narrow/intermediate/desktop behavior is planned, not patched later.
5. **Accessibility is a gate** — WCAG 2.2 AA and WordPress accessibility standards are baseline targets.
6. **WordPress is an architecture, not an export target** — choose the correct theme/block/plugin/builder integration layer.
7. **Polish follows structure** — hierarchy and usability come before micro-effects.
8. **Verification is bounded and evidence-based** — report what was actually inspected/tested.

## Structure

```text
frontend-design-wordpress/
├── SKILL.md
├── README.md
├── references/
│   ├── accessibility.md
│   ├── audit-checklist.md
│   ├── design-quality.md
│   ├── responsive-design.md
│   ├── source-analysis.md
│   └── wordpress-adapter.md
└── scripts/
    └── validate_skill.py
```

`SKILL.md` is the agent entry point. References are loaded only when the task requires them.

## Task modes

The skill routes work through five modes:

- **Design** — establish a new frontend direction.
- **Build** — implement an approved/inferable direction.
- **Redesign** — materially replace visual structure while preserving product truth.
- **Polish** — improve an existing interface without replacing its identity.
- **Audit** — inspect and report with explicit scope/evidence.

It also classifies the surface as **Marketing**, **Application**, **Content**, or **Showcase** so the same aesthetic behavior is not applied to every product surface.

## WordPress modes

The WordPress adapter distinguishes:

- block theme / Site Editor;
- classic theme;
- custom Gutenberg block;
- plugin-rendered frontend;
- page builder;
- Custom HTML/constrained embed.

This prevents recommendations such as "rewrite in Next.js" or "add Tailwind" when the actual task is a WordPress plugin/theme interface.

## Research basis

The architecture was developed after revalidating six notable frontend design skills/projects:

- Anthropic `frontend-design`;
- UI/UX Pro Max;
- `make-interfaces-feel-better`;
- Vercel `web-design-guidelines`;
- Impeccable;
- Taste Skill v2.

See [`references/source-analysis.md`](./references/source-analysis.md) for the detailed comparison: strengths, limits, ideas adopted, ideas intentionally rejected, current upstream paths, and licensing/provenance policy.

The WordPress layer additionally uses primary WordPress Developer documentation and W3C WCAG 2.2 as standards sources.

## External skills are optional

This skill does not vendor or require the six researched skills. If an agent runtime already has them installed, `SKILL.md` defines bounded delegation roles for them. Without them, this skill remains fully usable.

That makes it suitable for portable skill ecosystems, including agent runtimes that understand `SKILL.md`, without binding the core workflow to a Claude-specific directory or a React-specific toolchain.

## Validation

From the repository root:

```bash
python frontend-design-wordpress/scripts/validate_skill.py
```

The validator checks the skill frontmatter and required reference files. It has no external Python dependencies.

## Status

**Initial structured version / in development.**

The next maturation steps should be empirical: use the skill on real WordPress application, content, and marketing surfaces; collect failure patterns; then improve the rules based on observed gaps rather than adding generic design advice.
