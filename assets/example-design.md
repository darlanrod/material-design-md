# Bossa

---
version: alpha
name: Bossa
description: Clean geometric grids softened by organic curves, saturated earth-and-ocean palettes, and rhythmic asymmetry.
colors:
  primary: "#9ed49d"
  surfaceTint: "#9ed49d"
  onPrimary: "#043912"
  primaryContainer: "#1f5026"
  onPrimaryContainer: "#b9f0b7"
  secondary: "#d9c770"
  onSecondary: "#393000"
  secondaryContainer: "#524600"
  onSecondaryContainer: "#f7e388"
  tertiary: "#b5c4ff"
  onTertiary: "#1c2d60"
  tertiaryContainer: "#344478"
  onTertiaryContainer: "#dce1ff"
  error: "#ffb4ab"
  onError: "#690005"
  errorContainer: "#93000a"
  onErrorContainer: "#ffdad6"
  background: "#101410"
  onBackground: "#e0e4db"
  surface: "#101410"
  onSurface: "#e0e4db"
  surfaceVariant: "#424940"
  onSurfaceVariant: "#c2c9bd"
  outline: "#8c9389"
  outlineVariant: "#424940"
  shadow: "#000000"
  scrim: "#000000"
  inverseSurface: "#e0e4db"
  inverseOnSurface: "#2d322c"
  inversePrimary: "#38693c"
  primaryFixed: "#b9f0b7"
  onPrimaryFixed: "#002107"
  primaryFixedDim: "#9ed49d"
  onPrimaryFixedVariant: "#1f5026"
  secondaryFixed: "#f7e388"
  onSecondaryFixed: "#211b00"
  secondaryFixedDim: "#d9c770"
  onSecondaryFixedVariant: "#524600"
  tertiaryFixed: "#dce1ff"
  onTertiaryFixed: "#02174b"
  tertiaryFixedDim: "#b5c4ff"
  onTertiaryFixedVariant: "#344478"
  surfaceDim: "#101410"
  surfaceBright: "#363a34"
  surfaceContainerLowest: "#0b0f0b"
  surfaceContainerLow: "#181d18"
  surfaceContainer: "#1c211b"
  surfaceContainerHigh: "#272b26"
  surfaceContainerHighest: "#313630"
typography:
  display-large:
    fontFamily: Fraunces
    fontSize: 57px
    fontWeight: 400
    lineHeight: 1.1
  display-medium:
    fontFamily: Fraunces
    fontSize: 48px
    fontWeight: 400
    lineHeight: 1.1
  display-small:
    fontFamily: Fraunces
    fontSize: 40px
    fontWeight: 400
    lineHeight: 1.1
  headline-large:
    fontFamily: Fraunces
    fontSize: 33px
    fontWeight: 400
    lineHeight: 1.2
  headline-medium:
    fontFamily: Fraunces
    fontSize: 28px
    fontWeight: 400
    lineHeight: 1.2
  headline-small:
    fontFamily: Fraunces
    fontSize: 23px
    fontWeight: 400
    lineHeight: 1.2
  title-large:
    fontFamily: Fraunces
    fontSize: 19px
    fontWeight: 500
    lineHeight: 1.2
  title-medium:
    fontFamily: Fraunces
    fontSize: 16px
    fontWeight: 500
    lineHeight: 1.2
  title-small:
    fontFamily: Fraunces
    fontSize: 13px
    fontWeight: 500
    lineHeight: 1.2
  body-large:
    fontFamily: Gabarito
    fontSize: 16px
    fontWeight: 400
    lineHeight: 1.5
  body-medium:
    fontFamily: Gabarito
    fontSize: 13px
    fontWeight: 400
    lineHeight: 1.5
  body-small:
    fontFamily: Gabarito
    fontSize: 11px
    fontWeight: 400
    lineHeight: 1.5
  label-large:
    fontFamily: Gabarito
    fontSize: 13px
    fontWeight: 500
    lineHeight: 1.4
  label-medium:
    fontFamily: Gabarito
    fontSize: 11px
    fontWeight: 500
    lineHeight: 1.4
  label-small:
    fontFamily: Gabarito
    fontSize: 9px
    fontWeight: 500
    lineHeight: 1.4
rounded:
  xs: 4px
  sm: 8px
  md: 12px
  lg: 16px
  xl: 24px
  full: 9999px
spacing:
  xs: 4px
  sm: 8px
  md: 16px
  lg: 24px
  xl: 48px
components:
  button-primary:
    backgroundColor: "{colors.primary}"
    textColor: "{colors.onPrimary}"
    typography: "{typography.label-large}"
    rounded: "{rounded.full}"
    padding: "{spacing.md}"
    height: "40px"
  button-primary-hover:
    backgroundColor: "{colors.primary}"
    textColor: "{colors.onPrimary}"
    stateLayer: "{colors.onPrimary}"
    stateLayerOpacity: "8%"
  button-primary-pressed:
    backgroundColor: "{colors.primary}"
    textColor: "{colors.onPrimary}"
    stateLayer: "{colors.onPrimary}"
    stateLayerOpacity: "10%"
  button-primary-disabled:
    backgroundColor: "{colors.onSurface}"
    backgroundOpacity: "12%"
    textColor: "{colors.onSurface}"
    textOpacity: "38%"
  button-secondary:
    backgroundColor: "{colors.secondaryContainer}"
    textColor: "{colors.onSecondaryContainer}"
    typography: "{typography.label-large}"
    rounded: "{rounded.full}"
    padding: "{spacing.md}"
    height: "40px"
  button-secondary-hover:
    backgroundColor: "{colors.secondaryContainer}"
    textColor: "{colors.onSecondaryContainer}"
    stateLayer: "{colors.onSecondaryContainer}"
    stateLayerOpacity: "8%"
  button-text:
    backgroundColor: "transparent"
    textColor: "{colors.primary}"
    typography: "{typography.label-large}"
    rounded: "{rounded.full}"
    padding: "{spacing.sm}"
    height: "40px"
  button-text-hover:
    backgroundColor: "transparent"
    textColor: "{colors.primary}"
    stateLayer: "{colors.primary}"
    stateLayerOpacity: "8%"
  input-field:
    backgroundColor: "{colors.surfaceContainerHighest}"
    textColor: "{colors.onSurface}"
    typography: "{typography.body-large}"
    rounded: "{rounded.xs}"
    padding: "{spacing.md}"
    height: "56px"
    outlineColor: "{colors.outline}"
    outlineWidth: "1px"
  input-field-focused:
    backgroundColor: "{colors.surfaceContainerHighest}"
    textColor: "{colors.onSurface}"
    outlineColor: "{colors.primary}"
    outlineWidth: "2px"
  input-field-error:
    backgroundColor: "{colors.surfaceContainerHighest}"
    textColor: "{colors.error}"
    outlineColor: "{colors.error}"
    outlineWidth: "2px"
  input-field-disabled:
    backgroundColor: "{colors.onSurface}"
    backgroundOpacity: "4%"
    textColor: "{colors.onSurface}"
    textOpacity: "38%"
    outlineColor: "{colors.onSurface}"
    outlineOpacity: "12%"
    outlineWidth: "1px"
  card:
    backgroundColor: "{colors.surfaceContainerLow}"
    textColor: "{colors.onSurface}"
    rounded: "{rounded.md}"
    padding: "{spacing.md}"
  chip:
    backgroundColor: "{colors.surfaceContainerLow}"
    textColor: "{colors.onSurfaceVariant}"
    typography: "{typography.label-large}"
    rounded: "{rounded.sm}"
    padding: "{spacing.sm}"
    height: "32px"
  chip-selected:
    backgroundColor: "{colors.secondaryContainer}"
    textColor: "{colors.onSecondaryContainer}"
  tooltip:
    backgroundColor: "{colors.inverseSurface}"
    textColor: "{colors.inverseOnSurface}"
    typography: "{typography.body-small}"
    rounded: "{rounded.xs}"
    padding: "{spacing.sm}"
---

## Overview

Bossa is a system for products that want to feel *composed* — not in the formal sense, but in the musical one. Like its namesake, it favors a strict underlying structure (a 16px grid, a fixed type scale, a defined palette) that exists to be played with: components offset from where the eye expects them, headlines that breathe across a column gutter, type sizes that step a beat larger than the system "needs". The geometry is the metronome; the curves and saturated colors are the improvisation.

Visually the brand sits at the intersection of editorial publication and modern field guide. Photography is documentary nature work — high-saturation, golden-hour, often slightly off-center compositions where the subject sits in a quiet quarter of the frame. Illustration, if used at all, leans into hand-drawn botanical or topographic linework. Stock imagery is forbidden.

The default scheme is dark because the saturated earth-and-ocean palette resolves best on a slightly green-tinted graphite (`surface`, `#101410`) — the same way jewel tones pop on black velvet. In light mode the surfaces warm to an off-white (`#f7fbf2`) that still carries a whisper of the primary hue.

- **Main color scheme:** Dark
- **Design framework:** Material Design 3
- **Iconography:** Material Symbols, Rounded
- **Image style:** Documentary nature photography, saturated, rhythmically asymmetric compositions

## Colors

The palette is a saturated earth-and-ocean triad: **forest moss** anchors the system, **golden ochre** carries supporting weight, **slate indigo** provides the cool counterpoint. Color in Bossa is not decoration — it is meaning. Each role does one thing only.

- **Forest moss** (`primary`, `#9ed49d` in dark / `#38693c` in light) is the voice of action. It marks the single most important call-to-action per view and the brand mark itself. The dark-mode tone (palette tone 80) feels lit-from-within; the light-mode tone (palette tone 40) reads as deep undergrowth. Either way it carries the brand.
- **Golden ochre** (`secondary`, `#d9c770` in dark / `#6c5e10` in light) handles supporting actions, selected states, and accent moments where the eye should pause but not leap. Think of it as the warm spotlight that catches an editor's pull-quote without competing with a primary action.
- **Slate indigo** (`tertiary`, `#b5c4ff` in dark / `#4c5c92` in light) is the cool counterpoint — used for informational chips, secondary data visualizations, and the rare moment when the palette needs a third voice. It refuses to be loud, which is precisely why it's effective in small doses.
- **Mossy graphite** (`surface`, `#101410`) is the dark-mode page. It is not pure black; the neutral palette derives its hue from the primary, so the surface carries a barely-perceptible green undertone. In light mode the equivalent is a warm off-white (`#f7fbf2`) — paper that has seen sunlight, not bleached card stock.

Tonal palette tones worth knowing when discussing the system: primary tone 40 (`#38693c`) is the brand-mark color in print contexts; secondary tone 95 (`#fff1b9`) is the upper bound for warm highlights in light mode; tertiary tone 30 (`#344478`) is the slate-indigo container in light mode and a useful "deep but cool" accent in either scheme.

## Typography

Two voices share the system, and the contrast between them is intentional. **Fraunces** carries every title and headline (`display-large` down through `title-small`) — a contemporary serif with optical-size axes that lets its weight shift naturally as it scales up. At `display-large` (57px) Fraunces gets to perform; at `title-small` (13px) it tightens into utility. The variable-font features (especially the SOFT and WONK axes) are *encouraged* for editorial moments where a headline can afford a beat of personality.

**Gabarito** handles body and label work — a geometric sans with friendly curves that read well at small sizes and stay legible against the saturated surfaces. `body-large` (16px) is the default for any sustained reading; `body-medium` (13px) for secondary text and metadata; `body-small` (11px) reserved for footnotes and inline references where the reader has explicitly signaled "I want the fine print".

Labels (`label-large` 13px, `label-medium` 11px) use Gabarito at weight 500. For categorical chips and status markers, set them in uppercase and add `letterSpacing: 0.08em` in the typography token — the geometry holds tracking well and the slight wide set reinforces the "this is a tag, not a word" reading.

A note on weights: do not introduce more than two weights of Fraunces or Gabarito on a single screen. The variable axes give you all the expressive range you need within one weight; reaching for a second is usually a sign of an unresolved hierarchy.

## Layout

The system runs on a **fluid 12-column grid** on desktop with a **fixed 1280px max-width**, transitioning to a 4-column grid on mobile. Gutters are constant at `spacing.lg` (24px); margins are `spacing.xl` (48px) on desktop and `spacing.md` (16px) on mobile.

The 16px rhythm (`spacing.md`) is the heartbeat. Every other step is harmonic: `xs` (4px) and `sm` (8px) for inner padding and tight clusters, `lg` (24px) for region separation, `xl` (48px) for major page-level breaks. Do not mix the scale with arbitrary values — if the rhythm doesn't fit, the layout is wrong, not the scale.

**Rhythmic asymmetry** is a core principle. Don't center compositions unless centering carries meaning. A 12-column grid lets you offset a heading from columns 2–7 while its supporting image sits in 8–12; that quiet displacement is what gives Bossa its bossa. Use it on hero sections, article openers, and any moment that wants visual emphasis without yelling.

## Elevation & Depth

Depth is conveyed through **tonal layering**, not shadows. The progression starts at `surfaceContainerLowest` (`#0b0f0b`) — the recessed page bed — and steps up through `surfaceContainerLow` (`#181d18`) for cards, `surfaceContainer` (`#1c211b`) for sustained content regions, and `surfaceContainerHigh` (`#272b26`) for modals, menus, and bottom sheets. The whole progression carries the same mossy undertone as `surface`, so depth feels like layered fabric rather than stacked planes of glass.

Shadows are reserved for one case only: floating action buttons or pinned overlays that genuinely sit *above* scrolling content. Even then, prefer `outlineVariant` (`#424940`) as a hairline divider before reaching for `shadow`. If two regions need to be distinguished, change the surface container level; don't draw a line between them.

## Shapes

The shape language follows the brand thesis directly: **geometric grids softened by organic curves**. Most surfaces stay rectangular with light rounding — cards at `rounded.md` (12px), inputs at `rounded.xs` (4px), section dividers fully square. The base reads as architectural.

Buttons are the deliberate exception. Every button takes `rounded.full` (the pill) — an organic counterpoint to the rectilinear base. A pill button on a square card is the shape-language equivalent of a syncopated melody over a steady bass line. Avatars are full circles. Chips take `rounded.sm` (8px) — softened, not pilled, because they sit alongside text and full-pill chips break the line. Tooltips take `rounded.xs` so they read as system speech, not decorative bubbles.

## Components

The button system uses M3's tonal hierarchy with intent: filled (`button-primary`) marks the single critical action per view, tonal (`button-secondary`) handles supporting actions where the page expects forward motion but not urgency, text-only (`button-text`) is for cancel, dismiss, and tertiary navigation. Hover and pressed states do not change color — they shift by a single elevation step. Color is too expensive a signal in this palette to spend on state changes.

Inputs are filled (`input-field` on `surfaceContainerHighest`), with a subtle bottom-edge focus state that uses `primary` as the focus indicator. Error state (`input-field-error`) shifts the text color to `error` (`#ffb4ab`) but keeps the same track — the error is a fact, not an alarm. Inputs sit at `rounded.xs` (4px) because they are write-targets, distinct from buttons which are press-targets.

Cards (`card`) lift to `surfaceContainerLow` at `rounded.md` with `spacing.md` of internal padding. They never carry shadows; depth comes from the tonal step alone. Chips (`chip`) are compact, set in `label-large` Gabarito at weight 500, `rounded.sm`. Selected chips switch to `secondaryContainer` (the ochre family), reinforcing the rule that ochre marks selection. Tooltips (`tooltip`) use `inverseSurface` so they feel like the system speaking in voiceover — light text on a light surface in dark mode, the inverse in light mode.

## Do's and Don'ts

- Do use `primary` (forest moss) for exactly one action per screen — the one whose absence would cost the user the most.
- Don't use `tertiary` (slate indigo) as a button color. It belongs to informational chips and the occasional accent moment.
- Do embrace asymmetric layouts on hero moments; a 12-column grid is permission, not a cage.
- Don't introduce shadows. The tonal-layer system carries every legitimate depth case.
- Do let Fraunces play at display sizes — the variable-font axes (especially SOFT/WONK) are part of the brand voice at `display-large` and `display-medium`.
- Don't pair more than two weights of either font on a single screen. If the hierarchy needs a third weight, the hierarchy needs work, not another weight.
- Do scale spacing by the named steps (`xs`, `sm`, `md`, `lg`, `xl`); a layout that needs a 20px gap is a layout that wants 16px or 24px and hasn't decided yet.
- Don't mix `rounded.full` shapes with `rounded.md`+ shapes in a single composition outside the established button-on-card pattern. Pills against squares is the look; pills against pills against rectangles is noise.
- Do maintain WCAG AA contrast: 4.5:1 for body text, 3:1 for large text. The default dark-scheme palette satisfies this; verify any new color before adopting it.
- Don't reach outside the 49-role M3 palette for a new color before checking whether `tertiaryContainer`, `surfaceContainerHigh`, or a tonal-palette tone already solves the problem. They almost always do.
