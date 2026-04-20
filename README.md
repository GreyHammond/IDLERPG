# I.D.L.E.R.P.G. — Complete Edition

A lightweight, feature-rich Idle RPG built with Python and Tkinter. This edition features full-screen character creation, dynamic questing, and a modular design that makes expanding the game world as simple as editing a list.

## Features

- **Character Customization** — Choose from 20 races and 20 classes with unique stat modifiers. Roll your own stats using the classic 4d6 drop-lowest method, or let the game generate a random name for you.
- **Persistent Progress** — Full save/load functionality means your hero's journey continues exactly where you left off.
- **Dynamic Gameplay** — Colored progress bars, dice-rolling mechanics, and multi-stage quests keep gameplay engaging.
- **Loot & Economy** — Manage an inventory with per-item selling, equipment upgrades, and a dynamic loot system with 30+ item prefixes and multiple equipment slots.
- **Spell System** — Unlock spells based on your class stats, progressing from Minor to Major to Tier II and beyond.
- **Death & Respawn** — Face consequence with a full death sequence, ghost mechanics, and respawn system.

## How to Play

## Screenshots
![I.D.L.E.R.P.G.](https://i.imgur.com/q3hhB53.png)

### Windows (No Installation Required)

Download `IDLERPG.exe` from the [latest Releases](https://github.com/your-repo/releases) page. Run it directly — no Python needed.

### Running from Source

1. Ensure you have **Python 3.x** installed.
2. Clone or download this repository.
3. Run the game:
   ```bash
   python rebuild.py
   ```

## Easy Expansion

The entire game is designed to be modded without touching any logic. Every piece of content lives in dictionaries and lists at the top of `rebuild.py`. Add new races, classes, items, quests, spells, or even flavor text by simply adding entries to the appropriate list.

### What's Moddable

| Content | Variable | Example |
|---------|----------|---------|
| Playable races | `RACES` | `"Orc"` |
| Classes | `CLASSES` | `"Necromancer"` |
| Name parts | `NAME_PREFIXES`, `NAME_SUFFIXES` | `"Xor"`, `"gath"` |
| Stats | `STAT_DEFS` | `"W": ("Wisdom", "...")` |
| Prologue quests | `PROLOGUE_QUESTS` | `{"name": "...", "steps": [...]}` |
| Main quests | `QUEST_TEMPLATES` | `{"name": "...", "steps": [...]}` |
| Boss quests | `BOSS_QUESTS` | `{"name": "...", "steps": [...]}` |
| Item prefixes | `ITEM_PREFIXES` | `"Atomic"` |
| Item bases | `ITEM_BASES` | `"Laser Sword"` (in "Weapon" list) |
| Action flavor text | `ACTION_FLAVORS` | `"fight": ["Punched a goon."]` |
| Spells | `TIERED_SPELLS` | `"Minor": ["Magic Bolt"]` |

### Example: Adding a New Race

Open `rebuild.py` and find line 30:

```python
RACES = [
    "Human",    "Elf",       "Dwarf",      "Halfling",  "Gnome",
    "Half-Orc", "Tiefling",  "Dragonborn", "Aasimar",   "Kenku",
    "Tabaxi",   "Lizardfolk", "Goliath",    "Firbolg",   "Tortle",
    "Changeling", "Shifter",  "Warforged",  "Fire Genasi", "Yuan-ti",
]
```

Add your new race:

```python
RACES = [
    "Human",    "Elf",       "Dwarf",      "Halfling",  "Gnome",
    "Half-Orc", "Tiefling",  "Dragonborn", "Aasimar",   "Kenku",
    "Tabaxi",   "Lizardfolk", "Goliath",    "Firbolg",   "Tortle",
    "Changeling", "Shifter",  "Warforged",  "Fire Genasi", "Yuan-ti",
    "Minotaur",  # ← new race!
]
```

That's it. The game automatically handles the rest. No code changes required.

### Example: Adding a New Quest

Find `QUEST_TEMPLATES` around line 113 and add:

```python
{"name": "Retrieve the Holy Bagel",
 "steps": [("travel",1),("fight",3),("loot",1),("return",1)]},
```

Quests use a simple step system: each tuple is `(action_type, count)`. Available action types include: `travel`, `search`, `locate`, `scout`, `speak`, `investigate`, `gather`, `escort`, `inspect`, `collect`, `fight`, `loot`, `return`, `rest`.

## Screenshots

> *(Add your screenshots here)*

## Tech Stack

- **Python 3.x**
- **Tkinter** (standard library GUI)
- **PyInstaller** (for .exe build)

## Building the .exe

```bash
pip install pyinstaller
pyinstaller rebuild.py --onefile --noconsole --icon=rpg.ico
```

## Credits

- **Grey Hammond** — Project Manager & Executive Director

## License

MIT License — do whatever you want with it.
