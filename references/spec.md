# DESIGN.md Specification (Reference)

Distilled from the [official spec](https://github.com/google-labs-code/design.md/blob/main/docs/spec.md). Use this as the conformance checklist — the generated file MUST satisfy these rules.

## File shape

A DESIGN.md file has two parts:

1. **Optional YAML frontmatter** — machine-readable design tokens, fenced by lines containing exactly `---`. Comes first.
2. **Markdown body** — human-readable prose organized into ordered sections.

An H1 may appear at the very top (typically the brand name); it is NOT parsed as a section. All actual sections use H2.

## Frontmatter schema

```yaml
version: <string>       # optional; current label: "alpha"
name: <string>          # required
description: <string>   # optional
colors:
  <token-name>: <Color>
typography:
  <token-name>: <Typography>
rounded:
  <scale-level>: <Dimension>
spacing:
  <scale-level>: <Dimension | number>
components:
  <component-name>:
    <token-name>: <string | token-reference>
```

### Value types

- **Color**: `"#RRGGBB"` (6 hex digits, SRGB, leading `#`). Always quote in YAML.
- **Dimension**: number + unit suffix. Valid units: `px`, `em`, `rem`. Examples: `48px`, `1.5rem`.
- **Typography**: an object with keys:
  - `fontFamily` (string)
  - `fontSize` (Dimension)
  - `fontWeight` (number, e.g. `400`, `700`)
  - `lineHeight` (Dimension OR unitless number; unitless = multiplier of fontSize, preferred)
  - `letterSpacing` (Dimension, optional)
  - `fontFeature` (string, optional — maps to CSS `font-feature-settings`)
  - `fontVariation` (string, optional — maps to CSS `font-variation-settings`)
- **Token reference**: `"{path.to.token}"` — quoted, curly braces, dotted path. Example: `"{colors.primary}"`, `"{typography.body-large}"`. For most groups the reference must resolve to a primitive; inside `components`, composite references (e.g. `{typography.label-large}`) are permitted.

## Required section order

H2 headings, in this exact order. Sections may be omitted if not relevant — but those present must appear in this sequence:

1. **Overview** (also acceptable: "Brand & Style")
2. **Colors**
3. **Typography**
4. **Layout** (also acceptable: "Layout & Spacing")
5. **Elevation & Depth** (also acceptable: "Elevation")
6. **Shapes**
7. **Components**
8. **Do's and Don'ts**

Duplicate H2 headings are an error per the spec — the file would be rejected.

## What each section is for

### Overview / Brand & Style
Holistic description of look-and-feel: brand personality, target audience, emotional response. Foundational context for stylistic decisions when no token explicitly applies. This is where the brand lives.

### Colors
Defines color palettes via prose, with a description of each palette's role. The `colors:` token block in the frontmatter contains the systematic role tokens (`primary`, `surface`, etc.); the prose may use descriptive names (e.g., "Midnight Forest Green") that map to those tokens.

### Typography
Defines typography levels via prose (Headlines, Body, Labels, etc.) with the `typography:` token block giving exact font properties per level. Most systems have 9–15 levels.

### Layout / Layout & Spacing
Describes the layout strategy (grid model, fluid vs fixed, containment patterns) and the spacing scale. Prose explains the philosophy; `spacing:` block gives the tokens.

### Elevation & Depth
How visual hierarchy is conveyed. Could be shadow-based, tonal-layer-based, border-based, or a mix. If shadows are used, specify spread/blur/color.

### Shapes
The corner-radius philosophy. Sharp vs soft. Variations by component family. The `rounded:` block gives the scale tokens.

### Components
Style guidance for component atoms (buttons, chips, lists, tooltips, checkboxes, radios, inputs). The `components:` token block defines per-component properties using token references where possible.

### Do's and Don'ts
Short, concrete guardrails. The most actionable section for a downstream agent — write rules they can check.

## Recommended token names (non-normative)

The spec suggests these names for consistency, but does not require them:

- **Colors:** `primary`, `secondary`, `tertiary`, `neutral`, `surface`, `on-surface`, `error`
- **Typography:** `headline-display`, `headline-lg`, `headline-md`, `body-lg`, `body-md`, `body-sm`, `label-lg`, `label-md`, `label-sm`
- **Rounded:** `none`, `sm`, `md`, `lg`, `xl`, `full`

This skill uses the **full Material 3 conventions** instead (49 color roles, 15 typography levels) because the M3 ecosystem is the largest concrete consumer of this spec. The DESIGN.md spec explicitly allows "any consistent naming convention."

## Consumer behavior for unknown content

| Scenario | Behavior |
|---|---|
| Unknown section heading | Preserve; do not error |
| Unknown color token name | Accept if value is valid |
| Unknown typography token name | Accept as valid typography |
| Unknown spacing value | Accept; store as string if not a valid dimension |
| Unknown component property | Accept with warning |
| Duplicate section heading | **Error — reject the file** |

The takeaway: extra fields are tolerated, but section duplicates are fatal. Run a `grep -c '^## '` quality check before delivering if you're unsure.

## Example minimal frontmatter

```yaml
---
version: alpha
name: Daylight Prestige
colors:
  primary: "#1A1C1E"
  secondary: "#6C7278"
  tertiary: "#B8422E"
typography:
  body-large:
    fontFamily: Public Sans
    fontSize: 16px
    fontWeight: 400
    lineHeight: 1.5
---
```
