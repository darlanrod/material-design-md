# Material Design 3 — Token Conventions Used by This Skill

This document explains *why* the token generator emits the values it does, so the prose can reference them accurately and so the user understands the system.

## Why Material 3 as the basis

The DESIGN.md spec is intentionally framework-agnostic. We use Material 3 as the *generation strategy* because:

- M3's [Dynamic Color](https://m3.material.io/styles/color/dynamic/overview) algorithm produces accessible, consistent palettes from any seed.
- The 49-role color system covers every UI scenario most products need (states, fixed colors, containers, surfaces at five elevation levels).
- Most agentic design tools and component libraries (Flutter, Angular Material, MUI v6, M3 Web Components) speak M3 natively.

If a user wants a non-M3 system, this skill is the wrong tool.

## Color tokens (the `colors:` block)

The script emits 49 M3 role tokens — the full set defined by `MaterialDynamicColors`. Grouped semantically:

**Accent (primary/secondary/tertiary):** Each group has 4 tokens — the role color itself, its `on*` text color, a `*Container` variant for tinted surfaces, and `on*Container` for text on those.

**Error:** Same four-token pattern (`error`, `onError`, `errorContainer`, `onErrorContainer`).

**Surfaces:** The most-used group. M3 defines five surface levels (`surfaceContainerLowest` through `surfaceContainerHighest`) plus `surfaceDim` / `surfaceBright` for explicit ambient brightness. Use these for elevation in flat designs (instead of shadows).

**Background, Outline, Inverse:** `background`, `onBackground`, `outline`, `outlineVariant`, `inverseSurface`, `inverseOnSurface`, `inversePrimary`. Inverses are used for snackbars and high-contrast call-outs.

**Fixed:** `primaryFixed`, `primaryFixedDim`, `onPrimaryFixed`, `onPrimaryFixedVariant` (and the same for secondary/tertiary). Fixed colors stay constant across light/dark schemes — useful for brand elements that shouldn't theme-shift.

**Effects:** `shadow`, `scrim`, `surfaceTint`.

### Scheme choice

The user picks `light` or `dark` and the script generates the active 49-role table. Tonal palettes (the underlying tones 0–100) are scheme-invariant — only the role→tone mapping changes between schemes. Prose should reference both schemes where relevant; the JSON output exposes `opposite_scheme.colors` for that purpose.

### Tonal palettes

The script also exposes tonal palettes via `--json`, with tones at the standard M3 steps: 0, 5, 10, 15, 20, 25, 30, 35, 40, 50, 60, 70, 80, 90, 95, 98, 99, 100. Use these when prose names a specific tone (e.g., "neutral tone 95 forms the page surface in light mode").

## Typography tokens

The script generates the full M3 type scale — 15 levels — using a geometric ratio:

| Token | Step | Default size (16 × 1.2^step) | Weight | Line height |
|---|---|---|---|---|
| `display-large` | +7 | 57px | 400 | 1.1 |
| `display-medium` | +6 | 48px | 400 | 1.1 |
| `display-small` | +5 | 40px | 400 | 1.1 |
| `headline-large` | +4 | 33px | 400 | 1.2 |
| `headline-medium` | +3 | 28px | 400 | 1.2 |
| `headline-small` | +2 | 23px | 400 | 1.2 |
| `title-large` | +1 | 19px | 500 | 1.2 |
| `title-medium` | 0 | 16px | 500 | 1.2 |
| `title-small` | -1 | 13px | 500 | 1.2 |
| `body-large` | 0 | 16px | 400 | 1.5 |
| `body-medium` | -1 | 13px | 400 | 1.5 |
| `body-small` | -2 | 11px | 400 | 1.5 |
| `label-large` | -1 | 13px | 500 | 1.4 |
| `label-medium` | -2 | 11px | 500 | 1.4 |
| `label-small` | -3 | 10px | 500 | 1.4 |

**Title fonts vs body fonts.** `display-*`, `headline-*`, `title-*` use the titles font. `body-*` and `label-*` use the body font. This is a strong default; deviate only if the brand explicitly calls for it.

**Line heights are unitless.** Per the DESIGN.md spec recommendation, unitless lineHeight is the CSS-preferred form (it scales with the element's font size).

**Letter spacing is not emitted by default.** If the brand wants tracked uppercase labels (a common "tech / data display" pattern), the agent should add `letterSpacing` manually to the relevant typography entries in post-processing — but don't do this unless the brand voice calls for it.

## Spacing tokens (the `spacing:` block)

```yaml
spacing:
  xs: 4px      # spacer × 0.25
  sm: 8px      # spacer × 0.5
  md: 16px     # spacer (base)
  lg: 24px     # spacer × 1.5
  xl: 48px     # spacer × 3
```

This five-step scale covers nearly every layout need. Larger paddings (cards, page gutters) typically use multiples of `lg`; tighter inner padding uses `sm` or `xs`.

## Rounded tokens (the `rounded:` block)

```yaml
rounded:
  xs: 4px      # rounder × 1
  sm: 8px      # rounder × 2
  md: 12px     # rounder × 3
  lg: 16px     # rounder × 4
  xl: 24px     # rounder × 6
  full: 9999px # pill / circle
```

`full: 9999px` is the conventional way to express "fully rounded" in token systems — any value larger than half the element height collapses to a pill.

## Components (the `components:` block)

The script emits 16 canonical component tokens, each referencing foundation tokens via `{path.to.token}` syntax. These are intentionally minimal — they cover the most-used interactive surfaces and serve as a *pattern* the consumer can extend.

| Component | Notes |
|---|---|
| `button-primary` (+ `-hover`, `-pressed`, `-disabled`) | Filled button, primary container, pill shape. |
| `button-secondary` (+ `-hover`) | Tonal button — secondary container, also pill. |
| `button-text` (+ `-hover`) | Transparent, primary-colored label. |
| `input-field` (+ `-focused`, `-error`, `-disabled`) | Filled text field on `surfaceContainerHighest`, slight rounding. |
| `card` | `surfaceContainerLow`, medium rounding. |
| `chip` (+ `-selected`) | Compact, `label-large`, smaller rounding. |
| `tooltip` | Inverse surface, body-small text. |

**Variants follow the `name-state` convention** the DESIGN.md spec recommends (e.g., `button-primary-hover`). The consumer is expected to apply each base + its variants together.

### Interactive state properties (non-normative)

The DESIGN.md spec defines a small set of standard component properties (`backgroundColor`, `textColor`, `typography`, `rounded`, `padding`, `size`, `height`, `width`) and says unknown properties are accepted with warning. This skill emits **five additional non-normative properties** to encode M3 interactive states faithfully:

| Property | Value type | Purpose |
|---|---|---|
| `stateLayer` | Color reference | The tinting color composited over `backgroundColor` to indicate hover/pressed/focus. |
| `stateLayerOpacity` | Percentage string (e.g. `"8%"`) | The opacity at which `stateLayer` is composited. M3 conventions: hover = 8%, pressed = 10%, focus = 10%, dragged = 16%. |
| `backgroundOpacity` | Percentage string | Opacity applied to `backgroundColor`. Used in disabled states (M3 default: 12% for buttons, 4% for input fields). |
| `textOpacity` | Percentage string | Opacity applied to `textColor`. Used in disabled states (M3 default: 38%). |
| `outlineColor` / `outlineWidth` / `outlineOpacity` | Color / dimension / percentage | Input-field border treatment. M3 conventions: enabled = `outline` 1px, focused = `primary` 2px, error = `error` 2px, disabled = `onSurface` 1px at 12% opacity. |

A consumer that doesn't understand these properties will fall back to the base color values and still render a usable (if state-blind) UI. A consumer that does understand them produces an M3-faithful result.

**When to extend:** if the brand needs domain-specific components (e.g., `alert-warning`, `bottom-sheet`, `nav-rail`), add them to the YAML during composition. Reference foundation tokens — never inline hex codes — to keep the system internally consistent.

## Custom-triplet behavior

When the user supplies `--primary --secondary --tertiary` instead of `--seed`:

1. Each color is parsed to its HCT (Hue, Chroma, Tone) representation.
2. A `TonalPalette` is built from each color's hue + chroma — so the palette's hue and saturation match the brand color exactly.
3. Neutral and neutral-variant palettes are derived from the primary hue with low chroma (6 and 8 respectively) — this gives surfaces a subtle tint of the brand rather than dead gray.
4. A `DynamicScheme` is assembled with these five palettes using the Tonal Spot variant.

The result: the chosen scheme honors the three brand colors exactly at their natural tone, and all derived roles (containers, on-colors, surfaces) flow from those palettes via the M3 algorithm.

## Why these defaults, not the others

- **Variant = Tonal Spot.** M3's default and most balanced variant. Other options (`Vibrant`, `Expressive`, `Fidelity`, `Content`) push the algorithm toward more saturated or more brand-faithful outputs; they're tuned for specific aesthetics and are not safe defaults.
- **Contrast level = 0.0.** Standard M3 contrast. The system can re-render at higher contrast levels for accessibility; we don't bake that in.
- **Spec version 2021 (Python).** Matches the mainstream M3 ecosystem (Flutter, MUI, Angular Material). The 2025 "expressive" spec is newer and not yet broadly adopted by component libraries.
