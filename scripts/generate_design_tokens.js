#!/usr/bin/env node
/*
 * Generate Material Design 3 design tokens for a DESIGN.md file.
 *
 * This is the Node.js counterpart to `generate_design_tokens.py` — they share
 * a CLI, output format, and produce byte-identical YAML / JSON for the same
 * inputs. See the Python script's docstring for the full design rationale.
 *
 * Two color-input modes (mutually exclusive):
 *   --seed "#38693c"
 *   --primary "#38693c" --secondary "#6c5e10" --tertiary "#4c5c92"
 *
 * Dependency:
 *   npm install @material/material-color-utilities@0.2.7
 *
 * (Note: newer 0.3.x has ESM-resolution quirks in plain Node; 0.2.7 is the
 * canonical M3 spec — what Material 3 design tooling expects.)
 */

'use strict';

const fs = require('fs');
const path = require('path');

let mcu;
try {
  mcu = require('@material/material-color-utilities');
} catch (err) {
  process.stderr.write(
    "Missing dependency '@material/material-color-utilities'. Install with:\n" +
    '  npm install @material/material-color-utilities@0.2.7\n' +
    `Original error: ${err.message}\n`,
  );
  process.exit(2);
}

const {
  Hct,
  SchemeTonalSpot,
  MaterialDynamicColors,
  DynamicScheme,
  TonalPalette,
  argbFromHex,
} = mcu;

// Variant.TONAL_SPOT — numeric value (see Variant enum in package source). We
// hardcode the integer rather than importing because v0.2.7 of the package
// doesn't expose the Variant enum from its main exports map. Value taken from
// the package's `variant.d.ts`.
const VARIANT_TONAL_SPOT = 2;

// ---------------------------------------------------------------------------
// Configuration mirrors the Python module exactly so outputs match.
// ---------------------------------------------------------------------------

const COLOR_ROLES = [
  'primary', 'surfaceTint', 'onPrimary', 'primaryContainer', 'onPrimaryContainer',
  'secondary', 'onSecondary', 'secondaryContainer', 'onSecondaryContainer',
  'tertiary', 'onTertiary', 'tertiaryContainer', 'onTertiaryContainer',
  'error', 'onError', 'errorContainer', 'onErrorContainer',
  'background', 'onBackground', 'surface', 'onSurface',
  'surfaceVariant', 'onSurfaceVariant', 'outline', 'outlineVariant',
  'shadow', 'scrim', 'inverseSurface', 'inverseOnSurface', 'inversePrimary',
  'primaryFixed', 'onPrimaryFixed', 'primaryFixedDim', 'onPrimaryFixedVariant',
  'secondaryFixed', 'onSecondaryFixed', 'secondaryFixedDim', 'onSecondaryFixedVariant',
  'tertiaryFixed', 'onTertiaryFixed', 'tertiaryFixedDim', 'onTertiaryFixedVariant',
  'surfaceDim', 'surfaceBright',
  'surfaceContainerLowest', 'surfaceContainerLow', 'surfaceContainer',
  'surfaceContainerHigh', 'surfaceContainerHighest',
];

const PALETTE_TONES = [0, 5, 10, 15, 20, 25, 30, 35, 40, 50, 60, 70, 80, 90, 95, 98, 99, 100];

// [size_step, weight, line_height, is_title]
const TYPE_SCALE = {
  'display-large': [7, 400, 1.1, true],
  'display-medium': [6, 400, 1.1, true],
  'display-small': [5, 400, 1.1, true],
  'headline-large': [4, 400, 1.2, true],
  'headline-medium': [3, 400, 1.2, true],
  'headline-small': [2, 400, 1.2, true],
  'title-large': [1, 500, 1.2, true],
  'title-medium': [0, 500, 1.2, true],
  'title-small': [-1, 500, 1.2, true],
  'body-large': [0, 400, 1.5, false],
  'body-medium': [-1, 400, 1.5, false],
  'body-small': [-2, 400, 1.5, false],
  'label-large': [-1, 500, 1.4, false],
  'label-medium': [-2, 500, 1.4, false],
  'label-small': [-3, 500, 1.4, false],
};

// Interactive-state convention follows Material 3:
//   - hover/pressed apply a state layer (translucent overlay color) over the
//     base background — emitted as `stateLayer` + `stateLayerOpacity` (%).
//     M3: hover = 8%, pressed = 10%, focus = 10%, dragged = 16%.
//   - disabled uses `backgroundOpacity: 12%` and `textOpacity: 38%` on
//     `onSurface`, the M3-standard "out of play" appearance.
//   - inputs add `outlineColor` + `outlineWidth` that vary across states.
//
// These extra properties are non-normative per the DESIGN.md spec (unknown
// component properties are accepted with warning) but match M3 conventions
// so any M3-aware downstream tool can apply them.
function buildComponentTokens() {
  return {
    'button-primary': {
      backgroundColor: '{colors.primary}',
      textColor: '{colors.onPrimary}',
      typography: '{typography.label-large}',
      rounded: '{rounded.full}',
      padding: '{spacing.md}',
      height: '40px',
    },
    'button-primary-hover': {
      backgroundColor: '{colors.primary}',
      textColor: '{colors.onPrimary}',
      stateLayer: '{colors.onPrimary}',
      stateLayerOpacity: '8%',
    },
    'button-primary-pressed': {
      backgroundColor: '{colors.primary}',
      textColor: '{colors.onPrimary}',
      stateLayer: '{colors.onPrimary}',
      stateLayerOpacity: '10%',
    },
    'button-primary-disabled': {
      backgroundColor: '{colors.onSurface}',
      backgroundOpacity: '12%',
      textColor: '{colors.onSurface}',
      textOpacity: '38%',
    },
    'button-secondary': {
      backgroundColor: '{colors.secondaryContainer}',
      textColor: '{colors.onSecondaryContainer}',
      typography: '{typography.label-large}',
      rounded: '{rounded.full}',
      padding: '{spacing.md}',
      height: '40px',
    },
    'button-secondary-hover': {
      backgroundColor: '{colors.secondaryContainer}',
      textColor: '{colors.onSecondaryContainer}',
      stateLayer: '{colors.onSecondaryContainer}',
      stateLayerOpacity: '8%',
    },
    'button-text': {
      backgroundColor: 'transparent',
      textColor: '{colors.primary}',
      typography: '{typography.label-large}',
      rounded: '{rounded.full}',
      padding: '{spacing.sm}',
      height: '40px',
    },
    'button-text-hover': {
      backgroundColor: 'transparent',
      textColor: '{colors.primary}',
      stateLayer: '{colors.primary}',
      stateLayerOpacity: '8%',
    },
    'input-field': {
      backgroundColor: '{colors.surfaceContainerHighest}',
      textColor: '{colors.onSurface}',
      typography: '{typography.body-large}',
      rounded: '{rounded.xs}',
      padding: '{spacing.md}',
      height: '56px',
      outlineColor: '{colors.outline}',
      outlineWidth: '1px',
    },
    'input-field-focused': {
      backgroundColor: '{colors.surfaceContainerHighest}',
      textColor: '{colors.onSurface}',
      outlineColor: '{colors.primary}',
      outlineWidth: '2px',
    },
    'input-field-error': {
      backgroundColor: '{colors.surfaceContainerHighest}',
      textColor: '{colors.error}',
      outlineColor: '{colors.error}',
      outlineWidth: '2px',
    },
    'input-field-disabled': {
      backgroundColor: '{colors.onSurface}',
      backgroundOpacity: '4%',
      textColor: '{colors.onSurface}',
      textOpacity: '38%',
      outlineColor: '{colors.onSurface}',
      outlineOpacity: '12%',
      outlineWidth: '1px',
    },
    card: {
      backgroundColor: '{colors.surfaceContainerLow}',
      textColor: '{colors.onSurface}',
      rounded: '{rounded.md}',
      padding: '{spacing.md}',
    },
    chip: {
      backgroundColor: '{colors.surfaceContainerLow}',
      textColor: '{colors.onSurfaceVariant}',
      typography: '{typography.label-large}',
      rounded: '{rounded.sm}',
      padding: '{spacing.sm}',
      height: '32px',
    },
    'chip-selected': {
      backgroundColor: '{colors.secondaryContainer}',
      textColor: '{colors.onSecondaryContainer}',
    },
    tooltip: {
      backgroundColor: '{colors.inverseSurface}',
      textColor: '{colors.inverseOnSurface}',
      typography: '{typography.body-small}',
      rounded: '{rounded.xs}',
      padding: '{spacing.sm}',
    },
  };
}

// ---------------------------------------------------------------------------
// Color helpers
// ---------------------------------------------------------------------------

function argbToHex(argb) {
  // Strip alpha; emit lowercase 6-digit hex.
  return '#' + (argb & 0xFFFFFF).toString(16).padStart(6, '0');
}

function validateHex(value, label) {
  const cleaned = String(value).trim().replace(/^#/, '');
  if (!/^[0-9a-fA-F]{6}$/.test(cleaned)) {
    throw new Error(`${label}: expected '#RRGGBB' (6 hex digits), got ${JSON.stringify(value)}`);
  }
  return '#' + cleaned;
}

function makeScheme({ seed, primary, secondary, tertiary, isDark }) {
  if (seed) {
    const hct = Hct.fromInt(argbFromHex(seed));
    return new SchemeTonalSpot(hct, isDark, 0);
  }
  const pHct = Hct.fromInt(argbFromHex(primary));
  const sHct = Hct.fromInt(argbFromHex(secondary));
  const tHct = Hct.fromInt(argbFromHex(tertiary));
  return new DynamicScheme({
    sourceColorArgb: pHct.toInt(),
    variant: VARIANT_TONAL_SPOT,
    contrastLevel: 0,
    isDark,
    primaryPalette: TonalPalette.fromHueAndChroma(pHct.hue, pHct.chroma),
    secondaryPalette: TonalPalette.fromHueAndChroma(sHct.hue, sHct.chroma),
    tertiaryPalette: TonalPalette.fromHueAndChroma(tHct.hue, tHct.chroma),
    neutralPalette: TonalPalette.fromHueAndChroma(pHct.hue, 6),
    neutralVariantPalette: TonalPalette.fromHueAndChroma(pHct.hue, 8),
  });
}

function roleHex(scheme, role) {
  return argbToHex(MaterialDynamicColors[role].getArgb(scheme));
}

// ---------------------------------------------------------------------------
// Token assembly
// ---------------------------------------------------------------------------

function formatNumber(value) {
  if (value === Math.trunc(value)) return String(Math.trunc(value));
  return value.toFixed(2).replace(/0+$/, '').replace(/\.$/, '');
}

function buildTokens(opts) {
  const isDark = opts.scheme === 'dark';
  const scheme = makeScheme({ ...opts, isDark });
  const opposite = makeScheme({ ...opts, isDark: !isDark });

  const tokens = {
    version: opts.version,
    name: opts.brandName,
    description: opts.description || null,
    schemeUsed: opts.scheme,
    colors: {},
    typography: {},
    rounded: {},
    spacing: {},
    components: {},
    palettes: {},
    oppositeColors: {},
  };

  for (const role of COLOR_ROLES) {
    tokens.colors[role] = roleHex(scheme, role);
    tokens.oppositeColors[role] = roleHex(opposite, role);
  }

  const palettes = {
    primary: scheme.primaryPalette,
    secondary: scheme.secondaryPalette,
    tertiary: scheme.tertiaryPalette,
    neutral: scheme.neutralPalette,
    'neutral-variant': scheme.neutralVariantPalette,
  };
  for (const [name, palette] of Object.entries(palettes)) {
    tokens.palettes[name] = {};
    for (const tone of PALETTE_TONES) {
      tokens.palettes[name][tone] = argbToHex(palette.tone(tone));
    }
  }

  for (const [tokenName, [step, weight, lineHeight, isTitle]] of Object.entries(TYPE_SCALE)) {
    const sizePx = Math.round(opts.fontBase * Math.pow(opts.typeScale, step));
    const family = isTitle ? opts.titleFont : opts.bodyFont;
    tokens.typography[tokenName] = {
      fontFamily: family,
      fontSize: `${sizePx}px`,
      fontWeight: weight,
      lineHeight: formatNumber(lineHeight),
    };
  }

  tokens.rounded = {
    xs: `${formatNumber(opts.rounder)}px`,
    sm: `${formatNumber(opts.rounder * 2)}px`,
    md: `${formatNumber(opts.rounder * 3)}px`,
    lg: `${formatNumber(opts.rounder * 4)}px`,
    xl: `${formatNumber(opts.rounder * 6)}px`,
    full: '9999px',
  };

  tokens.spacing = {
    xs: `${formatNumber(opts.spacer * 0.25)}px`,
    sm: `${formatNumber(opts.spacer * 0.5)}px`,
    md: `${formatNumber(opts.spacer)}px`,
    lg: `${formatNumber(opts.spacer * 1.5)}px`,
    xl: `${formatNumber(opts.spacer * 3)}px`,
  };

  if (opts.components) {
    tokens.components = buildComponentTokens();
  }

  return tokens;
}

// ---------------------------------------------------------------------------
// YAML / JSON emission — must match Python output exactly for the same inputs.
// ---------------------------------------------------------------------------

function yamlEscape(value) {
  const v = String(value);
  const needsQuote = (
    v === '' ||
    v.includes(':') ||
    v.includes('#') ||
    v !== v.trim() ||
    '[{&*!|>\'"%@`'.includes(v[0] || '')
  );
  if (!needsQuote) return v;
  return '"' + v.replace(/\\/g, '\\\\').replace(/"/g, '\\"') + '"';
}

function emitYaml(tokens) {
  const out = ['---'];
  out.push(`version: ${yamlEscape(tokens.version)}`);
  out.push(`name: ${yamlEscape(tokens.name)}`);
  if (tokens.description) {
    out.push(`description: ${yamlEscape(tokens.description)}`);
  }

  out.push('colors:');
  for (const [k, v] of Object.entries(tokens.colors)) {
    out.push(`  ${k}: "${v}"`);
  }

  out.push('typography:');
  for (const [name, props] of Object.entries(tokens.typography)) {
    out.push(`  ${name}:`);
    out.push(`    fontFamily: ${yamlEscape(props.fontFamily)}`);
    out.push(`    fontSize: ${props.fontSize}`);
    out.push(`    fontWeight: ${props.fontWeight}`);
    out.push(`    lineHeight: ${props.lineHeight}`);
  }

  out.push('rounded:');
  for (const [k, v] of Object.entries(tokens.rounded)) {
    out.push(`  ${k}: ${v}`);
  }

  out.push('spacing:');
  for (const [k, v] of Object.entries(tokens.spacing)) {
    out.push(`  ${k}: ${v}`);
  }

  if (Object.keys(tokens.components).length > 0) {
    out.push('components:');
    for (const [comp, props] of Object.entries(tokens.components)) {
      out.push(`  ${comp}:`);
      for (const [prop, val] of Object.entries(props)) {
        out.push(`    ${prop}: "${val}"`);
      }
    }
  }

  out.push('---');
  return out.join('\n') + '\n';
}

function emitJson(tokens) {
  const payload = {
    version: tokens.version,
    name: tokens.name,
    description: tokens.description,
    scheme_used: tokens.schemeUsed,
    colors: tokens.colors,
    typography: tokens.typography,
    rounded: tokens.rounded,
    spacing: tokens.spacing,
    components: tokens.components,
    palettes: tokens.palettes,
    opposite_scheme: {
      scheme: tokens.schemeUsed === 'light' ? 'dark' : 'light',
      colors: tokens.oppositeColors,
    },
  };
  return JSON.stringify(payload, null, 2) + '\n';
}

// ---------------------------------------------------------------------------
// CLI
// ---------------------------------------------------------------------------

function parseArgs(argv) {
  // Minimal hand-rolled flag parser — `--flag value` and `--flag=value`.
  // Booleans: `--json`, `--no-components`.
  const opts = {
    brandName: null,
    description: null,
    version: 'alpha',
    seed: null,
    primary: null,
    secondary: null,
    tertiary: null,
    scheme: 'light',
    titleFont: null,
    bodyFont: null,
    fontBase: 16,
    typeScale: 1.2,
    spacer: 16,
    rounder: 4,
    json: false,
    components: true,
    output: null,
    help: false,
  };

  const aliases = {
    '--brand-name': 'brandName',
    '--description': 'description',
    '--version': 'version',
    '--seed': 'seed',
    '--primary': 'primary',
    '--secondary': 'secondary',
    '--tertiary': 'tertiary',
    '--scheme': 'scheme',
    '--title-font': 'titleFont',
    '--body-font': 'bodyFont',
    '--font-base': 'fontBase',
    '--type-scale': 'typeScale',
    '--spacer': 'spacer',
    '--rounder': 'rounder',
    '--output': 'output',
    '-o': 'output',
  };
  const numericKeys = new Set(['fontBase', 'typeScale', 'spacer', 'rounder']);

  for (let i = 0; i < argv.length; i++) {
    const raw = argv[i];
    if (raw === '--help' || raw === '-h') { opts.help = true; continue; }
    if (raw === '--json') { opts.json = true; continue; }
    if (raw === '--no-components') { opts.components = false; continue; }

    let key = raw, value;
    if (raw.includes('=')) {
      const eq = raw.indexOf('=');
      key = raw.slice(0, eq);
      value = raw.slice(eq + 1);
    } else {
      value = argv[++i];
    }

    if (!(key in aliases)) {
      throw new Error(`Unknown flag: ${raw}`);
    }
    const dest = aliases[key];
    if (numericKeys.has(dest)) {
      const num = Number(value);
      if (!Number.isFinite(num)) throw new Error(`${key} expects a number, got ${value}`);
      opts[dest] = num;
    } else {
      opts[dest] = value;
    }
  }

  if (opts.help) return opts;

  // Required.
  if (!opts.brandName) throw new Error('Missing required --brand-name');
  if (!opts.titleFont) throw new Error('Missing required --title-font');
  if (!opts.bodyFont) throw new Error('Missing required --body-font');

  // Color mode.
  const triplet = [opts.primary, opts.secondary, opts.tertiary];
  const tripletPresent = triplet.map(x => x != null);
  if (opts.seed && tripletPresent.some(Boolean)) {
    throw new Error('Use either --seed OR --primary/--secondary/--tertiary, not both.');
  }
  if (!opts.seed && !tripletPresent.every(Boolean)) {
    throw new Error('Color input required: provide --seed, OR all three of --primary --secondary --tertiary.');
  }

  // Hex sanity.
  for (const [label, val] of [['--seed', opts.seed], ['--primary', opts.primary],
    ['--secondary', opts.secondary], ['--tertiary', opts.tertiary]]) {
    if (val != null) validateHex(val, label);
  }

  // Scheme.
  if (!['light', 'dark'].includes(opts.scheme)) {
    throw new Error(`--scheme must be 'light' or 'dark', got ${opts.scheme}`);
  }

  if (opts.fontBase <= 0) throw new Error('--font-base must be positive.');
  if (opts.typeScale <= 1) throw new Error('--type-scale must be greater than 1.');
  if (opts.spacer <= 0) throw new Error('--spacer must be positive.');
  if (opts.rounder < 0) throw new Error('--rounder must be non-negative.');

  return opts;
}

function printHelp() {
  process.stdout.write(`Usage: node generate_design_tokens.js [options]

Required:
  --brand-name TEXT          Brand or project name.
  --title-font TEXT          Font family for titles.
  --body-font TEXT           Font family for body text.
  --seed "#RRGGBB"           OR provide all three of:
  --primary, --secondary, --tertiary  (custom palette mode)

Optional:
  --description TEXT         One-line description (the General Style phrase).
  --version TEXT             DESIGN.md schema version label (default: alpha).
  --scheme light|dark        Main color scheme (default: light).
  --font-base NUMBER         Body base size in px (default: 16).
  --type-scale NUMBER        Geometric ratio between type steps (default: 1.2).
  --spacer NUMBER            Base spacing unit in px (default: 16).
  --rounder NUMBER           Base corner radius in px (default: 4).
  --json                     Emit JSON (tokens + palettes) instead of YAML.
  --no-components            Skip the components: block.
  --output, -o FILE          Write to FILE instead of stdout.
  -h, --help                 Show this help.
`);
}

function main(argv) {
  let opts;
  try {
    opts = parseArgs(argv);
  } catch (err) {
    process.stderr.write(`Error: ${err.message}\n\n`);
    printHelp();
    return 2;
  }
  if (opts.help) { printHelp(); return 0; }

  const tokens = buildTokens(opts);
  const output = opts.json ? emitJson(tokens) : emitYaml(tokens);
  if (opts.output) {
    fs.writeFileSync(opts.output, output, 'utf8');
  } else {
    process.stdout.write(output);
  }
  return 0;
}

if (require.main === module) {
  process.exit(main(process.argv.slice(2)));
}

module.exports = { buildTokens, emitYaml, emitJson, parseArgs };
