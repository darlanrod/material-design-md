#!/usr/bin/env python3
"""
Generate Material Design 3 design tokens for a DESIGN.md file.

Produces the YAML frontmatter block (between `---` delimiters) that conforms to
the DESIGN.md specification at
https://github.com/google-labs-code/design.md/blob/main/docs/spec.md

Two color-input modes are supported (mutually exclusive):

  Seed mode:
      --seed "#38693c"
      Generates primary/secondary/tertiary palettes from a single seed color
      using the Material 3 Tonal Spot variant. This is the standard M3 dynamic
      color flow.

  Custom mode:
      --primary "#38693c" --secondary "#6c5e10" --tertiary "#4c5c92"
      Builds palettes directly from three brand-supplied colors. Neutral and
      neutral-variant palettes are derived from the primary hue with low chroma
      (6 and 8 respectively), matching Google's reference behavior.

Output modes:

  Default:       writes the YAML frontmatter (with leading/trailing `---`) to
                 stdout.
  --json:        writes a JSON payload to stdout containing the same tokens
                 plus the tonal palettes (tones 0..100 stepped) for both the
                 chosen scheme and the opposite scheme. Useful for the agent
                 when writing prose that references specific tones.

Requires the `materialyoucolor` PyPI package (>= 2.0).
"""

from __future__ import annotations

import argparse
import json
import math
import sys
from dataclasses import dataclass, field
from typing import Optional

try:
    from materialyoucolor.hct import Hct
    from materialyoucolor.scheme.scheme_tonal_spot import SchemeTonalSpot
    from materialyoucolor.dynamiccolor.material_dynamic_colors import (
        MaterialDynamicColors,
    )
    from materialyoucolor.dynamiccolor.dynamic_scheme import DynamicScheme
    from materialyoucolor.dynamiccolor.variant import Variant
    from materialyoucolor.palettes.tonal_palette import TonalPalette
except ImportError as exc:  # pragma: no cover
    sys.stderr.write(
        "Missing dependency 'materialyoucolor'. Install with:\n"
        "  pip install materialyoucolor\n"
        f"Original error: {exc}\n"
    )
    sys.exit(2)


# ---------------------------------------------------------------------------
# Configuration: the M3 color roles, M3 type scale, components canonical set.
# These are intentionally defined as data so the skill can read them and so
# the same data drives both YAML emission and the JSON output.
# ---------------------------------------------------------------------------

# Material Design 3 color roles. We use the camelCase attribute names from
# `MaterialDynamicColors` (which match the M3 spec) and emit YAML keys with the
# same camelCase, since this matches the Dart reference and the DESIGN.md spec
# allows any consistent naming convention.
COLOR_ROLES = [
    "primary",
    "surfaceTint",
    "onPrimary",
    "primaryContainer",
    "onPrimaryContainer",
    "secondary",
    "onSecondary",
    "secondaryContainer",
    "onSecondaryContainer",
    "tertiary",
    "onTertiary",
    "tertiaryContainer",
    "onTertiaryContainer",
    "error",
    "onError",
    "errorContainer",
    "onErrorContainer",
    "background",
    "onBackground",
    "surface",
    "onSurface",
    "surfaceVariant",
    "onSurfaceVariant",
    "outline",
    "outlineVariant",
    "shadow",
    "scrim",
    "inverseSurface",
    "inverseOnSurface",
    "inversePrimary",
    "primaryFixed",
    "onPrimaryFixed",
    "primaryFixedDim",
    "onPrimaryFixedVariant",
    "secondaryFixed",
    "onSecondaryFixed",
    "secondaryFixedDim",
    "onSecondaryFixedVariant",
    "tertiaryFixed",
    "onTertiaryFixed",
    "tertiaryFixedDim",
    "onTertiaryFixedVariant",
    "surfaceDim",
    "surfaceBright",
    "surfaceContainerLowest",
    "surfaceContainerLow",
    "surfaceContainer",
    "surfaceContainerHigh",
    "surfaceContainerHighest",
]

# Tones reported for each palette in the JSON output. Match the Dart custom
# script and the official M3 tonal palette tones list.
PALETTE_TONES = [0, 5, 10, 15, 20, 25, 30, 35, 40, 50, 60, 70, 80, 90, 95, 98, 99, 100]


@dataclass(frozen=True)
class TypoLevel:
    """One row in the M3 type scale.

    `size_step` is the integer exponent applied to `type_scale_ratio` relative
    to `font_base`. Negative numbers mean smaller than base. The exponent
    layout matches Google's published M3 type-scale ratios at a 1.2 ratio.
    """

    size_step: int
    weight: int
    line_height: float
    is_title: bool  # determines whether title or body font is used


# Full M3 type scale (15 levels). This matches the user's Dart reference and
# Material 3's published type system.
TYPE_SCALE: dict[str, TypoLevel] = {
    "display-large": TypoLevel(7, 400, 1.1, True),
    "display-medium": TypoLevel(6, 400, 1.1, True),
    "display-small": TypoLevel(5, 400, 1.1, True),
    "headline-large": TypoLevel(4, 400, 1.2, True),
    "headline-medium": TypoLevel(3, 400, 1.2, True),
    "headline-small": TypoLevel(2, 400, 1.2, True),
    "title-large": TypoLevel(1, 500, 1.2, True),
    "title-medium": TypoLevel(0, 500, 1.2, True),
    "title-small": TypoLevel(-1, 500, 1.2, True),
    "body-large": TypoLevel(0, 400, 1.5, False),
    "body-medium": TypoLevel(-1, 400, 1.5, False),
    "body-small": TypoLevel(-2, 400, 1.5, False),
    "label-large": TypoLevel(-1, 500, 1.4, False),
    "label-medium": TypoLevel(-2, 500, 1.4, False),
    "label-small": TypoLevel(-3, 500, 1.4, False),
}


# Canonical component tokens. Each component references foundation tokens via
# DESIGN.md's `{path.to.token}` reference syntax — the agent or downstream
# tooling can resolve them. This set is intentionally small but covers the
# most-used interactive surfaces. The skill prose explains how to extend.
#
# Interactive-state convention follows Material 3:
#   - hover/pressed apply a state layer (a translucent overlay of a tinting
#     color) on top of the base background — emitted as `stateLayer` (color
#     reference) + `stateLayerOpacity` (percentage). M3 spec: hover = 8%,
#     pressed = 10%, focus = 10%, dragged = 16%. Downstream consumers
#     composite state-layer color over the base.
#   - disabled drops `backgroundOpacity` to 12% and `textOpacity` to 38% on
#     `onSurface`, the M3-standard "out of play" appearance.
#   - inputs grow an `outlineColor` + `outlineWidth` on focus and error,
#     matching the bottom-line / full-outline focus indicators in M3.
#
# These extra properties are non-normative per the DESIGN.md spec ("Unknown
# component property" → accept with warning) but match M3 conventions so any
# M3-aware downstream tool can apply them.
def build_component_tokens() -> dict[str, dict[str, str]]:
    return {
        "button-primary": {
            "backgroundColor": "{colors.primary}",
            "textColor": "{colors.onPrimary}",
            "typography": "{typography.label-large}",
            "rounded": "{rounded.full}",
            "padding": "{spacing.md}",
            "height": "40px",
        },
        "button-primary-hover": {
            "backgroundColor": "{colors.primary}",
            "textColor": "{colors.onPrimary}",
            "stateLayer": "{colors.onPrimary}",
            "stateLayerOpacity": "8%",
        },
        "button-primary-pressed": {
            "backgroundColor": "{colors.primary}",
            "textColor": "{colors.onPrimary}",
            "stateLayer": "{colors.onPrimary}",
            "stateLayerOpacity": "10%",
        },
        "button-primary-disabled": {
            "backgroundColor": "{colors.onSurface}",
            "backgroundOpacity": "12%",
            "textColor": "{colors.onSurface}",
            "textOpacity": "38%",
        },
        "button-secondary": {
            "backgroundColor": "{colors.secondaryContainer}",
            "textColor": "{colors.onSecondaryContainer}",
            "typography": "{typography.label-large}",
            "rounded": "{rounded.full}",
            "padding": "{spacing.md}",
            "height": "40px",
        },
        "button-secondary-hover": {
            "backgroundColor": "{colors.secondaryContainer}",
            "textColor": "{colors.onSecondaryContainer}",
            "stateLayer": "{colors.onSecondaryContainer}",
            "stateLayerOpacity": "8%",
        },
        "button-text": {
            "backgroundColor": "transparent",
            "textColor": "{colors.primary}",
            "typography": "{typography.label-large}",
            "rounded": "{rounded.full}",
            "padding": "{spacing.sm}",
            "height": "40px",
        },
        "button-text-hover": {
            "backgroundColor": "transparent",
            "textColor": "{colors.primary}",
            "stateLayer": "{colors.primary}",
            "stateLayerOpacity": "8%",
        },
        "input-field": {
            "backgroundColor": "{colors.surfaceContainerHighest}",
            "textColor": "{colors.onSurface}",
            "typography": "{typography.body-large}",
            "rounded": "{rounded.xs}",
            "padding": "{spacing.md}",
            "height": "56px",
            "outlineColor": "{colors.outline}",
            "outlineWidth": "1px",
        },
        "input-field-focused": {
            "backgroundColor": "{colors.surfaceContainerHighest}",
            "textColor": "{colors.onSurface}",
            "outlineColor": "{colors.primary}",
            "outlineWidth": "2px",
        },
        "input-field-error": {
            "backgroundColor": "{colors.surfaceContainerHighest}",
            "textColor": "{colors.error}",
            "outlineColor": "{colors.error}",
            "outlineWidth": "2px",
        },
        "input-field-disabled": {
            "backgroundColor": "{colors.onSurface}",
            "backgroundOpacity": "4%",
            "textColor": "{colors.onSurface}",
            "textOpacity": "38%",
            "outlineColor": "{colors.onSurface}",
            "outlineOpacity": "12%",
            "outlineWidth": "1px",
        },
        "card": {
            "backgroundColor": "{colors.surfaceContainerLow}",
            "textColor": "{colors.onSurface}",
            "rounded": "{rounded.md}",
            "padding": "{spacing.md}",
        },
        "chip": {
            "backgroundColor": "{colors.surfaceContainerLow}",
            "textColor": "{colors.onSurfaceVariant}",
            "typography": "{typography.label-large}",
            "rounded": "{rounded.sm}",
            "padding": "{spacing.sm}",
            "height": "32px",
        },
        "chip-selected": {
            "backgroundColor": "{colors.secondaryContainer}",
            "textColor": "{colors.onSecondaryContainer}",
        },
        "tooltip": {
            "backgroundColor": "{colors.inverseSurface}",
            "textColor": "{colors.inverseOnSurface}",
            "typography": "{typography.body-small}",
            "rounded": "{rounded.xs}",
            "padding": "{spacing.sm}",
        },
    }


# ---------------------------------------------------------------------------
# Color helpers
# ---------------------------------------------------------------------------


def hex_to_argb(value: str) -> int:
    """Parse '#RRGGBB' (or 'RRGGBB') to an ARGB int with full alpha."""
    cleaned = value.strip().lstrip("#")
    if len(cleaned) != 6:
        raise ValueError(
            f"Invalid hex color {value!r}: expected '#RRGGBB' (6 hex digits)."
        )
    try:
        rgb = int(cleaned, 16)
    except ValueError as exc:
        raise ValueError(f"Invalid hex color {value!r}: {exc}") from exc
    return 0xFF000000 | rgb


def argb_to_hex(argb: int) -> str:
    """Format an ARGB int as a lowercase '#rrggbb' string."""
    return "#{:06x}".format(argb & 0xFFFFFF)


def make_scheme(
    seed_hex: Optional[str],
    primary_hex: Optional[str],
    secondary_hex: Optional[str],
    tertiary_hex: Optional[str],
    is_dark: bool,
) -> DynamicScheme:
    """Build a DynamicScheme either from a seed color or from custom triplet."""
    if seed_hex is not None:
        seed_hct = Hct.from_int(hex_to_argb(seed_hex))
        # spec_version='2021' = the classic M3 spec — matches the Dart reference
        # and is what most M3 design tooling expects. `2025` is the newer
        # expressive spec, which we intentionally don't default to because the
        # mainstream M3 ecosystem hasn't caught up yet.
        return SchemeTonalSpot(seed_hct, is_dark, 0.0, spec_version="2021")

    # Custom triplet — build palettes from each brand color's HCT, then assemble
    # a DynamicScheme. Neutrals use the primary hue with low chroma to preserve
    # a subtle tint of the brand throughout surfaces, mirroring the Dart code.
    p_hct = Hct.from_int(hex_to_argb(primary_hex))
    s_hct = Hct.from_int(hex_to_argb(secondary_hex))
    t_hct = Hct.from_int(hex_to_argb(tertiary_hex))

    return DynamicScheme(
        source_color_hct=p_hct,
        variant=Variant.TONAL_SPOT,
        contrast_level=0.0,
        is_dark=is_dark,
        spec_version="2021",
        primary_palette=TonalPalette.from_hue_and_chroma(p_hct.hue, p_hct.chroma),
        secondary_palette=TonalPalette.from_hue_and_chroma(s_hct.hue, s_hct.chroma),
        tertiary_palette=TonalPalette.from_hue_and_chroma(t_hct.hue, t_hct.chroma),
        neutral_palette=TonalPalette.from_hue_and_chroma(p_hct.hue, 6.0),
        neutral_variant_palette=TonalPalette.from_hue_and_chroma(p_hct.hue, 8.0),
    )


def role_hex(scheme: DynamicScheme, role_name: str) -> str:
    """Resolve an M3 color role on the given scheme to a hex string."""
    role = getattr(MaterialDynamicColors, role_name)
    return argb_to_hex(role.get_argb(scheme))


# ---------------------------------------------------------------------------
# Token assembly
# ---------------------------------------------------------------------------


def format_number(value: float) -> str:
    """Render a number without trailing zeros (16.0 -> '16', 1.25 -> '1.25')."""
    if value == int(value):
        return str(int(value))
    # Two decimals max, strip trailing zeros.
    return f"{value:.2f}".rstrip("0").rstrip(".")


@dataclass
class TokenSet:
    """Pure-data representation of all tokens, suitable for JSON or YAML emit."""

    version: str
    name: str
    description: Optional[str]
    colors: dict[str, str] = field(default_factory=dict)
    typography: dict[str, dict[str, object]] = field(default_factory=dict)
    rounded: dict[str, str] = field(default_factory=dict)
    spacing: dict[str, str] = field(default_factory=dict)
    components: dict[str, dict[str, str]] = field(default_factory=dict)
    palettes: dict[str, dict[int, str]] = field(default_factory=dict)
    opposite_palettes: dict[str, dict[int, str]] = field(default_factory=dict)
    opposite_colors: dict[str, str] = field(default_factory=dict)
    scheme_used: str = "light"


def build_tokens(args: argparse.Namespace) -> TokenSet:
    is_dark = args.scheme.lower() == "dark"
    scheme = make_scheme(
        args.seed, args.primary, args.secondary, args.tertiary, is_dark=is_dark
    )
    opposite = make_scheme(
        args.seed, args.primary, args.secondary, args.tertiary, is_dark=not is_dark
    )

    tokens = TokenSet(
        version=args.version,
        name=args.brand_name,
        description=args.description,
        scheme_used=args.scheme.lower(),
    )

    # Colors — the chosen scheme is what lives in `colors:`.
    for role in COLOR_ROLES:
        tokens.colors[role] = role_hex(scheme, role)

    # Opposite scheme — included only in JSON output, for the agent's prose.
    for role in COLOR_ROLES:
        tokens.opposite_colors[role] = role_hex(opposite, role)

    # Tonal palettes — same for light/dark (palettes are scheme-independent).
    # Useful for the markdown body's Colors section.
    palettes = {
        "primary": scheme.primary_palette,
        "secondary": scheme.secondary_palette,
        "tertiary": scheme.tertiary_palette,
        "neutral": scheme.neutral_palette,
        "neutral-variant": scheme.neutral_variant_palette,
    }
    for name, palette in palettes.items():
        tokens.palettes[name] = {
            tone: argb_to_hex(palette.tone(tone)) for tone in PALETTE_TONES
        }
    # Same palettes for the opposite scheme JSON, for symmetry.
    tokens.opposite_palettes = tokens.palettes

    # Typography — title rows use the titles font, others use the body font.
    for token_name, level in TYPE_SCALE.items():
        size_px = round(args.font_base * (args.type_scale ** level.size_step))
        family = args.title_font if level.is_title else args.body_font
        tokens.typography[token_name] = {
            "fontFamily": family,
            "fontSize": f"{size_px}px",
            "fontWeight": level.weight,
            "lineHeight": format_number(level.line_height),
        }

    # Rounded scale — geometric progression off the `rounder` base.
    # We expose the standard names from the DESIGN.md spec: xs/sm/md/lg/xl/full.
    tokens.rounded = {
        "xs": f"{format_number(args.rounder)}px",
        "sm": f"{format_number(args.rounder * 2)}px",
        "md": f"{format_number(args.rounder * 3)}px",
        "lg": f"{format_number(args.rounder * 4)}px",
        "xl": f"{format_number(args.rounder * 6)}px",
        "full": "9999px",
    }

    # Spacing scale — matches the Dart reference's geometric progression around
    # the `spacer` value, with the M3-recommended base.
    tokens.spacing = {
        "xs": f"{format_number(args.spacer * 0.25)}px",
        "sm": f"{format_number(args.spacer * 0.5)}px",
        "md": f"{format_number(args.spacer)}px",
        "lg": f"{format_number(args.spacer * 1.5)}px",
        "xl": f"{format_number(args.spacer * 3)}px",
    }

    # Components — only emit when requested.
    if args.components:
        tokens.components = build_component_tokens()

    return tokens


# ---------------------------------------------------------------------------
# YAML / JSON emission
# ---------------------------------------------------------------------------


def yaml_escape(value: str) -> str:
    """Quote a string if YAML might misinterpret it. Conservative: quote when
    the value contains a colon, '#', leading/trailing whitespace, or is empty.
    Otherwise emit unquoted for readability."""
    needs_quote = (
        value == ""
        or ":" in value
        or "#" in value
        or value != value.strip()
        or value[0] in ("[", "{", "&", "*", "!", "|", ">", "'", '"', "%", "@", "`")
    )
    if not needs_quote:
        return value
    escaped = value.replace("\\", "\\\\").replace('"', '\\"')
    return f'"{escaped}"'


def emit_yaml(tokens: TokenSet) -> str:
    out: list[str] = ["---"]
    out.append(f"version: {yaml_escape(tokens.version)}")
    out.append(f"name: {yaml_escape(tokens.name)}")
    if tokens.description:
        out.append(f"description: {yaml_escape(tokens.description)}")

    out.append("colors:")
    for k, v in tokens.colors.items():
        out.append(f'  {k}: "{v}"')

    out.append("typography:")
    for token_name, props in tokens.typography.items():
        out.append(f"  {token_name}:")
        # Preserve insertion order: fontFamily, fontSize, fontWeight, lineHeight
        out.append(f"    fontFamily: {yaml_escape(str(props['fontFamily']))}")
        out.append(f"    fontSize: {props['fontSize']}")
        out.append(f"    fontWeight: {props['fontWeight']}")
        out.append(f"    lineHeight: {props['lineHeight']}")

    out.append("rounded:")
    for k, v in tokens.rounded.items():
        out.append(f"  {k}: {v}")

    out.append("spacing:")
    for k, v in tokens.spacing.items():
        out.append(f"  {k}: {v}")

    if tokens.components:
        out.append("components:")
        for comp, props in tokens.components.items():
            out.append(f"  {comp}:")
            for prop, val in props.items():
                # token references contain '{', which is a YAML flow indicator,
                # so always quote.
                out.append(f'    {prop}: "{val}"')

    out.append("---")
    return "\n".join(out) + "\n"


def emit_json(tokens: TokenSet) -> str:
    payload = {
        "version": tokens.version,
        "name": tokens.name,
        "description": tokens.description,
        "scheme_used": tokens.scheme_used,
        "colors": tokens.colors,
        "typography": tokens.typography,
        "rounded": tokens.rounded,
        "spacing": tokens.spacing,
        "components": tokens.components,
        "palettes": tokens.palettes,
        "opposite_scheme": {
            "scheme": "dark" if tokens.scheme_used == "light" else "light",
            "colors": tokens.opposite_colors,
        },
    }
    return json.dumps(payload, indent=2, ensure_ascii=False) + "\n"


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


def parse_args(argv: Optional[list[str]] = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Generate Material Design 3 design tokens for a DESIGN.md "
            "YAML frontmatter block."
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    # Brand
    parser.add_argument("--brand-name", required=True, help="Brand or project name.")
    parser.add_argument(
        "--description",
        default=None,
        help="Optional one-line description (e.g. the General Style phrase).",
    )
    parser.add_argument(
        "--version",
        default="alpha",
        help="DESIGN.md schema version label. Default: alpha.",
    )

    # Colors — either seed OR triplet.
    color_group = parser.add_argument_group(
        "color input (choose one mode)",
        "Provide --seed for single-color M3 derivation, OR all three of "
        "--primary --secondary --tertiary to bring your own palette.",
    )
    color_group.add_argument("--seed", help='Seed color, e.g. "#38693c"')
    color_group.add_argument("--primary", help='Primary brand color, e.g. "#38693c"')
    color_group.add_argument("--secondary", help='Secondary brand color')
    color_group.add_argument("--tertiary", help='Tertiary brand color')

    parser.add_argument(
        "--scheme",
        choices=["light", "dark"],
        default="light",
        help="Main color scheme. Default: light.",
    )

    # Typography
    parser.add_argument("--title-font", required=True, help="Font family for titles.")
    parser.add_argument("--body-font", required=True, help="Font family for body.")
    parser.add_argument(
        "--font-base",
        type=float,
        default=16.0,
        help="Body-large base font size in px. Default: 16.",
    )
    parser.add_argument(
        "--type-scale",
        type=float,
        default=1.2,
        help="Geometric ratio between type scale steps. Default: 1.2.",
    )

    # Spacing & shape
    parser.add_argument(
        "--spacer",
        type=float,
        default=16.0,
        help="Base spacing unit in px (drives xs..xl). Default: 16.",
    )
    parser.add_argument(
        "--rounder",
        type=float,
        default=4.0,
        help="Base corner-radius unit in px. Default: 4.",
    )

    # Output
    parser.add_argument(
        "--json",
        action="store_true",
        help="Emit a JSON payload (tokens + palettes) instead of YAML.",
    )
    parser.add_argument(
        "--no-components",
        dest="components",
        action="store_false",
        help="Skip the `components:` block in the YAML output.",
    )
    parser.set_defaults(components=True)
    parser.add_argument(
        "--output",
        "-o",
        help="Write to this file instead of stdout.",
    )

    args = parser.parse_args(argv)

    # Validate color input.
    triplet = [args.primary, args.secondary, args.tertiary]
    triplet_present = [x is not None for x in triplet]
    if args.seed and any(triplet_present):
        parser.error(
            "Use either --seed OR --primary/--secondary/--tertiary, not both."
        )
    if not args.seed and not all(triplet_present):
        parser.error(
            "Color input required: provide --seed, OR all three of "
            "--primary --secondary --tertiary."
        )

    # Quick hex sanity check.
    for label, value in [
        ("--seed", args.seed),
        ("--primary", args.primary),
        ("--secondary", args.secondary),
        ("--tertiary", args.tertiary),
    ]:
        if value is not None:
            try:
                hex_to_argb(value)
            except ValueError as exc:
                parser.error(f"{label}: {exc}")

    if args.font_base <= 0:
        parser.error("--font-base must be positive.")
    if args.type_scale <= 1.0:
        parser.error("--type-scale must be greater than 1.")
    if args.spacer <= 0:
        parser.error("--spacer must be positive.")
    if args.rounder < 0:
        parser.error("--rounder must be non-negative.")

    return args


def main(argv: Optional[list[str]] = None) -> int:
    args = parse_args(argv)
    tokens = build_tokens(args)
    output = emit_json(tokens) if args.json else emit_yaml(tokens)
    if args.output:
        with open(args.output, "w", encoding="utf-8") as fh:
            fh.write(output)
    else:
        sys.stdout.write(output)
    return 0


if __name__ == "__main__":
    sys.exit(main())
