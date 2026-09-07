# Changelog

All notable changes to this skill should be documented here.

## 0.2.0 — 2026-09-07

Identity and portability clarification.

- renamed the skill from `frontend-design-wordpress` to `web-frontend-design` so discovery reflects its actual framework-neutral web scope;
- renamed the skill directory and frontmatter identity to `web-frontend-design`;
- clarified that WordPress is an optional first-class **platform adapter**, not the skill's default target or identity;
- clarified applicability across browser-based projects implemented with React, Vue, Angular, Svelte, plain HTML/CSS/JavaScript, server-rendered frameworks, template engines, and other web stacks;
- preserved WordPress-specific expertise in `references/wordpress-adapter.md`, loaded only when WordPress is detected;
- updated lifecycle routing, repository documentation, machine-readable registry entries, validation commands, and OpenClaw installation examples to the new identity;
- retained the detailed 0.1.0 source-analysis snapshot as historical provenance while refreshing the active source-analysis document for the new architecture;
- kept the skill focused on web frontend design rather than claiming native mobile/desktop UI specialization.

## 0.1.0 — 2026-09-07

Initial reviewed baseline, originally published under the name `frontend-design-wordpress`.

- added framework-neutral frontend design workflow for Design, Build, Redesign, Polish, and Audit modes;
- added surface routing for Marketing, Application, Content, and Showcase interfaces;
- added WordPress adapter for block themes, classic themes, Gutenberg blocks, plugin frontend UI, WordPress admin/settings UI, page builders, and Custom HTML;
- added WCAG 2.2 AA operational accessibility baseline with normative requirements separated from platform guidance and usability heuristics;
- added responsive-design and data-heavy UI guidance, including explicit WordPress 7.1+ compatibility boundaries for responsive Global Styles;
- added visual-quality and bounded audit references;
- documented provenance, observed versions/status, and source SHAs for six researched upstream design skills;
- added Agent Skills/OpenClaw-oriented structural validation and installation notes;
- added repository CI to execute bundled skill validators after integration;
- hardened validation for skill-name/description limits, directory-name matching, progressive disclosure, required references, and referenced-file existence;
- deliberately avoided React, Next.js, Tailwind, Motion, or any other framework as a universal default.
