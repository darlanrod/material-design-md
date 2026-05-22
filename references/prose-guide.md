# Writing the Markdown Body — Quality Rubric

This is the highest-leverage reference for the skill. The YAML tokens are mechanical; the prose is where a DESIGN.md earns its keep. A downstream design agent reading this file should come away with three things:

1. **A working palette of the brand in their head** — colors with character, fonts with intent, spacing with rhythm.
2. **Decision rules they can apply** — "use primary only for the single most important action per screen" is more useful than "primary is brand color".
3. **A voice to write in** — when the agent generates UI copy or component descriptions, the document should have already established the register.

If a section can't do at least one of those, cut it down. Pad nothing.

## Universal principles

### Pair token names with descriptive names

On first mention, always pair:

> The page anchors on a deep ink (`primary`, `#1a1c1e`) — a near-black that reads as authoritative without industrial coldness.

Token name in backticks; hex in backticks; descriptive phrase in prose. After the first mention, either name works.

### Reference *this* brand, not "a brand"

Bad: "The primary color is used for important actions."
Good: "Bottle green (`primary`, `#1f5a3d`) appears exactly once per screen — on the action that, if undone, would lose the user the most work."

The agent at the other end of this document is making thousands of micro-decisions. Specifics steer those; generalities don't.

### Both schemes, where it matters

The active scheme is in `colors:`; the opposite is in the JSON's `opposite_scheme`. Whenever a description's meaning changes between light and dark, name both:

> In light mode the surface (`#fcf8ff`) reads as warm white linen; in dark mode it inverts to a deep graphite (`#131318`) that lets the accent colors hold the eye.

### Length follows substance

Aim for roughly:

- Overview: 4–8 sentences (longest — this is where personality lives)
- Colors: short opener + tokens + 1–2 sentences per role
- Typography: 4–8 sentences explaining the system
- Layout, Elevation, Shapes: 3–6 sentences each
- Components: brief opener; tokens carry the load
- Do's and Don'ts: 4–8 concrete rules

If a section runs short because the brand is genuinely minimal there, leave it short. If it runs long, you're padding.

---

## Section-by-section guidance

### 1. Overview

**Job:** Encode brand personality so every downstream decision aligns.

**Must cover:**

- Who the brand is for (target audience, implicit if not given).
- The emotional register (playful? clinical? warm? austere?).
- The general visual style (echo the user's "general style" phrase but expand it).
- The image style (the user's image style phrase, in context).
- A subtle commitment: dense vs spacious, conservative vs expressive, restrained vs maximal.

**Must also include** the following four-bullet block at the end of the Overview. This is a canonical pattern — every DESIGN.md should carry it, even if the prose above already covered image style. The bullets serve as a "quick reference card" for an agent scanning the document; they should appear in this exact order:

- **Main color scheme:** Light or Dark (the value used in `colors:`).
- **Design framework:** Material Design 3.
- **Iconography:** Material Symbols, with the variant the brand uses (Rounded / Sharp / Outlined / Filled). Default is Rounded.
- **Image style:** A one-line restatement of the user's image-style phrase. Do not omit this even when the prose above mentions it — the bullet acts as a structured anchor.

If the user did not provide image-style input, ask before generating. Don't invent it.

**Example pattern:**

> Veritage speaks to readers who notice the difference between a typeface set with care and one that wasn't. The interface should feel like a well-edited magazine: confident in its hierarchy, warm in its restraint, never loud. Documentary photography — grainy, naturally lit, human — is the only image style. We default to a dark color scheme because most reading sessions happen at night, and graphite surfaces let amber accents do the work without shouting.
>
> - **Main color scheme:** Dark
> - **Design framework:** Material Design 3
> - **Iconography:** Material Symbols, Rounded
> - **Image style:** Documentary photography with visible grain, natural light, off-center compositions

### 2. Colors

**Job:** Explain what each palette is for, in this brand's language. Define the tokens via the frontmatter; let prose describe *role and feeling*.

**Pattern:**

1. One sentence framing the palette as a whole. ("The palette is rooted in two greens against warm neutrals.")
2. A short prose description of each of `primary`, `secondary`, `tertiary`, and one neutral — each with a descriptive name, the token name, and the hex. Mention *what it's used for* in this system.
3. If light vs dark behavior is interesting, a sentence on that.

**Pitfall:** Don't list all 49 tokens in prose. The YAML has them. Prose covers the 4–6 colors a designer actually thinks about.

**Example:**

> The palette pairs **deep ink** (`primary`, `#1a1c1e`) with a single evocative accent.
>
> - **Deep ink** (`primary`, `#1a1c1e`) anchors headlines and core text — chosen for permanence over freshness.
> - **Sophisticated slate** (`secondary`, `#6c7278`) handles utilitarian elements: borders, captions, metadata. Never used for an action.
> - **Vibrant earthy red** (`tertiary`, `#b8422e`) is the sole driver of interaction. It appears once on most screens, twice at most.
> - **Warm limestone** (`surface`, `#f7f5f2`) replaces pure white as the page foundation — softer, more organic.

### 3. Typography

**Job:** Explain the type *strategy* — which font carries what weight in the system.

**Pattern:**

1. A sentence positioning the two font choices. (What kind of voice does each font lend?)
2. Per role family (headlines, body, labels), one or two sentences on how it's used. Mention the actual font names and one or two specific tokens.
3. Optional: a sentence on letter-spacing or other type micro-decisions if the brand has a position.

**Pitfall:** Don't restate the type-scale table. The YAML has it.

**Example:**

> Two voices share the system. **Cormorant** carries narrative weight: every headline (`display-large`, `headline-medium`) is set in its semi-bold to feel literary, slightly editorial. **Montserrat** does the workmanlike job of `body-large` and below — its even rhythm makes long-form reading effortless. Labels (`label-medium`, `label-small`) borrow Montserrat as well but earn slight emphasis via weight (500), not size or color.

### 4. Layout

**Job:** Describe the spacing rhythm and any layout philosophy (grid model, containment, etc).

**Pattern:**

- One sentence on the layout model (fluid? fixed max-width? grid-based?).
- One or two sentences on the spacing scale — which step does what.
- If the brand has containment patterns (cards, regions with internal padding), describe them.

**Example:**

> The layout is a **fluid grid on mobile** transitioning to a **fixed 1200px max-width** on desktop. Components sit on a strict 16px rhythm (`spacing.md`), with the smaller steps (`xs`, `sm`) reserved for inner padding and the larger ones (`lg`, `xl`) used to separate distinct regions. Cards hold their content at `spacing.md` of internal padding — generous enough to feel breathable, not so loose that it reads as empty.

### 5. Elevation & Depth

**Job:** Define how hierarchy is conveyed. The default in M3 is *tonal layers*, not shadows.

**Pattern:**

- One sentence stating the approach (tonal layers, shadows, borders, or a hybrid).
- If tonal: name two or three surface levels (`surfaceContainerLow`, `surfaceContainerHigh`, etc.) and what sits on each.
- If shadows: specify spread, blur, and color.
- If flat: explain what does the work instead (color contrast, weight contrast, scale).

**Example:**

> Depth comes from **tonal layering**, not shadow. The page sits on `surface`; cards and elevated regions lift to `surfaceContainerLow`; modals and menus stand on `surfaceContainerHigh`. The progression is subtle by design — the eye registers the depth without consciously seeing it.

### 6. Shapes

**Job:** State the shape language and its tokens.

**Pattern:**

- One sentence on the philosophy (rounded soft? architectural sharp? mixed?).
- If mixed, explain *which* components use which radius (e.g., "Buttons are pill-shaped to signal interactivity; cards stay rectangular at `rounded.md`").
- If consistent, just state it.

**Example:**

> The shape language is **architectural** — minimal corner rounding throughout (4–12px range). Buttons are the one exception: they take `rounded.full` to read unambiguously as actionable. Everything else (cards, inputs, surfaces) sits between `rounded.xs` and `rounded.md`.

### 7. Components

**Job:** Brief opener, then let the YAML token block carry the specifics.

**Pattern:**

- 2–3 sentences framing the component approach.
- Specifically call out: how is the *primary action* indicated? How do disabled states look? Are inputs filled or outlined?
- Don't restate the YAML in prose.

**Example:**

> The button system follows M3's tonal hierarchy: filled (`button-primary`) for the one critical action per view, tonal (`button-secondary`) for supporting actions, and text-only (`button-text`) for cancel / dismiss. Inputs are filled (`input-field` uses `surfaceContainerHighest` as its track), with a subtle bottom-edge focus state rather than a heavy border. All interactive components share `rounded.full` for buttons and `rounded.xs` for inputs — a small visual cue that buttons are press-targets and inputs are write-targets.

### 8. Do's and Don'ts

**Job:** Hand the downstream agent a short list of *checkable* rules. This is the single most-actionable section.

**Pattern:** 4–8 imperatives, alternating Do and Don't. Concrete enough that an agent could test conformance. Use the bullet form.

**Tests for a good rule:**

- ✅ "Do use `primary` only for the single most important action per screen." (Checkable: count primary appearances.)
- ✅ "Don't mix `rounded.full` and `rounded.xs` corners in a single composition." (Checkable: scan the rounding used in one view.)
- ✅ "Do maintain WCAG AA contrast: 4.5:1 for body text, 3:1 for large text." (Checkable: contrast pair.)
- ❌ "Use color thoughtfully." (Not checkable, no signal.)

**Example:**

```
## Do's and Don'ts

- Do use `primary` for exactly one action per screen — the one whose absence would cost the user the most.
- Don't mix display fonts and body fonts in the same heading.
- Do let `surfaceContainerLow` carry cards; don't introduce shadows.
- Don't tighten letter-spacing on body text — Montserrat is metrically tuned for its default tracking.
- Do uppercase labels (`label-*`) only when they convey a category or status, never a verb.
- Don't introduce new colors outside the 49-role palette without first checking whether an existing token fits.
- Do scale spacing by the named steps (`xs`, `sm`, ...); don't pick arbitrary px values.
```

## Final pass: read it aloud

After composing all eight sections, read the whole document straight through. A few diagnostic questions:

- **Voice consistency:** Does the Overview's tone match what's in the Do's and Don'ts? If Overview says "playful and warm" and rules read like a manual, fix one of them.
- **Specificity:** Could you swap any sentence into another brand's DESIGN.md without changing meaning? If yes, that sentence is generic — rewrite it.
- **Decision power:** Does the document tell a downstream agent how to choose between two options it might face? (E.g., "When in doubt between `secondary` and `tertiary`, prefer `secondary` for supporting actions and reserve `tertiary` for highlights and one-off accents.")
