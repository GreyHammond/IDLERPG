# Changelog

All notable changes to I.D.L.E.R.P.G. will be documented in this file.

## [Unreleased]

### Added
- **Grammar-Based Item Naming System** - Items now build names dynamically based on power level:
  - Power 1-9: `[Base]` → "Dagger"
  - Power 10-19: `[Prefix] [Base]` → "Polished Dagger"
  - Power 20-34: `[Prefix] [Material] [Base]` → "Polished Steel Dagger"
  - Power 35-49: `[Quality] [Material] [Base] [Suffix]` → "Vorpal Steel Dagger of Whispers"
  - Power 50+: `[Title], the [Quality] [Material] [Base] [Suffix]` → "The Harbinger, the Vorpal Steel Dagger of Whispers"

- **5 New Tiered Name Pools:**
  - `LOW_TIER_PREFIX` - Physical conditions (Rusty, Polished, Weighted...)
  - `MID_TIER_MATERIAL` - Substances (Steel, Mithril, Adamantite...)
  - `HIGH_TIER_SUFFIX` - "of X" phrases (of Whispers, of the Void...)
  - `QUALITY_TIER` - Legendary descriptors (Vorpal, Ruinous, Exalted...)
  - `LEGENDARY_TITLES` - Unique names (The Harbinger, Doomgiver...)

- **Act Display Fix** - Added `get_act_name()` helper to safely handle Act 21+ displaying "Restarting the Universe" instead of crashing

### Confirmed Formulas
- `power = level + random(0, 1)`
- `bonus = 1 + (level // 3)`
