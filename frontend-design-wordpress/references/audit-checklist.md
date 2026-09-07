# Frontend Audit Checklist

Use for `Audit` mode and for final verification after significant implementation/redesign work.

## 1. Declare scope first

Record:

- exact files/routes/screens inspected;
- task mode and surface mode;
- platform/framework/WordPress surface;
- styling system;
- viewports/devices actually checked;
- interactions/states actually exercised;
- automated/manual checks run;
- anything explicitly not inspected.

Never imply that the whole application was reviewed when only one page or source file was inspected.

## 2. Severity

Use four levels:

- **BLOCKER** — prevents completing the core task, causes severe accessibility failure, data loss/misleading action, or makes the requested surface unusable.
- **HIGH** — significant accessibility, responsive, interaction, comprehension, or correctness defect on a primary path.
- **MEDIUM** — noticeable usability, consistency, content handling, performance, or design-system defect with a practical user impact.
- **LOW** — isolated polish/consistency issue that does not materially block the task.

Do not inflate aesthetic preference into HIGH severity.

## 3. Review order

Review in this order so cosmetic detail does not hide structural defects:

### A. Product/task integrity

- core action is discoverable and understandable;
- navigation/state does not mislead;
- redesign did not remove required behavior/content;
- destructive actions are proportionate and clear;
- loading/error/empty states preserve task continuity.

### B. Accessibility

Use `accessibility.md`:

- semantics;
- names/labels;
- keyboard;
- focus;
- forms/errors/status;
- contrast/non-color signals;
- zoom/reflow;
- motion;
- images/media;
- table/chart alternatives.

### C. Responsive behavior

Use `responsive-design.md`:

- narrow, intermediate, desktop layouts;
- overflow;
- navigation;
- forms;
- dense data/tables;
- dialogs/overlays;
- long content/localization;
- viewport/safe area concerns.

### D. WordPress architecture

When applicable use `wordpress-adapter.md`:

- correct customization layer;
- no core/vendor edits that will be overwritten;
- editor/frontend parity;
- appropriate `theme.json`/theme/plugin/block ownership;
- scoped plugin/custom-HTML CSS;
- maintainable asset loading;
- WordPress coding/accessibility conventions.

### E. Visual hierarchy and consistency

Use `design-quality.md`:

- hierarchy;
- spacing rhythm;
- typography roles;
- semantic color roles;
- component consistency;
- cards/surfaces used with purpose;
- icon consistency;
- states;
- motion restraint;
- anti-template/design-brief fit.

### F. Frontend performance risks

Inspect proportionately:

- unnecessary render/layout work;
- oversized or layout-shifting images/media;
- animation of layout-heavy properties;
- excessive third-party assets;
- unnecessary JavaScript for CSS-solvable layout;
- long lists rendered without an appropriate strategy;
- font loading/fallback behavior;
- duplicate WordPress/theme/plugin assets.

Do not claim performance measurements unless you actually measured them.

## 4. Finding format

Group by severity, then by file/screen.

| Severity | Location | Finding | User impact | Recommended change | Evidence |
|---|---|---|---|---|---|
| HIGH | `path/file.css:42` or `Dashboard > filters` | Concrete defect | What the user experiences | Specific fix | Source inspection, keyboard test, screenshot, etc. |

For systemic issues, use one finding and list all affected locations rather than repeating the same sentence many times.

Distinguish:

- **Observed** — verified directly.
- **Likely** — strong source evidence but runtime not verified.
- **Potential** — needs targeted testing; do not present as confirmed.

## 5. WordPress audit additions

For WordPress surfaces, also check:

- theme/plugin ownership of changed CSS;
- update-safety of edited files;
- block editor versus frontend rendering;
- Global Styles/token duplication;
- full/wide/content alignment behavior;
- plugin styles leaking outside the plugin wrapper;
- theme styles unintentionally overriding plugin controls;
- accessible output after WordPress filters/plugins modify markup.

## 6. Visual verification

When screenshots/browser access exists:

- inspect the completed scope at narrow, intermediate, and desktop widths;
- compare alignment, wrapping, clipping, overflow, hierarchy, and state contrast;
- inspect hover/focus/active/loading/error states relevant to the requested flow;
- if motion is important, inspect interrupted/reduced-motion behavior and optionally slow animations to reveal timing problems.

Do not keep iterating indefinitely. Fix the identified batch and run one confirmation pass.

## 7. Verdict

Use:

- **Block** — any BLOCKER remains.
- **Needs changes** — no BLOCKER, but HIGH or meaningful MEDIUM findings remain.
- **Approve with notes** — only LOW findings or explicitly accepted limitations remain.
- **Approve** — no actionable findings in the inspected scope and required verification passed.

Always list unverified checks next to the verdict.

## 8. Example concise audit output

```text
Scope: account dashboard; plugin frontend; CSS + PHP template; 360/768/1440 px; keyboard primary flow.

HIGH
- dashboard.css:118 — filter row has a 760px min-width and forces page-level horizontal scroll at 360px. Move scrolling/stacking behavior to the filter/table component.

MEDIUM
- account-form.php:74 — validation message is visible but not programmatically associated with the field. Add an error id + aria-describedby and move focus/summary as appropriate after submit.

LOW
- dashboard.css:203 — icon and adjacent label have inconsistent optical weight compared with the shared action pattern.

Verification: primary keyboard flow passed after fixes; screen-reader announcement behavior not verified.
Verdict: Approve with notes — screen-reader verification remains.
```
