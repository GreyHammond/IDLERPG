# I.D.L.E.R.P.G. — Complete Edition (v1.4 — Age of Magic)

A lightweight, feature-rich Idle RPG built with Python and Tkinter. This edition introduces a full spell and skill system — 56 spells across 7 stat affinities, active MP usage, in-field transmutation, Tier III arcane crafting, and 31 new achievements — on top of the complete feature set from prior versions.

## Features

* **Character Customization** — Choose from 20 races and 20 classes with unique stat modifiers. Roll your own stats using the classic 4d6 drop-lowest method, or let the game generate a random name for you.
* **Persistent Progress** — Full save/load functionality means your hero's journey continues exactly where you left off.
* **Dynamic Gameplay** — Colored progress bars, dice-rolling mechanics, and multi-stage quests keep gameplay engaging.
* **Grammar-Based Loot** — Dynamic item naming that builds legendary names as power increases: "Rusty Dagger" → "Polished Steel Dagger" → "The Harbinger, the Vorpal Steel Dagger of Whispers".
* **Loot & Economy** — Manage an inventory with per-item selling, equipment upgrades, and multiple equipment slots.
* **Spell & Skill System** *(v1.4)* — 56 spells across 7 stat affinities (I, P, D, E, R, L, G) and 4 tiers (Minor → Major → II → III). Spells are learned every 5 levels. Each spell has MP cost, duration, effect type, magnitude, and a description shown on mouse-over tooltip. Classes cast spells that match their affinities — fighters don't spam arcane bolts.
* **Active MP Usage** *(v1.4)* — Spells consume MP on cast. The MP bar flashes bright on each cast. Regen spells restore MP over time. A 25% MP floor prevents spells from draining the character dry.
* **10 Effect Categories** *(v1.4)* — XP boost, gold boost, stat buff, HP regen, MP regen, combat damage, combat defense, loot quality, transmutation, and Tier III arcane crafting.
* **Smart Cast Logic** *(v1.4)* — Spells fire at appropriate action boundaries only (e.g. combat spells in fights, regen during rest). Priority queue: heal first if low HP, restore MP if low, then maintain buffs. No-recast guard prevents stacking the same buff.
* **In-Field Transmutation** *(v1.4)* — Characters with transmute spells can convert inventory items to gold in the field instead of returning to market. Efficiency scales logarithmically with Intelligence and spell tier, hard-capped at 92% of market value (convenience always costs something).
* **Tier III Arcane Crafting** *(v1.4)* — Reality Collapse, God-Hand Roll, and similar Tier III spells reforge a weak inventory item into a superior Arcane-Forged version at level+2 power, with auto-equip if better.
* **[ACTIVE Nt] Spell List** *(v1.4)* — Running effects show a live countdown in the spell list. Mouse over any spell for a full tooltip: tier, MP cost, duration, effect type, and description.
* **Spell Preview on Character Creation** *(v1.4)* — Selecting a class shows the first spells that class will learn, so players aren't picking blind.
* **Death & Respawn** — Face consequence with a full death sequence, ghost mechanics, and respawn system. Death clears all active spell effects and reverts any stat buffs cleanly.
* **Infinite Adventure** — 100 acts per cycle. Act 99 is "The Final Battle", Act 100 resets the universe. Repeats infinitely with prestige titles.
* **Encumbered Return / Transmute** *(v1.4 enhanced)* — At 100% encumbrance, if the character has a transmute spell it may elect to convert items in-field (tier-scaled chance) rather than travelling to market.
* **Prestige Titles** — Build a legendary stacked title with each universe reset. Prestige clears active spell effects safely.
* **Achievement System** — 179 achievements across 9 categories including 31 new Magic achievements: spells learned, spells cast, transmutations performed, items crafted, status effects applied, and ticks spent under active effects.
* **Dev Tools** — Testing menu (Dev →) for force reset, level scaling, gold/XP injection.

## How to Play

### Windows (No Installation Required)

Download `IDLERPG.exe` from the [latest Releases](https://github.com/GreyHammond/IDLERPG/releases) page. Run it directly — no Python needed.

### Running from Source

1. Ensure you have **Python 3.x** installed.
2. Clone or download this repository.
3. Run the game:

   ```
   python IDLERPG.py
   ```

## Easy Expansion

The entire game is designed to be modded without touching any logic. Every piece of content lives in dictionaries and lists at the top of `IDLERPG.py`. Add new races, classes, items, quests, spells, or flavor text by simply editing the appropriate structure.

### What's Moddable

| Content | Variable | Example |
|---|---|---|
| Playable races | `RACES` | `"Orc"` |
| Classes | `CLASSES` | `"Necromancer"` |
| Name parts | `NAME_PREFIXES`, `NAME_SUFFIXES` | `"Xor"`, `"gath"` |
| Stats | `STAT_DEFS` | `"W": ("Wisdom", "...")` |
| Prologue quests | `PROLOGUE_QUESTS` | `{"name": "...", "steps": [...]}` |
| Main quests | `QUEST_TEMPLATES` | `{"name": "...", "steps": [...]}` |
| Boss quests | `BOSS_QUESTS` | `{"name": "...", "steps": [...]}` |
| Item bases | `ITEM_BASES` | `"Laser Sword"` (in "Weapon" list) |
| Item prefixes | `STANDARD_PREFIXES` | `"Rusty"`, `"Polished"` |
| Item materials | `MID_TIER_MATERIAL` | `"Steel"`, `"Mithril"` |
| Item suffixes | `HIGH_TIER_SUFFIX` | `"of the Void"`, `"of Embers"` |
| Item quality | `QUALITY_TIER` | `"Vorpal"`, `"Ruinous"` |
| Legendary titles | `LEGENDARY_TITLES` | `"The Harbinger"` |
| Act names | `ACT_NAMES` | `"The Shattered Dawn"` (98 unique names) |
| Action flavor text | `ACTION_FLAVORS` | `"fight": ["Punched a goon."]` |
| Spells | `SPELL_DEFINITIONS` | Full object with tier, cost, effect, description |
| Achievements | `achievements.py` | Add tiers to any generator function |

### Example: Adding a New Spell

Open `IDLERPG.py` and find `SPELL_DEFINITIONS`. Add a new entry:

```python
"Frost Nova": {
    "stat": "I", "tier": "Major", "mp_cost": 14, "duration": 6,
    "effect_type": "combat_defense", "magnitude": 0.18,
    "description": "Erupts in a burst of ice. Reduces incoming damage by 18% for 6 actions.",
},
```

`TIERED_SPELLS` is rebuilt automatically from `SPELL_DEFINITIONS` — no other changes needed. The spell becomes learnable by any class with Intelligence as a primary or secondary stat.

### Example: Adding a New Race

Find `RACES` and add an entry:

```python
"Minotaur",  # ← new race!
```

That's it. The game handles the rest automatically.

### Example: Adding a New Quest

Find `QUEST_TEMPLATES` and add:

```python
{"name": "Retrieve the Holy Bagel",
 "steps": [("travel",1),("fight",3),("loot",1),("return",1)]},
```

Available action types: `travel`, `search`, `locate`, `scout`, `speak`, `investigate`, `gather`, `escort`, `inspect`, `collect`, `fight`, `loot`, `return`, `rest`, `transmute`.

## Screenshots

[![I.D.L.E.R.P.G.](https://i.imgur.com/q3hhB53.png)](https://i.imgur.com/q3hhB53.png)

## Changelog

For detailed release notes and update history, see [CHANGELOG.md](https://github.com/GreyHammond/IDLERPG/blob/main/CHANGELOG.md).

## Tech Stack

* **Python 3.x**
* **Tkinter** (standard library GUI)
* **PyInstaller** (for .exe build)

## Building the .exe

```
pip install pyinstaller
pyinstaller IDLERPG.py --onefile --noconsole --icon=rpg.ico
```

## Credits

* **Grey Hammond** — Project Manager & Executive Director

## License

MIT License — do whatever you want with it.
