---
name: material-design-md
description: Generate a high-quality DESIGN.md file (the open Google-Labs spec for brand & design-system documentation) grounded in Material Design 3. Use this skill whenever the user wants to create, scaffold, draft, or generate a DESIGN.md, a design-system spec, a brand design document, a Material 3 design system, an MD3 spec, design tokens for an agentic design tool, or asks to "produce a DESIGN.md" — even if they don't name the spec explicitly. Also use this skill when the user describes a brand and asks for tokens, color schemes, type scale, spacing scale, or component styles together in a single markdown deliverable. The skill collects brand inputs (name, style phrase, seed or three brand colors, fonts, scheme, scale ratios), runs a Python or Node.js script to deterministically generate the YAML frontmatter (M3 tokens for colors, typography, rounded, spacing, components), and then writes rich brand-aligned prose for the eight DESIGN.md sections.
license: MPL-2.0
metadata:
  version: 1.0.1
  author: Darlan Rod <darlan@rodot.dev>
  repository: https://github.com/darlanrod/material-design-md
  tags:
    - design-system
    - design-tokens
    - material-design-3
    - material-you
    - design-md
    - agentic-design
---

# DESIGN.md Generator (Material Design 3)

This skill produces a complete `DESIGN.md` file that:

1. Conforms to the [DESIGN.md spec](https://github.com/google-labs-code/design.md/blob/main/docs/spec.md) — YAML frontmatter with design tokens, followed by eight markdown sections.
2. Uses Material Design 3 conventions for colors (Tonal Spot variant), the full 15-level M3 type scale, M3 spacing and shape scales, and a canonical set of component tokens.
3. Pairs deterministic, machine-generated tokens with **rich, brand-aligned prose** that gives downstream agentic design tools enough context to make decisions consistent with the brand's voice.

The split is deliberate: scripts handle math (color palette generation, type scale calculation, token references); the agent handles language (Overview prose, the rationale for color choices, voice-aware Do's and Don'ts). Together they produce a document that's both parseable *and* opinionated.

## Inputs

Before generating, gather these inputs. **If any are missing, ask the user via `AskUserQuestion` — don't guess.** Group missing fields into one question wherever possible.

### Required

| Field | Example | Notes |
|---|---|---|
| Brand name | `"Bossa"` | Goes into `name:` and the `# Title` heading. |
| General style | `"Clean geometric grids softened by organic curves"` | Free phrase. Drives the Overview prose. Saved as `description:`. |
| Seed color **OR** Primary/Secondary/Tertiary | `"#38693c"` OR `"#38693c" "#6c5e10" "#4c5c92"` | Mutually exclusive. Seed mode is M3-canonical (one color derives everything); custom-triplet mode lets the brand pin three distinct hues. |
| Main color scheme | `light` or `dark` | The scheme that lives in `colors:` (the other is documented in prose). |
| Image style | `"Editorial nature photography, saturated"` | Free phrase. Goes into Overview. |
| Title font | `"Fraunces"` | Used by display/headline/title levels. |
| Body font | `"Gabarito"` | Used by body/label levels. |

### Optional (with defaults)

| Field | Default | Notes |
|---|---|---|
| Font base size | `16` | px. Sets `body-large` size; everything else scales geometrically from this. |
| Type scale ratio | `1.2` | Geometric ratio between adjacent type-scale steps. M3 default. |
| Spacer base | `16` | px. Drives `xs`..`xl` (×0.25, ×0.5, ×1, ×1.5, ×3). |
| Rounder base | `4` | px. Drives `rounded.xs`..`xl` (×1, ×2, ×3, ×4, ×6). |
| Version label | `"alpha"` | Goes into `version:` in the frontmatter. |

If the user gives partial inputs, ask for *only* what's missing. Don't re-collect what they already provided.

### Asking pattern

Use one `AskUserQuestion` call grouping the gaps. Prefer multiple-choice when reasonable (e.g., scheme = light/dark, color mode = seed vs triplet), and leave free text for names/phrases via the "Other" option.

## Workflow

**Read these references before you begin so the prose and tokens land correctly:**

- `references/spec.md` — Excerpt of the DESIGN.md spec (section order, schema, conventions for unknown tokens). The output must conform.
- `references/material-design-3.md` — M3 token naming, the canonical component set the script emits, palette guidance, rationale.
- `references/prose-guide.md` — How to write each markdown section so the prose is brand-aligned and useful to downstream design agents. **The single highest-leverage reference — read it before writing prose.**

Then execute:

### Step 1 — Generate the tokens (deterministic)

Run the token generator and capture its `--json` output so you have the palette tones for prose. Choose **Python** unless the environment is Node-only:

```bash
# Python (preferred — uses the most current M3 contrast-curve algorithm)
python3 scripts/generate_design_tokens.py \
  --brand-name "Bossa" \
  --description "Clean geometric grids softened by organic curves, saturated earth-and-ocean palettes, and rhythmic asymmetry." \
  --seed "#38693c" \
  --scheme dark \
  --title-font "Fraunces" \
  --body-font "Gabarito" \
  --json > /tmp/tokens.json
```

Or with a custom triplet:

```bash
python3 scripts/generate_design_tokens.py \
  --brand-name "Bossa" \
  --primary "#38693c" --secondary "#6c5e10" --tertiary "#4c5c92" \
  --scheme dark --title-font "Fraunces" --body-font "Gabarito" \
  --json > /tmp/tokens.json
```

Node alternative (only when Python is unavailable):

```bash
node scripts/generate_design_tokens.js [same flags...] --json > /tmp/tokens.json
```

> **Why prefer Python:** the `materialyoucolor` package in Python uses the updated M3 contrast-curve algorithm for `on*Container` colors (better accessibility). The Node `@material/material-color-utilities` v0.2.7 uses the original 2022 M3 algorithm. For **dark** scheme the outputs are byte-identical between runtimes. For **light** scheme they differ on 4 colors (`onPrimaryContainer`, `onSecondaryContainer`, `onTertiaryContainer`, `onErrorContainer`) regardless of whether you used seed or triplet mode — Python yields lighter, higher-contrast on-container tones; Node yields the strict tone-10 tones from the original M3 spec. Both are valid M3. Pick one runtime and stick with it.

Also run **without** `--json` to get the YAML frontmatter you'll embed in the final file:

```bash
python3 scripts/generate_design_tokens.py [same flags...] > /tmp/frontmatter.yaml
```

> **CRITICAL — copy the frontmatter literally.** When you assemble the final DESIGN.md, copy the script's YAML output **byte-for-byte** into the file (between the `---` delimiters). Do **not** retype hex codes from memory, "round" decimals, or normalize whitespace. The whole point of the deterministic generator is reproducibility — two people with the same seed must end up with the same tokens. The simplest reliable approach is: write the frontmatter to a temp file with `--output /tmp/frontmatter.yaml`, then read that file and embed its contents verbatim. Never paraphrase the colors block.

### Step 2 — Read the JSON to ground your prose

The JSON gives you:

- `colors` — the 49 M3 role tokens for the chosen scheme (hex codes).
- `opposite_scheme.colors` — the same roles for the *other* scheme. Reference these in the markdown body when discussing how the design behaves in both modes.
- `palettes` — tones 0..100 (stepped) for `primary`, `secondary`, `tertiary`, `neutral`, `neutral-variant`. Use these when prose names a specific tone (e.g., "primary tone 40 anchors the brand mark").
- `typography`, `rounded`, `spacing`, `components` — exact computed values.

Read the JSON before writing prose. Concrete numbers are the difference between generic copy and a document that feels grounded in the actual system.

### Step 3 — Compose the DESIGN.md

Assemble the final file in this order. **Section order is normative per the spec.** Use H1 only for the brand title; sections use H2.

```
# {Brand name}

{YAML frontmatter from step 1, including the --- delimiters}

## Overview
## Colors
## Typography
## Layout
## Elevation & Depth
## Shapes
## Components
## Do's and Don'ts
```

For each section, follow the prose rubric in `references/prose-guide.md`. The rubric tells you what to cover and what tone to strike — it's the most important reference for quality.

A few cross-section principles to keep in mind while writing:

- **Token names are normative, descriptive names are mnemonic.** Prose may say "forest moss anchors the brand" while the token is `primary`. Always pair the two on first mention: *"forest moss (`primary`, #38693c)"*. After first mention, either name is fine.
- **Reference both schemes when relevant.** "In light mode the surface reads as warm linen (#FAF9FF); in dark mode it inverts to graphite (#131318)." The reader needs both pictures.
- **No filler.** If a section can't say something substantive about *this* brand, write less rather than padding. The agent at the other end of this document is reading every line for signal.
- **The Overview is where the brand lives.** Most other sections are technical; the Overview is your one chance to encode personality. Spend the writing budget there.

### Step 4 — Output the file

Write to `outputs/DESIGN.md` (or the path the user specified) and share via a `computer://` link.

## Quality checks before delivering

1. **Frontmatter parses:** `python3 -c "import yaml; yaml.safe_load(open('outputs/DESIGN.md').read().split('---')[1])"` must succeed.
2. **Section order matches the spec:** Overview → Colors → Typography → Layout → Elevation & Depth → Shapes → Components → Do's and Don'ts.
3. **Every hex code is lowercase 6 digits with leading `#`.** (The script enforces this; if you write hexes by hand in prose, match.)
4. **Token references in prose use the actual token names** from the YAML (`primary`, `body-large`, `surfaceContainerHighest`, etc.), not invented ones.
5. **No duplicate H2 headings.** The spec rejects files with duplicate sections.
6. **Overview ends with the canonical four-bullet block:** Main color scheme / Design framework / Iconography / Image style. All four bullets present, in that order.
7. **The colors block in YAML is byte-for-byte the script's output.** Diff the final file's frontmatter against the script's `--output` file if in doubt. Drift here defeats the whole point of the deterministic generator.
8. **Brand voice is consistent across sections.** Read the whole file once after writing. If "playful and irreverent" appears in Overview but Components prose is dry technical writing, fix it.

## Examples

A complete reference output lives at `assets/example-design.md`. Skim it before composing your first file to calibrate length and tone — it's not a template to fill in, but a quality bar to match.

## When NOT to use this skill

- The user wants a Figma-native design system or wants tokens written *to* Figma. Use a Figma skill instead.
- The user wants raw Material 3 token JSON without prose. Use `--json` on the script and return the JSON directly without writing markdown.
- The user wants a Tailwind config or CSS variables. The DESIGN.md format is intentionally agnostic — convert *afterward* if needed; this skill produces the source of truth, not the implementation.
- The user wants a UI component library or actual code. This document describes the system; it isn't the system itself.
