#!/usr/bin/env python3
"""
I.D.L.E.R.P.G.  —  Complete Edition
======================================
Idle RPG with full-screen character creation, radio-button race/class
selection, dice rolling, save/load, coloured progress bars, per-item
selling, and expanded quest stages.

╔══════════════════════════════════════════════════════╗
║         EXPANSION GUIDE — READ THIS FIRST            ║
║  Everything the game uses lives in the lists/dicts   ║
║  in the "EASY EXPANSION" section below.              ║
║  Add entries to any list to instantly add content.   ║
║  No other code changes are required.                 ║
╚══════════════════════════════════════════════════════╝
"""

import tkinter as tk
from tkinter import ttk, messagebox
import random
import json
import sys
import os
import time

try:
    from achievements import ACHIEVEMENTS, ACHIEVEMENT_LOOKUP
except ImportError:
    ACHIEVEMENTS = []
    ACHIEVEMENT_LOOKUP = {}

# ══════════════════════════════════════════════════════════════════════════════
#  ▶▶  EASY EXPANSION  ◀◀  — Add to any list/dict here to expand the game
# ══════════════════════════════════════════════════════════════════════════════

# ── Races ─────────────────────────────────────────────────────────────────────
RACES = [
    "Human",        "Elf",           "Dwarf",      "Halfling",    "Gnome",
    "Half-Orc",     "Tiefling",      "Dragonborn", "Aasimar",     "Kenku",
    "Tabaxi",       "Lizardfolk",    "Goliath",    "Firbolg",     "Tortle",
    "Changeling",   "Shifter",       "Warforged",  "Fire Genasi", "Yuan-ti",
]

# ── Classes ───────────────────────────────────────────────────────────────────
CLASSES = [
    "Fighter",       "Wizard",         "Rogue",         "Cleric",       "Ranger",
    "Paladin",       "Barbarian",      "Bard",          "Druid",        "Warlock",
    "Sorcerer",      "Monk",           "Blood Hunter",  "Artificer",    "Mystic",
    "Necromancer",   "Berserker",      "Shadow Dancer", "Arcane Archer","Templar",
]

# ── Random Name Parts (prefix + suffix) ───────────────────────────────────────
NAME_PREFIXES = [
    "Ald", "Ulbra", "Bran", "Cor", "Drav", "Eld", "Fyn", "Ghor", "Hael", "Iras", "Jor",
    "Kael", "Ulbra", "Lor", "Mor", "Nyx", "Orn", "Pyr", "Quen", "Rav", "Ser", "Thal",
    "Uld", "Vor", "Wren", "Xar", "Yev", "Zar", "Bel", "Cyn", "Dax", "Eon",
    "Fal", "Grix", "Hul", "Isen", "Jath", "Krell", "Luv", "Mox", "Nal", "Osh",
    "Pha", "Rhun", "Ulbra", "Siv", "Tox", "Val", "Zan", "Ulbra", "Ky", "Vex", "Mal", "Zeph", "Ulbra", "Ham"
]

NAME_SUFFIXES = [
    "an", "xtika", "ath", "en", "iel", "ion", "is", "ix", "on", "or", "thas",
    "wyn", "xtika", "dor", "fen", "gen", "har", "kar", "lar", "mar", "nar", "par",
    "aly", "xtika", "ark", "eb", "elle", "ia", "in", "ius", "og", "ora", "ross",
    "tyn", "xtika", "um", "ura", "vail", "via", "vorn", "xen", "yas", "yth", "zen",
    "eth", "xtika", "os", "un", "ryn", "vash", "tor", "gan", "mora", "lin", "del", "xtika", "mmond"
]

# ── Stat Definitions  key: (display_name, description) ───────────────────────
STAT_DEFS = {
    "I": ("Intellect",  "Increases XP gain and reduces ability cooldowns."),
    "D": ("Dexterity",  "Improves movement speed and chance to dodge attacks."),
    "L": ("Luck",       "Boosts critical hit rate and found loot quality."),
    "E": ("Endurance",  "Increases maximum Health points."),
    "R": ("Resilience", "Reduces incoming damage from all sources."),
    "P": ("Power",      "Increases raw physical damage dealt."),
    "G": ("Greed",      "Increases gold dropped and overall loot rates."),
}
STAT_KEYS = list("IDLERPG")

# ── Prologue Quests (tutorial) ────────────────────────────────────────────────
PROLOGUE_QUESTS = [
    {"name": "Learn to Walk", "steps": [("travel", 1), ("return", 1)]},
    {"name": "Look Around", "steps": [("search", 1), ("return", 1)]},
    {"name": "First Words", "steps": [("speak", 1), ("return", 1)]},
    {"name": "Open Your Bag", "steps": [("gather", 1), ("return", 1)]},
    {"name": "Inspect Your Gear", "steps": [("inspect", 1), ("return", 1)]},
    {"name": "Meet the Locals", "steps": [("travel", 1), ("speak", 1), ("return", 1)]},
    {"name": "First Purchase", "steps": [("travel", 1), ("speak", 1), ("return", 1)]},
    {"name": "Rest Up", "steps": [("rest", 1), ("return", 1)]},
]

PROLOGUE_COMPLETE = len(PROLOGUE_QUESTS)

# ── Act System ────────────────────────────────────────────────────────────────
QUESTS_PER_ACT = 10

ACT_NAMES = [
    "The Beginning", "The Journey", "The Trials", "The Dark Woods",
    "The Rising Shadow", "The Lost City", "The Ancient Evil", "The Final Stand",
    "The End of Days", "The New Era",
    "The Shattered Dawn", "The Broken Chains", "The Forgotten Path", "The Echoing Void",
    "The Crimson Skies", "The Iron Dominion", "The Falling Stars", "The Eternal Night",
    "The Azure Horizon", "The Sunken Kingdom", "The Whispering Tomb", "The Frozen Crown",
    "The Scorched Earth", "The Crystal Spire", "The Hidden Realm", "The Dying Light",
    "The Rusted Throne", "The Golden Age", "The Silent Storm", "The Burning Sea",
    "The Jagged Peaks", "The Hollow Mountain", "The Crimson Tide", "The Wandering Spirit",
    "The Eternal Flame", "The Shadow Realm", "The Frozen Wastes", "The Wandering Star",
    "The Ashen Wind", "The Crystal Cave", "The Forgotten Gate", "The Dying Kingdom",
    "The Iron Will", "The Silver Moon", "The Crimson Storm", "The Midnight Sun",
    "The Ancient Oath", "The Broken Mirror", "The Fiery Descent", "The Frozen Heart",
    "The Crimson Crown", "The Shadow King", "The Eternal Sorrow", "The Dark Eclipse",
    "The Radiant Dawn", "The Crimson Moon", "The Iron Fortress", "The Vanishing Point",
    "The Crimson Pact", "The Shadow Empire", "The Eternal Chaos", "The Dying Dawn",
    "The Iron Crown", "The Shadow Realm", "The Eternal Dream", "The Dark Convergence",
    "The Frozen Throne", "The Crimson King", "The Iron Covenant", "The Shadow War",
    "The Eternal Truth", "The Dark Awakening", "The Iron Rebellion", "The Shadow Eclipse",
    "The Crimson Covenant", "The Frozen Empire", "The Iron Conquest", "The Shadow Dawn",
    "The Eternal Vow", "The Dark Rebirth", "The Iron Legacy", "The Shadow Requiem",
    "The Crimson Requiem", "The Frozen Dawn", "The Iron Awakening", "The Shadow Genesis",
    "The Eternal Genesis", "The Dark Genesis", "The Iron Genesis", "The Shadow Ascension",
    "The Crimson Ascension", "The Frozen Ascension", "The Eternal Crown", "The Dark Crown",
    "The Iron Ascension", "The Shadow Nemesis", "The Crimson Nemesis", "The Frozen Nemesis"
]

# ── Title System ───────────────────────────────────────────────────────────────
TITLE_NOUNS = [
    "Vagabond", "Squire", "Slayer", "Hero", "Champion", "Saviour", "Templar", "Paladin",
    "Paragon", "Sentinel", "Archon", "Conqueror", "Monarch", "Sovereign", "Ascendant",
    "Mythos", "Grandmaster", "Legend", "Acolyte", "Crusader", "Warmaster", "Justiciar",
    "Oracle", "Harbinger", "Titan", "Deity", "Infinite", "Ethereal", "Wanderer",
    "Vanguard", "Overlord", "Hierophant", "Demiurge", "Highness", "Arbiter",
    "Luminary", "Warden", "Vindicator", "Gallant", "Revenant", "Dragoon",
    "Exorcist", "Seraph", "Cherub", "Vertex", "Apex", "Omniscience", "Nephilim",
    "Zealot", "Zero"
]

TITLE_ADJECTIVES = [
    "Revered", "Cursed", "Blessed", "Fallen", "Exalted", "Eternal", "Infallible",
    "Wretched", "Ancient", "Radiant", "Formidable", "Dread", "Venerated", "Gilded",
    "Spectral", "Mythic", "Absolute", "Primal", "Cosmic", "Hallowed", "Resolute",
    "Unyielding", "Shining", "Polished", "Automated", "Unstoppable", "Gleaming",
    "Tarnished", "Noble", "Corrupt", "Ascended", "Diligent", "Patient", "Calculated",
    "Relentless", "Sturdy", "Fragmented", "Wholistic", "Prime", "Void-Touched",
    "Star-Crossed", "Iron-Bound", "Silver-Tongued", "Blood-Soaked", "Aether-Born",
    "Light-Bearing", "Shadow-Wrapped", "Dust-Covered", "Elder"
]

TITLE_SUFFIXES = [
    "of the Dawn", "of the Void", "of Silence", "of the Infinite", "of Dust",
    "of Aeons", "of the Star", "of Entropy", "of the Cloud", "of the Heap",
    "of the Stack", "of the Legacy Code", "of the Alpha Build", "of the Final Boss",
    "of the Tutorial NPC", "of the Loading Bar", "of the Potato", "of the Sloth",
    "of the Gnat", "of Recurrence", "of the Grind", "of the Loot", "of the Spreadsheet"
]

TITLE_PREFIXES = [
    "Lesser", "Greater", "High", "Grand", "Master", "Uber", "Ultra", "True", "Elder",
    "Zenith", "Prism", "Hyper", "Super", "Mega", "Alpha", "Omega", "Transcendent",
    "Meta", "Extreme", "Ultimate", "Final", "Maximum", "Deep", "Wide", "Total",
    "Absolute", "Infinite", "Micro", "Macro", "Beyond", "Neo", "Retro", "Pro", "Elite"
]

# 98 Total Acts (Acts 1-98 index 0-97)

def to_roman(num):
    if num <= 0:
        return ""
    roman_numerals = [
        (100, ""), (90, "XC"), (50, "L"), (40, "XL"), (10, "X"),
        (9, "IX"), (5, "V"), (4, "IV"), (1, "I")
    ]
    result = ""
    for value, numeral in roman_numerals[1:]:
        while num >= value:
            result += numeral
            num -= value
    return result

def get_current_title(prestige_level):
    """Returns the most recent title tier for display"""
    if prestige_level < 0:
        return "Vagabond"
    pl = min(prestige_level, len(TITLE_NOUNS) - 1)
    position = pl % 5
    tier = pl // 5
    tier = min(tier, len(TITLE_NOUNS) - 1)
    
    if position == 0:
        return TITLE_NOUNS[tier]
    elif position == 1:
        adj = random.choice(TITLE_ADJECTIVES)
        return f"{adj} {TITLE_NOUNS[tier]}"
    elif position == 2:
        adj = random.choice(TITLE_ADJECTIVES)
        suff = random.choice(TITLE_SUFFIXES)
        return f"{adj} {TITLE_NOUNS[tier]} {suff}"
    else:  # position 3
        pref = random.choice(TITLE_PREFIXES)
        adj = random.choice(TITLE_ADJECTIVES)
        suff = random.choice(TITLE_SUFFIXES)
        return f"{pref} {adj} {TITLE_NOUNS[tier]} {suff}"

def get_full_title(prestige_level):
    """Returns the full stacked title for tooltip"""
    if prestige_level < 0:
        return "Vagabond"
    
    personas = []
    for pl in range(prestige_level + 1):
        position = pl % 5
        tier = pl // 5
        tier = min(tier, len(TITLE_NOUNS) - 1)
        
        if position == 0:
            personas.append(TITLE_NOUNS[tier])
        elif position == 1:
            adj = random.choice(TITLE_ADJECTIVES)
            personas.append(f"{adj} {TITLE_NOUNS[tier]}")
        elif position == 2:
            adj = random.choice(TITLE_ADJECTIVES)
            suff = random.choice(TITLE_SUFFIXES)
            personas.append(f"{adj} {TITLE_NOUNS[tier]} {suff}")
        elif position == 3:
            pref = random.choice(TITLE_PREFIXES)
            adj = random.choice(TITLE_ADJECTIVES)
            suff = random.choice(TITLE_SUFFIXES)
            personas.append(f"{pref} {adj} {TITLE_NOUNS[tier]} {suff}")
    
    return ", ".join(personas)

def get_act_name(act_index):
    if act_index == 99:
        return "The Final Battle"
    if act_index == 100:
        return "Resetting the Universe"
    if act_index > 100:
        cycle = ((act_index - 1) // 100) + 1
        roman = to_roman(cycle)
        base_index = (act_index - 1) % 98
        return f"{ACT_NAMES[base_index]} {roman}"
    return ACT_NAMES[act_index - 1]

# ── Boss Quest Templates ────────────────────────────────────────────────────
BOSS_QUESTS = [
    {"name": "The Gatekeeper", "steps": [("travel", 2), ("fight", 4), ("loot", 1), ("return", 1)]},
    {"name": "The Shadow Lord", "steps": [("travel", 2), ("scout", 1), ("fight", 5), ("loot", 1), ("return", 1)]},
    {"name": "The Dragon of the North", "steps": [("travel", 3), ("fight", 6), ("loot", 2), ("return", 1)]},
    {"name": "The Corrupted King", "steps": [("travel", 2), ("investigate", 1), ("fight", 5), ("loot", 1), ("return", 1)]},
    {"name": "The Ancient Horror", "steps": [("travel", 2), ("purify", 2), ("fight", 6), ("loot", 2), ("return", 1)]},
    {"name": "The Void Incarnate", "steps": [("travel", 3), ("fight", 8), ("loot", 2), ("return", 1)]},
    {"name": "The World Eater", "steps": [("travel", 4), ("fight", 10), ("loot", 3), ("return", 1)]},
    {"name": "The Final Nemesis", "steps": [("travel", 5), ("fight", 12), ("loot", 3), ("return", 1)]},
    {"name": "The End of Everything", "steps": [("travel", 8), ("fight", 15), ("loot", 4), ("return", 1)]},
    {"name": "The Last Battle", "steps": [("travel", 5), ("scout", 1), ("fight", 5), ("loot", 5), ("investigate", 2), ("purify", 10), ("return", 1)]},
]

# ── Quest Templates ───────────────────────────────────────���───────────────────
# Steps: list of (action_type, count). See ACTION_LABELS for valid action types.
QUEST_TEMPLATES = [
    {"name": "Exterminate the Djinns",
     "steps": [("travel",1),("search",1),("fight",3),("loot",1),("return",1)]},
    {"name": "Deliver the Sacred Parcel",
     "steps": [("travel",2),("locate",1),("speak",1),("return",1)]},
    {"name": "Retrieve the Enchanted Relic",
     "steps": [("travel",1),("search",1),("investigate",1),("fight",2),("loot",1),("return",1)]},
    {"name": "Placate the Ancient Spirits",
     "steps": [("travel",1),("locate",1),("speak",2),("fight",2),("return",1)]},
    {"name": "Seek the Gleaming Scabbard",
     "steps": [("travel",2),("search",1),("fight",4),("loot",2),("return",1)]},
    {"name": "Purge the Goblin Warren",
     "steps": [("travel",1),("scout",1),("fight",5),("loot",1),("return",1)]},
    {"name": "The Missing Merchant",
     "steps": [("travel",2),("investigate",2),("speak",1),("fight",1),("return",1)]},
    {"name": "Recover the Stolen Algorithm",
     "steps": [("travel",2),("locate",1),("speak",1),("fight",3),("loot",1),("return",1)]},
    {"name": "Silence the Haunted Forge",
     "steps": [("travel",1),("investigate",1),("fight",4),("loot",1),("return",1)]},
    {"name": "The Dungeon Audit",
     "steps": [("travel",2),("inspect",2),("speak",1),("fight",2),("loot",1),("return",1)]},
    {"name": "Escort the Frightened Witness",
     "steps": [("travel",1),("locate",1),("speak",1),("escort",2),("fight",2),("return",1)]},
    {"name": "Gather the Mystic Components",
     "steps": [("travel",1),("search",2),("gather",3),("fight",1),("return",1)]},
    {"name": "Defend the Outpost",
     "steps": [("travel",1),("scout",1),("fight",5),("rest",1),("fight",2),("return",1)]},
    {"name": "The Vanishing Village",
     "steps": [("travel",2),("investigate",2),("locate",1),("speak",2),("fight",3),("return",1)]},
    {"name": "Collect the Overdue Debts",
     "steps": [("travel",1),("locate",1),("speak",2),("fight",1),("collect",2),("return",1)]},
    {"name": "The Dragon's Hoard",
     "steps": [("travel",3),("scout",1),("fight",6),("loot",3),("return",1)]},
    {"name": "The Cursed Library",
     "steps": [("travel",1),("investigate",3),("fight",2),("gather",1),("return",1)]},
    {"name": "Infiltrate the Dark Spire",
     "steps": [("travel",2),("scout",2),("stealth",3),("fight",1),("loot",1),("return",1)]},
    {"name": "Hunt the Rogue Beast",
     "steps": [("travel",2),("track",3),("fight",1),("harvest",1),("return",1)]},
    {"name": "Sabotage the War Machine",
     "steps": [("travel",1),("scout",1),("sabotage",2),("fight",3),("return",1)]},
    {"name": "Bridge the Diplomatic Rift",
     "steps": [("travel",2),("speak",4),("gift",1),("speak",1),("return",1)]},
    {"name": "Survey the Uncharted Rift",
     "steps": [("travel",3),("scout",2),("inspect",3),("rest",1),("return",1)]},
    {"name": "Cleanse the Corrupted Well",
     "steps": [("travel",1),("fight",2),("purify",1),("loot",1),("return",1)]},
    {"name": "The Abandoned Mine Survey",
     "steps": [("travel",1),("inspect",4),("fight",2),("gather",2),("return",1)]},
    {"name": "Ransom the Captured Noble",
     "steps": [("travel",2),("speak",2),("trade",1),("escort",1),("return",1)]},
    {"name": "Siege of the Iron Citadel",
     "steps": [("travel",3),("scout",2),("sabotage",3),("fight",10),("loot",2),("return",1)]},
    {"name": "The Great Migration Escort",
     "steps": [("travel",5),("scout",3),("fight",4),("rest",2),("fight",4),("escort",5),("return",1)]},
    {"name": "Exorcise the Cathedral of Ashes",
     "steps": [("travel",2),("investigate",4),("purify",3),("fight",5),("speak",1),("return",1)]},
    {"name": "Navigate the Infinite Labyrinth",
     "steps": [("travel",4),("search",6),("inspect",4),("fight",3),("locate",1),("loot",2),("return",1)]},
    {"name": "The God-King's Assassination",
     "steps": [("travel",3),("stealth",5),("scout",2),("locate",1),("fight",1),("escape",3),("return",1)]},
    {"name": "Map the Abyssal Floor",
     "steps": [("travel",4),("scout",5),("inspect",5),("fight",2),("rest",1),("return",1)]},
    {"name": "Reclaim the Fallen Capital",
     "steps": [("travel",2),("scout",3),("fight",8),("locate",2),("fight",4),("loot",5),("return",1)]},
    {"name": "The Eternal Winter Ritual",
     "steps": [("travel",3),("gather",6),("locate",1),("purify",4),("fight",6),("return",1)]},
    {"name": "Ghost Ship Salvage Op",
     "steps": [("travel",2),("search",4),("fight",3),("loot",6),("investigate",2),("return",1)]}
]

# ── Action Flavor Text ────────────────────────────────────────────────────────
ACTION_FLAVORS = {
    "travel": [
        "Trudged through the Whispering Bog.",
        "Navigated the Bureaucratic Wastes.",
        "Crossed the Bridge of Mild Inconvenience.",
        "Wandered past several ominous signs.",
        "Hitched a ride on a sentient cart.",
        "Squeezed through the Corridor of Minor Regret.",
        "Took the long way around a suspicious swamp.",
        "Followed a road that wasn't on any map.",
        "Passed through a village that seemed too quiet.",
        "Rode hard for three hours in the wrong direction.",
        "Took a shortcut that definitely wasn't.",
        "Marched until the boots started complaining.",
        "Stumbled into a clearing that felt far too intentional.",
    ],
    "search": [
        "Swept the area for clues or enemies.",
        "Combed through the ruins methodically.",
        "Checked every shadow and alcove.",
        "Scoured the hillside for signs of life.",
        "Inspected the perimeter carefully.",
        "Dug through rubble looking for anything useful.",
        "Searched in the most obvious place last.",
        "Turned over every rock; found mostly bugs.",
        "Squinted at the horizon until eyes watered.",
        "Ransacked the area with surprising efficiency.",
    ],
    "locate": [
        "Tracked the quarry by footprints and rumour.",
        "Asked around until someone finally talked.",
        "Consulted a crumpled map. Mostly right.",
        "Followed the smoke to its source.",
        "Used the Compass of Vague Direction.",
        "Found it — exactly where the locals said to avoid.",
        "Cross-referenced three conflicting tip-offs.",
        "Tripped over the target while looking elsewhere.",
        "Spotted a shimmering glint in the distance.",
        "Followed an increasingly loud rhythmic thumping.",
    ],
    "scout": [
        "Observed from the treeline for a while.",
        "Counted enemy patrols and planned accordingly.",
        "Mapped the entrances. Two in, one out.",
        "Climbed a rock for a better view.",
        "Noted the guard rotation. Useful.",
        "Scouted silently on the downwind side.",
        "Watched. Waited. Learned.",
        "Sketching a crude map in the dirt.",
        "Confirmed the perimeter was poorly defended.",
        "Identified the leader by the size of their hat.",
    ],
    "speak": [
        "Negotiated with a reluctant NPC.",
        "Listened to an elderly quest-giver ramble for ages.",
        "Exchanged pleasantries with a suspicious merchant.",
        "Convinced a guard using only vague gestures.",
        "Agreed to terms without fully reading them.",
        "Delivered the bad news diplomatically. Mostly.",
        "Extracted information through persistent questioning.",
        "Read a cryptic notice board.",
        "Endured a lecture on local tax codes.",
        "Bantered with a rival adventurer. It was awkward.",
        "Nodded politely while ignoring the lore dump.",
    ],
    "investigate": [
        "Examined the scene for clues.",
        "Found something that didn't belong there.",
        "Cross-referenced three conflicting accounts.",
        "Noticed the footprints. Interesting.",
        "Deduced the culprit. Probably.",
        "Filed a mental report for later.",
        "The evidence was damning, if inexplicable.",
        "Puzzled over a cipher written in gravy.",
        "Found a scrap of fabric from a very expensive cloak.",
        "Connected the dots. They formed a circle.",
    ],
    "gather": [
        "Harvested the required herbs from a suspicious field.",
        "Collected components from the forest floor.",
        "Mined ore from the vein marked on the map.",
        "Gathered reagents. Some may be mildly toxic.",
        "Filled the satchel with the requisite materials.",
        "Foraged carefully. Did not get poisoned. Mostly.",
        "Plucked a rare mushroom from a rotting log.",
        "Scooped up glowing sand into a vial.",
        "Carefully detached a sample of pulsating moss.",
    ],
    "escort": [
        "Guided the charge safely past the first obstacle.",
        "Kept the civilian from wandering off. Again.",
        "Matched pace with the considerably slower traveller.",
        "Deflected two ambush attempts en route.",
        "Finally convinced them to stop humming loudly.",
        "Bodyblocked a stray arrow intended for the VIP.",
        "Repeatedly pointed out that 'this way' means 'not that way'.",
        "Dragged the client through a particularly deep puddle.",
    ],
    "inspect": [
        "Examined the ledgers with professional scepticism.",
        "Found several irregularities. Filed nothing.",
        "Catalogued the dungeon's assets.",
        "Measured things. Wrote down numbers. Looked busy.",
        "Tapped on walls for hollow sounds.",
        "The inventory was... creative.",
        "Peer-reviewed the structural integrity of a ruin.",
        "Noted that the traps were poorly maintained.",
        "Critiqued the decor of a villainous lair.",
    ],
    "collect": [
        "Knocked on doors until someone answered.",
        "Accepted payment. Eventually.",
        "Recovered the outstanding debt. With interest.",
        "Politely but firmly collected what was owed.",
        "Debtor was most persuaded by the drawn sword.",
        "Filled a jar with samples of local ectoplasm.",
        "Gathered the scattered pages of a ruined book.",
        "Retrieved the deposit from a very angry chest.",
    ],
    "fight": [
        "Brawled with a confused goblin.",
        "Defeated a moderately threatening skeleton.",
        "Exchanged blows with a disgruntled imp.",
        "Overcome a surprisingly chatty bandit.",
        "Subdued a feral accountant.",
        "Punched a specter into submission.",
        "Outsmarted a troll using basic arithmetic.",
        "Survived an ambush by aggressive staplers.",
        "Fended off a tax collector with extreme prejudice.",
        "Defeated a Mimic disguised as an armchair.",
        "Slew a wyvern. Lost a boot in the process.",
        "Trounced a cultist who wouldn't stop monologuing.",
        "Bested a cave troll in a staring contest, then hit it.",
        "Engaged in a high-stakes duel involving heavy sighs.",
        "Accidentally won a fight by slipping at the right time.",
        "Crushed a swarm of mechanical spiders.",
    ],
    "loot": [
        "Rifled through some abandoned luggage.",
        "Pried open a suspiciously unlocked chest.",
        "Collected something from the corpse. Gross.",
        "Found a hidden cache behind a loose stone.",
        "Scooped up coins from a defeated enemy.",
        "Discovered a trapped compartment. Disarmed it. Mostly.",
        "Looted a dungeon gift shop.",
        "Pocketed a shiny trinket of questionable value.",
        "Stripped the boss of their unnecessarily shiny armor.",
        "Found a single copper piece and a stale biscuit.",
    ],
    "return": [
        "Limped triumphantly back to town.",
        "Returned via the scenic route.",
        "Stumbled back to the tavern, victorious.",
        "Filed the quest paperwork at the guild.",
        "Arrived to modest applause.",
        "Made it back before the gates closed. Just.",
        "Retreated with more dignity than expected.",
        "Collapsed at the feet of the quest-giver.",
        "Walked back through the front gate like a hero.",
    ],
    "rest": [
        "Napped behind a mossy boulder.",
        "Meditated in a suspicious clearing.",
        "Ate some trail rations. Adequate.",
        "Sat down. Just for a minute. Two hours later...",
        "Made camp. Rolled a lumpy bedroll. Slept anyway.",
        "Stared into the campfire and questioned life choices.",
        "Sharpened a blade while ignoring a distance howl.",
        "Patched up a wound with a piece of a clean-ish shirt.",
    ],
    "sell": [
        "Haggled aggressively with the shopkeeper.",
        "Laid the item on the counter and waited.",
        "The merchant eyed it. Made an offer.",
        "Negotiated up by three gold. Felt good.",
        "Sold it for less than expected but more than nothing.",
        "The merchant grumbled but paid fair coin.",
        "A brief bidding war. Won it.",
        "Convinced the vendor that 'slightly used' meant 'vintage'.",
        "Dumped a bag of rusty swords on the floor. Took the gold.",
    ],
    "market": [
        "Bargained with every merchant in town.",
        "Compared prices across three shops.",
        "Persuaded the blacksmith to part with premium gear.",
        "Scoured the marketplace for bargains.",
        "Negotiated like a seasoned trader.",
        "Found exactly what was needed. Maybe.",
        "Left no merchant unbothered.",
    ],
    "find_vendor": [
        "Asked around for the best local trader.",
        "Followed rumors of a wealthy merchant.",
        "Checked the usual spots in the market district.",
        "A shopkeeper waved from across the street.",
        "Found a merchant with decent prices.",
        "Bargained with a roadside vendor.",
        "Located a specialty trader.",
    ],
    "return_town": [
        "Trudged back toward town.",
        "Carried the heavy load home.",
        "Struggled under the weight.",
        "Made slow progress back.",
        "Hauled everything to town.",
        "Dragged the loot back.",
    ],
    "ghost": [
        "Haunted the corridor in transparent indignation.",
        "Rattled chains for lack of options.",
        "漂ed through a wall because it was there.",
        "Tried to pick up a coin; hand went right through.",
        "Moaned spookily at a passing stray cat.",
    ],
    "body": [
        "Followed the trail of lost equipment back to the body.",
        "Located the corpse. Disappointing.",
        "Found the remains; they looked surprisingly peaceful.",
        "Identified the pile of gear. That's definitely yours.",
        "Recovered the physical shell. Still cold.",
    ],
    "reanimate": [
        "Convinced the soul to return. It complained the whole time.",
        "Stitched the spirit back to the flesh. Roughly.",
        "Invoked a loophole in the laws of mortality.",
        "Applied a spark of life to a very reluctant engine.",
        "Woke up with a gasp and a sudden craving for toast.",
    ],
    "respawn": [
        "Deposited back at the last known tavern.",
        "Reappeared with hair dishevelled and dignity missing.",
        "Manifested out of thin air, much to a goat's surprise.",
        "Re-materialized near a familiar-looking fountain.",
        "Returned to the world of the living. Gross...",
    ],
    "transmute": [
        "Drew arcane sigils in the air above the item.",
        "Whispered the words of unmaking. Something gleamed.",
        "The item dissolved into a shower of gold flecks.",
        "Focused intensely. The item collapsed into value.",
        "Transmuted the essence of the item into coin.",
        "The runes lit up. The item became gold.",
        "An alchemical gesture — and the bag got lighter.",
    ],
}

# ── Item Generation ────────────────────────────────────────────────────────────
STANDARD_PREFIXES = [
    "Shoddy", "Rusty", "Iron", "Crude", "Basic", "Simple", "Battered",
    "Used", "Second-Hand", "Plain", "Common", "Ordinary", "Humble"
]

EPIC_PREFIXES = [
    "Knight's", "Heroic", "Noble", "Ancient", "Champion's", "Warden",
    "Veteran's", "Master's", "Royal", "Arcane", "Enchanted", "Blessed",
    "Guardian", "Protector's", "Avenger", "Crusader", "Paladin's", "Runic"
]

LEGENDARY_PREFIXES = [
    "Legendary", "Divine", "Celestial", "Eternal", "Sovereign", "Mythic",
    "Heavenly", "Archangel's", "Sacred", "Transcendent", "Primordial", "Ethereal",
    "Aegis", "Pantheon's", "Olympian", "Celestia's", "Ascendant", "Elysian"
]

# ── Grammar-Based Item Naming Pools ───────────────────────────────────────────────
LOW_TIER_PREFIX = [
    "Rusty", "Shoddy", "Crude", "Bent", "Dull", "Worn", "Battered", "Polished",
    "Weighted", "Reinforced", "Tempered", "Pitted", "Blunted", "Sooty", "Dented",
    "Notched", "Corroded", "Oiled", "Balanced", "Reliable", "Sturdy", "Heavy",
    "Lightweight", "Scratched", "Chipped", "Splintered", "Grubby", "Mended",
    "Serviceable", "Glittering", "Pristine", "Brilliant", "Cold-Forged",
    "Warped", "Fractured", "Loose", "Ragged", "Tarnished", "Scuffed", "Faded",
    "Dusty", "Grimed", "Rough", "Uneven", "Patchwork", "Repaired", "Makeshift",
    "Weathered", "Cracked", "Stained", "Hardened", "Overused", "Wicked"
]

MID_TIER_MATERIAL = [
    "Steel", "Iron", "Bronze", "Mithril", "Adamantite", "Obsidian", "Dragonbone",
    "Ebonsteel", "Crystal", "Silver", "Cold-Iron", "Meteorite", "Cobalt", "Titanium",
    "Electrum", "Ghost-Wood", "Sun-Glass", "Void-Stone", "Living-Wood", "Darkscale",
    "Aether-Silk", "Star-Metal", "Orichalcum", "Plasteel", "Brimstone", "Moonsilver",
    "Deep-Platinum", "Runite", "Dwarven-Gold", "Ancient-Oak",
    "Blacksteel", "Blood-Iron", "Stormsteel", "Frost-Iron", "Emberstone", "Gravebone",
    "Nightglass", "Soulsteel", "Ironwood", "Sky-Crystal", "Hellforged Steel",
    "Ashen Bronze", "Doomsteel", "Spiritwood", "Wyrmscale", "Netherite",
    "Gloomstone", "Starforged Iron", "Duskwrought Steel", "Runebound Silver"
]

HIGH_TIER_SUFFIX = [
    "of Whispers", "of the Void", "of Embers", "of Darkness", "of Light",
    "of Storms", "of the Deep", "of Shadows", "of Many Sorrows", "of the Phoenix",
    "of Frozen Time", "of Blight", "of Thousand Cuts", "of the Mad King",
    "of Unending Night", "of the Sun-Eater", "of Woe", "of Infinite Regret",
    "of the Comet", "of Raging Tides", "of the Blood Moon", "of Ruin",
    "of Fallen Empires", "of the Silent One", "of Eternal Rest", "of Catastrophe",
    "of Malice", "of Grace", "of Dread", "of the Outer Planes",
    "of Shattered Stars", "of the Abyss", "of Final Breath", "of Endless Hunger",
    "of the Black Sun", "of Ash and Bone", "of Crimson Skies", "of the Last Dawn",
    "of Broken Oaths", "of Hollow Souls", "of the Dying World", "of Grim Tides",
    "of the Veil", "of Withering Flame", "of Starfall", "of the Deep Void",
    "of Silent Screams", "of the Iron Judgment", "of Gilded Ruin", "of Twilight’s End"
]

QUALITY_TIER = [
    "Ruinous", "Vorpal", "Exalted", "Eternal", "Primordial", "Divine", "Celestial",
    "Mythic", "Hallowed", "Blighted", "Shattered", "Transcendent", "Cursed",
    "Anomalous", "God-Slaying", "World-Ender", "Apostate", "Vengeful", "Ineffable",
    "Sovereign", "Singularity", "Apex", "Omniscient", "Radiant", "Fabled",
    "Ethereal", "Infinite", "Doomed", "Unstoppable", "Abyssal",
    "Mythforged", "Ascendant", "Paragon", "Empyrean", "Oblivion-Touched",
    "Star-Blessed", "Void-Bound", "Doomforged", "God-Touched", "Unbound",
    "Everlasting", "Cataclysmic", "Fatewoven", "Chrono-Broken", "Eclipse-Born",
    "Nether-Touched", "Heavenfall", "Gravebound", "Stormforged", "Runeblessed"
]


LEGENDARY_TITLES = [
    "The Harbinger", "Last Light", "Doomgiver", "The End", "Hope's Edge",
    "World-Breaker", "The Void", "Eternal Dawn", "Silence", "The Final Word",
    "Shattered Promise", "Grave-Digger", "Fate-Twister", "The Architect", "Echo of the Fall",
    "The Last Laugh", "Star-Crush", "Oblivion's Kiss", "The Unmaker", "Soul-Anchor",
    "Aether-Spire", "Calamity's Wake", "The Mourning Star", "Heart-Stopper", "The Paradox",
    "Nightfall", "The Great Leveller", "Cruel Mercy", "Sun-Eater", "The Iron Grave",
    "Truth-Seeker", "The Bitter End", "Crown of Thorns", "God-Slayer", "The Nameless",
    "Winter’s Breath", "The Gilded Lie", "Omen-Bringer", "The Hollow King", "Ashen Wake",
    "The Second Chance", "Blood-Letter", "The Weaver", "Broken Sky", "The Quiet",
    "Storm-Caller", "Lost Memory", "The First Stone", "The Glass Horizon", "Void-Stitcher",
    "The Midnight Sun", "Reaper’s Toll", "The Unspoken", "Dream-Eater", "The Pale Horse",
    "Cinder-Soul", "The Last Witness", "Gravity’s Grip", "The Ruined King", "Shadow-Stalker",
    "The Infinite Breath", "Star-Fell", "The Merciless", "Bone-Warden", "The False Prophet",
    "Aura of Ash", "The Dying Ember", "Finality's Reach", "The Black Horizon", "Fury Incarnate",
    "The Last Ember", "Oath-Breaker", "The Deep Silence", "Heaven’s Ruin", "The Fallen Crown",
    "Ashbringer", "The Final Horizon", "Storm of Bones", "The Fractured One", "Light’s Bane",
    "The Burning Veil", "Warden of Ruin", "The Crimson Oath", "Dread Sovereign", "The Cold Reckoning",
    "Veil-Piercer", "The Endless March", "Ruin’s Herald", "The Shrouded Truth", "King of Nothing",
    "The Severed Path", "Flame of Judgment", "The Withered Hand", "The Iron Oath", "Harvester of Echoes",
    "The Bleak Star", "The Unseen End", "Crownbreaker", "The Silent Cataclysm", "Bearer of Ash",
    "The Last Oracle", "Duskbringer", "The Forsaken Light", "Grave of Kings", "The Hollow Flame",
    "Tyrant of Dust", "The Veiled End", "Emberfall",
    "The Crawling Vast", "Eyes Beyond the Veil", "The Starved Cosmos", "Whisperer in Black Suns", "The Infinite Maw",
    "He Who Waits Beneath", "The Shattered Firmament", "Voice of the Outer Dark", "The Unblinking Abyss", "Dreams of the Drowned Sky",
    "The Hungering Silence", "Watcher Beyond Time", "The Spiral Madness", "The Void That Breathes", "The Broken Constellation",
    "The Flesh of Stars", "Harbinger of the Unseen", "The Blackened Orbit", "The Eternal Below", "The Mind Unraveled",
    "The Endless Eye", "The Screaming Horizon", "The Nameless Depth", "The Living Darkness", "The Outer Hunger",
    "The Sky That Watches", "The Depth Without End", "The Cosmic Blight", "The Unknowable Shape", "The Starless Dream",
    "The Drowned Cosmos", "The Hollow Universe", "The Rift Eternal", "The Many-Voiced Silence", "The Breach in Reality",
    "The Twisted Infinity", "The Crawling Eternity", "The Veil Torn Asunder", "The Unseen Choir", "The Beyond Made Flesh",
    "The Dark Between Stars", "The Shivering Expanse", "The Abyss Gazes Back", "The Fractured Cosmos", "The Unending Spiral",
    "The Echoing Void", "The Great Unraveling", "The Horror Unbound", "The Black Tide Rising", "The Infinite Descent",
    "Crown of Eternity", "The Divine Heir", "Sovereign of Stars", "The Golden Ascendant", "The Celestial Throne",
    "Bearer of the First Crown", "The Radiant Monarch", "The Ivory King", "Queen of the Last Dawn", "The Imperishable Crown",
    "The Sunforged Sovereign", "Lord of Endless Light", "The Sacred Regent", "The Crown Unbroken", "The Silver Emperor",
    "The Ascended King", "The Lion of Heaven", "The Throne Eternal", "The Crown of Ages", "The God-Crowned",
    "The High Sovereign", "The Anointed Flame", "The Crown of Judgment", "The King Undying", "The Throne of Glory",
    "The Regal Ascension", "The Crown Forged in Heaven", "The Divine Arbiter", "The King of First Light", "The Eternal Sovereign",
    "The Crown of the World", "The Sacred King", "The Throne Bearer", "The Crown of Stars", "The Monarch Eternal",
    "The Blessed Emperor", "The Crown of Dawn", "The King Beyond Time", "The Celestial King", "The Throne Unending",
    "The Crown of Radiance", "The Divine Kingmaker", "The Sovereign Ascendant", "The Crown of Infinity", "The Everlasting King",
    "The Throne of Ages", "The Crown of Divinity", "The King of Light Eternal", "The Crown Unyielding", "The Sovereign Immortal",
    "The Black Blade", "Gravewalker", "The Iron Oathbreaker", "Ashwalker", "The Bloodbound",
    "The Last Sellsword", "The Gallows King", "The Broken Blade", "The Wretched Knight", "The Dread Mercenary",
    "The Iron Tyrant", "The Hollow Blade", "The Bleeding Crown", "The Forsworn", "The Last Reaver",
    "The Mudborn King", "The Rusted Crown", "The Blackened Knight", "The Oathsworn Killer", "The Dagger in the Dark",
    "The Thorn Knight", "The Withered King", "The Ashen Blade", "The Bastard King", "The Broken Oath",
    "The Last Executioner", "The Bloodied Throne", "The Iron Bastard", "The Grim Sellsword", "The Dying Knight",
    "The War-Torn King", "The Crownless", "The Black Oath", "The Rust Knight", "The Hollow Crown",
    "The King in Chains", "The Blade of Ash", "The Fallen Sellsword", "The Bleak Knight", "The Red Reaver",
    "The Broken Throne", "The Black Gallows", "The Iron Reaver", "The King of Crows", "The Last Blackblade",
    "The Forsaken Knight", "The Blood Oath", "The Crown in Ruin", "The Ashen King", "The Dread Blade"
]


ITEM_BASES = {
    "Weapon": [
        "Dagger", "Mace", "Staff", "Crossbow", "Greatsword", "Wand", "Halberd", 
        "Rapier", "Battle Axe", "Scimitar", "Shortsword", "Warhammer", "Longbow", 
        "Maul", "Scythe", "Club", "Morning Star", "Flail", "Katar", "Trident"
    ],
    "Shield": [
        "Buckler", "Kite Shield", "Riot Lid", "Skull Plate", "Plank", 
        "Tower Shield", "Heater Shield", "Pavise", "Roundel", "Force Field"
    ],
    "Helm": [
        "Coif", "Dented Pot", "Horned Cap", "Visor", "Balaclava", "Great Helm", 
        "Crown", "Circlet", "Hood", "Sallet", "Bascinet", "Mask", "Turban"
    ],
    "Body": [
        "Chainmail", "Leather Vest", "Robe", "Hazmat Suit", "Plate Armour", 
        "Scale Mail", "Tunic", "Breastplate", "Gambeson", "Cuirass", "Brigandine"
    ],
    "Legs": [
        "Greaves", "Chaps", "Plate Skirt", "Shin Guards", "Mail Chausses", 
        "Leggings", "Trousers", "Poleyns", "Cuisses"
    ],
    "Ring": [
        "Ring of Fortune", "Signet Ring", "Band of Confusion", "Mood Ring", 
        "Iron Band", "Promise Ring", "Skull Ring", "Warding Band", "Loop of Agony"
    ],
    "Amulet": [
        "Lucky Charm", "Cursed Pendant", "Tooth Necklace", "Amulet of Power", 
        "Rune Pendant", "Medallion", "Locket", "Torc", "Reliquary", "Choker"
    ],
}

EQUIP_SLOTS = ["Weapon", "Shield", "Helm", "Body", "Legs", "Ring", "Amulet"]

# ── Class Stat Mapping: Name: (Major Stat, Minor Stat) ──────────────────
CLASS_STATS = {
    "Wizard": ("I", "D"), "Fighter": ("P", "E"), "Rogue": ("D", "L"),
    "Cleric": ("R", "I"), "Paladin": ("P", "R"), "Barbarian": ("E", "P"),
    "Bard": ("L", "D"), "Druid": ("I", "E"), "Warlock": ("I", "P"),
    "Sorcerer": ("I", "L"), "Monk": ("D", "R"), "Necromancer": ("I", "R"),
    "Berserker": ("P", "L"), "Shadow Dancer": ("D", "I"), "Arcane Archer": ("D", "P"),
    "Templar": ("R", "P"), "Ranger": ("D", "E"), "Blood Hunter": ("E", "I"),
    "Artificer": ("I", "L"), "Mystic": ("I", "D")
}

# ── Spell Definitions ───────────────────────────────────────────────────
# Each spell is a full object with behaviour data.
# effect_type keys:
#   xp_boost      — multiply XP gained while active
#   gold_boost    — multiply gold gained while active
#   stat_buff     — temporarily raise stat_key by magnitude (reverted on expiry)
#   hp_regen      — restore magnitude HP per tick while active
#   mp_regen      — restore magnitude MP per tick while active
#   combat_damage — add magnitude flat bonus damage in fights
#   combat_defense— reduce damage taken by magnitude fraction
#   loot_quality  — shift item power up by magnitude during drops
#   transmute     — convert inventory items in-field (instant, no duration)
#   craft         — Tier III: reroll an inventory item to higher power (instant)

SPELL_DEFINITIONS = {
    # ── Intellect (I) ─────────────────────────────────────────────────────
    "Magic Spark": {
        "stat": "I", "tier": "Minor", "mp_cost": 6, "duration": 6,
        "effect_type": "xp_boost", "magnitude": 0.15,
        "description": "Ignites a spark of arcane focus. Gain +15% XP for 6 actions.",
    },
    "Mana Drip": {
        "stat": "I", "tier": "Minor", "mp_cost": 0, "duration": 5,
        "effect_type": "mp_regen", "magnitude": 2,
        "description": "Slowly draws ambient mana inward. Restores 2 MP per action for 5 actions.",
    },
    "Arcane Blast": {
        "stat": "I", "tier": "Major", "mp_cost": 14, "duration": 0,
        "effect_type": "combat_damage", "magnitude": 8,
        "description": "Releases stored arcane energy in a single burst. Deals 8 bonus damage in the next fight.",
    },
    "Spell Shield": {
        "stat": "I", "tier": "Major", "mp_cost": 16, "duration": 8,
        "effect_type": "combat_defense", "magnitude": 0.20,
        "description": "Wraps the caster in a lattice of force. Reduces incoming damage by 20% for 8 actions.",
    },
    "Meteor Shower": {
        "stat": "I", "tier": "II", "mp_cost": 29, "duration": 0,
        "effect_type": "combat_damage", "magnitude": 22,
        "description": "Calls down a rain of arcane meteors. Deals 22 bonus damage in the next fight.",
    },
    "Time Warp": {
        "stat": "I", "tier": "II", "mp_cost": 27, "duration": 10,
        "effect_type": "xp_boost", "magnitude": 0.40,
        "description": "Bends the flow of time around the caster. Gain +40% XP for 10 actions.",
    },
    "The Omega Protocol": {
        "stat": "I", "tier": "III", "mp_cost": 57, "duration": 15,
        "effect_type": "xp_boost", "magnitude": 0.80,
        "description": "Unlocks a forbidden layer of cognition. Gain +80% XP for 15 actions.",
    },
    "Reality Collapse": {
        "stat": "I", "tier": "III", "mp_cost": 62, "duration": 0,
        "effect_type": "craft", "magnitude": 1,
        "description": "Tears the fabric of an item and reweaves it at higher power. Crafts one inventory item into a superior version.",
    },
    # ── Power (P) ─────────────────────────────────────────────────────────
    "Heavy Strike": {
        "stat": "P", "tier": "Minor", "mp_cost": 7, "duration": 0,
        "effect_type": "combat_damage", "magnitude": 6,
        "description": "A focused blow that bypasses armour. Deals 6 bonus damage in the next fight.",
    },
    "Pommel Bash": {
        "stat": "P", "tier": "Minor", "mp_cost": 6, "duration": 4,
        "effect_type": "stat_buff", "stat_key": "P", "magnitude": 3,
        "description": "Loosens up the weapon arm. Raises Power by 3 for 4 actions.",
    },
    "Sunder Armor": {
        "stat": "P", "tier": "Major", "mp_cost": 16, "duration": 8,
        "effect_type": "combat_defense", "magnitude": 0.15,
        "description": "Shatters the enemy's guard. Reduces damage taken by 15% for 8 actions.",
    },
    "Whirlwind": {
        "stat": "P", "tier": "Major", "mp_cost": 18, "duration": 0,
        "effect_type": "combat_damage", "magnitude": 14,
        "description": "Spins into a vortex of steel. Deals 14 bonus damage in the next fight.",
    },
    "Mountain Splitter": {
        "stat": "P", "tier": "II", "mp_cost": 32, "duration": 0,
        "effect_type": "combat_damage", "magnitude": 28,
        "description": "A strike so powerful it reshapes terrain. Deals 28 bonus damage in the next fight.",
    },
    "Dragon Roar": {
        "stat": "P", "tier": "II", "mp_cost": 27, "duration": 10,
        "effect_type": "stat_buff", "stat_key": "P", "magnitude": 8,
        "description": "Channels the ferocity of a dragon. Raises Power by 8 for 10 actions.",
    },
    "God-Slayer Impact": {
        "stat": "P", "tier": "III", "mp_cost": 62, "duration": 0,
        "effect_type": "combat_damage", "magnitude": 60,
        "description": "A blow capable of felling divine beings. Deals 60 bonus damage in the next fight.",
    },
    "World Ender": {
        "stat": "P", "tier": "III", "mp_cost": 57, "duration": 12,
        "effect_type": "stat_buff", "stat_key": "P", "magnitude": 18,
        "description": "Channels the force that breaks worlds. Raises Power by 18 for 12 actions.",
    },
    # ── Dexterity (D) ─────────────────────────────────────────────────────
    "Quick Stab": {
        "stat": "D", "tier": "Minor", "mp_cost": 6, "duration": 0,
        "effect_type": "combat_damage", "magnitude": 5,
        "description": "A lightning-fast thrust. Deals 5 bonus damage in the next fight.",
    },
    "Side Step": {
        "stat": "D", "tier": "Minor", "mp_cost": 5, "duration": 5,
        "effect_type": "stat_buff", "stat_key": "D", "magnitude": 3,
        "description": "Shifts weight to a lighter footing. Raises Dexterity by 3 for 5 actions.",
    },
    "Flurry of Blows": {
        "stat": "D", "tier": "Major", "mp_cost": 17, "duration": 0,
        "effect_type": "combat_damage", "magnitude": 16,
        "description": "Unleashes a rapid sequence of strikes. Deals 16 bonus damage in the next fight.",
    },
    "Shadow Dash": {
        "stat": "D", "tier": "Major", "mp_cost": 15, "duration": 7,
        "effect_type": "stat_buff", "stat_key": "D", "magnitude": 6,
        "description": "Moves through shadows faster than the eye can track. Raises Dexterity by 6 for 7 actions.",
    },
    "Assassinate": {
        "stat": "D", "tier": "II", "mp_cost": 31, "duration": 0,
        "effect_type": "combat_damage", "magnitude": 32,
        "description": "Finds the gap in every defence. Deals 32 bonus damage in the next fight.",
    },
    "Ghost Walk": {
        "stat": "D", "tier": "II", "mp_cost": 29, "duration": 10,
        "effect_type": "combat_defense", "magnitude": 0.25,
        "description": "Becomes briefly intangible. Reduces incoming damage by 25% for 10 actions.",
    },
    "Thousand Cuts": {
        "stat": "D", "tier": "III", "mp_cost": 60, "duration": 0,
        "effect_type": "combat_damage", "magnitude": 55,
        "description": "A thousand strikes in a single breath. Deals 55 bonus damage in the next fight.",
    },
    "Dimension Strike": {
        "stat": "D", "tier": "III", "mp_cost": 57, "duration": 12,
        "effect_type": "stat_buff", "stat_key": "D", "magnitude": 16,
        "description": "Strikes from a fold in space. Raises Dexterity by 16 for 12 actions.",
    },
    # ── Endurance (E) ─────────────────────────────────────────────────────
    "Iron Skin": {
        "stat": "E", "tier": "Minor", "mp_cost": 7, "duration": 6,
        "effect_type": "combat_defense", "magnitude": 0.12,
        "description": "Hardens the flesh to iron. Reduces incoming damage by 12% for 6 actions.",
    },
    "Deep Breath": {
        "stat": "E", "tier": "Minor", "mp_cost": 5, "duration": 5,
        "effect_type": "hp_regen", "magnitude": 4,
        "description": "Steadies the heart and heals. Restores 4 HP per action for 5 actions.",
    },
    "Unstoppable Will": {
        "stat": "E", "tier": "Major", "mp_cost": 18, "duration": 8,
        "effect_type": "stat_buff", "stat_key": "E", "magnitude": 6,
        "description": "Refuses to yield to pain. Raises Endurance by 6 for 8 actions.",
    },
    "Second Wind": {
        "stat": "E", "tier": "Major", "mp_cost": 16, "duration": 7,
        "effect_type": "hp_regen", "magnitude": 8,
        "description": "Draws on hidden reserves. Restores 8 HP per action for 7 actions.",
    },
    "Juggernaut Aura": {
        "stat": "E", "tier": "II", "mp_cost": 33, "duration": 12,
        "effect_type": "combat_defense", "magnitude": 0.30,
        "description": "Becomes an unstoppable force of endurance. Reduces incoming damage by 30% for 12 actions.",
    },
    "Eternal Stand": {
        "stat": "E", "tier": "II", "mp_cost": 29, "duration": 10,
        "effect_type": "hp_regen", "magnitude": 15,
        "description": "Roots to the earth and regenerates. Restores 15 HP per action for 10 actions.",
    },
    "Immortal Essence": {
        "stat": "E", "tier": "III", "mp_cost": 62, "duration": 15,
        "effect_type": "hp_regen", "magnitude": 25,
        "description": "Taps into an undying life force. Restores 25 HP per action for 15 actions.",
    },
    "Bastion of Life": {
        "stat": "E", "tier": "III", "mp_cost": 60, "duration": 14,
        "effect_type": "combat_defense", "magnitude": 0.45,
        "description": "Becomes an immovable bastion of pure vitality. Reduces incoming damage by 45% for 14 actions.",
    },
    # ── Resilience (R) ────────────────────────────────────────────────────
    "Guard Up": {
        "stat": "R", "tier": "Minor", "mp_cost": 6, "duration": 5,
        "effect_type": "stat_buff", "stat_key": "R", "magnitude": 3,
        "description": "Raises the shield and steadies the stance. Raises Resilience by 3 for 5 actions.",
    },
    "Stone Flesh": {
        "stat": "R", "tier": "Minor", "mp_cost": 7, "duration": 5,
        "effect_type": "combat_defense", "magnitude": 0.10,
        "description": "Skin becomes briefly stone-hard. Reduces incoming damage by 10% for 5 actions.",
    },
    "Reflective Shell": {
        "stat": "R", "tier": "Major", "mp_cost": 18, "duration": 8,
        "effect_type": "combat_defense", "magnitude": 0.22,
        "description": "Wraps the body in a reflective ward. Reduces incoming damage by 22% for 8 actions.",
    },
    "Mana Shield": {
        "stat": "R", "tier": "Major", "mp_cost": 14, "duration": 7,
        "effect_type": "mp_regen", "magnitude": 4,
        "description": "Converts defensive focus into mana. Restores 4 MP per action for 7 actions.",
    },
    "Absolute Barrier": {
        "stat": "R", "tier": "II", "mp_cost": 35, "duration": 12,
        "effect_type": "combat_defense", "magnitude": 0.35,
        "description": "An impenetrable ward of pure will. Reduces incoming damage by 35% for 12 actions.",
    },
    "Kinetic Dampener": {
        "stat": "R", "tier": "II", "mp_cost": 29, "duration": 10,
        "effect_type": "stat_buff", "stat_key": "R", "magnitude": 10,
        "description": "Absorbs and redirects kinetic force. Raises Resilience by 10 for 10 actions.",
    },
    "Diamond Soul": {
        "stat": "R", "tier": "III", "mp_cost": 62, "duration": 15,
        "effect_type": "combat_defense", "magnitude": 0.50,
        "description": "The soul crystallises into pure diamond. Reduces incoming damage by 50% for 15 actions.",
    },
    "Nullification Field": {
        "stat": "R", "tier": "III", "mp_cost": 57, "duration": 14,
        "effect_type": "stat_buff", "stat_key": "R", "magnitude": 20,
        "description": "Generates a field that nullifies hostile forces. Raises Resilience by 20 for 14 actions.",
    },
    # ── Luck (L) ──────────────────────────────────────────────────────────
    "Lucky Coin": {
        "stat": "L", "tier": "Minor", "mp_cost": 5, "duration": 6,
        "effect_type": "gold_boost", "magnitude": 0.20,
        "description": "Flips a coin that always lands lucky. Gain +20% gold for 6 actions.",
    },
    "Fate's Flick": {
        "stat": "L", "tier": "Minor", "mp_cost": 6, "duration": 5,
        "effect_type": "loot_quality", "magnitude": 2,
        "description": "Nudges fate just enough. Increases item power by +2 on next 5 drops.",
    },
    "Critical Eye": {
        "stat": "L", "tier": "Major", "mp_cost": 16, "duration": 8,
        "effect_type": "loot_quality", "magnitude": 5,
        "description": "Sees the hidden value in everything. Increases item power by +5 on next 8 drops.",
    },
    "Double Down": {
        "stat": "L", "tier": "Major", "mp_cost": 15, "duration": 8,
        "effect_type": "gold_boost", "magnitude": 0.45,
        "description": "Bets everything and wins. Gain +45% gold for 8 actions.",
    },
    "Jackpot Strike": {
        "stat": "L", "tier": "II", "mp_cost": 31, "duration": 10,
        "effect_type": "gold_boost", "magnitude": 0.80,
        "description": "Every action pays out like a jackpot. Gain +80% gold for 10 actions.",
    },
    "Fortune's Favor": {
        "stat": "L", "tier": "II", "mp_cost": 29, "duration": 10,
        "effect_type": "loot_quality", "magnitude": 10,
        "description": "Fortune itself reaches down to help. Increases item power by +10 on next 10 drops.",
    },
    "Reality Cheat": {
        "stat": "L", "tier": "III", "mp_cost": 60, "duration": 14,
        "effect_type": "gold_boost", "magnitude": 1.50,
        "description": "Cheats the rules of reality in your favour. Gain +150% gold for 14 actions.",
    },
    "God-Hand Roll": {
        "stat": "L", "tier": "III", "mp_cost": 57, "duration": 0,
        "effect_type": "craft", "magnitude": 1,
        "description": "Rolls the dice of creation itself. Crafts one inventory item into a superior version.",
    },
    # ── Greed (G) ─────────────────────────────────────────────────────────
    "Coinsense": {
        "stat": "G", "tier": "Minor", "mp_cost": 5, "duration": 6,
        "effect_type": "gold_boost", "magnitude": 0.25,
        "description": "Nose twitches at the scent of gold. Gain +25% gold for 6 actions.",
    },
    "Bargain Hint": {
        "stat": "G", "tier": "Minor", "mp_cost": 4, "duration": 5,
        "effect_type": "transmute", "magnitude": 0.40,
        "description": "Sees what an item is truly worth. Transmutes one inventory item to gold at 40% market rate.",
    },
    "Golden Touch": {
        "stat": "G", "tier": "Major", "mp_cost": 16, "duration": 9,
        "effect_type": "gold_boost", "magnitude": 0.60,
        "description": "Everything touched turns to profit. Gain +60% gold for 9 actions.",
    },
    "Treasure Sense": {
        "stat": "G", "tier": "Major", "mp_cost": 14, "duration": 0,
        "effect_type": "transmute", "magnitude": 0.55,
        "description": "Extracts the hidden value from an item. Transmutes one inventory item to gold at 55% market rate.",
    },
    "Midas Grip": {
        "stat": "G", "tier": "II", "mp_cost": 32, "duration": 12,
        "effect_type": "gold_boost", "magnitude": 1.00,
        "description": "The legendary touch of Midas. Gain +100% gold for 12 actions.",
    },
    "Wealth Aura": {
        "stat": "G", "tier": "II", "mp_cost": 27, "duration": 0,
        "effect_type": "transmute", "magnitude": 0.70,
        "description": "Radiates an aura of pure value. Transmutes one inventory item to gold at 70% market rate.",
    },
    "King's Fortune": {
        "stat": "G", "tier": "III", "mp_cost": 60, "duration": 15,
        "effect_type": "gold_boost", "magnitude": 2.00,
        "description": "Commands the wealth of kings. Gain +200% gold for 15 actions.",
    },
    "Everfull Purse": {
        "stat": "G", "tier": "III", "mp_cost": 52, "duration": 0,
        "effect_type": "transmute", "magnitude": 0.82,
        "description": "The purse that is never empty. Transmutes one inventory item to gold at 82% market rate. (Tier III cap.)",
    },
}

# Convenience lookup: name -> definition
SPELL_BY_NAME = {k: v for k, v in SPELL_DEFINITIONS.items()}

# Rebuild TIERED_SPELLS as name lists (preserves generate_stat_spell logic)
TIERED_SPELLS = {}
for _name, _sp in SPELL_DEFINITIONS.items():
    _st = _sp["stat"]
    _ti = _sp["tier"]
    TIERED_SPELLS.setdefault(_st, {}).setdefault(_ti, []).append(_name)

# ══════════════════════════════════════════════════════════════════════════════
#  CONFIG  (tweak gameplay here)
# ══════════════════════════════════════════════════════════════════════════════
if getattr(sys, 'frozen', False):
    # The directory where the .exe is located
    BASE_DIR = os.path.dirname(sys.executable)
else:
    # The directory where the .py script is located
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

SAVES_DIR = os.path.join(BASE_DIR, "saves")

DEATH_SEQUENCE = [
    "☠ You have been slain.",
    "  Lost all inventory. Lost half your gold.",
    "  Becoming a ghost...",
]
RESPAWN_STEPS = [
    ("ghost",    "Haunting the area as a ghost..."),
    ("body",     "Locating the body..."),
    ("reanimate","Reanimating the corpse..."),
    ("respawn",  "Respawning in last known town..."),
]
ACTION_LABELS = {
    "travel":      "Traveling...",
    "search":      "Searching the area...",
    "locate":      "Locating the target...",
    "scout":       "Scouting ahead...",
    "speak":       "Speaking with locals...",
    "investigate": "Investigating...",
    "gather":      "Gathering resources...",
    "escort":      "Escorting the charge...",
    "inspect":     "Inspecting...",
    "collect":     "Collecting...",
    "fight":       "Fighting!",
    "loot":        "Looting...",
    "return":      "Returning to town...",
    "rest":        "Resting...",
    "market":      "At the market...",
    "find_vendor":  "Finding a vendor...",
    "sell":        "Selling at vendor...",
    "restore":     "Restoring HP/MP...",
    "transmute":   "Transmuting items...",
    "upgrade":     "Upgrading gear...",
    "return_town":  "Returning to town...",
    "ghost":       "Haunting the area...",
    "body":        "Finding the body...",
    "reanimate":   "Reanimating...",
    "respawn":     "Respawning...",
}

# ══════════════════════════════════════════════════════════════════════════════
#  HELPERS
# ══════════════════════════════════════════════════════════════════════════════

def roll_stat():
    """4d6 drop-lowest — classic D&D method, returns 3–18."""
    dice = sorted(random.randint(1, 6) for _ in range(4))
    return sum(dice[1:])

def random_name():
    return random.choice(NAME_PREFIXES) + random.choice(NAME_SUFFIXES)

def generate_item(level, allow_stacked_prefix=True):
    slot   = random.choice(EQUIP_SLOTS)
    base   = random.choice(ITEM_BASES[slot])
    stat   = random.choice(STAT_KEYS)
    bonus  = 1 + (level // 3)
    power  = level + random.randint(0, 1)
    weight = 1 + (power // 5)

    parts = []

    # Slot 1: LEGENDARY_TITLE (Power 50+)
    if power >= 50:
        parts.append(random.choice(LEGENDARY_TITLES) + ", the")

    # Slot 2: QUALITY_TIER replaces LOW_TIER_PREFIX (Power 35+)
    if power >= 35:
        parts.append(random.choice(QUALITY_TIER))

    # Slot 3: MATERIAL (Power 20+)
    material = ""
    if power >= 20:
        material = random.choice(MID_TIER_MATERIAL)

    # Slot 4: PREFIX (Power 10+), MATERIAL (Power 20+)
    if power >= 10 and power < 35:
        prefix = random.choice(LOW_TIER_PREFIX)
        if material:
            parts.append(f"{prefix} {material}")
        else:
            parts.append(prefix)
    elif power >= 20 and material:
        parts.append(material)

    # Slot 5: BASE (always)
    parts.append(base)

    # Slot 6: SUFFIX (Power 35+)
    if power >= 35:
        parts.append(random.choice(HIGH_TIER_SUFFIX))

    name = " ".join(parts)

    return {"name": name, "slot": slot,
            "stat": stat, "bonus": bonus, "power": power, "weight": weight, "upgrade": 0}

def item_display(item):
    upg = item.get("upgrade", 0)
    upg_str = f"+{upg}" if upg > 0 else ""
    return f"{item['name']}{upg_str} [{item['stat']}+{item['bonus']}]"

def item_sell_value(item, luck):
    base = item["power"] * 3 + item["bonus"] * 2
    upg_bonus = item.get("upgrade", 0) * 5
    return max(1, int((base + upg_bonus) * (1 + luck * 0.01)))

def upgrade_cost(item):
    lvl = item.get("upgrade", 0)
    return int(10 * (1.15) ** lvl)

def generate_stat_spell(char):
    class_info = CLASS_STATS.get(char.get("class", "Wizard"), ("I", "L"))
    target_stat = class_info[0] if random.random() > 0.3 else class_info[1]
    pool = TIERED_SPELLS.get(target_stat, TIERED_SPELLS["I"])
    current_spells = char["spells"]

    eligible_tiers = ["Minor"]
    if any(s in pool["Minor"] for s in current_spells):
        eligible_tiers.append("Major")
    if any(s in pool["Major"] for s in current_spells):
        eligible_tiers.append("II")
    if any(s in pool["II"] for s in current_spells):
        eligible_tiers.append("III")

    chosen_tier = random.choice(eligible_tiers)
    return random.choice(pool[chosen_tier])

# ── Spell / Active-Effect Helpers ─────────────────────────────────────────────
import math as _math

def transmute_efficiency(spell_tier, intelligence):
    """Returns a float 0..0.92 — fraction of market value a transmute yields."""
    tier_base = {"Minor": 0.40, "Major": 0.55, "II": 0.70, "III": 0.82}
    base = tier_base.get(spell_tier, 0.40)
    i_bonus = 0.18 * _math.log(1 + intelligence / 20)
    return min(0.92, base + i_bonus)

def cast_chance(spell_def, char):
    """Probability [0..1] that this spell fires this tick, given class affinity."""
    class_stats = CLASS_STATS.get(char.get("class", "Wizard"), ("I", "L"))
    tier_base = {"Minor": 0.35, "Major": 0.25, "II": 0.18, "III": 0.10}
    base = tier_base.get(spell_def["tier"], 0.20)
    # Class primary stat match gives full chance; secondary half; off-stat 1/6
    if spell_def["stat"] == class_stats[0]:
        affinity = 1.0
    elif spell_def["stat"] == class_stats[1]:
        affinity = 0.5
    else:
        affinity = 0.16
    return base * affinity

# Action types where each category of spell is permitted to fire
SPELL_CAST_WINDOWS = {
    "xp_boost":       {"rest", "travel", "search", "locate", "scout",
                       "investigate", "gather", "escort", "inspect", "collect", "speak"},
    "gold_boost":     {"loot", "rest", "travel"},
    "stat_buff":      {"rest", "travel", "fight"},
    "hp_regen":       {"rest"},
    "mp_regen":       {"rest", "travel"},
    "combat_damage":  {"fight"},
    "combat_defense": {"fight", "rest"},
    "loot_quality":   {"loot"},
    "transmute":      {"loot"},          # in-field transmutation
    "craft":          {"loot", "rest"},  # Tier III crafting roll
}

def tick_active_effects(char):
    """Decrement ticks on all active effects; revert expired stat buffs."""
    remaining = []
    for eff in char.get("active_effects", []):
        eff["ticks_left"] -= 1
        if eff["ticks_left"] <= 0:
            # Revert stat buffs cleanly
            if eff["effect_type"] == "stat_buff":
                key = eff.get("stat_key", "")
                if key and key in char["stats"]:
                    char["stats"][key] -= eff["magnitude"]
        else:
            remaining.append(eff)
    char["active_effects"] = remaining

def has_active_effect(char, effect_type):
    """True if an effect of this type is currently running."""
    return any(e["effect_type"] == effect_type for e in char.get("active_effects", []))

def get_max_capacity(stats):
    return stats.get("P", 10) * 5 + stats.get("E", 10) * 2

def get_inventory_weight(inventory):
    return sum(item.get("weight", 1) for item in inventory)

def item_stat_power(item):
    return item.get("power", 1) + item.get("bonus", 0) + item.get("upgrade", 0)

def item_buy_value(item, luck):
    base = item.get("power", 1) * 5 + item.get("bonus", 0) * 3
    upg = item.get("upgrade", 0)
    return max(10, int((base * (1.15 ** upg)) * (1 + luck * 0.01)))

# ══════════════════════════════════════════════════════════════════════════════
#  SCROLLABLE RADIO FRAME  (reusable widget for race/class lists)
# ══════════════════════════════════════════════════════════════════════════════

class ScrollableRadioFrame(tk.Frame):
    """Canvas-backed scrollable frame of radio buttons."""
    def __init__(self, parent, options, variable, panel_bg="#141428", **kwargs):
        super().__init__(parent, bg=panel_bg, **kwargs)
        self._bg = panel_bg

        canvas = tk.Canvas(self, borderwidth=0, highlightthickness=0, bg=panel_bg)
        sb     = ttk.Scrollbar(self, orient="vertical", command=canvas.yview)
        inner  = tk.Frame(canvas, bg=panel_bg)

        inner.bind("<Configure>",
                   lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        win = canvas.create_window((0, 0), window=inner, anchor="nw")
        canvas.configure(yscrollcommand=sb.set)
        canvas.bind("<Configure>", lambda e: canvas.itemconfig(win, width=e.width))

        canvas.pack(side="left", fill="both", expand=True)
        sb.pack(side="right", fill="y")

        def _mwheel(event):
            canvas.yview_scroll(-1 * (event.delta // 120), "units")

        for opt in options:
            rb = tk.Radiobutton(inner, text=opt, variable=variable, value=opt,
                                font=("Segoe UI", 10), anchor="w",
                                bg=panel_bg, fg="#ddddee",
                                activebackground=panel_bg, activeforeground="white",
                                selectcolor="#2a2a50", cursor="hand2")
            rb.pack(fill="x", padx=8, pady=2)
            rb.bind("<MouseWheel>", _mwheel)
            canvas.bind("<MouseWheel>", _mwheel)

# ══════════════════════════════════════════════════════════════════════════════
#  MAIN APPLICATION
# ══════════════════════════════════════════════════════════════════════════════

BG_DARK  = "#000000"
BG_MID   = "#0a0a0a"
BG_PANEL = "#000000"
BG_ROW   = "#0a0a0a"
FG_GOLD  = "#00ff00"
FG_TEXT  = "#00ff00"
FG_DIM   = "#00aa00"
BTN_DARK = "#003300"
BTN_GO   = "#006600"
BTN_BAK  = "#330000"

THEMES = {
    "Classic": {
        "bg_dark":   "#000000",
        "bg_mid":    "#0a0a0a",
        "bg_panel":  "#000000",
        "bg_row":    "#0a0a0a",
        "fg_gold":   "#00ff00",
        "fg_text":   "#00ff00",
        "fg_dim":    "#00aa00",
        "btn_dark":  "#003300",
        "btn_go":    "#006600",
        "btn_bak":   "#330000",
        "hp_bar":    "#cc3333",
        "mp_bar":    "#2266dd",
        "xp_bar":    "#22aa44",
        "gold_bar":  "#cc9922",
        "input_bg":  "#1e1e38",
        "story_bg":  "#08080f",
        "panel_bg":  "#0a0a18",
        "text_death":  "#ff4455",
        "text_ghost":  "#aa88ff",
        "text_level":  "#44ff88",
        "text_quest":  "#ffcc44",
        "text_vendor": "#44ddff",
        "text_normal": "#cccccc",
    },
    "Sunshine": {
        "bg_dark":   "#ffffe0",
        "bg_mid":    "#fff8dc",
        "bg_panel":  "#fffacd",
        "bg_row":    "#fff8b8",
        "fg_gold":   "#8b7500",
        "fg_text":   "#4a3c00",
        "fg_dim":    "#6b5a00",
        "btn_dark":  "#daa520",
        "btn_go":    "#228b22",
        "btn_bak":   "#cd5c5c",
        "hp_bar":    "#ff6347",
        "mp_bar":    "#4682b4",
        "xp_bar":    "#32cd32",
        "gold_bar":  "#ffd700",
        "input_bg":  "#fffef0",
        "story_bg":  "#fffff0",
        "panel_bg":  "#fff8dc",
        "text_death":  "#dc143c",
        "text_ghost":  "#9370db",
        "text_level":  "#228b22",
        "text_quest":  "#d2691e",
        "text_vendor": "#1e90ff",
        "text_normal": "#4a3c00",
    },
    "Pastel": {
        "bg_dark":   "#2d2d3a",
        "bg_mid":    "#3d3d4a",
        "bg_panel":  "#252530",
        "bg_row":    "#353545",
        "fg_gold":   "#ffd1dc",
        "fg_text":   "#e6e6fa",
        "fg_dim":   "#b0c4de",
        "btn_dark":  "#6a5acd",
        "btn_go":    "#20b2aa",
        "btn_bak":   "#cd5c5c",
        "hp_bar":    "#ffb6c1",
        "mp_bar":    "#87ceeb",
        "xp_bar":    "#98fb98",
        "gold_bar":  "#ffe4b5",
        "input_bg":  "#404050",
        "story_bg":  "#1a1a25",
        "panel_bg":  "#2a2a35",
        "text_death":  "#ff6961",
        "text_ghost":  "#b39eb5",
        "text_level":  "#77dd77",
        "text_quest":  "#ffb347",
        "text_vendor": "#79c0ff",
        "text_normal": "#d8bfd8",
    },
    "Terminal": {
        "bg_dark":   "#0c0c0c",
        "bg_mid":    "#1a1a1a",
        "bg_panel":  "#0c0c0c",
        "bg_row":    "#141414",
        "fg_gold":   "#00ffff",
        "fg_text":   "#00ff00",
        "fg_dim":    "#008800",
        "btn_dark":  "#003300",
        "btn_go":    "#004400",
        "btn_bak":   "#440000",
        "hp_bar":    "#ff0000",
        "mp_bar":    "#0000ff",
        "xp_bar":    "#00ff00",
        "gold_bar":  "#ffff00",
        "input_bg":  "#0a0a0a",
        "story_bg":  "#080808",
        "panel_bg":  "#0a0a0a",
        "text_death":  "#ff0000",
        "text_ghost":  "#ff00ff",
        "text_level":  "#00ff00",
        "text_quest":  "#ffff00",
        "text_vendor": "#00ffff",
        "text_normal": "#00ff00",
    },
        "Midnight": {
        "bg_dark":   "#0b1020",
        "bg_mid":    "#141b2d",
        "bg_panel":  "#111827",
        "bg_row":    "#1b2438",
        "fg_gold":   "#7dd3fc",
        "fg_text":   "#e0f2fe",
        "fg_dim":    "#94a3b8",
        "btn_dark":  "#1e3a5f",
        "btn_go":    "#256d85",
        "btn_bak":   "#7f1d1d",
        "hp_bar":    "#ef4444",
        "mp_bar":    "#3b82f6",
        "xp_bar":    "#10b981",
        "gold_bar":  "#f59e0b",
        "input_bg":  "#0f172a",
        "story_bg":  "#0b1120",
        "panel_bg":  "#111827",
        "text_death":  "#f87171",
        "text_ghost":  "#c084fc",
        "text_level":  "#34d399",
        "text_quest":  "#fbbf24",
        "text_vendor": "#38bdf8",
        "text_normal": "#dbeafe",
    },
    "Crimson": {
        "bg_dark":   "#1a0d0d",
        "bg_mid":    "#2b1111",
        "bg_panel":  "#220909",
        "bg_row":    "#311313",
        "fg_gold":   "#ffcc99",
        "fg_text":   "#ffe4e1",
        "fg_dim":    "#d4a5a5",
        "btn_dark":  "#5c1f1f",
        "btn_go":    "#8b2e2e",
        "btn_bak":   "#3b0d0d",
        "hp_bar":    "#ff4d4d",
        "mp_bar":    "#5dade2",
        "xp_bar":    "#58d68d",
        "gold_bar":  "#f5b041",
        "input_bg":  "#2a1010",
        "story_bg":  "#180808",
        "panel_bg":  "#220909",
        "text_death":  "#ff6b6b",
        "text_ghost":  "#d7bde2",
        "text_level":  "#82e0aa",
        "text_quest":  "#f8c471",
        "text_vendor": "#85c1e9",
        "text_normal": "#f5c6c6",
    },
    "Forest": {
        "bg_dark":   "#0f1c12",
        "bg_mid":    "#1b2b1f",
        "bg_panel":  "#132017",
        "bg_row":    "#1d3323",
        "fg_gold":   "#d4af37",
        "fg_text":   "#e8f5e9",
        "fg_dim":    "#9db59e",
        "btn_dark":  "#2d4a2d",
        "btn_go":    "#3f6b3f",
        "btn_bak":   "#5c2f2f",
        "hp_bar":    "#c0392b",
        "mp_bar":    "#2980b9",
        "xp_bar":    "#27ae60",
        "gold_bar":  "#d4af37",
        "input_bg":  "#16261a",
        "story_bg":  "#0d170f",
        "panel_bg":  "#132017",
        "text_death":  "#e74c3c",
        "text_ghost":  "#bb8fce",
        "text_level":  "#58d68d",
        "text_quest":  "#f7dc6f",
        "text_vendor": "#5dade2",
        "text_normal": "#d5e8d4",
    },
    "Cyberpunk": {
        "bg_dark":   "#0d0221",
        "bg_mid":    "#1a0333",
        "bg_panel":  "#120126",
        "bg_row":    "#220544",
        "fg_gold":   "#ff00ff",
        "fg_text":   "#00f5ff",
        "fg_dim":    "#9d4edd",
        "btn_dark":  "#3c096c",
        "btn_go":    "#00b4d8",
        "btn_bak":   "#9d0208",
        "hp_bar":    "#ff006e",
        "mp_bar":    "#3a86ff",
        "xp_bar":    "#06d6a0",
        "gold_bar":  "#ffd60a",
        "input_bg":  "#14042b",
        "story_bg":  "#0a0118",
        "panel_bg":  "#120126",
        "text_death":  "#ff4d6d",
        "text_ghost":  "#c77dff",
        "text_level":  "#00f5d4",
        "text_quest":  "#ffd60a",
        "text_vendor": "#4cc9f0",
        "text_normal": "#caf0f8",
    },
    "Royal": {
        "bg_dark":   "#1a1633",
        "bg_mid":    "#2a2450",
        "bg_panel":  "#201b40",
        "bg_row":    "#312a5e",
        "fg_gold":   "#ffd700",
        "fg_text":   "#f8f4ff",
        "fg_dim":    "#c3b1e1",
        "btn_dark":  "#483d8b",
        "btn_go":    "#6a5acd",
        "btn_bak":   "#8b0000",
        "hp_bar":    "#dc143c",
        "mp_bar":    "#4169e1",
        "xp_bar":    "#32cd32",
        "gold_bar":  "#ffd700",
        "input_bg":  "#241d45",
        "story_bg":  "#18122b",
        "panel_bg":  "#201b40",
        "text_death":  "#ff4f6d",
        "text_ghost":  "#d8bfd8",
        "text_level":  "#7fff7f",
        "text_quest":  "#ffdf80",
        "text_vendor": "#87cefa",
        "text_normal": "#eee6ff",
    },
    "Desert": {
        "bg_dark":   "#3b2f2f",
        "bg_mid":    "#5a4632",
        "bg_panel":  "#4a3928",
        "bg_row":    "#6b523a",
        "fg_gold":   "#f4d35e",
        "fg_text":   "#fff8e7",
        "fg_dim":    "#d9c7a1",
        "btn_dark":  "#8b6f47",
        "btn_go":    "#a67c52",
        "btn_bak":   "#7b3f00",
        "hp_bar":    "#d1495b",
        "mp_bar":    "#3c91e6",
        "xp_bar":    "#6ab04c",
        "gold_bar":  "#f4d35e",
        "input_bg":  "#5a4632",
        "story_bg":  "#34271f",
        "panel_bg":  "#4a3928",
        "text_death":  "#ff7675",
        "text_ghost":  "#c8a2c8",
        "text_level":  "#9be564",
        "text_quest":  "#ffd166",
        "text_vendor": "#74c0fc",
        "text_normal": "#fcecc9",
    },
        "Steampunk": {
        "bg_dark":   "#2b1d14",
        "bg_mid":    "#3d2a1d",
        "bg_panel":  "#332419",
        "bg_row":    "#4a3525",
        "fg_gold":   "#d4a373",
        "fg_text":   "#f1e0c5",
        "fg_dim":    "#b08968",
        "btn_dark":  "#6f4e37",
        "btn_go":    "#8c6a43",
        "btn_bak":   "#5c2c2c",
        "hp_bar":    "#b03a2e",
        "mp_bar":    "#2874a6",
        "xp_bar":    "#239b56",
        "gold_bar":  "#c89b3c",
        "input_bg":  "#3a2b20",
        "story_bg":  "#241811",
        "panel_bg":  "#332419",
        "text_death":  "#e74c3c",
        "text_ghost":  "#c39bd3",
        "text_level":  "#58d68d",
        "text_quest":  "#f8c471",
        "text_vendor": "#5dade2",
        "text_normal": "#ead7b7",
    },
    "Ice Cavern": {
        "bg_dark":   "#0b1d2a",
        "bg_mid":    "#12384d",
        "bg_panel":  "#102b3a",
        "bg_row":    "#18465d",
        "fg_gold":   "#bde0fe",
        "fg_text":   "#e0fbfc",
        "fg_dim":    "#98c1d9",
        "btn_dark":  "#1d3557",
        "btn_go":    "#457b9d",
        "btn_bak":   "#7b2d26",
        "hp_bar":    "#ef476f",
        "mp_bar":    "#3a86ff",
        "xp_bar":    "#06d6a0",
        "gold_bar":  "#90e0ef",
        "input_bg":  "#153243",
        "story_bg":  "#08141d",
        "panel_bg":  "#102b3a",
        "text_death":  "#ff758f",
        "text_ghost":  "#b8c0ff",
        "text_level":  "#80ffdb",
        "text_quest":  "#caf0f8",
        "text_vendor": "#48cae4",
        "text_normal": "#edf6f9",
    },
    "Blood Moon": {
        "bg_dark":   "#14080e",
        "bg_mid":    "#2a0f19",
        "bg_panel":  "#1d0b12",
        "bg_row":    "#34121f",
        "fg_gold":   "#ffb4a2",
        "fg_text":   "#ffe5d9",
        "fg_dim":    "#c08497",
        "btn_dark":  "#5e2129",
        "btn_go":    "#8b2635",
        "btn_bak":   "#2b0a0f",
        "hp_bar":    "#ff4d6d",
        "mp_bar":    "#5dade2",
        "xp_bar":    "#57cc99",
        "gold_bar":  "#f4a261",
        "input_bg":  "#261019",
        "story_bg":  "#10060a",
        "panel_bg":  "#1d0b12",
        "text_death":  "#ff758f",
        "text_ghost":  "#d0a2f7",
        "text_level":  "#80ed99",
        "text_quest":  "#ffd6a5",
        "text_vendor": "#74c0fc",
        "text_normal": "#f8d7da",
    },
    "Vaporwave": {
        "bg_dark":   "#2b0a3d",
        "bg_mid":    "#4b1d6d",
        "bg_panel":  "#3a1459",
        "bg_row":    "#5c2a82",
        "fg_gold":   "#ff9ff3",
        "fg_text":   "#f1f2f6",
        "fg_dim":    "#c8a2c8",
        "btn_dark":  "#6c5ce7",
        "btn_go":    "#00cec9",
        "btn_bak":   "#d63031",
        "hp_bar":    "#ff6b81",
        "mp_bar":    "#54a0ff",
        "xp_bar":    "#1dd1a1",
        "gold_bar":  "#feca57",
        "input_bg":  "#44235f",
        "story_bg":  "#1e082e",
        "panel_bg":  "#3a1459",
        "text_death":  "#ff7675",
        "text_ghost":  "#e0aaff",
        "text_level":  "#55efc4",
        "text_quest":  "#ffeaa7",
        "text_vendor": "#74b9ff",
        "text_normal": "#f8f9fa",
    },
    "Dark Souls": {
        "bg_dark":   "#111111",
        "bg_mid":    "#1e1e1e",
        "bg_panel":  "#181818",
        "bg_row":    "#242424",
        "fg_gold":   "#c0a062",
        "fg_text":   "#d6d3ce",
        "fg_dim":    "#8d8b87",
        "btn_dark":  "#3a3a3a",
        "btn_go":    "#556b2f",
        "btn_bak":   "#5a1f1f",
        "hp_bar":    "#9b2226",
        "mp_bar":    "#3a86ff",
        "xp_bar":    "#588157",
        "gold_bar":  "#c0a062",
        "input_bg":  "#202020",
        "story_bg":  "#0d0d0d",
        "panel_bg":  "#181818",
        "text_death":  "#d62828",
        "text_ghost":  "#9d4edd",
        "text_level":  "#6a994e",
        "text_quest":  "#e9c46a",
        "text_vendor": "#4ea8de",
        "text_normal": "#d9d9d9",
    },
    "Arcade": {
        "bg_dark":   "#111827",
        "bg_mid":    "#1f2937",
        "bg_panel":  "#0f172a",
        "bg_row":    "#273449",
        "fg_gold":   "#facc15",
        "fg_text":   "#f8fafc",
        "fg_dim":    "#94a3b8",
        "btn_dark":  "#2563eb",
        "btn_go":    "#16a34a",
        "btn_bak":   "#dc2626",
        "hp_bar":    "#ef4444",
        "mp_bar":    "#3b82f6",
        "xp_bar":    "#22c55e",
        "gold_bar":  "#facc15",
        "input_bg":  "#1e293b",
        "story_bg":  "#0b1220",
        "panel_bg":  "#0f172a",
        "text_death":  "#f87171",
        "text_ghost":  "#c084fc",
        "text_level":  "#4ade80",
        "text_quest":  "#fde047",
        "text_vendor": "#38bdf8",
        "text_normal": "#e2e8f0",
    },
    "Parchment": {
        "bg_dark":   "#d8c9a3",
        "bg_mid":    "#e6d8b8",
        "bg_panel":  "#f3ead7",
        "bg_row":    "#e9dcc0",
        "fg_gold":   "#8b6f47",
        "fg_text":   "#3e2f1c",
        "fg_dim":    "#6e5a3c",
        "btn_dark":  "#a68a64",
        "btn_go":    "#6b8e23",
        "btn_bak":   "#b22222",
        "hp_bar":    "#cd5c5c",
        "mp_bar":    "#4682b4",
        "xp_bar":    "#6b8e23",
        "gold_bar":  "#daa520",
        "input_bg":  "#f8f1df",
        "story_bg":  "#f5eedc",
        "panel_bg":  "#f3ead7",
        "text_death":  "#b22222",
        "text_ghost":  "#9370db",
        "text_level":  "#228b22",
        "text_quest":  "#8b4513",
        "text_vendor": "#1e90ff",
        "text_normal": "#3e2f1c",
    },
}

CURRENT_THEME = "Classic"

class IdleRPG:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("I.D.L.E.R.P.G. — Complete Edition")
        try:
            ico_path = os.path.join(BASE_DIR, "rpg.ico")
            self.root.iconbitmap(ico_path)
        except Exception:
            pass
        try:
            self.root.state("zoomed")
        except tk.TclError:
            self.root.attributes("-zoomed", True)
        self._dead = False
        self.theme = tk.StringVar(value=CURRENT_THEME)
        os.makedirs(SAVES_DIR, exist_ok=True)
        self._setup_styles()
        self.show_menu()

    # ── ttk styles ────────────────────────────────────────────────────────────
    def _setup_styles(self):
        s = ttk.Style()
        s.theme_use("clam")
        theme_name = self.theme.get() if hasattr(self, 'theme') else CURRENT_THEME
        theme = THEMES.get(theme_name, THEMES["Classic"])
        for name, key in [
            ("HP",    "hp_bar"),
            ("MP",    "mp_bar"),
            ("XP",    "xp_bar"),
            ("Gold",  "gold_bar"),
            ("Blue",  "mp_bar"),
            ("Flash", "mp_bar"),   # bright flash style for spell casts
        ]:
            col = theme.get(key, "#000000")
            if name == "Flash":
                col = "#aaddff"   # always bright white-blue regardless of theme
            s.configure(f"{name}.Horizontal.TProgressbar",
                        troughcolor="#222233", background=col,
                        bordercolor="#111122", lightcolor=col,
                        darkcolor=col, thickness=18)
        s.configure("TLabelframe",       background=theme["bg_panel"], foreground=theme["fg_gold"])
        s.configure("TLabelframe.Label", background=theme["bg_panel"], foreground=theme["fg_gold"],
                    font=("Segoe UI", 9, "bold"))
        s.configure("TFrame",  background=theme["bg_panel"])
        s.configure("TLabel",  background=theme["bg_panel"], foreground=theme["fg_text"])
        s.configure("Treeview", background="#101020", fieldbackground="#101020",
                    foreground=theme["fg_text"], rowheight=20)
        s.configure("Treeview.Heading", background=theme["bg_mid"], foreground=theme["fg_gold"])

    # ── helpers ───────────────────────────────────────────────────────────────
    def clear_screen(self):
        if hasattr(self, "_stat_tip") and self._stat_tip.winfo_exists():
            self._stat_tip.destroy()
        for w in self.root.winfo_children():
            w.destroy()
        self.root.configure(bg=BG_DARK, menu=tk.Menu(self.root))  # clear menu bar

    def _btn(self, parent, text, cmd, bg=BTN_DARK, fg=FG_TEXT,
             font=("Segoe UI", 11), padx=14, pady=6):
        return tk.Button(parent, text=text, command=cmd, font=font,
                         bg=bg, fg=fg, activebackground=fg, activeforeground=bg,
                         relief="flat", cursor="hand2", padx=padx, pady=pady)

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    #  MAIN MENU
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    def show_menu(self):
        self.clear_screen()
        outer = tk.Frame(self.root, bg=BG_DARK)
        outer.place(relx=0.5, rely=0.5, anchor="center")

        tk.Label(outer, text="I.D.L.E.R.P.G.",
                 font=("Courier New", 56, "bold"), fg=FG_GOLD, bg=BG_DARK).pack(pady=(0, 4))
        tk.Label(outer, text="A Modern Re-Imagining Of The Zero-Player Progress Simulator",
                 font=("Courier New", 12), fg=FG_DIM, bg=BG_DARK).pack()
        tk.Label(outer, text="─" * 38, fg="#333355", bg=BG_DARK,
                 font=("Courier New", 16)).pack(pady=18)

        for txt, cmd in [
            ("⚔   New Character",   self.new_character_screen),
            ("📂  Load Character",  self.load_character_screen),
            ("🚪  Exit",            self.root.quit),
        ]:
            self._btn(outer, txt, cmd, font=("Segoe UI", 14),
                      padx=30, pady=12).pack(pady=7, ipadx=10)

    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    #  CHARACTER CREATION
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    def new_character_screen(self):
        self.clear_screen()

        # ── header ────────────────────────────────────────────────────────
        hdr = tk.Frame(self.root, bg=BG_DARK)
        hdr.pack(fill="x", padx=24, pady=(18, 6))
        tk.Label(hdr, text="⚔  Character Creation",
                 font=("Courier New", 26, "bold"), fg=FG_GOLD, bg=BG_DARK).pack(side="left")
        self._btn(hdr, "← Menu", self.show_menu,
                  font=("Segoe UI", 10), padx=10, pady=4).pack(side="right")
        tk.Frame(self.root, bg="#333355", height=1).pack(fill="x", padx=24)

        # ── name bar ──────────────────────────────────────────────────────
        nf = tk.Frame(self.root, bg=BG_DARK)
        nf.pack(fill="x", padx=28, pady=12)
        tk.Label(nf, text="Character Name:", font=("Segoe UI", 12, "bold"),
                 fg=FG_TEXT, bg=BG_DARK).pack(side="left")
        self._name_var = tk.StringVar(value=random_name())
        tk.Entry(nf, textvariable=self._name_var, font=("Segoe UI", 13), width=22,
                 bg="#1e1e38", fg="white", insertbackground="white",
                 relief="flat", bd=4).pack(side="left", padx=10)
        self._btn(nf, "🎲 Random", lambda: self._name_var.set(random_name()),
                  font=("Segoe UI", 10), padx=8, pady=3).pack(side="left")

        # ── four-column area ────────────────────────────────────────────
        body = tk.Frame(self.root, bg=BG_DARK)
        body.pack(fill="both", expand=True, padx=20, pady=4)
        body.columnconfigure(0, weight=1)
        body.columnconfigure(1, weight=1)
        body.columnconfigure(2, weight=1)
        body.columnconfigure(3, weight=1)
        body.rowconfigure(0, weight=1)

        # ─ Race column ───────────────────────────────────────────────────
        race_frm = tk.LabelFrame(body, text="  Race  ",
                                  font=("Segoe UI", 11, "bold"), fg=FG_GOLD,
                                  bg=BG_PANEL, bd=2, relief="groove")
        race_frm.grid(row=0, column=0, sticky="nsew", padx=8, pady=4)

        self._race_var = tk.StringVar(value=RACES[0])
        ScrollableRadioFrame(race_frm, RACES, self._race_var,
                              panel_bg=BG_PANEL).pack(fill="both", expand=True, padx=4, pady=4)

        crf = tk.Frame(race_frm, bg=BG_PANEL)
        crf.pack(fill="x", padx=8, pady=(0, 8))
        tk.Radiobutton(crf, text="Custom:", variable=self._race_var,
                       value="__custom_race__", font=("Segoe UI", 10),
                       bg=BG_PANEL, fg=FG_TEXT, activebackground=BG_PANEL,
                       selectcolor="#2a2a50", cursor="hand2").pack(side="left")
        self._custom_race = tk.Entry(crf, font=("Segoe UI", 10), width=14,
                                      bg="#1e1e38", fg="white", insertbackground="white",
                                      relief="flat", bd=3)
        self._custom_race.pack(side="left", padx=4)
        self._custom_race.bind("<FocusIn>",
                                lambda e: self._race_var.set("__custom_race__"))

        # ─ Class column ──────────────────────────────────────────────────
        cls_frm = tk.LabelFrame(body, text="  Class  ",
                                 font=("Segoe UI", 11, "bold"), fg=FG_GOLD,
                                 bg=BG_PANEL, bd=2, relief="groove")
        cls_frm.grid(row=0, column=1, sticky="nsew", padx=8, pady=4)

        self._class_var = tk.StringVar(value=CLASSES[0])
        ScrollableRadioFrame(cls_frm, CLASSES, self._class_var,
                              panel_bg=BG_PANEL).pack(fill="both", expand=True, padx=4, pady=4)
        self._class_var.trace_add("write", self._on_class_changed)

        ccf = tk.Frame(cls_frm, bg=BG_PANEL)
        ccf.pack(fill="x", padx=8, pady=(0, 8))
        tk.Radiobutton(ccf, text="Custom:", variable=self._class_var,
                       value="__custom_class__", font=("Segoe UI", 10),
                       bg=BG_PANEL, fg=FG_TEXT, activebackground=BG_PANEL,
                       selectcolor="#2a2a50", cursor="hand2").pack(side="left")
        self._custom_class = tk.Entry(ccf, font=("Segoe UI", 10), width=14,
                                       bg="#1e1e38", fg="white", insertbackground="white",
                                       relief="flat", bd=3)
        self._custom_class.pack(side="left", padx=4)
        self._custom_class.bind("<FocusIn>",
                                 lambda e: self._class_var.set("__custom_class__"))

        # ─ Stats column ──────────────────────────────────────────────────
        stat_frm = tk.LabelFrame(body, text="  Stats  ",
                                  font=("Segoe UI", 11, "bold"), fg=FG_GOLD,
                                  bg=BG_PANEL, bd=2, relief="groove")
        stat_frm.grid(row=0, column=2, sticky="nsew", padx=8, pady=4)

        self._rolled = {k: roll_stat() for k in STAT_KEYS}
        self._sv      = {}   # StringVar per stat
        self._sbars   = {}   # Progressbar per stat

        sgrid = tk.Frame(stat_frm, bg=BG_PANEL)
        sgrid.pack(fill="both", expand=True, padx=12, pady=8)
        sgrid.columnconfigure(0, weight=1)

        for i, key in enumerate(STAT_KEYS):
            full, desc = STAT_DEFS[key]
            tk.Label(sgrid, text=f"{key}  {full}",
                     font=("Segoe UI", 10, "bold"), fg=FG_GOLD, bg=BG_PANEL,
                     anchor="w").grid(row=i*3,   column=0, columnspan=2, sticky="w", pady=(8,0))
            tk.Label(sgrid, text=desc,
                     font=("Segoe UI", 8),  fg=FG_DIM, bg=BG_PANEL,
                     anchor="w").grid(row=i*3+1, column=0, columnspan=2, sticky="w")

            bar = ttk.Progressbar(sgrid, orient="horizontal", mode="determinate",
                                   style="Blue.Horizontal.TProgressbar", length=170)
            bar["maximum"] = 18
            bar["value"]   = self._rolled[key]
            bar.grid(row=i*3+2, column=0, sticky="ew", pady=2)
            self._sbars[key] = bar

            sv = tk.StringVar(value=str(self._rolled[key]))
            self._sv[key] = sv
            tk.Label(sgrid, textvariable=sv, font=("Consolas", 11, "bold"),
                     fg="white", bg=BG_PANEL, width=3,
                     anchor="center").grid(row=i*3+2, column=1, padx=(4, 0))

        self._total_sv = tk.StringVar()
        tk.Label(stat_frm, textvariable=self._total_sv,
                 font=("Segoe UI", 11, "bold"), fg=FG_GOLD, bg=BG_PANEL).pack(pady=(4, 2))

        self._btn(stat_frm, "🎲 Roll Stats", self._roll_stats,
                  bg="#2a3a7a", fg="white", font=("Segoe UI", 11, "bold"),
                  padx=16, pady=8).pack(pady=6)

        self._update_stat_display()

        # ─ Spell Preview column ──────────────────────────────────────────
        spell_frm = tk.LabelFrame(body, text="  Starting Spells  ",
                                   font=("Segoe UI", 11, "bold"), fg=FG_GOLD,
                                   bg=BG_PANEL, bd=2, relief="groove")
        spell_frm.grid(row=0, column=3, sticky="nsew", padx=8, pady=4)

        tk.Label(spell_frm,
                 text="Spells learned every 5 levels.\nFirst spells for this class:",
                 font=("Segoe UI", 8), fg=FG_DIM, bg=BG_PANEL,
                 justify="left").pack(anchor="w", padx=8, pady=(8, 4))

        self._spell_preview = tk.Text(
            spell_frm, state="disabled",
            font=("Consolas", 8), bg="#0d0d1e", fg="#88ddff",
            relief="flat", bd=0, wrap="word", height=16, width=28,
            padx=6, pady=4)
        self._spell_preview.pack(fill="both", expand=True, padx=6, pady=(0, 8))
        self._spell_preview.tag_configure("name",  foreground="#44ff88", font=("Consolas", 8, "bold"))
        self._spell_preview.tag_configure("tier",  foreground="#ffcc44", font=("Consolas", 7))
        self._spell_preview.tag_configure("desc",  foreground="#aaaacc", font=("Consolas", 7))
        self._spell_preview.tag_configure("cost",  foreground="#88ddff", font=("Consolas", 7))

        # ── bottom bar ────────────────────────────────────────────────────
        tk.Frame(self.root, bg="#333355", height=1).pack(fill="x", padx=24)
        bot = tk.Frame(self.root, bg=BG_DARK)
        bot.pack(fill="x", padx=28, pady=12)
        self._btn(bot, "⚔  Begin Quest!", self._begin_quest,
                  bg=BTN_GO, fg="white", font=("Segoe UI", 14, "bold"),
                  padx=28, pady=11).pack(side="right")

    def _roll_stats(self):
        for k in STAT_KEYS:
            self._rolled[k] = roll_stat()
        self._update_stat_display()

    def _update_stat_display(self):
        for k, v in self._rolled.items():
            self._sv[k].set(str(v))
            self._sbars[k]["value"] = v
        self._total_sv.set(f"Total: {sum(self._rolled.values())}")

    def _on_class_changed(self, *args):
        cls = self._class_var.get()
        if cls == "__custom_class__":
            self._affinity_frm.grid()
        else:
            self._affinity_frm.grid_remove()
            info = CLASS_STATS.get(cls, ("I", "L"))
            self._major_stat.set(f"{info[0]} - {STAT_DEFS[info[0]][0]}")
            self._minor_stat.set(f"{info[1]} - {STAT_DEFS[info[1]][0]}")

        # ── Populate spell preview ────────────────────────────────────────
        if not hasattr(self, "_spell_preview"):
            return
        primary, secondary = CLASS_STATS.get(cls, ("I", "L")) if cls != "__custom_class__" else ("I", "L")

        # Gather Minor + Major spells for primary stat, Minor for secondary
        preview_spells = []
        for stat, tiers in [(primary, ["Minor", "Major"]), (secondary, ["Minor"])]:
            for tier in tiers:
                pool = TIERED_SPELLS.get(stat, {}).get(tier, [])
                for name in pool[:2]:  # show up to 2 per bucket
                    sp = SPELL_BY_NAME.get(name)
                    if sp:
                        preview_spells.append((name, sp))

        widget = self._spell_preview
        widget.config(state="normal")
        widget.delete("1.0", "end")

        if not preview_spells:
            widget.insert("end", "No spells found for this class.\n", "desc")
        else:
            for name, sp in preview_spells:
                cost_str = f"{sp['mp_cost']} MP" if sp['mp_cost'] > 0 else "Passive"
                dur_str  = f"{sp['duration']}t" if sp['duration'] > 0 else "Instant"
                widget.insert("end", f"{name}\n", "name")
                widget.insert("end", f"[{sp['tier']}] {cost_str}  {dur_str}\n", "tier")
                widget.insert("end", f"{sp['description']}\n\n", "desc")

        widget.config(state="disabled")

    def _begin_quest(self):
        name = self._name_var.get().strip() or random_name()

        race = self._race_var.get()
        if race == "__custom_race__":
            race = self._custom_race.get().strip() or "Mysterious Being"

        cls = self._class_var.get()
        if cls == "__custom_class__":
            cls = self._custom_class.get().strip() or "Wanderer"
            self._pending_name = name
            self._pending_race = race
            self._pending_class = cls
            self._pending_stats = dict(self._rolled)
            self.show_affinity_screen()
            return

        info = CLASS_STATS.get(cls, ("I", "L"))
        self.start_game(name, race, cls, dict(self._rolled), info)

    def show_affinity_screen(self):
        self.clear_screen()

        hdr = tk.Frame(self.root, bg=BG_DARK)
        hdr.pack(fill="x", padx=24, pady=(18, 6))
        tk.Label(hdr, text="⚔  Stat Affinity",
                 font=("Courier New", 26, "bold"), fg=FG_GOLD, bg=BG_DARK).pack(side="left")
        self._btn(hdr, "← Back", self.new_character_screen,
                  font=("Segoe UI", 10), padx=10, pady=4).pack(side="right")
        tk.Frame(self.root, bg="#333355", height=1).pack(fill="x", padx=24)

        outer = tk.Frame(self.root, bg=BG_DARK)
        outer.pack(pady=40)

        tk.Label(outer, text=f"Class: {self._pending_class}",
               font=("Segoe UI", 14), fg=FG_GOLD, bg=BG_DARK).pack(pady=(0, 20))
        tk.Label(outer, text="Choose your stat affinities:",
               font=("Segoe UI", 12), fg=FG_TEXT, bg=BG_DARK).pack(pady=(0, 20))

        stat_vals = [f"{k} - {v[0]}" for k, v in STAT_DEFS.items()]

        frm = tk.Frame(outer, bg=BG_DARK)
        frm.pack(pady=20)

        tk.Label(frm, text="Major Stat:",
                font=("Segoe UI", 11), fg=FG_TEXT, bg=BG_DARK).grid(row=0, column=0, sticky="e", padx=10, pady=10)
        self._aff_major = tk.StringVar(value=stat_vals[0])
        ttk.Combobox(frm, textvariable=self._aff_major, values=stat_vals,
                    state="readonly", font=("Segoe UI", 11), width=16).grid(row=0, column=1, padx=10, pady=10)

        tk.Label(frm, text="Minor Stat:",
                font=("Segoe UI", 11), fg=FG_TEXT, bg=BG_DARK).grid(row=1, column=0, sticky="e", padx=10, pady=10)
        self._aff_minor = tk.StringVar(value=stat_vals[1])
        ttk.Combobox(frm, textvariable=self._aff_minor, values=stat_vals,
                    state="readonly", font=("Segoe UI", 11), width=16).grid(row=1, column=1, padx=10, pady=10)

        self._btn(outer, "⚔  Begin Quest!", self._finalizeCharacter,
                 bg=BTN_GO, fg="white", font=("Segoe UI", 14, "bold"),
                 padx=28, pady=11).pack(pady=30)

    def _finalizeCharacter(self):
        major = self._aff_major.get().split(" - ")[0]
        minor = self._aff_minor.get().split(" - ")[0]
        self.start_game(self._pending_name, self._pending_race, self._pending_class, self._pending_stats, (major, minor))

    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    #  LOAD CHARACTER SCREEN
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    def load_character_screen(self):
        self.clear_screen()

        hdr = tk.Frame(self.root, bg=BG_DARK)
        hdr.pack(fill="x", padx=24, pady=(18, 6))
        tk.Label(hdr, text="📂  Load Character",
                 font=("Courier New", 26, "bold"), fg=FG_GOLD, bg=BG_DARK).pack(side="left")
        self._btn(hdr, "← Menu", self.show_menu,
                  font=("Segoe UI", 10), padx=10, pady=4).pack(side="right")
        tk.Frame(self.root, bg="#333355", height=1).pack(fill="x", padx=24)

        saves = sorted(f for f in os.listdir(SAVES_DIR) if f.endswith(".json"))

        if not saves:
            tk.Label(self.root, text="\n\nNo saved characters found.\n\nCreate a new character to get started.",
                     font=("Segoe UI", 14), fg=FG_DIM, bg=BG_DARK).pack(pady=60)
            return

        # Scrollable save list
        canvas = tk.Canvas(self.root, bg=BG_DARK, borderwidth=0, highlightthickness=0)
        vsb    = ttk.Scrollbar(self.root, orient="vertical", command=canvas.yview)
        canvas.configure(yscrollcommand=vsb.set)
        vsb.pack(side="right", fill="y")
        canvas.pack(fill="both", expand=True, padx=24, pady=16)
        inner  = tk.Frame(canvas, bg=BG_DARK)
        win    = canvas.create_window((0, 0), window=inner, anchor="nw")
        inner.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.bind("<Configure>", lambda e: canvas.itemconfig(win, width=e.width))

        self._load_rows = inner  # keep ref

        for fname in saves:
            self._add_save_row(inner, fname)

    def _add_save_row(self, parent, fname):
        path = os.path.join(SAVES_DIR, fname)
        try:
            with open(path) as f:
                d = json.load(f)
            label = (f"  {d['name']}   Lv {d['lvl']} {d['race']} {d['class']}"
                     f"   |  Quests: {d.get('quests_completed', 0)}"
                     f"   |  Gold: {d.get('gold', 0)}"
                     f"   |  Deaths: {d.get('deaths', 0)}  ")
        except Exception:
            label = f"  {fname}  (unreadable)"

        row = tk.Frame(parent, bg=BG_ROW, bd=1, relief="groove")
        row.pack(fill="x", pady=5, padx=8)
        tk.Label(row, text=label, font=("Segoe UI", 12), fg=FG_TEXT,
                 bg=BG_ROW, anchor="w").pack(side="left", padx=10, pady=12)
        self._btn(row, "Delete", lambda p=path, r=row: self._delete_save(p, r),
                  bg=BTN_BAK, fg="#ffaaaa", font=("Segoe UI", 9),
                  padx=10, pady=4).pack(side="right", padx=6, pady=8)
        self._btn(row, "Load →", lambda p=path: self._load_file(p),
                  bg=BTN_GO, fg="white", font=("Segoe UI", 11, "bold"),
                  padx=14, pady=6).pack(side="right", padx=4, pady=8)

    def _load_file(self, path):
        try:
            with open(path) as f:
                data = json.load(f)
            self.start_game_from_save(data)
        except Exception as e:
            messagebox.showerror("Load Failed", str(e))

    def _delete_save(self, path, row):
        if messagebox.askyesno("Delete Save", "Permanently delete this save file?"):
            try:
                os.remove(path)
            except OSError:
                pass
            row.destroy()

    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    #  SAVE
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    def save_character(self):
        safe = "".join(c if c.isalnum() or c in "_ -" else "_"
                       for c in self.char["name"])
        path = os.path.join(SAVES_DIR, f"{safe}.json")
        try:
            with open(path, "w") as f:
                json.dump(self.char, f, indent=2)
            self.log_story(f"[SAVE] Saved to {path}", "vendor")
            messagebox.showinfo("Saved", f"'{self.char['name']}' saved successfully!")
        except Exception as e:
            messagebox.showerror("Save Failed", str(e))

    def save_and_quit(self):
        self.save_character()
        self.root.quit()

    def _confirm_menu(self):
        if messagebox.askyesno("Return to Menu",
                                "Return to main menu?\nUnsaved progress will be lost."):
            self.show_menu()

    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    #  GAME INIT
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    def start_game(self, name, race, char_class, stats, stat_affinity=None):
        hp = 20 + stats.get("E", 10) // 3
        mp = 10 + stats.get("I", 10) // 4

        if stat_affinity:
            custom_stats = dict(CLASS_STATS)
            custom_stats[char_class] = stat_affinity
            CLASS_STATS.update(custom_stats)

        self.char = {
            "name":  name,  "race":  race,  "class": char_class,
            "lvl":   1,     "exp":   0,     "exp_next": 100,
            "hp":    hp,    "max_hp": hp,
            "mp":    mp,    "max_mp": mp,
            "gold":  25,
            "stats": {k: stats.get(k, 10) for k in STAT_KEYS},
            "equip": {s: None for s in EQUIP_SLOTS},
            "inventory": [],
            "spells":    [],
            "active_effects": [],
            "deaths":    0,
            "quests_completed": 0,
            "prologue_done": False,
            "current_act": 0,
            "act_quests_done": 0,
            "in_boss_quest": False,
            "boss_attempts": 0,
            "completed_acts": [],
            "completed_quests": [],
            "prestige_level": 0,
            "current_title": "Vagabond",
            "title_history": [],
            "achievements": {
                "unlocked": {},
                "stats": {
                    "gold_earned":          0,
                    "gold_spent":           0,
                    "enemies_killed":       0,
                    "items_sold":           0,
                    "quests_completed":     0,
                    "world_resets":         0,
                    "bosses_defeated":      0,
                    "times_died":           0,
                    "progress_ticks":       0,
                    "actions_travel":       0,
                    "actions_fight":        0,
                    "actions_loot":         0,
                    "actions_search":       0,
                    "actions_rest":         0,
                    "max_level":            1,
                    "upgrades_total":       0,
                }
            },
        }
        self.char["equip"]["Weapon"] = {
            "name": "Rusty Dagger", "slot": "Weapon", "stat": "P", "bonus": 1, "power": 1, "weight": 1, "upgrade": 0
        }
        self.char["stats"]["P"] += 1

        starter_spell = generate_stat_spell(self.char)
        self.char["spells"].append(starter_spell)
        self._launch()

    def start_game_from_save(self, d):
        d.setdefault("quests_completed", 0)
        d.setdefault("deaths",           0)
        d.setdefault("spells",           [])
        d.setdefault("active_effects",   [])
        # pending_spell_damage is mid-fight transient — never restore from disk
        d.pop("pending_spell_damage", None)
        d.setdefault("equip",            {s: None for s in EQUIP_SLOTS})
        d.setdefault("prestige_level",   0)
        d.setdefault("current_title", "Vagabond")
        d.setdefault("title_history", [])
        d.setdefault("achievements", {"unlocked": {}, "stats": {}})
        # Ensure all stat keys exist for old saves
        _ach_defaults = {
            "gold_earned": 0, "gold_spent": 0, "enemies_killed": 0,
            "items_sold": 0, "quests_completed": 0, "world_resets": 0,
            "bosses_defeated": 0, "times_died": 0, "progress_ticks": 0,
            "actions_travel": 0, "actions_fight": 0, "actions_loot": 0,
            "actions_search": 0, "actions_rest": 0, "max_level": 1,
            "upgrades_total": 0,
        }
        for k, v in _ach_defaults.items():
            d["achievements"]["stats"].setdefault(k, v)
        self.char = d
        self._launch()

    def _launch(self):
        self._dead               = False
        self.quest_template      = None
        self.quest_steps         = []
        self.quest_step_index    = 0
        self.quest_total_steps   = 0
        self.current_action_type = None
        self._hist_descending    = False
        self._current_quest_name = None
        self._pending_transmute_tier = None
        self.clear_screen()
        self._build_ui()
        self._refresh_story_tree()
        self._refresh_hist_tree()
        self._update_act_bars()
        self._refresh_spell_list()
        self._refresh_equip_list()
        self._refresh_inv_list()
        self.start_new_quest()
        self.run_game_loop()

    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    #  GAME UI
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    def t(self, key):
        theme_name = self.theme.get() if hasattr(self, 'theme') else CURRENT_THEME
        return THEMES[theme_name].get(key, THEMES["Classic"].get(key, "#000000"))

    def _build_ui(self):
        tc = self.t
        self.root.configure(bg=tc("bg_dark"))

#  menu bar
        mb = tk.Menu(self.root, bg=tc("bg_panel"), fg=tc("fg_text"), activebackground=tc("btn_dark"))
        filemenu = tk.Menu(mb, tearoff=0, bg=tc("bg_panel"), fg=tc("fg_text"))
        filemenu.add_command(label="Save Character", command=self.save_character)
        filemenu.add_command(label="Save & Quit", command=self.save_and_quit)
        filemenu.add_separator()
        filemenu.add_command(label="Return to Menu", command=self._confirm_menu)
        filemenu.add_command(label="Exit", command=self.root.quit)
        mb.add_cascade(label="File", menu=filemenu)

        thememenu = tk.Menu(mb, tearoff=0, bg=tc("bg_panel"), fg=tc("fg_text"))
        for theme_name in THEMES:
            thememenu.add_radiobutton(label=theme_name, variable=self.theme,
                                    value=theme_name, command=self._change_theme)
        mb.add_cascade(label="Theme", menu=thememenu)

        devmenu = tk.Menu(mb, tearoff=0, bg=tc("bg_panel"), fg=tc("fg_text"))
        devmenu.add_command(label="Force Universe Reset", command=self._dev_force_reset)
        devmenu.add_command(label="Scale to Act 100 (Level Up)", command=self._dev_scale_to_act_100)
        devmenu.add_command(label="Add 10,000 Gold", command=self._dev_add_gold)
        devmenu.add_command(label="Add 100 XP", command=self._dev_add_xp)
        mb.add_cascade(label="Dev", menu=devmenu)

        self.root.configure(menu=mb)

# paned layout
        vpane = tk.PanedWindow(self.root, orient=tk.VERTICAL,  sashwidth=4, bg="#1a1a2e")
        vpane.pack(fill="both", expand=True)
        hpane = tk.PanedWindow(vpane,     orient=tk.HORIZONTAL, sashwidth=4, bg="#1a1a2e")
        self._hpane = hpane
        vpane.add(hpane, stretch="always")

        hpane.columnconfigure(0, weight=1)
        hpane.columnconfigure(1, weight=6)
        hpane.columnconfigure(2, weight=1)

        # ─ Col 1: CHARACTER SHEET ───────────────────────────────────────────────
        c1 = tk.PanedWindow(hpane, orient=tk.VERTICAL, sashwidth=2, bg="#1a1a2e")
        hpane.add(c1, width=220)

        ft = ttk.LabelFrame(c1, text=" TRAITS ", padding=2)
        self.info_label = ttk.Label(ft, text="", font=("Consolas", 9), justify="left")
        self.info_label.pack(padx=4, pady=2, anchor="w")
        c1.add(ft, height=90)

        fs = ttk.LabelFrame(c1, text=" STATS ", padding=2)
        self.stat_tree = ttk.Treeview(fs, columns=("K","V","D"), show="headings", height=7)
        self.stat_tree.heading("K", text="Stat")
        self.stat_tree.heading("V", text="Val")
        self.stat_tree.heading("D", text="Desc")
        self.stat_tree.column("K", width=30, anchor="center")
        self.stat_tree.column("V", width=30, anchor="center")
        self.stat_tree.column("D", width=70, anchor="w")
        self.stat_tree.pack(fill="both", expand=True)
        for s in STAT_KEYS:
            self.stat_tree.insert("", "end", iid=s, values=(s, self.char["stats"][s], STAT_DEFS[s][0]))
        c1.add(fs, height=210)
        self._refresh_stat_tree()

        # ── stat tooltip ─────────────────────────────────────────────────
        self._stat_tip = tk.Toplevel(self.root)
        self._stat_tip.withdraw()
        self._stat_tip.overrideredirect(True)
        self._stat_tip.configure(bg="#1a1a2e")
        tk.Frame(self._stat_tip, bg="#00aa00", bd=1).place(relx=0, rely=0, relwidth=1, relheight=1)
        self._stat_tip_lbl = tk.Label(self._stat_tip, text="", font=("Consolas", 9, "bold"),
                                      bg="#0a0a1e", fg=FG_GOLD, justify="left",
                                      padx=8, pady=5)
        self._stat_tip_lbl.pack(padx=1, pady=1)

        def _stat_tip_show(event):
            row = self.stat_tree.identify_row(event.y)
            if row and row in STAT_DEFS:
                desc = STAT_DEFS[row][1]
                self._stat_tip_lbl.config(text=desc)
                self._stat_tip.deiconify()
                self._stat_tip.lift()
            else:
                self._stat_tip.withdraw()

        def _stat_tip_move(event):
            if self._stat_tip.winfo_exists() and self._stat_tip.winfo_viewable():
                self._stat_tip.geometry(f"+{event.x_root + 14}+{event.y_root - 10}")

        def _stat_tip_hide(event):
            self._stat_tip.withdraw()

        self.stat_tree.bind("<Motion>",  _stat_tip_show)
        self.stat_tree.bind("<Motion>",  _stat_tip_move, add="+")
        self.stat_tree.bind("<Leave>",   _stat_tip_hide)

        def bar_row(parent, lbl, style):
            row = ttk.Frame(parent)
            row.pack(fill="x", padx=4, pady=1)
            ttk.Label(row, text=lbl, font=("Consolas", 8), width=3).pack(side="left")
            bar = ttk.Progressbar(row, orient="horizontal", mode="determinate", style=style, length=80)
            bar.pack(side="left", fill="x", expand=True, padx=(2, 0))
            lv = ttk.Label(row, text="", font=("Consolas", 8), width=10)
            lv.pack(side="left", padx=2)
            return bar, lv

        fb = ttk.LabelFrame(c1, text="", padding=2)
        self.xp_bar, self.xp_lbl = bar_row(fb, "XP", "XP.Horizontal.TProgressbar")
        self.hp_bar, self.hp_lbl = bar_row(fb, "HP", "HP.Horizontal.TProgressbar")
        self.mp_bar, self.mp_lbl = bar_row(fb, "MP", "MP.Horizontal.TProgressbar")
        self.enc_bar, self.enc_lbl = bar_row(fb, "ENC", "Gold.Horizontal.TProgressbar")
        self.enc_bar["maximum"] = 100
        c1.add(fb, height=110)

        fsp = ttk.LabelFrame(c1, text=" SPELLS/SKILLS ", padding=2)
        self.spell_list = tk.Listbox(fsp, font=("Consolas", 8), bg="#0d0d1e", fg="#88ddff", selectbackground="#223344", height=3)
        self.spell_list.pack(fill="both", expand=True)
        c1.add(fsp)

        # ── Spell tooltip (same pattern as stat_tree tooltip) ──────────────
        self._spell_tip = tk.Toplevel(self.root)
        self._spell_tip.withdraw()
        self._spell_tip.overrideredirect(True)
        self._spell_tip.configure(bg="#1a1a2e")
        self._spell_tip_lbl = tk.Label(
            self._spell_tip, text="", font=("Consolas", 8),
            bg="#1a1a2e", fg="#aaddff", justify="left",
            wraplength=280, padx=6, pady=4)
        self._spell_tip_lbl.pack()

        def _spell_tip_show(event):
            idx = self.spell_list.nearest(event.y)
            if idx < 0 or idx >= self.spell_list.size():
                self._spell_tip.withdraw()
                return
            raw = self.spell_list.get(idx)
            # Strip active-effect annotation to get base name
            name = raw.split("  [")[0].strip()
            sp = SPELL_BY_NAME.get(name)
            if sp:
                tier    = sp["tier"]
                cost    = sp["mp_cost"]
                dur     = sp["duration"]
                dur_str = f"{dur} actions" if dur > 0 else "instant"
                cost_str = f"{cost} MP" if cost > 0 else "passive"
                lines = [
                    f"{name}  [{tier}]",
                    f"Cost: {cost_str}   Duration: {dur_str}",
                    f"Effect: {sp['effect_type'].replace('_', ' ')}",
                    "",
                    sp["description"],
                ]
                self._spell_tip_lbl.config(text="\n".join(lines))
                self._spell_tip.deiconify()
                self._spell_tip.lift()
            else:
                self._spell_tip.withdraw()

        def _spell_tip_move(event):
            if self._spell_tip.winfo_exists() and self._spell_tip.winfo_viewable():
                self._spell_tip.geometry(f"+{event.x_root + 14}+{event.y_root - 10}")

        def _spell_tip_hide(event):
            self._spell_tip.withdraw()

        self.spell_list.bind("<Motion>",  _spell_tip_show)
        self.spell_list.bind("<Motion>",  _spell_tip_move, add="+")
        self.spell_list.bind("<Leave>",   _spell_tip_hide)

        # ─ Col 2: Equipment + Inventory ───────────────────────────────────────
        c2 = tk.PanedWindow(hpane, orient=tk.VERTICAL, sashwidth=2, bg="#1a1a2e")
        hpane.add(c2, width=900)

        feq = ttk.LabelFrame(c2, text=" Equipment ", padding=2)
        self.equip_list = tk.Listbox(feq, font=("Consolas", 8), bg="#0d0d1e", fg="#ddcc88", selectbackground="#334422", height=6)
        self.equip_list.pack(fill="both", expand=True)
        c2.add(feq, height=160)
        self._refresh_equip_list()

        fiv = ttk.LabelFrame(c2, text=" INVENTORY ", padding=2)
        self.inv_list = tk.Listbox(fiv, font=("Consolas", 8), bg="#0d0d1e", fg="#aaffaa", selectbackground="#224433", height=12)
        self.inv_list.pack(fill="both", expand=True)
        c2.add(fiv)

        # ─ Col 3: STORY + QUESTS ───────────────────────────────────────────
        c3 = tk.PanedWindow(hpane, orient=tk.VERTICAL, sashwidth=2, bg="#1a1a2e")
        self._c3 = c3
        hpane.add(c3, width=260)

        f_story = ttk.LabelFrame(c3, text=" STORY ", padding=2)
        story_scroll = ttk.Scrollbar(f_story, orient="vertical")
        story_scroll.pack(side="right", fill="y")
        self.story_tree = ttk.Treeview(f_story, columns=("S","N"), show="headings", height=8, yscrollcommand=story_scroll.set)
        self.story_tree.heading("S", text="")
        self.story_tree.heading("N", text="Name")
        self.story_tree.column("S", width=20, anchor="center")
        self.story_tree.column("N", width=200, anchor="w")
        self.story_tree.pack(fill="both", expand=True)
        story_scroll.config(command=self.story_tree.yview)
        c3.add(f_story, height=160)

        f_act_prog = ttk.LabelFrame(c3, text=" ACT PROGRESS ", padding=2)
        self.act_pbar = ttk.Progressbar(f_act_prog, orient="horizontal", mode="determinate", style="Gold.Horizontal.TProgressbar")
        self.act_pbar["maximum"] = QUESTS_PER_ACT
        self.act_pbar.pack(fill="x", padx=5, pady=2)
        self.act_label = ttk.Label(f_act_prog, text="Prologue", font=("Consolas", 9, "bold"))
        self.act_label.pack(pady=1)
        c3.add(f_act_prog, height=55)

        f_hist = ttk.LabelFrame(c3, text=" QUEST HISTORY ", padding=2)
        hdr = tk.Frame(f_hist, bg=BG_PANEL)
        hdr.pack(fill="x", padx=2, pady=2)
        tk.Button(hdr, text="⇅", command=self._toggle_hist_order, font=("Consolas", 8),
                bg=BTN_DARK, fg=FG_TEXT, width=2).pack(side="left")
        hist_scroll = ttk.Scrollbar(f_hist, orient="vertical")
        hist_scroll.pack(side="right", fill="y")
        self.hist_tree = ttk.Treeview(f_hist, columns=("S","Q"), show="headings", height=6, yscrollcommand=hist_scroll.set)
        self.hist_tree.heading("S", text="")
        self.hist_tree.heading("Q", text="Quest")
        self.hist_tree.column("S", width=20, anchor="center")
        self.hist_tree.column("Q", width=210)
        self.hist_tree.pack(fill="both", expand=True)
        hist_scroll.config(command=self.hist_tree.yview)
        c3.add(f_hist, stretch="always")

        f_qprog = tk.Frame(c3, bg="#0a0a18")
        tk.Label(f_qprog, text="QUEST PROGRESS", font=("Consolas", 7, "bold"),
                 bg="#0a0a18", fg=FG_GOLD, anchor="w").pack(fill="x", padx=6, pady=(4, 1))
        self.quest_pbar = ttk.Progressbar(f_qprog, orient="horizontal", mode="determinate",
                                          style="XP.Horizontal.TProgressbar")
        self.quest_pbar["maximum"] = 1
        self.quest_pbar["value"]   = 0
        self.quest_pbar.pack(fill="x", padx=6, pady=(0, 4))
        c3.add(f_qprog, height=40)

        # ─ Bottom: STORY OUTPUT ─────────────────────────────────────────
        bot = tk.Frame(vpane, bg="#0a0a18")
        vpane.add(bot, height=180)

        fst = tk.Frame(bot, bg="#08080f")
        fst.pack(fill="both", expand=True)
        self.story_text = tk.Text(fst, state="disabled", font=("Consolas", 8), bg="#08080f", fg="#cccccc", wrap="word")
        sb2 = ttk.Scrollbar(fst, command=self.story_text.yview)
        self.story_text.configure(yscrollcommand=sb2.set)
        sb2.pack(side="right", fill="y")
        self.story_text.pack(fill="both", expand=True)
        for tag, col, style in [("death", "#ff4455", "bold"), ("ghost", "#aa88ff", "italic"), ("level", "#44ff88", "bold"), ("quest", "#ffcc44", "bold"), ("vendor", "#44ddff", "bold"), ("normal", "#cccccc", "")]:
            self.story_text.tag_configure(tag, foreground=col, font=("Consolas", 8, style) if style else ("Consolas", 8))

        # ─ Bottom: CURRENT ACTION BAR ──────────────────────────────────────
        bottom = tk.Frame(vpane, bg="#0a0a18", height=50)
        vpane.add(bottom, height=50)
        self.task_label = tk.Label(bottom, text="Preparing...", font=("Arial", 9), bg="#0a0a18", fg="#cccccc")
        self.task_label.pack(pady=(4, 1))
        self.pbar = ttk.Progressbar(bottom, orient="horizontal", mode="determinate", style="Blue.Horizontal.TProgressbar")
        self.pbar.pack(fill="x", padx=20, pady=1)

        self._update_char_panel()
        self.root.after(50, self._set_sash_positions)

    def _set_sash_positions(self):
        """Force column widths after the window has fully rendered."""
        total = self._hpane.winfo_width()
        if total < 100:
            self.root.after(50, self._set_sash_positions)
            return
        col1 = 220
        col3 = 260
        col2 = total - col1 - col3
        self._hpane.sash_place(0, col1, 0)
        self._hpane.sash_place(1, col1 + col2, 0)

    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    #  QUEST MANAGEMENT
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    def start_new_quest(self):
        self._check_boss_death_restart()

        max_cap = get_max_capacity(self.char["stats"])
        current_weight = get_inventory_weight(self.char["inventory"])
        encumbrance = (current_weight / max_cap * 100) if max_cap > 0 else 100

        if encumbrance >= 100:
            # Check if the character has a transmute spell and roll to use it
            if self._can_transmute_in_field():
                self._inject_transmute_quest()
            else:
                self._inject_market_quest()
            return

        if not self.char["prologue_done"]:
            self._prologue_quest()
        elif self.char["in_boss_quest"]:
            self._boss_quest()
        else:
            act_done = self.char["act_quests_done"]
            if act_done >= QUESTS_PER_ACT:
                self._start_boss()
            else:
                self._regular_quest()

        self._update_act_bars()

    def _check_boss_death_restart(self):
        if self.char["in_boss_quest"] and self.char["boss_attempts"] > 0:
            self.char["in_boss_quest"] = False
            self.char["boss_attempts"] = 0
            self.log_story("  [BOSS] You were defeated... restarting the trial.", "death")

    def _prologue_quest(self):
        idx = self.char["quests_completed"]
        if idx >= PROLOGUE_COMPLETE:
            self.char["prologue_done"] = True
            self.char["current_act"] = 1
            self.char["act_quests_done"] = 0
            self.log_story("★ PROLOGUE COMPLETE! Act 101: The Beginning II begins...", "level")
            self._regular_quest()
            return
        tmpl = PROLOGUE_QUESTS[idx]
        self._start_quest(tmpl)

    def _start_boss(self):
        self.char["in_boss_quest"] = True
        self.char["boss_attempts"] = 0
        if self.char["current_act"] == 99:
            tmpl = {"name": "The Final Battle", "steps": [("travel", 8), ("fight", 25), ("loot", 6), ("return", 1)]}
        else:
            act_idx = (self.char["current_act"] - 1) % len(BOSS_QUESTS)
            tmpl = BOSS_QUESTS[act_idx]
        self.log_story(f"⚠ BOSS: {tmpl['name']} appears!", "death")
        self._start_quest(tmpl)

    def _start_special_quest(self, special_type):
        if special_type == "world_reset":
            tmpl = {"name": "Resetting the Universe",
                    "steps": [("travel", 3), ("fight", 3), ("search", 3), ("return", 1)]}
        else:
            return
        self._start_quest(tmpl)

    def _boss_quest(self):
        self.char["boss_attempts"] += 1

    def _reset_universe(self):
        self.char["prestige_level"] = self.char.get("prestige_level", 0) + 1
        self._ach_stat("world_resets", 1)
        self._check_achievements()
        pl = self.char["prestige_level"]
        self.char["current_act"] = 1
        self.char["act_quests_done"] = 0
        self.char["gold"] = 0
        self.char["inventory"] = []
        self.char["completed_quests"] = []
        self.char["quests_completed"] = 0
        self.quest_template = None
        self.quest_steps = []
        self.quest_step_index = 0
        self._current_quest_name = None
        self.char["in_boss_quest"] = False
        self.char["boss_attempts"] = 0
        self.char["equip"] = {s: None for s in EQUIP_SLOTS}
        for slot in ["Weapon", "Shield", "Helm", "Body", "Legs", "Ring", "Amulet"]:
            self.char["equip"][slot] = None
        # Clear all active spell effects — buffs don't survive a reset
        for eff in self.char.get("active_effects", []):
            if eff["effect_type"] == "stat_buff":
                key = eff.get("stat_key", "")
                if key and key in self.char["stats"]:
                    self.char["stats"][key] -= eff["magnitude"]
        self.char["active_effects"] = []
        self.char.pop("pending_spell_damage", None)
        self._pending_transmute_tier = None

        old_title = self.char.get("current_title", "Vagabond")
        new_title = get_current_title(pl)
        self.char["current_title"] = new_title
        if "title_history" not in self.char:
            self.char["title_history"] = []
        self.char["title_history"].append(old_title)
        
        self._refresh_equip_list()
        self._refresh_inv_list()
        self._update_gold()
        self._update_act_bars()
        self._update_char_panel()
        self._refresh_stat_tree()
        self._refresh_story_tree()
        self._refresh_hist_tree()
        
        displayed_act = (pl * 100) + 1
        roman_suffix = f" {to_roman(pl+1)}" if pl > 0 else ""
        self.log_story("★ UNIVERSE RESET! Everything begins anew...", "level")
        self.log_story(f"  Prestige Level: {pl}", "level")
        self.log_story(f"  Previous Title: {old_title}", "level")
        self.log_story(f"  New Title: {new_title}", "level")
        self.log_story(f"  Act {displayed_act}: The Beginning{roman_suffix} begins!", "level")
        
        self._regular_quest()
        self.run_game_loop()

    def _start_quest(self, tmpl):
        self.quest_template = tmpl
        self._current_quest_name = tmpl["name"]
        self.quest_steps = [atype for atype, n in tmpl["steps"] for _ in range(n)]
        self.quest_step_index = 0
        self.quest_total_steps = len(self.quest_steps)
        self._refresh_hist_tree()
        self.quest_pbar["maximum"] = max(1, self.quest_total_steps)
        self.quest_pbar["value"]   = 0

        ptype = "PROLOGUE" if not self.char["prologue_done"] else "BOSS" if self.char["in_boss_quest"] else "QUEST"
        self.log_story(f"[{ptype}] {tmpl['name']}", "quest")
        self._advance_to_next_step()

    def _regular_quest(self):
        tmpl = random.choice(QUEST_TEMPLATES)
        self._start_quest(tmpl)

    def _update_act_bars(self):
        if self.char["prologue_done"]:
            prestige = self.char.get("prestige_level", 0)
            act = self.char["current_act"]
            display_act = (prestige * 100) + act
            act_name = get_act_name(act)
            self.act_label.config(text=f"Act {display_act}: {act_name}")
            self.act_pbar["maximum"] = QUESTS_PER_ACT
            self.act_pbar["value"] = self.char["act_quests_done"]
        else:
            self.act_label.config(text="Prologue")
            self.act_pbar["maximum"] = PROLOGUE_COMPLETE
            self.act_pbar["value"] = self.char["quests_completed"]

    def _can_transmute_in_field(self):
        """
        Returns (spell_name, spell_def) if the character has a transmute spell
        and the random roll succeeds, else False.
        Higher-tier transmute spells have better odds of firing.
        """
        char = self.char
        transmute_spells = [
            (name, SPELL_BY_NAME[name])
            for name in char.get("spells", [])
            if SPELL_BY_NAME.get(name, {}).get("effect_type") == "transmute"
        ]
        if not transmute_spells:
            return False
        # Pick the highest-tier spell available
        tier_order = {"Minor": 0, "Major": 1, "II": 2, "III": 3}
        best_name, best_sp = max(
            transmute_spells, key=lambda x: tier_order.get(x[1]["tier"], 0))
        # Roll chance: Minor 40%, Major 55%, II 70%, III 88%
        tier_chances = {"Minor": 0.40, "Major": 0.55, "II": 0.70, "III": 0.88}
        chance = tier_chances.get(best_sp["tier"], 0.40)
        # Also requires enough MP
        if char["mp"] < best_sp["mp_cost"]:
            return False
        if random.random() < chance:
            return (best_name, best_sp)
        return False

    def _inject_transmute_quest(self):
        """
        In-field transmutation instead of a market trip.
        One transmute step per inventory item; no travel or restore.
        """
        char = self.char
        result = self._can_transmute_in_field()
        if not result:
            self._inject_market_quest()
            return
        spell_name, spell_def = result
        tier = spell_def["tier"]
        inv_count = len(char["inventory"])
        eff = transmute_efficiency(tier, char["stats"].get("I", 10))

        self.quest_template   = {"name": "Field Transmutation"}
        self.quest_steps      = []
        for _ in range(inv_count):
            self.quest_steps.append("transmute")
        self.quest_step_index  = 0
        self.quest_total_steps = len(self.quest_steps)

        # Deduct MP for the casting
        char["mp"] = max(0, char["mp"] - spell_def["mp_cost"])
        self._pending_transmute_tier = tier

        self.log_story(
            f"✦ [{spell_name}] Encumbered — transmuting in-field! "
            f"({int(eff*100)}% rate, {inv_count} items)",
            "level")
        self._ach_stat("transmutes_performed", inv_count)
        self._ach_stat("spells_cast", 1)
        self._update_char_panel()
        self.quest_pbar["maximum"] = max(self.quest_total_steps, 1)
        self.quest_pbar["value"]   = 0
        self._advance_to_next_step()

    def _inject_market_quest(self):
        max_cap = get_max_capacity(self.char["stats"])
        current_weight = get_inventory_weight(self.char["inventory"])
        encumbrance = int(100 * current_weight / max_cap) if max_cap > 0 else 100
        self.quest_template    = {"name": "Market Day"}
        self.quest_steps       = ["travel", "find_vendor"]
        for _ in range(len(self.char["inventory"])):
            self.quest_steps.append("sell")
        if len(self.char["inventory"]) > 0:
            self.quest_steps.append("restore")
        for _ in range(len(EQUIP_SLOTS)):
            self.quest_steps.append("upgrade")
        self.quest_step_index  = 0
        self.quest_total_steps = len(self.quest_steps)
        self.log_story(f"[MARKET] Encumbered ({encumbrance}%) — heading to market.", "vendor")
        self.quest_pbar["maximum"] = self.quest_total_steps
        self.quest_pbar["value"]   = 0
        self._advance_to_next_step()

    def _trigger_emergency_return(self):
        if self.char.get("in_emergency_return", False):
            return
        self.char["in_emergency_return"] = True

        current_step = self.quest_step_index
        total_steps = self.quest_total_steps
        steps_remaining = total_steps - current_step
        steps_done = current_step

        self.log_story(f"[!] ENCUMBERED! Returning to town...", "vendor")
        self.log_story(f"  Return journey: {steps_remaining} steps to town.", "vendor")

        self.saved_quest_state = {
            "template": self.quest_template,
            "steps": self.quest_steps,
            "step_index": self.quest_step_index,
            "total_steps": self.quest_total_steps,
            "current_action_type": self.current_action_type,
        }

        self.quest_template = {"name": "Return to Town"}
        return_seconds = steps_remaining * 8
        return_steps = max(1, return_seconds // 8)
        self.quest_steps = ["return_town"] * return_steps
        self.quest_step_index = 0
        self.quest_total_steps = len(self.quest_steps)
        self.log_story(f"  [SLOW RETURN] {return_steps} steps back to town ({return_seconds}s)...", "vendor")

        self.quest_pbar["maximum"] = self.quest_total_steps
        self.quest_pbar["value"] = 0

    def _complete_emergency_return(self):
        self.log_story("  [TOWN] Made it back to town. Selling loot...", "vendor")

        self.quest_template = {"name": "Market Day"}
        self.quest_steps = ["find_vendor"]
        for _ in range(len(self.char["inventory"])):
            self.quest_steps.append("sell")
        if len(self.char["inventory"]) > 0:
            self.quest_steps.append("restore")
        for _ in range(len(EQUIP_SLOTS)):
            self.quest_steps.append("upgrade")

        self.quest_step_index = 0
        self.quest_total_steps = len(self.quest_steps)
        self.quest_pbar["maximum"] = self.quest_total_steps
        self.quest_pbar["value"] = 0

        self._advance_to_next_step()

    def _complete_market_after_return(self):
        saved = self.saved_quest_state
        steps_done = saved.get("step_index", 0)

        self.log_story(f"  [RETURN] Heading back to quest...", "vendor")

        rejoin_seconds = steps_done * 8
        rejoin_steps = max(1, rejoin_seconds // 8)
        self.quest_template = {"name": "Return to Quest"}
        self.quest_steps = ["travel"] * rejoin_steps
        self.quest_step_index = 0
        self.quest_total_steps = len(self.quest_steps)
        self.log_story(f"  [SLOW RETURN] {rejoin_steps} steps back to quest ({rejoin_seconds}s)...", "vendor")

        self.quest_pbar["maximum"] = self.quest_total_steps
        self.quest_pbar["value"] = 0
        self._advance_to_next_step()

    def _resume_original_quest(self):
        self.log_story("  [RESUME] Resuming original quest...", "quest")
        saved = self.saved_quest_state
        self.quest_template = saved.get("template")
        self.quest_steps = saved.get("steps", [])
        self.quest_total_steps = saved.get("total_steps", 1)
        self.quest_step_index = saved.get("step_index", 0)
        self.char["in_emergency_return"] = False
        self.saved_quest_state = None

        self.quest_pbar["maximum"] = self.quest_total_steps
        self.quest_pbar["value"] = self.quest_step_index

        self._advance_to_next_step()

    def _apply_market_loop(self):
        max_cap = get_max_capacity(self.char["stats"])
        current_weight = get_inventory_weight(self.char["inventory"])
        encumbrance = int(100 * current_weight / max_cap) if max_cap > 0 else 100

        self.log_story(f"  [MARKET] Arrived at market. Encumbrance: {encumbrance}% / {max_cap} cap")

        total_gold = 0
        for item in self.char["inventory"]:
            value = item_sell_value(item, self.char["stats"]["L"])
            total_gold += value
            self.log_story(f"    SOLD: {item_display(item)} -> {value} gold", "vendor")

        self.char["gold"] += total_gold
        self.log_story(f"  Total: {total_gold} gold from {len(self.char['inventory'])} items.", "vendor")
        self.char["inventory"].clear()
        self._update_gold()

        hp_missing = self.char["max_hp"] - self.char["hp"]
        mp_missing = self.char["max_mp"] - self.char["mp"]
        spend = 0

        if hp_missing > 0:
            hp_heal = min(hp_missing, total_gold // 3)
            hp_cost = hp_heal
            spend += hp_cost
            self.char["hp"] = min(self.char["max_hp"], self.char["hp"] + hp_heal)
            self.log_story(f"    Healed {hp_heal} HP ({hp_cost} gold)")

        if mp_missing > 0 and total_gold - spend > 0:
            mp_heal = min(mp_missing, (total_gold - spend) // 2)
            mp_cost = mp_heal
            self.char["mp"] = min(self.char["max_mp"], self.char["mp"] + mp_heal)
            self.log_story(f"    Recovered {mp_heal} MP ({mp_cost} gold)")
            spend += mp_cost

        remaining_gold = self.char["gold"]

        for slot in EQUIP_SLOTS:
            current_item = self.char["equip"].get(slot)
            current_power = item_stat_power(current_item) if current_item else 0

            best_candidate = None
            best_candidate_power = 0

            for _ in range(15):
                candidate = generate_item(self.char["lvl"], allow_stacked_prefix=False)
                if candidate["slot"] != slot:
                    continue
                candidate_power = item_stat_power(candidate)
                if candidate_power > current_power:
                    cost = item_buy_value(candidate, self.char["stats"]["L"])
                    if cost <= remaining_gold and candidate_power > best_candidate_power:
                        best_candidate = candidate
                        best_candidate_power = candidate_power
                        best_candidate_cost = cost

            if best_candidate and best_candidate_power > current_power:
                old_item = self.char["equip"].get(slot)
                if old_item:
                    self.char["stats"][old_item["stat"]] -= old_item["bonus"]

                self.char["stats"][best_candidate["stat"]] += best_candidate["bonus"]
                remaining_gold -= best_candidate_cost

                old_display = item_display(old_item) if old_item else "---"
                self.log_story(f"    UPGRADED [{slot}]: {old_display} -> {item_display(best_candidate)} ({best_candidate_cost} gold)", "vendor")

                best_candidate["weight"] = 1 + (best_candidate.get("power", 1) // 5)
                self.char["equip"][slot] = best_candidate

        self.char["gold"] = remaining_gold
        self.log_story(f"  Remaining gold: {remaining_gold}", "vendor")

        new_weight = get_inventory_weight(self.char["inventory"])
        new_encumbrance = int(100 * new_weight / max_cap) if max_cap > 0 else 0
        self.log_story(f"  Encumbrance now: {new_encumbrance}%", "vendor")

        self._update_gold()
        self._refresh_inv_list()
        self._update_char_panel()
        self._refresh_equip_list()

    def _advance_to_next_step(self):
        if self.quest_step_index < len(self.quest_steps):
            self.current_action_type = self.quest_steps[self.quest_step_index]
            self.pbar["value"]       = 0
            self.task_label.config(
                text=ACTION_LABELS.get(self.current_action_type, "Working..."))
            self._update_step_label()
            self.quest_pbar["value"] = self.quest_step_index
        else:
            self.quest_pbar["value"] = self.quest_total_steps
            if self.char.get("in_emergency_return"):
                if self.quest_template.get("name") == "Return to Town":
                    self._complete_emergency_return()
                elif self.quest_template.get("name") == "Market Day":
                    self._complete_market_after_return()
                elif self.quest_template.get("name") == "Return to Quest":
                    self._resume_original_quest()
                else:
                    self._complete_quest()
            else:
                self._complete_quest()

    def _update_step_label(self):
        done  = self.quest_step_index
        total = self.quest_total_steps
        atype = (self.current_action_type or "").replace("_", " ")
        self.task_label.config(text=f"{self.quest_template['name']}: {atype.capitalize()} ({done+1}/{total})")

    def _complete_quest(self):
        if getattr(self, '_quest_completing', False):
            return
        self._quest_completing = True
        
        if self.quest_template.get("name") == "Resetting the Universe":
            self._reset_universe()
            self._quest_completing = False
            return
        if self.quest_template.get("name") != "Visit the Vendor":
            self._current_quest_name = None

            xp_r   = self.char["lvl"] * 40 + random.randint(10, 30)
            gold_r  = self.char["lvl"] * 10 + random.randint(5, 20)

            if self.char["in_boss_quest"]:
                self.char["in_boss_quest"] = False
                self.char["current_act"] += 1
                self._ach_stat("bosses_defeated", 1)
                if self.char["current_act"] == 100:
                    pr = self.char.get("prestige_level", 0)
                    displayed_act = (pr * 100) + 100
                    self.log_story(f"★ BOSS DEFEATED! Act {displayed_act}: Resetting the Universe begins!", "level")
                    self.char["act_quests_done"] = 0
                    self._start_special_quest("world_reset")
                    gold_r *= 3
                    xp_r *= 2
                else:
                    self.char["act_quests_done"] = 0
                    pr = self.char.get("prestige_level", 0)
                    displayed_act = (pr * 100) + self.char["current_act"] + 1
                    self.log_story(f"★ BOSS DEFEATED! Act {displayed_act} begins!", "level")
                    gold_r *= 3
                    xp_r *= 2
            else:
                self.char["quests_completed"] += 1
                self._ach_stat("quests_completed", 1)
                q_name = self.quest_template["name"]
                if "completed_quests" not in self.char:
                    self.char["completed_quests"] = []
                self.char["completed_quests"].append(q_name)
                if self.char["prologue_done"]:
                    self.char["act_quests_done"] += 1

            self.char["gold"] += gold_r
            self._ach_stat("gold_earned", gold_r)
            self.log_story(f"[QUEST DONE] {self.quest_template['name']}", "quest")
            self.log_story(f"  Reward: {xp_r} XP, {gold_r} gold.")
            self._gain_xp(xp_r)
            self._update_gold()
            self._refresh_story_tree()
            self._refresh_hist_tree()
            self._update_act_bars()
            self._update_char_panel()
            self._check_achievements()
            self.log_story("  [SCOUT] Searching for new quest...")
        self.pbar["value"] = 0
        self.task_label.config(text="Scouting for new quest...")
        total_delay = random.randint(600, 10000)
        step_delay = 30
        steps = min(100, total_delay // step_delay)
        self._animate_new_quest(steps, step_delay)

    def _animate_new_quest(self, remaining, step_delay):
        if remaining > 0:
            self.root.after(step_delay, lambda: self._animate_new_quest(remaining - 1, step_delay))
            self.pbar["value"] = 100 - remaining
        else:
            self.pbar["value"] = 100
            self.start_new_quest()
            self._quest_completing = False

    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    #  GAME LOOP
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    def run_game_loop(self):
        if self._dead:
            return
        try:
            if not self.pbar.winfo_exists():
                return
        except:
            return
        speed = max(50, 250 - self.char["stats"]["D"] * 2)
        if self.pbar["value"] >= 100:
            self.pbar["value"] = 0
            self._complete_action()
            self.quest_step_index += 1
            self._check_encumbrance()
            self._advance_to_next_step()
        else:
            self.pbar["value"] += 2
        self.root.after(speed, self.run_game_loop)

    def _check_encumbrance(self):
        if self.char.get("in_emergency_return", False):
            return
        try:
            if not self.pbar.winfo_exists():
                return
        except:
            return
        max_cap = get_max_capacity(self.char["stats"])
        current_weight = get_inventory_weight(self.char["inventory"])
        pct = int(100 * current_weight / max_cap) if max_cap > 0 else 100
        if pct >= 100:
            self._trigger_emergency_return()

    def _complete_action(self):
        atype  = self.current_action_type
        flavor = random.choice(ACTION_FLAVORS.get(atype, ["Did something."]))
        self.log_story(f"  {flavor}")

        # ── Achievement stat tracking ─────────────────────────────────────────
        self._ach_stat("progress_ticks", 1)
        if atype == "travel":
            self._ach_stat("actions_travel", 1)
        elif atype == "loot":
            self._ach_stat("actions_loot", 1)
        elif atype in ("search","locate","scout","investigate",
                       "gather","escort","inspect","collect","speak"):
            self._ach_stat("actions_search", 1)
        elif atype == "rest":
            self._ach_stat("actions_rest", 1)
        # ─────────────────────────────────────────────────────────────────────

        # ── Tick active effects (regen, expiry) ───────────────────────────────
        char = self.char
        spell_changed = False
        ticks_active = len([e for e in char.get("active_effects", []) if e["ticks_left"] > 0])
        if ticks_active:
            self._ach_stat("ticks_under_effect", ticks_active)
        for eff in char.get("active_effects", []):
            if eff["effect_type"] == "hp_regen":
                gained = min(int(eff["magnitude"]), char["max_hp"] - char["hp"])
                if gained > 0:
                    char["hp"] += gained
            elif eff["effect_type"] == "mp_regen":
                gained = min(int(eff["magnitude"]), char["max_mp"] - char["mp"])
                if gained > 0:
                    char["mp"] += gained
        tick_active_effects(char)   # decrements ticks, reverts expired stat buffs
        self._refresh_spell_list()

        # ── Attempt a spell cast for this action type ─────────────────────────
        if atype not in ("return", "ghost", "body", "reanimate", "respawn", "return_town"):
            self._attempt_spell_cast(atype)

        # ── Action resolution ─────────────────────────────────────────────────
        if atype == "fight":
            self._resolve_fight()
        elif atype == "loot":
            # Gold boost from active effects
            gold_mult = 1.0
            for eff in char.get("active_effects", []):
                if eff["effect_type"] == "gold_boost":
                    gold_mult += eff["magnitude"]
            gold = int(random.randint(10, 30) * (1 + char["stats"]["G"] * 0.02) * gold_mult)
            char["gold"] += gold
            self._ach_stat("gold_earned", gold)
            self._update_gold()
            self.log_story(f"    +{gold} gold")
            if random.random() < 0.55 + char["stats"]["L"] * 0.01:
                self._drop_item()
        elif atype == "return":
            char["hp"] = char["max_hp"]
            char["mp"] = char["max_mp"]
            self.log_story("    Fully healed.")
            self._update_char_panel()
        elif atype == "rest":
            h = random.randint(3, 8)
            char["hp"] = min(char["max_hp"], char["hp"] + h)
            char["mp"] = min(char["max_mp"], char["mp"] + h)
            self.log_story(f"    Recovered {h} HP/MP.")
            self._update_char_panel()
        elif atype == "travel":
            if random.random() < 0.08:
                gold_mult = 1.0
                for eff in char.get("active_effects", []):
                    if eff["effect_type"] == "gold_boost":
                        gold_mult += eff["magnitude"]
                g = int(random.randint(1, 6) * gold_mult)
                char["gold"] += g
                self._ach_stat("gold_earned", g)
                self._update_gold()
                self.log_story(f"    Found {g} gold on the road!")
        elif atype in ("search","locate","scout","investigate",
                        "gather","escort","inspect","collect","speak"):
            if random.random() < 0.30:
                xp_mult = 1.0
                for eff in char.get("active_effects", []):
                    if eff["effect_type"] == "xp_boost":
                        xp_mult += eff["magnitude"]
                xp = int(random.randint(2, 6) * xp_mult)
                self._gain_xp(xp)
                self.log_story(f"    +{xp} XP")
        elif atype == "market":
            self._apply_market_loop()
        elif atype == "find_vendor":
            self.log_story("  [VENDOR] Found a buyer.", "vendor")
        elif atype == "sell":
            self._sell_item_only()
        elif atype == "restore":
            self._restore_hp_mp()
        elif atype == "upgrade":
            self._upgrade_gear()
        elif atype == "transmute":
            # In-field transmute step injected by _check_transmute_option
            self._transmute_one_item(self._pending_transmute_tier or "Minor")
            self._pending_transmute_tier = None
        elif atype == "return_town":
            pass

    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    #  COMBAT & DEATH
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    def _resolve_fight(self):
        char = self.char
        if random.random() < 0.04 + char["stats"]["L"] * 0.005:
            self.log_story("    DODGE! Took no damage.")
        else:
            raw  = random.randint(3, 10)
            # combat_defense active effects reduce damage
            mit  = min(0.60, char["stats"]["R"] * 0.03)
            for eff in char.get("active_effects", []):
                if eff["effect_type"] == "combat_defense":
                    mit = min(0.85, mit + eff["magnitude"])
            dmg  = max(1, int(raw * (1 - mit)))
            char["hp"] -= dmg
            self.log_story(f"    Took {dmg} damage. "
                           f"({max(0,char['hp'])}/{char['max_hp']} HP)")
            self._update_char_panel()
            if char["hp"] <= 0:
                char["hp"] = 0
                self._update_char_panel()
                self._trigger_death()
                return

        self._ach_stat("enemies_killed", 1)
        self._ach_stat("actions_fight", 1)
        char = self.char
        # Apply pending spell damage bonus (from combat_damage spells)
        bonus_dmg = char.pop("pending_spell_damage", 0)
        if bonus_dmg:
            self.log_story(f"    ✦ Spell damage: +{bonus_dmg}")
        xp_mult = 1.0
        for eff in char.get("active_effects", []):
            if eff["effect_type"] == "xp_boost":
                xp_mult += eff["magnitude"]
        xp = int((random.randint(8, 20) + char["stats"]["I"] // 5) * xp_mult)
        self._gain_xp(xp)
        self.log_story(f"    +{xp} XP")
        if random.random() < 0.25 + char["stats"]["L"] * 0.01:
            self._drop_item()
        self._check_achievements()

    def _trigger_death(self):
        if self._dead:
            return
        self._dead = True
        self.char["deaths"] += 1
        self._ach_stat("times_died", 1)
        self._check_achievements()
        for line in DEATH_SEQUENCE:
            self.log_story(line, "death")
        lost = len(self.char["inventory"])
        self.char["inventory"].clear()
        lg = self.char["gold"] // 2
        self.char["gold"] = max(0, self.char["gold"] - lg)
        self.log_story(f"  Lost {lost} items and {lg} gold.", "death")
        # Revert all active stat buffs and wipe effects
        for eff in self.char.get("active_effects", []):
            if eff["effect_type"] == "stat_buff":
                key = eff.get("stat_key", "")
                if key and key in self.char["stats"]:
                    self.char["stats"][key] -= eff["magnitude"]
        self.char["active_effects"] = []
        self.char.pop("pending_spell_damage", None)
        self._update_gold()
        self._refresh_inv_list()
        self._refresh_spell_list()
        self._run_respawn_sequence(0)

    def _run_respawn_sequence(self, idx):
        if idx >= len(RESPAWN_STEPS):
            self._finish_respawn()
            return
        _, label = RESPAWN_STEPS[idx]
        self.task_label.config(text=label)
        self.log_story(f"  {label}", "ghost")
        self.pbar["value"] = 0
        self._animate_respawn_bar(idx, 0)

    def _animate_respawn_bar(self, idx, val):
        val += 5
        self.pbar["value"] = min(val, 100)
        if val < 100:
            self.root.after(80, lambda: self._animate_respawn_bar(idx, val))
        else:
            self.root.after(350, lambda: self._run_respawn_sequence(idx + 1))

    def _finish_respawn(self):
        self.char["hp"] = self.char["max_hp"]
        self.char["mp"] = self.char["max_mp"]
        self._dead      = False
        self.log_story("  Back in the land of the living. Somehow.", "ghost")
        self._update_char_panel()
        self.start_new_quest()
        self.run_game_loop()

    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    #  VENDOR — individual item selling with per-item progress animation
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    def _sell_item_only(self):
        """Sell one item from inventory without healing/upgrade."""
        if not self.char["inventory"]:
            self.log_story("    Nothing left to sell. Browsed awkwardly.", "vendor")
            return
        item  = self.char["inventory"].pop(0)
        value = item_sell_value(item, self.char["stats"]["L"])
        self.char["gold"] += value
        self._ach_stat("items_sold", 1)
        self._ach_stat("gold_earned", value)
        self._update_gold()
        self._refresh_inv_list()
        self.log_story(f"  [SOLD] {item_display(item)}  ➜  {value} gold", "vendor")
        self._check_achievements()

    def _restore_hp_mp(self):
        """Restore HP and MP from sell proceeds. Called once after all sells."""
        total_gold = self.char["gold"]
        hp_missing = self.char["max_hp"] - self.char["hp"]
        mp_missing = self.char["max_mp"] - self.char["mp"]
        spent = 0

        if hp_missing > 0:
            hp_heal = min(hp_missing, total_gold // 2)
            hp_cost = hp_heal
            spent += hp_cost
            self.char["hp"] = min(self.char["max_hp"], self.char["hp"] + hp_heal)
            self.log_story(f"    Recovered {hp_heal} HP ({hp_cost} gold)")

        if mp_missing > 0 and total_gold - spent > 0:
            mp_heal = min(mp_missing, (total_gold - spent) // 2)
            mp_cost = mp_heal
            self.char["mp"] = min(self.char["max_mp"], self.char["mp"] + mp_heal)
            self.log_story(f"    Recovered {mp_heal} MP ({mp_cost} gold)")
            spent += mp_cost

        self.char["gold"] -= spent
        self._update_gold()
        self._update_char_panel()
        self.log_story(f"  Remaining: {self.char['gold']} gold", "vendor")

    def _upgrade_gear(self):
        """Try to upgrade one equipment slot. Called per upgrade step."""
        for slot in EQUIP_SLOTS:
            item = self.char["equip"].get(slot)
            if not item:
                continue
            current_upgrade = item.get("upgrade", 0)
            cost = upgrade_cost(item)
            if self.char["gold"] >= cost:
                self.char["gold"] -= cost
                item["upgrade"] = current_upgrade + 1
                item["bonus"] = item.get("bonus", 1) + 1
                item["power"] = item.get("power", 1) + 1
                # FIX: keep the live stat in sync with the upgraded bonus.
                # Without this, each upgrade increases item["bonus"] but never
                # adds the matching point to the character stat. When the item
                # is later unequipped the full current bonus is subtracted,
                # causing a net loss of (upgrade count) points per gear swap —
                # which is how stats silently drift into negative values.
                self.char["stats"][item["stat"]] += 1
                self._ach_stat("upgrades_total", 1)
                self.log_story(f"    UPGRADED [{slot}]: {item_display(item)} +{item['upgrade']} ({cost} gold)", "vendor")
                self._update_gold()
                self._refresh_equip_list()
                self._refresh_stat_tree()
                self._update_char_panel()
                return
        self.log_story("    No upgrades available.", "vendor")

    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    #  ITEMS
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    def _drop_item(self):
        item  = generate_item(self.char["lvl"])
        # Apply loot quality buff from active effects
        for eff in self.char.get("active_effects", []):
            if eff["effect_type"] == "loot_quality":
                item["power"] += int(eff["magnitude"])
                item["bonus"] += max(0, int(eff["magnitude"]) // 3)
        slot  = item["slot"]
        equip = self.char["equip"].get(slot)
        if equip is None or item["power"] > equip["power"]:
            if equip:
                self.char["inventory"].append(equip)
                self.char["stats"][equip["stat"]] -= equip["bonus"]
                self.log_story(f"    Unequipped: {item_display(equip)}")
            self.char["equip"][slot] = item
            self.char["stats"][item["stat"]] += item["bonus"]
            self.log_story(f"    Equipped: {item_display(item)}  ({slot})")
            self._refresh_equip_list()
            self._refresh_stat_tree()
        else:
            self.char["inventory"].append(item)
            self.log_story(f"    Looted (bag): {item_display(item)}")
        self._refresh_inv_list()
        max_cap = get_max_capacity(self.char["stats"])
        current_weight = get_inventory_weight(self.char["inventory"])
        if max_cap > 0 and current_weight >= max_cap:
            pct = int(100 * current_weight / max_cap)
            self.log_story(f"  [!] Encumbered ({pct}% / {max_cap}) — market visit queued.", "vendor")

    def _refresh_equip_list(self):
        self.equip_list.delete(0, tk.END)
        for slot in EQUIP_SLOTS:
            item = self.char["equip"].get(slot)
            self.equip_list.insert(
                tk.END, f"{slot:<8} {item_display(item) if item else '---'}")

    def _refresh_inv_list(self):
        self.inv_list.delete(0, tk.END)
        gold = self.char.get("gold", 0)
        self.inv_list.insert(tk.END, f"GOLD: {gold}")
        n = len(self.char["inventory"])
        if n == 0:
            self.inv_list.insert(tk.END, "---")
        else:
            for item in self.char["inventory"]:
                self.inv_list.insert(tk.END, item_display(item))

    def _refresh_spell_list(self):
        """Rebuild the spell listbox, annotating any currently active effects."""
        self.spell_list.delete(0, tk.END)
        active_names = {e["spell"] for e in self.char.get("active_effects", [])}
        active_ticks = {e["spell"]: e["ticks_left"] for e in self.char.get("active_effects", [])}
        for sp_name in self.char.get("spells", []):
            if sp_name in active_names:
                t = active_ticks[sp_name]
                self.spell_list.insert(tk.END, f"{sp_name}  [ACTIVE {t}t]")
            else:
                self.spell_list.insert(tk.END, sp_name)

    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    #  SPELL CASTING
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    def _attempt_spell_cast(self, action_type):
        """
        Evaluate each known spell against the current action type.
        Priority: HP regen if low HP → MP regen if low MP →
                  reapply expired buffs → opportunistic cast.
        A spell will not recast while already active (no-spam rule).
        Cast chance is gated by class affinity (cast_chance helper).
        """
        char = self.char
        known = char.get("spells", [])
        if not known:
            return

        mp = char["mp"]
        max_mp = char["max_mp"]
        hp = char["hp"]
        max_hp = char["max_hp"]

        # Build candidate list: spells whose window includes this action
        candidates = []
        for name in known:
            sp = SPELL_BY_NAME.get(name)
            if not sp:
                continue
            etype = sp["effect_type"]
            # Check action window
            if action_type not in SPELL_CAST_WINDOWS.get(etype, set()):
                continue
            # No recast if already active (except instant spells which have duration 0)
            if sp["duration"] > 0 and has_active_effect(char, etype):
                continue
            # MP floor: skip non-regen spells if below 25% MP
            if etype not in ("hp_regen", "mp_regen") and mp < max_mp * 0.25:
                continue
            # Must have enough MP
            if sp["mp_cost"] > mp:
                continue
            candidates.append((name, sp))

        if not candidates:
            return

        # ── Priority selection ──────────────────────────────────────────────
        def pick_by_type(etype):
            return [(n, s) for n, s in candidates if s["effect_type"] == etype]

        chosen_name, chosen_sp = None, None

        # 1. Low HP → try hp_regen
        if hp < max_hp * 0.40:
            pool = pick_by_type("hp_regen")
            if pool:
                chosen_name, chosen_sp = random.choice(pool)

        # 2. Low MP → try mp_regen
        if not chosen_name and mp < max_mp * 0.35:
            pool = pick_by_type("mp_regen")
            if pool:
                chosen_name, chosen_sp = random.choice(pool)

        # 3. Key buffs/offence whose type isn't running
        if not chosen_name:
            priority_types = ["combat_defense", "stat_buff", "xp_boost",
                              "gold_boost", "loot_quality", "combat_damage",
                              "transmute", "craft"]
            for ptype in priority_types:
                if has_active_effect(char, ptype):
                    continue
                pool = pick_by_type(ptype)
                if pool:
                    chosen_name, chosen_sp = random.choice(pool)
                    break

        # 4. Fallback: random from remaining candidates
        if not chosen_name:
            chosen_name, chosen_sp = random.choice(candidates)

        # ── Class-affinity cast roll ────────────────────────────────────────
        chance = cast_chance(chosen_sp, char)
        if random.random() > chance:
            return

        # ── Fire the spell ──────────────────────────────────────────────────
        char["mp"] = max(0, mp - chosen_sp["mp_cost"])
        self._ach_stat("spells_cast", 1)
        self._fire_spell(chosen_name, chosen_sp)

    def _flash_cast(self):
        """Briefly flash the story log background and MP bar to signal a spell cast."""
        try:
            self.story_text.config(bg="#1a1a44")
            self.mp_bar.config(style="Flash.Horizontal.TProgressbar")
            self.root.after(200, lambda: self.story_text.config(bg="#08080f"))
            self.root.after(200, lambda: self.mp_bar.config(style="MP.Horizontal.TProgressbar"))
        except Exception:
            pass  # safe if widgets not yet built

    def _fire_spell(self, name, sp):
        """Apply the spell effect to the character."""
        self._flash_cast()
        char   = self.char
        etype  = sp["effect_type"]
        mag    = sp["magnitude"]
        dur    = sp["duration"]
        tier   = sp["tier"]

        # ── Instant effects ─────────────────────────────────────────────────
        if etype == "transmute":
            self._transmute_one_item(tier)
            self.log_story(f"  ✦ {name} — transmuted an item in-field.", "level")
            self._update_char_panel()
            self._refresh_spell_list()
            return

        if etype == "craft":
            self._craft_one_item()
            self.log_story(f"  ✦ {name} — item reforged by arcane craft!", "level")
            self._update_char_panel()
            self._refresh_spell_list()
            return

        if etype == "combat_damage":
            # Stored as a one-shot pending bonus; consumed in _resolve_fight
            char.setdefault("pending_spell_damage", 0)
            char["pending_spell_damage"] += int(mag)
            self.log_story(f"  ✦ {name} — +{int(mag)} spell damage primed.", "level")
            self._update_char_panel()
            self._refresh_spell_list()
            return

        # ── Duration effects ────────────────────────────────────────────────
        effect = {
            "spell":       name,
            "effect_type": etype,
            "magnitude":   mag,
            "ticks_left":  dur,
        }

        if etype == "stat_buff":
            key = sp.get("stat_key", "")
            effect["stat_key"] = key
            if key and key in char["stats"]:
                char["stats"][key] += int(mag)
                self.log_story(
                    f"  ✦ {name} — +{int(mag)} {key} for {dur} actions.", "level")
        elif etype == "hp_regen":
            self.log_story(
                f"  ✦ {name} — regenerating {int(mag)} HP/action for {dur} actions.", "level")
        elif etype == "mp_regen":
            self.log_story(
                f"  ✦ {name} — regenerating {int(mag)} MP/action for {dur} actions.", "level")
        elif etype == "xp_boost":
            self.log_story(
                f"  ✦ {name} — +{int(mag*100)}% XP for {dur} actions.", "level")
        elif etype == "gold_boost":
            self.log_story(
                f"  ✦ {name} — +{int(mag*100)}% gold for {dur} actions.", "level")
        elif etype == "loot_quality":
            self.log_story(
                f"  ✦ {name} — item power +{int(mag)} on next {dur} drops.", "level")
        elif etype == "combat_defense":
            self.log_story(
                f"  ✦ {name} — {int(mag*100)}% damage reduction for {dur} actions.", "level")

        char.setdefault("active_effects", []).append(effect)
        self._ach_stat("status_effects_applied", 1)
        self._update_char_panel()
        self._refresh_spell_list()

    def _transmute_one_item(self, spell_tier):
        """Convert the oldest inventory item to gold at transmute_efficiency rate."""
        char = self.char
        inv  = char.get("inventory", [])
        if not inv:
            return
        item   = inv.pop(0)
        eff    = transmute_efficiency(spell_tier, char["stats"].get("I", 10))
        market = item_sell_value(item, char["stats"]["L"])
        value  = max(1, int(market * eff))
        lost   = market - value
        char["gold"] += value
        self._ach_stat("gold_earned", value)
        self._ach_stat("items_transmuted", 1)
        self.log_story(
            f"  ✦ TRANSMUTE [{int(eff*100)}% rate]  {item_display(item)}",
            "level")
        self.log_story(
            f"    {value} gold received  (market: {market}, saved travel, lost {lost})",
            "vendor")
        self._update_gold()
        self._refresh_inv_list()

    def _craft_one_item(self):
        """
        Tier III crafting: reforge the weakest inventory item into a higher-power
        version of the same slot.  If inventory is empty, try equipped items.
        """
        char = self.char
        inv  = char.get("inventory", [])
        if inv:
            # Pick the weakest item by power
            target = min(inv, key=lambda i: i.get("power", 0))
            inv.remove(target)
        else:
            # Try to upgrade weakest equipped item
            equipped = [(s, it) for s, it in char["equip"].items() if it is not None]
            if not equipped:
                self.log_story("    (No items to craft — inventory empty.)", "vendor")
                return
            slot, target = min(equipped, key=lambda x: x[1].get("power", 0))
            char["stats"][target["stat"]] -= target["bonus"]
            char["equip"][slot] = None

        # Generate a new item at current level +2 (power bump)
        crafted = generate_item(char["lvl"] + 2)
        # Force same slot for thematic consistency
        crafted["slot"] = target["slot"]
        crafted["name"] = "Arcane-Forged " + crafted["name"]

        self.log_story(
            f"    Crafted: {item_display(target)} → {item_display(crafted)}", "vendor")
        self._ach_stat("items_crafted", 1)

        # Auto-equip if better than current slot
        slot     = crafted["slot"]
        equipped = char["equip"].get(slot)
        if equipped is None or crafted["power"] > equipped["power"]:
            if equipped:
                inv.append(equipped)
                char["stats"][equipped["stat"]] -= equipped["bonus"]
            char["equip"][slot] = crafted
            char["stats"][crafted["stat"]] += crafted["bonus"]
            self.log_story(f"    Auto-equipped: {item_display(crafted)}")
            self._refresh_equip_list()
            self._refresh_stat_tree()
        else:
            inv.append(crafted)

        self._refresh_inv_list()

    def _refresh_story_tree(self):
        self.story_tree.delete(*self.story_tree.get_children())
        pr = self.char.get("prestige_level", 0)
        if not self.char["prologue_done"]:
            self.story_tree.insert("", "end", values=("☐", "Prologue"))
        else:
            self.story_tree.insert("", "end", values=("☑", "Prologue"))
            for prior_pr in range(pr):
                for i in range(1, 100):
                    displayed_act = (prior_pr * 100) + i
                    name = get_act_name(displayed_act)
                    self.story_tree.insert("", "end", values=("☑", f"Act {displayed_act}: {name}"))
                displayed_act = (prior_pr * 100) + 100
                name = "Resetting the Universe"
                self.story_tree.insert("", "end", values=("☑", f"Act {displayed_act}: {name}"))
            for i in range(1, self.char["current_act"]):
                displayed_act = (pr * 100) + i
                name = get_act_name(displayed_act)
                self.story_tree.insert("", "end", values=("☑", f"Act {displayed_act}: {name}"))
            act = self.char["current_act"]
            displayed_act = (pr * 100) + act
            name = get_act_name(displayed_act)
            self.story_tree.insert("", "end", values=("☐", f"Act {displayed_act}: {name}"))

    def _refresh_hist_tree(self):
        self.hist_tree.delete(*self.hist_tree.get_children())
        if self._current_quest_name:
            self.hist_tree.insert("", "end", values=("☐", f"> {self._current_quest_name}"))
        quests = self.char.get("completed_quests", [])[-10:]
        if self._hist_descending:
            quests = quests[::-1]
        for q_name in quests:
            self.hist_tree.insert("", "end", values=("☑", q_name))

    def _toggle_hist_order(self, event=None):
        self._hist_descending = not self._hist_descending
        self._refresh_hist_tree()

    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    #  XP / LEVELLING
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    def _gain_xp(self, amount):
        self.char["exp"] += amount
        while self.char["exp"] >= self.char["exp_next"]:
            self.char["exp"] -= self.char["exp_next"]
            self._level_up()
        self._update_char_panel()

    def _level_up(self):
        self.char["lvl"]      += 1
        self.char["exp_next"]  = self.char["lvl"] * 100
        # Track max level reached across all resets
        ach_stats = self.char.get("achievements", {}).get("stats", {})
        if self.char["lvl"] > ach_stats.get("max_level", 0):
            self._ach_stat_set("max_level", self.char["lvl"])
        self._check_achievements()
        pick_keys = []
        if self.char["lvl"] % 2 == 0:
            pick_keys = random.sample(STAT_KEYS, 2)
            for s in pick_keys:
                self.char["stats"][s] += 2
        self.char["max_hp"] = 20 + (self.char["lvl"]-1)*5 + self.char["stats"]["E"]//3
        self.char["max_mp"] = 10 + (self.char["lvl"]-1)*3 + self.char["stats"]["I"]//4
        self.char["hp"]     = self.char["max_hp"]
        self.char["mp"]     = self.char["max_mp"]
        if pick_keys:
            gain = f"+2 to {', '.join(pick_keys)}"
        else:
            gain = ""
        self.log_story(f"★ LEVEL UP! Now Lv {self.char['lvl']}. ({gain})  HP/MP restored.", "level")
        if self.char["lvl"] % 5 == 0:
            new_spell = generate_stat_spell(self.char)
            if new_spell not in self.char["spells"]:
                self.char["spells"].append(new_spell)
                self._ach_stat("spells_learned", 1)
                sp_def = SPELL_BY_NAME.get(new_spell, {})
                tier   = sp_def.get("tier", "")
                cost   = sp_def.get("mp_cost", 0)
                self.log_story(f"  Learned: {new_spell}  [{tier}] ({cost} MP)", "level")
                self._refresh_spell_list()
        self._refresh_stat_tree()

    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    #  UI HELPERS
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    def _update_char_panel(self):
        c = self.char
        pl = c.get("prestige_level", 0)
        current_title = c.get("current_title", "Vagabond")
        title_history = c.get("title_history", [])
        full_title = ", ".join(title_history + [current_title]) if title_history else current_title
        self.info_label.config(
            text=(f"Name: {c['name']}\n"
                  f"Title: {current_title}\n"
                  f"Race: {c['race']}\n"
                  f"Class: {c['class']}\n"
                  f"Lv: {c['lvl']} | Prestige: {pl}"))
        
        def pct(v, m): return int(100 * v / m) if m else 0
        self.hp_bar["value"] = pct(c["hp"],  c["max_hp"])
        self.hp_lbl.config(text=f"{c['hp']}/{c['max_hp']}")
        self.mp_bar["value"] = pct(c["mp"],  c["max_mp"])
        self.mp_lbl.config(text=f"{c['mp']}/{c['max_mp']}")
        self.xp_bar["value"] = pct(c["exp"], c["exp_next"])
        self.xp_lbl.config(text=f"{c['exp']}/{c['exp_next']}")
        max_cap = get_max_capacity(c["stats"])
        current_weight = get_inventory_weight(c.get("inventory", []))
        enc = int(100 * current_weight / max_cap) if max_cap > 0 else 0
        self.enc_bar["value"] = enc
        self.enc_lbl.config(text=f"{current_weight}/{max_cap}")

    def _show_title_tooltip(self, event, full_title):
        if hasattr(self, '_title_tip') and self._title_tip.winfo_exists():
            self._title_tip.destroy()
        c = self.char
        title_history = c.get("title_history", [])
        tooltip_text = ", ".join(title_history) if title_history else "No previous titles"
        self._title_tip = tk.Toplevel(self.root)
        self._title_tip.wm_overrideredirect(True)
        self._title_tip.wm_geometry(f"+{event.x_root+15}+{event.y_root+15}")
        tk.Label(self._title_tip, text=tooltip_text, font=("Consolas", 8),
                bg="#1a1a2e", fg="#00ff00", wraplength=400).pack()
        self._title_tip.update_idletasks()

    def _hide_title_tooltip(self):
        if hasattr(self, '_title_tip') and self._title_tip.winfo_exists():
            self._title_tip.destroy()

    def _dev_force_reset(self):
        if messagebox.askyesno("Dev: Force Reset", "Force universe reset now?"):
            self.char["prologue_done"] = True
            self.char["current_act"] = 100
            self.char["act_quests_done"] = 0
            self.char["quests_completed"] = 100
            pr = self.char.get("prestige_level", 0)
            displayed_act = (pr * 100) + 100
            self.log_story(f"[DEV] Act {displayed_act}: Resetting the Universe begins!", "level")
            self._refresh_story_tree()
            self._update_act_bars()
            self._update_char_panel()
            self._start_special_quest("world_reset")
            self.run_game_loop()

    def _dev_scale_to_act_100(self):
        target_lvl = 100
        current_lvl = self.char["lvl"]
        self.char["lvl"] = target_lvl
        self.char["exp"] = 0
        self.char["exp_next"] = target_lvl * 100 + 50
        self.char["hp"] = 50 + (target_lvl * 10)
        self.char["max_hp"] = 50 + (target_lvl * 10)
        self.char["mp"] = 50 + (target_lvl * 5)
        self.char["max_mp"] = 50 + (target_lvl * 5)
        for stat in STAT_KEYS:
            self.char["stats"][stat] = min(30, self.char["stats"][stat] + target_lvl - current_lvl)
        self._update_char_panel()
        self._update_gold()
        self.log_story(f"[DEV] Scaled to Level {target_lvl}!", "level")

    def _dev_add_gold(self):
        self.char["gold"] += 10000
        self._update_gold()
        self.log_story("[DEV] +10,000 gold!", "vendor")

    def _dev_add_xp(self):
        self._gain_xp(100)
        self.log_story("[DEV] +100 XP!", "level")

    def _update_gold(self):
        self._refresh_inv_list()

    def _change_theme(self):
        theme_name = self.theme.get()
        self._setup_styles()
        self._update_char_panel()
        self._refresh_stat_tree()
        self._refresh_story_tree()
        self._refresh_hist_tree()
        self.log_story(f"[THEME] Switched to {theme_name} theme.", "level")
        if hasattr(self, 'char'):
            self._update_char_panel()
            self._refresh_stat_tree()
            self._refresh_story_tree()
            self._refresh_hist_tree()

    def _refresh_stat_tree(self):
        for s in STAT_KEYS:
            self.stat_tree.item(s, values=(s, self.char["stats"][s], STAT_DEFS[s][0]))

    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    #  ACHIEVEMENTS
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

    def _ach_stat(self, key, amount):
        """Increment an achievement stat by amount."""
        try:
            self.char["achievements"]["stats"][key] = \
                self.char["achievements"]["stats"].get(key, 0) + amount
        except (KeyError, TypeError):
            pass

    def _ach_stat_set(self, key, value):
        """Set an achievement stat to a specific value (for max tracking)."""
        try:
            self.char["achievements"]["stats"][key] = value
        except (KeyError, TypeError):
            pass

    def _check_achievements(self):
        """Check all achievements and unlock any newly met thresholds."""
        if not ACHIEVEMENTS:
            return
        unlocked = self.char.get("achievements", {}).get("unlocked", {})
        stats    = self.char.get("achievements", {}).get("stats", {})
        newly_unlocked = []

        for ach in ACHIEVEMENTS:
            ach_id = ach["id"]
            if ach_id in unlocked:
                continue  # Already got it

            # Standard threshold check
            if "stat" in ach and "threshold" in ach:
                current = stats.get(ach["stat"], 0)
                if current >= ach["threshold"]:
                    newly_unlocked.append(ach)
                    continue

            # Special condition checks
            if ach.get("special") == "all_slots_filled":
                equip = self.char.get("equip", {})
                if all(equip.get(slot) is not None for slot in EQUIP_SLOTS):
                    newly_unlocked.append(ach)

        for ach in newly_unlocked:
            unlocked[ach["id"]] = time.time()
            self.char["achievements"]["unlocked"] = unlocked
            self.log_story(f"🏆 ACHIEVEMENT UNLOCKED: {ach['name']}!", "level")
            self._show_achievement_toast(ach)

    def _show_achievement_toast(self, ach):
        """Show a brief toast popup in the bottom-right corner."""
        try:
            toast = tk.Toplevel(self.root)
            toast.wm_overrideredirect(True)
            toast.attributes("-topmost", True)
            toast.attributes("-alpha", 0.0)

            # Position: bottom-right of the main window
            self.root.update_idletasks()
            rx = self.root.winfo_rootx()
            ry = self.root.winfo_rooty()
            rw = self.root.winfo_width()
            rh = self.root.winfo_height()
            w, h = 300, 64
            x = rx + rw - w - 16
            y = ry + rh - h - 16
            toast.wm_geometry(f"{w}x{h}+{x}+{y}")

            # Dark styled frame
            frame = tk.Frame(toast, bg="#1a1a2e", bd=2, relief="solid",
                             highlightbackground="#ffd700", highlightthickness=2)
            frame.pack(fill="both", expand=True)

            tk.Label(frame, text="🏆  ACHIEVEMENT UNLOCKED",
                     font=("Consolas", 8, "bold"),
                     bg="#1a1a2e", fg="#ffd700").pack(anchor="w", padx=8, pady=(6,0))
            tk.Label(frame, text=ach["name"],
                     font=("Consolas", 10, "bold"),
                     bg="#1a1a2e", fg="#ffffff").pack(anchor="w", padx=8)
            tk.Label(frame, text=ach.get("desc", ""),
                     font=("Consolas", 7),
                     bg="#1a1a2e", fg="#aaaaaa").pack(anchor="w", padx=8)

            # Queue any waiting toasts so they don't overlap
            if not hasattr(self, '_toast_queue'):
                self._toast_queue = []
            self._toast_queue.append(toast)

            if len(self._toast_queue) == 1:
                self._animate_toast_in(toast, 0.0)

        except Exception:
            pass  # Never crash the game over a toast

    def _animate_toast_in(self, toast, alpha):
        """Fade in, hold, then fade out the toast."""
        try:
            if not toast.winfo_exists():
                self._next_toast()
                return
            if alpha < 1.0:
                alpha = min(alpha + 0.08, 1.0)
                toast.attributes("-alpha", alpha)
                self.root.after(20, lambda: self._animate_toast_in(toast, alpha))
            else:
                # Hold for 2.8 seconds then fade out
                self.root.after(2800, lambda: self._animate_toast_out(toast, 1.0))
        except Exception:
            self._next_toast()

    def _animate_toast_out(self, toast, alpha):
        """Fade the toast out then destroy it."""
        try:
            if not toast.winfo_exists():
                self._next_toast()
                return
            if alpha > 0.0:
                alpha = max(alpha - 0.08, 0.0)
                toast.attributes("-alpha", alpha)
                self.root.after(20, lambda: self._animate_toast_out(toast, alpha))
            else:
                toast.destroy()
                self._next_toast()
        except Exception:
            self._next_toast()

    def _next_toast(self):
        """Pop the finished toast and start the next one if queued."""
        try:
            if hasattr(self, '_toast_queue') and self._toast_queue:
                self._toast_queue.pop(0)
                if self._toast_queue:
                    next_toast = self._toast_queue[0]
                    self._animate_toast_in(next_toast, 0.0)
        except Exception:
            pass

    def log_story(self, msg, tag="normal"):
        self.story_text.config(state="normal")
        self.story_text.insert(tk.END, msg + "\n", tag)
        self.story_text.see(tk.END)
        self.story_text.config(state="disabled")


# ══════════════════════════════════════════════════════════════════════════════
#  ENTRY POINT
# ══════════════════════════════════════════════════════════════════════════════
import logging
import traceback

def log_crash(exc_type, exc_value, exc_traceback):
    if issubclass(exc_type, KeyboardInterrupt):
        sys.__excepthook__(exc_type, exc_value, exc_traceback)
        return
    log_path = os.path.join(BASE_DIR, "crash.log")
    with open(log_path, "a") as f:
        f.write(f"\n=== CRASH {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} ===\n")
        f.write("".join(traceback.format_exception(exc_type, exc_value, exc_traceback)))
    messagebox.showerror("CRASH", f"Error saved to:\n{log_path}")

if __name__ == "__main__":
    from datetime import datetime
    import sys
    sys.excepthook = log_crash
    root = tk.Tk()
    IdleRPG(root)
    root.mainloop()