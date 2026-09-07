# Source Analysis and Architecture Rationale

Research revalidated: **2026-09-07**.

This skill is an independent synthesis. It does **not** vendor or reproduce the six upstream skills. Their strongest architectural ideas are used as research inputs, and the resulting rules are independently written for a framework-neutral frontend workflow with a first-class WordPress adapter.

## Validation snapshot

The revalidation used the current default-branch files below. File SHAs are recorded so later reviews can determine whether an upstream source changed after this research pass.

| Source | Observed version/status | File observed | Blob SHA at revalidation |
|---|---|---|---|
| Anthropic `frontend-design` | no version field observed | `anthropics/skills/skills/frontend-design/SKILL.md` | `a5333457c414d20d625f307df945842c0952ecc3` |
| UI/UX Pro Max | manifest `2.13.0` | `nextlevelbuilder/ui-ux-pro-max-skill/.claude/skills/ui-ux-pro-max/SKILL.md` | `41f8e2fd7f8c568228d0b55186ebe3f7b4007377` |
| make-interfaces-feel-better | no version field observed | `jakubkrehel/make-interfaces-feel-better/skills/make-interfaces-feel-better/SKILL.md` | `e47b87b369396655fa6bea7240c17f108ea494d5` |
| Vercel `web-design-guidelines` wrapper | `1.0.0` | `vercel-labs/agent-skills/skills/web-design-guidelines/SKILL.md` | `ceae92ab319216a68274168fba9b63b998b65997` |
| Vercel live guideline source | living ruleset | `vercel-labs/web-interface-guidelines/command.md` | `e1e8e3460db7c1440e34642c4f7b885185ca5366` |
| Impeccable | `4.2.2` | `pbakaus/impeccable/.github/skills/impeccable/SKILL.md` | `788dac1dcd96581882eb8f7af8c070f1c188022c` |
| Taste Skill v2 | upstream describes v2 as experimental/actively iterating | `Leonxlnx/taste-skill/skills/taste-skill/SKILL.md` | `b72132fcd466da605623ffe96e370b3991fc5285` |

These SHAs are evidence anchors, not update pins. The skill does not depend on the upstream repositories at runtime.

## Research objective

The six upstream skills solve different parts of frontend design:

1. visual direction and anti-template judgment;
2. searchable UI/UX knowledge;
3. micro-polish;
4. code-centric audit;
5. broad design lifecycle/hardening;
6. high-variance anti-slop design direction.

The gap is that none of them serves as a deep WordPress adapter while remaining equally comfortable with application UI, responsive behavior, and accessibility. `frontend-design-wordpress` is designed to fill that gap without inheriting a JavaScript framework as its architecture.

## 1. Anthropic `frontend-design`

**Upstream**

- Repository: https://github.com/anthropics/skills
- Skill: `skills/frontend-design/SKILL.md`
- License: the current skill package includes `LICENSE.txt`, observed as Apache-2.0 at revalidation.

**What it does especially well**

- grounds visual choices in subject matter, audience, and the page's actual job;
- treats typography/layout/color as deliberate design decisions rather than defaults;
- includes an explicit plan → review against brief → build → critique loop;
- identifies recurring AI-generated visual clichés and asks whether each choice is justified;
- emphasizes restraint and one strong visual idea rather than decoration everywhere;
- treats interface copy as design material.

**Limitations for this project**

- it is primarily a design-direction skill, not a WordPress implementation guide;
- it provides a broad quality floor but not a deep application/dashboard workflow;
- some aesthetic observations are time-sensitive and should not become permanent bans.

**Adopted here**

- subject-grounded design read;
- compact design contract before major implementation;
- anti-template self-critique;
- bounded critique after build;
- content/copy as part of UX.

**Not adopted as universal law**

- any specific current-fashion blacklist;
- any assumption that visual distinctiveness should outrank task clarity in application UI.

## 2. UI/UX Pro Max

**Upstream**

- Repository: https://github.com/nextlevelbuilder/ui-ux-pro-max-skill
- Skill: `.claude/skills/ui-ux-pro-max/SKILL.md`
- Manifest observed: v2.13.0.
- License: MIT.
- Current manifest explicitly lists OpenClaw among supported platforms.

**What it does especially well**

- large searchable local knowledge base rather than loading all guidance into the prompt;
- progressive disclosure through domains/references;
- detects the implementation stack instead of assuming one;
- prioritizes accessibility, touch/interaction, performance, responsive layout, typography/color, forms, navigation, and charts;
- supports persistent design-system output;
- separates product/style/color/typography/UX/stack queries.

**Limitations for this project**

- the current stack list is broad but no WordPress stack entry was found during revalidation;
- many recommendation tables contain numeric heuristics that are useful defaults but not normative standards;
- its search database and scripts are an external runtime dependency if used directly.

**Adopted here**

- progressive disclosure with small references loaded on demand;
- detect-stack-first behavior;
- accessibility/responsive as first-class priorities;
- design-system/token thinking;
- explicit distinction between normative requirements and heuristics.

**Not adopted**

- dependence on its search database;
- treating one heuristic value as a universal requirement;
- non-WordPress stack defaults.

## 3. `make-interfaces-feel-better`

**Upstream**

- Repository: https://github.com/jakubkrehel/make-interfaces-feel-better
- Skill: `skills/make-interfaces-feel-better/SKILL.md`
- License: MIT.

**What it does especially well**

- focuses on details that compound into perceived quality;
- explicitly says to detect and use the project's existing styling system instead of introducing a second one;
- covers typography, surfaces, icons, motion, and performance;
- distinguishes structural borders from elevation/shadow roles;
- emphasizes optical alignment, numeric stability, interaction states, and motion restraint;
- has clear quick/full review modes, severity, evidence, verification, and verdict language.

**Limitations for this project**

- micro-polish is not a replacement for information architecture, accessibility, or responsive structure;
- some fixed numerical prescriptions are author preferences/heuristics, not universal standards;
- no WordPress architecture layer.

**Adopted here**

- never introduce a second styling system just for polish;
- polish after structure works;
- optical as well as geometric review;
- explicit states and numeric/data legibility;
- evidence-based audit format and bounded verification.

**Not adopted as absolutes**

- hard-coded animation scale/duration values;
- universal surface/shadow/icon prescriptions.

## 4. Vercel `web-design-guidelines`

**Upstream**

- Wrapper repository: https://github.com/vercel-labs/agent-skills
- Skill: `skills/web-design-guidelines/SKILL.md`
- Live rule source: https://github.com/vercel-labs/web-interface-guidelines/blob/main/command.md
- Wrapper version observed: 1.0.0.
- License: MIT. The wrapper repository declares MIT in its README and the live rules repository contains an MIT `LICENSE` file at revalidation.

**What it does especially well**

- keeps the wrapper tiny and fetches fresh audit rules;
- produces terse `file:line` findings;
- covers semantic HTML, focus, forms, animation, content handling, images, performance, navigation/state, touch, safe areas, theming, i18n, and anti-patterns;
- treats source-code review as a separate specialist activity rather than design generation.

**Limitations for this project**

- it is audit-centric, not a full design lifecycle;
- some content/style rules are product opinions, not accessibility/web standards;
- some examples are React/Tailwind-flavored;
- the living ruleset can contain recommendations that should not be mistaken for WCAG requirements;
- no WordPress ownership/updateability/editor-parity analysis.

**Adopted here**

- code-centric audit as a distinct mode;
- high-signal finding format with exact location;
- fresh-source mindset for changing guidelines;
- semantic HTML, focus, form, overflow, media, and interaction audit categories.

**Changed here**

- findings distinguish observed/likely/potential evidence;
- normative accessibility requirements are separated from UX heuristics;
- WordPress architecture is an explicit audit category.

## 5. Impeccable

**Upstream**

- Repository: https://github.com/pbakaus/impeccable
- Skill: `.github/skills/impeccable/SKILL.md`
- Version observed: 4.2.2.
- License: Apache-2.0.

**What it does especially well**

- covers the entire frontend lifecycle: shape, build, critique, audit, polish, harden, adapt, optimize, document, extract, and more;
- explicitly distinguishes refinement from redesign;
- separates surface intent so the same aesthetic rules are not applied to every UI;
- uses durable product/design context documents;
- performs bounded visual QA instead of endless self-polish;
- includes production concerns such as edge cases, i18n, accessibility, performance, responsive adaptation, and reusable tokens.

**Limitations for this project**

- current implementation is a substantial toolchain with launcher/binary/context artifacts and many command references;
- using its complete runtime would make this skill dependent on a specific external ecosystem;
- it is broad enough that a lightweight WordPress-focused skill should not duplicate it.

**Adopted here**

- task/surface routing;
- preserve-and-improve versus replace-visual-direction distinction;
- durable design-contract thinking;
- bounded QA cycle;
- production states/edge cases before approval.

**Not adopted**

- launcher/binary requirement;
- Impeccable-specific commands, hooks, detectors, or file contracts;
- any assumption that the external tool is installed.

## 6. Taste Skill v2

**Upstream**

- Repository: https://github.com/Leonxlnx/taste-skill
- Skill: `skills/taste-skill/SKILL.md`
- Install name: `design-taste-frontend`.
- Current upstream describes v2 as experimental/actively iterating.
- License: MIT.

**What it does especially well**

- forces brief inference before design;
- aggressively counters generic AI visual output;
- connects design direction to audience, reference signals, brand assets, and trust/accessibility constraints;
- distinguishes real design systems from aesthetic trends;
- uses adjustable variance/motion/density concepts rather than pretending one visual intensity fits every brief;
- has a strong redesign-audit mindset.

**Critical limitation for this project**

The skill explicitly states that its primary scope is landing pages, portfolios, and redesigns—not dashboards, data tables, or multi-step product UI. It also currently defaults to React/Next.js, Tailwind, and Motion for many implementations. Those defaults are unsuitable as a universal base for WordPress and data-heavy application interfaces.

**Adopted here**

- infer the design read before implementation;
- anti-default discipline;
- adjust visual variance/motion/density conceptually according to product context;
- use established design systems when the brief genuinely calls for them;
- accessibility/trust constraints override aesthetic novelty.

**Explicitly rejected here**

- default React/Next.js/Tailwind/Motion architecture;
- fixed default design dials;
- applying high-variance landing-page rules to dashboards/forms/data tables;
- font/icon/aesthetic preferences as universal rules.

## Why the new skill is not just a seventh design prompt

The resulting architecture is intentionally layered:

```text
User brief + existing repository
            |
            v
Task/surface classification
            |
            v
Design contract
            |
   +--------+---------+
   |        |         |
   v        v         v
UI/UX   Responsive   Accessibility
   |        |         |
   +--------+---------+
            |
            v
     WordPress adapter
            |
            v
      Implementation
            |
            v
     Polish + audit
```

The key difference is the **adapter layer**: visual/UX reasoning is separated from framework/platform implementation. WordPress is detected and handled explicitly instead of inheriting React/Next/Tailwind assumptions.

## Optional specialist routing

If an agent runtime can invoke other installed skills, `frontend-design-wordpress` may delegate a bounded subtask:

| Need | Optional specialist | Boundary |
|---|---|---|
| exploratory visual direction | Anthropic frontend-design | return direction/options; platform skill decides implementation |
| searchable UI/UX lookup | UI/UX Pro Max | return verified relevant guidance; do not impose its stack |
| final micro-polish | make-interfaces-feel-better | refine existing system only |
| code-centric audit | Vercel web-design-guidelines | findings become audit evidence, not automatic truth |
| broad production hardening | Impeccable | use only if installed/desired; preserve WordPress/project constraints |
| expressive marketing/showcase direction | Taste Skill | only when surface fits its stated scope |

External skills are optional. The core skill must remain functional alone.

## WordPress and standards validation

Primary sources used beyond the six skills:

- WordPress 7.1 release: https://wordpress.org/news/2026/08/wordpress-7-1-mary-lou/
- Theme Handbook: https://developer.wordpress.org/themes/
- Block Editor Handbook: https://developer.wordpress.org/block-editor/
- `theme.json`: https://developer.wordpress.org/themes/global-settings-and-styles/introduction-to-theme-json/
- WordPress 7.1 responsive block styles: https://make.wordpress.org/core/2026/08/05/responsive-block-styles-and-configurable-viewports-in-wordpress-7-1/
- WordPress Coding Standards: https://developer.wordpress.org/coding-standards/wordpress-coding-standards/
- WordPress Accessibility Coding Standards: https://developer.wordpress.org/coding-standards/wordpress-coding-standards/accessibility/
- WCAG 2.2: https://www.w3.org/TR/WCAG22/

Validated conclusions:

- WordPress 7.1 was released on 2026-08-19.
- WordPress 7.1 introduced responsive block style states using `@mobile` and `@tablet`, plus configurable `settings.viewport`; older WordPress core versions must not be assumed to support those APIs.
- WordPress Accessibility Coding Standards state that code integrated into the official WordPress ecosystem—including core, WordPress.org sites, and official plugins—is expected to conform to WCAG 2.2 AA.
- This skill applies WCAG 2.2 AA as its own baseline for third-party WordPress work without claiming that official WordPress policy automatically governs every third-party project.
- WCAG 2.2 AA Target Size (Minimum), SC 2.5.8, is 24 × 24 CSS pixels with defined exceptions/spacing alternatives. A 44 × 44 target is not treated here as the general AA minimum.

## Agent Skills and OpenClaw validation

The bundle was also checked against current Agent Skills/OpenClaw authoring guidance:

- Agent Skills specification: https://agentskills.io/specification
- OpenClaw Skills: https://docs.openclaw.ai/tools/skills
- OpenClaw Creating Skills: https://docs.openclaw.ai/tools/creating-skills
- OpenClaw Skills CLI: https://docs.openclaw.ai/cli/skills

Relevant conclusions:

- Agent Skills requires `SKILL.md` with YAML frontmatter; `name` and `description` are required.
- Agent Skills requires the `name` to use lowercase letters/numbers/hyphens, remain within 64 characters, and match the parent directory name.
- Agent Skills allows descriptions up to 1024 characters; OpenClaw's authoring guidance recommends a one-line description under 160 characters for discovery. This project's description follows the stricter OpenClaw recommendation.
- Agent Skills recommends progressive disclosure, a main `SKILL.md` below 500 lines, and focused one-level references. This bundle follows that structure.
- OpenClaw follows the Agent Skills format and can discover nested skills in configured skill roots.
- OpenClaw Git/local installation expects `SKILL.md` at the directory being installed. Because `ariel-agent-skills` is a multi-skill repository whose repository root has no `SKILL.md`, install the cloned `frontend-design-wordpress` subdirectory locally or expose the repository as a configured/scanned skill root rather than treating the repository root as a single skill.

## Provenance and licensing rule

This repository's skill is MIT-licensed under the repository license. That license covers the independently written material in this repository; it does not relicense upstream projects.

Do not copy upstream skill files into this repository without separately satisfying their licenses and attribution/NOTICE requirements where applicable. Prefer linking to upstream projects or installing them as optional external skills.

If future revisions incorporate substantial upstream text or code instead of independent synthesis, update the repository's attribution/licensing documentation before release.