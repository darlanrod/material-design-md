# Contributing to material-design-md

Thanks for considering a contribution. This document explains how the project is structured, what kinds of changes are most welcome, and the small set of conventions that keep the skill predictable across releases.

## What this project is (and isn't)

material-design-md is a [Claude/agent skill](./SKILL.md) plus a pair of token-generator scripts (Python + Node.js). Its job is to turn brand inputs into a `DESIGN.md` file conforming to the [open Google-Labs spec](https://github.com/google-labs-code/design.md), grounded in Material Design 3.

**In scope:**
- Improving the deterministic token generator (more accurate M3 algorithm coverage, edge cases, additional input modes).
- Improving the prose-writing rubric (`references/prose-guide.md`) so the agent produces sharper, more brand-aligned output.
- Extending the canonical component set (`components:` in the generator) with patterns that show up across many design systems.
- Adapter work — making the skill installable in more AI tools (Cursor rules, Copilot instructions, etc).
- Documentation, examples, accessibility audits.

**Out of scope:**
- Non-M3 design systems. If you need Apple HIG, shadcn, or a custom system, fork and re-implement; the structure is straightforward to port. Pull requests adding "alternative system" modes to this repo will be declined to keep the core focused.
- Implementation code (React components, Flutter widgets, CSS). This project produces the *source of truth* document; it deliberately does not produce the implementation.

## Quick start for development

```bash
git clone https://github.com/darlanrod/material-design-md
cd material-design-md

# Python script
pip install materialyoucolor pyyaml
python3 scripts/generate_design_tokens.py --help

# Node.js script
cd scripts && npm install && cd ..
node scripts/generate_design_tokens.js --help
```

Sanity check both implementations stay in sync:

```bash
# Dark scheme should be byte-identical between Python and Node (any color mode)
python3 scripts/generate_design_tokens.py \
  --brand-name Test --seed "#38693c" --scheme dark \
  --title-font Inter --body-font Inter > /tmp/py.yaml
node scripts/generate_design_tokens.js \
  --brand-name Test --seed "#38693c" --scheme dark \
  --title-font Inter --body-font Inter > /tmp/js.yaml
diff /tmp/py.yaml /tmp/js.yaml  # should print nothing
```

A note on runtime parity: Python's `materialyoucolor` 3.x ships the newer M3 contrast-curve algorithm; Node's `@material/material-color-utilities` 0.2.x uses the original 2022 algorithm. For the **dark scheme** the two runtimes are byte-identical regardless of color-input mode. For the **light scheme** they diverge on 4 `on*Container` colors regardless of color-input mode (Python yields lighter, higher-contrast on-container tones; Node yields the strict tone-10 tones). Both are valid M3. This is documented in [SKILL.md](./SKILL.md) and is not a bug — but if a future Node release of the upstream package restores parity, a PR closing that gap is welcome.

## Where the high-leverage improvements are

Roughly in order of expected impact:

### 1. `references/prose-guide.md` — section-by-section writing rubric

This is the single document that most shapes the *quality* of the generated `DESIGN.md`. Concrete improvements that move the needle:

- Better examples in any of the eight sections. Real-world DESIGN.md files do not yet exist in volume; one well-written example beats three abstract rules.
- New diagnostic questions for the final "read it aloud" pass.
- Guidance for edge cases the current rubric doesn't cover (e.g. brands that explicitly want a flat palette, brands with non-English typography, brands targeting accessibility-first products).

### 2. `scripts/generate_design_tokens.{py,js}` — component set

The current canonical set (13 components) covers the most-used surfaces. Worth considering additions if a pattern shows up in 5+ real design systems:

- `alert`, `alert-warning`, `alert-error`, `alert-success`
- `nav-rail`, `nav-bar`
- `dialog`, `bottom-sheet`
- `progress-linear`, `progress-circular`

Keep each new component referencing foundation tokens (`{colors.*}`, `{rounded.*}`, etc.) — never inline hexes. The components section is a pattern, not a kitchen sink; if you add a component you should be ready to justify it.

### 3. `SKILL.md` workflow — input collection & quality checks

The current input flow assumes the user provides eight inputs. Improvements:

- Smarter handling of partial input (e.g. user says "use Inter for everything").
- Better default suggestions when the user is unsure (e.g. "for a dark scheme finance product, suggest these colors").
- Additional quality checks before delivery — e.g. WCAG contrast verification on all body-text role pairs.

### 4. Distribution adapters

Currently the skill installs natively in Claude Code/Cowork (via `.skill` drag-drop) and any tool that supports the `npx skills add` convention. A future `npx material-design-md install --target=cursor` (or similar) that detects the project and writes platform-specific rule files would meaningfully widen reach. See [README → How to install](./README.md#install) for the current state.

## Code conventions

### Python

- Target Python 3.10+. Use type hints (`from __future__ import annotations` to enable modern syntax on older versions).
- Standard library first; the only third-party dependency is `materialyoucolor`. Adding a new runtime dependency requires a strong justification in the PR description.
- Format with `black` (default settings).

### Node.js

- Target Node 18+. CommonJS (the script uses `require`) to avoid the ESM resolution quirks the upstream package has on newer versions.
- Only dependency: `@material/material-color-utilities@0.2.7`. Pinned because newer versions break.
- No build step. The script runs directly via `node generate_design_tokens.js`.

### Both scripts must produce identical CLI surfaces

If you add a flag to one, add it to the other in the same PR. Help text, error messages, validation rules, and output format all stay in lockstep. This is intentional and load-bearing — it means a downstream tool can pick either runtime and get the same behavior.

### Markdown style (SKILL.md, references, README)

- Prose first; lists only when the content is genuinely a list. Bullet-pointing a paragraph is a code smell.
- Token names in backticks (`primary`, `body-large`).
- Hex codes in backticks, always 6-digit lowercase (`#38693c`, not `#38693C` or `#386`).
- Section headings stay in the canonical order defined by the DESIGN.md spec.
- Don't add emoji unless they're load-bearing (e.g. mapping `✅ / ❌` to "do / don't"). The skill's voice is professional.

## Submitting a change

1. **Open an issue first** for anything non-trivial. A short conversation upfront usually saves a long one in the PR.
2. **Branch from `main`** with a descriptive name (`fix/python-node-onContainer-parity`, not `patch-1`).
3. **Keep PRs focused.** One concept per PR. Refactors and feature changes go in separate PRs.
4. **Update tests / examples / docs** in the same PR as the code change. Don't leave them for "later".
5. **Run both generators** and confirm the validation script before opening the PR:
   ```bash
   # Validates frontmatter, section order, hex casing, token refs
   python3 -c "
   import yaml, re, sys
   doc = open('assets/example-design.md').read()
   parts = doc.split('---', 2)
   fm = yaml.safe_load(parts[1])
   assert fm['name'], 'missing name'
   assert len(fm['colors']) >= 30, 'too few color roles'
   headings = re.findall(r'^## (.+)$', parts[2], re.MULTILINE)
   want = ['Overview','Colors','Typography','Layout','Elevation & Depth','Shapes','Components',\"Do's and Don'ts\"]
   assert headings == want, f'wrong section order: {headings}'
   print('OK')
   "
   ```
6. **Write a PR description that explains the why.** What problem does this solve? What was the alternative considered? Why this approach? A one-line PR title is fine; the description carries the substance.

## Reviewing

When reviewing someone else's PR:

- Confirm Python ↔ Node parity is preserved (run the diff command from "Quick start" above).
- Read the diff in the prose rubric / SKILL.md / references with a writer's eye. Does the new text actually help an agent make a decision, or is it word-count?
- Check that any new component tokens use `{path.to.token}` references and not inline hexes.
- Look for new dependencies. Each one is a tax on every future contributor.

## Licensing

By contributing you agree that your contributions will be licensed under the project's [MPL-2.0](./LICENSE) license. There's no separate CLA to sign — MPL handles this via the standard "inbound = outbound" convention.

If your employer requires a Contributor License Agreement before you can contribute, mention it in your first PR and we'll work it out.

## Communication

- **Bugs and concrete proposals:** GitHub Issues.
- **Open-ended design discussion:** GitHub Discussions (if enabled), otherwise Issues with a "discussion" label.
- **Security issues:** email darlan@rodot.dev directly. Please don't open public issues for vulnerabilities.

## Code of conduct

Be kind, assume good faith, and remember that maintainers and contributors are all spending volunteer time on this. Disagreement is fine; condescension isn't. If something feels off in an interaction, flag it — privately or publicly — and we'll work through it.
