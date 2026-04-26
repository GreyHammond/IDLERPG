"""
I.D.L.E.R.P.G. Achievement Definitions

MIT License - Community editable
https://github.com/anomalyco/idle-rpg

Achievement Types:
- threshold: Numeric milestone (e.g., 1000 gold)
- counter: Action count milestone (e.g., 100 fights)
- special: Complex condition (e.g., all equipment legendary)
"""

from typing import Dict, List, Any, Callable

# Scientific notation scales
SCALES = [
    "", "K", "M", "B", "T", "Qa", "Qi", "Sx", "Sp", "Oc", "No", "Dc",
    "Ud", "Dd", "Td", "Qdd", "Sxd", "Spd", "Ocd", "Nxd", "Vg"
]

def format_large(num: int) -> str:
    """Format large numbers: 1000 → 1K, 1000000 → 1M"""
    if num < 0:
        return str(num)
    if num < 1000:
        return str(num)
    
    import math
    magnitude = int(math.log10(num))
    scale_idx = min(magnitude // 3, len(SCALES) - 1)
    scaled = num / (10 ** (scale_idx * 3))
    return f"{scaled:.1f}{SCALES[scale_idx]}"

# Achievement categories
CAT_WEALTH = "wealth"
CAT_COMBAT = "combat"
CAT_TRADING = "trading"
CAT_PROGRESS = "progress"
CAT_PRESTIGE = "prestige"
CAT_LEVEL = "level"
CATQUESTS = "quests"
CAT_EQUIP = "equipment"
CAT_MAGIC = "magic"

# ══════════════════════════════════════════════════════════════════════════════
# ACHIEVEMENT DEFINITIONS
# ══════════════════════════════════════════════════════════════════════════════

def _generate_gold_achievements() -> List[Dict]:
    """Generate gold accumulation achievements"""
    thresholds = [1000, 5000, 10000, 25000, 50000, 100000, 250000, 500000, 1000000,
                   2500000, 5000000, 10000000, 25000000, 50000000, 100000000, 250000000,
                   500000000, 1000000000, 2500000000, 5000000000, 10000000000,
                   25000000000, 50000000000, 100000000000, 250000000000, 500000000000]
    achievements = []
    names = [
        "First 1,000 Gold", "First 5,000 Gold", "First 10,000 Gold", "First 25,000 Gold",
        "First 50,000 Gold", "First 100,000 Gold", "First 250,000 Gold", "First 500,000 Gold",
        "First Million Gold", "First 2.5 Million Gold", "First 5 Million Gold",
        "First 10 Million Gold", "First 25 Million Gold", "First 50 Million Gold",
        "First 100 Million Gold", "First 250 Million Gold", "First 500 Million Gold",
        "Billionaire", "First 2.5 Billion Gold", "First 5 Billion Gold",
        "First 10 Billion Gold", "First 25 Billion Gold", "First 50 Billion Gold",
        "First 100 Billion Gold", "First 250 Billion Gold", "First 500 Billion Gold"
    ]
    for i, (threshold, name) in enumerate(zip(thresholds, names)):
        achievements.append({
            "id": f"gold_{i+1}",
            "name": name,
            "desc": f"Accumulate {format_large(threshold)} gold",
            "category": CAT_WEALTH,
            "stat": "gold_earned",
            "threshold": threshold
        })
    return achievements

def _generate_action_achievements() -> List[Dict]:
    """Generate action count achievements"""
    achievements = []
    
    # Travel achievements
    travel_thresholds = [100, 500, 1000, 5000, 10000, 50000, 100000, 500000, 1000000]
    travel_names = ["Wayfarer", "Roamer", "Wanderer", "Explorer", "Adventurer", "Trailblazer", "Pathfinder", "Legendary Explorer", "Infinite Traveler"]
    for i, (t, n) in enumerate(zip(travel_thresholds, travel_names)):
        achievements.append({
            "id": f"travel_{i+1}",
            "name": n,
            "desc": f"Wander {format_large(t)} times",
            "category": CAT_PROGRESS,
            "stat": "actions_travel",
            "threshold": t
        })
    
    # Fight achievements
    fight_thresholds = [10, 50, 100, 500, 1000, 5000, 10000, 50000, 100000, 500000, 1000000]
    fight_names = ["First Blood", "Monster Hunter", "Combat Initiate", "Battler", "Warrior", "Champion", "Veteran", "Elite Warrior", "Master of Arms", "Legendary Hero", "Mythic Slayer"]
    for i, (t, n) in enumerate(zip(fight_thresholds, fight_names)):
        achievements.append({
            "id": f"fight_{i+1}",
            "name": n,
            "desc": f"Engage in {format_large(t)} battles",
            "category": CAT_COMBAT,
            "stat": "actions_fight",
            "threshold": t
        })
    
    # Loot achievements
    loot_thresholds = [10, 50, 100, 500, 1000, 5000, 10000, 50000, 100000]
    loot_names = ["First Find", "Scrounger", "Looter", "Plunderer", "Treasure Hunter", "Rich Finder", "Booty Baron", "Treasure Magnate", "Master of Riches"]
    for i, (t, n) in enumerate(zip(loot_thresholds, loot_names)):
        achievements.append({
            "id": f"loot_{i+1}",
            "name": n,
            "desc": f"Loot {format_large(t)} times",
            "category": CAT_PROGRESS,
            "stat": "actions_loot",
            "threshold": t
        })
    
    # Search achievements
    search_thresholds = [10, 50, 100, 500, 1000, 5000, 10000, 50000]
    search_names = ["Seeker", "Searcher", " Investigator", "Finder", "Discovery Expert", "Treasure Seeker", "Master Seeker", "Grand Discovery Expert"]
    for i, (t, n) in enumerate(zip(search_thresholds, search_names)):
        achievements.append({
            "id": f"search_{i+1}",
            "name": n,
            "desc": f"Search {format_large(t)} times",
            "category": CAT_PROGRESS,
            "stat": "actions_search",
            "threshold": t
        })
    
    # Rest achievements
    rest_thresholds = [10, 50, 100, 500, 1000, 5000, 10000]
    rest_names = ["Rested Once", "Nap Enthusiast", "Rest Seeker", "Champions Rest", "Relaxation Master", "Rest Legend", "Grand Master of Rest"]
    for i, (t, n) in enumerate(zip(rest_thresholds, rest_names)):
        achievements.append({
            "id": f"rest_{i+1}",
            "name": n,
            "desc": f"Rest {format_large(t)} times",
            "category": CAT_PROGRESS,
            "stat": "actions_rest",
            "threshold": t
        })
    
    return achievements

def _generate_sell_achievements() -> List[Dict]:
    """Generate trading/selling achievements"""
    thresholds = [1, 5, 10, 25, 50, 100, 250, 500, 1000, 2500, 5000, 10000, 25000, 50000, 100000]
    names = [
        "First Sale", "Peddler", "Merchant Initiate", "Trader", "Merchant", "Senior Merchant",
        "Expert Merchant", "Master Merchant", "Trade Master", "Trade Expert", "Cartel Member",
        "Trade Baron", "Trade Prince", "Trade King", "Cartel King", "Trade Emperor"
    ]
    achievements = []
    for i, (t, n) in enumerate(zip(thresholds, names)):
        achievements.append({
            "id": f"sell_{i+1}",
            "name": n,
            "desc": f"Sell {format_large(t)} items",
            "category": CAT_TRADING,
            "stat": "items_sold",
            "threshold": t
        })
    return achievements

def _generate_reset_achievements() -> List[Dict]:
    """Generate universe reset achievements"""
    thresholds = [1, 5, 10, 25, 50, 100, 250, 500, 1000, 2500, 5000, 10000]
    names = [
        "Rebirth", "Five Timer", "Quantum Leaper", "Cycle Breaker", "Dimension Jumper",
        "Universe Reaper", "Reality Shifter", "Chronos Walker", "Time Lord", "Eternal Being",
        "Infinity Walker", "God Tier"
    ]
    achievements = []
    for i, (t, n) in enumerate(zip(thresholds, names)):
        achievements.append({
            "id": f"reset_{i+1}",
            "name": n,
            "desc": f"Reset the universe {format_large(t)} times",
            "category": CAT_PRESTIGE,
            "stat": "world_resets",
            "threshold": t
        })
    return achievements

def _generate_level_achievements() -> List[Dict]:
    """Generate level milestones"""
    thresholds = [5, 10, 25, 50, 75, 100, 150, 200, 250, 300, 400, 500, 750, 1000]
    names = [
        "Level 5", "Double Digits", "Quarter Century", "Half Century", "Three Quarter",
        "Centurion", "Level 150", "Two Centuries", "Level 250", "Three Hundred",
        "Four Hundred", "Five Hundred", "Seven Fifty", "Grand Master"
    ]
    achievements = []
    for i, (t, n) in enumerate(zip(thresholds, names)):
        achievements.append({
            "id": f"lvl_{i+1}",
            "name": n,
            "desc": f"Reach level {t}",
            "category": CAT_LEVEL,
            "stat": "max_level",
            "threshold": t
        })
    return achievements

def _generate_quest_achievements() -> List[Dict]:
    """Generate quest completion achievements"""
    thresholds = [1, 5, 10, 25, 50, 100, 250, 500, 1000, 2500, 5000, 10000]
    names = [
        "First Quest", "Five Quests", "Adventurer", "Veteran", "Seasoned Adventurer",
        "Quest Master", "Quest Legend", "Grand Quest Master", "Epic Adventurer",
        "Legendary Quester", "Ultimate Quester", "Mythic Quester"
    ]
    achievements = []
    for i, (t, n) in enumerate(zip(thresholds, names)):
        achievements.append({
            "id": f"quest_{i+1}",
            "name": n,
            "desc": f"Complete {format_large(t)} quests",
            "category": CATQUESTS,
            "stat": "quests_completed",
            "threshold": t
        })
    return achievements

def _generate_kill_achievements() -> List[Dict]:
    """Generate enemy kill achievements"""
    thresholds = [10, 50, 100, 500, 1000, 5000, 10000, 50000, 100000, 500000, 1000000]
    names = [
        "Monster Slayer", "Creature Hunter", "Beast Killer", "Demon Slayer",
        "Darkness Vanquisher", "Evil Eradicator", "Champion of Light", "Supreme Bane",
        "Ultimate Nemesis", "Mythic Bane", "Legendary Bane"
    ]
    achievements = []
    for i, (t, n) in enumerate(zip(thresholds, names)):
        achievements.append({
            "id": f"kill_{i+1}",
            "name": n,
            "desc": f"Defeat {format_large(t)} enemies",
            "category": CAT_COMBAT,
            "stat": "enemies_killed",
            "threshold": t
        })
    return achievements

def _generate_progress_achievements() -> List[Dict]:
    """Generate progress bar tick achievements"""
    thresholds = [100, 500, 1000, 5000, 10000, 50000, 100000, 500000, 1000000, 5000000]
    names = [
        "Progress Initiate", "Stepping Up", "Getting Somewhere", "Making Progress",
        "Steady Advance", "Moving Forward", "Rapid Progress", "Speeding Along",
        "Fast Track", "Infinite Progress"
    ]
    achievements = []
    for i, (t, n) in enumerate(zip(thresholds, names)):
        achievements.append({
            "id": f"tick_{i+1}",
            "name": n,
            "desc": f"Progress {format_large(t)} times",
            "category": CAT_PROGRESS,
            "stat": "progress_ticks",
            "threshold": t
        })
    return achievements

def _generate_special_achievements() -> List[Dict]:
    """Generate special condition achievements"""
    achievements = [
        {
            "id": "full_equip",
            "name": "Fully Equipped",
            "desc": "Fill all 7 equipment slots",
            "category": CAT_EQUIP,
            "special": "all_slots_filled"
        },
        {
            "id": "first_boss",
            "name": "Boss Slayer",
            "desc": "Defeat your first boss",
            "category": CAT_COMBAT,
            "stat": "bosses_defeated",
            "threshold": 1
        },
        {
            "id": "died_once",
            "name": "Near Death Experience",
            "desc": "Die for the first time (It happens)",
            "category": CAT_COMBAT,
            "stat": "times_died",
            "threshold": 1
        },
        {
            "id": "gold_spent_1m",
            "name": "Big Spender",
            "desc": "Spend 1,000,000 gold at vendors",
            "category": CAT_TRADING,
            "stat": "gold_spent",
            "threshold": 1000000
        }
    ]
    return achievements

def _generate_magic_achievements() -> List[Dict]:
    """Generate spell-casting and magic system achievements."""
    achievements = []

    # ── Spells Learned ────────────────────────────────────────────────────
    learned_tiers = [
        (1,  "First Spell",        "Learn your first spell or skill."),
        (3,  "Apprentice Mage",    "Learn 3 spells."),
        (5,  "Journeyman Mage",    "Learn 5 spells."),
        (10, "Adept of the Arcane","Learn 10 spells."),
        (20, "Master of Spells",   "Learn 20 spells."),
        (56, "The Omnimancer",     "Learn every spell and skill in existence."),
    ]
    for threshold, name, desc in learned_tiers:
        achievements.append({
            "id": f"spells_learned_{threshold}",
            "name": name,
            "desc": desc,
            "category": CAT_MAGIC,
            "stat": "spells_learned",
            "threshold": threshold,
        })

    # ── Spells Cast ───────────────────────────────────────────────────────
    cast_tiers = [
        (1,    "First Cast",          "Cast your first spell."),
        (10,   "Minor Caster",        "Cast 10 spells."),
        (50,   "Practiced Hand",      "Cast 50 spells."),
        (100,  "Spell Slinger",       "Cast 100 spells."),
        (500,  "Arcane Engine",       "Cast 500 spells."),
        (1000, "Living Spellbook",    "Cast 1,000 spells."),
        (5000, "The Eternal Caster",  "Cast 5,000 spells."),
    ]
    for threshold, name, desc in cast_tiers:
        achievements.append({
            "id": f"spells_cast_{threshold}",
            "name": name,
            "desc": desc,
            "category": CAT_MAGIC,
            "stat": "spells_cast",
            "threshold": threshold,
        })

    # ── Transmutations ────────────────────────────────────────────────────
    transmute_tiers = [
        (1,   "Field Alchemist",      "Transmute an item in the field for the first time."),
        (10,  "The Travelling Forge", "Transmute 10 items in the field."),
        (50,  "Gold from Dross",      "Transmute 50 items in the field."),
        (100, "Midas Protocol",       "Transmute 100 items — why even visit a market?"),
        (500, "The Philosopher",      "Transmute 500 items. A true master of conversion."),
    ]
    for threshold, name, desc in transmute_tiers:
        achievements.append({
            "id": f"transmutes_{threshold}",
            "name": name,
            "desc": desc,
            "category": CAT_MAGIC,
            "stat": "transmutes_performed",
            "threshold": threshold,
        })

    # ── Items Crafted (Tier III) ──────────────────────────────────────────
    craft_tiers = [
        (1,  "First Reforge",     "Use a Tier III spell to craft a superior item."),
        (5,  "The Smith Arcane",  "Craft 5 items with Tier III spells."),
        (10, "Reforged World",    "Craft 10 items — reality bends to your will."),
        (25, "The Architect",     "Craft 25 items. You no longer find loot — you make it."),
    ]
    for threshold, name, desc in craft_tiers:
        achievements.append({
            "id": f"crafted_{threshold}",
            "name": name,
            "desc": desc,
            "category": CAT_MAGIC,
            "stat": "items_crafted",
            "threshold": threshold,
        })

    # ── Status Effects Applied ────────────────────────────────────────────
    effect_tiers = [
        (10,  "Buffed Up",            "Apply 10 status effects."),
        (50,  "Walking Enchantment",  "Apply 50 status effects."),
        (100, "Aura Weaver",          "Apply 100 status effects."),
        (500, "The Perpetual Buffer", "Apply 500 status effects."),
    ]
    for threshold, name, desc in effect_tiers:
        achievements.append({
            "id": f"effects_applied_{threshold}",
            "name": name,
            "desc": desc,
            "category": CAT_MAGIC,
            "stat": "status_effects_applied",
            "threshold": threshold,
        })

    # ── Ticks Under Effect ────────────────────────────────────────────────
    tick_tiers = [
        (50,   "Briefly Blessed",       "Spend 50 action-ticks under an active effect."),
        (200,  "Sustained Caster",      "Spend 200 action-ticks under an active effect."),
        (500,  "Perpetual Enchantment", "Spend 500 ticks under active effects."),
        (1000, "Always Buffed",         "Spend 1,000 ticks under active effects."),
        (5000, "The Living Spell",      "Spend 5,000 ticks under active effects. You practically are magic."),
    ]
    for threshold, name, desc in tick_tiers:
        achievements.append({
            "id": f"ticks_buffed_{threshold}",
            "name": name,
            "desc": desc,
            "category": CAT_MAGIC,
            "stat": "ticks_under_effect",
            "threshold": threshold,
        })

    return achievements


# ══════════════════════════════════════════════════════════════════════════════
# MASTER ACHIEVEMENT LIST
# ══════════════════════════════════════════════════════════════════════════════

ACHIEVEMENTS = (
    _generate_gold_achievements() +
    _generate_action_achievements() +
    _generate_sell_achievements() +
    _generate_reset_achievements() +
    _generate_level_achievements() +
    _generate_quest_achievements() +
    _generate_kill_achievements() +
    _generate_progress_achievements() +
    _generate_special_achievements() +
    _generate_magic_achievements()
)

# Create lookup dict
ACHIEVEMENT_LOOKUP = {ach["id"]: ach for ach in ACHIEVEMENTS}

# Reward titles (future use)
ACHIEVEMENT_TITLES = {
    "gold_1": "Of Modest Means",
    "gold_9": "Wealthy",
    "gold_13": "Rich",
    "sell_5": "Trader",
    "sell_10": "Merchant",
    "reset_1": "Reborn",
    "reset_3": "Quantum",
    "kill_3": "Slayer",
    "quest_5": "Adventurer",
    "quest_10": "Veteran",
}

# ══════════════════════════════════════════════════════════════════════════════
# HELPER FUNCTIONS
# ══════════════════════════════════════════════════════════════════════════════

def get_achievements_by_category(category: str) -> List[Dict]:
    """Get all achievements in a category"""
    return [a for a in ACHIEVEMENTS if a.get("category") == category]

def get_achievement(id: str) -> Dict:
    """Get achievement by ID"""
    return ACHIEVEMENT_LOOKUP.get(id)

def get_unlocked_count(unlocked_ids: List[str]) -> int:
    """Count unlocked achievements"""
    return len(unlocked_ids)