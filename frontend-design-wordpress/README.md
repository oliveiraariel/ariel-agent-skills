# Frontend Design + WordPress Skill

A portable Agent Skill for designing, implementing, reviewing, and refining frontend interfaces with first-class support for **UI/UX, responsive design, accessibility, and WordPress**.

**Current version:** `0.1.0` — reviewed baseline, ready for field testing.

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
- WordPress plugin admin/settings UI;
- page-builder or Custom HTML constraints;
- redesigns;
- responsive/accessibility remediation;
- frontend audit and final polish.

## Design principles

1. **Brief first** — product, audience, task, brand, and constraints drive design.
2. **Detect the real stack** — never replace or duplicate the project's styling architecture by default.
3. **Application UI is not a landing page** — data-heavy/task-heavy surfaces prioritize clarity and operation over visual spectacle.
4. **Responsive by design** — narrow/intermediate/desktop behavior is planned, not patched later.
5. **Accessibility is a gate** — WCAG 2.2 AA is the baseline; platform guidance is kept distinct from normative requirements.
6. **WordPress is an architecture, not an export target** — choose the correct theme/block/plugin/admin/builder integration layer.
7. **Polish follows structure** — hierarchy and usability come before micro-effects.
8. **Verification is bounded and evidence-based** — report what was actually inspected/tested.

## Structure

```text
frontend-design-wordpress/
├── SKILL.md
├── README.md
├── CHANGELOG.md
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
- plugin admin/settings UI;
- page builder;
- Custom HTML/constrained embed.

It is version-aware: WordPress 7.1 responsive Global Styles (`@mobile`, `@tablet`, `settings.viewport`) are not assumed to exist on older WordPress core versions.

This prevents recommendations such as "rewrite in Next.js" or "add Tailwind" when the actual task is a WordPress plugin/theme interface.

## Research basis

The architecture was developed after revalidating six notable frontend design skills/projects:

- Anthropic `frontend-design`;
- UI/UX Pro Max;
- `make-interfaces-feel-better`;
- Vercel `web-design-guidelines`;
- Impeccable;
- Taste Skill v2.

See [`references/source-analysis.md`](./references/source-analysis.md) for the detailed comparison, validation snapshot, strengths, limits, ideas adopted/rejected, standards sources, runtime compatibility, and licensing/provenance policy.

The WordPress layer additionally uses primary WordPress Developer/Make Core documentation and W3C WCAG 2.2. The design-quality layer is an independent synthesis: researched aesthetic preferences remain heuristics unless separately grounded in a standard or project requirement.

## External skills are optional

This skill does not vendor or require the six researched skills. If an agent runtime already has them installed, `SKILL.md` defines bounded delegation roles for them. Without them, this skill remains fully usable.

That makes it suitable for portable skill ecosystems that understand the Agent Skills format without binding the core workflow to a Claude-specific directory or a React-specific toolchain.

## OpenClaw

OpenClaw follows the Agent Skills format. This skill keeps its discovery description under 160 characters and its `name` aligned with the directory name.

Because `ariel-agent-skills` is a **multi-skill repository**, do not assume the OpenClaw Git installer can install the repository root as one skill: Git/local installs expect `SKILL.md` at the source directory root.

A reliable local workflow is:

```bash
git clone https://github.com/oliveiraariel/ariel-agent-skills.git
openclaw skills install ./ariel-agent-skills/frontend-design-wordpress
openclaw skills check
```

Alternatively, an OpenClaw workspace can expose the cloned repository as a scanned skill root through its supported skill-loading configuration; nested `SKILL.md` files are discoverable in configured roots.

## Validation

From the repository root, run the bundled dependency-free validator:

```bash
python frontend-design-wordpress/scripts/validate_skill.py
```

It checks project invariants plus key Agent Skills/OpenClaw constraints: skill name/directory alignment, naming syntax, description limits, progressive-disclosure line limit, and required files/references.

When available, also use the official/reference runtime checks rather than relying only on the bundled validator:

```bash
skills-ref validate ./frontend-design-wordpress
```

After installing in OpenClaw:

```bash
openclaw skills check
openclaw skills info frontend-design-wordpress
```

The repository also includes `.github/workflows/validate-skills.yml`. Once that workflow exists on the base branch, relevant pull requests and pushes to `main` execute each discovered `scripts/validate_skill.py`. The initial integration PR that introduces the workflow may not receive a pre-merge run because the workflow does not yet exist on the base branch; the push to `main` after merge provides the first repository CI execution.

## Status and maturity

`0.1.0` is the **review-complete baseline**, not a claim of universal production maturity. Architecture, standards boundaries, WordPress 7.1 version-sensitive guidance, upstream provenance, and skill-format compatibility were revalidated on 2026-09-07.

The next maturation step is empirical: use the skill on real WordPress Application, Content, Marketing, admin, and redesign surfaces; record failure patterns; then evolve the rules from observed gaps rather than adding generic advice.

See [`CHANGELOG.md`](./CHANGELOG.md) for version history.