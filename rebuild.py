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
    "The End of Days", "The New Era"
]

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
    {"name": "The End of Everything", "steps": [("travel", 6), ("fight", 15), ("loot", 4), ("return", 1)]},
    {"name": "The Last Battle", "steps": [("travel", 8), ("fight", 20), ("loot", 5), ("return", 1)]},
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
}

# ── Item Generation ────────────────────────────────────────────────────────────
ITEM_PREFIXES = [
    "Shoddy", "Iron", "Gleaming", "Obsidian", "Cursed", "Arcane", "Gilded",
    "Rusted", "Enchanted", "Blessed", "Tainted", "Ancient", "Shadow", "Storm",
    "Void", "Radiant", "Infernal", "Divine", "Silver", "Mythril",
    "Cracked", "Fabled", "Ethereal", "Grim", "Luminous", "Vexed", "Jagged",
    "Frozen", "Volcanic", "Celestial", "Corrupted", "Starlight", "Bloodstained",
    "Titanic", "Whispering", "Forgotten", "Prismatic", "Abyssal", "Hallowed"
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

# ── Tiered Spell Pools ──────────────────────────────────────────────────
# Structured as Stat -> Tier -> List of Spells
TIERED_SPELLS = {
    "I": {
        "Minor": ["Magic Spark", "Mana Drip"], "Major": ["Arcane Blast", "Spell Shield"],
        "II": ["Meteor Shower", "Time Warp"], "III": ["The Omega Protocol", "Reality Collapse"]
    },
    "P": {
        "Minor": ["Heavy Strike", "Pommel Bash"], "Major": ["Sunder Armor", "Whirlwind"],
        "II": ["Mountain Splitter", "Dragon Roar"], "III": ["God-Slayer Impact", "World Ender"]
    },
    "D": {
        "Minor": ["Quick Stab", "Side Step"], "Major": ["Flurry of Blows", "Shadow Dash"],
        "II": ["Assassinate", "Ghost Walk"], "III": ["Thousand Cuts", "Dimension Strike"]
    },
    "E": {
        "Minor": ["Iron Skin", "Deep Breath"], "Major": ["Unstoppable Will", "Second Wind"],
        "II": ["Juggernaut Aura", "Eternal Stand"], "III": ["Immortal Essence", "Bastion of Life"]
    },
    "R": {
        "Minor": ["Guard Up", "Stone Flesh"], "Major": ["Reflective Shell", "Mana Shield"],
        "II": ["Absolute Barrier", "Kinetic Dampener"], "III": ["Diamond Soul", "Nullification Field"]
    },
    "L": {
        "Minor": ["Lucky Coin", "Fate's Flick"], "Major": ["Critical Eye", "Double Down"],
        "II": ["Jackpot Strike", "Fortune's Favor"], "III": ["Reality Cheat", "God-Hand Roll"]
    },
    "G": {
        "Minor": ["Coinsense", "Bargain Hint"], "Major": ["Golden Touch", "Treasure Sense"],
        "II": ["Midas Grip", "Wealth Aura"], "III": ["King's Fortune", "Everfull Purse"]
    }
}

# ══════════════════════════════════════════════════════════════════════════════
#  CONFIG  (tweak gameplay here)
# ══════════════════════════════════════════════════════════════════════════════
VENDOR_QUEST_INTERVAL = 6     # quests between forced vendor visits
INVENTORY_MAX         = 20    # slots before bag-full vendor trip
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
    "sell":        "Selling at vendor...",
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

def generate_item(level):
    slot   = random.choice(EQUIP_SLOTS)
    prefix = random.choice(ITEM_PREFIXES)
    base   = random.choice(ITEM_BASES[slot])
    stat   = random.choice(STAT_KEYS)
    bonus  = random.randint(1, max(1, level // 2 + 1))
    power  = level + random.randint(0, 3)
    return {"name": f"{prefix} {base}", "slot": slot,
            "stat": stat, "bonus": bonus, "power": power, "upgrade": 0}

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
            ("HP",   "hp_bar"),
            ("MP",   "mp_bar"),
            ("XP",   "xp_bar"),
            ("Gold", "gold_bar"),
            ("Blue", "mp_bar"),
        ]:
            col = theme.get(key, "#000000")
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
            "gold":  0,
            "stats": {k: stats.get(k, 10) for k in STAT_KEYS},
            "equip": {s: None for s in EQUIP_SLOTS},
            "inventory": [],
            "spells":    [],
            "deaths":    0,
            "quests_completed": 0,
            "prologue_done": False,
            "current_act": 0,
            "act_quests_done": 0,
            "in_boss_quest": False,
            "boss_attempts": 0,
            "completed_acts": [],
            "completed_quests": [],
        }
        starter_spell = generate_stat_spell(self.char)
        self.char["spells"].append(starter_spell)
        self._launch()

    def start_game_from_save(self, d):
        d.setdefault("quests_completed", 0)
        d.setdefault("deaths",           0)
        d.setdefault("spells",           [])
        d.setdefault("equip",            {s: None for s in EQUIP_SLOTS})
        self.char = d
        self._launch()

    def _launch(self):
        self._dead               = False
        self.quest_template      = None
        self.quest_steps         = []
        self.quest_step_index    = 0
        self.quest_total_steps   = 0
        self.current_action_type = None
        self._hist_descending  = False
        self._current_quest_name = None
        self.clear_screen()
        self._build_ui()
        self._refresh_story_tree()
        self._refresh_hist_tree()
        self._update_act_bars()
        for sp in self.char["spells"]:
            self.spell_list.insert(tk.END, sp)
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
        self.enc_bar["maximum"] = INVENTORY_MAX
        c1.add(fb, height=110)

        fsp = ttk.LabelFrame(c1, text=" SPELLS/SKILLS ", padding=2)
        self.spell_list = tk.Listbox(fsp, font=("Consolas", 8), bg="#0d0d1e", fg="#88ddff", selectbackground="#223344", height=3)
        self.spell_list.pack(fill="both", expand=True)
        c1.add(fsp)

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
        self.story_tree = ttk.Treeview(f_story, columns=("S","N"), show="headings", height=8)
        self.story_tree.heading("S", text="")
        self.story_tree.heading("N", text="Name")
        self.story_tree.column("S", width=20, anchor="center")
        self.story_tree.column("N", width=200, anchor="w")
        self.story_tree.pack(fill="both", expand=True)
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
        self.hist_tree = ttk.Treeview(f_hist, columns=("S","Q"), show="headings", height=6)
        self.hist_tree.heading("S", text="")
        self.hist_tree.heading("Q", text="Quest")
        self.hist_tree.column("S", width=20, anchor="center")
        self.hist_tree.column("Q", width=210)
        self.hist_tree.pack(fill="both", expand=True)
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

        inv_full = len(self.char["inventory"]) >= INVENTORY_MAX
        overdue  = (self.char["quests_completed"] > 0 and
                    self.char["quests_completed"] % VENDOR_QUEST_INTERVAL == 0 and
                    len(self.char["inventory"]) > 0)
        if inv_full or overdue:
            self._inject_vendor_quest()
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
            self.log_story("★ PROLOGUE COMPLETE! Act I begins...", "level")
            self._regular_quest()
            return
        tmpl = PROLOGUE_QUESTS[idx]
        self._start_quest(tmpl)

    def _start_boss(self):
        self.char["in_boss_quest"] = True
        self.char["boss_attempts"] = 0
        act = min(self.char["current_act"], len(BOSS_QUESTS) - 1)
        tmpl = BOSS_QUESTS[act]
        self.log_story(f"⚠ BOSS: {tmpl['name']} appears!", "death")
        self._start_quest(tmpl)

    def _boss_quest(self):
        self.char["boss_attempts"] += 1

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
            act = self.char["current_act"]
            act_name = ACT_NAMES[min(act - 1, len(ACT_NAMES) - 1)]
            self.act_label.config(text=f"Act {act}: {act_name}")
            self.act_pbar["maximum"] = QUESTS_PER_ACT
            self.act_pbar["value"] = self.char["act_quests_done"]
        else:
            self.act_label.config(text="Prologue")
            self.act_pbar["maximum"] = PROLOGUE_COMPLETE
            self.act_pbar["value"] = self.char["quests_completed"]

    def _inject_vendor_quest(self):
        inv_count = len(self.char["inventory"])
        reason    = "Bag full!" if inv_count >= INVENTORY_MAX else "Time to sell some loot."
        self.quest_template    = {"name": "Visit the Vendor"}
        self.quest_steps       = ["sell"] * max(1, inv_count)
        self.quest_step_index  = 0
        self.quest_total_steps = len(self.quest_steps)
        self.log_story(f"[VENDOR] {reason} Heading to market.", "vendor")
        self.quest_pbar["maximum"] = max(1, self.quest_total_steps)
        self.quest_pbar["value"]   = 0
        self._advance_to_next_step()

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
            self._complete_quest()

    def _update_step_label(self):
        done  = self.quest_step_index
        total = self.quest_total_steps
        atype = self.current_action_type or ""
        self.task_label.config(text=f"{self.quest_template['name']}: {atype.capitalize()} ({done+1}/{total})")

    def _complete_quest(self):
        if self.quest_template.get("name") != "Visit the Vendor":
            self._current_quest_name = None

            xp_r   = self.char["lvl"] * 40 + random.randint(10, 30)
            gold_r  = self.char["lvl"] * 10 + random.randint(5, 20)

            if self.char["in_boss_quest"]:
                self.char["in_boss_quest"] = False
                self.char["current_act"] += 1
                self.char["act_quests_done"] = 0
                self.log_story(f"★ BOSS DEFEATED! Act {self.char['current_act']} begins!", "level")
                gold_r *= 3
                xp_r *= 2
            else:
                self.char["quests_completed"] += 1
                q_name = self.quest_template["name"]
                if "completed_quests" not in self.char:
                    self.char["completed_quests"] = []
                self.char["completed_quests"].append(q_name)
                if self.char["prologue_done"]:
                    self.char["act_quests_done"] += 1

            self.char["gold"] += gold_r
            self.log_story(f"[QUEST DONE] {self.quest_template['name']}", "quest")
            self.log_story(f"  Reward: {xp_r} XP, {gold_r} gold.")
            self._gain_xp(xp_r)
            self._update_gold()
            self._refresh_story_tree()
            self._refresh_hist_tree()
            self._update_act_bars()

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

    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    #  GAME LOOP
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    def run_game_loop(self):
        if self._dead:
            return
        speed = max(50, 250 - self.char["stats"]["D"] * 2)
        if self.pbar["value"] >= 100:
            self.pbar["value"] = 0
            self._complete_action()
            self.quest_step_index += 1
            self._advance_to_next_step()
        else:
            self.pbar["value"] += 2
        self.root.after(speed, self.run_game_loop)

    def _complete_action(self):
        atype  = self.current_action_type
        flavor = random.choice(ACTION_FLAVORS.get(atype, ["Did something."]))
        self.log_story(f"  {flavor}")

        if atype == "fight":
            self._resolve_fight()
        elif atype == "loot":
            gold = int(random.randint(10, 30) * (1 + self.char["stats"]["G"] * 0.02))
            self.char["gold"] += gold
            self._update_gold()
            self.log_story(f"    +{gold} gold")
            if random.random() < 0.55 + self.char["stats"]["L"] * 0.01:
                self._drop_item()
        elif atype == "return":
            self.char["hp"] = self.char["max_hp"]
            self.char["mp"] = self.char["max_mp"]
            self.log_story("    Fully healed.")
            self._update_char_panel()
        elif atype == "rest":
            h = random.randint(3, 8)
            self.char["hp"] = min(self.char["max_hp"], self.char["hp"] + h)
            self.char["mp"] = min(self.char["max_mp"], self.char["mp"] + h)
            self.log_story(f"    Recovered {h} HP/MP.")
            self._update_char_panel()
        elif atype == "travel":
            if random.random() < 0.08:
                g = random.randint(1, 6)
                self.char["gold"] += g
                self._update_gold()
                self.log_story(f"    Found {g} gold on the road!")
        elif atype in ("search","locate","scout","investigate",
                        "gather","escort","inspect","collect","speak"):
            if random.random() < 0.30:
                xp = random.randint(2, 6)
                self._gain_xp(xp)
                self.log_story(f"    +{xp} XP")
        elif atype == "sell":
            self._sell_one_item()

    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    #  COMBAT & DEATH
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    def _resolve_fight(self):
        if random.random() < 0.04 + self.char["stats"]["L"] * 0.005:
            self.log_story("    DODGE! Took no damage.")
        else:
            raw  = random.randint(3, 10)
            mit  = min(0.60, self.char["stats"]["R"] * 0.03)
            dmg  = max(1, int(raw * (1 - mit)))
            self.char["hp"] -= dmg
            self.log_story(f"    Took {dmg} damage. "
                           f"({max(0,self.char['hp'])}/{self.char['max_hp']} HP)")
            self._update_char_panel()
            if self.char["hp"] <= 0:
                self.char["hp"] = 0
                self._update_char_panel()
                self._trigger_death()
                return

        xp = random.randint(8, 20) + self.char["stats"]["I"] // 5
        self._gain_xp(xp)
        self.log_story(f"    +{xp} XP")
        if random.random() < 0.25 + self.char["stats"]["L"] * 0.01:
            self._drop_item()

    def _trigger_death(self):
        if self._dead:
            return
        self._dead = True
        self.char["deaths"] += 1
        for line in DEATH_SEQUENCE:
            self.log_story(line, "death")
        lost = len(self.char["inventory"])
        self.char["inventory"].clear()
        lg = self.char["gold"] // 2
        self.char["gold"] = max(0, self.char["gold"] - lg)
        self.log_story(f"  Lost {lost} items and {lg} gold.", "death")
        self._update_gold()
        self._refresh_inv_list()
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
    def _sell_one_item(self):
        """Sell one item from inventory; called once per sell action step."""
        if not self.char["inventory"]:
            self.log_story("    Nothing left to sell. Browsed awkwardly.", "vendor")
            return
        item  = self.char["inventory"].pop(0)
        value = item_sell_value(item, self.char["stats"]["L"])
        self.char["gold"] += value
        self._update_gold()
        self._refresh_inv_list()
        self.log_story(f"  [SOLD] {item_display(item)}  ➜  {value} gold", "vendor")

        hp_missing = self.char["max_hp"] - self.char["hp"]
        mp_missing = self.char["max_mp"] - self.char["mp"]
        spent = 0

        if hp_missing > 0:
            hp_heal = min(hp_missing, value // 2)
            hp_cost = hp_heal
            spent += hp_cost
            self.char["hp"] = min(self.char["max_hp"], self.char["hp"] + hp_heal)
            self.log_story(f"    Recovered {hp_heal} HP ({hp_cost} gold)")

        if mp_missing > 0 and value - spent > 0:
            mp_heal = min(mp_missing, (value - spent) // 2)
            mp_cost = mp_heal
            self.char["mp"] = min(self.char["max_mp"], self.char["mp"] + mp_heal)
            self.log_story(f"    Recovered {mp_heal} MP ({mp_cost} gold)")
            spent += mp_cost

        self.char["gold"] -= spent
        remaining = self.char["gold"]

        for slot in EQUIP_SLOTS:
            if remaining <= 0:
                break
            item = self.char["equip"].get(slot)
            if not item:
                continue
            cost = upgrade_cost(item)
            if remaining >= cost:
                remaining -= cost
                item["upgrade"] = item.get("upgrade", 0) + 1
                item["bonus"] = item.get("bonus", 1) + 1
                item["power"] = item.get("power", 1) + 1
                self.log_story(f"    UPGRADE: {item_display(item)} now +{item['upgrade']}")

        self.char["gold"] = remaining
        self._update_gold()
        self._refresh_inv_list()
        self._update_char_panel()
        self._refresh_equip_list()

    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    #  ITEMS
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    def _drop_item(self):
        item  = generate_item(self.char["lvl"])
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
        if len(self.char["inventory"]) >= INVENTORY_MAX:
            self.log_story(f"  [!] Bag full ({INVENTORY_MAX} items) — vendor visit queued.", "vendor")

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

    def _refresh_story_tree(self):
        self.story_tree.delete(*self.story_tree.get_children())
        if not self.char["prologue_done"]:
            self.story_tree.insert("", "end", values=("☐", "Prologue"))
        else:
            self.story_tree.insert("", "end", values=("☑", "Prologue"))
            for i in range(1, self.char["current_act"]):
                name = ACT_NAMES[min(i - 1, len(ACT_NAMES) - 1)]
                self.story_tree.insert("", "end", values=("☑", f"Act {i}: {name}"))
            act = self.char["current_act"]
            name = ACT_NAMES[min(act - 1, len(ACT_NAMES) - 1)]
            self.story_tree.insert("", "end", values=("☐", f"Act {act}: {name}"))

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

    def _update_act_bars(self):
        if self.char["prologue_done"]:
            self.act_label.config(text=f"Act {self.char['current_act']}: {ACT_NAMES[min(self.char['current_act']-1, len(ACT_NAMES)-1)]}")
            self.act_pbar["maximum"] = QUESTS_PER_ACT
            self.act_pbar["value"] = self.char["act_quests_done"]
        else:
            self.act_label.config(text="Prologue")
            self.act_pbar["maximum"] = PROLOGUE_COMPLETE
            self.act_pbar["value"] = self.char["quests_completed"]

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
                self.spell_list.insert(tk.END, new_spell)
                self.log_story(f"  Learned: {new_spell}", "level")
        self._refresh_stat_tree()

    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    #  UI HELPERS
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    def _update_char_panel(self):
        c = self.char
        self.info_label.config(
            text=(f"Name: {c['name']}\n"
                  f"Race: {c['race']}\n"
                  f"Class: {c['class']}\n"
                  f"Lv: {c['lvl']} | Deaths: {c['deaths']}"))
        def pct(v, m): return int(100 * v / m) if m else 0
        self.hp_bar["value"] = pct(c["hp"],  c["max_hp"])
        self.hp_lbl.config(text=f"{c['hp']}/{c['max_hp']}")
        self.mp_bar["value"] = pct(c["mp"],  c["max_mp"])
        self.mp_lbl.config(text=f"{c['mp']}/{c['max_mp']}")
        self.xp_bar["value"] = pct(c["exp"], c["exp_next"])
        self.xp_lbl.config(text=f"{c['exp']}/{c['exp_next']}")
        enc = len(c.get("inventory", []))
        self.enc_bar["value"] = enc
        self.enc_lbl.config(text=f"{enc}/{INVENTORY_MAX}")

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