# Changelog

All notable changes to I.D.L.E.R.P.G. will be documented in this file.

## v1.2 - Ascension

### Added
- **Expanded Act System** - Now supports 100 acts per cycle:
  - Acts 1-98: Regular questing with 98 unique narrative act names
  - Act 99: "The Final Battle" - harder boss (25 fights, 6 loot)
  - Act 100: "Resetting the Universe" - resets gold, inventory, equipment
  - Acts 101+: Continues with Roman numeral cycles (II, III, IV...)

- **Roman Numeral Support** - `to_roman()` function for cycle numbering

- **Universe Reset** - `_reset_universe()` method:
  - Keeps: Level, XP, spells
  - Resets: Gold, Inventory, Equipment, Quests completed, Act progress

### Changed
- **get_act_name()** - Updated to handle 99/100/101+ acts with proper naming:
  - Act 99: "The Final Battle"
  - Act 100: "Resetting the Universe"
  - Act 101+: Uses Roman numerals (The Beginning II, etc.)

- **Boss Quest Cycling** - Bosses now cycle through BOSS_QUESTS for acts 1-98

---

## v1.1 - Age of Artifacts

=======
>>>>>>> f3e15f7ce97354eefc5fcc548d60211b29ca4436
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
