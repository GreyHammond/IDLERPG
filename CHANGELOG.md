# Changelog

All notable changes to I.D.L.E.R.P.G. will be documented in this file.

## v1.3 - Age of Heroes

### Added
- **Achievement System** — 148 achievements across 8 categories, tracked persistently in the character save file:
  - **Wealth** — Gold accumulation milestones from 1K → 500B (26 tiers)
  - **Combat** — Enemies killed and fights engaged (22 tiers)
  - **Trading** — Items sold from 1 → 100K (15 tiers)
  - **Progress** — Progress bar ticks, travel steps, loot runs, searches, and rest actions (43 tiers)
  - **Prestige** — Universe resets from 1 → 10,000 (12 tiers)
  - **Level** — Level milestones from 5 → 1,000 (14 tiers)
  - **Quests** — Quests completed from 1 → 10,000 (12 tiers)
  - **Equipment** — Fill all equipment slots (1 achievement, more planned)

- **`achievements.py`** — Standalone community-editable definitions file (MIT license):
  - All achievement data lives here — add new milestones without touching game logic
  - `format_large()` helper for human-readable large numbers (1K, 1M, 1B, 500B...)
  - `ACHIEVEMENT_TITLES` dict for future title reward integration
  - Helper functions: `get_achievements_by_category()`, `get_achievement()`, `get_unlocked_count()`

- **Toast Notification System** — Smooth animated popup on achievement unlock:
  - Fades in (bottom-right corner), holds 2.8 seconds, fades out
  - Queues correctly — multiple unlocks don't overlap
  - Displays achievement name, description, and gold trophy icon
  - Never crashes the game if the UI is in an unexpected state

- **Achievement Stat Tracking** — Cumulative stats recorded in `char["achievements"]["stats"]`:
  - Tracked per action: `progress_ticks`, `actions_travel`, `actions_fight`, `actions_loot`, `actions_search`, `actions_rest`
  - Tracked per event: `gold_earned`, `gold_spent`, `enemies_killed`, `items_sold`, `quests_completed`, `bosses_defeated`, `world_resets`, `times_died`, `max_level`, `upgrades_total`
  - `max_level` persists across universe resets — tracks highest level ever reached
  - `quests_completed` in achievement stats is cumulative (unlike `char["quests_completed"]` which resets on prestige)

- **Save Compatibility** — `start_game_from_save()` backfills all achievement stat keys so existing saves load without errors

- **STORY Scrollbar** — Vertical scrollbar for navigating long act histories:
  - Supports scrolling through all completed acts across multiple prestige cycles
  - STORY now shows all prior cycles as completed when prestige > 0
  - Act 1-99 → ☑, Act 100 → ☐, then Act 101-199 → ☐, etc.

- **`_refresh_story_tree()` Overhaul** — Shows complete prestige history:
  - Loop through all prior prestige cycles: `for prior_pr in range(pr)`
  - Each prior cycle shows Acts 1-99 as ☑, Act 100 as ☑
  - Current cycle shows up to current_act as ☑, current act as ☐

- **Act Name Roman Numerals** — `get_act_name()` updated for multi-prestige:
  - Formula: `cycle = ((act_index - 1) // 100) + 1`
  - Displays: "The Beginning II", "Defend the Hold III", etc.
  - Act 100/200/300 keep "Resetting the Universe" (no roman numeral)

- **Quest Completion Guard** — Prevents duplicate quest entries:
  - Added `_quest_completing` flag to prevent double completion
  - Flag resets after new quest starts in `_animate_new_quest()`

- **Prestige Title System** — Additive titles that build with each universe reset:
  - 4-part title progression per prestige: Noun → Adj+Noun → Adj+Noun+Suffix → Prefix+Adj+Noun+Suffix
  - After each P4 (position 4), a new persona starts with comma separation
  - Titles stored in arrays: 50 nouns, 50 adjectives, 22 suffixes, 36 prefixes

- **Title Functions**:
  - `get_current_title(prestige_level)` — returns single title for display
  - `get_full_title(prestige_level)` — returns full stacked title for tooltip

- **Title UI Display**:
  - Shows current title under character name, above race
  - Mouseover tooltip shows full stacked title history
  - Title updates on universe reset

- **Act Display with Prestige** — Shows full act number including prestige cycle:
  - Formula: `(prestige × 100) + current_act`
  - Act 101 shows as "The Beginning II", Act 202 shows as "The Beginning III"

- **Special Act 100 Quest** — After defeating Act 99 boss, triggers special "Resetting the Universe" quest:
  - 3 travel, 3 fight, 3 search, 1 return steps
  - After completing → triggers universe reset
  - Creates seamless prestige transition

- **Dev Menu** — Testing tools in File menu:
  - Force Universe Reset
  - Scale to Act 100
  - Add 10,000 Gold
  - Add 100 XP

- **Market Day Overhaul** — Individual step-by-step market actions:
  - Each sell: individual step (not all at once)
  - Each restore: individual step
  - Each upgrade attempt: individual step
  - Steps: travel → find_vendor → sell × inventory → restore → upgrade × 7 slots

### Fixed
- **Universe Reset Crash** — Removed invalid `self.update_idletasks()` call
- **Quest History Duplicates** — Fixed quests appearing twice in history after reset:
  - Now clears: `completed_quests`, `quests_completed`, quest state variables
  - Resets: `quest_template`, `quest_steps`, `quest_step_index`, `_current_quest_name`
  - Resets: `in_boss_quest`, `boss_attempts`
- **Character Panel Bars** — HP/MP/XP/ENC now update after each quest
- **Step Label Display** — Replaces underscores with spaces (e.g., "return_town" → "Return Town")
- **Duplicate Act Progress Bar** — Removed conflicting function definition
- **Act Progression Bar** — Fixed duplicate `_update_act_bars()` that was preventing prologue tracking from working correctly
- **Encumbrance Emergency Return** — Player at 100% encumbrance now triggers automatic return:
  - Check runs after each quest step completes
  - If 100%+, triggers emergency return sequence
  - Return time proportional to quest progress: `steps_remaining × 8 seconds`
  - Rejoin time also proportional: `steps_done × 8 seconds`
  - Blue progress bar shows entire return-and-resume cycle
  - Saves quest state and resumes from exact step where player left off
  - Protects against TclError: verifies pbar exists before access
- **`_dev_force_reset()` Fix** — Added `_refresh_story_tree()` call:
  - Now displays all 1-99 as ☑ when starting Act 100 special quest

### Technical Notes
- `_ach_stat(key, amount)` — increment helper used at every tracked event
- `_ach_stat_set(key, value)` — used for max-value tracking (e.g. `max_level`)
- `_check_achievements()` — called after fights, sells, quests, level-ups, resets, and deaths
- Graceful import fallback: if `achievements.py` is missing, game runs normally with no achievements

---

## v1.2 - Age of Ascension

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