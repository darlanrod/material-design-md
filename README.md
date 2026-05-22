# material-design-md

> Generate a high-quality **DESIGN.md** file — the open Google-Labs spec for brand and design-system documentation — grounded in **Material Design 3**.

[![License: MPL 2.0](https://img.shields.io/badge/License-MPL%202.0-brightgreen.svg)](https://www.mozilla.org/en-US/MPL/2.0/)
[![Skill: SKILL.md](https://img.shields.io/badge/Skill-SKILL.md-blueviolet)](./SKILL.md)
[![Spec: DESIGN.md](https://img.shields.io/badge/Spec-DESIGN.md-blue)](https://github.com/google-labs-code/design.md)
[![Material 3](https://img.shields.io/badge/Material-3-1976D2)](https://m3.material.io/)

A self-contained agent skill that turns a few brand inputs (name, style phrase, seed color or three brand colors, fonts) into a complete, ready-to-use `DESIGN.md` file: 49 Material 3 color role tokens, 15 typography levels, spacing and shape scales, 13 component tokens — all paired with eight markdown sections of rich, brand-aligned prose written for downstream agentic design tools.

---

## What it produces

Given inputs like *"Bossa — clean geometric grids softened by organic curves, dark scheme, Fraunces + Gabarito, primary #38693c, secondary #6c5e10, tertiary #4c5c92"*, the skill produces a single `DESIGN.md` containing:

- YAML frontmatter with **49 M3 color roles** (Tonal Spot variant), **15 typography levels**, **rounded** (`xs`..`xl` + `full`), **spacing** (`xs`..`xl`), and **13 component tokens** with proper `{token.references}`.
- Eight markdown sections in spec order: **Overview**, **Colors**, **Typography**, **Layout**, **Elevation & Depth**, **Shapes**, **Components**, **Do's and Don'ts** — each written to give downstream design agents concrete decision rules in your brand's voice.

See [`assets/example-design.md`](./assets/example-design.md) for a complete reference output.

---

## Install

The skill is installable in three ways, depending on which agent or IDE you use.

### Option 1 — Universal: `npx skills add` (recommended)

Works with **any** agent that follows the [open SKILL.md convention](https://github.com/vercel-labs/skills) (Claude Code, Cursor, Cline, Continue, Codex, and more):

**Install for all detected agents in the current project**
```bash
npx skills add darlanrod/material-design-md
```

**Install for a specific agent**
```bash
npx skills add darlanrod/material-design-md -a claude-code
```

**Install globally (available across all projects)**
```bash
npx skills add darlanrod/material-design-md --global
```

**Equivalent CLIs in the same ecosystem also work:**

```bash
npx add-skill darlanrod/material-design-md
```
```bash
npx clawhub@latest install darlanrod/material-design-md
```

### Option 2 — Claude Cowork / Claude Code (drag-and-drop)

Download the latest `material-design-md.skill` bundle from the [Releases page](https://github.com/darlanrod/material-design-md/releases) and drag it into Claude Cowork, or place it in `~/.claude/skills/` for Claude Code.

### Option 3 — Standalone (no AI agent required)

The token generator runs perfectly well on its own. Clone the repo or vendor `scripts/` into your project:

```bash
git clone https://github.com/darlanrod/material-design-md
cd material-design-md/scripts

# Python
pip install materialyoucolor
python3 generate_design_tokens.py --help

# Node.js
npm install
node generate_design_tokens.js --help
```

---

## Update

If you installed via `npx skills add`, pull the latest version with the `update` command. See the [CHANGELOG](./CHANGELOG.md) for what changed in each release.

```bash
# Update only this skill
npx skills update material-design-md

# Update all installed skills at once
npx skills update

# Restrict to global OR project scope (auto-detected if omitted)
npx skills update material-design-md -g    # global only
npx skills update material-design-md -p    # project only

# Non-interactive (CI/CD friendly) — auto-detects scope
npx skills update material-design-md -y
```

For other install methods:

- **Drag-and-drop `.skill` (Claude Cowork)** — download the new `material-design-md.skill` from the [Releases page](https://github.com/darlanrod/material-design-md/releases/latest) and drop it in; it replaces the previous version.
- **Standalone clone** — `cd material-design-md && git pull` (then re-run `pip install -U materialyoucolor` or `npm install` if dependencies bumped).

To remove the skill entirely: `npx skills remove material-design-md`.

---

## Quickstart

Once the skill is installed, just describe the brand and your agent does the rest:

> *"Generate a DESIGN.md for Bossa — clean geometric grids softened by organic curves, saturated earth-and-ocean palettes, and rhythmic asymmetry. Dark scheme, Fraunces for titles and Gabarito for body, primary `#38693c`, secondary `#6c5e10`, tertiary `#4c5c92`."*

The agent collects any missing inputs, runs the deterministic token generator, then composes the eight markdown sections from your brand description. Output: a single `DESIGN.md` you can hand to any downstream design agent (Figma plugins, Tailwind generators, component libraries) as the source of truth.

### Direct script use

```bash
# Single-seed mode (M3 canonical — derives everything from one color)
python3 scripts/generate_design_tokens.py \
  --brand-name "Bossa" \
  --description "Clean geometric grids softened by organic curves, saturated earth-and-ocean palettes, and rhythmic asymmetry." \
  --seed "#38693c" \
  --scheme dark \
  --title-font "Fraunces" --body-font "Gabarito" \
  > frontmatter.yaml

# Custom-triplet mode (you control primary/secondary/tertiary)
python3 scripts/generate_design_tokens.py \
  --brand-name "Bossa" \
  --primary "#38693c" --secondary "#6c5e10" --tertiary "#4c5c92" \
  --scheme dark \
  --title-font "Fraunces" --body-font "Gabarito" \
  > frontmatter.yaml

# JSON mode (returns tokens + tonal palettes — useful when building tooling on top)
python3 scripts/generate_design_tokens.py [flags...] --json > tokens.json
```

Node.js variant:

```bash
node scripts/generate_design_tokens.js [same flags...]
```

---

## Inputs reference

| Input | Required | Default | Notes |
|---|---|---|---|
| `--brand-name` | yes | — | Brand or project name. |
| `--seed` **OR** `--primary` + `--secondary` + `--tertiary` | yes | — | One color (M3-canonical derivation) OR three brand-pinned colors. |
| `--scheme` | yes | `light` | `light` or `dark` — which scheme lives in `colors:`. |
| `--title-font` | yes | — | Font family for titles (display, headline, title). |
| `--body-font` | yes | — | Font family for body and label. |
| `--description` | no | — | One-line brand style phrase. Goes into `description:` in YAML. |
| `--font-base` | no | `16` | Body base size in px. |
| `--type-scale` | no | `1.2` | Geometric ratio between type-scale steps. |
| `--spacer` | no | `16` | Base spacing unit in px. |
| `--rounder` | no | `4` | Base corner-radius unit in px. |
| `--version` | no | `alpha` | Schema version label in `version:`. |
| `--no-components` | no | (off) | Skip the components: token block. |
| `--json` | no | (off) | Output JSON (tokens + palettes) instead of YAML. |
| `--output` / `-o` | no | stdout | Write to file instead of stdout. |

The full input collection workflow (including how the agent prompts for missing inputs) is documented in [`SKILL.md`](./SKILL.md).

---

## How it works

The skill is split into two layers — a deliberate separation between deterministic and creative work:

**Layer 1 — Deterministic token generation** (`scripts/`)

Python and Node.js implementations of the same generator. Both use the official [Material Color Utilities](https://github.com/material-foundation/material-color-utilities) (the same algorithm Flutter, Android, and Material Web use). For the **dark scheme** the two outputs are byte-identical regardless of color-input mode. For the **light scheme** they differ on four `on*Container` colors due to algorithm vintage: Python's `materialyoucolor` 3.x ships the newer M3 contrast-curve spec (lighter, higher-contrast on-container tones), Node's `@material/material-color-utilities` 0.2.x uses the original 2022 algorithm (strict tone-10). Both are valid M3.

**Layer 2 — Agentic prose composition** (`SKILL.md` + `references/`)

The agent reads the generated tokens, then writes brand-aligned prose for each section, guided by:

- [`references/spec.md`](./references/spec.md) — DESIGN.md conformance checklist.
- [`references/material-design-3.md`](./references/material-design-3.md) — M3 token conventions and rationale.
- [`references/prose-guide.md`](./references/prose-guide.md) — section-by-section writing rubric; this is the single highest-leverage reference for output quality.

Result: tokens are correct and consistent across projects; prose is grounded in *this* brand.

---

## Why Material Design 3 as the basis?

The DESIGN.md spec is intentionally framework-agnostic — any consistent token system works. This skill uses Material 3 because:

- M3's **Dynamic Color** algorithm produces accessible palettes from any seed.
- The 49-role color system covers every UI scenario most products need.
- Most agentic design tools (Flutter, Angular Material, MUI v6, M3 Web Components) speak M3 natively, so the output works out-of-the-box downstream.

If you need a non-M3 system (Apple HIG, shadcn, custom), this skill is the wrong tool — but the structure here is straightforward to fork and re-implement.

---

## Contributing

Issues and pull requests welcome. See [CONTRIBUTING.md](./CONTRIBUTING.md) for the full guide — including development setup, where the highest-leverage improvements live, code conventions, and the Python ↔ Node parity rule.

The short version: the areas with the highest leverage for improvement are the prose-writing rubric (`references/prose-guide.md`), the canonical component set in the token generator, and distribution adapters for AI tools that don't yet support `npx skills add`.

---

## License

[MPL-2.0](./LICENSE) © Darlan Rod

This means: you can use, modify, and redistribute this project — including inside closed-source or commercial work — as long as any modifications you make to the source files themselves remain open. See the [LICENSE](./LICENSE) file for the full text, or [Mozilla's MPL 2.0 FAQ](https://www.mozilla.org/en-US/MPL/2.0/FAQ/) for a plain-English explanation.

---

## Related

- [google-labs-code/design.md](https://github.com/google-labs-code/design.md) — the open DESIGN.md specification this skill targets.
- [material-foundation/material-color-utilities](https://github.com/material-foundation/material-color-utilities) — the M3 color algorithm.
- [vercel-labs/skills](https://github.com/vercel-labs/skills) — the open agent skills tool (`npx skills add`).
