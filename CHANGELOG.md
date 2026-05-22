# Changelog

All notable changes to this project are documented in this file.

Format follows [Keep a Changelog 1.1.0](https://keepachangelog.com/en/1.1.0/); versioning follows [SemVer 2.0.0](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

—

## [1.0.1] — 2026-05-22

### Added

- `stateLayer` / `stateLayerOpacity` on hover and pressed component variants (M3: 8% / 10%).
- `backgroundOpacity` / `textOpacity` on disabled variants.
- `outlineColor` / `outlineWidth` / `outlineOpacity` on input-field variants.
- New components: `button-secondary-hover`, `button-text-hover`, `input-field-disabled` (16 total).
- Canonical `Image style:` bullet required in Overview.

### Changed

- SKILL.md requires copying frontmatter byte-for-byte from the script's output.
- Parity docs corrected: dark scheme is byte-identical between Python and Node; light scheme diverges on 4 `on*Container` colors regardless of color-input mode.
- `assets/example-design.md` regenerated with new component tokens.

### Fixed

- `button-primary-disabled` previously rendered invisible (both layers were `onSurface` with no opacity).
- `button-primary-hover` / `-pressed` previously identical to base.

## [1.0.0] — 2026-05-22

Initial public release.

### Added

- Skill that converts brand inputs into a DESIGN.md grounded in Material Design 3.
- Python and Node.js token generators (49 colors, 15 typography levels, rounded + spacing scales, 13 components).
- `SKILL.md` workflow, `references/` (spec, M3 conventions, prose rubric), `assets/example-design.md`, `README.md`, `CONTRIBUTING.md`.
- Install paths: `npx skills add`, `.skill` drag-drop, standalone scripts.
- MPL-2.0 license.

[Unreleased]: https://github.com/darlanrod/material-design-md/compare/v1.0.1...HEAD
[1.0.1]: https://github.com/darlanrod/material-design-md/compare/v1.0.0...v1.0.1
[1.0.0]: https://github.com/darlanrod/material-design-md/releases/tag/v1.0.0
