# Changelog

All notable changes to this skill should be documented here.

## 0.1.0 — 2026-09-07

Initial reviewed baseline.

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
