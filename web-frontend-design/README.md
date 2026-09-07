# Web Frontend Design Skill

A portable Agent Skill for designing, implementing, reviewing, and refining **web frontend interfaces across frameworks and languages**, with first-class support for UI/UX, responsive design, accessibility, and optional platform adapters such as WordPress.

**Current version:** `0.2.0` — renamed and clarified framework-neutral baseline, ready for broader field testing.

## Identity and scope

This skill is **not WordPress-only**. Its core is framework-neutral and targets browser-based frontend work regardless of whether the implementation uses React, Vue, Angular, Svelte, plain HTML/CSS/JavaScript, PHP templates, Laravel Blade, Django templates, Rails, ASP.NET, Java templates, or another web stack.

The skill separates **design judgment** from **platform implementation**. Platform-specific guidance is loaded only when needed. WordPress remains a deep supported platform through `references/wordpress-adapter.md`, but it is an adapter rather than the identity of the skill.

It is designed for:

- web applications and dashboards;
- landing/marketing pages;
- content sites;
- browser-based application interfaces;
- redesigns;
- responsive/accessibility remediation;
- frontend audit and final polish;
- WordPress block themes and Global Styles when WordPress is present;
- classic themes, Gutenberg blocks, plugin-rendered frontend interfaces, WordPress plugin admin/settings UI, page builders, and Custom HTML when those WordPress surfaces are present.

It is not intended to be the primary authority for native mobile UI, native desktop UI, backend architecture, databases, infrastructure, or unrelated security analysis.

## Design principles

1. **Brief first** — product, audience, task, brand, and constraints drive design.
2. **Detect the real stack** — never replace or duplicate the project's styling or component architecture by default.
3. **Framework-neutral web core** — React, Vue, Angular, Svelte, server rendering, template engines, WordPress, and plain web stacks are implementation contexts, not the identity of the skill.
4. **Application UI is not a landing page** — data-heavy/task-heavy surfaces prioritize clarity and operation over visual spectacle.
5. **Responsive by design** — narrow/intermediate/desktop behavior is planned, not patched later.
6. **Accessibility is a gate** — WCAG 2.2 AA is the baseline; platform guidance is kept distinct from normative requirements.
7. **Platform adapters are conditional** — load platform-specific guidance only when the detected project needs it.
8. **WordPress is an adapter, not an export target** — when WordPress is present, choose the correct theme/block/plugin/admin/builder integration layer.
9. **Polish follows structure** — hierarchy and usability come before micro-effects.
10. **Verification is bounded and evidence-based** — report what was actually inspected/tested.

## Structure

```text
web-frontend-design/
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

`SKILL.md` is the agent entry point. References are loaded only when the task requires them. `wordpress-adapter.md` is not part of the default context for non-WordPress projects.

## Task modes

The skill routes work through five modes:

- **Design** — establish a new frontend direction.
- **Build** — implement an approved/inferable direction.
- **Redesign** — materially replace visual structure while preserving product truth.
- **Polish** — improve an existing interface without replacing its identity.
- **Audit** — inspect and report with explicit scope/evidence.

It also classifies the surface as **Marketing**, **Application**, **Content**, or **Showcase** so the same aesthetic behavior is not applied to every product surface.

## Framework and language neutrality

The core guidance operates primarily at the web-platform and design level:

- information architecture;
- UI/UX;
- typography, spacing, color, hierarchy, and states;
- semantic HTML and browser interaction;
- CSS layout and responsive behavior;
- accessibility;
- frontend verification and audit.

The server language or web framework may change how the interface is implemented, but it does not change these core design obligations. The skill therefore inspects and preserves the project's actual rendering model, component conventions, styling system, and build tooling instead of introducing a preferred stack.

Framework-specific engineering concerns such as React Server Components, Vue reactivity, Angular dependency injection, framework routing, state management, hydration, or bundling remain responsibilities to be composed with engineering skills such as `software-architecture`, `implementation`, `testing`, and `debugging` when needed.

## WordPress adapter

WordPress remains first-class because its frontend architecture has platform-specific concerns that generic web guidance cannot safely infer:

- block theme / Site Editor;
- classic theme;
- custom Gutenberg block;
- plugin-rendered frontend;
- plugin admin/settings UI;
- page builder;
- Custom HTML/constrained embed;
- `theme.json`, Global Styles, editor/frontend parity, hooks, enqueueing, and version-sensitive block APIs.

The adapter is loaded **only when WordPress is detected**. It is version-aware: WordPress 7.1 responsive Global Styles (`@mobile`, `@tablet`, `settings.viewport`) are not assumed to exist on older WordPress core versions.

## Research basis

The architecture was developed after revalidating six notable frontend design skills/projects:

- Anthropic `frontend-design`;
- UI/UX Pro Max;
- `make-interfaces-feel-better`;
- Vercel `web-design-guidelines`;
- Impeccable;
- Taste Skill v2.

See [`references/source-analysis.md`](./references/source-analysis.md) for the detailed comparison, validation snapshot, strengths, limits, ideas adopted/rejected, standards sources, runtime compatibility, and licensing/provenance policy.

The WordPress adapter additionally uses primary WordPress Developer/Make Core documentation and W3C WCAG 2.2. The design-quality layer is an independent synthesis: researched aesthetic preferences remain heuristics unless separately grounded in a standard or project requirement.

## External skills are optional

This skill does not vendor or require the six researched skills. If an agent runtime already has them installed, `SKILL.md` defines bounded delegation roles for them. Without them, this skill remains fully usable.

That makes it suitable for portable skill ecosystems that understand the Agent Skills format without binding the core workflow to a Claude-specific directory, a React-specific toolchain, or WordPress.

## OpenClaw

OpenClaw follows the Agent Skills format. This skill keeps its discovery description under 160 characters and its `name` aligned with the directory name.

Because `ariel-agent-skills` is a **multi-skill repository**, do not assume the OpenClaw Git installer can install the repository root as one skill: Git/local installs expect `SKILL.md` at the source directory root.

A reliable local workflow is:

```bash
git clone https://github.com/oliveiraariel/ariel-agent-skills.git
openclaw skills install ./ariel-agent-skills/web-frontend-design
openclaw skills check
```

Alternatively, an OpenClaw workspace can expose the cloned repository as a scanned skill root through its supported skill-loading configuration; nested `SKILL.md` files are discoverable in configured roots.

## Validation

From the repository root, run the bundled dependency-free validator:

```bash
python web-frontend-design/scripts/validate_skill.py
```

It checks project invariants plus key Agent Skills/OpenClaw constraints: skill name/directory alignment, naming syntax, description limits, progressive-disclosure line limit, required files, and explicitly referenced local Markdown/Python files.

When available, also use the official/reference runtime checks rather than relying only on the bundled validator:

```bash
skills-ref validate ./web-frontend-design
```

After installing in OpenClaw:

```bash
openclaw skills check
openclaw skills info web-frontend-design
```

The repository also includes `.github/workflows/validate-skills.yml`, which discovers bundled skill validators and runs them on relevant pushes and pull requests.

## Status and maturity

`0.2.0` changes the skill identity from the former `frontend-design-wordpress` name to `web-frontend-design` so discovery reflects the architecture that already existed: a **framework-neutral web frontend skill with an optional WordPress adapter**.

The next maturation step is empirical: use the skill on real projects across multiple web stacks and WordPress surfaces, record failure patterns, and evolve the rules from observed gaps rather than adding framework-specific advice without evidence.

See [`CHANGELOG.md`](./CHANGELOG.md) for version history.
