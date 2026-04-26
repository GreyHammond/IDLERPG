# Changelog — I.D.L.E.R.P.G.

All notable changes to this project are documented here.
Format follows [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

---

## [v1.4] — Age of Magic

### Added

**Spell System — Core**
- `SPELL_DEFINITIONS` — 56 fully-defined spells replacing the old bare string lists. Each spell carries `mp_cost`, `duration`, `effect_type`, `magnitude`, `stat`, `tier`, and `description`.
- `SPELL_BY_NAME` — O(1) lookup dict auto-built from definitions.
- `TIERED_SPELLS` — Auto-rebuilt from `SPELL_DEFINITIONS`; generator logic unchanged.
- `char["active_effects"]` — New runtime list tracking all running spell effects. Each entry stores spell name, effect type, magnitude, ticks remaining, and stat delta for safe revert.
- `tick_active_effects()` — Decrements ticks each action; reverts expired stat buffs by stored delta.
- `has_active_effect()` — Guards against recasting the same effect type while it is still running.
- `cast_chance()` — Class-affinity gating: primary stat spells cast at full rate, secondary at 50%, off-stat at 16%.
- `SPELL_CAST_WINDOWS` — Dict mapping each effect type to the action types it is permitted to fire during.
- `_attempt_spell_cast()` — Priority queue: HP regen if low → MP regen if low → expired buffs → opportunistic. MP floor: no non-regen spells below 25% MP.
- `_fire_spell()` — Dispatches cast to the correct effect path, logs with ✦ prefix, updates UI.

**10 Effect Categories**
- `xp_boost` — % XP bonus while active.
- `gold_boost` — % gold bonus while active.
- `stat_buff` — Directly raises `char["stats"][key]`; cleanly reverted on expiry or death.
- `hp_regen` — Restores HP each tick while active.
- `mp_regen` — Restores MP each tick while active.
- `combat_damage` — Stored as `pending_spell_damage`; consumed in `_resolve_fight`.
- `combat_defense` — Reduces incoming damage by magnitude fraction in `_resolve_fight`.
- `loot_quality` — Adds power/bonus bump to items in `_drop_item` while active.
- `transmute` — Converts oldest inventory item to gold at efficiency rate.
- `craft` — Tier III: reforges weakest item into an Arcane-Forged version at `level+2`.

**Transmutation**
- `transmute_efficiency()` — Logarithmic formula: `tier_base + 0.18 × log(1 + I/20)`. Hard cap 0.92.
- `_transmute_one_item()` — Converts item at efficiency rate, logs rate and gold lost vs market.
- Encumbrance path now checks `_can_transmute_in_field()` before defaulting to market. Roll chance scales by tier (Minor 40% → Tier III 88%).
- `_inject_transmute_quest()` — Builds a queue of `transmute` steps instead of a market trip.

**Arcane Crafting (Tier III)**
- `_craft_one_item()` — Targets weakest inventory item, generates `level+2` replacement named "Arcane-Forged …", auto-equips if better.

**UI**
- Spell tooltip on mouse-over: shows name, tier, MP cost, duration, effect type, full description.
- `[ACTIVE Nt]` live countdown in spell list, updated every action.
- `_flash_cast()` — Story log and MP bar flash bright on cast, revert after 200ms.
- Creation screen column 3: spell preview panel showing starting spells for each class, updates live as class is selected.
- Level-up spell log now shows tier and MP cost.
- `transmute` added to `ACTION_LABELS` and `ACTION_FLAVORS`.

**Lifecycle Safety**
- Death reverts all active stat buffs before clearing `active_effects`.
- Prestige clears `active_effects`, `pending_spell_damage`, `_pending_transmute_tier`.
- Save/load: `pending_spell_damage` popped on load; `active_effects` defaults to `[]` for old saves.

**Achievements (31 new — magic category)**
- `spells_learned` — 6 tiers (1 → 56, "The Omnimancer")
- `spells_cast` — 7 tiers (1 → 5,000, "The Eternal Caster")
- `transmutes_performed` — 5 tiers (1 → 500, "The Philosopher")
- `items_crafted` — 4 tiers (1 → 25, "The Architect")
- `status_effects_applied` — 4 tiers (10 → 500)
- `ticks_under_effect` — 5 tiers (50 → 5,000, "The Living Spell")

**Balance**
- MP costs increased: Minor +2, Major +4, Tier II +7, Tier III +12.

---

## [v1.3] — Age of Heroes

### Added
- Full achievement system with 148 achievements across wealth, combat, quests, levels, prestige, and trading categories.
- Prestige title system — stacked titles built with each universe reset, with full history tooltip.
- Bug fix: item bonuses now tracked and reverted correctly on unequip; repeated unequip no longer drives stats negative.
- 20 playable races and 20 classes with unique stat modifiers.
- Dynamic grammar-based item naming ("Rusty Dagger" → "The Harbinger, the Vorpal Steel Dagger of Whispers").
- Multi-slot equipment system (Weapon, Shield, Helm, Body, Legs, Ring, Amulet).
- Death sequence with ghost mechanics, respawn, and inventory/gold loss.
- Encumbrance system — auto-returns to town at 100% capacity.
- 100-act cycle with boss quests, universe reset, and infinite prestige loop.
- Dev menu (force reset, level scaling, gold/XP injection).

---

## [v1.2] — Lorekeeper

### Added
- CHANGELOG introduced.
- Spell pool system (Minor → Major → Tier II → Tier III) based on class stat affinity.
- Spell list UI panel with per-level unlock every 5 levels.
- 98 unique act names.
- Action flavor text system (`ACTION_FLAVORS`).
- Grammar-based loot prefix/suffix/material/quality system.

---

## [v1.1]

### Added
- Persistent save/load (JSON).
- Multiple equipment slots.
- Market trip system with sell, restore, and upgrade steps.
- Progress bar UI for quest and action timing.

---

## [v1.0] — Initial Release

### Added
- Core idle loop: quests, actions, XP, levelling.
- Character creation with stat rolling (4d6 drop lowest).
- Basic inventory and gold system.
- Tkinter UI with story log, stat panel, and equipment list.
